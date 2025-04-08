from sqlalchemy.orm import Session
from app import models, schemas
from uuid import UUID
from app.security import get_password_hash, verify_password
from pydantic import BaseModel
import uuid

# Создание нового пользователя
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Создание новой задачи
def create_task(db: Session, task: schemas.TaskCreate, user_id: str):
    db_task = models.Task(
        id=str(uuid.uuid4()),  # Генерация уникального идентификатора
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        completed=task.completed,
        executor_id=user_id,  # Привязка задачи к пользователю
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# Получение задачи по ID
def get_task(db: Session, task_id: UUID, user_id: UUID):
    return db.query(models.Task).filter(models.Task.id == task_id, models.Task.executor_id == user_id).first()

# Получение списка задач
def get_tasks(db: Session, user_id: UUID, skip: int = 0, limit: int = 10):
    return db.query(models.Task).filter(models.Task.executor_id == user_id).offset(skip).limit(limit).all()

# Получение пользователя по email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# Проверка пароля пользователя
def verify_user_password(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if user and verify_password(password, user.hashed_password):
        return user
    return None

# Функция обновления задачи
def update_task(db: Session, task_id: UUID, task_update: schemas.TaskUpdate, user_id: UUID):
    task = get_task(db, task_id, user_id)
    if not task:
        return None

    for field, value in task_update.dict(exclude_unset=True).items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task

# Функция удаления задачи
def delete_task(db: Session, task_id: UUID, user_id: UUID):
    task = get_task(db, task_id, user_id)
    if not task:
        return None
    db.delete(task)
    db.commit()
    return {"msg": "Task successfully deleted"}

class UserCreate(BaseModel):
    # ...existing fields...
    class Config:
        from_attributes = True  # Updated from orm_mode

class TaskCreate(BaseModel):
    # ...existing fields...
    class Config:
        from_attributes = True  # Updated from orm_mode

class TaskUpdate(BaseModel):
    # ...existing fields...
    class Config:
        from_attributes = True  # Updated from orm_mode