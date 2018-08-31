from Bot.Basis import command_system
from Bot.Basis.Keyboards.GetButtons import getDefaultScreenButtons
from Bot.Basis.YandexGoogle.GoogleTables import setNameUnSelectedToGoogle


def removePerson(values):
    name = values.message.split(' ')[1]
    surname = values.message.split(' ')[2]
    fullname = surname + ' ' + name
    group = values.message.split(' ')[3]

    for user in values.users.items():
        first = user[1]
        if (first['name'] == name) & (first['surname'] == surname):
            id = user[0]

    connect = values.connect
    values.users.pop(id)
    setNameUnSelectedToGoogle(fullname, group)
    # TODO: removePersonFromDB(connect, id), думаю, тут не нужны имя и группа
    # TODO: есть функция для этого removeFromQueueInDB(connect, queue, id)
    # Это если вдруг кто ошибется, чтоб в бд вручную не лезть
    # Чтоб удалить, надо писать боту removePerson Фамилия Имя Группа
    message = 'Пользователь снова незарегистрирован'
    return message, None, getDefaultScreenButtons()


command = command_system.Command()

command.keys = ['removePerson']
command.description = 'Удалить человека из всех таблиц, если кто-то ошибся'
command.process = removePerson