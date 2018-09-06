from Bot.Basis import command_system
from Bot.Basis.Keyboards.getButtons import get_asking_week_buttons


def askTheWeek(values):
    message = 'Расписание какой недели прислать?'
    keyboard = get_asking_week_buttons()

    return message, None, keyboard


command = command_system.Command()

command.keys = ['askTheWeek']
command.description = 'Запрос, расписание какой недели нужно пользователю'
command.process = askTheWeek
