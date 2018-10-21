from Bot.Basis import command_system
from Bot.Basis.Functions.getButtons import get_default_buttons


def kroukMenu(values):
    message = 'Доступные алгоритмы:\n'\
              '1) Решение сравнения вида x^2 = a (mod p)\n' \
              'Чтобы получить таблицу, отправь мне \"Крук (число a) (модуль)\"\n' \
              'Пример: Крук 14 193\n\n' \
              '2) Расширенный алгоритм Евклида для решения сравнения вида ax = b (mod m)\n' \
              'Чтобы получить решение, отправь \"РАЕ (число a) (число b) (модуль)\"\n' \
              'Пример: РАЕ 26 53 97'
    return message, None, get_default_buttons(values)


command = command_system.Command()

command.keys = ['kroukMenu']
command.description = 'Подсказка для обращения к решебнику Крука'
command.process = kroukMenu
