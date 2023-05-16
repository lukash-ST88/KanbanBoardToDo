import time

from fastapi import APIRouter, Depends

from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from todo_app.schemas.entries import ThemeBase
from todo_app.db.database import get_async_session
from todo_app.models.entries import Theme

router = APIRouter(
    prefix='/theme',
    tags=['Theme']
)


@router.post('/create')
async def add_new_theme(new_theme: ThemeBase, session: AsyncSession = Depends(get_async_session)):
    statement = insert(Theme).values(**new_theme.dict())
    await session.execute(statement)
    await session.commit()
    return {'status': 'success'}


@router.get('/')
async def get_all_themes(session: AsyncSession = Depends(get_async_session)):
    result = await session.scalars(select(Theme))
    return result.all()


@router.get('/theme_slug}')
async def get_category(theme_slug: str, session: AsyncSession = Depends(get_async_session)):
    result = await session.scalars(select(Theme).where(Theme.slug == theme_slug))
    return result.first()


@router.put('/{theme_slug}/update')
async def update_theme(theme_slug: str, update_theme: ThemeBase,
                       session: AsyncSession = Depends(get_async_session)):
    statement = update(Theme).where(Theme.slug == theme_slug).values(**update_theme.dict())
    await session.execute(statement)
    await session.commit()
    return {'status': 'success'}


@router.delete('/{theme_slug}/delete')
async def delete_theme(theme_slug: str, session: AsyncSession = Depends(get_async_session)):
    statement = delete(Theme).where(Theme.slug == theme_slug)
    await session.execute(statement)
    await session.commit()
    return {'status': 'success'}
