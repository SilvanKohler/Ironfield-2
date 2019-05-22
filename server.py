# import pickle
# import random
# import socket
# import sys
# import threading
# import time
# from time import sleep

# from opensimplex import OpenSimplex

# clients = []
# CHUNK = 2048
# count = 0
# users = 0
# directions = [['up', 'up', 'down', 'down', 'left', 'left', 'right', 'right', 'idle'], ['up', 'down', 'left', 'right', 'idle', 'idle'], ['up', 'down', 'left', 'right', 'idle']]
# states = ['walker', 'idler', 'average']
# howManyBots = 100
# bots = []
# frames = 0
# fps = 10

# class lobby(threading.Thread):
#     def __init__(self, clientAddress, clientsocket):
#         global count
#         global clients
#         threading.Thread.__init__(self)
#         self.num = count
#         count += 1
#         clients.append(clientsocket)
#         self.csocket = clientsocket
#         self.addr = clientAddress
#         print('Client at ' + str(self.addr) + ' queued...')
#     def run(self):
#         global count
#         global users
#         global clients
#         print('Client at ' + str(self.addr) + ' joined the game')
#         users += 1
#         print('{} users'.format(users))
#         while True:
#             try:
#                 data = self.csocket.recv(CHUNK)
#             except:
#                 print('Client at ' + str(self.addr) + ' disconnected...')
#                 clients.remove(self.csocket)
#                 count -= 1
#                 users -= 1
#                 print('{} users'.format(users))
#                 break
#             finally:
#                 if pickle.loads(data)[0] == 'targethitbot':
#                     for b in bots:
#                         if bots.index(b) == pickle.loads(data)[1][0]:
#                             if pickle.loads(data)[1][1] <= 0:
#                                 bots.remove(b)
#                             else:
#                                 b.health = pickle.loads(data)[1][1]
#                             break
#                 for i in range(len(clients)):
#                     if not clients[i] == self.csocket:
#                         clients[i].send(data)
#             sleep(0.2)
                    
# if len(sys.argv) > 1:
#     IP = sys.argv[1]
#     PORT = int(sys.argv[2])
# else:
#     IP = '0.0.0.0'
#     PORT = 6969
# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# server.bind((IP, PORT))
# print('Server started on ' + str(IP) + ':' + str(PORT))
# print('Waiting for client request..')
# class listen(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#     def run(self):
#         while True:
#             try:
#                 server.listen(1)
#                 clientsock, clientAddress = server.accept()
#                 newthread = lobby(clientAddress, clientsock)
#                 newthread.start()
#             except:
#                 pass
# class Bot():
#     global directions
#     def __init__(self):
#         self.x = ((random.randint(-98, 98)*10)/8)/10
#         self.y = ((random.randint(-98, 98)*10)/8)/10
#         self.char = '()'
#         self.movenum = 0
#         self.state = random.choice(states)
#         self.frequency = random.randint(15, 20)
#         self.seed = random.randint(0, 1000000)
#         self.noise = OpenSimplex(seed=self.seed)
#         self.health = 100
#     def move(self):
#         self.movenum += 1
#         if self.state == 'walker':
#             index = int((self.noise.noise2d(0, self.movenum * (1/self.frequency))+1)*8)%9
#             direction = directions[states.index(self.state)][index]
#         elif self.state == 'idler':
#             index = int((self.noise.noise2d(0, self.movenum * (1/self.frequency))+1)*5)%6
#             direction = directions[states.index(self.state)][index]
#         elif self.state == 'average':
#             index = int((self.noise.noise2d(0, self.movenum * (1/self.frequency))+1)*4)%5
#             direction = directions[states.index(self.state)][index]
#         if direction == 'up':
#             for bot in bots:
#                 if bot.y == self.y-1/8 and bot.x == self.x:
#                     return
#             if self.y - 1/8 <= 100/8:
#                 return
#             self.y -= 1/8
#         elif direction == 'down':
#             for bot in bots:
#                 if bot.y == self.y+1/8 and bot.x == self.x:
#                     return
#             if self.y + 1/8 >= 100/8:
#                 return
#             self.y += 1/8
#         elif direction == 'left':
#             for bot in bots:
#                 if bot.x == self.x-1/8 and bot.y == self.y:
#                     return
#             if self.x - 1/8 <= 100/8:
#                 return
#             self.x -= 1/8
#         elif direction == 'right':
#             for bot in bots:
#                 if bot.x == self.x+1/8 and bot.y == self.y:
#                     return
#             if self.x + 1/8 >= 100/8:
#                 return
#             self.x += 1/8
#         self.movenum += 1
# class BotAdministration(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#         for i in range(howManyBots):
#             bots.append(Bot())
        
#     def run(self):
#         pass
# class BotSending(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#     def run(self):
#         global frames
#         global clients
#         while True:
#             try:
#                 t = time.time()
#                 if frames%2 == 0:
#                     for bot in bots:
#                         bot.move()
#                 datalist = ['botdata', []]
#                 for bot in bots:
#                     datalist[1].append([bots.index(bot), [bot.x, bot.y], bot.state, bot.health])
#                 for i in range(len(clients)):
#                     clients[i].send(pickle.dumps(datalist))
#                 timeDif = time.time()-t
#                 if 1/fps-timeDif > 0:
#                     time.sleep(1/fps-timeDif)
#                 frames += 1
#             except:
#                 pass
            
