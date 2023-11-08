from machine import I2C, Pin, Timer
from pixelpie import Matrix, OutOfBounds, Sprite, SpriteCollision
import time, random
from math import pi, sin
from collections import namedtuple

ColorRGB = namedtuple('ColorRGB', 'r g b')


m = Matrix(11,11)
drop_start_times = [random.random() for _ in range(11)]  # Random start times for each column

def delta(timerInstance):
    t = time.ticks_ms() / 189

    for y in range(11):
        for x in range(11):
            phase_shift = -x / 10.0 + drop_start_times[y]  # This will shift the wave by 0.1 for each step in y
            brightness = 150 * (sin(2 * pi * (t - phase_shift)) / 2 + 0.5)
            r, g, b = [int(brightness) for _ in range(3)]  # Convert brightness to an RGB value
            m.setPixel(y, x, ColorRGB(r, g, b))

    if random.random() < 0.001:  # 1% chance each frame
        drop_start_times[random.randint(0, 10)] = t  # Start a new drop at the current time




Timer().init(period=30, mode=Timer.PERIODIC, callback=delta)

