from Bot.Basis import command_system
from Bot.Basis.Functions.workWithDataBase import addPersonToDB
from Bot.Basis.Functions.getButtons import get_default_buttons
from Bot.Basis.YandexGoogle.GoogleTables import setNameSelectedToGoogle


def endOfRegistration(values):
    fullname = values.item['text']
    surname, name = fullname.split()
    group = values.message.split()[1]
    user_id = values.item['from_id']

    values.users.setdefault(user_id, {'name': name,
                                      'surname': surname,
                                      'group': int(group)})
    # setNameSelectedToGoogle(fullname, group)
    # addPersonToDB(user_id, name, surname, int(group))

    message = 'Ты зарегистрирован как ' + fullname + '!) ' \
              'Если случайно нажал не туда - напиши администратору!\n\n' \
              'Я новый бот, созданный для облегчения жизни студентам 52 кафедры. ' \
              'Я буду учиться решать алгоритмы и задачи, чтоб помогать тебе на контрольных, ' \
              'хранить материалы и лабы, которыми поделятся твои однокурсники и ты. ' \
              'Я умею выстраивать электронную очередь, присылать расписание и оперативно помогать ' \
              'в учёбе при помощи википедии, вольфрама и переводчика.\n' \
              'Чтобы узнать, что я могу и как меня об этом попросить, нажми на знак вопроса )\n\n'

    return message, None, get_default_buttons(values)


command = command_system.Command()

command.keys = ['endOfRegistration']
command.description = 'Добавление человека в базу данных'
command.process = endOfRegistration
