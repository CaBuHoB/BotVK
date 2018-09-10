# -*- coding: utf-8 -*-
import datetime as dt
import json
import time
from threading import Thread

from Bot.Basis.DataBase.workWithDataBase import getDateDeletedTables

asked_about_queue_users = []


def in_asked_list(admin_id):
    return admin_id in asked_about_queue_users


def remove_from_asked_list(admin_id):
    if admin_id in asked_about_queue_users:
        asked_about_queue_users.remove(admin_id)


def get_button(label, payload, color):
    return {
        "action": {"type": "text",
                   "payload": json.dumps(payload, ensure_ascii=False),
                   "label": label},
        "color": color
    }


def queue_removing_buttons(queue):
    return json.dumps({
        "one_time": False,
        "buttons": [
            [
                get_button('Удалить очередь', 'removeQueue ' + queue, 'negative')
            ],
            [
                get_button('Перенести удаление на три дня', 'rewriteQueueDelete ' + queue, 'positive')
            ]
        ]
    }, ensure_ascii=False)


def ask_about_queue_removal(vk, connect):
    queues_to_delete = getDateDeletedTables(connect)

    something_was_sent = False
    for queue in queues_to_delete:
        queue_name, date, admin_id = queue[0], queue[1], queue[2]
        day, month, year = date.split('.')
        difference = (dt.datetime.now() - dt.datetime(int(year), int(month), int(day), 10, 0)).days
        if difference >= 0:
            if admin_id not in asked_about_queue_users:
                vk.messages.send(user_id=admin_id, message='Удалить очередь ' + queue_name + ' ?',
                                 attachment=None, keyboard=queue_removing_buttons(queue_name))
                asked_about_queue_users.append(admin_id)
            something_was_sent = True
    return something_was_sent


class QueueThread(Thread):

    def __init__(self, vk, connect):
        Thread.__init__(self)
        self.vk = vk
        self.connect = connect

    def run(self):
        while True:
            someone_was_asked = ask_about_queue_removal(self.vk, self.connect)

            now = dt.datetime.now()
            then = dt.datetime(now.timetuple()[0], now.timetuple()[1], now.timetuple()[2], 10, 0)

            if (then - now).total_seconds() <= 0:
                then += dt.timedelta(1)
            difference = int((then - now).total_seconds())  # время до 22.00

            if not someone_was_asked:
                time.sleep(difference)  # Спит до следующих 22.00
            else:
                sleep_time = min(1800, difference)
                time.sleep(sleep_time)  # Кого-то спросили об удалении и он еще не ответил, спим полчаса,
                # вдруг у него ещё есть очереди, о которых нужно сегодня спросить
