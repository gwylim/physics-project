from sys import stderr
from math import exp

f = open('output')
data = []
while True:
    try:
        e, g = map(float, f.readline().split())
        data.append((e,g))
    except:
        break
div=100
beg=1.0
end=2.0
print "clear"
print "reset"
print "set terminal gif animate delay 10"
print "set output \"animate.gif\""
print "set xrange [0:1000]"
print "set yrange [0:0.03]"
print "set xlabel \"Energy\""
print "set ylabel \"Probability\""
print "set isosample 40"
for i in xrange(div):
    beta = beg + (end-beg)*i/div
    partition = 0.0
    for e, g in data:
        partition += exp(g - e*beta)
    print "plot \"output\" using 1:(exp($2-$1*%f)/%f) title \"beta = %f\" with lines" % (beta, partition, beta)
