# -*- coding: utf-8 -*-

import psycopg2


def getConnect():
    dbname = 'd83jm6venn88s5'
    user = 'uniyqmorkhqebp'
    password = '49fc88f50aa5ab5769aef22fbc2313bb56f8b14ed38e3dc08b5157f5c35c9d9e'
    host = 'ec2-54-217-250-0.eu-west-1.compute.amazonaws.com'
    port = 5432

    con = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    return con


def getAllUsers(connect):
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

    return users


def addPersonToDB(connect, id, name, surname, group):
    cursor = connect.cursor()

    cursor.execute('INSERT INTO users VALUES (%s, %s, %s, %s)',
                                            [id, name, surname, group])
    cursor.close()
    connect.commit()


def getQueueNames(connect):
    cursor = connect.cursor()

    cursor.execute('SELECT table_name FROM information_schema.tables \
                                            WHERE table_schema = %s', ['queue'])
    tables = [answ[0] for answ in cursor]
    cursor.close()

    return tables


def getQueueList(connect, queue):
    cursor = connect.cursor()

    cursor.execute('SELECT name FROM queue.{}'.format(queue))
    queueList = [name[0] for name in cursor]
    cursor.close()

    return queueList


def removeFromQueueInDB(connect, queue, id):
    cursor = connect.cursor()

    cursor.execute('DELETE FROM queue.{} WHERE id = {}'.format(queue, id))
    cursor.close()
    connect.commit()


def setToQueue(connect, queue, id, name, addEvenIfAlreadyIn=False):
    # то не записывать и возвращать false, если последний параметр true, то выкидывать
    # и записывать в конец, при этом возвращать true (!!!)
    # Если человека ещё нет, записывать и возвращать true

    cursor = connect.cursor()

    cursor.execute('SELECT * FROM queue.{} WHERE id = {}'.format(queue, id))
    isWritten = True if len(cursor.fetchall()) != 0 else False
    if isWritten and not addEvenIfAlreadyIn:
        return False
    if isWritten and addEvenIfAlreadyIn:
        cursor.execute('DELETE FROM queue.{} WHERE id = {}'.format(queue, id))
        connect.commit()
        cursor.execute('INSERT INTO queue.{} VALUES (%s, %s)'.format(queue),
                                                            [id, name])
    elif not isWritten:
        cursor.execute('INSERT INTO queue.{} VALUES (%s, %s)'.format(queue),
                                                            [id, name])

    cursor.close()
    connect.commit()

    return True


connect = getConnect()
print(setToQueue(connect, 'test', 1, 'max', True))
print(getQueueList(connect, "test"))
