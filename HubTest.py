from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor, ColorDistanceSensor, Light
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = TechnicHub()
hub.light.on(Color.GREEN)

motor = Motor(Port.A)

light = Light(Port.C)
light.off()

sensor = ColorDistanceSensor(Port.B)
while True:
    d = sensor.distance()
    print(d)
    #print(sensor.color())
    if d > 50:
        light.on(d/2)
        motor.run(d*10)
    else:
        light.off()
        motor.stop()
    wait(500)
    #hub.light.on(sensor.hsv())
