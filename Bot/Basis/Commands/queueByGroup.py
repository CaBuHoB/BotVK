from Bot.Basis import command_system
from Bot.Basis.Functions.getButtons import get_subjects_for_queue_creation_buttons


def queueByGroup(values):
    groups = values.item['text']
    date = values.message.split()[1:]
    date_str = ' '.join(date)
    tail_of_queue_name = groups + '_' + date_str
    message = 'Выбери предмет'
    keyboard = get_subjects_for_queue_creation_buttons(values, tail_of_queue_name)

    return message, None, keyboard


command = command_system.Command()

command.keys = ['queueByGroup']
command.description = 'Название предмета для очереди'
command.process = queueByGroup
