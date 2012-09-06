from sys import argv, stderr
from math import exp

beta = float(argv[1])
while True:
    try:
        e, g = map(float, raw_input().split())
        if g != 0:
            print e, g - e*beta
    except Exception, e:
        break
