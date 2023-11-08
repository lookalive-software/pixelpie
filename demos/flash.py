from machine import Pin
from plasma import plasma2040
from pimoroni import RGBLED
import time

led = RGBLED(plasma2040.LED_R, plasma2040.LED_G, plasma2040.LED_B)


while True:
    led.set_rgb(100,100,100)
    time.sleep_ms(1000)
    led.set_rgb(100,0,0)
    time.sleep_ms(1000)
