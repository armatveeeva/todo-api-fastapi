from sqlalchemy.orm import Session
from . import models, schemas, notifications
from typing import List, Optional


def get_todos(db: Session, skip: int = 0, limit: int = 10, completed: Optional[bool] = None) -> List[models.Todo]:
    query = db.query(models.Todo)
    if completed is not None:
        query = query.filter(models.Todo.completed == completed)
    return query.offset(skip).limit(limit).all()


def get_todo(db: Session, todo_id: int) -> Optional[models.Todo]:
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()


def create_todo(db: Session, todo: schemas.TodoCreate) -> models.Todo:
    db_todo = models.Todo(**todo.model_dump())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)

    # Вызываем функцию уведомления после успешного создания
    notifications.send_notification(db_todo.title)

    return db_todo


def update_todo(db: Session, todo_id: int, todo: schemas.TodoUpdate) -> Optional[models.Todo]:
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if db_todo:
        update_data = todo.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_todo, key, value)
        db.commit()
        db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, todo_id: int) -> bool:
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if db_todo:
        db.delete(db_todo)
        db.commit()
        return True
    return False
