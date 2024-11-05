from contextlib import asynccontextmanager

from core.config import settings
from core.models import Base, db_helper
from fastapi import FastAPI
import uvicorn
from items_views import router as items_router
from users.views import router as users_router
from api_v1 import router as router_v1


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router_v1, prefix=settings.api_v1_prefix)
app.include_router(items_router, tags=["items"])
app.include_router(users_router)


@app.get("/")
def hello_index():
    return {"message": "Hello index!"}


@app.get("/hello/")
def hello_world(name: str = "World"):
    name = name.strip().title()
    return {"name": f"Hello, {name}!"}


@app.get("/calc/add/")
def add(a: int, b: int):
    return {"a": a, "b": b, "result": a + b}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
