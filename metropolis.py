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
                e += delta(lattice[a][b], lattice[x][y])
    for i in xrange(n + k):
        while True:
            a, b = randint(0, l-1), randint(0, l-1)
            new_value = (lattice[a][b] + randint(-1, 1))%q
            de = 0
            for x, y in adjacent(l, a, b):
                de += - delta(new_value, lattice[x][y]) + delta(lattice[a][b], lattice[x][y])
            if random() < exp(-beta*de):
                lattice[a][b] = new_value
                e += de
                if i > k: yield (e, lattice)
                break

def energy(lattice):
    e = 0
    l = len(lattice)
    for a in xrange(l):
        for b in xrange(l):
            for x, y in adjacent(l, a, b):
                e += 1-delta(lattice[a][b], lattice[x][y])
    return e

def magnetization(lattice):
    mx, my = 0, 0
    for x in lattice:
        for s in x:
            mx += cos(s*2*pi/q)
            my += sin(s*2*pi/q)
    return (mx, my)

l = 50
n = 1000000000
k = 10000000
beta = log(1+sqrt(q))

energies = defaultdict(int)
min_e = 1e10
max_e = 0

for i, (e, lattice) in enumerate(metropolis(l, n, k, beta)):
    e = int(2*e)
    energies[e] += 1
    min_e = min(min_e, e)
    max_e = max(max_e, e)
    if i%100000 == 0:
        mx, my = magnetization(lattice)
        for line in lattice:
            for x in line:
                print >>stderr, int(x),
            print >>stderr, '\n',
        print >>stderr, i, e, energies[e], sqrt(mx**2 + my**2)/(l**2)
        stderr.flush()

        output = open(argv[1], 'w')
        for e in xrange(min_e, max_e+1):
            if e in energies:
                print >>output, e, energies[e]
        output.close()
