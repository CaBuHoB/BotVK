from Bot.Basis import command_system
from Bot.Basis.Functions.getButtons import queue_removing_buttons


def removeQueueOrDont(values):
    name = ' '.join(values.message.split()[1:])
    message = 'Безвозвратно удалить очередь ' + name + ' ?'
    keyboard = queue_removing_buttons(name)

    return message, None, keyboard


command = command_system.Command()

command.keys = ['removeQueueOrDont']
command.description = 'Удаление очереди (подтверждение)'
command.process = removeQueueOrDont
