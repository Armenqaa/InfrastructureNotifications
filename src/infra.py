import telegram
import tools
import os
import ast
from fastapi import FastAPI
from pydantic import BaseModel
import aiohttp
import pickle


def load_all_items():
    with open('.mapping', 'rb') as mapping:
        while True:
            try:
                chat_name_and_id = pickle.load(mapping)
                chat_names[chat_name_and_id[0]] = chat_name_and_id[1]
            except EOFError:
                break


chat_names = {}
load_all_items()
app = FastAPI()
bot_token = os.environ['BOT_TOKEN']
telegram_api_url = f'https://api.telegram.org/bot{bot_token}/getUpdates'
subs_api_url = 'http://notificationsubscribers_subs_1:8000/receive_subscribers'


@app.get('/')
async def root():
    return {'message': f'{chat_names}'}


async def get_subscribers(name_of_notification: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{subs_api_url}?name_of_notification={name_of_notification}') as resp:
            return await resp.json()


class Notification(BaseModel):
    name: str
    text: str


@app.put('/send_notification')
async def send_notification(notification: Notification):
    async with aiohttp.ClientSession() as session:
        async with session.get(telegram_api_url) as resp:
            chats = await get_subscribers(notification.name)
            response = []
            print(chat_names)
            for chat in ast.literal_eval(chats['result']):
                chat_name = chat['address']
                if chat_name in chat_names:
                    chat_id = chat_names[chat_name]
                else:
                    chat_id = tools.get_chat_id(await resp.json(), chat_name, chat_names)
                if not chat_id:
                    response.append({'err': 'can not find chat'})
                else:
                    bot = telegram.Bot(token=bot_token)
                    bot.sendMessage(chat_id=chat_id, text=f'{notification.name}\n\n{notification.text}')
                    response.append({'result': 'fine'})
            return response
