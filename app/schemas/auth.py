from datetime import datetime
from typing import Optional

class AuthSession:
    def __init__(self, user_id: str, token: str, email: Optional[str] = None):
        self.user_id = user_id
        self.token = token
        self.email = email
        self.created_at = datetime.utcnow()
        self.status = 1
        self.mssg = "Login successful."

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "token": self.token,
            "email": self.email,
            "created_at": self.created_at,
            "status": self.status,
            "mssg": self.mssg
        }
