from datetime import datetime, timedelta
from typing import Optional

class AuthSession:
    def __init__(
        self,
        user_id: str,
        refresh_token: str,
        expires_in_days: int = 30,
        email: Optional[str] = None
    ):
        self.user_id = user_id
        self.token = refresh_token
        self.email = email
        self.created_at = datetime.utcnow()
        self.expires_at = self.created_at + timedelta(days=expires_in_days)
        self.revoked = False

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "token": self.token,
            "email": self.email,
            "created_at": self.created_at,
            "expires_at": self.expires_at,
            "revoked": self.revoked
        }