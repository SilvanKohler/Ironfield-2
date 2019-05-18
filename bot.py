import random
import time

from opensimplex import OpenSimplex

howManyBots = 1
bots = []

directions = [['up', 'up', 'down', 'down', 'left', 'left', 'right', 'right', 'idle'], ['up', 'down', 'left', 'right', 'idle', 'idle'], ['up', 'down', 'left', 'right', 'idle']]
states = ['walker', 'idler', 'average']
class Bot():
    global directions
    def __init__(self):
        self.x = random.randint(-100, 100)/8
        self.y = random.randint(-100, 100)/8
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
            self.y -= 1/8
        elif direction == 'down':
            self.y += 1/8
        elif direction == 'left':
            self.x -= 1/8
        elif direction == 'right':
            self.x += 1/8
        self.movenum += 1
        print(self.state, self.frequency, self.x, self.y)
for i in range(howManyBots):
    bots.append(Bot())
frames = 0
fps = 10
while True:
    t = time.time()
    if frames%5 == 0:
        for bot in bots:
            bot.move()
    timeDif = time.time()-t
    if 1/fps-timeDif > 0:
        time.sleep(1/fps-timeDif)
    frames += 1
