from datetime import datetime

class ClaimModel:
    def __init__(self, item_id: str, user_id: str, justification: str):
        self.item_id = item_id
        self.user_id = user_id
        self.justification = justification
        self.claim_id = f"claim_{user_id}_{item_id}"
        self.status = "Pending"
        self.submitted_at = datetime.utcnow()
        self.mssg = "Claim submitted successfully."

    def to_dict(self):
        return {
            "item_id": self.item_id,
            "user_id": self.user_id,
            "justification": self.justification,
            "claim_id": self.claim_id,
            "status": self.status,
            "submitted_at": self.submitted_at,
            "mssg": self.mssg
        }
