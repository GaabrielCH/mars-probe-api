from fastapi import FastAPI

from app.routers.probes import router as probes_router

app = FastAPI(title="Mars Probe API", version="1.0.0")
app.include_router(probes_router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
