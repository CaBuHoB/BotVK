from Bot.Basis import command_system
from Bot.Basis.Keyboards.GetButtons import getLessonsForQueueButtons


def queueByGroup(values):
    groups = values.item['text']
    date = values.message.split(' ')[1]
    tale_of_queue_name = groups + '_' + date
    message = 'Выбери предмет'
    keyboard = getLessonsForQueueButtons(tale_of_queue_name)

    return message, None, keyboard


command = command_system.Command()

command.keys = ['queueByGroup']
command.description = 'Название предмета для очереди'
command.process = queueByGroup