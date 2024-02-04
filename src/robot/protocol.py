from robot_hw import PathfinderRobot

#
# Handler Functions for different commands
#

# distances to move for one unit of space (in deg)
# This was measured empirically 
UNIT_OF_SPACE = -700

def echo(data: dict, bot: PathfinderRobot):
    # Just for testing the connection and latency
    return data

def color(data: dict, bot: PathfinderRobot):
    #  Reading for the color sensor (not used)
    return {"color" : bot.colorSensor.rgb}

def move(data: dict, bot: PathfinderRobot):
    # Lets the Robot drive for n units of spaces
    # If no n present just move by one unit of space
    
    if "n" in data.keys():
        try:
            for i in range(int(data["n"])):
                bot.motors.on_for_degrees(50, 50, UNIT_OF_SPACE, brake=True, block=True)
        except:
            bot.motors.on_for_degrees(50, 50, UNIT_OF_SPACE, brake=True, block=True)
    else:
        bot.motors.on_for_degrees(50, 50, UNIT_OF_SPACE, brake=True, block=True)

def turn_old(data: dict, bot: PathfinderRobot):
    # Turns the Robot by n degree
    # First iteration of this function => DEPRECATED

    # If n is not present, the robot does not turn
    if "n" in data.keys() and type(data["n"]) == int:
        n = data["n"]
    else:
        n = 0
        
    bot.turn_by(n)
    
def turn(data: dict, bot: PathfinderRobot):
    # Turns the robot to n degree
    # the reference angle is the angle the robot had when turned on
    # No recalibration
    
    # If n is not present, then we don't turn
    if "n" in data.keys() and type(data["n"]) == int:
        n = data["n"]
    else:
        n = 0

    bot.turn_to(n)

def scan_old(data: dict, bot: PathfinderRobot):
    return {"scan" : bot.scan_old()}


def scan(data: dict, bot: PathfinderRobot):
    values = []

    turn({"n":-90})
    values.append(bot.infra.proximity)
    for i in range(2): # pylint: disable=unused-variable
        turn({"n":90})
        values.append(bot.infra.proximity)

    turn({"n":-90})
    return {"scan" : values}

def con(data: dict, bot: PathfinderRobot):
    # Print to robots stdout
    if "msg" in data.keys():
        print(data.get("msg"))

def conIn(data: dict, bot: PathfinderRobot):
    # Read from robots stdin
    if "msg" in data.keys():
        return {"input" : input(data.get("msg"))}
    else:
        return {"input" : input()}

def led(data: dict, bot: PathfinderRobot):
    # Sets the led color
    if "color" in data.keys() and "group" in data.keys():
        if data["color"] not in ["BLACK", "RED", "GREEN", "AMBER", "ORANGE", "YELLOW"]:
            bot.leds.all_off()

        if data["group"] != "LEFT" and data["group"] != "RIGHT":
            bot.leds.set_color("LEFT", data["color"], pct=1)
            bot.leds.set_color("RIGHT", data["color"], pct=1)
        else:
            bot.leds.set_color(data["group"], data["color"], pct=1)

def reset(data: dict, bot: PathfinderRobot):
    # Reset everything
    bot.leds.all_off()
    bot.motorD.stop()
    bot.motors.stop()
    bot.motors.gyro = bot.gyro
    bot.motors.gyro.calibrate()
    _ = bot.colorSensor.rgb

def stop(data: dict, bot: PathfinderRobot):
    # Shut everything off
    bot.leds.all_off()
    bot.motorD.stop()

def noop(data: dict):
    print(data)

operations = {
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