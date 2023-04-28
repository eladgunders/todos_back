from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.deps import get_async_session
from app.api.deps import current_logged_user
from app.dao.db_facade import DBFacade
from app.schemas import PriorityRead

router = APIRouter(
    prefix='/priorities',
    dependencies=[
        Depends(current_logged_user),
        Depends(get_async_session)
    ],
    tags=['Priorities']
)

db_facade = DBFacade.get_instance()


@router.get('', response_model=list[PriorityRead])
async def get_priorities(
    session: AsyncSession = Depends(get_async_session)
):
    return await db_facade.get_priorities()
