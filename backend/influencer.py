from flask import Blueprint, request, jsonify
from model import db, User, Campaign, AdRequest, Influencer
from functools import wraps
from flask_cors import cross_origin
import jwt
from datetime import datetime, timedelta


import helper

from config import cache

influencer = Blueprint("influencer", __name__)
SECRET_KEY = 'your_secret_key'
from flask_cors import cross_origin


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


def influencer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.user.get('role') != 'influencer':
            return jsonify({"message": "Unauthorized"}), 403
        return f(*args, **kwargs)
    return decorated_function

@influencer.route("/login",methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username = username).first()
    # print(user)

    if user and user.check_password(password):
        influencer_data = Influencer.query.filter_by(user_id = user.id).first()
        
        # print(influencer_data.to_dict())
        
        token = jwt.encode({
            'user_id': user.id,
            'username': user.username,
            'role': user.role,
            'exp': datetime.utcnow() + timedelta(hours=1)
        }, SECRET_KEY, algorithm='HS256')
        user.login_date = datetime.utcnow()
        db.session.commit()
        return jsonify({"token": token ,  "role": user.role}), 200
    return jsonify({"message": "Invalid credentials"}), 401



@influencer.route("/register" , methods=["POST"])
def register():

    data = request.json
    #Register as User
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    role = data.get("role")

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "User already exists"}), 400
    
    new_user = User(username=username, email=email, role="influencer")
    new_user.set_password(password)

    try:
        db.session.add(new_user)
        db.session.commit()

        #Register as Influencer
        user_id = new_user.id
        name = data.get("name")
        category = data.get("category")
        niche = data.get("niche")
        reach = data.get("reach")

        new_influ = Influencer(
                user_id=user_id,
                category=category,
                name=name,
                niche=niche,
                reach=reach,
            )

        db.session.add(new_influ)
        db.session.commit()
        
        return jsonify({"message": "New Influencer registered successfully"}), 201
    
    except Exception as e:
        error_message = str(e).split("\n")[0]
        db.session.rollback()
        return jsonify({"message": error_message}), 400



