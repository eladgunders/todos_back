from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.deps import get_async_session
from app.api.deps import current_logged_user
from app.dao import DBFacade
from app.schemas import TodoRead, TodoInDB, TodoCreate
from app.utils import exception_handler


router = APIRouter(
    prefix='/todos',
    dependencies=[
        Depends(current_logged_user),
        Depends(get_async_session)
    ],
    tags=['Todos']
)

db_facade = DBFacade.get_instance()


@router.get('', response_model=list[TodoRead])
async def get_todos(
    session: AsyncSession = Depends(get_async_session),
    user=Depends(current_logged_user)
):
    return await db_facade.get_todos(session, created_by_id=user.id)


@router.post('', response_model=TodoRead, status_code=status.HTTP_201_CREATED)
@exception_handler
async def add_todo(
    todo_in: TodoCreate,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(current_logged_user)
):
    todo_in = TodoInDB(
        content=todo_in.content,
        priority_id=todo_in.priority_id,
        categories_ids=todo_in.categories_ids,
        created_by_id=user.id
    )
    return await db_facade.add_todo(session, todo_in=todo_in)


@router.delete('/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
@exception_handler
async def delete_todo(
    todo_id: int,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(current_logged_user)
):
    await db_facade.delete_todo(session, id_to_delete=todo_id, created_by_id=user.id)
