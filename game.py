import os
import pickle
# import mysql.connector
import random  # , mysql.connector
import socket
import sys
import threading
import time
from time import sleep

import numpy as np
from asciimatics.renderers import Rainbow
from asciimatics.screen import Screen
from opensimplex import OpenSimplex

import cloudeffect

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = ('localhost', 6969)

players = []
NAME = 0
POS = 1 # [y, x]
DIR = 2 # 'left' 'right' 'up' 'down'

blocks = [
    'XX',
    '//',
    '**',
    '..',
    '**',
    '\\\\',
    'XX'
]
barrier = '##'
boundaries = [(-100,100), (-100,100)]
player = None
height = 20
width = 20
seed = 4908
default_zoom = 8
runthreads = True
directions = [['up', 'up', 'down', 'down', 'left', 'left', 'right', 'right', 'idle'], ['up', 'down', 'left', 'right', 'idle', 'idle'], ['up', 'down', 'left', 'right', 'idle']]
states = ['walker', 'idler', 'average']
howManyBots = 10
bots = []
class Character():
    global width, height
    def __init__(self):
        self.x = -0.125
        self.y = 0.75
        self.name = ''
        self.direction = 'right'
        self.char = '[}'
    def move(self, direction):
        self.direction = direction
        if direction == 'up':
            self.char = '[}'
            for bot in bots:
                if bot.y == self.y-1/8 and bot.x == self.x:
                    return
            self.y -= 1/8
        if direction == 'down':
            self.char = '{]'
            for bot in bots:
                if bot.y == self.y+1/8 and bot.x == self.x:
                    return
            self.y += 1/8
        if direction == 'left':
            self.char = '{]'
            for bot in bots:
                if bot.x == self.x-1/8 and bot.y == self.y:
                    return
            self.x -= 1/8
        if direction == 'right':
            self.char = '[}'
            for bot in bots:
                if bot.x == self.x+1/8 and bot.y == self.y:
                    return
            self.x += 1/8

player = Character()



# class Bot():
#     global directions
#     def __init__(self):
#         self.x = random.randint(-100, 100)/8
#         self.y = random.randint(-100, 100)/8
#         self.char = '()'
#     def move(self):
#         direction = random.choice(directions)
#         if direction == 'up':
#             self.y -= 1/8
#         elif direction == 'down':
#             self.y += 1/8
#         elif direction == 'left':
#             self.x -= 1/8
#         elif direction == 'right':
#             self.x += 1/8
# for i in range(howManyBots):
#     bots.append(Bot())
class Bot():
    global directions
    def __init__(self):
        self.x = random.randint(-1, 1)/8
        self.y = random.randint(-1, 1)/8
        self.char = '()'
        self.movenum = 0
        self.state = random.choice(states)
        self.frequency = random.randint(15, 20)
        self.seed = random.randint(0, 1000000)
        self.noise = OpenSimplex(seed=self.seed)
    def move(self):
        self.movenum += 1
        if self.state == 'walker':
            index = int((self.noise.noise2d(0, self.movenum * (1/self.frequency))+1)*8)%9
            direction = directions[states.index(self.state)][index]
        elif self.state == 'idler':
            index = int((self.noise.noise2d(0, self.movenum * (1/self.frequency))+1)*5)%6
            direction = directions[states.index(self.state)][index]
        elif self.state == 'average':
            index = int((self.noise.noise2d(0, self.movenum * (1/self.frequency))+1)*4)%5
            direction = directions[states.index(self.state)][index]
        if direction == 'up':
            for bot in bots:
                if bot.y == self.y-1/8 and bot.x == self.x:
                    return
            self.y -= 1/8
        elif direction == 'down':
            for bot in bots:
                if bot.y == self.y+1/8 and bot.x == self.x:
                    return
            self.y += 1/8
        elif direction == 'left':
            for bot in bots:
                if bot.x == self.x-1/8 and bot.y == self.y:
                    return
            self.x -= 1/8
        elif direction == 'right':
            for bot in bots:
                if bot.x == self.x+1/8 and bot.y == self.y:
                    return
            self.x += 1/8
        self.movenum += 1
for i in range(howManyBots):
    bots.append(Bot())
# def generateMap(width, height):
#     output = []
#     for i in range(height):
#         newLine = []
#         for j in range(width):
#             newLine.append(random.choice(['..', 'MM', 'XX', '¦¦']))
#         output.append(newLine)
#     return output

# with open(f'map{mp}.map') as loadedmap:
#     for line in loadedmap.readline():
#         map_tmp = []
#         for char in line.split(','):
#             map_tmp.append(char)
#         mapp.append(map_tmp)

