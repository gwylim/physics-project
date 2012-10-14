from sys import argv, stderr
from math import exp

beta = float(argv[1])
p = {}
while True:
    try:
        e, ge = map(float, raw_input().split())
        if ge != 0:
            p[e] = ge - beta*e
    except Exception, e:
        break

max_p = max(p.itervalues())
for e in p.iterkeys():
    p[e] -= max_p

for e, pe in p.iteritems():
    print e, pe
