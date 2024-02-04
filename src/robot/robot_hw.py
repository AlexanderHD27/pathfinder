import time

import ev3dev2.sensor.lego # pylint: disable=import-error
import ev3dev2.motor # pylint: disable=import-error
import ev3dev2.led # pylint: disable=import-error

# Util function, because python has no sign()
sign = lambda x: 1 if x > 0 else -1

class PathfinderRobot:
    
    def __init__(self) -> None:
        # Init Motor, Sensors, etc
        self.leds = ev3dev2.led.Leds()
        self.colorSensor = ev3dev2.sensor.lego.ColorSensor()
        self.gyro = ev3dev2.sensor.lego.GyroSensor()
        self.infra = ev3dev2.sensor.lego.InfraredSensor()

        self.motors = ev3dev2.motor.MoveTank("A", "B")
        self.motorD = ev3dev2.motor.Motor(address="D")
        
    def get_sensor(self, n=10) -> int:
        # Helper method to read form the infra read sensor and calc average result (because the sensor, sometime sees wired things)
        s = 0
        for i in range(n):
            s += self.infra.proximity
        return round(s/n)
    
    def turn_by(self, deg: int):
        # Turns the robot by deg, relative to current position
        
        # Sets the robots current rotation ot 0
        self.gyro.calibrate()

        # Start the motors and turn...
        if deg > 0:
            self.motors.on(-40, 40)
        elif deg < 0:
            self.motors.on(40, -40)
        else:
            return

        # ... and wait until we hit your goal...
        while True:
            v = self.gyro.value()
            print(v)

            if deg < 0 and v <= deg:
                break
            if deg > 0 and v >= deg:
                break

        # And we switch of the motors!
        self.motors.off()

        # The Robot probably overshot so we need to readjust slowly!
        if self.gyro.value() != deg:
            if deg > 0:
                self.motors.on(5, -5)
            else:
                self.motors.on(-5, 5)

        if deg > 0:
            cor = 2
        elif deg < 0:
            cor = 1
        else:
            cor = 0

        while True:
            v = self.gyro.value()
            print((abs(deg)+cor) * sign(deg), v)    

            if v == (abs(deg)+cor) * sign(deg):
                break

        self.motors.off()
        
    def turn_to(self, deg: int):
        # Turns the robot to deg, absolute to starting calibration
            # If we are already at the correct position, the robot does not need to turn
        if self.gyro.value() == deg:
            return
        
        # Start the motors and...
        self.motors.on(-40, 40)

        # ... turn until we hit our goal and...
        while True:
            v = self.gyro.value() % 360 # The gyro sensor does not stop at 360 but keeps going, so we need to mod 360
            print(v)

            if deg < 350 and v >= deg:
                break
            elif deg >= 350 and (v >= deg or v < 10):
                break 

        # ...switch of the motors
        self.motors.off()
        
        # we probably over shot, so we need to readjust again!
        if self.gyro.value() != deg:
            self.motors.on(5, -5)
        
        while True:
            v = self.gyro.value()

            if v == deg:
                break

        self.motors.off()
        
    def scan_old(self) -> list[int]:
        # Checks left, front, right for presents of a wall
        # DEFECATED
        values = []

        self.motorD.on_for_degrees(50, -90, brake=True, block=True)
        time.sleep(0.25)
        values.append(self.get_sensor())
        for i in range(2): # pylint: disable=unused-variable
            self.motorD.on_for_degrees(50, 90, brake=True, block=True)
            time.sleep(0.25)
            values.append(self.get_sensor())
        
        self.motorD.on_for_degrees(50, -90, brake=True, block=True)
        
        return values
