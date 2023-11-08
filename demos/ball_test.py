from machine import I2C, Pin, Timer
from pixelpie import Matrix, ColorRGB, OutOfBounds, Sprite, SpriteCollision, Nunchuk
import time
from math import pi, sin

joystick = Nunchuk(I2C(
    0,
    scl=Pin(21),
    sda=Pin(20),
    freq=100_000
))

ballbitmap = [[True, True],[True,True]]

m = Matrix(11,11)

ball = Sprite(m, ballbitmap, (5,5))

def delta(timerInstance):
    #t = time.ticks_ms() / 1789
    joystick.update()
    # brightness = 120 * (sin(2 * pi * t) / 2 + 0.5)  # adjust the sin function output to range from 0 to 1
    if joystick.joystick_up():
        ball.translate(1,0)
    elif joystick.joystick_down():
        ball.translate(-1,0)
    elif joystick.joystick_left():
        ball.translate(0,1)
    elif joystick.joystick_right():
        ball.translate(0,-1)


Timer().init(period=100, mode=Timer.PERIODIC, callback=delta)
