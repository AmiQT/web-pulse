import os
from curl_cffi import requests
from loguru import logger

async def send_telegram_alert(target: str, session: requests.AsyncSession = None):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id or token == "your_token_here":
        logger.warning("💀 Telegram bot token atau chat ID takde weh! Alert terpaksa di-cancel-kan. Check .env kau!")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": f"🚨 Peringatan Global Service Sentinel:\nWebsite {target} is DOWN untuk 3 kali check berturut-turut! Pegi check server sekarang!"
    }
    
    try:
        if session:
            response = await session.post(url, json=payload)
            if response.status_code == 200:
                logger.success(f"📲 Pesanan kecemasan berjaya dihantar ke Telegram untuk {target}!")
            else:
                logger.error(f"Gagal hantar alert. Status: {response.status_code}")
        else:
            async with requests.AsyncSession() as fallback_sess:
                response = await fallback_sess.post(url, json=payload)
                logger.info("Telegram alert dihantar guna fallback session.")
    except Exception as e:
        logger.error(f"Aduh, error time nak hantar Telegram alert: {e}")
