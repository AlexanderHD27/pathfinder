import sys
import socket
import json
import time

#
# This is a test client to send commands manual to the EV3
# (just for testing)
#

def recvall(sock, BUFF_SIZE = 2048):
        data = b""
        while True:
            part = sock.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                break
        return data   

def recv():
    return json.loads(recvall(sock).decode("utf-8"))

def send(data):
    sock.sendall(json.dumps(data).encode("utf-8"))
    return json.loads(recvall(sock).decode("utf-8"))

def sendop(op, data={}):
    data_ = {"op": op}
    data_.update(data)
    return send(data_)

operations = [
    "exit",
    "print",
    "input",
    "led",
    "color",
    "scan",
    "move",
    "turn"
]

if len(sys.argv) < 3:
    sys.stderr.write("Usage: <host> <port>\n")
    sys.stderr.flush()
    exit()

address = sys.argv[1]
port = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connecting
sys.stdout.write("Connecting... ")
sock.connect((address, port))
print("\rConneced to {} on {}".format(address, port))

# latency
start = time.time()
sendop("echo")
print("The Connection as a letency of {:.3f}".format(time.time()-start))

while True:
    cmd = input("$ ")
    if "list" in cmd or "help" in cmd:
        print("List of commands:")


        if len(cmd.split(" ")) > 1:
            if cmd.split(" ")[1] == "leds":
                print(" Colors: BLACK, RED, GREEN, AMBER, ORANGE, YELLOW")
                print(" Leds  : LEFT, RIGHT, ALL")

        else:
            for i in operations:
                print("", i)

    if cmd == "exit":
        send({"op":"exit"})
        break

    elif cmd == "print":
        text = input("msg> ")
        sendop("con", {"msg" : text})

    elif cmd == "input":
        text = input("msg> ")
        print(sendop("conIn", {"msg" : text})["input"])

    elif cmd == "led":

        color = input("color> ")
        if color not in ["BLACK", "RED", "GREEN", "AMBER", "ORANGE", "YELLOW"]:
            color = "BLACK"

        group = input("group> ")
        sendop("led", {"color":color, "group":group})
    
    elif cmd == "color":
        print(sendop("color")["color"])

    elif cmd == "scan":
        print(sendop("scan")["scan"])

    elif cmd == "scan_old":
        print(sendop("scan_old"))

    elif cmd == "move":
        n = input("n> ")
        try:
            sendop("move", {"n":int(n)})
        except:
            sendop("move", {"n":1})

    elif cmd == "turn":
        n = input("n> ")
        try:
            sendop("turn", {"n":int(n)})
        except:
            sendop("turn", {"n":1})
    

print("Stoped Program!")