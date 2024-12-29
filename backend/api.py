from flask import Blueprint, jsonify, request
from model import db, User, Sponsor, Influencer, Campaign, AdRequest
from flask_cors import cross_origin

from config import cache

api = Blueprint("api", __name__)

@api.route("/users", methods=["GET"])
@cache.cached(timeout=100)
@cross_origin()
def get_all_users():
    data = dict()

    # Filter users by role
    data["admin"] = [user.to_dict() for user in User.query.filter_by(role="admin").all()]
    data["sponsor"] = [user.to_dict() for user in User.query.filter_by(role="sponsor").all()]
    data["influencer"] = [user.to_dict() for user in User.query.filter_by(role="influencer").all()]

    return jsonify(data)


@api.route("/influencers", methods=["GET"])
@cache.cached(timeout=100)
@cross_origin()
def get_all_influencers():
    try:
        influencers = Influencer.query.all()
        return jsonify([influencer.to_dict() for influencer in influencers])
    except Exception as e:
        return jsonify({"message": str(e), "success": False}), 500


@api.route("/influencer/<int:influencer_id>", methods=["GET"])
@cache.cached(timeout=100)
@cross_origin()
def get_influencer(influencer_id):
    try:
        influencer = Influencer.query.get(influencer_id)
        if not influencer:
            return jsonify({"message": "Influencer not found", "success": False}), 404
        return jsonify(influencer.to_dict())
    except Exception as e:
        return jsonify({"message": str(e), "success": False}), 500


@api.route("/campaigns", methods=["GET"])
@cache.cached(timeout=100)
@cross_origin()
def get_all_campaigns():
    try:
        campaigns = Campaign.query.all()
        return jsonify([campaign.to_dict() for campaign in campaigns])
    except Exception as e:
        return jsonify({"message": str(e), "success": False}), 500


@api.route("/campaign/<int:campaign_id>", methods=["GET"])
@cache.cached(timeout=100)
@cross_origin()
def get_campaign(campaign_id):
    try:
        campaign = Campaign.query.get(campaign_id)
        if not campaign:
            return jsonify({"message": "Campaign not found", "success": False}), 404
        return jsonify(campaign.to_dict())
    except Exception as e:
        return jsonify({"message": str(e), "success": False}), 500


@api.route("/campaigns/public", methods=["GET"])
@cache.cached(timeout=100)
@cross_origin()
def get_public_campaigns():
    try:
        campaigns = Campaign.query.filter_by(visibility="public").all()
        return jsonify([campaign.to_dict() for campaign in campaigns])
    except Exception as e:
        return jsonify({"message": str(e), "success": False}), 500


@api.route("/adrequests", methods=["GET"])
@cache.cached(timeout=100)
@cross_origin()
def get_all_adrequests():
    try:
        adrequests = AdRequest.query.all()
        return jsonify([ad_request.to_dict() for ad_request in adrequests])
    except Exception as e:
        return jsonify({"message": str(e), "success": False}), 500


@api.route("/adrequest/<int:ad_request_id>", methods=["GET"])
@cache.cached(key_prefix='api_adrequest_data')
@cross_origin()
def get_adrequest(ad_request_id):
    try:
        adrequest = AdRequest.query.get(ad_request_id)
        if not adrequest:
            return jsonify({"message": "AdRequest not found", "success": False}), 404
        return jsonify(adrequest.to_dict())
    except Exception as e:
        return jsonify({"message": str(e), "success": False}), 500


# Endpoint for User Flagging
# @api.route("/flag_user", methods=["POST"])
# @cross_origin()
# def flag_user():
#     data = request.json
#     user_id = data.get("user_id")
#     reason = data.get("reason")

#     if not user_id or not reason:
#         return jsonify({"message": "User ID and reason are required"}), 400

#     if request.user['user_id'] == user_id:
#         return jsonify({"message": "You cannot flag yourself"}), 403

#     user_to_flag = User.query.get(user_id)
#     if not user_to_flag:
#         return jsonify({"message": "User not found"}), 404

#     flag = UserFlag(user_id=user_id, reason=reason)
#     db.session.add(flag)
#     db.session.commit()

#     return jsonify({"message": "User flagged successfully"}), 201


# # Endpoint for Campaign Flagging
# @api.route("/flag_campaign", methods=["POST"])
# @cross_origin()
# def flag_campaign():
#     data = request.json
#     campaign_id = data.get("campaign_id")
#     reason = data.get("reason")

#     if not campaign_id or not reason:
#         return jsonify({"message": "Campaign ID and reason are required"}), 400

#     campaign_to_flag = Campaign.query.get(campaign_id)
#     if not campaign_to_flag:
#         return jsonify({"message": "Campaign not found"}), 404

#     flag = CampaignFlag(campaign_id=campaign_id, reason=reason)
#     db.session.add(flag)
#     db.session.commit()

#     return jsonify({"message": "Campaign flagged successfully"}), 201
