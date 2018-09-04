from Bot.Basis import command_system
from Bot.Basis.DataBase.workWithDataBase import addTableInDateDeleteTable, createQueueInBD, getDateDeletedTables, \
    getQueueNames
from Bot.Basis.Keyboards.GetButtons import getDefaultScreenButtons
from Bot.Basis.MessageReplay import send_msg
from datetime import datetime, timedelta


def queueCteation(values):
    subject = values.item['text']
    tail_of_queue_name = values.message.split(' ')[1:]
    tail_of_queue_name_str = ' '.join(tail_of_queue_name)
    groups, date = tail_of_queue_name_str.split('_')
    name = subject + '_' + groups + '_' + date

    if name in getQueueNames(values.connect):
        return 'Такая очередь уже есть!', None, getDefaultScreenButtons(values)

    date = date.split(' ')[0]
    day, month = date.split('.')
    if month[0] == '0':
        month = month[1]

    now = datetime.now()
    one_day_delta = timedelta(1)
    three_days_delta = timedelta(3)

    for i in range(0, 5):
        day_str = str(now.timetuple()[2])
        month_str = str(now.timetuple()[1])

        if (day_str == day) and (month_str == month):
            now += three_days_delta
            day_str = str(now.timetuple()[2])
            month_str = str(now.timetuple()[1])
            year_str = str(now.timetuple()[0])
            data_delete = day_str + '.' + month_str + '.' + year_str
            break
        now += one_day_delta

    connect = values.connect
    n = '\"' + name + '\"'
    createQueueInBD(connect, n)
    addTableInDateDeleteTable(connect, name, data_delete, values.item['from_id'])

    message = 'Создана очередь: ' + name
    groupList = groups.split(' ')
    for user in values.users:
        if str(values.users[user]['group']) in groupList and \
                user != values.item['from_id']:
            send_msg(values.vkApi.get_api(), user, message, attachment=None, keyboard=None)
    keyboard = getDefaultScreenButtons(values)

    return message, None, keyboard


command = command_system.Command()

command.keys = ['queueCteation']
command.description = 'Наконец, создание'
command.process = queueCteation