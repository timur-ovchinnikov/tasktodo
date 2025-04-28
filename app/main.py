from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import schemas, crud, jwt
from app.security import verify_password
from app.schemas import UserCreate, TaskCreate, UserOut, TaskOut, TaskUpdate
from app.database import get_db
from app.routers import task, auth, tasks  # Импортируем маршруты задач
from app.schemas import User  # Добавляем импорт User
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from contextlib import asynccontextmanager
from .database import engine, Base
from .core.logging import logger
from .core.tasks import check_due_tasks

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up application...")
    Base.metadata.create_all(bind=engine)
    
    # Start background tasks
    db = next(get_db())
    asyncio.create_task(check_due_tasks(db))
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    db.close()

app = FastAPI(
    title="TaskTodo API",
    description="A simple task management API",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(task.router, prefix="/api/v1/tasks", tags=["tasks"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])

@app.get("/")
async def root():
    return {"message": "Welcome to TaskTodo API"}

# Регистрация пользователя
@app.post("/register")
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # Check if the email already exists
        existing_user = crud.get_user_by_email(db, email=user.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        db_user = crud.create_user(db, user)
        return {"msg": "User created", "user": db_user}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error creating user: " + str(e))

# Логин пользователя и получение JWT токена
@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
        )
    access_token = jwt.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Получение текущего пользователя из JWT токена
@app.get("/users/me", response_model=UserOut)
def read_users_me(current_user: User = Depends(jwt.get_current_user)):
    return current_user

# Создание задачи
@app.post("/api/v1/task/new", response_model=TaskOut)
def create_task(task: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(jwt.get_current_user)):
    try:
        return crud.create_task(db=db, task=task, user_id=current_user.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# Получение всех задач для текущего пользователя
@app.get("/api/v1/task", response_model=list[schemas.TaskListItem])
def read_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(jwt.get_current_user)):
    return crud.get_tasks(db=db, user_id=current_user.id, skip=skip, limit=limit)

from uuid import UUID

@app.get("/api/v1/task/{task_id}", response_model=TaskOut)
def read_task(task_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(jwt.get_current_user)):
    task = crud.get_task(db, task_id=task_id, user_id=current_user.id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.delete("/api/v1/task/{task_id}", response_model=TaskOut)
def delete_task(task_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(jwt.get_current_user)):
    task = crud.delete_task(db=db, task_id=task_id, user_id=current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Регистрируем маршруты задач
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["tasks"])