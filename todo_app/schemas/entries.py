from datetime import datetime

from pydantic import BaseModel, constr, ValidationError, validator
from pydantic.fields import Field
from pydantic.color import Color as color


# TODO: validate date_created must be less then date_expiration

class ColorBase(BaseModel):
    code: color

    class Config:
        orm_mode = True

    @validator('code')
    def valid_color_code(cls, code: color):
        if code:
            print('pydentic verified color')
            return code.as_hex()
        else:
            raise ValueError('value must be filled in by color format')


""""""


class CategoryBase(BaseModel):
    name: str
    slug: str | None
    color_id: int

    class Config:
        orm_mode = True


class CategoryRead(CategoryBase):
    pass


class CategoryCreate(CategoryBase):
    user_id: int


class CategoryUpdate(CategoryBase):
    pass


""""""


class ThemeBase(BaseModel):
    name: str
    slug: str
    cat_id: int
    color_id: int

    class Config:
        orm_mode = True


class ThemeCreate(ThemeBase):
    pass


class ThemeRead(ThemeBase):
    pass


class ThemeUpdate(ThemeBase):
    pass


""""""


class TaskBase(BaseModel):
    title: str
    description: str | None
    completed: bool = False
    theme_id: int

    class Config:
        orm_mode = True


class TaskRead(TaskBase):
    creation_date: datetime
    update_date: datetime | None
    expiration_date: datetime


class TaskCreate(TaskBase):
    slug: str
    expiration_date: datetime = Field(...)
    user_id: int  # remove in the future


class TaskUpdate(TaskBase):
    slug: str
    update_date: datetime = datetime.now()
