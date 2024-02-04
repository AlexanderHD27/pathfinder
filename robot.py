modules = 8
print("Importing...")
import sys
sys.stdout.write("\r1/{}".format(modules))
import time
sys.stdout.write("\r2/{}".format(modules))
import socket
sys.stdout.write("\r3/{}".format(modules))
import json
sys.stdout.write("\r4/{}".format(modules))
import traceback
sys.stdout.write("\r5/{}".format(modules))
import ev3dev2.led # pylint: disable=import-error
sys.stdout.write("\r6/{}".format(modules))
import ev3dev2.motor # pylint: disable=import-error
sys.stdout.write("\r7/{}".format(modules))
import ev3dev2.sensor.lego # pylint: disable=import-error
sys.stdout.write("\r8/{}".format(modules))

unit = -700

leds = ev3dev2.led.Leds()
colorSensor = ev3dev2.sensor.lego.ColorSensor()
gyro = ev3dev2.sensor.lego.GyroSensor()
infra = ev3dev2.sensor.lego.InfraredSensor()

motors = ev3dev2.motor.MoveTank("A", "B")
motorD = ev3dev2.motor.Motor(address="D")

address = (sys.argv[1], 1337)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(address)

sign = lambda x: 1 if x > 0 else -1

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

def echo(data: dict):
    return data

def color(data: dict):
    return {"color" : colorSensor.rgb}

def move(data: dict):
    if "n" in data.keys():
        try:
            for i in range(int(data["n"])):
                motors.on_for_degrees(50, 50, unit, brake=True, block=True)
        except:
            motors.on_for_degrees(50, 50, unit, brake=True, block=True)
    else:
        motors.on_for_degrees(50, 50, unit, brake=True, block=True)

def turn_old(data: dict):
    if "n" in data.keys() and type(data["n"]) == int:
        n = data["n"]
    else:
        n = 0

    gyro.calibrate()

    if n > 0:
        motors.on(-40, 40)
    elif n < 0:
        motors.on(40, -40)
    else:
        return

    while True:
        v = gyro.value()
        print(v)

        if n < 0 and v <= n:
            break
        if n > 0 and v >= n:
            break

    motors.off()
    
    if gyro.value() != n:
        if n > 0:
            motors.on(5, -5)
        else:
            motors.on(-5, 5)
    
    if n > 0:
      cor = 2
    elif n < 0:
      cor = 1
    else:
      cor = 0

    while True:
        v = gyro.value()
        print((abs(n)+cor) * sign(n), v)    

        if v == (abs(n)+cor) * sign(n):
            break

    motors.off()
    
def turn(data: dict):
    if "n" in data.keys() and type(data["n"]) == int:
        n = data["n"]
    else:
        n = 0

    if gyro.value() == n:
        return

    motors.on(-40, 40)

    while True:
        v = gyro.value() % 360
        print(v)

        if n < 350 and v >= n:
            break
        elif n >= 350 and (v >= n or v < 10):
            break 

    motors.off()
    
    if gyro.value() != n:
        motors.on(5, -5)
    
    while True:
        v = gyro.value()

        if v == n:
            break

    motors.off()

def get_sensor(n=10):
  s = 0
  for i in range(n):
    s += infra.proximity
  return round(s/n)

def scan_old(data: dict):
    values = []

    motorD.on_for_degrees(50, -90, brake=True, block=True)
    time.sleep(0.25)
    values.append(get_sensor())
    for i in range(2): # pylint: disable=unused-variable
        motorD.on_for_degrees(50, 90, brake=True, block=True)
        time.sleep(0.25)
        values.append(get_sensor())
    
    motorD.on_for_degrees(50, -90, brake=True, block=True)

    return {"scan" : values}


def scan(data: dict):
    values = []

    turn({"n":-90})
    values.append(infra.proximity)
    for i in range(2): # pylint: disable=unused-variable
        turn({"n":90})
        values.append(infra.proximity)

    turn({"n":-90})
    return {"scan" : values}

def con(data: dict):
    if "msg" in data.keys():
        print(data.get("msg"))

def conIn(data: dict):
    if "msg" in data.keys():
        return {"input" : input(data.get("msg"))}
    else:
        return {"input" : input()}

def led(data: dict):
    if "color" in data.keys() and "group" in data.keys():
        if data["color"] not in ["BLACK", "RED", "GREEN", "AMBER", "ORANGE", "YELLOW"]:
            leds.all_off()

        if data["group"] != "LEFT" and data["group"] != "RIGHT":
            leds.set_color("LEFT", data["color"], pct=1)
            leds.set_color("RIGHT", data["color"], pct=1)
        else:
            leds.set_color(data["group"], data["color"], pct=1)

def reset():
    leds.all_off()
    motorD.stop()
    motors.stop()
    motors.gyro = gyro
    motors.gyro.calibrate()
    _ = colorSensor.rgb

def stop():
    leds.all_off()
    motorD.stop()

def noop(data: dict):
    print(data)

operations = {
    "exit" : exit_,
    "echo" : echo,
    "move" : move,
    "turn" : turn,
    "color": color,
    "scan" : scan,
    "scan_old" : scan_old,
    "con"  : con,
    "conIn": conIn,
    "led"  : led,
    "reset": noop,
    "status": noop
}

reset()

while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(address)
    try:
        while True:
            sock.settimeout(1)
            sock.listen()
            sys.stdout.write("\rListing...")

            try:
                conn, addr = sock.accept()
                conn.settimeout(None)
            except socket.timeout:
                continue

            print("\nGot connection from {} on {}".format(addr[0], addr[1]))
            gyro.calibrate()

            while True:
                data = json.loads(recvall().decode("utf-8"))

                if "op" in data.keys():
                    command = operations.get(data["op"])
    
                    if command != None:
                        try:
                            data = command(data)

                        except KeyboardInterrupt:
                            exit()

                        except:
                            data = None
                            traceback.print_exc()

                        if data == None:
                            conn.sendall(b"{}")
                        else:
                            send(data)

    except KeyboardInterrupt:
        reset()
        stop()
        print("Abord")
        exit()
    except:
        reset()
        stop()
        print("An Error had occured:")
        traceback.print_exc()
        print("Conntinue testing...")
        try:
            sock.close()
        except:
            pass
