from Bot.Basis import command_system
from Bot.Basis.Keyboards.getButtons import get_queue_names_for_removing, get_default_buttons


def deleteQueue(values):
    message = 'Какую очередь удалить?'
    keyboard = get_queue_names_for_removing()
    if keyboard is None:
        message = 'Очередей больше нет'
        keyboard = get_default_buttons()

    return message, None, keyboard


command = command_system.Command()

command.keys = ['deleteQueue']
command.description = 'Удаление очереди'
command.process = deleteQueue