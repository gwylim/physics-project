undefined = [1,2,3,5]

i = 0
t = 0.
while True:
    try:
        e, g = map(float,raw_input().split())
        if e not in undefined:
            t += g
            print e, t
    except:
        break
