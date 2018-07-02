# -*- coding: utf-8 -*-
from Bot.Basis import command_system

from Bot.Basis.Keyboards.GetButtons import getTestButtons

def test(vkApi, item=None):
    message = 'Test'
    return message, None, getTestButtons()


hello_command = command_system.Command()

hello_command.keys = ['Test']
hello_command.description = 'Просто учусь создавать кнопки. Это полная жесть'
hello_command.process = test
