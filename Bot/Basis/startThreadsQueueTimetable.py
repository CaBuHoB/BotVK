from argparse import Namespace

import vk

from Bot.Basis import QueueThread
from Bot.Basis.DataBase.workWithDataBase import getConnect, getAllUsers
from Bot.Basis.Keyboards.getButtons import get_default_buttons
from Bot.Basis.Timetable import TimetableNotifications

token = '890e1e0743f9afdcf2787f6338c1fd0bc73327a2aa398d8cd38d4e6fdb998b08b43f0a26b905bf25ae47b'

users = getAllUsers()

session = vk.Session(token)
api = vk.API(session, v=5.85)

# Установка главной клавиатуры всем пользователям
for user in users:
    api.messages.send(user_id=user,
                      message='Бот обновился. Ошибки исправлены, '
                              'производительность повышена, посуда вымыта, '
                              'мусор вынесен, теперь можно и чаю попить)',
                      attachment=None,
                      keyboard=get_default_buttons(Namespace(users=users), users_id=user))

notifications_thread = TimetableNotifications.TimetableNotifications(api)
notifications_thread.start()

queue_thread = QueueThread.QueueThread(api)
queue_thread.start()
queue_thread.join()
