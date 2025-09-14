# JWT token creation, verification, and other security helpers
# JWT token creation and verification helper functions
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.config import JWT_SECRET, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # Ensure correct token URL



def create_access_token(data: dict):
    """
    Generate a JWT token with expiration.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str):
    """
    Verify a JWT token and return decoded payload.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload  # Contains user data (e.g., email)
    except JWTError:
        return None  # Token is invalid or expired

# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     """
#     Verify password. Replace this with a proper hashing function in production.
#     For demo purposes, assume plain text.
#     """
#     return plain_password == hashed_password

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    """
    Hash a plaintext password.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)


# OAuth2 dependency for FastAPI
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
