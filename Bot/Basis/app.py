from datetime import datetime
from argparse import Namespace

from flask import Flask, request, json

from Bot.Basis import MessageReplay
from Bot.Basis.Timetable.getSchedule import getTimetableDict, getDate
from Bot.Basis.Configs import confirmation_token, timetableDict, api, users, messageFromAdmin
from Bot.Basis import Configs

app = Flask(__name__)


@app.route('/')
def hello_world():
    now = datetime.now().timetuple()
    if now[3] == 0 and now[4] == 1:
        timetableDict.update(getTimetableDict([5621, 5622, 5623]))
        Configs.isUpper = getDate()['isUpper']
        api.messages.send(user_id=38081883, message='Все норм, я обновил расписане:)')
        # TODO: сделать обновление isUpper
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
        api.messages.markAsRead(peer_id=data['object']['peer_id'])
        values = Namespace(vkApi=api, item=data['object'], users=users,
                           timetableDict=timetableDict, messageFromAdmin=messageFromAdmin, isUpper=Configs.isUpper)
        mr = MessageReplay.MessageReplay(values)
        mr.run()
        return 'ok'


if __name__ == '__main__':
    app.run()
