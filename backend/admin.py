from flask import Blueprint, request, jsonify
from model import db, User, Sponsor, Campaign, AdRequest, Influencer, RoleEnum, UserFlag
from functools import wraps
from flask_cors import cross_origin
import jwt
from datetime import datetime, timedelta
from config import cache

admin = Blueprint("admin", __name__)
SECRET_KEY = 'your_secret_key'


# Token validation decorator
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"message": "Token is missing!"}), 403
        try:
            token = token.split(" ")[1]  # Get token from "Bearer <token>"
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.user = data
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired!"}), 403
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token!"}), 403
        return f(*args, **kwargs)
    return decorated_function


# Admin role validation decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.user.get('role') != RoleEnum.ADMIN.value:
            return jsonify({"message": "Unauthorized"}), 403
        return f(*args, **kwargs)
    return decorated_function



# Admin login route
@admin.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        token = jwt.encode({
            'user_id': user.id,
            'username': user.username,
            'role': user.role,
            'exp': datetime.utcnow() + timedelta(hours=1)
        }, SECRET_KEY, algorithm='HS256')
        user.update_login_time()  # Update last login time
        db.session.commit()
        return jsonify({"token": token, "role": user.role}), 200
    return jsonify({"message": "Invalid credentials"}), 401


# Admin dashboard data route
@admin.route("/dashboard/data", methods=["GET"])
@cross_origin()
@token_required
@admin_required
@cache.cached(key_prefix='dashboard_data')
def dashboard_data():
    try:
        data = {
            "total_users": User.query.count(),
            "total_sponsors": Sponsor.query.count(),
            "total_campaigns_public": Campaign.query.filter_by(visibility="public").count(),
            "total_campaigns_private": Campaign.query.filter_by(visibility="private").count(),
            "total_ad_requests_pending": AdRequest.query.filter_by(status="Pending").count(),
            "total_ad_requests_accepted": AdRequest.query.filter_by(status="Accepted").count(),
            "total_ad_requests_rejected": AdRequest.query.filter_by(status="Rejected").count(),
            "total_influencers": Influencer.query.count(),
            "flagged_users": User.query.filter_by(flagged=True).count(),
            "pending_sponsors": Sponsor.query.filter_by(status="Pending").count()  # Count pending sponsors
        }
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Get all pending sponsors for approval
@admin.route("/pending_sponsors", methods=["GET"])
@token_required
@admin_required
@cache.cached()
def pending_sponsors():
    try:
        sponsors = Sponsor.query.filter_by(status="Pending").all()
        return jsonify([{
            "id": sponsor.id,
            "company_name": sponsor.company_name,
            "industry": sponsor.industry,
            "budget": sponsor.budget
        } for sponsor in sponsors])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Approve a sponsor
@admin.route("/approve_sponsor/<int:sponsor_id>", methods=["POST"])
@token_required
@admin_required
def approve_sponsor(sponsor_id):
    try:
        sponsor = Sponsor.query.get(sponsor_id)
        if not sponsor:
            return jsonify({"message": "Sponsor not found"}), 404
        sponsor.status = "Approved"
        db.session.commit()

        # Clear cache for dashboard data after approval
        cache.delete('dashboard_data')
        return jsonify({"message": "Sponsor approved successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Flag a user (e.g., influencer or sponsor)
@admin.route("/flag_user", methods=["POST"])
@token_required
@admin_required
def flag_user():
    data = request.json
    user_id_to_flag = data.get("user_id")
    reason = data.get("reason")

    if request.user['user_id'] == user_id_to_flag:
        return jsonify({"message": "You cannot flag yourself"}), 403

    user_to_flag = User.query.get(user_id_to_flag)
    if not user_to_flag:
        return jsonify({"message": "User not found"}), 404

    # Flag user by creating a flag entry (you can extend this for both Users and Campaigns)
    user_to_flag.flagged = True  # Mark user as flagged
    user_to_flag.flag_reason = reason  # Store the reason for flagging
    db.session.commit()
    
    # Insert a record into the UserFlag table
    user_flag = UserFlag(user_id=user_to_flag.id, reason=reason)
    db.session.add(user_flag)
    db.session.commit()

    # Clear cache for dashboard data after flagging
    cache.delete('dashboard_data')
    return jsonify({"message": "User flagged successfully"}), 201