@influencer.route("/dashboard", methods=["GET", "POST"])
@cross_origin()
@token_required
@influencer_required
@cache.cached(key_prefix='influencer_dashboard')
def dashboard():
    try :
        user_id = request.user.get('user_id')
        influencer = Influencer.query.filter_by(user_id=user_id).first()

        # print(influencer)
        
        if not influencer:
            return jsonify({"message": "Influencer not found"}), 404
        
        influencer_id = influencer.id

        data = helper.get_influencer_campaigns(influencer_id)

        # print(data)
        return jsonify({"data": data}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    

@influencer.route("/acceptAdRequest/<int:ad_request_id>", methods=["POST", "GET"])
@cross_origin()
@token_required
@influencer_required
def acceptAdRqst(ad_request_id: int):
    try:
        user_id = request.user.get('user_id')
        influencer = Influencer.query.filter_by(user_id=user_id).first()

        if not influencer:
            return jsonify({"message": "Influencer not found"}), 404

        influencer_id = influencer.id
        data = helper.get_influencer_campaigns(influencer_id)
        show_info = None
        
        # Find the ad request in the data
        for d in data:
            if d["ad_request_id"] == ad_request_id:
                show_info = d
                break

        if not show_info:
            return jsonify({"message": "Ad request not found"}), 404

        # Check if Already Accepted
        if show_info.get("negotiation_status") == "accepted" and show_info.get("status") == "accepted":
            return jsonify({"message": "You have already accepted the ad request."}), 400

        # Check if Already Rejected
        if show_info.get("negotiation_status") == "rejected":
            return jsonify({"message": "You have already rejected the ad request."}), 400

        if request.method == "POST":
            # Update the negotiation status and payment amount in the AdRequest
            ad_reqst = AdRequest.query.filter_by(id=ad_request_id).first_or_404()
            
            # Check if there's an existing negotiation status and update it
            if ad_reqst.negotiation_status != "accepted":
                ad_reqst.negotiation_status = "accepted"
                ad_reqst.negotiated_payment_amount = ad_reqst.payment_amount  # Assuming agreed payment is the negotiated amount
            else:
                return jsonify({"message": "Negotiation already accepted."}), 400

            # Change ad_request status to accepted
            ad_reqst.status = "accepted"
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return jsonify({"message": str(e)}), 500

            # Clear the cache for the dashboard
            cache.delete('influencer_dashboard')

            return jsonify({"message": "Ad request accepted successfully!"}), 200

        else:
            return jsonify(show_info), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
    
@influencer.route("/rejectAdRequest/<int:ad_request_id>", methods=["POST", "GET"])
@cross_origin()
@token_required
@influencer_required
def reject_adrequest(ad_request_id):

    try:
        user_id = request.user.get('user_id')
        influencer = Influencer.query.filter_by(user_id=user_id).first()

        if not influencer:
            return jsonify({"message": "Influencer not found"}), 404
        
        influencer_id = influencer.id
        data = helper.get_influencer_campaigns(influencer_id)
        show_info = next((d for d in data if d["ad_request_id"] == ad_request_id), None)

        if not show_info:
            return jsonify({"message": "Ad request not found"}), 404

        # Check if Already Accepted
        if show_info.get("negotiation_status") == "accepted" and show_info.get("status") == "accepted":
            return jsonify({"message": "You have already accepted the ad request."}), 400

        # Check if Already Rejected
        if show_info.get("negotiation_status") == "rejected" and show_info.get("status") == "rejected":
            return jsonify({"message": "You have already rejected the ad request."}), 400

        if request.method == "POST":
            # Reject the AdRequest by changing its status to "rejected"
            ad_reqst = AdRequest.query.filter_by(id=ad_request_id).first_or_404()
            ad_reqst.status = "rejected"

            # Update the negotiation status to "rejected" as well
            if ad_reqst.negotiation_status != "rejected":
                ad_reqst.negotiation_status = "rejected"
                ad_reqst.negotiated_payment_amount = None  # Clear negotiated payment if rejected
            else:
                return jsonify({"message": "Negotiation already rejected."}), 400

            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return jsonify({"message": str(e)}), 500

            # Clear the cache for dashboard data
            cache.delete('influencer_dashboard')

            return jsonify({"message": "Ad request rejected successfully!"}), 200

        else:
            return jsonify(show_info), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500

@influencer.route("/negoAdRequest/<int:ad_request_id>", methods=["POST", "GET"])
@cross_origin()
@token_required
@influencer_required
def nego_adrequest(ad_request_id):
    try:
        user_id = request.user.get('user_id')
        influencer = Influencer.query.filter_by(user_id=user_id).first()

        if not influencer:
            return jsonify({"message": "Influencer not found"}), 404
        
        influencer_id = influencer.id
        data = helper.get_influencer_campaigns(influencer_id)
        show_info = next((d for d in data if d["ad_request_id"] == ad_request_id), None)

        if not show_info:
            return jsonify({"message": "Ad request not found"}), 404

        # Check if Already Accepted
        if show_info.get("negotiation_status") == "accepted" and show_info.get("status") == "accepted":
            return jsonify({"message": "You have already accepted the ad request!"}), 400

        # Check if Already Rejected
        if show_info.get("negotiation_status") == "rejected":
            return jsonify({"message": "You have already rejected the ad request!"}), 400

        if request.method == "POST":
            new_nego_amount = request.form.get("nego_amount")
            if not new_nego_amount:
                return jsonify({"message": "Empty response won't be accepted!"}), 500

            # Update AdRequest status to 'negotiation'
            ad_reqst = AdRequest.query.filter_by(id=ad_request_id).first_or_404()
            ad_reqst.status = "negotiation"

            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return jsonify({"message": str(e).split("\n")[0]}), 500

            # Update negotiation-related information in AdRequest
            if ad_reqst.negotiation_status != "rejected":
                ad_reqst.negotiated_payment_amount = new_nego_amount
                ad_reqst.negotiation_status = "pending"  # Set negotiation status to pending

                try:
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    return jsonify({"message": str(e).split("\n")[0]}), 500
            else:
                return jsonify({"message": "Negotiation already rejected, cannot proceed!"}), 400

            return jsonify({"message": f"Updated the negotiation with amount: {new_nego_amount}"}), 200

        else:
            return jsonify(show_info), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500


@influencer.route("/sendAdReqst/<int:campaign_id>", methods=["POST"])
@cross_origin()
@token_required
@influencer_required
def sendAdReqst(campaign_id):
    try:
        user_id = request.user.get('user_id')
        influencer = Influencer.query.filter_by(user_id=user_id).first()

        if not influencer:
            return jsonify({"message": "Influencer not found"}), 404
        
        # Check if the campaign exists
        campaign = Campaign.query.get(campaign_id)
        if not campaign:
            return jsonify({"message": "Campaign not found"}), 404
        
        # Get the sponsor_id from the campaign
        sponsor_id = campaign.sponsor_id

        influencer_id = influencer.id
        new_ad = AdRequest(
            campaign_id=campaign_id,
            influencer_id=influencer_id,
            sponsor_id=sponsor_id, 
            requirements="Ad Request from Influencer! Edit and Negotiate it",
            payment_amount=0,
            messages="Payment Amount Yet to be decided!",
            #status="pending",
            #negotiation_status="pending"
        )

        db.session.add(new_ad)
        db.session.commit()

        # #Clear relevant cache
        cache.delete('influencer_dashboard')
        
        return jsonify({"message": "New ad request added successfully", "success": True}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500



@influencer.route("/profile", methods=["GET", "POST"])
@cross_origin()
@token_required
@influencer_required
def influProfile():
    try:
        user_id = request.user.get('user_id')
        influencer = Influencer.query.filter_by(user_id=user_id).first()
        # print(influencer)
        if not influencer:
            return jsonify({"message": "Influencer not found"}), 404

        # Handle GET request
    
        influ_data = influencer.to_dict()
        # print(influ_data)

        # Handle POST request
        if request.method == "POST":
            data = request.json
            # print("this is data" , data)
            # Validate the incoming data
            if not all(key in data for key in ("name", "niche", "reach")):
                return jsonify({"message": "Missing required fields"}), 400

            # Update influencer details
            influencer.name = data.get("name")
            influencer.niche = data.get("niche")
            influencer.reach = data.get("reach")
            influencer.category = data.get("category")


            db.session.commit()

            return jsonify({"message": "Profile updated successfully"})
        
        else:
            return jsonify({"influ_data": influ_data})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500