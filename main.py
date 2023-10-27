from functools import lru_cache
import httpx
import requests

from fastapi import FastAPI, Depends, Request
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi_security_telegram_webhook import OnlyTelegramNetworkWithSecret
from database.database import get_db
from init_service import init_services
from services.process_chat_service import ProcessChatService


# from routers import todos

import config
from utils.strings import convert_to_url

app = FastAPI()
secret = config.Settings().telegram_webhook_secret
webhook_security = OnlyTelegramNetworkWithSecret(
    real_secret=secret)

client = httpx.AsyncClient()


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    print(f"{repr(exc)}")
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@lru_cache()
def get_settings():
    return config.Settings()


@app.get("/")
def read_root(settings: config.Settings = Depends(get_settings)):
    print(settings.app_name)
    return "Hello World"


@app.post("/webhook/{secret}", dependencies=[Depends(webhook_security)])
async def webhook(request: Request, settings: config.Settings = Depends(get_settings), session=Depends(get_db)):
    chat_service = init_services(session)
    data = await request.json()
    chat_id = data['message']['chat']['id']

    BASE_URL = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"

    return_text = chat_service.process(data)

    payload = {
        'chat_id': chat_id,
        'text': return_text
    }

    requests.post(BASE_URL, json=payload)


@app.post("/test")
async def webhook(request: Request, settings: config.Settings = Depends(get_settings), session=Depends(get_db)):
    chat_service = init_services(session)
    data = await request.json()

    return_text = chat_service.process(data)
    return return_text
