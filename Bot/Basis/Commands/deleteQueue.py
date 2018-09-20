from Bot.Basis import command_system
from Bot.Basis.Functions.getButtons import get_queue_names_for_removing, get_default_buttons


def deleteQueue(values):
    message = 'Какую очередь удалить?'
    keyboard = get_queue_names_for_removing(values)
    if keyboard is None:
        message = 'Очередей для твоей группы больше нет'
        keyboard = get_default_buttons(values)

    return message, None, keyboard


command = command_system.Command()

command.keys = ['deleteQueue']
command.description = 'Удаление очереди'
command.process = deleteQueue