from Bot.Basis import command_system
from Bot.Basis.Functions.getButtons import get_choose_name_buttons, get_choose_group_buttons


def showNamesList(values):
    group = values.item['text']
    message = 'Выбери себя в списке группы ' + group + \
              '\nЕсли это не твоя группа - вернись к началу регистрации!'
    keyboard = get_choose_name_buttons(group)

    if keyboard is None:
        message = 'В этой группе все уже зарегистрированы. Если ты точно ' \
                  'выбрал свою группу и ещё не регистрировался - обратись к администратору'
        keyboard = get_choose_group_buttons()

    return message, None, keyboard


command = command_system.Command()

command.keys = ['showNamesList']
command.description = 'Вывод клавиатуры с именами незарегистрированных'
command.process = showNamesList
