from datetime import datetime
from typing import Optional

class UserModel:
    def __init__(self, username: str, user_id: str, passwd: str, email: Optional[str] = None, is_admin: bool = False):
        self.username = username
        self.user_id = user_id
        self.passwd = passwd
        self.email = email
        self.is_admin = is_admin
        self.acc_created = datetime.utcnow()

    def to_dict(self):
        return {
            "username": self.username,
            "user_id": self.user_id,
            "passwd": self.passwd,
            "email": self.email,
            "is_admin": self.is_admin,
            "acc_created": self.acc_created
        }
