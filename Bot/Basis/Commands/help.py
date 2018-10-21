# -*- coding: utf-8 -*-
from Bot.Basis import command_system
from Bot.Basis.Functions.getButtons import get_default_buttons


def help(values):
    message = 'Общение с ботом:\n' \
              '• Чтобы перейти к архиву лаб, нажми на кнопку \"Лабы и материалы\"\n' \
              '• Для открытия решебника задач нажми на кнопку \"Алгоритмы\"\n\n' \
              '• Нажми на кнопку \"Очередь\", чтобы перейти в меню доступных очередей,' \
              'встать в очередь или посмотреть списки уже имеющихся\n\n' \
              '• Чтобы воспользоваться переводчиком, ' \
              'напиши \"переведи\", далее через пробел в этом же сообщении пиши текст для перевода. ' \
              'Аналогично ты можешь найти что-то в Вольфраме (\"вольфрам текст запроса\")' \
              ' и Википедии (\"вики текст запроса\")\n' \
              '• Напиши боту \"погода\" и увидишь прогноз в Питере :)\n\n' \
              '• Бот понимает аудиосообщения, так что если нет возможности написать ' \
              '(или просто лень) - говори!)\n\n' \
              '• Кроме этого в боте доступны рассылки. Ты можешь подписаться и получать уведомление с краткой информацией ' \
              'и номером аудитории за 15 минут до каждой пары, а так же расписание на следующий день (в 21:00) и ' \
              'погоду на текущий (в 9:00). Ты сможешь отписаться в любой момент и подписаться снова в меню подписок)\n\n' \
              '• Если у тебя возникли проблемы или вопросы, отправь боту \"admin (сообщение)\" ' \
              'без скобок или обратись к разработчикам лично! Бот очень хочет развиваться, ' \
              'поэтому если у тебя есть предложения по оптимизации, идеи или пожелания - ' \
              'не сиди, вноси свою лепту, мы будем рады!)'

    return message, None, get_default_buttons(values)


command = command_system.Command()

command.keys = ['/help', 'help', 'Помощь', 'помощь', '?']
command.description = 'Описание команд и кнопок'
command.process = help
