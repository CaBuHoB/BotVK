# -*- coding: utf-8 -*-
from Bot.Basis import command_system

from Bot.Basis.Keyboards.GetButtons import getTestButtons


def test(values):
    return values.message, None, getTestButtons()


command = command_system.Command()

command.keys = ['Test']
command.description = 'Просто учусь создавать кнопки. Это полная жесть'
command.process = test
