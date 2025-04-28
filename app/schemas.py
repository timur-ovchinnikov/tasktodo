from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional, List
from enum import Enum

# Схема для создания задачи
class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: TaskStatus = TaskStatus.TODO
    priority: Optional[int] = None
    tags: Optional[List[str]] = None

class TaskCreate(TaskBase):
    pass

class TaskResponse(BaseModel):
    id: str  # Убедитесь, что это str
    title: str
    description: str | None
    due_date: datetime
    completed: bool
    executor_id: str  # Убедитесь, что это str

    class Config:
        from_attributes = True  # Для поддержки ORM

# Схема для вывода задачи
class TaskOut(BaseModel):
    id: UUID
    title: str
    description: str
    due_date: datetime
    completed: bool
    executor_id: UUID  # Поле для идентификатора исполнителя

    class Config:
        orm_mode = True

# Схема для вывода пользователя
class UserOut(BaseModel):
    id: UUID
    email: str

    class Config:
        orm_mode = True

# Схема для создания пользователя
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

# Схема для пользователя (используется в зависимостях)
class User(BaseModel):
    id: UUID
    email: str

    class Config:
        orm_mode = True

# Схема для токена
class Token(BaseModel):
    access_token: str
    token_type: str

class TaskListItem(BaseModel):
    id: UUID
    title: str

    class Config:
        orm_mode = True

class TaskUpdate(TaskBase):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[TaskStatus] = None
    priority: Optional[int] = None
    tags: Optional[List[str]] = None

    class Config:
        orm_mode = True

# Схема для входа пользователя
class UserLogin(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True

class PaginationParams(BaseModel):
    page: int = 1
    per_page: int = 10

class SortParams(BaseModel):
    sort_by: str = "created_at"
    sort_order: str = "desc"

class TaskFilterParams(BaseModel):
    status: Optional[TaskStatus] = None
    priority: Optional[int] = None
    tags: Optional[List[str]] = None
    due_date_from: Optional[datetime] = None
    due_date_to: Optional[datetime] = None