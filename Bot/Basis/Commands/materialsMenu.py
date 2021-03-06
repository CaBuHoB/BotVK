from Bot.Basis import command_system
from Bot.Basis.Functions.getButtons import get_materials_actions_buttons, get_default_buttons


def materialsMenu(values):
    message = 'Вот список предметов, по которым имеются материалы. ' \
              'Если у тебя есть что-то ещё и ты хочешь этим поделиться - напиши админу!)'
    keyboard = get_materials_actions_buttons(values)

    if keyboard is None:
        message = 'Бот запустился недавно, материалов пока нет =(\n' \
                  'Если хочешь внести свою лепту - напиши админу!)'
        keyboard = get_default_buttons(values)

    return message, None, keyboard


command = command_system.Command()

command.keys = ['materialsMenu']
command.description = 'Меню материалов'
command.process = materialsMenu