def renderMap(x, y, width, height, seed, zoom=default_zoom, boundaries=[(-100, 100), (-100, 100)]):
    noise = OpenSimplex(seed=seed)
    screen = np.array([])

    for i in np.arange(-height//2, height//2):
        newLine = np.array([])
        for j in np.arange(-width//2, width//2):
            newLine = np.append(newLine, noise.noise2d(y + i * (1/zoom), x + j * (1/zoom)))
        screen = np.append(screen, newLine)

    output = np.reshape(screen, (height, width))

    newOut = np.array([], dtype=str)
    for i in np.reshape(output, output.size):
        index = int((i + 1) * len(blocks)/2)

        char = blocks[index]

        newOut = np.append(newOut, char)
        
    output = np.reshape(newOut, (height, width))

    return output


# for i in np.arange(1,20):
#     map1 = renderMap(i * i * 0.01, 0, 2 * i, 2 * i, seed, zoom=i) 
#     for line in map1:
#         for block in line:
#             print(block, end='')
#         print('')
    
#     os.system('cls')

def game(screen):
    screen.set_title('Ironfield 2')
    global player
    frames = 0
    fps = 10
    while True:
        global players
        if frames%5 == 0:
            for bot in bots:
                bot.move()
        t = time.time()
        terrain = renderMap(player.x, player.y, width, height, seed)
        # print(len(terrain), len(terrain[0]))

        # Rahmen:
        screenOff = [1,1]
        # clouds = cloudeffect.cloudEffect(width, height, player.x, player.y)
        # newclouds = np.zeros((height, width))
        # for i, p in enumerate(clouds):
        #     print(i, p)
        #     newclouds[i] = 1 if p < 5 else 0
        # clouds = newclouds

        corner = '+'
        screen.print_at(corner, 0,0)
        screen.print_at(corner, width * 2 + screenOff[0],0)
        screen.print_at(corner, 0,height + screenOff[1])
        screen.print_at(corner, width * 2 + screenOff[0],height + screenOff[1])
        for x in range(width * 2):
            screen.print_at('-', x + screenOff[0], 0)
            screen.print_at('-', x + screenOff[0], height + screenOff[1])
        for y in range(height):
            screen.print_at('¦', 0, y + screenOff[1])
            screen.print_at('¦', width * 2 + screenOff[0], y + screenOff[1])
        #===============
        screen.print_at('                       ', 0, height+screenOff[1]*2)
        screen.print_at(f'y: {int(player.y*8)}, x: {int(player.x*8)}', 0, height+screenOff[1]*2)
        
        for y in range(height):
            for x in range(width):
                if y == height/2 and x * 2 == width:
                    screen.print_at(player.char, x * 2 + screenOff[0], y + screenOff[1], colour=1)
                else:
                    if terrain[y][x] == '**':
                        screen.print_at(terrain[y][x], x * 2 + screenOff[0], y + screenOff[1], colour=2)
                    elif terrain[y][x] == '\\\\' or terrain[y][x] == '//':
                        screen.print_at(terrain[y][x], x * 2 + screenOff[0], y + screenOff[1], colour=3)
                    elif terrain[y][x] == 'XX':
                        screen.print_at(terrain[y][x], x * 2 + screenOff[0], y + screenOff[1], colour=4)
                    else:
                        screen.print_at(terrain[y][x], x * 2 + screenOff[0], y + screenOff[1])
                pass
        for p, y in zip(players, range(len(players))):
            screen.print_at(str(p), width*2+screenOff[0], y)
        colour = 0
        for bot in bots:
            colour = 5 if bot.state == 'walker' else 6 if bot.state == 'idler' else 7
            if abs(player.y*8 - bot.y*8)  < height//2 and abs(player.x*8 - bot.x*8) < width//2:
                screen.print_at(bot.char, int(bot.x*16 - player.x*16 + width) + screenOff[0], int(bot.y - player.y*8 + height/2) + screenOff[1], colour=colour)
        for p in players:
            colour += 1
            colour %= 7
            if p[DIR] == 'right' or p[DIR] == 'up':
                char = '[}'
            elif p[DIR] == 'left' or p[DIR] == 'down':
                char = '{]'
            # if abs(player.y*8 - p[POS][1]*8)  < height//2 and abs(player.x*8 - p[POS][0]*8) < width//2:
            if abs(player.y*8 - p[POS][1]*8)  < height//2 and abs(player.x*8 - p[POS][0]*8) < width//2:
                screen.print_at(char, int(p[POS][0]*16 - player.x*16 + width) + screenOff[0], int(p[POS][1]*8 - player.y*8 + height/2) + screenOff[1], colour=colour+1)
            
        # i = 0
        # for objects in terrain:
        #     for obj in objects:
        #         print(obj, end='')
        #     print()
        # os.system('cls')
        screen.refresh()
        timeDif = time.time()-t
        if 1/fps-timeDif > 0:
            time.sleep(1/fps-timeDif)
        ev = screen.get_key()
        if ev in (ord('W'), ord('w'), -204):
            player.move('up')
        elif ev in (ord('S'), ord('s'), -206):
            player.move('down')
        elif ev in (ord('A'), ord('a'), -203):
            player.move('left')
        elif ev in (ord('D'), ord('d'), -205):
            player.move('right')
        elif ev in (ord('Q'), ord('q')):
            runthreads = False
            client.close()
            quit()
            print(renderMap(player.x, player.y, width, height, seed))
            return
        elif not ev is None:
            print(ev)
        frames += 1
class upload(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while runthreads:
            client.send(pickle.dumps([player.name, [player.x, player.y], player.direction]))
            sleep(0.1)
class download(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        global players
        while runthreads:
            someplayer = client.recv(256)
            weg = False
            for index, item in enumerate(players):
                if item[0] == pickle.loads(someplayer)[0]:
                    players[index] = pickle.loads(someplayer)
                    weg = True
                    break
            if not weg:
                players.append(pickle.loads(someplayer))
def __init__(name):
    player.name = name
    print('name set')
    try:
        client.connect(server)
    except:
        print('SERVER OFFLINE OR NO CONNECTION TO THE INTERNET')
    print('connected')
    thread1 = upload()
    print('uploaded')
    thread2 = download()
    print('downloaded')
    thread1.start()
    print('start 1')
    thread2.start()
    print('start 2')
    Screen.wrapper(game)
if __name__ == "__main__":
    quit()
