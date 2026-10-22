import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api import auth, vault
from app.core.limiter import limiter
from app.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    # session_id -> encryption key (bytes). Cleared on restart by design.
    app.state.sessions = {}
    yield
    app.state.sessions.clear()


app = FastAPI(
    title="Local Password Manager",
    version="1.0.0",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(auth.router)
app.include_router(vault.router)

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))