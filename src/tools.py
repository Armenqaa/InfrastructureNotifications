import pickle
from enum import Enum
import json


class TypeOfChat(str, Enum):
    telegram_private = 'private',
    telegram_group = 'group'
    email = 'email'


def get_chat_id(json_data: json, chat_name: str, chat_names: dict) -> int | None:
    """
    Get chat id by name of chat and chat type
    :param json_data: response by telegram's api
    :param chat_name: name of chat
    :param chat_type: type of chat
    :param chat_names chat names that stored in .mapping
    :return: chat id or None
    """
    if chat_name.startswith('@'):
        chat_type = TypeOfChat.telegram_private
    else:
        chat_type = TypeOfChat.telegram_group

    for elem in json_data['result']:
        if 'message' in elem:
            chat = elem['message']['chat']
            if chat['type'] == chat_type:
                if ('username' in chat and chat['username'] == chat_name[1:]) \
                        or ('title' in chat and chat['title'] == chat_name):
                    chat_names[chat_name] = chat['id']
                    with open('.mapping', 'ab') as mapping:
                        pickle.dump((chat_name, chat['id']), mapping)
                    return chat['id']
