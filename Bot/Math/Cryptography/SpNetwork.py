# -*- coding: utf-8 -*-


def getAlphabet():
    return "абвгдежзийклмнопрстуфхцчшщъыьэюя+-,.!?:\"vin()0123456789"


def powMinusFirst(a, mod):
    res = 0.0
    chisl = 1
    flag = False
    while not flag:
        res = chisl * 1.0 / a
        chisl += mod
        flag = (res - int(res)) == 0.0

    return int(res)


def encodeCharWithAffineCipher(num, keyA, keyB):
    alf = getAlphabet()
    A = powMinusFirst(keyA, len(alf))
    number = (A * (num - keyB)) % len(alf)
    return number


def mesToInt(messages):
    alf = getAlphabet()
    messagesInt = [[alf.index(char) for char in mes] for mes in messages]

    return messagesInt


def permutationFunc(mes, permutation):
    return [mes[i] for i in permutation]


def spNetwork(message, keyA, keyB, permutation):
    message = permutationFunc(message, permutation)
    for i in range(len(message)):
        message[i] = encodeCharWithAffineCipher(message[i], keyA, keyB)

    return message


def messagesIntToStr(messages):
    alf = getAlphabet()
    text = ""
    for mes in messages:
        for index in mes:
            text = text + alf[index]

    return text


def decoderSpNetwork(message, keyA, keyB, permutation):
    permutation = [abs(int(num) - 4) for num in permutation]
    permutation.reverse()
    blockLength = len(permutation)

    messages = [list(message[i:i + blockLength]) for i in range(0, len(message), blockLength)]
    messages = mesToInt(messages)

    for i in range(len(messages)):
        for j in range(2):
            messages[i] = spNetwork(messages[i], keyA, keyB, permutation)

    message = messagesIntToStr(messages)

    return message
