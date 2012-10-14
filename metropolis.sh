for ((l=20; l<=25; l+=5))
do
    nice -n19 pypy metropolis.py dist m$l $l $[l*l*500000] $[l*l*100] 1.42
done
