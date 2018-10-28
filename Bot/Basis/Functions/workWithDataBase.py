# -*- coding: utf-8 -*-

import psycopg2
import os


def getConnect():
    # TODO: исправить, когда вернемся к основному серверу DATABASE_URL
    return psycopg2.connect(os.environ['DATABASE'])


def getAllUsers():
    connect = getConnect()
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM users')

    users = {}
    for userData in cursor:
        users.setdefault(
            userData[0],
            {
                'name': userData[1],
                'surname': userData[2],
                'group': userData[3]
            }
        )
    cursor.close()
    connect.close()

    return users


def addPersonToDB(personID, name, surname, group):
    connect = getConnect()
    cursor = connect.cursor()

    cursor.execute('INSERT INTO users VALUES (%s, %s, %s, %s)', [personID, name, surname, group])
    cursor.close()
    connect.commit()
    connect.close()


def createQueueInBD(name):
    connect = getConnect()
    cursor = connect.cursor()

    cursor.execute('CREATE TABLE queue.{} (id int NOT NULL, name varchar(50) NOT NULL);'.format(name))
    cursor.close()
    connect.commit()
    connect.close()


def removeQueueInBD(queue):
    connect = getConnect()
    cursor = connect.cursor()

    cursor.execute('DROP TABLE queue.{}'.format(queue))
    cursor.close()
    connect.commit()
    connect.close()


def removeFromDateDeleted(queue):
    connect = getConnect()
    cursor = connect.cursor()

    cursor.execute('DELETE FROM public."date deleted tables" WHERE name = %s', [queue])
    cursor.close()
    connect.commit()
    connect.close()


def getDateDeletedTables():
    connect = getConnect()
    cursor = connect.cursor()

    cursor.execute('SELECT * FROM public."date deleted tables"')
    nameDate = [[table[0], table[1], table[2]] for table in cursor]
    cursor.close()
    connect.close()

    return nameDate


def addTableInDateDeleteTable(name, date, ID):
    connect = getConnect()
    cursor = connect.cursor()

    cursor.execute('INSERT INTO public."date deleted tables" VALUES (%s, %s, %s)', [name, date, ID])
    cursor.close()
    connect.commit()
    connect.close()


def updateDateInDateDeleted(queue, newDate):
    connect = getConnect()
    cursor = connect.cursor()

    cursor.execute('UPDATE public."date deleted tables" SET date = %s WHERE name = %s', [newDate, queue])
    cursor.close()
    connect.commit()
    connect.close()


def getQueueNames():
    connect = getConnect()
    cursor = connect.cursor()

    cursor.execute('SELECT table_name FROM information_schema.tables WHERE table_schema = %s', ['queue'])
    tables = [answ[0] for answ in cursor]
    cursor.close()
    connect.close()

    return tables


def getQueueList(queue):
    connect = getConnect()
    cursor = connect.cursor()

    cursor.execute('SELECT name FROM queue.{}'.format(queue))
    queueList = [name[0] for name in cursor]
    cursor.close()
    connect.close()

    return queueList


def getSubjects():
    connect = getConnect()
    cursor = connect.cursor()

    cursor.execute('SELECT name FROM public.subjects')
    subjectsList = [name[0] for name in cursor]
    cursor.close()
    connect.close()

    return subjectsList


def removeFromQueueInDB(queue, userId):
    connect = getConnect()
    cursor = connect.cursor()

    cursor.execute('DELETE FROM queue.{} WHERE id = {}'.format(queue, userId))
    cursor.close()
    connect.commit()
    connect.close()


def setToQueue(queue, userId, name):
    connect = getConnect()
    cursor = connect.cursor()

    cursor.execute('SELECT * FROM queue.{} WHERE id = {}'.format(queue, userId))
    if len(cursor.fetchall()) != 0:
        cursor.execute('DELETE FROM queue.{} WHERE id = {}'.format(queue, userId))
        connect.commit()
        cursor.execute('INSERT INTO queue.{} VALUES (%s, %s)'.format(queue), [userId, name])
    else:
        cursor.execute('INSERT INTO queue.{} VALUES (%s, %s)'.format(queue), [userId, name])

    cursor.close()
    connect.commit()
    connect.close()

    return True


def subscribePerson(user_id):
    connect = getConnect()
    cursor = connect.cursor()

    cursor.execute('INSERT INTO public.subscribers VALUES (%s)', [user_id])
    cursor.close()
    connect.commit()
    connect.close()


def unSubscribePerson(user_id):
    connect = getConnect()
    cursor = connect.cursor()

    cursor.execute('DELETE FROM public.subscribers WHERE id = {}'.format(user_id))
    cursor.close()
    connect.commit()
    connect.close()


def getSubscribedUsers():
    connect = getConnect()
    cursor = connect.cursor()

    cursor.execute('SELECT id FROM public.subscribers')
    subscribers = [userId[0] for userId in cursor]
    cursor.close()
    connect.close()

    return subscribers


def subscribePersonWeather(user_id):
    connect = getConnect()
    cursor = connect.cursor()

    cursor.execute("INSERT INTO public.\"subscribers weather\" VALUES (%s)", [user_id])
    cursor.close()
    connect.commit()
    connect.close()


def unSubscribePersonWeather(user_id):
    connect = getConnect()
    cursor = connect.cursor()

    cursor.execute("DELETE FROM public.\"subscribers weather\" WHERE id = {}".format(user_id))
    cursor.close()
    connect.commit()
    connect.close()


def getSubscribedUsersWeather():
    connect = getConnect()
    cursor = connect.cursor()

    cursor.execute("SELECT id FROM public.\"subscribers weather\"")
    subscribers = [userId[0] for userId in cursor]
    cursor.close()
    connect.close()

    return subscribers


def getDictWithMessageFromAdmin(userId):
    connect = getConnect()
    cursor = connect.cursor()

    cursor.execute("SELECT dict FROM public.\"message from admin\" WHERE id = {}".format(userId))
    dictUser = cursor.fetchone()
    dictUser = dictUser[0] if dictUser is not None else None
    cursor.close()
    connect.close()

    return dictUser


def deleteDictWithMessageFromAdmin(userId):
    connect = getConnect()
    cursor = connect.cursor()

    cursor.execute("DELETE FROM public.\"message from admin\" WHERE id = {}".format(userId))
    cursor.close()
    connect.commit()
    connect.close()


def setDictWithMessageFromAdmin(userId, dictMes):
    connect = getConnect()
    cursor = connect.cursor()

    cursor.execute("SELECT dict FROM public.\"message from admin\" WHERE id = {}".format(userId))
    if len(cursor.fetchall()) != 0:
        cursor.execute("DELETE FROM public.\"message from admin\" WHERE id = {}".format(userId))
        connect.commit()
    cursor.execute("INSERT INTO public.\"message from admin\" VALUES (%s, %s)", [userId, dictMes])

    cursor.close()
    connect.commit()
    connect.close()
