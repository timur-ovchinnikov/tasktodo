# app/api/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta

from app import crud, schemas, models
from app.utils import create_access_token
from app.dependencies import get_db

router = APIRouter()

@router.post("/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Создание нового пользователя
    db_user = crud.create_user(db=db, user=user)
    return db_user

@router.post("/login", response_model=schemas.Token)
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    # Поиск пользователя по email
    db_user = crud.get_user_by_email(db=db, email=user.email)
    if db_user is None or not db_user.verify_password(user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    # Генерация токена
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": db_user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
