# -*- coding: utf-8 -*-
from inspect import getframeinfo, currentframe
from threading import Thread
import os
import importlib
import vk_api

from Bot.Basis.Keyboards.getButtons import get_choose_group_buttons, get_default_buttons, \
    get_asking_if_send_message_buttons
from Bot.Basis.YandexGoogle.YandexApi import voice_processing
from Bot.Basis.command_system import command_list


def upload_file(filePath, peer_id, title, vkApi):
    typeFile = {1: 'doc', 4: 'photo', 6: 'video'}

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
    message = values.item['text']
    if 'payload' in values.item:
        message = values.item['payload'].replace("\"", "")
    body = message.lower().split()
    from_id = values.item['from_id']
    
    # Пользователь не участник группы
    if (values.vkApi.method('groups.isMember', {'group_id': str(168330527), 'user_id': from_id}) == 1):
        return 'Для общения с ботом вступи в группу!', None, None

    # Пользователь не зарегистрирован
    if (from_id not in values.users) and (body[0] != 'shownameslist') and (body[0] != 'endofregistration')\
            and (body[0] != 'erroringroupchoosing'):
        return 'Тебе нужно зарегистрироваться! Выбери свою группу:', None, get_choose_group_buttons()

    # Сообщение от пользователя отправлено в рассылку ?
    if (from_id in values.messageFromAdmin) and (body[0] != 'infosendmessage') \
            and (body[0] != 'backtodefaultkeyboard') \
            and (body[0] != 'infobygroup'):
        values.messageFromAdmin[from_id]['message'] = values.item
        groups = values.messageFromAdmin[from_id]['groups']
        message = 'Сделать рассылку группам: ' + ' '.join(groups) + '?'
        return message, None, get_asking_if_send_message_buttons()

    # Обработка аудио/вложений
    if len(values.item['attachments']) > 0:
        message = 'Я не понимаю, чего ты от меня хочешь. Чтобы узнать, ' \
                  'что я умею, нажми на зелёную кнопку со знаком вопроса'
        if values.item['attachments'][0]['doc']['ext'] == 'ogg':
            url = values.item['attachments'][0]['doc']['url']
            message = voice_processing(url)

    # Обработка команд
    values.message = message
    body = message.lower().split()
    attachment = None
    key = get_default_buttons(values)
    for c in command_list:
        if body[0] in c.keys:
            message, attachment, key = c.process(values)
            break

    return message, attachment, key


class MessageReplay(Thread):

    def __init__(self, values):
        Thread.__init__(self)
        self.values = values

    def run(self):
        load_modules()
        message, attachment, key = get_answer(self.values)
        send_msg(self.values.vkApi.get_api(), self.values.item['from_id'], message, attachment, key)
