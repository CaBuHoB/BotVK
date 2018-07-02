# -*- coding: utf-8 -*-

import vk_api
import time

from Bot.Basis import MessageReplay
from Bot.Basis.DataBase.DBWorker import getConnect

api_token = '890e1e0743f9afdcf2787f6338c1fd0bc73327a2aa398d8cd38d4e6fdb998b08b43f0a26b905bf25ae47b'
api_token = '07bad0077791b970f09942de845145ae326dc6c6b3d89c03690b1240f4a4a033899cf96e5fa72d6a334bb'  ##тестовый
vkApi = vk_api.VkApi(token=api_token)
vk = vkApi.get_api()

values = {'out': 0, 'count': 100, 'time_offset': 60}

connect = getConnect()

while True:
    response = vkApi.method('messages.get', values)
    if response['items']:
        values['last_message_id'] = response['items'][0]['id']
    for item in response['items']:
        my_thread = MessageReplay.MessageReplay(vkApi, item, connect)
        my_thread.start()
    time.sleep(1)
