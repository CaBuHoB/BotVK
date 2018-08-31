from Bot.Basis import command_system
from Bot.Basis.Keyboards.GetButtons import getButtonsWithNames, getButtonsWithGroups


def showNamesList(values):
    group = values.item['text']
    message = 'Выбери себя в списке группы' + group + \
              '\nЕсли это не твоя группа - вернись к началу регистрации!'
    keyboard = getButtonsWithNames(group)
    if keyboard is None:
        message = 'В этой группе все уже зарегистрированы. Если ты точно ' \
                  'выбрал свою группу и ещё не регистрировался - обратись к администратору'
        keyboard = getButtonsWithGroups()
    return message, None, keyboard


command = command_system.Command()

command.keys = ['showNamesList']
command.description = 'Вывод клавиатуры с именами незарегистрированных'
command.process = showNamesList