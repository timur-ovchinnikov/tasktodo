from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

# Схема для создания задачи
class TaskCreate(BaseModel):
    title: str
    description: str
    due_date: datetime
    completed: bool = False  # Убедитесь, что поле completed указано

    class Config:
        orm_mode = True

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
class UserCreate(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True

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

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    due_date: datetime | None = None
    completed: bool | None = None

    class Config:
        orm_mode = True

# Схема для входа пользователя
class UserLogin(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True