# -*- coding: utf-8 -*-
import os
from threading import Lock

from Bot.Basis import command_system
from Bot.Basis.Functions.MessageReplay import upload_file
from Bot.Math.Cryptography import TableOfQuadraticComp as tableKr

lock = Lock()

def krouk(values):
    lock.acquire()

    try:
        message = 'Держи таблицу!\n' + values.item['text']
        filepathOrMessage, check, _ = tableKr.getFile(values.item['text'], str(values.item['from_id']))
        if check:
            file = upload_file(filepathOrMessage, values.item['from_id'], values.item['text'] + '.pdf', values.vkApi)
            os.remove(filepathOrMessage)
            return message, file, None
        message = filepathOrMessage
    finally:
        lock.release()

    return message, None, None


command = command_system.Command()

command.keys = ['КРУК']
command.description = 'Тут надо как то с круком разобраться'
command.process = krouk
