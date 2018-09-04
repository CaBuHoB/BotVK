from Bot.Basis import command_system
from Bot.Basis.Keyboards.GetButtons import getDefaultScreenButtons


def kroukMenu(values):
    message = 'Пока я умею решать только сравнения вида x^2 = a (mod p)\n' \
              'Чтобы получить таблицу, отправь мне \"Крук (число a) (модуль)\"\n' \
              'Пример: Крук 14 193'
    return message, None, getDefaultScreenButtons(values)


command = command_system.Command()

command.keys = ['kroukMenu']
command.description = 'Подсказка для обращения к решебнику Крука'
command.process = kroukMenu
