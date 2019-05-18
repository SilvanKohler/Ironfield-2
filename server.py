import pickle
import socket
import sys
import threading

clients = []
CHUNK = 4096
count = 0
users = 0
directions = [['up', 'up', 'down', 'down', 'left', 'left', 'right', 'right', 'idle'], ['up', 'down', 'left', 'right', 'idle', 'idle'], ['up', 'down', 'left', 'right', 'idle']]
states = ['walker', 'idler', 'average']
howManyBots = 10
bots = []


class lobby(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        global count
        threading.Thread.__init__(self)
        self.num = count
        count += 1
        clients.append(clientsocket)
        self.csocket = clientsocket
        self.addr = clientAddress
        print('Client at ' + str(self.addr) + ' queued...')
    def run(self):
        global count
        global users
        print('Client at ' + str(self.addr) + ' joined the game')
        users += 1
        print('{} users'.format(users))
        while True:
            try:
                data = self.csocket.recv(CHUNK)
                print(pickle.loads(data))
            except:
                print('Client at ' + str(self.addr) + ' disconnected...')
                clients.remove(clients[self.num])
                count -= 1
                users -= 1
                print('{} users'.format(users))
                break
            finally:
                for i in range(len(clients)):
                    if not i == self.num:
                        try:
                            clients[i].send(data)
                        except:
                            pass
if len(sys.argv) > 1:
    IP = sys.argv[1]
    PORT = int(sys.argv[2])
else:
    IP = '0.0.0.0'
    PORT = 6969
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((IP, PORT))
print('Server started on ' + str(IP) + ':' + str(PORT))
print('Waiting for client request..')
class listen(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while True:
            try:
                server.listen(1)
                clientsock, clientAddress = server.accept()
                newthread = lobby(clientAddress, clientsock)
                newthread.start()
            except:
                pass
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
class BotAdministration(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        for i in range(howManyBots):
            bots.append(Bot())
    def run(self):
        while True:
            for bot in bots:-
                bot.move()
thread1 = listen()
thread2 = BotAdministration()
thread1.start()
thread2.start()
