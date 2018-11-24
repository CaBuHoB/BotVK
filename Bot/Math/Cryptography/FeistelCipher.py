# -*- coding: utf-8 -*-


def getAlphabet():
    return "абвгдежзийклмнопрстуфхцчшщъыьэюя+-,.!?:\"vin()0123456789"


def fFunc(x, key, permutation):
    s = "".zfill(len(x))
    alf = getAlphabet()
    for i in range(len(x)):
        index = (alf.index(x[i]) * key) % len(alf)
        s = s[:permutation[i]] + alf[index] + s[permutation[i] + 1:]

    return s


def decoderFeistelCipher(message, keys, permutation):
    decryptedText = ""
    permutation = [int(x) for x in permutation]
    keys.reverse()
    alf = getAlphabet()
    chunks, chunk_size = len(message), len(permutation) * 2
    messages = [message[i:i + chunk_size] for i in range(0, chunks, chunk_size)]
    for mes in messages:
        chunks, chunk_size = len(mes), int(len(mes) / 2)
        mes = [mes[i:i + chunk_size] for i in range(0, chunks, chunk_size)]
        mes.reverse()
        for i in range(3):
            L = mes[1]
            R = "".zfill(len(mes[0]))
            f = fFunc(L, keys[i], permutation)
            for j in range(len(mes[0])):
                index = (alf.index(mes[0][j]) + alf.index(f[j])) % len(alf)
                R = R[:j] + alf[index] + R[j + 1:]
            mes[0], mes[1] = L, R

        decryptedText = decryptedText + mes[0] + mes[1]

    return decryptedText


print(decoderFeistelCipher(".гпщ0лнмп-д6е\"щх", [12, 40, 18], "0123"))
