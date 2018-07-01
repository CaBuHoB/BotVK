# -*- coding: utf-8 -*-
import os

from Bot.Basis import command_system
from Bot.Math.Cryptography import TableOfQuadraticComp as tableKr
import vk_api

typeFile = {1: 'doc'}


def krouk(vkApi, item):
    message = 'Здесь должна быть таблица!!!!!\n' + item['body']
    filepath = tableKr.getFile(item['body'])
    upload = vk_api.VkUpload(vkApi)
    fileInfo = upload.document_message(filepath, peer_id=item['user_id'])
    file = [typeFile[fileInfo[0]['type']] + str(fileInfo[0]['owner_id']) + '_' + str(fileInfo[0]['id'])]
    os.remove(filepath)
    return message, file, None


hello_command = command_system.Command()

hello_command.keys = ['КРУК']
hello_command.description = 'Тут надо как то с круком разобраться'
hello_command.process = krouk
