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
                         keyboard=get_default_buttons(Namespace(users=users), users_id=user))


def send_subject_notification(vk, connect, subject):
    users = getAllUsers(connect)
    timetable_dict = getTimetableDict([5621, 5622, 5623])
    is_upper = getDate()['isUpper']
    week = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    day_number = dt.datetime.weekday(dt.datetime.now())

    for group in range(5621, 5624):
        if week[day_number] in timetable_dict[str(group)]:
            timetable = timetable_dict[str(group)][week[day_number]]
            if subject in timetable:
                for sub in timetable[subject]:
                    if sub['isUpper'] == is_upper or sub['isUpper'] is None:
                        message = '🕓 '
                        message += sub['type'] + ' ('
                        message += sub['lecture hall'] + ') - ' + sub['name'] + ' '
                        message += '(' + sub['teacher'] + ')'
                        message += ' - начнётся через 15 минут'
                        for user in getSubscribedUsers(connect):
                            if users[user]['group'] == group:
                                vk.messages.send(user_id=user, message=message, attachment=None,
                                                 keyboard=get_default_buttons(Namespace(users=users),
                                                                              users_id=user))


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
            # По списку предметов, так как они в дне раньше
            for sub in self.timeList:
                now = dt.datetime.now()
                then = dt.datetime(now.timetuple()[0], now.timetuple()[1], now.timetuple()[2],
                                   self.timeList[sub][0], self.timeList[sub][1])
                difference = (then - now).total_seconds()
                if difference < 0:  # если прошло нужное время в этом дне
                    continue
                else:
                    if difference >= 0:  # если это время еще не прошло и нужно ждать
                        time.sleep(difference)  # Сон до следующего предмета
                    send_subject_notification(self.vk, self.connect, sub)

            # Вечерняя рассылка
            now = dt.datetime.now()
            then = dt.datetime(now.timetuple()[0], now.timetuple()[1], now.timetuple()[2], 21, 0)
            difference = (then - now).total_seconds()

            if difference < 0:  # если в этом дне время рассылки прошло
                                  # заснуть до 0:01, начать цикл заново
                now += dt.timedelta(1)
                then = dt.datetime(now.timetuple()[0], now.timetuple()[1], now.timetuple()[2], 0, 1)
                now -= dt.timedelta(1)
                time.sleep((then - now).total_seconds())  # Сон до 00:01
            else:
                if difference >= 0:
                    time.sleep(difference)
                send_day_timetable(self.vk, self.connect)
