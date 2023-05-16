from datetime import datetime

from pydantic import BaseModel, constr, ValidationError, validator
from typing import List
from todo_app.auth.schemas import UserRead
import re
from pydantic.color import Color as cl


# TODO: validate date_created must be less then date_expiration

class ColorBase(BaseModel):
    id: int
    code: cl

    class Config:
        orm_mode = True

    @validator('code')
    def valid_color_code(cls, code: cl):
        if code:
            print('pydentic verified color')
            return code.as_hex()
        else:
            raise ValueError('value must be filled in by color format')


class CategoryBase(BaseModel):
    name: str
    slug: str | None
    color_id: int

    class Config:
        orm_mode = True


class CategoryRead(CategoryBase):
    pass


class CategoryCreate(CategoryBase):
    id: int
    user_id: int


class CategoryUpdate(CategoryBase):
    pass


class ThemeBase(BaseModel):
    id: int
    name: str
    slug: str
    cat_id: int
    color_id: int

    # cat: CategoryBase
    # color: ColorBase

    class Config:
        orm_mode = True


class TaskBase(BaseModel):
    id: int
    title: str
    slug: str
    description: str
    date_created_timezone: datetime
    date_created: datetime = datetime.now()
    date_updated: datetime | None
    date_expiration: datetime
    completed: bool = False
    theme_id: int
    user_id: int

    # theme: ThemeBase
    # user: UserRead

    class Config:
        orm_mode = True
