from app.models.user import UserResponse
from app.models.item import ItemResponse
from app.repositories.user_repository import UserRepo
import resend
import os
from app.core.config import settings

resend.api_key = settings.RESEND_API_KEY

class NotificationService:
    def __init__(self, user_repo: UserRepo):
        self.user_repository = user_repo
    
    async def send_email(self, recipient_email: str, subject: str, body: str) -> bool:
        try:
            print(f"Sending email to {recipient_email}")

            resend.Emails.send({
                "from": "Lost & Found <onboarding@resend.dev>",
                "to": [recipient_email],
                "subject": subject,
                "html": body
            })
            return True

        except Exception as e:
            print("Email error:", e)
            return False
        
        
    async def notify_match_found(self, user_id: str, item_type: str, score: float) -> bool:
        user_data = await self.user_repository.get_user_by_id(user_id)
        
        if not user_data or not user_data.get("email"):
            print(f"User {user_id} not found or has no email for match alert")
            return False

        recipient_email = user_data.get("email")
        match_percent = f"{round(score * 100)}%"
        
        subject = f" Smart Match Found: Your {item_type}"
        
        html_body = f"""
        <div style="font-family: sans-serif; background-color: #0a0a0a; color: #cccccc; padding: 40px; border-radius: 12px; border: 1px solid #D4AF37;">
            <h2 style="color: #D4AF37; border-bottom: 1px solid #333; padding-bottom: 10px;">Potential Match Found!</h2>
            <p style="font-size: 16px;">Our AI matching engine has detected a high-probability match for an item you posted.</p>
            
            <div style="background: rgba(212, 175, 55, 0.1); padding: 20px; border-radius: 8px; margin: 20px 0; border: 1px solid rgba(212, 175, 55, 0.3);">
                <p style="margin: 0; color: #D4AF37;"><strong>Item Type:</strong> {item_type}</p>
                <p style="margin: 5px 0 0 0;"><strong>Match Confidence:</strong> {match_percent}</p>
            </div>

            <p>Log in to your dashboard now to review the match and contact the other party.</p>
            
            <div style="margin-top: 30px;">
                <a href="https://lost-and-found-inventory.onrender.com/my-items" 
                   style="display: inline-block; background: #D4AF37; color: black; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: bold;">
                   View My Matches
                </a>
            </div>
            
            <p style="font-size: 12px; color: #666; margin-top: 30px; border-top: 1px solid #333; padding-top: 20px;">
                This is an automated message from the Lost & Found Inventory.
            </p>
        </div>
        """

        return await self.send_email(recipient_email, subject, html_body)

    async def notify_item_poster_of_claim(self, item: ItemResponse, claimant: UserResponse) -> bool:
        owner = await self.user_repository.get_user_by_id(item.user_id)

        if not owner:
            print("Owner not found")
            return False

        poster_email = owner.get("email")

        if not poster_email:
            print("Owner has no email")
            return False
        
        subject = f"ACTION REQUIRED: New Claim for Item {item.item_id}"
        body = f"""
        <div style="font-family: sans-serif; background-color: #0a0a0a; color: #cccccc; padding: 40px; border-radius: 12px; border: 1px solid #D4AF37;">
            <h2 style="color: #D4AF37; border-bottom: 1px solid #333; padding-bottom: 10px;">New Claim Submitted</h2>
            <p style="font-size: 16px;">User <strong>{claimant.user_id}</strong> has submitted a claim for the item you posted.</p>
            
            <div style="background: rgba(212, 175, 55, 0.05); padding: 20px; border-radius: 8px; margin: 20px 0; border: 1px solid rgba(212, 175, 55, 0.2);">
                <p style="margin: 0; color: #D4AF37;"><strong>Item:</strong> {item.type}</p>
                <p style="margin: 5px 0 0 0; color: #999;"><strong>Description:</strong> {item.desc[:50]}...</p>
            </div>

            <p>Please review the justification provided by the claimant to verify ownership.</p>
            
            <div style="margin-top: 30px;">
                <a href="https://lost-and-found-inventory.onrender.com/my-items" 
                   style="display: inline-block; background: #D4AF37; color: black; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: bold;">
                   Review Claim
                </a>
            </div>
        </div>
        """

        return await self.send_email(poster_email, subject, body)
        
    async def notify_claimant_of_decision(self, claimant: UserResponse, item: ItemResponse, decision: str) -> bool:
        claimant_email = claimant.email

        if not claimant_email:
            print("Claimant has no email")
            return False
        
        accent_color = "#4CAF50" if decision.lower() == "approved" else "#e74c3c"
        subject = f"Claim Update: Item {item.item_id} - {decision}"
        body = f"""
        <div style="font-family: sans-serif; background-color: #0a0a0a; color: #cccccc; padding: 40px; border-radius: 12px; border: 1px solid {accent_color};">
            <h2 style="color: {accent_color}; border-bottom: 1px solid #333; padding-bottom: 10px;">Claim {decision.upper()}</h2>
            <p style="font-size: 16px;">The owner has reviewed your claim for the <strong>{item.type}</strong>.</p>
            
            <div style="background: rgba(255, 255, 255, 0.03); padding: 20px; border-radius: 8px; margin: 20px 0; border: 1px solid #333;">
                <p style="margin: 0;">Status: <span style="color: {accent_color}; font-weight: bold;">{decision.upper()}</span></p>
            </div>

            <p>{"Please coordinate with the owner via messages to arrange a pickup." if decision.lower() == 'approved' else "If you believe this is a mistake, you can try contacting the poster directly."}</p>
            
            <div style="margin-top: 30px;">
                <a href="https://lost-and-found-inventory.onrender.com/messages" 
                   style="display: inline-block; background: {accent_color}; color: {'white' if decision.lower() != 'approved' else 'black'}; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: bold;">
                   Go to Messages
                </a>
            </div>
        </div>
        """

        return await self.send_email(claimant_email, subject, body)