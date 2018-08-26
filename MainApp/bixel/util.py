def srange(a, b, step=1):
    if a <= b:
        return range(a, b + 1, step)
    else:
        return range(b, a - 1, -1 * step)