from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database.supabase_client import SupabaseClient
from .bots.user_bot.telegram_user import TelegramUserBot
# Import other modules as needed...

app = FastAPI(title="Aura Sales Autopilot", version="1.0.0")

supabase = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Init DB, bots, etc.
    global supabase
    supabase = SupabaseClient()
    yield
    # Shutdown

app.router.lifespan_context = lifespan

@app.get("/")
async def root():
    return {"message": "Aura Sales Autopilot is running!"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
