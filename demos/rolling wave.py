from machine import I2C, Pin, Timer
from pixelpie import Matrix, OutOfBounds, Sprite, SpriteCollision, ColorRGB
import time
from math import pi, sin

m = Matrix(11,11)

def delta(timerInstance):
    t = time.ticks_ms() / 5189
    #brightness = 150 * (sin(2 * pi * t) / 2 + 0.5)  # adjust the sin function output to range from 0 to 1
    #m.palette[0] = ColorRGB( int(brightness), int(brightness), int(brightness))
    #print(m.palette[0])
    #m.show()
        
    for y in range(11):
        for x in range(11):
            phase_shift = -y / 10.0  # This will shift the wave by 0.1 for each step in x
            brightness = 150 * (sin(2 * pi * (t - phase_shift)) / 2 + 0.5)
            color = ColorRGB( int(brightness), int(brightness), int(brightness))
            m.setPixel(x, y, color)




Timer().init(period=30, mode=Timer.PERIODIC, callback=delta)
