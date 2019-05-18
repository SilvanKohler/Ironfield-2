from opensimplex import OpenSimplex
import numpy as np
import os
import time

def dist(pos1, pos2):
    return (abs(pos1[0] - pos2[0]) ** 2 + abs(pos1[1] - pos2[1]) ** 2) ** 0.5

def cloudEffect(width, height, x, y):
    output = np.array([])
    n = OpenSimplex()
    middle = width//2, height//2
    for i in np.arange(height):
        newLine = np.array([])
        for j in np.arange(width):
            d = dist((j,i), middle)
            # newLine = np.append(newLine, d)
            newLine = np.append(newLine, n.noise2d(i/5 + y/20,j/50 + x/20) * (d))
        output = np.append(output, newLine)
    for i, n in enumerate(output):
        output[i] = int(n + 1)
    output = np.reshape(output, (height,width))
    return output

for x in np.arange(0,40):
    for line in cloudEffect(30, 30, x, 0):
        for p in line:
            print('  ' if p < 4 else 'XX' if p < 8 else 'MM', end='')
        print('')
    time.sleep(0.1)
    os.system('cls')