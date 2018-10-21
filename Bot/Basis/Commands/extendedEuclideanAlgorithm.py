# -*- coding: utf-8 -*-
import os
from threading import Lock

from Bot.Basis import command_system
from Bot.Basis.Functions.MessageReplay import upload_file
from Bot.Math.Cryptography.ExtendedEuclideanAlgorithm import createFileExtendedEuclideanAlgorithm

lock = Lock()


def krouk(values):
    lock.acquire()

    try:
        message = 'Держи решение!\n' + values.item['text']
        mes, filepath = createFileExtendedEuclideanAlgorithm(values.item['text'].split(' ')[1:],
                                                                 values.item['from_id'])
        if filepath is not None:
            file = upload_file(filepath, values.item['from_id'], values.item['text'] + '.pdf', values.vkApi)
            os.remove(filepath)
            return message, file, None
        message = mes
    finally:
        lock.release()

    return message, None, None


command = command_system.Command()

command.keys = ['РАЕ']
command.description = 'Расширенный алгоритм Евклида'
command.process = krouk
