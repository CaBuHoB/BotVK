from Bot.Basis import command_system
from Bot.Basis.Functions.getButtons import get_default_buttons


def kroukMenu(values):
    message = 'Пока я умею только решать сравнения вида x^2 = a (mod p)\n' \
              'Чтобы получить таблицу, отправь мне \"Крук (число a) (модуль)\"\n' \
              'Пример: Крук 14 193'
    return message, None, get_default_buttons(values)


command = command_system.Command()

command.keys = ['kroukMenu']
command.description = 'Подсказка для обращения к решебнику Крука'
command.process = kroukMenu
