print("Importing... ", end="", flush=True)
import sys
import socket
import json
import traceback
from robot_hw import PathfinderRobot
from protocol import operations, reset, stop
print("Done!")
# Importing takes ages, because EV3 are potatoes processor wise

#
# This could should be run on the EV3, not a normal computer
#

# Init hardware
robot = PathfinderRobot()

# Setting up TCP Server
address = (sys.argv[1], 1337)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(address)

# Helper functions to deal with network
def send(data):
    conn.sendall(json.dumps(data).encode("utf-8"))
def recvall(BUFF_SIZE = 2048):
        data = b""
        while True:
            part = conn.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                break
        return data   

def exit_(data: dict):
    conn.sendall(b"{}")
    sock.close()
    print("Exiting Programm...")
    raise KeyboardInterrupt

operations.update({
    "exit" : exit_,
})

reset()

# Bit loop, if something crashes (because restarting takes ages)
while True:
    # Create listing socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(address)
    
    try:
        while True:
            # Waiting and accepting connection (only one at a time)
            sock.settimeout(1)
            sock.listen()
            sys.stdout.write("\rListing...")

            try:
                conn, addr = sock.accept()
                conn.settimeout(None)
            except socket.timeout:
                continue

            print("\nGot connection from {} on {}".format(addr[0], addr[1]))
            
            # Setting the current rotation to 0°
            robot.gyro.calibrate()

            # Main Command loop
            while True:
                data = json.loads(recvall().decode("utf-8"))

                if "op" in data.keys():
                    command = operations.get(data["op"])
    
                    if command != None:
                        try:
                            data = command(data, robot)

                        except KeyboardInterrupt:
                            exit()

                        except:
                            data = None
                            traceback.print_exc()

                        if data == None:
                            conn.sendall(b"{}")
                        else:
                            send(data)

    # On CTRL+C we exit
    except KeyboardInterrupt:
        reset()
        stop()
        print("Abord")
        exit()
    
    # If any other exception occurred, we reset and try again
    except:
        reset()
        stop()
        print("An Error had occurred:")
        traceback.print_exc()
        print("Continue testing...")
        try:
            sock.close()
        except:
            pass
