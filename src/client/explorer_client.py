from PIL import Image
import datetime
import socket
import time
import sys

from toolkit.console import ui
import src.client.maze as maze

# Get server address
if len(sys.argv) < 3:
    sys.stderr.write("Usage: <host> <port>\n")
    sys.stderr.flush()
    exit()

address = sys.argv[1]
port = int(sys.argv[2])

filename = "maps/{}".format(str(datetime.datetime.now()).split(".")[0].replace(":", "-").replace(" ", "-"))
start = tuple(reversed([int(input("StartX: ")), int(input("StartY: "))]))

# Networking
maze.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sys.stdout.write("Connecting... ")
maze.sock.connect((address, port))
print("\rConneced to {} on {}".format(address, port))
print("Connection has a letency of {:.03f}s".format(maze.latency()))

# ---=: Main part :=---
nav = maze.Maze((4, 4), start)

if nav.pos[0] == 0:
    nav.turn("s")

print(nav)
nav.scan()

while not nav.isFinished():
    new = nav.unvisted.pop()
    print(nav.__str__())

    nav.goto(new)    
    nav.scan()

nav.export_map(filename)

print(nav.__str__())

# exiting
print("Closing Connection...")
exit()


