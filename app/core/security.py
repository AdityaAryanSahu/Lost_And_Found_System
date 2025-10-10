from passlib.context import CryptContext
from datetime import timedelta, datetime
import jwt
import uuid
import logging

SECRET_KEY = "b6718f5b621697e4b10ed7c6187bca24"  # Use a strong, environment-loaded key!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pswd_context=CryptContext(
    schemes=['bycrypt']
)

def gen_pswd_hash(pswd:str) -> str:
    hash=pswd_context.hash(pswd)
    return hash

def verify_pswd(pswd:str, hash:str) -> bool:
    return pswd_context.verify(pswd, hash)
    
def create_access_token(user_data: dict, expiry:timedelta= None, refresh:bool= False):
    payload={}
    payload['sub']=str(user_data['user_id'])
    payload['exp']=datetime.now() + (expiry if expiry is not None else timedelta(minutes==ACCESS_TOKEN_EXPIRE_MINUTES))
    payload['jti']=str(uuid.uuid4())
    payload['refresh']=refresh
    
    #algo and secret key set as env variable
    token=jwt.encode(
        payload=payload,
        key=SECRET_KEY, #hard coded for now dont forget to add to env var
        algorithm=ALGORITHM
    )
    return token

def decode_token(token:str)-> dict:
    try:
        token_data=jwt.decode(
            jwt=token,
            key=SECRET_KEY,
            algorithm=[ALGORITHM]
        )
        return token_data
    except jwt.PYJWTError as e:
        logging.exception(e)
        return None