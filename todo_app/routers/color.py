import time

from fastapi import APIRouter, Depends

from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from todo_app.schemas.entries import ColorBase
from todo_app.db.database import get_async_session
from todo_app.models.entries import Color

router = APIRouter(
    prefix='/API/color',
    tags=['Color']
)


@router.post('/create')
async def add_new_color(new_color: ColorBase = Depends(ColorBase.as_form),
                        session: AsyncSession = Depends(get_async_session)):
    statement = insert(Color).values(**new_color.dict()).returning(Color)
    result = await session.execute(statement)
    await session.commit()
    return result.scalars().first()



@router.get('/')
async def get_all_colors(session: AsyncSession = Depends(get_async_session)):
    result = await session.scalars(select(Color))
    return result.all()

@router.delete('/delete/{color_id}')
async def delete_color(color_id: int, session: AsyncSession = Depends(get_async_session)):
    statement = delete(Color).where(Color.id == color_id)
    await session.execute(statement)
    await session.commit()
    return {'status': 'success'}

# TODO: refactor get query using util method
