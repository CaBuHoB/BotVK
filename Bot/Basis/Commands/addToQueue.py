from Bot.Basis import command_system
from Bot.Basis.DataBase.workWithDataBase import setToQueue, getQueueList
from Bot.Basis.Keyboards.GetButtons import getDefaultScreenButtons, getAlreadyInQueueButtons


def addToQueue(values):
    queue = values.message.split(' ')[1]
    id = values.item['from_id']
    name = values.users[id]['name'] + ' ' + values.users[id]['surname']
    connect = values.connect

    # Если "Встать в очередь", то человек первый раз обращается, тогда не надо пока его перезаписывать
    # Если "Встать в конец", то человек уже подтвердил, что он там есть и что надо кинуть его в конец
    addEvenIfAlreadyIn = False if (values.item['text'] == 'Встать в очередь') else True

    newSet = setToQueue(connect, queue, id, name, addEvenIfAlreadyIn)

    list = getQueueList(connect, queue)
    stringList = '\nОчередь на данный момент:'
    for name in list:
        stringList += '\n'
        stringList += name
    if newSet:
        message = 'Ты записан!\n' + stringList
        keyboard = getDefaultScreenButtons()
    else:
        message = 'Ты уже есть в очереди. Тебя переместить в конец?' + stringList
        keyboard = getAlreadyInQueueButtons(queue)

    return message, None, keyboard


command = command_system.Command()

command.keys = ['addToQueue']
command.description = 'Запись или перезапись в очередь'
command.process = addToQueue