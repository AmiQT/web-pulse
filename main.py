import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv
from loguru import logger

from engine.monitor import monitor_state, MonitorEngine

# Load environment variable
load_dotenv()

async def ping_scheduler():
    logger.info("Scheduler mula beroperasi boss! Akan jalan setiap 60 saat ⏰")
    while True:
        try:
            await monitor_state.run_checks()
        except Exception as e:
            logger.error(f"Alamak, the scheduler pancit la: {e}")
        
        await asyncio.sleep(60)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Inisialisasi Global Service Sentinel...")
    bg_task = asyncio.create_task(ping_scheduler())
    
    yield
    
    logger.info("Shutting down... membersihkan aiohttp session 🧹")
    bg_task.cancel()
    await MonitorEngine.close_session()

app = FastAPI(title="Global Service Sentinel API", lifespan=lifespan)

from fastapi.responses import FileResponse

@app.get("/")
def get_dashboard_ui():
    return FileResponse("dashboard.html")

@app.get("/api/state")
def get_state():
    return {
        "status": "😎 All good. Sentinel sedang memerhati.",
        "dashboard_results": monitor_state.results
    }
