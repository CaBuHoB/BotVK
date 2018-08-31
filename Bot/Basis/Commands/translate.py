# -*- coding: utf-8 -*-
from Bot.Basis import command_system
from Bot.Basis.YandexGoogle.GoogleApi import getTranslatedText


def translate(values):
    # TODO: исправить перевод. Сейчас переводит только с руссуого на англ
    message = getTranslatedText(values.message[values.message.find(' '):])
    return message, None, None


command = command_system.Command()

command.keys = ['переведи', 'перевести', 'перевод']
command.description = 'Переводит текст, который идет после слова "переведи"'
command.process = translate
