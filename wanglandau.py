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

def difference(g, a, b):
    if b < a:
        return -difference(g, b, a)
    result = 0.
    for i in xrange(a+1, b+1):
        result += g[i]
    return result

def wanglandau(l, threshold, initial_r, epsilon, inner_loop):
    lattice = [[0 for i in xrange(l)] for i in xrange(l)]
    reached_zero = False
    max_e = 2*l*l
    g = [0. for i in xrange(max_e+1)]
    next = range(1, max_e+1)
    next[0] = 4
    next[4] = 6
    hist = [0 for i in xrange(max_e+1)]
    r = initial_r
    e = 0
    for a in xrange(l):
        for b in xrange(l):
            for x, y in adjacent(l, a, b):
                e += 1-delta(lattice[a][b], lattice[x][y])
    while r > epsilon:
        for i in xrange(inner_loop):
            a, b = randint(0, l-1), randint(0, l-1)
            new_value = randint(0, q-1)
            de = 0
            for x, y in adjacent(l, a, b):
                de += - delta(new_value, lattice[x][y]) + delta(lattice[a][b], lattice[x][y])
            p = difference(g, e+de, e)
            if p > 1 or random() < exp(p):
                lattice[a][b] = new_value
                e += de
            if e > 0:
                g[e] += r
            if e < max_e:
                g[next[e]] -= r
            hist[e] += 1
            if e == 0 and not reached_zero:
                reached_zero = True
                hist = [0 for i in xrange(max_e+1)]
        nonzero = filter(lambda x: x != 0, hist)

        for line in lattice:
            for x in line:
                print >>stderr, int(x),
            print >>stderr, '\n',
        print >>stderr, float(min(nonzero)) / max(nonzero), r
        stderr.flush()

        if len(hist)-len(nonzero) < 10 and float(min(nonzero)) / max(nonzero) > threshold:
            hist = [0 for i in xrange(max_e+1)]
            r /= 2
        f = open(argv[1], 'w')
        for i, x in enumerate(g):
            f.write(str(i) + " " + str(x) + "\n")
        f.close()
        f = open(argv[2], 'w')
        for i, x in enumerate(hist):
            f.write(str(i) + " " + str(x) + "\n")
        f.close()
    return g

def energy(lattice):
    e = 0
    l = len(lattice)
    for a in xrange(l):
        for b in xrange(l):
            for x, y in adjacent(l, a, b):
                e += 1-delta(lattice[a][b], lattice[x][y])
    return e

for i, x in enumerate(wanglandau(int(argv[3]), 0.8, 1.0, 1e-8, 1000000)):
    print i, x
