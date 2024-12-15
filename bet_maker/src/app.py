from logging import config as logging_config

import aioredis
import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from db import redis
from api.v1 import bet, event
from core.config import settings
from core.logger import LOGGING
from core.http_client import http_client

logging_config.dictConfig(LOGGING)


origins = [
    "*",
]


app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup_event():
    await http_client.init_client()
    redis.redis = await aioredis.from_url(
        f"redis://{settings.redis_host}:{settings.redis_port}",
        encoding="utf-8",
        decode_responses=True
    )


@app.on_event("shutdown")
async def shutdown_event():
    await http_client.close_client()
    await redis.redis.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(bet.router, prefix="/api/v1/bets", tags=["bet"])
app.include_router(event.router, prefix="/api/v1/events", tags=["event"])


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=settings.project_host,
        port=settings.project_port,
        log_config=LOGGING,
    )