while True:
    try:
        e, g = map(float, raw_input().split())
        if g > 0:
            print e, g-1.0
    except:
        break
