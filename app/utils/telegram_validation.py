import requests
from fastapi import HTTPException

def validate_telegram_token(bot_token: str):
    """Проверяет валидность токена через Telegram API"""
    url = f"https://api.telegram.org/bot{bot_token}/getMe"
    try:
        response = requests.get(url, timeout=5)
        if not response.json().get("ok"):
            raise HTTPException(
                status_code=400,
                detail="Invalid Telegram bot token"
            )
    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code=400,
            detail="Telegram API unavailable"
        )