# -*- coding: utf-8 -*-
from Bot.Basis import command_system
from Bot.Basis.Functions.getButtons import get_materials_list_buttons


def nextMaterialsPage(values):
    subject = values.message.split()[1]
    message = 'Смена страницы'
    page_num = values.message.split()[2]

    return message, None, get_materials_list_buttons(subject, values, int(page_num))


command = command_system.Command()

command.keys = ['nextMaterialsPage']
command.description = 'Переключение к другой странице материалов'
command.process = nextMaterialsPage
