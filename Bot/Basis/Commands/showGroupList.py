from Bot.Basis import command_system
from Bot.Basis.Keyboards.GetButtons import getButtonsWithNames, getButtonsWithGroups


def showNamesList(values):
    message = 'Выбери себя'
    group = values.item['body']
    keyboard = getButtonsWithNames(group)
    if keyboard is None:
        message = 'В этой группе все уже зарегистрированы'
        keyboard = getButtonsWithGroups()
    return message, None, keyboard


command = command_system.Command()

command.keys = ['showNamesList']
command.description = 'Вывод клавиатуры с именами незарегистрированных'
command.process = showNamesList