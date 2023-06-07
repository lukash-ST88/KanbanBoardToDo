from fastapi import APIRouter, Depends
from todo_app.db.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from todo_app.auth.models import User


router = APIRouter(prefix="/API/user", tags=['User'])


@router.get('/')
async def get_users(session: AsyncSession = Depends(get_async_session)):
    result = await session.scalars(select(User))
    return result.all()