# thread1 = listen()
# thread2 = BotAdministration()
# thread3 = BotSending()
# thread1.start()
# thread2.start()
# thread3.start()

#UDP
import pickle
import random
import socket
import sys
import threading
import time
from time import sleep

from opensimplex import OpenSimplex

clients = []
CHUNK = 2048
count = 0
users = 0
directions = [['up', 'up', 'down', 'down', 'left', 'left', 'right', 'right', 'idle'], ['up', 'down', 'left', 'right', 'idle', 'idle'], ['up', 'down', 'left', 'right', 'idle']]
states = ['walker', 'idler', 'average']
howManyBots = 0
bots = []
frames = 0
fps = 10
addresses = []
# class lobby(threading.Thread):
#     def __init__(self, clientAddress, clientsocket):
#         global count
#         global clients
#         threading.Thread.__init__(self)
#         self.num = count
#         count += 1
#         clients.append(clientsocket)
#         self.csocket = clientsocket
#         self.addr = clientAddress
#         print('Client at ' + str(self.addr) + ' queued...')
#     def run(self):
#         global count
#         global users
#         global clients
#         print('Client at ' + str(self.addr) + ' joined the game')
#         users += 1
#         print('{} users'.format(users))
#         while True:
#             try:
#                 # data = self.csocket.recv(CHUNK)
#                 data = self.csocket.recvfrom(CHUNK)
#             except:
#                 print('Client at ' + str(self.addr) + ' disconnected...')
#                 clients.remove(self.csocket)
#                 count -= 1
#                 users -= 1
#                 print('{} users'.format(users))
#                 break
#             finally:
#                 if pickle.loads(data)[0] == 'targethitbot':
#                     for b in bots:
#                         if bots.index(b) == pickle.loads(data)[1][0]:
#                             if pickle.loads(data)[1][1] <= 0:
#                                 bots.remove(b)
#                             else:
#                                 b.health = pickle.loads(data)[1][1]
#                             break
#                 for i in range(len(clients)):
#                     if not clients[i] == self.csocket:
#                         clients[i].send(data)
#             sleep(0.2)
                    
if len(sys.argv) > 1:
    IP = sys.argv[1]
    PORT = int(sys.argv[2])
else:
    IP = '192.168.1.159'
    PORT = 6969
# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# server.bind((IP, PORT))
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((IP, PORT))
print('Server started on ' + str(IP) + ':' + str(PORT))
print('Waiting for client request..')
class listen(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while True:
            try:
                data, addr = server.recvfrom(CHUNK)
                print(addr)
                for index, address in enumerate(addresses):
                        if address == addr:
                            bullets = [address for address in addresses if address != addr]
                            weg = True
                            break
                if not weg:
                    addresses.append(addr)
            except:
                pass
            finally:
                if pickle.loads(data)[0] == 'targethitbot':
                    for b in bots:
                        if bots.index(b) == pickle.loads(data)[1][0]:
                            if pickle.loads(data)[1][1] <= 0:
                                bots.remove(b)
                            else:
                                b.health = pickle.loads(data)[1][1]
                            break
                for address in addresses:
                    if address != addr:
                        server.sendto(pickle.dumps(data), address)
class Bot():
    global directions
    def __init__(self):
        self.x = ((random.randint(-98, 98)*10)/8)/10
        self.y = ((random.randint(-98, 98)*10)/8)/10
        self.char = '()'
        self.movenum = 0
        self.state = random.choice(states)
        self.frequency = random.randint(15, 20)
        self.seed = random.randint(0, 1000000)
        self.noise = OpenSimplex(seed=self.seed)
        self.health = 100
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
            if self.y - 1/8 <= 100/8:
                return
            self.y -= 1/8
        elif direction == 'down':
            for bot in bots:
                if bot.y == self.y+1/8 and bot.x == self.x:
                    return
            if self.y + 1/8 >= 100/8:
                return
            self.y += 1/8
        elif direction == 'left':
            for bot in bots:
                if bot.x == self.x-1/8 and bot.y == self.y:
                    return
            if self.x - 1/8 <= 100/8:
                return
            self.x -= 1/8
        elif direction == 'right':
            for bot in bots:
                if bot.x == self.x+1/8 and bot.y == self.y:
                    return
            if self.x + 1/8 >= 100/8:
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
            try:
                t = time.time()
                if frames%2 == 0:
                    for bot in bots:
                        bot.move()
                timeDif = time.time()-t
                if 1/fps-timeDif > 0:
                    time.sleep(1/fps-timeDif)
                frames += 1
            except:
                pass
# class BotSending(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#     def run(self):
#         global frames
#         global clients
#         while True:
#             try:
#                 t = time.time()
#                 if frames%2 == 0:
#                     for bot in bots:
#                         bot.move()
#                 datalist = ['botdata', []]
#                 for bot in bots:
#                     datalist[1].append([bots.index(bot), [bot.x, bot.y], bot.state, bot.health])
#                 for i in range(len(clients)):
#                     clients[i].send(pickle.dumps(datalist))
#                 timeDif = time.time()-t
#                 if 1/fps-timeDif > 0:
#                     time.sleep(1/fps-timeDif)
#                 frames += 1
#             except:
#                 pass
            
thread1 = listen()
thread2 = BotAdministration()
# thread3 = BotSending()
thread1.start()
thread2.start()
# thread3.start()
