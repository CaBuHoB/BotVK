# -*- coding: utf-8 -*-
from Bot.Basis import command_system
from Bot.Basis.Functions.getButtons import get_default_buttons
from Bot.Math.Cryptography.SpNetwork import decoderSpNetwork


def spNetwork(values):
    message = "Неверные данные"
    text = values.item['text'].split()
    if len(text) == 5:
        ciphertext = text[1]
        keyA, keyB = int(text[2]), int(text[3])
        permutation = text[4]
        message = decoderSpNetwork(ciphertext, keyA, keyB, permutation)

    return message, None, get_default_buttons(values)


command = command_system.Command()

command.keys = ['spNetwork']
command.description = 'Обработка шифротекста'
command.process = spNetwork
