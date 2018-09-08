# -*- coding: utf-8 -*-
from datetime import datetime
from argparse import Namespace

import vk_api

from Bot.Basis import MessageReplay, QueueThread, TimetableNotifications
from Bot.Basis.Keyboards.getButtons import get_default_buttons
from Bot.Basis.DataBase.workWithDataBase import getConnect, getAllUsers
from Bot.Basis.Timetable.getSchedule import getTimetableDict

api_token = '890e1e0743f9afdcf2787f6338c1fd0bc73327a2aa398d8cd38d4e6fdb998b08b43f0a26b905bf25ae47b'
# api_token = '07bad0077791b970f09942de845145ae326dc6c6b3d89c03690b1240f4a4a033899cf96e5fa72d6a334bb'  # тестовый
vkApi = vk_api.VkApi(token=api_token)

connect = getConnect()
users = getAllUsers(connect)
messageFromAdmin = {}
timetableDict = getTimetableDict([5621, 5622, 5623])

# Установка главной клавиатуры всем пользователям
for user in users:
   vkApi.get_api().messages.send(user_id=user,
                                 message='Бот обновился. Ошибки исправлены, '
                                         'производительность повышена, посуда вымыта, '
                                         'мусор вынесен, теперь можно и чаю попить)',
                                 attachment=None,
                                 keyboard=get_default_buttons(Namespace(users=users), users_id=user))

notifications_thread = TimetableNotifications.TimetableNotifications(vkApi.get_api(), connect)
notifications_thread.start()

queue_thread = QueueThread.QueueThread(vkApi.get_api(), connect)
queue_thread.start()

while True:
    now = datetime.now().timetuple()
    if now[3] == 21 and now[4] == 0:
        timetableDict.update(getTimetableDict([5621, 5622, 5623]))

    try:
        conversations = vkApi.method('messages.getConversations', {'filter': 'unread'})
    except BaseException:
        continue
    
    for item in conversations['items']:
        user_id = item['conversation']['peer']['id']
        count = item['conversation']['unread_count']
        messages = vkApi.method('messages.getHistory', {'user_id': user_id, 'count': count})
        vkApi.method('messages.markAsRead', {'peer_id': user_id})
        for message in messages['items']:
            values = Namespace(vkApi=vkApi, item=message, connect=connect, users=users,
                               timetableDict=timetableDict, messageFromAdmin=messageFromAdmin)
            my_thread = MessageReplay.MessageReplay(values)
            my_thread.start()
