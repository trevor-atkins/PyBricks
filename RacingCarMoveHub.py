from pybricks.hubs import MoveHub
from pybricks.pupdevices import Motor, Remote, Light, ColorDistanceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch


hub = MoveHub()

steering = Motor(Port.C)

steering_left = steering.run_until_stalled(-500)
steering_right = steering.run_until_stalled(500)
steering_center = (steering_right+steering_left)//2

steering.track_target(steering_center)

drivingA = Motor(Port.A)
drivingB = Motor(Port.B)
drivingA.stop()
drivingB.stop()
lights = Light(Port.D)
lights.off()
brightness = 0
no_accel = 0
brightness_req = False
hub.light.blink(Color.GREEN, [500,500])
remote = None
print("Waiting for remote...")
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
        steering.track_target(steering_left)
    elif Button.LEFT_PLUS in pressed:
        steering.track_target(steering_right)
    elif abs(steering.angle()) > 1:
        steering.track_target(steering_center)

    if Button.RIGHT_PLUS in pressed:
        drivingA.run(Constant.DRIVE_MAX_SPEED)
        drivingB.run(-Constant.DRIVE_MAX_SPEED)
        no_accel = 0
    elif Button.RIGHT in pressed:
        drivingA.run(Constant.DRIVE_MAX_SPEED//3)
        drivingB.run(-Constant.DRIVE_MAX_SPEED//3)
        no_accel = 0
    elif Button.RIGHT_MINUS in pressed:
        drivingA.run(-Constant.DRIVE_MAX_SPEED//3)
        drivingB.run(Constant.DRIVE_MAX_SPEED//3)
        no_accel = 0
    else:
        if no_accel < Constant.BREAK_DELAY:
            no_accel +=1
        elif no_accel == Constant.BREAK_DELAY:
            drivingA.stop()
            drivingB.stop()
            pass

    if Button.LEFT in pressed:
        brightness_req = True
    elif brightness_req:
        brightness = (brightness + Constant.BRIGHTNESS_STEP) % (100 + Constant.BRIGHTNESS_STEP)
        print("New brightness is %d"%brightness)
        lights.on(brightness)
        brightness_req = False