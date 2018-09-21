from Bot.Basis import command_system
from Bot.Basis.Functions.getButtons import get_default_buttons


def backToDefaultKeyboard(values):
    user_id = values.item['from_id']
    message = 'Главное меню'
    keyboard = get_default_buttons(values)

    if user_id in values.messageFromAdmin:
        values.messageFromAdmin.pop(user_id)

    return message, None, keyboard


command = command_system.Command()

command.keys = ['backToDefaultKeyboard']
command.description = 'Выход к главным кнопкам'
command.process = backToDefaultKeyboard
