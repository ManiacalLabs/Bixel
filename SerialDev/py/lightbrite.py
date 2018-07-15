import colors


clist = [
    colors.Off,
    colors.Red,
    colors.Orange,
    colors.Yellow,
    colors.Green,
    colors.Blue,
    colors.Purple  # maybe colors.Fuchsia?
]

def lightbrite(matrix, buttons, data):
    if not data:
        data['pegs'] = [[0 for y in range(16)] for x in range(16)]

    for x, y in buttons.int_high():
        data['pegs'][x][y] += 1
        if data['pegs'][x][y] >= len(clist):
            data['pegs'][x][y] = 0
        matrix.set(x, y, clist[data['pegs'][x][y]])

