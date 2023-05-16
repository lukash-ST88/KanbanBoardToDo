import time

from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from todo_app.schemas.entries import CategoryCreate, CategoryUpdate, CategoryRead
from todo_app.db.database import get_async_session
from todo_app.models.entries import Category

router = APIRouter(
    prefix='/category',
    tags=['Category']
)


@router.post('/create')
async def add_new_category(new_category: CategoryCreate, session: AsyncSession = Depends(get_async_session)):
    statement = insert(Category).values(**new_category.dict())
    await session.execute(statement)
    await session.commit()
    return {'status': 'success'}


@router.get('/')
async def get_all_categories(session: AsyncSession = Depends(get_async_session)):
    result = await session.scalars(select(Category))
    return result.all()


@router.get('/{cat_slug}', response_model=CategoryRead)
async def get_category(cat_slug: str, session: AsyncSession = Depends(get_async_session)):
    result = await session.scalars(select(Category).where(Category.slug == cat_slug))
    return result.first()


@router.put('/{cat_slug}/update')
async def update_category(cat_slug: str, update_category: CategoryUpdate,
                          session: AsyncSession = Depends(get_async_session)):
    statement = update(Category).where(Category.slug == cat_slug).values(**update_category.dict())
    await session.execute(statement)
    await session.commit()
    return {'status': 'success'}


@router.delete('/{cat_slug}/delete')
async def delete_category(cat_slug: str, session: AsyncSession = Depends(get_async_session)):
    statement = delete(Category).where(Category.slug == cat_slug)
    await session.execute(statement)
    await session.commit()
    return {'status': 'success'}
