import os
import time

import numpy as np
from opensimplex import OpenSimplex
#https://prod.liveshare.vsengsaas.visualstudio.com/join?91D41FFC1FF54C18E80F478C19B8AFFED337
def dist(pos1, pos2):
    return (abs(pos1[0] - pos2[0]) ** 2 + abs(pos1[1] - pos2[1]) ** 2) ** 0.5

def cloudEffect(width, height, x, y, wind):
    output = np.array([])
    n = OpenSimplex()
    middle = width//2, height//2
    for i in np.arange(height):
        newLine = np.array([])
        for j in np.arange(width):
            d = dist((j,i), middle)
            # newLine = np.append(newLine, d)
            newLine = np.append(newLine, (n.noise2d(i/5 + y*2.5,j/100 + x/5 + wind) + 1) * (d))
        output = np.append(output, newLine)
    output = np.reshape(output, (height,width))
    return output

if __name__ == '__main__':
    for x in np.arange(0,40):
        for line in cloudEffect(30, 30, x, 0):
            for p in line:
                print('  ' if p < 4 else '  ' if p < 6 else 'MM', end='')
            print('')
        time.sleep(0.1)
        os.system('cls')
