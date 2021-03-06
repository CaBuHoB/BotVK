# -*- coding: utf-8 -*-
from random import randrange

from reportlab import xrange
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from math import gcd

from Bot.Math.Cryptography import LegendreSymbol


def primfacs(n):
    i = 2
    primfac = []
    while i * i <= n:
        while n % i == 0:
            primfac.append(i)
            n = n / i
        i = i + 1
    if n > 1:
        primfac.append(n)
    return primfac


def powMinusFirst(a, mod):
    res = 0.0
    chisl = 1
    flag = False
    while not flag:
        res = chisl * 1.0 / a
        chisl += mod
        flag = (res - int(res)) == 0.0

    return int(res)


def createPDFFile(data, userId):
    doc = SimpleDocTemplate("/tmp/krouk" + userId + ".pdf", pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    Story = []
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

    data2 = data[:len(data) - 1]
    t = Table(data2, spaceBefore=25, spaceAfter=25)
    t.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))

    ptext = '<font size=12>%s</font>' % data[len(data) - 1][0]
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))

    doc.build(Story)
    return doc.filename


def toBinary(n):
    r = []
    while n > 0:
        r.append(n % 2)
        n = n / 2
    return r


def MillerRabin(n, k=10):
    if n == 2:
        return True
    if not n & 1:
        return False

    # noinspection PyShadowingNames
    def check(a, s, d, n):
        x = pow(a, d, n)
        if x == 1:
            return True
        for i in xrange(s - 1):
            if x == n - 1:
                return True
            x = pow(x, 2, n)
        return x == n - 1

    s = 0
    d = n - 1

    while d % 2 == 0:
        d >>= 1
        s += 1

    for i in xrange(k):
        a = randrange(2, n - 1)
        if not check(a, s, d, n):
            return False
    return True


def getFile(task, userId):
    task = task.split(" ")
    if len(task) != 3:
        return 'Чет не так с данными, введи по образцу', False, None

    data = []

    mod = int(task[2])
    if mod > 1000000:
        return 'Сомневаюсь, что ты правильно записал числа из задания. Иначе сочувствую, над тобой' \
               'издеваются. Я не смогу прислать решение такого сравнения (', False, None
    a = int(task[1]) % mod

    if mod <= 2 or not MillerRabin(mod):
        return 'mod должен быть простым и больше двух )', False, None

    if gcd(a, mod) != 1:
        return 'a и mod должены быть взаимнопростыми', False, None

    N = 0
    for i in range(3, mod - 1):
        if LegendreSymbol.calculateLegendre(i, mod) == -1:
            N = i
            break
    factorization = primfacs(mod - 1)
    k = len(factorization) - 1
    h = int(factorization[k])
    a1 = pow(a, int(((h + 1) / 2)), mod)
    a2 = powMinusFirst(a, mod)
    N1 = pow(N, h, mod)
    N2 = 1

    data.append(['i', 'b', 'c', 'd', 'j', 'N2'])

    for i in range(k - 1):
        b = a1 * N2 % mod
        c = (((a2 * b) % mod) * b) % mod
        d = pow(c, pow(2, k - 2 - i), mod)
        if d != 1:
            d = d - mod
        if d == 1:
            j = 0
        else:
            j = 1
        N2 = N2 * pow(N1, pow(2, i, mod) * j, mod) % mod
        data.append([str(i), str(b), str(c), str(d), str(j), str(N2)])

    x = a1 * N2 % mod
    data.append(['x = +- ' + str(x) + ' (mod ' + str(mod) + ')'])

    return createPDFFile(data, userId), True, None
