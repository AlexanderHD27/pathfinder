import src
import networking.Core
import time
import json
import random
import socket

random.seed(12345)
# 0 /\
# 1 \/
# 2 ->
# 3 <-

def updateData(self):

    rate = 0.01
    moved = 0
    facing = 0

    while True:
        for i in range(256):
            if i % 16 == 0:
                moved = random.randint(0, 4)
            else:
                moved = -1

            if i % 8 == 0:
                facing = random.randint(0, 4)
            else:
                facing = -1

            

            text = json.dumps({
                "color": (i*2 % 255, 255-i, 255-i),
                "infra": i,
                "moved": moved,
                "facing": facing
                })
            self.sock.sendall(text.encode("ascii"))
            time.sleep(rate)

def updateCmd(self):
    time.sleep(0.1)
    self.sock.sendall(b"Hello from the other side!")
    self.sock.sendall(b"  ")
    time.sleep(0.1)
    self.sock.sendall(b"!EXIT!")
    pass


connData = networking.Core.ClientCon(src.address, src.dataPort, None, updateData)
connCmd = networking.Core.ClientCon(src.address, src.cmdPort, None, updateCmd)
connData.start()
connCmd.start()
