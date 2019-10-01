# -*- coding: utf-8 -*-
from Bot.Math.latexBuild import *


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


def fFunc(mes, key, permutation, latex):
    lenAlf = len(getAlphabet())
    fMes = [(m * key) % lenAlf for m in mes]
    latex = latex + r"$f = P(" + str(fMes) + r") = "
    fMes = permutationFunc(fMes, permutation)
    latex = latex + str(fMes) + r"$ \\"

    return fMes, latex


def feistelCipher(message, keys, permutation, index, latex):
    halfMessageLength = int(len(message)/2)
    mes = [message[:halfMessageLength], message[halfMessageLength:]]
    latex = latex + r"$L_" + str(3 - index) + ":" + str(mes[0])
    latex = latex + r"~~R_" + str(3 - index) + str(mes[1]) + r"$ ~\\"
    R = mes[0]
    L = mes[1]
    latex = latex + r"$R_" + str(2 - index) + "=" + r"L_" + str(3 - index) + "=" + str(R) + r"$ \\"
    fMas, latex = fFunc(R, keys[index], permutation, latex)
    for i in range(halfMessageLength):
        L[i] = (L[i] - fMas[i]) % 55
    latex = latex + r"$L_" + str(2 - index) + r"=" + r"R_" + str(3 - index) + r"- f = "
    latex = latex + str(L) + r"$ \\ ~\\"

    return L + R, latex


def decoderFeistelCipher(message, keys, permutation, fromID):
    latex = getPreamble()
    permutation = [int(x) for x in permutation]
    keys.reverse()

    blockLength = len(permutation) * 2

    latex = latex + r"~\\Шифртекст: " + message + r"\\"
    latex = latex + r"Длина блока " + str(blockLength) + r"\\"
    latex = latex + r"$key1:" + str(keys[0]) + r";~key2:" + str(keys[1]) + r";~key3:" + str(keys[2]) + r"$ \\ \\"

    messages = [list(message[i:i + blockLength]) for i in range(0, len(message), blockLength)]
    messagesInt = mesToInt(messages)

    for i in range(len(messagesInt)):
        latex = latex + getMinipageBegin(80, 2) if i == 0 else latex + getMinipageBegin(80)
        latex = latex + r"\begin{center}"
        latex = latex + ''.join(messages[i]) + r" ~ = ~ $" + str(messagesInt[i]) + r"$\\ ~\\"
        for j in range(3):
            messagesInt[i], latex = feistelCipher(messagesInt[i], keys, permutation, j, latex)

        messageStr = messagesIntToStr([messagesInt[i]])
        latex = latex + r"$\underbrace{" + str(messagesInt[i][:len(permutation)])[:-1] + r",}_L"
        latex = latex + r"\underbrace{" + str(messagesInt[i][len(permutation):])[1:] + r"}_R "
        latex = latex + r" \Longrightarrow \text{" + messageStr + r"}$\\ \end{center}"
        latex = latex + getMinipageEnd()

    message = messagesIntToStr(messagesInt)

    latex = latex + r"\\ ~\\ ~\\Ответ: " + message + getEnd()
    name = str(fromID) + 'FeistelCipher.pdf'
    createPDF(latex, '/tmp', name)
    return os.path.join('/tmp', name)
