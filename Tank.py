from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor, Remote, Light
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = TechnicHub()

barrel_inc = Motor(Port.A)
barrel_inc.stop()
barrel_turn = Motor(Port.B)
barrel_turn.stop()

left_motor = Motor(Port.C)
left_motor.stop()
right_motor = Motor(Port.D)
right_motor.stop()
hub.light.blink(Color.GREEN, [500,500])
remote = None
while remote is None:
    try:
        remote = Remote(timeout=1000)
    except OSError:
        pass

class Constant:
    DRIVE_MAX_SPEED = 1024
    BARREL_MAX_SPEED = 640
    PARASITIC_BARREL_INCLINE = 1.5

class TrackMode:
    def __init__(self):
        self.color = Color.GREEN

    def step(self, pressed: Set[Button]):
        if Button.LEFT_MINUS in pressed:
            left_motor.run(Constant.DRIVE_MAX_SPEED)
        elif Button.LEFT_PLUS in pressed:
            left_motor.run(-Constant.DRIVE_MAX_SPEED)
        else:
            left_motor.brake()

        if Button.RIGHT_MINUS in pressed:
            right_motor.run(-Constant.DRIVE_MAX_SPEED)
        elif Button.RIGHT_PLUS in pressed:
            right_motor.run(Constant.DRIVE_MAX_SPEED)
        else:
            right_motor.brake()

class ClassicMode:
    def __init__(self):
        self.color = Color.MAGENTA

    def step(self, pressed: Set[Button]):
        if Button.LEFT_MINUS in pressed:
            left_motor.run(Constant.DRIVE_MAX_SPEED)
            right_motor.run(Constant.DRIVE_MAX_SPEED)
        elif Button.LEFT_PLUS in pressed:
            left_motor.run(-Constant.DRIVE_MAX_SPEED)
            right_motor.run(-Constant.DRIVE_MAX_SPEED)
        elif Button.RIGHT_MINUS in pressed:
            left_motor.run(Constant.DRIVE_MAX_SPEED)
            right_motor.run(-Constant.DRIVE_MAX_SPEED)
        elif Button.RIGHT_PLUS in pressed:
            left_motor.run(-Constant.DRIVE_MAX_SPEED)
            right_motor.run(Constant.DRIVE_MAX_SPEED)
        else:
            left_motor.brake()
            right_motor.brake()
        

class BarrelMode:
    def __init__(self):
        self.color = Color.YELLOW

    def step(self, pressed: Set[Button]):
        if Button.LEFT_MINUS in pressed:
            barrel_turn.run(-Constant.DRIVE_MAX_SPEED)
            barrel_inc.run(Constant.BARREL_MAX_SPEED*Constant.PARASITIC_BARREL_INCLINE)
        elif Button.LEFT_PLUS in pressed:
            barrel_turn.run(Constant.DRIVE_MAX_SPEED)
            barrel_inc.run(-Constant.BARREL_MAX_SPEED*Constant.PARASITIC_BARREL_INCLINE)
        elif Button.RIGHT_MINUS in pressed:
            barrel_inc.run(-Constant.BARREL_MAX_SPEED)
            barrel_turn.hold()
        elif Button.RIGHT_PLUS in pressed:
            barrel_inc.run(Constant.BARREL_MAX_SPEED)
            barrel_turn.hold()
        else:
            barrel_turn.brake()
            barrel_inc.brake()


modes = [ClassicMode(), BarrelMode()]
mode_idx = 0

color = modes[mode_idx].color
hub.light.on(color)
remote.light.on(color)

center_down = False

while True:
    pressed = remote.buttons.pressed()
    if center_down:
        if Button.CENTER not in pressed:
            center_down = False
            mode_idx = (mode_idx + 1)%len(modes)
            color = modes[mode_idx].color
            hub.light.on(color)
            remote.light.on(color)
        else:
            continue
    else:
        modes[mode_idx].step(pressed)

        if Button.CENTER in pressed:
            center_down = True

    #print("Battery voltage is", hub.battery.voltage())