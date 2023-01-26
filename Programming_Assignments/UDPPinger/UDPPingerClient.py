import time
from socket import *

serverName = 'localhost'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)

lostPackages = 0
total = 0
min = None
max = None


for i in range(1, 11):
    message = f'Ping {i} {time.time()}'
    start = time.time()
    clientSocket.sendto(message.encode(), (serverName, serverPort))

    try:
        response, addr = clientSocket.recvfrom(2048)
    except TimeoutError:
        print("Request timeout")
        lostPackages += 1
        continue
    takenTime = time.time() - start
    if min is None or takenTime < min:
        min = takenTime
    if max is None or takenTime > max:
        max = takenTime
    total += takenTime

    print(f'RTT: packet {i} in {takenTime}')
print('\n')
print(f'Min time: {min}')
print(f'Max time: {max}')
print(f'Average time: {total/(10-lostPackages)}')
print(f'Packet loss rate: {lostPackages/10}')

clientSocket.close()
