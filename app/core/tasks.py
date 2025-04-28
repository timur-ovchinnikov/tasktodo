import asyncio
from datetime import datetime, timedelta
from typing import List
from sqlalchemy.orm import Session

from .. import models, crud
from .notifications import notification
from .logging import logger

async def check_due_tasks(db: Session):
    """Check for tasks that are due soon and send notifications"""
    while True:
        try:
            # Get tasks due in the next 24 hours
            due_date_from = datetime.now()
            due_date_to = due_date_from + timedelta(days=1)
            
            filters = models.schemas.TaskFilterParams(
                due_date_from=due_date_from,
                due_date_to=due_date_to
            )
            
            # Get all tasks due soon
            tasks = await crud.get_tasks(
                db=db,
                user_id=None,  # We'll filter by user in the notification
                pagination=models.schemas.PaginationParams(page=1, per_page=100),
                sort=models.schemas.SortParams(),
                filters=filters
            )
            
            # Send notifications for each task
            for task in tasks:
                try:
                    await notification.send_task_notification(
                        to_email=task.owner.email,
                        task_title=task.title,
                        task_description=task.description or "",
                        due_date=str(task.due_date)
                    )
                except Exception as e:
                    logger.error(f"Failed to send notification for task {task.id}: {str(e)}")
            
            # Wait for 1 hour before checking again
            await asyncio.sleep(3600)
            
        except Exception as e:
            logger.error(f"Error in check_due_tasks: {str(e)}")
            await asyncio.sleep(60)  # Wait 1 minute before retrying 