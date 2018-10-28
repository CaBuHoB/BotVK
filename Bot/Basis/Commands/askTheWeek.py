from Bot.Basis import command_system
from Bot.Basis.Functions.getButtons import get_asking_week_buttons


def askTheWeek(values):
    return 'Расписание какой недели прислать?', None, get_asking_week_buttons()


command = command_system.Command()

command.keys = ['askTheWeek']
command.description = 'Запрос, расписание какой недели нужно пользователю'
command.process = askTheWeek
