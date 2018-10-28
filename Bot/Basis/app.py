from datetime import datetime
from argparse import Namespace

from flask import Flask, request, json

from Bot.Basis.Functions import MessageReplay
from Bot.Basis.Functions.getSchedule import getTimetableDict
from Bot.Basis import Configs
from Bot.Basis.Functions.getWeatherForecast import getWeather
from Bot.Basis.Functions.workWithDataBase import getAllUsers

app = Flask(__name__)


@app.route('/')
def hello_world():
    now = datetime.now().timetuple()
    if now[3] == 0 and now[4] == 1:
        Configs.timetableDict.update(getTimetableDict())
        Configs.isUpper = True if (datetime.now().isocalendar()[1] % 2 == 0) else False

        Configs.api.messages.send(user_id=38081883, message='Все норм, я обновил расписание:)')
    if now[4] % 5 == 0:
        Configs.weatherForecast = getWeather()
    return 'Hello, World!'


@app.route('/', methods=['POST'])
def processing():
    data = json.loads(request.data)
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return Configs.confirmation_token
    if data['type'] == 'message_typing_state':
        return 'ok'
    if data['type'] == 'message_reply':
        return 'ok'
    elif data['type'] == 'message_new':
        users = getAllUsers()
        Configs.api.messages.markAsRead(peer_id=data['object']['peer_id'])
        values = Namespace(vkApi=Configs.api, item=data['object'], users=users,
                           timetableDict=Configs.timetableDict, isUpper=Configs.isUpper,
                           weather=Configs.weatherForecast)
        mr = MessageReplay.MessageReplay(values)
        mr.run()
        return 'ok'


if __name__ == '__main__':
    app.run()
