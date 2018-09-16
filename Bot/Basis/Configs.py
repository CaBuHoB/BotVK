import vk

from Bot.Basis.DataBase.workWithDataBase import getConnect, getAllUsers
from Bot.Basis.Timetable.getSchedule import getDate, getTimetableDict

token = '07bad0077791b970f09942de845145ae326dc6c6b3d89c03690b1240f4a4a033899cf96e5fa72d6a334bb'
confirmation_token = 'e10e7673'

connect = getConnect()
users = getAllUsers(connect)
messageFromAdmin = {}
isUpper = getDate()['isUpper']
timetableDict = getTimetableDict([5621, 5622, 5623])

session = vk.Session(token)
api = vk.API(session, v=5.85)