from jose import jwt
from passlib.context import CryptContext
from app.utils import create_access_token, verify_access_token
from fastapi import Depends, HTTPException
from app.crud import verify_user_password  # Updated import
from app.crud import get_user_by_email
from sqlalchemy.orm import Session
from app.database import get_db
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    # Implement token decoding logic here
    user_email = decode_token(token)  # Replace with actual token decoding logic
    user = get_user_by_email(db, user_email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user
