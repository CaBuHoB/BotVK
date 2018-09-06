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
        "color": color.value
    }


def queue_removing_buttons(queue):
    json.dumps({
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
    something_was_sent = False
    queues_to_delete = getDateDeletedTables(connect)
    for queue in queues_to_delete:
        queue_name, date, admin_id = queue[0], queue[1], queue[2]
        day, month, year = date.split('.')
        difference = (dt.datetime.now() - dt.datetime(int(year), int(month), int(day), 0, 0)).days
        if difference >= 0:
            if admin_id not in asked_about_queue_users:
                vk.messages.send(user_id=admin_id, message='Удалить очередь ' + queue_name + ' ?', \
                                 attachment=None, keyboard=queue_removing_buttons(queue))
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
            if not ask_about_queue_removal(self.vk, self.connect):
                time.sleep(86400)
            else:
                time.sleep(1800)
