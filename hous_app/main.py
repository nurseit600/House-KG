from fastapi import FastAPI, HTTPException
from hous_app.api import house
import redis.asyncio as redis
from contextlib import asynccontextmanager
from hous_app.db.database import SessionLocal
from fastapi_limiter import FastAPILimiter
from sqlalchemy.orm import Session
import uvicorn
from hous_app.api import auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client = await init_redis()
    await FastAPILimiter.init(redis_client)
    yield
    await redis_client.close()

delivery_app = FastAPI(title="House KG", lifespan=lifespan)


delivery_app.include_router(house.house_router)
delivery_app.include_router(auth.auth_router)


async def init_redis():
    return redis.from_url('redis://localhost', encoding='utf-8', decode_responses=True)


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    uvicorn.run(delivery_app, host="127.0.0.1", port=8001)
