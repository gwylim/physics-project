from sys import argv, stderr
from math import exp
from copy import copy

start, end, step = float(argv[1]), float(argv[2]), float(argv[3])
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
    e = sum([i*exp(gbeta[i]) for i in g.iterkeys()])
    e2 = sum([i*i*exp(gbeta[i]) for i in g.iterkeys()])
    print beta, beta**2 * (e2 / partition - (e / partition)**2)
