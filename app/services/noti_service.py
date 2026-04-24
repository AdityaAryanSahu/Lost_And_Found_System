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
                "html": f"<p>{body.replace(chr(10), '<br>')}</p>"
            })
            return True

        except Exception as e:
            print("Email error:", e)
            return False

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
        body = (
            f"A new claim has been submitted by user {claimant.user_id} "
            f"for your item (Type: {item.type}).\n\n"
            f"Review the claim details now."
        )

        return await self.send_email(poster_email, subject, body)
        
    async def notify_claimant_of_decision(self, claimant: UserResponse, item: ItemResponse, decision: str) -> bool:
        claimant_email = claimant.email

        if not claimant_email:
            print("Claimant has no email")
            return False
        
        subject = f"Claim Update: Item {item.item_id} - {decision}"
        body = (
            f"Your claim for the item ({item.type}) has been {decision.upper()}.\n"
            f"The item is now marked as {decision.upper()}."
        )

        return await self.send_email(claimant_email, subject, body)