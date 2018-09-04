from Bot.Basis import command_system
from Bot.Basis.Keyboards.GetButtons import getAskingWeekButtons


def askTheWeek(values):
    message = 'Расписание какой недели прислать?'
    keyboard = getAskingWeekButtons()

    return message, None, keyboard


command = command_system.Command()

command.keys = ['askTheWeek']
command.description = 'Запрос, расписание какой недели нужно пользователю'
command.process = askTheWeek