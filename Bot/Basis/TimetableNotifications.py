# -*- coding: utf-8 -*-
import datetime as dt
from argparse import Namespace
from threading import Thread

import time

from Bot.Basis.DataBase.workWithDataBase import getSubscribedUsers, getAllUsers
from Bot.Basis.Keyboards.getButtons import get_default_buttons
from Bot.Basis.Timetable.getSchedule import getDate, getTimetableByDay, getTimetableDict


def send_day_timetable(vk, connect):
    users = getAllUsers(connect)
    timetable_dict = getTimetableDict([5621, 5622, 5623])
    is_upper = getDate()['isUpper']
    week = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    day_number = (dt.datetime.weekday(dt.datetime.now()) + 1) % 7
    if day_number == 0:
        is_upper = not is_upper

    for user in getSubscribedUsers(connect):
        message = getTimetableByDay(timetable_dict, users[user]['group'],
                                    week[day_number], is_upper)
        if message == '':
            continue
        message = 'Расписание на завтра:\n\n' + message
        vk.messages.send(user_id=user, message=message, attachment=None,
                         keyboard=get_default_buttons(Namespace(users=users)))


def send_subject_notification(vk, connect, subject):
    users = getAllUsers(connect)
    timetable_dict = getTimetableDict([5621, 5622, 5623])
    is_upper = getDate()['isUpper']
    week = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    day_number = dt.datetime.weekday(dt.datetime.now())

    for group in range(5621, 5624):
        timetable = timetable_dict[str(group)][week[day_number]]
        if subject in timetable:
            for sub in timetable[subject]:
                if sub['isUpper'] == is_upper or sub['isUpper'] is None:
                    message = 'Через 15 минут начнется пара: '
                    message += sub['type'] + ' - ' + sub['name'] + ' '
                    message += '(' + sub['teacher'] + ')\n'
                    message += sub['lecture hall'] + ' (' + ', '.join((group for group in sub['group'])) + ')\n'
                    for user in getSubscribedUsers(connect):
                        if user in users:
                            if users[user]['group'] == group:
                                vk.messages.send(user_id=user, message=message, attachment=None,
                                                 keyboard=get_default_buttons(Namespace(users=users)))


class TimetableNotifications(Thread):

    def __init__(self, vk, connect):
        Thread.__init__(self)
        self.vk = vk
        self.connect = connect
        self.timeList = {'1 пара (9:00-10:30)': [8, 45],
                         '2 пара (10:40-12:10)': [10, 25],
                         '3 пара (12:20-13:50)': [12, 5],
                         '4 пара (14:10-15:40)': [13, 55],
                         '5 пара (15:50-17:20)': [15, 35],
                         '6 пара (17:30-19:00)': [17, 15]}

    def run(self):
        while True:
            now = dt.datetime.now().timetuple()

            if (now[3] == 21) and (0 <= now[4] <= 5):
                send_day_timetable(self.vk, self.connect)
                time.sleep(41000)
            now = dt.datetime.now().timetuple()

            for sub in self.timeList:
                if (now[3] == self.timeList[sub][0]) & (now[4] == self.timeList[sub][1]):
                    send_subject_notification(self.vk, self.connect, sub)
                    time.sleep(5400)
