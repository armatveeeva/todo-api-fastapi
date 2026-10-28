from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from . import models, schemas, notifications
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


async def get_todos(db: AsyncSession, skip: int = 0, limit: int = 10, completed: Optional[bool] = None) -> List[
    models.Todo]:
    query = select(models.Todo)
    if completed is not None:
        query = query.where(models.Todo.completed == completed)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def get_todo(db: AsyncSession, todo_id: int) -> Optional[models.Todo]:
    result = await db.execute(select(models.Todo).where(models.Todo.id == todo_id))
    return result.scalar_one_or_none()


async def create_todo(db: AsyncSession, todo: schemas.TodoCreate) -> models.Todo:
    db_todo = models.Todo(**todo.model_dump())
    db.add(db_todo)
    await db.commit()
    await db.refresh(db_todo)

    await notifications.send_notification(db_todo.title)
    logger.info(f"Создана новая задача: {db_todo.title}")
    return db_todo


async def update_todo(db: AsyncSession, todo_id: int, todo: schemas.TodoUpdate) -> Optional[models.Todo]:
    db_todo = await get_todo(db, todo_id)
    if not db_todo:
        return None
    update_data = todo.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_todo, key, value)
    await db.commit()
    await db.refresh(db_todo)
    return db_todo


async def delete_todo(db: AsyncSession, todo_id: int) -> bool:
    db_todo = await get_todo(db, todo_id)
    if not db_todo:
        return False
    await db.delete(db_todo)
    await db.commit()
    return True
