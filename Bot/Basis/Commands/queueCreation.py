from Bot.Basis import command_system
from Bot.Basis.Functions.workWithDataBase import addTableInDateDeleteTable, createQueueInBD, getQueueNames
from Bot.Basis.Functions.getButtons import get_default_buttons, get_queue_actions_buttons
from Bot.Basis.Functions.MessageReplay import send_msg
from datetime import datetime, timedelta


def queueCreation(values):
    data_delete = ''
    subject = values.item['text']
    tail_of_queue_name = values.message.split()[1:]
    tail_of_queue_name_str = ' '.join(tail_of_queue_name)
    groups, date = tail_of_queue_name_str.split('_')

    queue_name = subject + '_' + groups + '_' + date
    if queue_name in getQueueNames():
        return 'Такая очередь уже есть!', None, get_default_buttons(values)

    date = date.split()[0]
    day, month = date.split('.')
    if month[0] == '0':
        month = month[1]

    now = datetime.now()
    for i in range(0, 5):
        day_str = str(now.timetuple()[2])
        month_str = str(now.timetuple()[1])

        if (day_str == day) and (month_str == month):
            now += timedelta(3)
            day_str = str(now.timetuple()[2])
            month_str = str(now.timetuple()[1])
            year_str = str(now.timetuple()[0])
            data_delete = day_str + '.' + month_str + '.' + year_str
            break
        now += timedelta(1)

    createQueueInBD('\"' + queue_name + '\"')
    addTableInDateDeleteTable(queue_name, data_delete, values.item['from_id'])

    message = 'Создана очередь: ' + queue_name

    for user in values.users:
        if (str(values.users[user]['group']) in groups.split()) and (user != values.item['from_id']):
            send_msg(values.vkApi, user, message,
                     attachment=None, keyboard=get_queue_actions_buttons(queue_name, False))

    return message, None, get_queue_actions_buttons(queue_name, False)


command = command_system.Command()

command.keys = ['queueCreation']
command.description = 'Наконец, создание'
command.process = queueCreation
