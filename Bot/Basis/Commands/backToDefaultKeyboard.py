from Bot.Basis import command_system
from Bot.Basis.Keyboards.GetButtons import getDefaultScreenButtons


def backToDefaultKeyboard(values):
    id = values.item['from_id']
    message = 'Главное меню'
    keyboard = getDefaultScreenButtons(values)
    if id in values.messageFromAdmin:
        values.messageFromAdmin.pop(id)
    return message, None, keyboard


command = command_system.Command()

command.keys = ['backToDefaultKeyboard']
command.description = 'Выход к главным кнопкам'
command.process = backToDefaultKeyboard
