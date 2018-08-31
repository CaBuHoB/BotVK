from Bot.Basis import command_system
from Bot.Basis.Keyboards.GetButtons import getTestButtons, getMaterialsActionsButtons, getDefaultScreenButtons


def materialsMenu(values):
    message = 'Вот список предметов, по которым имеются материалы. ' \
              'Если у тебя есть что-то ещё и ты хочешь этим поделиться - напиши админу!)'
    keyboard = getMaterialsActionsButtons()

    if keyboard is None:
        message = 'Материалов пока нет =(\n' \
                  'Если хочешь внести свою лепту - напиши админу!)'
        keyboard = getDefaultScreenButtons()

    return message, None, keyboard


command = command_system.Command()

command.keys = ['materialsMenu']
command.description = 'Меню материалов'
command.process = materialsMenu

