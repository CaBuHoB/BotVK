# -*- coding: utf-8 -*-
import os
from threading import Lock

from Bot.Basis import command_system
from Bot.Basis.Functions.MessageReplay import upload_file
from Bot.Basis.Functions.getButtons import get_default_buttons
from Bot.Math.Cryptography.SpNetwork import decoderSpNetwork

lock = Lock()


def spNetwork(values):
    lock.acquire()
    message = "Неверные данные"
    text = values.item['text'].split()

    try:
        if len(text) == 5:
            ciphertext = text[1]
            keyA, keyB = int(text[2]), int(text[3])
            permutation = text[4]
            message = 'Держи решение!\n'
            filepath = decoderSpNetwork(ciphertext, keyA, keyB, permutation, values.item['from_id'])
            if filepath is not None:
                file = upload_file(filepath, values.item['from_id'], values.item['text'] + '.pdf', values.vkApi)
                os.remove(filepath)
                return message, file, get_default_buttons(values)
    finally:
        lock.release()

    return message, None, get_default_buttons(values)


command = command_system.Command()

command.keys = ['spNetwork']
command.description = 'Обработка шифротекста'
command.process = spNetwork
