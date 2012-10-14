for ((l=20; l<=25; l+=5))
do
    nice -n19 pypy wanglandau.py ds$l h$l $l
done
