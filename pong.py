from neopixel import Matrix, ColorRGB, OutOfBounds, Sprite, SpriteCollision
from ball import Ball
from machine import Timer, I2C, Pin
import machine
import json
import nunchuk
import random

board = Matrix(13, 13)

# ballbitmap = json.load(open("ball.json"))
ballbitmap = [[True, True],[True,True]]
# ballbitmap = [[True]]
paddlebitmap = [[True],[True],[True],[True]]

controller = nunchuk.Nunchuk(I2C(
    0,
    scl=Pin(21),
    sda=Pin(20),
    freq=100000
))

player = Sprite(board, paddlebitmap, (0,6))
computer = Sprite(board, paddlebitmap, (12,6))
ball = Ball(board, ballbitmap, (6,6), (random.choice([-6,6]),random.randint(-5,5)), 1)

# given a samplerate and an acceleration value,
# set a timer to check the state of the nunchuk
sampleRate = 50 # every 50 milliseconds...
threshold = 5


def refresh(t):
    # gets called every 50 milliseconds
    # calls update on the nunchuk and then reads the vertical position of the joystick
    controller.update()
    mag = controller.joystick_y()
    # if magnitude is greater than 5, move the paddle up
    # if magnitude is less than -5, move the paddle down
    # otherwise do nothing
    if(mag > threshold):
        player.translate(0,-1)
    elif(mag < -threshold):
        player.translate(0,1)

    # AI will track the ball one pixel at a time, only when the ball is moving towards the computer
    if(ball.vx > 0):
        if(ball.offsetY <= computer.offsetY):
            computer.translate(0,-1)
        elif(ball.offsetY >= (computer.offsetY + 4)):
            computer.translate(0,1)

    # both the player and computer get a velocity property which is the last 5 choices, True for moved, False for not moved
    # this paddle velocity is added to the y velocity of the ball



Timer().init(period=sampleRate, mode=Timer.PERIODIC, callback=refresh)

# a missile is a subclass of Sprite, with an added x and y velocity
# when initialized, using the velocity, it will set up a one-shot timer to move the missile



