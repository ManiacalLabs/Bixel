import colors

color_map = []
for y in range(16):
    row = [colors.hue2rgb_spectrum(x + (y << 4)) for x in range(16)]
    color_map.append(row)

def circles(matrix, buttons, data):
    if not data:
        data['circles'] = []

    matrix.clear()
    for x, y in buttons.int_high():
        data['circles'].append({'x': x, 'y': y, 'size': 1, 'color':  color_map[x][y]})

    new_list = []
    for c in data['circles']:
        x = c['x']
        y = c['y']
        size = c['size']
        color = c['color']

        if (x + size < 24 or x - size >= -8) or (y + size < 24 or y - size >= -8):
            matrix.drawCircle(x, y, int(size), color_map[x][y])
            c['size'] += 0.5
            new_list.append(c)

    data['circles'] = new_list
