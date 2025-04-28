from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from .. import schemas, crud
from ..database import get_db
from ..auth import get_current_user
from ..core.logging import logger

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])

@router.get("/", response_model=List[schemas.Task])
async def read_tasks(
    pagination: schemas.PaginationParams = Depends(),
    sort: schemas.SortParams = Depends(),
    filters: schemas.TaskFilterParams = Depends(),
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    logger.info(f"Fetching tasks for user {current_user.id}")
    tasks = await crud.get_tasks(
        db=db,
        user_id=current_user.id,
        pagination=pagination,
        sort=sort,
        filters=filters
    )
    return tasks

@router.post("/", response_model=schemas.Task)
async def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    logger.info(f"Creating new task for user {current_user.id}")
    return await crud.create_task(db=db, task=task, user_id=current_user.id)

@router.get("/{task_id}", response_model=schemas.Task)
async def read_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    logger.info(f"Fetching task {task_id} for user {current_user.id}")
    task = await crud.get_task(db=db, task_id=task_id, user_id=current_user.id)
    if task is None:
        logger.warning(f"Task {task_id} not found for user {current_user.id}")
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=schemas.Task)
async def update_task(
    task_id: int,
    task: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    logger.info(f"Updating task {task_id} for user {current_user.id}")
    updated_task = await crud.update_task(
        db=db,
        task_id=task_id,
        task=task,
        user_id=current_user.id
    )
    if updated_task is None:
        logger.warning(f"Task {task_id} not found for user {current_user.id}")
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    logger.info(f"Deleting task {task_id} for user {current_user.id}")
    success = await crud.delete_task(db=db, task_id=task_id, user_id=current_user.id)
    if not success:
        logger.warning(f"Task {task_id} not found for user {current_user.id}")
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}
