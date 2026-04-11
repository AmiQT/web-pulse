# 🛰️ Global Service Sentinel

A high-performance, real-time remote service monitoring and alerting tool. Built with modern SRE (Site Reliability Engineering) principles to track the availability of mission-critical assets.

![Dashboard Preview](https://img.shields.io/badge/UI-Glassmorphism-66fcf1) ![Python](https://img.shields.io/badge/Python-3.12%2B-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-Modern-009688)

## ✨ Key Features

- **Blazing Fast Concurrency**: Utilizes `asyncio` and FastAPI to ping multiple targets concurrently without blocking the main event loop.
- **Advanced WAF Bypass**: Uses `curl_cffi` to perfectly impersonate Google Chrome's TLS/SSL Fingerprint (JA3), allowing the Sentinel to monitor targets protected by strict Web Application Firewalls (e.g., Cloudflare, Imperva, F5) that block generic HTTP clients.
- **Smart Alerting System**: Integrates seamlessly with Telegram bots. Implements a "3-strike" failure logic to prevent alert fatigue and spam before dispatching an emergency notification.
- **Real-Time Telemetry Dashboard**: A beautifully designed, zero-dependency, glassmorphism frontend that polls background metrics dynamically every 3 seconds.

## 📂 Project Structure

```text
web-pulse/
├── engine/
│   ├── __init__.py       
│   ├── monitor.py        # Core asynchronous ping engine and state manager
│   └── notifier.py       # Telegram notification dispatcher
├── .env                  # Secrets for Telegram API (Not committed to Git)
├── dashboard.html        # Responsive real-time frontend dashboard
├── main.py               # FastAPI entry point, background jobs, and API routes
├── render.yaml           # Blueprint for seamless Render.com cloud deployment
├── requirements.txt      # Python dependencies
└── targets.json          # Configuration file containing URLs to monitor
```

## 🛠️ Tech Stack

- **Backend**: Python 3.12+, FastAPI, Uvicorn
- **Networking**: `curl_cffi` (for advanced TLS impersonation)
- **Logging**: `loguru` (for clean, structured server logs)
- **Frontend**: Vanilla HTML5, CSS3 (No build step required)

## 🚀 Quick Start (Local Setup)

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd web-pulse
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables:**
   Create a `.env` file in the root directory and add your Telegram credentials:
   ```env
   TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
   TELEGRAM_CHAT_ID="your_telegram_chat_id"
   ```

4. **Add Monitoring Targets:**
   Edit the `targets.json` file with the URLs you wish to monitor:
   ```json
   [
     "https://www.google.com",
     "https://www.github.com"
   ]
   ```

5. **Spin up the Sentinel:**
   ```bash
   uvicorn main:app --reload
   ```
   *The real-time dashboard will now be accessible at `http://localhost:8000/`*

## ☁️ Cloud Deployment (Render)

This project is configured for one-click deployment via **Render**.
1. Push your code to GitHub.
2. Link the repository to your Render account.
3. Render will automatically detect the `render.yaml` blueprint and configure the Web Service.
4. Manually add `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` as Environment Variables in the Render Dashboard.
5. **Keep-Alive Note**: Render Free Tier sleeps after 15 minutes of inactivity. Use an external ping service like [UptimeRobot](https://uptimerobot.com/) to ping your deployed URL every 5 minutes to prevent cold starts.

---
*Built with ❤️ for High Availability and Peace of Mind.*
