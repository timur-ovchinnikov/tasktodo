from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app import schemas, crud, auth
from app.database import get_db

router = APIRouter()

@router.post("/tasks/")
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), user: schemas.User = Depends(auth.get_current_user)):
    return crud.create_task(db=db, task=task, user_id=user.id)

@router.get("/tasks/{task_id}")
def get_task(task_id: UUID, db: Session = Depends(get_db), user: schemas.User = Depends(auth.get_current_user)):
    db_task = crud.get_task(db=db, task_id=task_id, user_id=user.id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.get("/tasks/")
def get_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), user: schemas.User = Depends(auth.get_current_user)):
    tasks = crud.get_tasks(db=db, user_id=user.id, skip=skip, limit=limit)
    return tasks
