from Bot.Basis import command_system
from Bot.Basis.Functions.getButtons import get_default_buttons
from Bot.Basis.Functions.workWithDataBase import deleteDictWithMessageFromAdmin


def backToDefaultKeyboard(values):
    user_id = values.item['from_id']
    message = 'Главное меню'
    keyboard = get_default_buttons(values)

    deleteDictWithMessageFromAdmin(user_id)

    return message, None, keyboard


command = command_system.Command()

command.keys = ['backToDefaultKeyboard']
command.description = 'Выход к главным кнопкам'
command.process = backToDefaultKeyboard
