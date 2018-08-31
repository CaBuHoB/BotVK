from Bot.Basis import command_system
from Bot.Basis.Keyboards.GetButtons import getButtonsWithGroups


def errorInGroupChoosing(values):
    message = 'Выбери СВОЮ группу)'
    keyboard = getButtonsWithGroups()
    return message, None, keyboard


command = command_system.Command()

command.keys = ['errorInGroupChoosing']
command.description = 'Ошибка в выборе группы при регистрации'
command.process = errorInGroupChoosing
