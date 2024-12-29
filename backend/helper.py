
# helper functions for database

from model import User, Campaign, Sponsor, AdRequest, db




def get_data_by_name(username):
    user = User.query.filter_by(username=username).first()
    if user is not None:
        return user.to_dict()
    else:
        return None
    


from sqlalchemy import case

def get_influencer_campaigns(influencer_id):
    # Query to get all the campaigns, ad_requests, and sponsor names for the influencer
    campaigns = (
        db.session.query(
            Campaign.id.label("campaign_id"),
            Campaign.name.label("campaign_name"),
            Campaign.description,
            Campaign.goals,
            Campaign.start_date,
            Campaign.end_date,
            Sponsor.company_name.label("sponsor_name"),  # Fetch the sponsor name
            Campaign.sponsor_id,
            AdRequest.id.label("ad_request_id"),
            AdRequest.messages,
            AdRequest.payment_amount,
            AdRequest.requirements,
            AdRequest.status,
            AdRequest.influencer_id,
            # We directly use the negotiated fields from AdRequest
            AdRequest.negotiated_payment_amount.label("negotiated_amount"),
            AdRequest.negotiation_status.label("negotiation_status"),
        )
        .join(AdRequest, AdRequest.campaign_id == Campaign.id)  # Join AdRequest with Campaign
        .join(Sponsor, Sponsor.id == Campaign.sponsor_id)  # Join with Sponsor using the sponsor_id
        .filter(AdRequest.influencer_id == influencer_id)  # Filter by influencer_id
        .all()  # Execute the query
    )


    data = []

        # Process each campaign and convert the data into the required format
    for campaign in campaigns:
        campaign_data = {
            "campaign_id": campaign.campaign_id,
            "campaign_name": campaign.campaign_name,
            "description": campaign.description,
            "goals": campaign.goals,
            "sponsor_id": campaign.sponsor_id,
            "sponsor_name": campaign.sponsor_name,  # Add sponsor name
            "start_date": (
                campaign.start_date.strftime("%Y/%m/%d")
                if campaign.start_date
                else None
            ),
            "end_date": (
                campaign.end_date.strftime("%Y/%m/%d") if campaign.end_date else None
            ),
            "ad_request_id": campaign.ad_request_id,
            "influencer_id": campaign.influencer_id,
            "messages": campaign.messages,
            "payment_amount": str(campaign.payment_amount),  # Convert to string if necessary
            "requirements": campaign.requirements,
            "status": campaign.status,
            "negotiated_amount": str(campaign.negotiated_amount),  # Convert to string if necessary
            "negotiation_status": campaign.negotiation_status,
        }
        
        # Append the formatted campaign data to the list
        data.append(campaign_data)

    return data