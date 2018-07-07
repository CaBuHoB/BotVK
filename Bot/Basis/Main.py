# -*- coding: utf-8 -*-
from argparse import Namespace

import vk_api

from Bot.Basis import MessageReplay
from Bot.Basis.DataBase.DBWorker import getConnect

api_token = '890e1e0743f9afdcf2787f6338c1fd0bc73327a2aa398d8cd38d4e6fdb998b08b43f0a26b905bf25ae47b'
api_token = '07bad0077791b970f09942de845145ae326dc6c6b3d89c03690b1240f4a4a033899cf96e5fa72d6a334bb'  # тестовый
vkApi = vk_api.VkApi(token=api_token)
vk = vkApi.get_api()

connect = getConnect()
users = {38081883: {'name': 'Максим', 'surname': 'Савинов', 'group': 5621}}
# TODO создать функцию getAllUsers из БД

while True:
    conversations = vkApi.method('messages.getConversations', {'filter': 'unread'})

    for item in conversations['items']:
        user_id = item['conversation']['peer']['id']
        count = item['conversation']['unread_count']
        messages = vkApi.method('messages.getHistory', {'user_id': user_id, 'count': count})
        vkApi.method('messages.markAsRead', {'peer_id': user_id})
        for message in messages['items']:
            values = Namespace(vkApi=vkApi, item=message, connect=connect, users=users)
            my_thread = MessageReplay.MessageReplay(values)
            my_thread.start()
    # time.sleep(200)
