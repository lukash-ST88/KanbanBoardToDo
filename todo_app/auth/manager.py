import uuid
from typing import Optional

import starlette.status as status

from fastapi.responses import RedirectResponse
from fastapi import Depends, Request, Response
from fastapi_users import BaseUserManager, IntegerIDMixin

from .models import User

from .utils import get_user_db
from ..config import SECRET_TOKEN

SECRET = SECRET_TOKEN


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        return RedirectResponse('/tasks', status_code=status.HTTP_302_FOUND)

    async def on_after_forgot_password(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")

    async def on_after_login(
        self,
        user: User,
        request: Optional[Request] = None,
        response: Optional[Response] = None,
    ):
        print(f"User {user.id} logged in.")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
