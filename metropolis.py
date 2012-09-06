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
    l = int(argv[3])
    n = int(argv[4])
    k = int(argv[5])
    beta = float(argv[6])

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

            output = open(argv[2], 'w')
            for e in xrange(min_e, max_e+1):
                if e in energies:
                    print >>output, e, energies[e]
            output.close()
else:
    l = int(argv[1])
    k = int(argv[2])
    f = int(argv[3])
    a = int(argv[4])
    b = int(argv[5])
    s = int(argv[6])

    for beta in xrange(a, b, s):
        beta1 = beta/1000.0
        es = []
        for i in xrange(f):
            e, lattice = metropolis(l, 1, k, beta1).next()
            print >>stderr, beta1, i, e
            stderr.flush()
            es.append(e)
        mean_e = float(sum(es))/f
        stddev = sqrt(1.0/(f-1)*sum(map(lambda e: (e-mean_e)**2, es)))
        print beta1, mean_e, stddev/sqrt(f)
        stdout.flush()
