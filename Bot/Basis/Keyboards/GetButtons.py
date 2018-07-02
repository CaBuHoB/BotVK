import json


def getButton(label, payload, color='default', one_time=True):
    return {
                "action": {
                    "type": "text",
                    "payload": json.dumps(payload, ensure_ascii=False),
                    "label": label
                },
                "color": color
            }


def getTestButtons():
    return json.dumps({
        "one_time": True,
        "buttons": [
            [
                getButton('Нажми на меня', 'Testing')
            ]
        ]
    }, ensure_ascii=False)
