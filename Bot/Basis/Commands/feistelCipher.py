# -*- coding: utf-8 -*-
from Bot.Basis import command_system
from Bot.Basis.Functions.getButtons import get_default_buttons
from Bot.Math.Cryptography.FeistelCipher import decoderFeistelCipher


def feistelCipher(values):
    message = "Неверные данные"
    text = values.item['text'].split()
    if len(text) == 6:
        ciphertext = text[1]
        keys = [int(text[2]), int(text[3]), int(text[4])]
        permutation = text[5]
        message = decoderFeistelCipher(ciphertext, keys, permutation)

    return message, None, get_default_buttons(values)


command = command_system.Command()

command.keys = ['feistelCipher']
command.description = 'Обработка шифротекста'
command.process = feistelCipher
