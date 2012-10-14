from sys import argv, stderr
from math import exp

p = {}
while True:
    try:
        e, pe = map(float, raw_input().split())
        if pe != 0:
            p[e] = pe
    except Exception, e:
        break

total_p = sum(p.itervalues())

for e, pe in p.iteritems():
    print e, pe/total_p
