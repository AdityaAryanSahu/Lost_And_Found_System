from app.models.user import UserResponse
from app.models.item import ItemResponse

class NotificationService:
    
    async def send_email(self, recipient_email: str, subject: str, body: str) -> bool:
        """
        Mocks sending an email. In a real app, this dispatches a Celery task.
        """
        print(f"\n--- MOCK EMAIL DISPATCHED ---")
        print(f"TO: {recipient_email}")
        print(f"SUBJECT: {subject}")
        print(f"BODY: {body}\n---------------------------\n")
        return True

    async def notify_item_poster_of_claim(self, item: ItemResponse, claimant: UserResponse) -> bool:
        """Notifies the item poster when a new claim is submitted."""
        
        # NOTE: Using a hardcoded email based on item.user_id (Reg No)
        poster_email = f"user_{item.user_id}@college.edu" 
        
        subject = f"ACTION REQUIRED: New Claim for Item {item.item_id}"
        body = (
            f"A new claim has been submitted by user {claimant.user_id} for your item (Type: {item.type}).\n\n"
            f"Review the claim details now."
        )
        return await self.send_email(poster_email, subject, body)
        
    async def notify_claimant_of_decision(self, claimant: UserResponse, item: ItemResponse, decision: str) -> bool:
        """Notifies the claimant if their claim was approved or rejected."""
        
        claimant_email = claimant.email or f"user_{claimant.user_id}@college.edu"
        
        subject = f"Claim Update: Item {item.item_id} - {decision}"
        body = (
            f"Your claim for the item ({item.type}) has been {decision.upper()}.\n"
            f"The item is now marked as {decision.upper()}."
        )
        return await self.send_email(claimant_email, subject, body)