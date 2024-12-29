from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from enum import Enum
from datetime import datetime
from sqlalchemy.orm import validates
from flask_bcrypt import Bcrypt
from flask import flash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///iescp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)

# Enum for roles
class RoleEnum(Enum):
    ADMIN = 'admin'
    SPONSOR = 'sponsor'
    INFLUENCER = 'influencer'

# Enum for campaign visibility
class VisibilityEnum(Enum):
    PUBLIC = 'public'
    PRIVATE = 'private'

# Enum for flagging reasons
class FlagReasonEnum(Enum):
    INAPPROPRIATE_CONTENT = 'Inappropriate Content'
    SPAM = 'Spam'
    OFFENSIVE_LANGUAGE = 'Offensive Language'
    OTHER = 'Other'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False, default=RoleEnum.INFLUENCER.value)
    flagged = db.Column(db.Boolean, default=False)  # Flagging status
    flag_reason = db.Column(db.String(150), nullable=True)  # Reason for flagging
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Account creation timestamp
    last_login = db.Column(db.DateTime, nullable=True)  # Last login timestamp (nullable)
    
    #Relationships
    sponsors = db.relationship("Sponsor", backref="user", lazy=True)
    influencers = db.relationship("Influencer", backref="user", lazy=True)
    
    # user_flags = db.relationship(
    #     "UserFlag", foreign_keys="UserFlag.flagged_by", backref="flagger", lazy=True
    # )
    # flagged_by_user_flags = db.relationship(
    #     "UserFlag", foreign_keys="UserFlag.user_id", backref="flagged_user", lazy=True
    # )
    # campaign_flags = db.relationship(
    #     "CampaignFlag",
    #     foreign_keys="CampaignFlag.flagged_by",
    #     backref="flagger",
    #     lazy=True,
    # )
    
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    

    def __repr__(self):
        return f'<User {self.username}>'

    def update_login_time(self):
        """Method to update the last login time"""
        self.last_login = datetime.utcnow()
        db.session.commit()

class Sponsor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key to User
    company_name = db.Column(db.String(150), nullable=False)  # Name of the company or individual sponsor
    industry = db.Column(db.String(150), nullable=False)  # Industry of the sponsor (e.g., Tech, Fashion)
    budget = db.Column(db.Float, nullable=False)  # The budget for campaigns
    status = db.Column(db.String(50), default="Pending")  # Sponsor status: Pending, Approved, etc.

    # Relationship with User table
    campaigns = db.relationship("Campaign", backref="sponsor", lazy=True)
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return f'<Sponsor {self.company_name}>'

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.id'), nullable=False)  # Foreign key to Sponsor
    name = db.Column(db.String(150), nullable=False)  # Campaign name
    description = db.Column(db.Text, nullable=False)  # Campaign description
    start_date = db.Column(db.Date, nullable=False)  # Campaign start date
    end_date = db.Column(db.Date, nullable=False)  # Campaign end date
    budget = db.Column(db.Float, nullable=False)  # Campaign budget
    visibility = db.Column(db.String(50), nullable=False, default=VisibilityEnum.PUBLIC.value)  # Campaign visibility
    goals = db.Column(db.Text, nullable=True)  # Campaign goals
    flagged = db.Column(db.Boolean, default=False)  # Flagging status
    flag_reason = db.Column(db.String(150), nullable=True)  # Reason for flagging
    status = db.Column(db.String(50), default="Active")  # Campaign status: Active, Completed, Paused

    # Relationship with Sponsor table
    ad_requests = db.relationship(
        "AdRequest", backref="campaign", lazy=True, cascade="all, delete-orphan"
    )
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    @validates("end_date")
    def validate_end_date(self, key, end_date):
        if self.start_date and end_date:
            if end_date < self.start_date:
                flash("End date must be greater than start date", "error")
        return end_date

    def __repr__(self):
        return f'<Campaign {self.name}>'

    def is_active(self):
        """Check if the campaign is currently active"""
        return self.status == 'Active' and self.start_date <= datetime.utcnow().date() <= self.end_date

