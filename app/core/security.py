from passlib.context import CryptContext
from datetime import timedelta, datetime
import jwt
import uuid
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

pswd_context = CryptContext(schemes=['bcrypt'])

def gen_pswd_hash(pswd: str) -> str:
    """Generate bcrypt hash of password."""
    return pswd_context.hash(pswd)

def verify_pswd(pswd: str, hash: str) -> bool:
    """Verify password against hash."""
    return pswd_context.verify(pswd, hash)

def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False) -> str:
    """Create JWT access token."""
    payload = {}
    payload['sub'] = str(user_data.get('user_id', user_data))
    payload['exp'] = datetime.utcnow() + (expiry if expiry is not None else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    payload['jti'] = str(uuid.uuid4())
    payload['refresh'] = refresh
    
    token = jwt.encode(
        payload=payload,
        key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return token

def decode_token(token: str) -> dict:
    """Decode JWT token."""
    try:
        token_data = jwt.decode(
            jwt=token,
            key=settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]  # ← Must be a LIST
        )
        return token_data
    except jwt.PyJWTError as e:
        logger.error(f"Token decode error: {e}")
        raise ValueError(f"Invalid token: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise ValueError(f"Token validation failed: {e}")