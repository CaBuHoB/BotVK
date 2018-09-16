# -*- coding: utf-8 -*-
from datetime import datetime
from argparse import Namespace

import sys
import argparse
import vk_api

from Bot.Basis import MessageReplay, QueueThread
from Bot.Basis.Timetable import TimetableNotifications
from Bot.Basis.Keyboards.getButtons import get_default_buttons
from Bot.Basis.DataBase.workWithDataBase import getConnect, getAllUsers, getSubscribedUsers, unSubscribePerson
from Bot.Basis.Timetable.getSchedule import getTimetableDict


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-token', nargs='?',
                        default='07bad0077791b970f09942de845145ae326dc6c6b3d89c03690b1240f4a4a033899cf96e5fa72d6a334bb')

    return parser


def resetStatements(users):
    usersInGroup = vkApi.method('groups.getMembers', {'group_id': str(168330527)})['items']
    # Зареган, но не в группе => отписать от рассылки и удалить локально из юзеров, чтоб им лишнего не приходило
    # (Оставить в БД, чтоб когда вступит обратно не регался второй раз)
    for user in users:
        if user not in usersInGroup:
            if user in getSubscribedUsers(connect):
                unSubscribePerson(connect, user)
            users.pop(user)

    registrated_users = getAllUsers(connect)
    # В группе, зареган, но не записан в юзерах (пользователь удалился из группы, а потом венулся)
    # Возвращаем его в локальные юзеры из БД
    for user in usersInGroup:
        if user not in users and user in registrated_users:
            users.setdefault(registrated_users[user])

    return usersInGroup, users


parser = createParser()
namespace = parser.parse_args(sys.argv[1:])
api_token = namespace.token

vkApi = vk_api.VkApi(token=api_token)

connect = getConnect()
users = getAllUsers(connect)
messageFromAdmin = {}
timetableDict = getTimetableDict([5621, 5622, 5623])
materials = vkApi.method('docs.search', {'q': '>', 'search_own': 1, 'count': 200})['items']

usersInGroup, users = resetStatements(users)

# Установка главной клавиатуры всем пользователям
#for user in users:
#    if (vkApi.method('groups.isMember', {'group_id': str(168330527), 'user_id': user}) == 1):
#        vkApi.get_api().messages.send(user_id=user,
#                                  message='Бот обновился. Ошибки исправлены, '
#                                          'производительность повышена, посуда вымыта, '
#                                          'мусор вынесен, теперь можно и чаю попить)',
#                                  attachment=None,
#                                  keyboard=get_default_buttons(Namespace(users=users), users_id=user))

notifications_thread = TimetableNotifications.TimetableNotifications(vkApi.get_api(), connect)
notifications_thread.start()

queue_thread = QueueThread.QueueThread(vkApi.get_api(), connect)
queue_thread.start()

while True:
    now = datetime.now().timetuple()
    if now[3] == 21 and now[4] == 0:
        timetableDict.update(getTimetableDict([5621, 5622, 5623]))
        usersInGroup, users = resetStatements(users)

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
                               timetableDict=timetableDict, messageFromAdmin=messageFromAdmin,
                               materials=materials, usersInGroup=usersInGroup)
            my_thread = MessageReplay.MessageReplay(values)
            my_thread.start()
