from Bot.Basis import command_system
from Bot.Basis.Keyboards.getButtons import get_choose_group_buttons


def errorInGroupChoosing(values):
    message = 'Выбери СВОЮ группу)'
    keyboard = get_choose_group_buttons()
    return message, None, keyboard


command = command_system.Command()

command.keys = ['errorInGroupChoosing']
command.description = 'Ошибка в выборе группы при регистрации'
command.process = errorInGroupChoosing
