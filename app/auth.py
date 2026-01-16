from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from app.config import settings


# Create password context
pwd_context = CryptContext(
    schemes=["bcrypt"], 
    deprecated="auto"
)

def get_password_hash(password: str) -> str:
    if not isinstance(password, str):
        raise TypeError("Password must be a string")
    return pwd_context.hash(password[:72])

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password[:72], hashed_password)



def create_access_token(data: dict, expires_delta: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except Exception:
        return None
