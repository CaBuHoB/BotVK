from Bot.Basis import command_system
from Bot.Basis.Keyboards.GetButtons import getDefaultScreenButtons, getAlreadyInQueueButtons


def addToQueue(values):
    queue = values.message.split(' ')[1]
    id = values.item['user_id']

    # Если "Встать в очередь", то человек первый раз обращается, тогда не надо пока его перезаписывать
    # Если "Встать в конец", то человек уже подтвердил, что он там есть и что надо кинуть его в конец
    addEvenIfAlreadyIn = False if (values.item['body'] == 'Встать в очередь') else True

    # TODO: boolean запись в очередь в БД. Если человек уже есть, а последний параметр false,
    # то не записывать и возвращать false, если последний параметр true, то выкидывать
    # и записывать в конец, при этом возвращать true (!!!)
    # Если человека ещё нет, записывать и возвращать true
    # setToQueue(queue, id, addEvenIfAlreadyIn=false)
    setToQueue = True

    if setToQueue:
        message = 'Ты записан!'
        keyboard = getDefaultScreenButtons()
        # Тут можно сообщением отправить список этой очереди на текущий момент
        # Для этого функция запрашивается в TO DO в файле showQueue.py
    else:
        message = 'Ты уже есть в очереди. Тебя переместить в конец?' # + Показать человеку очередь
        keyboard = getAlreadyInQueueButtons(queue)

    return message, None, keyboard


command = command_system.Command()

command.keys = ['addToQueue']
command.description = 'Запись или перезапись в очередь'
command.process = addToQueue