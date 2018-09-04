# -*- coding: utf-8 -*-
import datetime as dt
from datetime import datetime, timedelta
from argparse import Namespace

import vk_api

from Bot.Basis import MessageReplay
from Bot.Basis.Keyboards.GetButtons import getDefaultScreenButtons, queueDeleteButtons
from Bot.Basis.DataBase.workWithDataBase import getConnect, getAllUsers, getDateDeletedTables, getSubscribedUsers
from Bot.Basis.Timetable.getSchedule import getDate, getTimetableDict, getTimetableByDay

api_token = '890e1e0743f9afdcf2787f6338c1fd0bc73327a2aa398d8cd38d4e6fdb998b08b43f0a26b905bf25ae47b'
# api_token = '07bad0077791b970f09942de845145ae326dc6c6b3d89c03690b1240f4a4a033899cf96e5fa72d6a334bb'  # тестовый
vkApi = vk_api.VkApi(token=api_token)
vk = vkApi.get_api()

connect = getConnect()
users = getAllUsers(connect)
messageFromAdmin = {}
timetableDict = getTimetableDict([5621, 5622, 5623])
appealsForQueueDelete = []
# Очередь: Предмет_Группы_Дата
# Документы: > Предмет Номер

now_ = datetime.now().timetuple()
sendingScheduleTime = dt.datetime(now_[0], now_[1], now_[2], 21, 0)

# Установка главной клавиатуры всем пользователям
for user in users:
   vk.messages.send(user_id=user, message='Бот обновился. Ошибки исправлены, \
       производительность повышена, посуда вымыта, мусор вынесен, теперь можно и чаю попить)', \
           attachment=None, keyboard=getDefaultScreenButtons(Namespace(users=users), id=user))

while True:
    # Рассылка расписания
    isUpper = getDate()['isUpper']
    week = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    dayWeek = (datetime.weekday(datetime.now()) + 1) % 7
    if dayWeek == 0:
        isUpper = not isUpper
    now = datetime.now()
    _message = 'Расписание на завтра:\n\n'
    if (sendingScheduleTime - now).days < 0:
        for user in getSubscribedUsers(connect):
            message = getTimetableByDay(timetableDict, users[user]['group'], \
                                        week[dayWeek], isUpper)
            if message == '':
                message = 'Выходной!)'
            vk.messages.send(user_id=user, message=message, attachment=None, \
                             keyboard=getDefaultScreenButtons(Namespace(users=users), id=user))
        sendingScheduleTime += timedelta(1)

    # Проверка очередей на удаление
    queuesToDelete = getDateDeletedTables(connect)
    for queue in queuesToDelete:
        queue_name, date, admin_id = queue[0], queue[1], queue[2]
        day, month, year = date.split('.')
        difference = (now - dt.datetime(int(year), int(month), int(day), 0, 0)).days
        if (difference >= 0) and (queue_name not in appealsForQueueDelete):
            appealsForQueueDelete.append(queue_name)
            vk.messages.send(user_id=admin_id, message='Удалить очередь ' + queue_name + ' ?', \
                    attachment=None, keyboard=queueDeleteButtons(admin_id))

    # Обработка сообщений
    conversations = vkApi.method('messages.getConversations', {'filter': 'unread'})
    for item in conversations['items']:
        user_id = item['conversation']['peer']['id']
        count = item['conversation']['unread_count']
        messages = vkApi.method('messages.getHistory', {'user_id': user_id, 'count': count})
        vkApi.method('messages.markAsRead', {'peer_id': user_id})
        for message in messages['items']:
            values = Namespace(vkApi=vkApi, item=message, connect=connect, users=users,
                               timetableDict=timetableDict, messageFromAdmin=messageFromAdmin,
                               appealsForQueueDelete=appealsForQueueDelete)
            my_thread = MessageReplay.MessageReplay(values)
            my_thread.start()
