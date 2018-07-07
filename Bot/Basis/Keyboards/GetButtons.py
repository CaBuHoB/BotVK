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


def getButtonsForRegistration():
    # TODO переписать кнопки для регистрации. Максимвльный размер 4х10. Придется разделять еще на группы
    return json.dumps({
        "one_time": True,
        "buttons": [
            [
                getButton('Зарегистрироваться', 'setNewUser', Color.RED)
            ]
        ]
    }, ensure_ascii=False)

# TODO здесь создать все нужные кнопки
