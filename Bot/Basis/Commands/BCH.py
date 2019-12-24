# -*- coding: utf-8 -*-
import os
from threading import Lock

from Bot.Basis import command_system
from Bot.Basis.Functions.MessageReplay import upload_file
from Bot.Basis.Functions.getButtons import get_default_buttons
from Bot.Math.Cryptography.BCH import search_error
from Bot.Math.latexBuild import getPreamble, getEnd, createPDF

lock = Lock()


def BCH(values):
    lock.acquire()
    message = "Неверные данные"
    text = values.item['text'].split()

    try:
        if len(text) == 2:
            v = text[1]
            message = 'Держи решение!\n'
            latex, _ = search_error(v)
            ID = values.item['from_id']
            document = getPreamble()
            document += latex
            document += getEnd()
            name = str(ID) + 'SpNetwork.pdf'
            createPDF(document, '/tmp', name)
            filepath = os.path.join('/tmp', name)
            if filepath is not None:
                file = upload_file(filepath, values.item['from_id'], values.item['text'] + '.pdf', values.vkApi)
                os.remove(filepath)
                return message, file, get_default_buttons(values)
    finally:
        lock.release()

    return message, None, get_default_buttons(values)


command = command_system.Command()

command.keys = ['BCH']
command.description = 'Обработка BCH'
command.process = BCH
