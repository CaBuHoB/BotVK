from Bot.Basis import command_system
from Bot.Basis.DataBase.workWithDataBase import subscribePerson, unSubscribePerson
from Bot.Basis.Keyboards.GetButtons import getTimetableButtons


def timetableSending(values):
    id = values.item['from_id']
    if values.message.split()[1] == 'sub':
        subscribePerson(values.connect, id)
        message = 'Ты подписался на рассылку расписания.\n' \
              'В 21:00 тебе будет приходить расписание на следующий день.\n' \
              'За 15 минут до начала пары также будет приходить уведомление. ' \
              'Чтобы отписаться от рассылки, нажми на красную кнопку \"Отписаться\" в меню расписания)'
    else:
        unSubscribePerson(values.connect, id)
        message = 'Ты отписан от рассылки расписания'

    return message, None, getTimetableButtons(values)


command = command_system.Command()

command.keys = ['timetableSending']
command.description = 'Подписка/Отписка рассылки'
command.process = timetableSending