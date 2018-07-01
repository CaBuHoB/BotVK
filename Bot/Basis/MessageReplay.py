# -*- coding: utf-8 -*-

from threading import Thread
import os
import importlib
from Bot.Basis.command_system import command_list


def send_msg(vk, user_id, msg, attachment=None, keyboard=None):
    vk.messages.send(user_id=user_id, message=msg, attachment=attachment, keyboard=keyboard)


def load_modules():
    files = os.listdir("Commands")
    modules = filter(lambda x: x.endswith('.py'), files)
    for m in modules:
        importlib.import_module("Commands." + m[0:-3])


def get_answer(item, vkApi):
    # message = "Прости, не понимаю тебя. Напиши 'помощь', чтобы узнать мои команды"
    message = item['body']
    if 'payload' in item:
        message = item['payload']
    body = message.lower().split(" ")
    attachment = None
    key = None
    for c in command_list:
        if body[0] in c.keys:
            message, attachment, key = c.process(vkApi, item)
            break
    return message, attachment, key


class MessageReplay(Thread):

    def __init__(self, vkApi, item):
        Thread.__init__(self)
        self.vkApi = vkApi
        self.item = item

    def run(self):
        load_modules()
        message, attachment, key = get_answer(self.item, self.vkApi)
        send_msg(self.vkApi.get_api(), self.item['user_id'], message, attachment, key)
