from Bot.Basis import command_system
from Bot.Basis.Keyboards.GetButtons import getDefaultScreenButtons


def backToDefaultKeyboard(values):
    message = 'Главное меню'
    keyboard = getDefaultScreenButtons()
    return message, None, keyboard


command = command_system.Command()

command.keys = ['backToDefaultKeyboard']
command.description = 'Выход к трем главным кнопкам'
command.process = backToDefaultKeyboard