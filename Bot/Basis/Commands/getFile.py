# -*- coding: utf-8 -*-
import os

from Bot.Basis import command_system
from Bot.Basis.MessageReplay import uploadFile
from Bot.Math.Cryptography import TableOfQuadraticComp as tableKr


def getFile(values):
    typeFile = {1: 'doc', 4: 'photo', 6: 'video'}

    message = 'Держи'
    fileName = values.message[values.message.find(' '):]
    doc = values.vkApi.method('docs.search', {'q': fileName, 'search_own': 1, 'count': 1})['items'][0]
    file = typeFile[doc[0]['type']] + str(doc[0]['owner_id']) + '_' + str(doc[0]['id'])
    # TODO вроде должно работать, с условием, что кнопки будут передавать "getfile full_file_name"
    return message, file, None


command = command_system.Command()

command.keys = ['getFile']
command.description = 'Здесь получаем файлы из группы и отправляем пользователю'
command.process = getFile