import telegram
import tools
import os
from fastapi import FastAPI
import aiohttp


app = FastAPI()
bot_token = os.environ['BOT_TOKEN']
telegram_api_url = f'https://api.telegram.org/bot{bot_token}/getUpdates'


@app.get('/send_notification')
async def send_notification(chat_name: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(telegram_api_url) as resp:
            print(resp.status)
            chat_id = tools.get_chat_id(await resp.json(), chat_name)
            if not chat_id:
                return {'err': 'can not find chat'}
            bot = telegram.Bot(token=bot_token)
            bot.sendMessage(chat_id=chat_id, text='alarm\nArmen')
            return {'result': 'fine'}
