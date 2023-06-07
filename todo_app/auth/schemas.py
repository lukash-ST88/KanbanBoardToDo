from typing import Optional

from fastapi_users import schemas
from fastapi_users import models
from pydantic import BaseModel, EmailStr
from fastapi.param_functions import Form

#TODO: make secure superuser


class UserRead(schemas.BaseUser[int]):
    id: models.ID
    name: str
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    color_id: int


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    name: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
    color_id: int

    class Config:
        orm_mode = True




class UserUpdate(schemas.BaseUserUpdate):
    password: Optional[str]
    name: Optional[str]
    email: Optional[EmailStr]
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
    color_id: int 

