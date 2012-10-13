for ((l=15; l<=25; l+=5))
do
    pypy metropolis.py dist metropolis_convergence$l $l $[l*l*50000] $[l*l*100] 1.417
done
