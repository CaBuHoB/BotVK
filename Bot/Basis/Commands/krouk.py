# -*- coding: utf-8 -*-
import os

from Bot.Basis import command_system
from Bot.Basis.MessageReplay import upload_file
from Bot.Math.Cryptography import TableOfQuadraticComp as tableKr


def krouk(values):
    message = 'Держи таблицу!\n' + values.item['text']
    filepath = tableKr.getFile(values.item['text'], str(values.item['from_id']))
    file = upload_file(filepath, values.item['from_id'], values.item['text'] + '.pdf', values.vkApi)
    os.remove(filepath)
    return message, file, None


command = command_system.Command()

command.keys = ['КРУК']
command.description = 'Тут надо как то с круком разобраться'
command.process = krouk
