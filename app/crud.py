from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from typing import List, Optional
from datetime import datetime

from app import models, schemas
from app.security import get_password_hash, verify_password
from pydantic import BaseModel
import uuid
from sqlalchemy.exc import SQLAlchemyError
from app.core.cache import cache, invalidate_cache

# Создание нового пользователя
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Создание новой задачи
def create_task(db: Session, task: schemas.TaskCreate, user_id: uuid.UUID):
    try:
        db_task = models.Task(
            id=uuid.uuid4(),  # Убедитесь, что UUID передаётся корректно
            title=task.title,
            description=task.description,
            due_date=task.due_date,
            completed=task.completed,
            executor_id=user_id,  # Привязка задачи к пользователю
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        invalidate_cache("get_tasks:*")
        return db_task
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Database error: {str(e)}")

# Получение задачи по ID
def get_task(db: Session, task_id: str, user_id: uuid.UUID):
    try:
        # Преобразуем task_id в UUID
        task_uuid = uuid.UUID(task_id)
        return db.query(models.Task).filter(models.Task.id == task_uuid, models.Task.executor_id == user_id).first()
    except ValueError:
        return None

# Получение списка задач
def get_tasks(db: Session, user_id: uuid.UUID, skip: int = 0, limit: int = 10):
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
    invalidate_cache(f"get_task:{task_id}:{user_id}")
    invalidate_cache("get_tasks:*")
    return task

# Функция удаления задачи
def delete_task(db: Session, task_id: str, user_id: uuid.UUID):
    try:
        # Преобразуем task_id в UUID
        task_uuid = uuid.UUID(task_id)
        task = db.query(models.Task).filter(models.Task.id == task_uuid, models.Task.executor_id == user_id).first()
        if task:
            db.delete(task)
            db.commit()
        invalidate_cache(f"get_task:{task_id}:{user_id}")
        invalidate_cache("get_tasks:*")
        return task
    except ValueError:
        return None

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

@cache(ttl=300)
async def get_tasks(
    db: Session,
    user_id: int,
    pagination: schemas.PaginationParams,
    sort: schemas.SortParams,
    filters: schemas.TaskFilterParams
) -> List[models.Task]:
    query = db.query(models.Task).filter(models.Task.user_id == user_id)
    
    # Apply filters
    if filters.status:
        query = query.filter(models.Task.status == filters.status)
    if filters.priority:
        query = query.filter(models.Task.priority == filters.priority)
    if filters.tags:
        query = query.filter(models.Task.tags.overlap(filters.tags))
    if filters.due_date_from:
        query = query.filter(models.Task.due_date >= filters.due_date_from)
    if filters.due_date_to:
        query = query.filter(models.Task.due_date <= filters.due_date_to)
    
    # Apply sorting
    sort_column = getattr(models.Task, sort.sort_by, models.Task.created_at)
    sort_func = desc if sort.sort_order == "desc" else asc
    query = query.order_by(sort_func(sort_column))
    
    # Apply pagination
    offset = (pagination.page - 1) * pagination.per_page
    query = query.offset(offset).limit(pagination.per_page)
    
    return query.all()

@cache(ttl=300)
async def get_task(db: Session, task_id: int, user_id: int) -> Optional[models.Task]:
    return db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.user_id == user_id
    ).first()

async def create_task(db: Session, task: schemas.TaskCreate, user_id: int) -> models.Task:
    db_task = models.Task(**task.dict(), user_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    invalidate_cache("get_tasks:*")
    return db_task

async def update_task(
    db: Session,
    task_id: int,
    task: schemas.TaskUpdate,
    user_id: int
) -> Optional[models.Task]:
    db_task = await get_task(db, task_id, user_id)
    if not db_task:
        return None
    
    for key, value in task.dict(exclude_unset=True).items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    invalidate_cache(f"get_task:{task_id}:{user_id}")
    invalidate_cache("get_tasks:*")
    return db_task

async def delete_task(db: Session, task_id: int, user_id: int) -> bool:
    db_task = await get_task(db, task_id, user_id)
    if not db_task:
        return False
    
    db.delete(db_task)
    db.commit()
    invalidate_cache(f"get_task:{task_id}:{user_id}")
    invalidate_cache("get_tasks:*")
    return True

async def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()