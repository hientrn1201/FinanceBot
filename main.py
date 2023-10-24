from functools import lru_cache
import httpx

from fastapi import FastAPI, Depends, Request
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi_security_telegram_webhook import OnlyTelegramNetworkWithSecret

# from routers import todos

import config

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
    print(settings)
    return "Hello World"


@app.post("/webhook/{secret}", dependencies=[Depends(webhook_security)])
async def webhook(request: Request, settings: config.Settings = Depends(get_settings)):
    data = await request.json()
    chat_id = data['message']['chat']['id']
    text = data['message']['text']

    BASE_URL = f"https://api.telegram.org/bot{settings.telegram_bot_token}/"

    await client.get(f"{BASE_URL}sendMessage?chat_id={chat_id}&text={text}")
