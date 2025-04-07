from datetime import timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.crud import get_user_by_email
from app.utils import create_access_token, verify_access_token
from app.database import get_db

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_access_token(token)
    user = get_user_by_email(db, email=payload.get("sub"))
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def login_for_access_token(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
