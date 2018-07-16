from __future__ import print_function

res = []
for y in range(16):
    res.append([])
for y in range(16):
    for x in range(16):
        xn = x % 8
        i = 0
        if y % 2:
            i += (7 - xn)
        else:
            i += xn
        i += (8 * y)
        if x >= 8:
            i += 128
        res[y].append(i)

for y in res:
    print(y)

