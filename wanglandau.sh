for ((l=15; l<=25; l+=5))
do
    pypy wanglandau.py ds$l h$l $l
done
