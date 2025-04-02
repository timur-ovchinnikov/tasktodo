from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate

def create_user(db: Session, user: UserCreate):
    db_user = User(email=user.email, hashed_password=user.password)  # Пример создания пользователя
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
