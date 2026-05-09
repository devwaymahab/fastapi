import jwt
from jwt import PyJWTError as JWTError
from fastapi import HTTPException

SECRET_KEY = "testkey"
ALGORITHM = "HS256"

def create_access_token(data: dict):
    token = jwt.encode(
        data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return token

def verify_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )