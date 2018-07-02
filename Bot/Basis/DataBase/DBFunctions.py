# -*- coding: utf-8 -*-

#здесь должны быть функции для работы с бд
from Bot.Basis.DataBase.DBWorker import getConnect

con = getConnect()
cur = con.cursor()
cur.execute('SELECT * FROM public.users')
print(cur.fetchone())