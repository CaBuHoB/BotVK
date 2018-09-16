# -*- coding: utf-8 -*-
from Bot.Basis import command_system
from Bot.Basis.Keyboards.getButtons import get_default_buttons
from Bot.Basis.MessageReplay import send_sticker


def getFile(values):
    type_file = {1: 'doc', 4: 'photo', 6: 'video', 8: 'doc'}

    message = 'Нашёл) Держи:'
    file_name = values.message[values.message.find(' ') + 1:]
    doc = values.vkApi.docs.search(q=file_name, search_own=1, count=200)['items']
    if len(doc) == 0:
        send_sticker(values.vkApi.get_api(), values.item['user_id'], 8480)
        return 'Ошибочка вышла', None, None
    file = type_file[doc[0]['type']] + str(doc[0]['owner_id']) + '_' + str(doc[0]['id'])
    return message, file, get_default_buttons(values)


command = command_system.Command()

command.keys = ['getFile']
command.description = 'Здесь получаем файлы из группы и отправляем пользователю'
command.process = getFile
