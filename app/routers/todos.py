from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[schemas.TodoResponse])
async def read_todos(
    skip: int = 0,
    limit: int = 10,
    completed: Optional[bool] = None,
    db: AsyncSession = Depends(get_db)
):
    return await crud.get_todos(db, skip=skip, limit=limit, completed=completed)

@router.get("/{todo_id}", response_model=schemas.TodoResponse)
async def read_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    todo = await crud.get_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return todo

@router.post("/", response_model=schemas.TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: schemas.TodoCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_todo(db, todo)

@router.put("/{todo_id}", response_model=schemas.TodoResponse)
async def update_todo(todo_id: int, todo: schemas.TodoUpdate, db: AsyncSession = Depends(get_db)):
    updated_todo = await crud.update_todo(db, todo_id, todo)
    if not updated_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return updated_todo

@router.delete("/{todo_id}", status_code=status.HTTP_200_OK)
async def delete_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    success = await crud.delete_todo(db, todo_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return {"message": "Todo deleted successfully"}
