from datetime import datetime, timedelta
from Bot.Basis import command_system
from Bot.Basis.Functions.workWithDataBase import updateDateInDateDeleted
from Bot.Basis.Functions.getButtons import get_default_buttons
from Bot.Basis.Threads.QueueThread import remove_from_asked_list


def rewriteQueueDelete(values):
    name = values.message.split()[1:]
    name = ' '.join(name)

    new_date = datetime.now() + timedelta(3)
    day = str(new_date.timetuple()[2])
    month = str(new_date.timetuple()[1])
    year = str(new_date.timetuple()[0])
    date = day + '.' + month + '.' + year

    message = 'Перенесена дата удаления очереди ' + name
    name = '\"' + name + '\"'

    updateDateInDateDeleted(name, date)
    remove_from_asked_list(values.item['from_id'])

    keyboard = get_default_buttons(values)

    return message, None, keyboard


command = command_system.Command()

command.keys = ['rewriteQueueDelete']
command.description = 'Перенос даты удаления очереди'
command.process = rewriteQueueDelete