class Influencer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key to User (influencer is a user)
    name = db.Column(db.String(150), nullable=False)  # Influencer's name
    category = db.Column(db.String(150), nullable=False)  # Influencer's category (e.g., Tech, Fashion)
    niche = db.Column(db.String(150), nullable=False)  # Influencer's niche (e.g., Gadgets, Lifestyle)
    reach = db.Column(db.Float, nullable=False)  # Reach (calculated by number of followers, engagements, etc.)

    # Relationship with User table
    ad_requests = db.relationship("AdRequest", backref="influencer", lazy=True)
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return f'<Influencer {self.name}>'

    def update_reach(self, followers_count, engagement_rate):
        """Method to calculate and update reach"""
        self.reach = followers_count * engagement_rate  # Example reach calculation
        db.session.commit()

class AdRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)  # Foreign key to Campaign
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.id'), nullable=False)  # Foreign key to Influencer
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.id'), nullable=False)  # Foreign key to Sponsor
    messages = db.Column(db.Text, nullable=True)  # Any messages exchanged between influencer and sponsor
    requirements = db.Column(db.Text, nullable=True)  # Ad request requirements from sponsor
    payment_amount = db.Column(db.Float, nullable=True)  # Original payment amount agreed by sponsor
    negotiated_payment_amount = db.Column(db.Float, nullable=True)  # Negotiated amount by influencer (if applicable)
    status = db.Column(db.String(50), nullable=False, default='Pending')  # Status: Pending, Accepted, Rejected
    negotiation_status = db.Column(db.String(50), nullable=True, default="Pending")  # Negotiation status: 'In Progress', 'Completed', 'Pending'

    # Relationships
    #influencer = db.relationship('Influencer', backref='ad_requests')  # Influencer's relationship with AdRequests
    sponsor = db.relationship('Sponsor', backref='ad_requests')  # Sponsor's relationship with AdRequests
    #campaign = db.relationship('Campaign', backref='ad_requests')  # Campaign's relationship with AdRequests

    def __repr__(self):
        return f'<AdRequest {self.id} - {self.status}>'

    def update_payment(self, new_payment_amount):
        """Method to update payment amount"""
        self.negotiated_payment_amount = new_payment_amount
        db.session.commit()
        
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
        
# User Flag model
class UserFlag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Flagged user
    #flagged_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # User who flagged
    reason = db.Column(db.String(150), nullable=False)  # Reason for flagging

    # Relationship to User (flagged user)
    flagged_user = db.relationship('User', foreign_keys=[user_id], backref=db.backref('flags_received', lazy=True))

    # Relationship to User (who flagged)
    #flagger = db.relationship('User', foreign_keys=[flagged_by], backref=db.backref('flags_given', lazy=True))

    def __repr__(self):
        return f'<UserFlag {self.user_id} flagged by {self.flagged_by} - {self.reason}>'

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "flagged_by": self.flagged_by,
            "reason": self.reason
        }

# Campaign Flag model
class CampaignFlag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)  # Campaign being flagged
    #flagged_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # User who flagged
    reason = db.Column(db.String(150), nullable=False)  # Reason for flagging

    # Relationship to Campaign (flagged campaign)
    campaign = db.relationship('Campaign', backref=db.backref('flags', lazy=True))

    # Relationship to User (who flagged the campaign)
    #flagger = db.relationship('User', foreign_keys=[flagged_by], backref=db.backref('campaign_flags', lazy=True))

    def __repr__(self):
        return f'<CampaignFlag {self.campaign_id} flagged by {self.flagged_by} - {self.reason}>'

    def to_dict(self):
        return {
            "id": self.id,
            "campaign_id": self.campaign_id,
            "flagged_by": self.flagged_by,
            "reason": self.reason
        }


