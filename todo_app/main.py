from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends
from .auth.config import fastapi_users, auth_backend, current_active_user
from .auth.schemas import UserRead, UserCreate, UserUpdate
from .auth.models import User
from .routers.color import router as router_color
from .routers.category import router as router_category
from .routers.theme import router as router_theme
from .routers.task import router as router_task
from .pages.views import router as router_page
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title='ToDoApp'
)
#TODO: schema for update
#TODO: preload data for update endpoint



origins = [
    "http://localhost:8000",
    "http://localhost:8080",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

app.mount("/static", StaticFiles(directory="todo_app/static"), name="static")

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/redis",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

app.include_router(router_color)
app.include_router(router_category)
app.include_router(router_theme)
app.include_router(router_task)
app.include_router(router_page)
# for test
@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}