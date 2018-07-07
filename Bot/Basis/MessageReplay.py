# -*- coding: utf-8 -*-
from inspect import getframeinfo, currentframe
from threading import Thread
import os
import importlib

import vk_api

from Bot.Basis.YandexGoogle.YandexApi import voice_processing
from Bot.Basis.command_system import command_list


def uploadFile(filePath, peer_id, title, vkApi):
    typeFile = {1: 'doc'}

    upload = vk_api.VkUpload(vkApi)
    fileInfo = upload.document_message(filePath, title=title, peer_id=peer_id)
    return typeFile[fileInfo[0]['type']] + str(fileInfo[0]['owner_id']) + '_' + str(fileInfo[0]['id'])


def send_msg(vk, user_id, msg, attachment=None, keyboard=None):
    vk.messages.send(user_id=user_id, message=msg, attachment=attachment, keyboard=keyboard)


def send_sticker(vk, user_id, sticker_id):
    vk.messages.send(user_id=user_id, sticker_id=sticker_id)


def load_modules():
    filename = getframeinfo(currentframe()).filename
    filename = filename[:filename.rfind('/') + 1]
    files = os.listdir(filename + "Commands")
    modules = filter(lambda x: x.endswith('.py'), files)
    for m in modules:
        importlib.import_module("Commands." + m[0:-3])


def get_answer(values):
    message = values.item['body']
    if 'payload' in values.item:
        message = values.item['payload'].replace("\"", "")

    if 'attachments' in values.item:
        message = 'Я не понимаю, что ты от меня хочешь'
        if values.item['attachments'][0]['doc']['ext'] == 'ogg':
            url = values.item['attachments'][0]['doc']['url']
            message = voice_processing(url)

    values.message = message
    body = message.lower().split(" ")
    attachment = None
    key = None
    for c in command_list:
        if body[0] in c.keys:
            message, attachment, key = c.process(values)
            break

    if (not values.item['user_id'] in values.user_ids) & (body[0] != 'регистрация'):
        message, attachment, key = 'Тебе нужно зарегистрироваться! Просто напиши мне слово "Регистрация"', None, None

    return message, attachment, key


class MessageReplay(Thread):

    def __init__(self, values):
        Thread.__init__(self)
        self.values = values

    def run(self):
        load_modules()
        message, attachment, key = get_answer(self.values)
        send_msg(self.values.vkApi.get_api(), self.values.item['user_id'], message, attachment, key)
