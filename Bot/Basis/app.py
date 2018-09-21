import os
from datetime import datetime
from argparse import Namespace

from flask import Flask, request, json

from Bot.Basis.Functions import MessageReplay
from Bot.Basis.Functions.getSchedule import getDate
from Bot.Basis.Configs import confirmation_token, timetableDict, api, messageFromAdmin
from Bot.Basis import Configs
from Bot.Basis.Functions.getWeatherForecast import getWeather
from Bot.Basis.Functions.workWithDataBase import getAllUsers

app = Flask(__name__)
users = {}


@app.route('/')
def hello_world():
    now = datetime.now().timetuple()
    if now[3] == 0 and now[4] == 1:
        path = os.path.split(os.path.abspath(__file__))[0]
        with open(path + '/Threads/timetable.json', 'r') as f:
            Configs.timetableDict.update(json.load(f))
        Configs.isUpper = getDate()['isUpper']
        api.messages.send(user_id=38081883, message='Все норм, я обновил расписане:)')
    if now[4] % 5 == 0:
        Configs.weatherForecast = getWeather()
    return 'Hello, World!'


@app.route('/', methods=['POST'])
def processing():
    data = json.loads(request.data)
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return confirmation_token
    if data['type'] == 'message_typing_state':
        return 'ok'
    if data['type'] == 'message_reply':
        return 'ok'
    elif data['type'] == 'message_new':
        print("First", users)
        api.messages.markAsRead(peer_id=data['object']['peer_id'])
        values = Namespace(vkApi=api, item=data['object'], users=users,
                           timetableDict=timetableDict, messageFromAdmin=messageFromAdmin, isUpper=Configs.isUpper)
        mr = MessageReplay.MessageReplay(values)
        mr.run()
        print("Second", users)
        return 'ok'


if __name__ == '__main__':
    users = getAllUsers()
    app.run()
