# -*- coding: utf-8 -*-
import os

from Bot.Basis import command_system
from yandex import Translater


def translate(values):
    # TODO: исправить перевод. Сейчас переводит только с русского на англ
    # message = getTranslatedText(values.message[values.message.find(' '):])
    # fixme: временный переводчик
    tr = Translater()
    tr.set_key(os.environ['YANDEX_TRNSL_KEY'])
    tr.set_text(values.message[values.message.find(' '):])
    fromLang = tr.detect_lang()
    if fromLang == 'ru':
        tr.set_from_lang('ru')
        tr.set_to_lang('en')
    else:
        tr.set_from_lang('en')
        tr.set_to_lang('ru')
    message = tr.translate()

    return message, None, None


command = command_system.Command()

command.keys = ['переведи', 'перевести', 'перевод']
command.description = 'Переводит текст, который идет после слова "переведи"'
command.process = translate
