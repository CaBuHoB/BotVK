from Bot.Basis import command_system
from Bot.Basis.Functions.workWithDataBase import unSubscribePersonWeather, subscribePersonWeather
from Bot.Basis.Functions.getButtons import get_sub_buttons


def weatherSending(values):
    if values.message.split()[1] == 'sub':
        subscribePersonWeather(values.item['from_id'])
        message = "Ты подписался на рассылку погоды.\n" \
                  "Каждый день в 9 утра тебе будет сообщаться прогноз. " \
                  "Чтобы отписаться, отправь боту \"погода\", затем нажми на нужную кнопку)"
    else:
        unSubscribePersonWeather(values.item['from_id'])
        message = 'Ты отписался от рассылки погоды'

    return message, None, get_sub_buttons(values)


command = command_system.Command()

command.keys = ['weatherSending']
command.description = 'Подписка/Отписка рассылки'
command.process = weatherSending
