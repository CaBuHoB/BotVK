from Bot.Basis import command_system
from Bot.Basis.Keyboards.GetButtons import getDefaultScreenButtons
from Bot.Basis.YandexGoogle.GoogleTables import setNameSelectedToGoogle


def endOfRegistration(values):
    message = 'Ты зарегистрирован!)'
    fullname = values.item['body']
    name = fullname.split(' ')[0]
    surname = fullname.split(' ')[1]
    group = values.message.split(' ')[1]
    id = values.item['user_id']
    values.users.setdefault(id, {'name': name,
                                 'surname': surname,
                                 'group': group})
    setNameSelectedToGoogle(fullname, group)
    # TODO: addPersonToDB(id, name, surname, group)
    return message, None, getDefaultScreenButtons()


command = command_system.Command()

command.keys = ['endOfRegistration']
command.description = 'Добавление человека в базу данных'
command.process = endOfRegistration