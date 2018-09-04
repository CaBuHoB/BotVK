from Bot.Basis import command_system
from Bot.Basis.DataBase.workWithDataBase import addPersonToDB
from Bot.Basis.Keyboards.GetButtons import getDefaultScreenButtons
from Bot.Basis.YandexGoogle.GoogleTables import setNameSelectedToGoogle


def endOfRegistration(values):
    fullname = values.item['text']
    name = fullname.split(' ')[1]
    surname = fullname.split(' ')[0]
    group = values.message.split(' ')[1]
    id = values.item['from_id']
    connect = values.connect
    values.users.setdefault(id, {'name': name,
                                 'surname': surname,
                                 'group': group})
    setNameSelectedToGoogle(fullname, group)
    addPersonToDB(connect, id, name, surname, group)
    message = 'Ты зарегистрирован как ' + fullname + \
              '!) Если случайно нажал не туда - напиши администратору!'
    return message, None, getDefaultScreenButtons(values)


command = command_system.Command()

command.keys = ['endOfRegistration']
command.description = 'Добавление человека в базу данных'
command.process = endOfRegistration
