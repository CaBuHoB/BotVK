# -*- coding: utf-8 -*-
from Bot.Basis import command_system
from Bot.Basis.YandexGoogle.GoogleApi import getTranslatedText


def translate(vkApi, item=None):
    message = item['body']
    message = getTranslatedText(message[message.find(' '):])
    return message, None, None


hello_command = command_system.Command()

hello_command.keys = ['переведи']
hello_command.description = 'Переводит текст, который идет после слова "переведи"'
hello_command.process = translate