# Initialize the database and create tables
with app.app_context():
    db.create_all()

    # Create admin if it doesn't exist
    if User.query.filter_by(username='admin').first() is None:
        admin_password = bcrypt.generate_password_hash('admin').decode('utf-8')
        admin = User(username='admin', email='admin@gmail.com', password=admin_password, role=RoleEnum.ADMIN.value)
        
        db.session.add(admin)
        db.session.commit()
    else:
        print('Admin already exists')
        
    # Create dummy users
    if User.query.filter_by(username='john_doe').first() is None:
        john_password = bcrypt.generate_password_hash('john123').decode('utf-8')
        john = User(username='john_doe', email='john.doe@example.com', password=john_password, role=RoleEnum.SPONSOR.value)
        db.session.add(john)
    
    if User.query.filter_by(username='jane_doe').first() is None:
        jane_password = bcrypt.generate_password_hash('jane123').decode('utf-8')
        jane = User(username='jane_doe', email='jane.doe@example.com', password=jane_password, role=RoleEnum.INFLUENCER.value)
        db.session.add(jane)

    db.session.commit()
    
    # Create dummy sponsors
    if Sponsor.query.filter_by(company_name='TechCorp').first() is None:
        tech_sponsor = Sponsor(user_id=1, company_name='TechCorp', industry='Technology', budget=10000.0, status='Approved')
        db.session.add(tech_sponsor)
    
    if Sponsor.query.filter_by(company_name='FashionPro').first() is None:
        fashion_sponsor = Sponsor(user_id=2, company_name='FashionPro', industry='Fashion', budget=15000.0, status='Pending')
        db.session.add(fashion_sponsor)

    db.session.commit()

    # Create dummy influencers
    if Influencer.query.filter_by(name='Alice Smith').first() is None:
        alice_influencer = Influencer(user_id=2, name='Alice Smith', category='Lifestyle', niche='Fashion', reach=15000)
        db.session.add(alice_influencer)
    
    if Influencer.query.filter_by(name='Bob Johnson').first() is None:
        bob_influencer = Influencer(user_id=3, name='Bob Johnson', category='Technology', niche='Gadgets', reach=20000)
        db.session.add(bob_influencer)

    db.session.commit()

    # Create dummy campaigns
    if Campaign.query.filter_by(name='Tech for All').first() is None:
        tech_campaign = Campaign(sponsor_id=1, name='Tech for All', description='A campaign promoting new technology.', start_date=datetime.utcnow().date(), end_date=datetime.utcnow().date(), budget=5000.0, visibility=VisibilityEnum.PUBLIC.value)
        db.session.add(tech_campaign)
    
    if Campaign.query.filter_by(name='Fashion for Everyone').first() is None:
        fashion_campaign = Campaign(sponsor_id=2, name='Fashion for Everyone', description='A campaign for promoting inclusive fashion.', start_date=datetime.utcnow().date(), end_date=datetime.utcnow().date(), budget=7000.0, visibility=VisibilityEnum.PRIVATE.value)
        db.session.add(fashion_campaign)

    db.session.commit()
    
    
    # Create dummy ad requests
    if AdRequest.query.filter_by(campaign_id=1, influencer_id=2, sponsor_id=1).first() is None:
        ad_request_1 = AdRequest(
            campaign_id=1,
            influencer_id=2,
            sponsor_id=1,
            messages="I'm interested in collaborating for the Tech for All campaign.",
            requirements="Promote tech gadgets and innovations through a series of Instagram posts.",
            payment_amount=500.0,
            negotiated_payment_amount=450.0,
            status="Pending",
            negotiation_status="In Progress"
        )
        db.session.add(ad_request_1)

    if AdRequest.query.filter_by(campaign_id=2, influencer_id=3, sponsor_id=2).first() is None:
        ad_request_2 = AdRequest(
            campaign_id=2,
            influencer_id=3,
            sponsor_id=2,
            messages="Excited to join the Fashion for Everyone campaign!",
            requirements="Share posts on fashion trends and inclusivity, targeting diverse audiences.",
            payment_amount=700.0,
            negotiated_payment_amount=650.0,
            status="Pending",
            negotiation_status="In Progress"
        )
        db.session.add(ad_request_2)

    db.session.commit()

    print("Dummy data created!")
