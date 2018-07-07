import json
from enum import Enum


class Color(Enum):
    RED = 'negative'
    GREEN = 'positive'
    WHITE = 'default'
    BLUE = 'primary'


def getButton(label, payload, color=Color.WHITE):
    return {
        "action": {
            "type": "text",
            "payload": json.dumps(payload),
            "label": label
        },
        "color": color.value
    }


def getTestButtons():
    return json.dumps({
        "one_time": True,
        "buttons": [
            [
                getButton('Нажми на меня', 'Тестируем кнопки', Color.RED)
            ]
        ]
    }, ensure_ascii=False)


def getButtonsForRegistration():
    return json.dumps({
        "one_time": True,
        "buttons": [
            [
                getButton('Зарегистрироваться', 'setNewUser', Color.RED)
            ]
        ]
    }, ensure_ascii=False)
