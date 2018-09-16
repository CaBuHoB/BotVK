from datetime import datetime
from argparse import Namespace

from flask import Flask, request, json

from Bot.Basis import MessageReplay
from Bot.Basis.Timetable.getSchedule import getTimetableDict, getDate
from Bot.Basis.Configs import confirmation_token, timetableDict, api, connect, users, messageFromAdmin, isUpper

app = Flask(__name__)


@app.route('/')
def hello_world():
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
        now = datetime.now().timetuple()
        if now[3] == 21 and now[4] == 0:
            timetableDict.update(getTimetableDict([5621, 5622, 5623]))
            # TODO: сделать обновление isUpper

        values = Namespace(vkApi=api, item=data['object'], connect=connect, users=users,
                           timetableDict=timetableDict, messageFromAdmin=messageFromAdmin, isUpper=isUpper)
        mr = MessageReplay.MessageReplay(values)
        mr.run()
        return 'ok'


if __name__ == '__main__':
    app.run()
