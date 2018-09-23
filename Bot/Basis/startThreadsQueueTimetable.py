import vk

from Bot.Basis.Threads import QueueThread, WeatherThread, TimetableNotifications
from Bot.Basis.Configs import token
from Bot.Basis.Functions.workWithDataBase import getAllUsers

users = getAllUsers()
session = vk.Session(token)
api = vk.API(session, v=5.85)

# Установка главной клавиатуры всем пользователям
# for user in users:
#     api.messages.send(user_id=user,
#                       message='Бот обновился. Ошибки исправлены, '
#                               'производительность повышена, посуда вымыта, '
#                               'мусор вынесен, теперь можно и чаю попить)',
#                       attachment=None,
#                       keyboard=get_default_buttons(Namespace(users=users), users_id=user))

api.messages.send(user_id=38081883, message='Бот обновился (:')
api.messages.send(user_id=388195126, message='Бот обновился :)')

notifications_thread = TimetableNotifications.TimetableNotifications(api)
notifications_thread.start()

queue_thread = QueueThread.QueueThread(api)
queue_thread.start()

weather_thread = WeatherThread.WeatherThread(api)
weather_thread.start()
