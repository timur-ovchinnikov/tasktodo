from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.utils import verify_access_token
from app.models import User as UserModel
from app import crud
from app.core.config import SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_db():
    # Здесь должна быть логика для подключения к базе данных
    pass

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_access_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        user = crud.get_user_by_email(db=db, email=email)
        if user is None:
            raise credentials_exception
        return user
    except Exception:
        raise credentials_exception
