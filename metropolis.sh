for l in 10 20 30 50
do
    nice -n19 pypy metropolis.py dist m$l $l $[l*l*500000] $[l*l*100] 1.424
done
