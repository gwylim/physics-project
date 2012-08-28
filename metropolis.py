from random import random, randint
from math import exp
from sys import argv, stdout

def delta(i, j):
    if i==j: return 1
    else: return 0

def adjacent(l, x, y):
    for dx in [-1,0,1]:
        for dy in [-1,0,1]:
            if 0 <= x+dx < l and 0 <= y+dy < l and dx*dy == 0:
                yield (x+dx, y+dy)

def metropolis(l, n, k, beta):
    result = []
    for i in xrange(n):
        lattice = [[0 for i in xrange(l)] for i in xrange(l)]
        for j in xrange(k):
            while True:
                a, b = randint(0, l-1), randint(0, l-1)
                de = 0
                for x, y in adjacent(l, a, b):
                    de += 1-delta(1-lattice[a][b], lattice[x][y])
                if random() < exp(-beta*de):
                    lattice[a][b] = 1-lattice[a][b]
                    break

        result.append(lattice)
    return result

def energy(lattice):
    e = 0
    l = len(lattice)
    for a in xrange(l):
        for b in xrange(l):
            for x, y in adjacent(l, a, b):
                e += 1-delta(lattice[a][b], lattice[x][y])
    return e

def magnetization(lattice):
    m = 0
    for x in lattice:
        for y in x:
            m += 1 if y==0 else -1
    return m

n = int(argv[1])
l = int(argv[2])
k = l**3

for beta in xrange(1, 100, 1):
    beta1 = float(beta)/100
    m = float(sum(map(magnetization, metropolis(l, n, k, beta1))))/(n*l*l)
    print beta1, m
    stdout.flush()
