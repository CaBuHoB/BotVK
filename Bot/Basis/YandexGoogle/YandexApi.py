import requests
import xml.etree.ElementTree as XmlElementTree

headers = {
    'Content-Type': 'audio/ogg;codecs=opus',
}

params = (
    ('uuid', '01ae13cb744628b88fb536d496daa1e6'),
    ('key', 'cd9555c4-e103-4ae6-af8a-6537785e762f'),
    ('topic', 'queries'),
)


def voice_processing(file):
    data = requests.get(file).content
    response = requests.post('https://asr.yandex.net/asr_xml', headers=headers, params=params, data=data)
    if response.status_code == requests.codes.ok:
        response_text = response.text
        xml = XmlElementTree.fromstring(response_text)

        if int(xml.attrib['success']) == 1:
            max_confidence = - float("inf")
            text = 'Что то пошло не так и я не распознал твой голос'

            for child in xml:
                if float(child.attrib['confidence']) > max_confidence:
                    text = child.text
                    max_confidence = float(child.attrib['confidence'])

            if max_confidence != - float("inf"):
                return text

    return 'Что то пошло не так и я не распознал твой голос'


class SpeechException(Exception):
    pass
