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


def encodeCharWithAffineCipher(alf, char, keyA, keyB):
    A = powMinusFirst(keyA, len(alf))
    num = (A * (alf.index(char) - keyB)) % len(alf)
    return alf[num]


def decoderSpNetwork(message, keyA, keyB, permutation):
    decryptedText = ""
    permutation = [int(x) for x in permutation]
    alf = getAlphabet()
    chunks, chunk_size = len(message), len(permutation)
    messages = [message[i:i + chunk_size] for i in range(0, chunks, chunk_size)]
    for mes in messages:
        newMes = "".zfill(len(permutation))
        for i in range(2):
            for j in range(len(mes)):
                char = encodeCharWithAffineCipher(alf, mes[j], keyA, keyB)
                mes = mes[:j] + char + mes[j + 1:]
                newMes = newMes[:permutation[j]] + char + newMes[permutation[j] + 1:]

        decryptedText = decryptedText + newMes

    return decryptedText
