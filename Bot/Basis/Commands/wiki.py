# -*- coding: utf-8 -*-
import wikipediaapi

from Bot.Basis import command_system


def wiki(values):
    newMessage = 'Я не нашел такого в wiki'  # TODO возможно надо поработать с обработкой текста, взятого с wiki
    wiki_wiki = wikipediaapi.Wikipedia('ru')
    page_py = wiki_wiki.page(values.message[values.message.find(' '):])
    if page_py.exists():
        page_py = page_py.summary
        name = page_py[:page_py.find('—')]
        other = page_py[page_py.find('—'):]
        newMessage = 'Иногда я не идеально обрабатываю информацию\n\n' + name + '—' + other[:other.find('.') + 1]

    return newMessage, None, None


command = command_system.Command()

command.keys = ['wiki', 'wikipedia', 'вики', 'википедия']
command.description = 'Получает определение из википедии'
command.process = wiki
