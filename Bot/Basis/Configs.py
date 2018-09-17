import vk

from Bot.Basis.DataBase.workWithDataBase import getConnect, getAllUsers
from Bot.Basis.Timetable.getSchedule import getDate, getTimetableDict

# Тестовый бот
token = '07bad0077791b970f09942de845145ae326dc6c6b3d89c03690b1240f4a4a033899cf96e5fa72d6a334bb'
confirmation_token = 'e10e7673'

# Основной бот
# token = '890e1e0743f9afdcf2787f6338c1fd0bc73327a2aa398d8cd38d4e6fdb998b08b43f0a26b905bf25ae47b'
# confirmation_token = 'c9a8cdcb'

users = getAllUsers()
messageFromAdmin = {}
isUpper = getDate()['isUpper']
timetableDict = getTimetableDict([5621, 5622, 5623])

session = vk.Session(token)
api = vk.API(session, v=5.85)
