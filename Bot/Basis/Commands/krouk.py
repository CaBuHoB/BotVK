# -*- coding: utf-8 -*-
import os

from Bot.Basis import command_system
from Bot.Basis.MessageReplay import uploadFile
from Bot.Math.Cryptography import TableOfQuadraticComp as tableKr


def krouk(values):
    message = 'Здесь должна быть таблица!!!!!\n' + values.item['body']
    filepath = tableKr.getFile(values.item['body'], str(values.item['user_id']))
    file = uploadFile(filepath, values.item['user_id'], values.item['body'] + '.pdf', values.vkApi)
    os.remove(filepath)
    return message, file, None


command = command_system.Command()

command.keys = ['КРУК']
command.description = 'Тут надо как то с круком разобраться'
command.process = krouk
