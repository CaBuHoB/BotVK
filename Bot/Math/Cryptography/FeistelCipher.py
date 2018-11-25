# -*- coding: utf-8 -*-


def getAlphabet():
    return "абвгдежзийклмнопрстуфхцчшщъыьэюя+-,.!?:\"vin()0123456789"


def mesToInt(messages):
    alf = getAlphabet()
    messagesInt = [[alf.index(char) for char in mes] for mes in messages]

    return messagesInt


def permutationFunc(mes, permutation):
    return [mes[i] for i in permutation]


def messagesIntToStr(messages):
    alf = getAlphabet()
    text = ""
    for mes in messages:
        for index in mes:
            text = text + alf[index]

    return text


def fFunc(mes, key, permutation):
    lenAlf = len(getAlphabet())
    fMes = [(m * key) % lenAlf for m in mes]
    fMes = permutationFunc(fMes, permutation)

    return fMes


def feistelCipher(message, key, permutation):
    halfMessageLength = int(len(message)/2)
    mes = [message[:halfMessageLength], message[halfMessageLength:]]
    R = mes[0]
    L = mes[1]
    fMas = fFunc(R, key, permutation)
    for i in range(halfMessageLength):
        L[i] = (L[i] - fMas[i]) % 55

    return L + R


def decoderFeistelCipher(message, keys, permutation):
    permutation = [int(x) for x in permutation]
    keys.reverse()

    blockLength = len(permutation) * 2

    messages = [list(message[i:i + blockLength]) for i in range(0, len(message), blockLength)]
    messages = mesToInt(messages)

    for i in range(len(messages)):
        for j in range(3):
            messages[i] = feistelCipher(messages[i], keys[j], permutation)

    message = messagesIntToStr(messages)

    return message
