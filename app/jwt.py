from datetime import datetime, timedelta
from app.db import get_db  # Импортируем get_db из db.py
import jwt
from app import schemas
from app.security import verify_password
from app.crud import get_user_by_email
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import SessionLocal

# Секретный ключ для подписи JWT токенов
SECRET_KEY = "your-secret-key"  # Замените на свой секретный ключ
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Время жизни токена

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # Схема для получения токена

# Функция для создания JWT токена
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Функция для проверки JWT токена
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Функция для получения текущего пользователя из токена
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_token(token)
    user = get_user_by_email(db, email=payload.get("sub"))
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Функция для логина (генерация токена)
def login_for_access_token(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    # Создаем JWT токен
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
