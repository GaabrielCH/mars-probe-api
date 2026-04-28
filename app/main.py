from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routers.probes import router as probes_router
from app.storage.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Mars Probe API", version="1.0.0", lifespan=lifespan)
app.include_router(probes_router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
