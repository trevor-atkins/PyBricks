from pybricks.hubs import MoveHub
from pybricks.pupdevices import Motor, ColorDistanceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = MoveHub()

Motor(Port.A).run_time(1000, 5000)
Motor(Port.B).run_time(1000, 5000)

hub.light.blink(Color.GREEN, [1000,1000,1000])