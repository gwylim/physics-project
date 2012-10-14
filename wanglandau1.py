from random import random, randint
from math import exp, pi, cos, sin, sqrt, log
from sys import argv, stdout, stderr
from collections import defaultdict
from copy import copy

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

def wanglandau1(l, threshold, initial_r, epsilon, inner_loop, start, end):
    lattice = [[0 for i in xrange(l)] for i in xrange(l)]
    #reached_zero = False
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
            if (start > e and de > 0) or (start <= e+de <= end):
                p = difference(g, e+de, e)
                if p > 1 or random() < exp(p):
                    lattice[a][b] = new_value
                    e += de
                if e > start:
                    g[e] += r
                if e < end:
                    g[next[e]] -= r
                hist[e] += 1
                #if e == 0 and not reached_zero:
                #    reached_zero = True
                #    hist = [0 for i in xrange(max_e+1)]
        nonzero = copy(hist)
        nonzero = nonzero[start:end+1]
        if start == 0:
            nonzero.pop(5)
            nonzero.pop(3)
            nonzero.pop(2)
            nonzero.pop(1)

        for line in lattice:
            for x in line:
                print >>stderr, int(x),
            print >>stderr, '\n',
        ratio = float(min(nonzero)) / sum(nonzero) * len(nonzero)
        print >>stderr, ratio, r, start, end
        stderr.flush()

        if all(map(lambda x: x != 0, nonzero)) and ratio > threshold:
            hist = [0 for i in xrange(max_e+1)]
            r /= 2
        #f = open(argv[1], 'w')
        #for i, x in enumerate(g[start:end+1]):
        #    f.write(str(i) + " " + str(x) + "\n")
        #f.close()
        f = open(argv[2], 'w')
        for i, x in enumerate(hist[start:end+1]):
            f.write(str(i) + " " + str(x) + "\n")
        f.close()
    return g[start:end+1]

def wanglandau(l, threshold, initial_r, epsilon, inner_loop, divisions):
    max_e = 2*l*l
    start = 0
    end = max_e/divisions
    g = []
    while True:
        g1 = wanglandau1(l, threshold, initial_r, epsilon, inner_loop, start, end)
        for i in xrange(1, len(g1)):
            if start+i < len(g):
                g[start+i] = g1[i]
            else:
                g.append(g1[i])
        if end == max_e:
            break
        start, end = end-int(max_e*0.03), min(max_e, end+max_e/divisions)
        f = open(argv[1], 'w')
        for i, x in enumerate(g):
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

l = int(argv[3])
d = int(argv[4])
for i, x in enumerate(wanglandau(l, 0.8, 1.0, 1e-8, 100000, d)):
    print i, x
