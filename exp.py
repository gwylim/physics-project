from sys import argv, stderr
from math import exp

p = {}
while True:
    try:
        e, ge = map(float, raw_input().split())
        p[e] = exp(ge)
    except Exception, e:
        break

total_p = sum(p)

for e, pe in p.iteritems():
    print e, pe/total_p
