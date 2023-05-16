import redis.asyncio
from fastapi_users.authentication import CookieTransport, AuthenticationBackend, RedisStrategy
from fastapi_users import FastAPIUsers
from .models import User
from .manager import get_user_manager


cookie_transport = CookieTransport(cookie_name='ToDoCookie', cookie_max_age=86400)

redis = redis.asyncio.from_url("redis://localhost:6379", decode_responses=True)


def get_redis_strategy() -> RedisStrategy:
    return RedisStrategy(redis, key_prefix='todo_app_users_token', lifetime_seconds=86400)


auth_backend = AuthenticationBackend(
    name="redis_auth_back",
    transport=cookie_transport,
    get_strategy=get_redis_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
current_active_user = fastapi_users.current_user(active=True)

