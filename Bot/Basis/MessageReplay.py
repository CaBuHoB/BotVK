# -*- coding: utf-8 -*-

from threading import Thread


def send_msg(vk, user_id, msg):
    vk.method('messages.send', {'user_id': user_id, 'message': msg})

class MessageReplay(Thread):

    def __init__(self, vk, item):
        Thread.__init__(self)
        self.vk = vk
        self.item = item

    def run(self):
        mess = self.item['body']
        help = 'Пока я умею только:\n' \
                '1) Отвечать на сообщение \"Hi\"\n' \
                '2) Пересылать твои сообщения\n' \
                '3) Строить таблицу. '
        krouk = 'Если у тебя есть уравнение вида x^2=a (mod p)\n' \
                'Чтобы получить готовую таблицу тебе надо отправить мне сообщение вида \"Крук a p n\", ' \
                'где n - число образующее квадратичный невычет с модулем L(n, p)=-1\nПример: Крук 14 193 5'

        if mess == 'Hi':
            send_msg(self.vk, self.item['user_id'], 'Привет!')
        elif mess == '/start':
            send_msg(self.vk, self.item['user_id'], 'Узнай, что я умею, вызвав /help')
        elif mess == '/help':
            send_msg(self.vk, self.item['user_id'], help + krouk)
        elif mess == 'Test':
            send_msg(self.vk, self.item['user_id'], 'Test')
        else:
            split = mess.split(" ")
            if (split[0] == 'Крук') & (len(split) == 4):
                send_msg(self.vk, self.item['user_id'], 'Здесь должна быть таблица!!!!!!!!!')
            else:
                send_msg(self.vk, self.item['user_id'], mess)

