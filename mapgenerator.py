import numpy as np
from opensimplex import OpenSimplex
from random import randint
import os
from time import sleep

tmp = None
width = 1000
height = 1000
#https://prod.liveshare.vsengsaas.visualstudio.com/join?65737EB70B773A94B35DADBCA6735D1D4526
blocks = [
    'XX',
    '//',
    '**',
    '..',
    '**',
    '\\\\',
    'XX'
]
# blocks = []
# blockstr = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,^`'. "
# for block in blockstr:
#     blocks.append(block)
    

def select(x, y):
    global tmp
    return blocks[int((tmp.noise2d(x, y)+1)*len(blocks)/2)]

zoom = 20
for z in range(1, 6):
    tmp = OpenSimplex(seed=randint(0, 1000000))
    with open(f'map{z}.map', 'w') as map1:
        for y in range(0, height):
            for x in range(0, width):
                map1.write(select(x/zoom, y/zoom) + ',')
            map1.write('\n')
    print(f"finished map {z}")