from Bot.Basis import command_system
from Bot.Basis.Functions.getButtons import get_default_buttons
from Bot.Basis.Functions.workWithDataBase import deleteDictWithMessageFromAdmin


def backToDefaultKeyboard(values):
    deleteDictWithMessageFromAdmin(values.item['from_id'])

    return 'Главное меню', None, get_default_buttons(values)


command = command_system.Command()

command.keys = ['backToDefaultKeyboard']
command.description = 'Выход к главным кнопкам'
command.process = backToDefaultKeyboard
