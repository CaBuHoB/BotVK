# -*- coding: utf-8 -*-
from Bot.Basis import command_system
from Bot.Basis.Keyboards.GetButtons import getDefaultScreenButtons


def help(values):
    # TODO: Дописать инструкцию к использованию
    # TODO: написать про yandex
    message = 'Помощь:\n' \
              '• Чтобы перейти к архиву лаб, билетов и конспектов, нажми на кнопку \"Материалы\"\n\n' \
              '• Для открытия решебника алгоритмов нажми на кнопку \"Решение задач\"\n\n' \
              '• Нажми на кнопку \"Очередь\", чтобы перейти в меню доступных очередей,' \
              'встать в очередь или посмотреть списки уже имеющихся\n\n' \
              '• Ещё тут есть переводчик, вольфрам, википедия, погода, ...\n\n' \
              '• Если у тебя возникли проблемы, вопросы, предложения, пожелания, ' \
              'отправь боту \"admin (сообщение)\" без скобок,' \
              'или обратись к нам! (ну тут типа контакты какие-нибудь)'
    return message, None, getDefaultScreenButtons()


command = command_system.Command()

command.keys = ['/help', 'help', 'Помощь', 'помощь']
command.description = 'Описание команд и кнопок'
command.process = help
