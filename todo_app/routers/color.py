import time

from fastapi import APIRouter, Depends

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from todo_app.schemas.entries import ColorBase
from todo_app.db.database import get_async_session
from todo_app.models.entries import Color

router = APIRouter(
    prefix='/color',
    tags=['Color']
)


@router.post('/create')
async def add_new_color(new_color: ColorBase, session: AsyncSession = Depends(get_async_session)):
    statement = insert(Color).values(**new_color.dict())
    await session.execute(statement)
    await session.commit()
    color = await session.scalars(select(Color))
    return {'status': color.all()}


@router.get('/')
async def get_all_colors(session: AsyncSession = Depends(get_async_session)):
    result = await session.scalars(select(Color))
    return result.all()

