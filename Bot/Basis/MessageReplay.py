# -*- coding: utf-8 -*-
from inspect import getframeinfo, currentframe
from threading import Thread
import os
import importlib

from Bot.Basis.YandexGoogle.YandexApi import voice_processing
from Bot.Basis.command_system import command_list


def send_msg(vk, user_id, msg, attachment=None, keyboard=None):
    vk.messages.send(user_id=user_id, message=msg, attachment=attachment, keyboard=keyboard)


def edit_msg(vk, peer_id, message_id, msg, attachment=None, keyboard=None):
    vk.messages.edit(peer_id=peer_id, message=msg, message_id=message_id, attachment=attachment, keyboard=keyboard)


def load_modules():
    filename = getframeinfo(currentframe()).filename
    filename = filename[:filename.rfind('/') + 1]
    files = os.listdir(filename + "Commands")
    modules = filter(lambda x: x.endswith('.py'), files)
    for m in modules:
        importlib.import_module("Commands." + m[0:-3])


def get_answer(item, vkApi):
    # message = "Прости, не понимаю тебя. Напиши 'помощь', чтобы узнать мои команды"
    message = item['body']
    if 'payload' in item:
        message = item['payload']

    if 'attachments' in item:
        message = 'Я не понимаю, что ты от меня хочешь'
        if item['attachments'][0]['doc']['ext'] == 'ogg':
            url = item['attachments'][0]['doc']['url']
            message = voice_processing(url)

    body = message.lower().split(" ")
    attachment = None
    key = None
    for c in command_list:
        if body[0] in c.keys:
            message, attachment, key = c.process(vkApi, message, item)
            break
    return message, attachment, key


class MessageReplay(Thread):

    def __init__(self, vkApi, item, connect):
        Thread.__init__(self)
        self.vkApi = vkApi
        self.item = item
        self.connect = connect

    def run(self):
        load_modules()
        message, attachment, key = get_answer(self.item, self.vkApi)
        send_msg(self.vkApi.get_api(), self.item['user_id'], message, attachment, key)
