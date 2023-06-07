import time

from fastapi import APIRouter, Depends
from todo_app.auth.config import current_active_user
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from todo_app.schemas.entries import ThemeCreate, ThemeUpdate
from todo_app.db.database import get_async_session
from todo_app.models.entries import Theme, Category

router = APIRouter(
    prefix='/API/theme',
    tags=['Theme']
)


@router.post('/create')
async def add_new_theme(new_theme: ThemeCreate = Depends(ThemeCreate.as_form), session: AsyncSession = Depends(get_async_session)):
    statement = insert(Theme).values(**new_theme.dict()).returning(Theme)
    result = await session.execute(statement)
    await session.commit()
    return result.scalars().first()


@router.get('/')
async def get_all_themes(session: AsyncSession = Depends(get_async_session), user=Depends(current_active_user)):
    result = await session.scalars(select(Theme).join(Theme.cat).where(Category.user_id == user.id))
    return result.all()


@router.get('/theme_slug}')
async def get_theme(theme_slug: str, session: AsyncSession = Depends(get_async_session)):
    result = await session.scalars(select(Theme).where(Theme.slug == theme_slug))
    return result.first()


@router.put('/{theme_slug}/update')
async def update_theme(theme_slug: str, update_theme: ThemeUpdate = Depends(ThemeUpdate.as_form),
                       session: AsyncSession = Depends(get_async_session)):
    statement = update(Theme).where(Theme.slug == theme_slug).values(**update_theme.dict()).returning(Theme)
    result = await session.execute(statement)
    await session.commit()
    return result.scalars().first()


@router.delete('/{theme_slug}/delete')
async def delete_theme(theme_slug: str, session: AsyncSession = Depends(get_async_session)):
    statement = delete(Theme).where(Theme.slug == theme_slug)
    await session.execute(statement)
    await session.commit()
    return {'status': 'success'}
