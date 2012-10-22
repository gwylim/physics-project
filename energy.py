from sys import argv, stderr
from math import exp
from copy import copy

l, start, end, step = int(argv[1]), float(argv[2]), float(argv[3]), float(argv[4])
g = {}
while True:
    try:
        e, ge = map(float, raw_input().split())
        if ge != 0:
            g[e] = ge
    except Exception, e:
        break

for b in xrange(int((end-start)/step)):
    beta = start + b*step
    gbeta = {}
    max_gbeta = 0
    for i in g.iterkeys():
        gbeta[i] = g[i] - beta*i
    max_gbeta = max(gbeta.itervalues())
    for i in gbeta.iterkeys():
        gbeta[i] -= max_gbeta
    partition = sum([exp(gbeta[i]) for i in g.iterkeys()])
    e = sum([i*exp(gbeta[i]) for i in g.iterkeys()]) / partition
    print beta, e / l**2
