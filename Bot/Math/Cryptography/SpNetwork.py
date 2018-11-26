# -*- coding: utf-8 -*-
from Bot.Math.latexBuild import *


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


def spNetwork(message, keyA, keyB, permutation, latex):
    latex = latex + "$P: " + str(message) + r" \Longrightarrow "
    message = permutationFunc(message, permutation)
    latex = latex + str(message) + r"$\\"

    latex = latex + r"$S: " + str(message) + r" \Longrightarrow "
    for i in range(len(message)):
        message[i] = encodeCharWithAffineCipher(message[i], keyA, keyB)
    latex = latex + str(message) + r"$\\ ~\\"

    return message, latex


def messagesIntToStr(messages):
    alf = getAlphabet()
    text = ""
    for mes in messages:
        for index in mes:
            text = text + alf[index]

    return text


def decoderSpNetwork(message, keyA, keyB, permutation, fromID):
    latex = getPreamble()
    permutation = [abs(int(num) - 4) for num in permutation]
    permutation.reverse()
    blockLength = len(permutation)

    latex = latex + r"~\\Шифртекст: " + message + r"\\"
    latex = latex + r"Длина блока " + str(blockLength) + r"\\"
    latex = latex + r"$\{a:" + str(keyA) + r";~b:" + str(keyB) + r"\}$ \\"
    latex = latex + r"$P = " + str(permutation) + r"$\\"
    latex = latex + r"$D(x) = a^{-1} \cdot (x-b) ~ mod ~m$ \\ \\"

    messages = [list(message[i:i + blockLength]) for i in range(0, len(message), blockLength)]
    messagesInt = mesToInt(messages)

    for i in range(len(messagesInt)):
        latex = latex + getMinipageBegin(80, 2) if i == 0 else latex + getMinipageBegin(80)
        latex = latex + r"\begin{center}"
        latex = latex + ''.join(messages[i]) + r" ~ = ~ $" + str(messagesInt[i]) + r"$\\ ~\\"
        for j in range(2):
            messagesInt[i], latex = spNetwork(messagesInt[i], keyA, keyB, permutation, latex)

        messageStr = messagesIntToStr([messagesInt[i]])
        latex = latex + r"$" + str(messagesInt[i]) + r" \Longrightarrow \text{" + messageStr + r"}$\\"
        latex = latex + r"\end{center}"
        latex = latex + getMinipageEnd()

    message = messagesIntToStr(messagesInt)

    latex = latex + r"\\ ~\\Ответ: " + message + getEnd()
    name = str(fromID) + 'SpNetwork.pdf'
    createPDF(latex, '/tmp', name)
    return os.path.join('/tmp', name)
