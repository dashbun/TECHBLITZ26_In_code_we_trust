from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.agents.sequence_engine import SequenceEngine
from src.api.routes import router as api_router

scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: launch APScheduler. Shutdown: stop it gracefully."""
    engine = SequenceEngine()

    # Run sequence step checks every hour
    scheduler.add_job(engine.check_due_steps, "interval", hours=1, id="sequence_check")
    scheduler.start()

    yield

    scheduler.shutdown(wait=False)


app = FastAPI(
    title="Aura Sales Autopilot",
    version="1.0.0",
    description="Backend for the Aura Sales dashboard and Telegram/WhatsApp bots.",
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# CORS — allow the Vite frontend dev server (and deployed origins)
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # Vite default
        "http://localhost:3000",   # CRA / alternative
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Route registration
# ---------------------------------------------------------------------------
app.include_router(api_router)


@app.get("/", tags=["health"])
async def root():
    return {"message": "Aura Sales Autopilot is running!"}


@app.get("/health", tags=["health"])
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
