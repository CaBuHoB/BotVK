from Bot.Basis import command_system
from Bot.Basis.DataBase.workWithDataBase import createQueueInBD
from Bot.Basis.Keyboards.GetButtons import getDefaultScreenButtons
from Bot.Basis.MessageReplay import send_msg


def queueCteation(values):
    lesson = values.item['text']
    tale_of_queue_name = values.message.split(' ')[1:]
    new_tale = ''
    for element in tale_of_queue_name:
        new_tale += element
        new_tale += ' '
    new_tale = str(new_tale[:-1])
    name = lesson + '_' + new_tale
    connect = values.connect
    # TODO: надо потом раскомментировать
    #createQueueInBD(connect, name)

    message = 'Создана очередь: ' + name
    groups = ''
    groups = str(new_tale.split('_')[0])
    groupList = groups.split(' ')
    for user in values.users:
        if str(values.users[user]['group']) in groupList:
            send_msg(values.vkApi.get_api(), user, message, attachment=None, keyboard=None)
    keyboard = getDefaultScreenButtons(values)

    return message, None, keyboard


command = command_system.Command()

command.keys = ['queueCteation']
command.description = 'Наконец, создание'
command.process = queueCteation