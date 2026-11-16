from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import crud
from ..database import get_db
from ..models import Todo
from ..schemas import TodoCreate, TodoResponse, TodoUpdate

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[TodoResponse])
async def get_todos(
    db: AsyncSession = Depends(get_db),
) -> list[TodoResponse]:
    result = await db.execute(select(Todo).order_by(Todo.id))
    todos = result.scalars().all()
    return [TodoResponse.model_validate(todo) for todo in todos]


@router.get("/list", response_model=list[TodoResponse])
async def read_todos(
    skip: int = 0,
    limit: int = 10,
    completed: bool | None = None,
    db: AsyncSession = Depends(get_db),
) -> list[TodoResponse]:
    todos = await crud.get_todos(db, skip=skip, limit=limit, completed=completed)
    return [TodoResponse.model_validate(todo) for todo in todos]


@router.get("/{todo_id}", response_model=TodoResponse)
async def read_todo(
    todo_id: int,
    db: AsyncSession = Depends(get_db),
) -> TodoResponse:
    todo = await crud.get_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return TodoResponse.model_validate(todo)


@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo: TodoCreate,
    db: AsyncSession = Depends(get_db),
) -> TodoResponse:
    created_todo = await crud.create_todo(db, todo)
    return TodoResponse.model_validate(created_todo)


@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: int,
    todo: TodoUpdate,
    db: AsyncSession = Depends(get_db),
) -> TodoResponse:
    updated_todo = await crud.update_todo(db, todo_id, todo)
    if not updated_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return TodoResponse.model_validate(updated_todo)


@router.delete("/{todo_id}", status_code=status.HTTP_200_OK)
async def delete_todo(
    todo_id: int,
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    success = await crud.delete_todo(db, todo_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return {"message": "Todo deleted successfully"}
