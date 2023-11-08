import time, random, json
from machine import I2C, Pin, Timer
from math import pi, sin
from pixelpie import Nunchuk, Matrix, ColorRGB, OutOfBounds, Sprite, SpriteCollision

# In this example, we're creating a list of rgb tuples to refer to
# and setting the color values of output directly via matrix.setPixel(x, y, Color)
# this operation updates the 

controller = Nunchuk(I2C(
    0,
    scl=Pin(21),
    sda=Pin(20),
    freq=100_000
))

colors = [ColorRGB(*each) for each in json.load(open("../bitmaps/colors.json"))]

m = Matrix(11,11)

def delta(timerInstance):
    thisColor = random.choice(colors)
    thisX = random.randint(0, 10)
    thisY = random.randint(0, 10)
    m.setPixel(thisX, thisY, thisColor)

Timer().init(period=250, mode=Timer.PERIODIC, callback=delta)
