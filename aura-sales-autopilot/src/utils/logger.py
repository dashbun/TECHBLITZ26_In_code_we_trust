import os
import httpx
from datetime import datetime

LOG_BOT_TOKEN = os.getenv('TELEGRAM_LOG_BOT_TOKEN')
LOG_CHAT_ID = os.getenv('TELEGRAM_LOG_CHAT_ID')

ICONS = {
    'info': '📘',
    'ok': '✅',
    'warn': '⚠️',
    'error': '🚨'
}

def log(level, event, **kwargs):
    """Log to console and Telegram"""
    ts = datetime.now().strftime("%H:%M:%S")
    icon = ICONS.get(level, '📋')
    
    # Format details
    details = " ".join(f"{k}={v}" for k, v in kwargs.items())
    
    # Console log
    print(f"[{ts}] {level.upper():5} {event:20} {details}")
    
    # Telegram log (non-blocking)
    if LOG_BOT_TOKEN and LOG_CHAT_ID:
        msg = f"`[{ts}]` {icon} `{event.upper()}`\n{details}"
        try:
            httpx.post(
                f"https://api.telegram.org/bot{LOG_BOT_TOKEN}/sendMessage",
                json={
                    "chat_id": LOG_CHAT_ID,
                    "text": msg,
                    "parse_mode": "Markdown"
                },
                timeout=2
            )
        except:
            pass  # Never crash for logging
