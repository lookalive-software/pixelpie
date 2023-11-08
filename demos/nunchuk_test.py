from pixelpie import Nunchuk
from machine import Timer, I2C, Pin

controller = Nunchuk(I2C(
    0,
    scl=Pin(21),
    sda=Pin(20),
    freq=100000
))

Timer().init(period=30, mode=Timer.PERIODIC, callback=lambda t: print(controller))
