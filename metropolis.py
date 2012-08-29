from random import random, randint
from math import exp, pi, cos, sin, sqrt, log
from sys import argv, stdout, stderr
from collections import defaultdict

q = 10

def delta(i, j):
    if i==j: return 1
    else: return 0

def adjacent(l, x, y):
    for dx in [-1,0,1]:
        for dy in [-1,0,1]:
            if dx*dy == 0 and dx + dy != 0:
                yield ((x+dx)%l, (y+dy)%l)

def metropolis(l, n, k, beta):
    lattice = [[0 for i in xrange(l)] for i in xrange(l)]
    e = 0
    for a in xrange(l):
        for b in xrange(l):
            for x, y in adjacent(l, a, b):
                e += 1-delta(lattice[a][b], lattice[x][y])
    for i in xrange(n + k):
        while True:
            a, b = randint(0, l-1), randint(0, l-1)
            new_value = randint(0, q-1)
            de = 0
            for x, y in adjacent(l, a, b):
                de += - delta(new_value, lattice[x][y]) + delta(lattice[a][b], lattice[x][y])
            if random() < exp(-beta*de):
                lattice[a][b] = new_value
                e += de
                if i >= k: yield (e, lattice)
                break
        if i%100000 == 0:
            e = 0
            for a in xrange(l):
                for b in xrange(l):
                    for x, y in adjacent(l, a, b):
                        e += 1-delta(lattice[a][b], lattice[x][y])
def energy(lattice):
    e = 0
    l = len(lattice)
    for a in xrange(l):
        for b in xrange(l):
            for x, y in adjacent(l, a, b):
                e += 1-delta(lattice[a][b], lattice[x][y])
    return e

if argv[1] == 'dist':
    l = 20
    n = 1000000000
    k = 10000000
    beta = log(1 + sqrt(q))

    energies = defaultdict(int)
    min_e = 1e10
    max_e = 0

    for i, (e, lattice) in enumerate(metropolis(l, n, k, beta)):
        energies[e] += 1
        min_e = min(min_e, e)
        max_e = max(max_e, e)
        if i%100000 == 0:
            for line in lattice:
                for x in line:
                    print >>stderr, int(x),
                print >>stderr, '\n',
            print >>stderr, i, e, energies[e]
            stderr.flush()

            output = open(argv[1], 'w')
            for e in xrange(min_e, max_e+1):
                if e in energies:
                    print >>output, e, energies[e]
            output.close()
else:
    l = 20
    k = 2000000
    f = 20

    for beta in xrange(1400, 1450, 3):
        beta1 = beta/1000.0
        e = 0.0
        for i in xrange(f):
            e1, lattice = metropolis(l, 1, k, beta1).next()
            print >>stderr, beta1, i, e1
            stderr.flush()
            e += e1
        e /= f
        print beta1, e
        stdout.flush()
