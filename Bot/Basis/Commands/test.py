# -*- coding: utf-8 -*-
from Bot.Basis import command_system
import json


def test(vkApi, item=None):
    message = 'Test'
    key = json.loads(open('Keyboards/keyboard.json').read())
    return message, None, key


hello_command = command_system.Command()

hello_command.keys = ['Test']
hello_command.description = 'Просто учусь создавать кнопки. Это полная жесть'
hello_command.process = test
