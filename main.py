from fastapi import FastAPI
from starlette.middleware import Middleware
from api.course.block import block_router
from api.course.course import course_router
from api.course.section import course_secion_router
from api.users.users import user_router
from core.middlewear.authentication import AuthenticationMiddleware, AuthBackend

app = FastAPI(
    title="Course API",
    description="Course API",
    version="0.0.1",
    middleware=[
        Middleware(
            AuthenticationMiddleware,
            backend=AuthBackend()
        )
    ]
)
app.include_router(user_router)
app.include_router(course_router)
app.include_router(course_secion_router)
app.include_router(block_router)


from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis.asyncio.utils import from_url

@app.on_event("startup")
async def startup():
    redis = from_url("redis://redis_cache")
    FastAPICache.init(RedisBackend(redis), prefix="cache")