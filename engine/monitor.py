import asyncio
import time
import json
from curl_cffi import requests
from loguru import logger
from engine.notifier import send_telegram_alert

class MonitorEngine:
    _session: requests.AsyncSession | None = None

    @classmethod
    async def get_session(cls) -> requests.AsyncSession:
        if cls._session is None:
            cls._session = requests.AsyncSession()
        return cls._session

    @classmethod
    async def close_session(cls):
        if cls._session:
            await cls._session.close()
            cls._session = None

    def __init__(self):
        self.results = {}
        self.failure_counts = {}
        self.targets = []

    def load_targets(self):
        try:
            with open("targets.json", "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Takleh baca targets.json la weh: {e}")
            return []

    async def check_target(self, target: str):
        session = await self.get_session()
        start_time = time.perf_counter()
        
        is_up = False
        status_code = None
        
        try:
            # Using curl_cffi with Chrome 120 impersonation to bypass Advanced WAFs
            response = await session.get(target, impersonate="chrome120", timeout=10)
            status_code = response.status_code
            if 200 <= status_code < 400:
                is_up = True
        except Exception as e:
            logger.error(f"Error ping {target}: {str(e)}")
            
        latency = int((time.perf_counter() - start_time) * 1000)
        
        self.results[target] = {
            "status_code": status_code,
            "latency_ms": latency,
            "availability": "UP" if is_up else "DOWN"
        }
        
        if is_up:
            self.failure_counts[target] = 0
            logger.info(f"✅ {target} is UP ({latency}ms, Status: {status_code})")
        else:
            self.failure_counts[target] = self.failure_counts.get(target, 0) + 1
            logger.warning(f"❌ {target} is DOWN! (Fail count: {self.failure_counts[target]})")
            
            if self.failure_counts[target] == 3:
                logger.critical(f"⚠️ 3 KALI GAGAL BERTURUT-TURUT! Hantar alert telegram untuk {target} sekarang!")
                asyncio.create_task(send_telegram_alert(target, session))

    async def run_checks(self):
        self.targets = self.load_targets()
        if not self.targets:
            logger.warning("Takde target nak monitor do. Check targets.json kau.")
            return
            
        logger.info(f"Dimulakan ping untuk {len(self.targets)} targets ⚡")
        tasks = [self.check_target(url) for url in self.targets]
        await asyncio.gather(*tasks)

monitor_state = MonitorEngine()
