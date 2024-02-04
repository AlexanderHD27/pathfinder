import traceback
import datetime
import socket
import json
import time
import sys

from toolkit.console import ui
import maze

# Get server address
if len(sys.argv) < 4:
    sys.stderr.write("Usage: <host> <port> <file>\n")
    sys.stderr.flush()
    exit()

address = sys.argv[1]
port = int(sys.argv[2])
file = sys.argv[3]


# Networking
maze.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sys.stdout.write("Connecting... ")
maze.sock.connect((address, port))
print("\rConneced to {} on {}".format(address, port))
print("Connection has a letency of {:.03f}s".format(maze.latency()))

# ---=: Main part :=---

start = tuple(reversed([int(input("Start X: ")), int(input("Start Y: "))]))
goal  = tuple(reversed([int(input("Stop  X: ")), int(input("Stop  Y: "))]))



nav = maze.Maze((3, 3), start)
nav.import_map(file)

if not nav.get(goal) and nav.get(goal) == 1:
    print(goal, "nicht erreichbar!")
    exit()

if not nav.get(start) and nav.get(start) == 1:
    print(start, "nicht erreichbar!")
    exit()
    
nav.goto(goal, display=True)
print(nav)

# exiting
print("Closing Connection...")
exit()