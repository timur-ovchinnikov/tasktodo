from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_current_user, get_db  # Предположим, что get_db - зависимость для подключения к базе
from app import crud, schemas

router = APIRouter()

@router.get("/tasks")
def read_tasks(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    tasks = crud.get_tasks(db, user_id=current_user.id)
    return tasks
