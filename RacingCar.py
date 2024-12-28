from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor, Remote, Light
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = TechnicHub()

steering = Motor(Port.A)
steering.reset_angle(0)
driving = Motor(Port.B)
driving.stop()
lights = Light(Port.C)
lights.off()
brightness = 0
no_accel = 0
brightness_req = False
hub.light.blink(Color.GREEN, [500,500])
remote = None
while remote is None:
    try:
        remote = Remote(timeout=1000)
    except OSError:
        pass
hub.light.on(Color.GREEN)
remote.light.on(Color.GREEN)

class Constant:
    BRIGHTNESS_STEP = 25
    BREAK_DELAY = 3
    DRIVE_MAX_SPEED = -1024

while True:
    pressed = remote.buttons.pressed()
    if Button.LEFT_MINUS in pressed:
        steering.track_target(90)
    elif Button.LEFT_PLUS in pressed:
        steering.track_target(-90)
    elif abs(steering.angle()) > 1:
        steering.track_target(0)

    if Button.RIGHT_PLUS in pressed:
        driving.run(Constant.DRIVE_MAX_SPEED)
        no_accel = 0
    elif Button.RIGHT in pressed:
        driving.run(Constant.DRIVE_MAX_SPEED/3)
        no_accel = 0
    elif Button.RIGHT_MINUS in pressed:
        driving.run(-Constant.DRIVE_MAX_SPEED/3)
        no_accel = 0
    else:
        if no_accel < Constant.BREAK_DELAY:
            no_accel +=1
        elif no_accel == Constant.BREAK_DELAY:
            driving.brake()

    if Button.LEFT in pressed:
        brightness_req = True
    elif brightness_req:
        brightness = (brightness + Constant.BRIGHTNESS_STEP) % (100 + Constant.BRIGHTNESS_STEP)
        print("New brightness is %d"%brightness)
        lights.on(brightness)
        brightness_req = False