from datetime import datetime

from pydantic import BaseModel, constr, ValidationError, validator
from pydantic.fields import Field
from pydantic.color import Color as color
from fastapi.param_functions import Form


# TODO: validate date_created must be less then date_expiration

class ColorBase(BaseModel):
    code: color

    class Config:
        orm_mode = True

    @classmethod
    def as_form(cls, code: color = Form(...)):
        return cls(code=code)

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
    slug: str
    color_id: int

    class Config:
        orm_mode = True


class CategoryRead(CategoryBase):
    pass


# @as_form
class CategoryCreate(CategoryBase):
    user_id: int

    @classmethod
    def as_form(
            cls,
            name: str = Form(...),
            slug: str = Form(...),
            color_id: int = Form(...),
            user_id: int = Form(...)

    ):
        return cls(
            name=name,
            slug=slug,
            color_id=color_id,
            user_id=user_id
        )


class CategoryUpdate(CategoryBase):
    @classmethod
    def as_form(
            cls,
            name: str = Form(...),
            slug: str = Form(...),
            color_id: int = Form(...)

    ):
        return cls(
            name=name,
            slug=slug,
            color_id=color_id
        )


""""""


class ThemeBase(BaseModel):
    name: str
    slug: str
    cat_id: int
    color_id: int

    class Config:
        orm_mode = True


class ThemeCreate(ThemeBase):
    @classmethod
    def as_form(
            cls,
            name: str = Form(...),
            slug: str = Form(...),
            color_id: int = Form(...),
            cat_id: int = Form(...)

    ):
        return cls(
            name=name,
            slug=slug,
            color_id=color_id,
            cat_id=cat_id
        )


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

    @classmethod
    def as_form(
            cls,
            title: str = Form(...),
            description: str | None = Form(...),
            completed: bool = Form(default=False),
            theme_id: int = Form(...),
            slug: str = Form(...),
            expiration_date: datetime = Form(...),
            user_id: int = Form(...)

    ):
        return cls(
            title=title,
            slug=slug,
            description=description,
            completed=completed,
            theme_id=theme_id,
            expiration_date=expiration_date,
            user_id=user_id
        )


class TaskUpdate(TaskBase):
    slug: str
    update_date: datetime = datetime.now()

# TODO: refactor schemas @as_form

###
# import inspect
# from typing import Type
#
# from fastapi import Form
# from pydantic import BaseModel
# from pydantic.fields import ModelField
#
# def as_form(cls: Type[BaseModel]):
#     new_parameters = []
#
#     for field_name, model_field in cls.__fields__.items():
#         model_field: ModelField  # type: ignore
#
#         new_parameters.append(
#              inspect.Parameter(
#                  model_field.alias,
#                  inspect.Parameter.POSITIONAL_ONLY,
#                  default=Form(...) if model_field.required else Form(model_field.default),
#                  annotation=model_field.outer_type_,
#              )
#          )
#
#     async def as_form_func(**data):
#         return cls(**data)
#
#     sig = inspect.signature(as_form_func)
#     sig = sig.replace(parameters=new_parameters)
#     as_form_func.__signature__ = sig  # type: ignore
#     setattr(cls, 'as_form', as_form_func)
#     return cls
