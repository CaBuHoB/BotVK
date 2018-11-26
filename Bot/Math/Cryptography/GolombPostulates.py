# -*- coding: utf-8 -*-


def GolombPostulates(number):
    numberOfZeros = 0
    numberOfUnits = 0
    for n in number:
        if n == "1":
            numberOfUnits = numberOfUnits + 1
        else:
            numberOfZeros = numberOfZeros + 1
