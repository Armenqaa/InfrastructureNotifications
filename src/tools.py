from enum import Enum
import json


class TypeOfChat(str, Enum):
    private = 'private',
    group = 'group'


def get_chat_id(json_data: json, chat_name: str) -> int | None:
    """
    Get chat id by name of chat and chat type
    :param json_data: response by telegram's api
    :param chat_name: name of chat
    :param chat_type: type of chat
    :return: chat id or None
    """
    if chat_name.startswith('@'):
        chat_type = TypeOfChat.private
        chat_name = chat_name[1:]
    else:
        chat_type = TypeOfChat.group
    for elem in json_data['result']:
        if 'message' in elem:
            chat = elem['message']['chat']
            if chat['type'] == chat_type:
                if ('username' in chat and chat['username'] == chat_name) \
                        or ('title' in chat and chat['title'] == chat_name):
                    return chat['id']
