# -*- coding: utf-8 -*-


def isPrime(a):
    return all(a % i for i in range(2, int(a)))


def factorize(n):
    factors = []

    p = 2
    while True:
        while n % p == 0 and n > 0:
            factors.append(p)
            n = n / p
        p += 1
        if p > n / p:
            break
    if n > 1:
        factors.append(n)
    return factors


def calculateLegendre(a, p):
    if a >= p or a < 0:
        return calculateLegendre(a % p, p)
    elif a == 0 or a == 1:
        return a
    elif a == 2:
        if p % 8 == 1 or p % 8 == 7:
            return 1
        else:
            return -1
    elif a == p - 1:
        if p % 4 == 1:
            return 1
        else:
            return -1
    elif not isPrime(a):
        factors = factorize(a)
        product = 1
        for pi in factors:
            product *= calculateLegendre(pi, p)
        return product
    else:
        if ((p - 1) / 2) % 2 == 0 or ((a - 1) / 2) % 2 == 0:
            return int(calculateLegendre(p, a))
        else:
            return int((-1) * calculateLegendre(p, a))
