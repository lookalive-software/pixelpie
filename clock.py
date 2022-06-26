from neopixel import Matrix, ColorRGB, Sprite
import machine
from collections import namedtuple
import json
import time

num = json.load(open("numbers4x6.json"))

# rtc = machine.RTC()
# # (year, month, day, weekday, hours, minutes, seconds, subseconds)
# rtc.datetime((2022, 6, 17, 4, 17, 32, 46, 0))

m = Matrix(13,13)
m.setForeground(ColorRGB(100,50,120))

four = m.addSprite(num["4"], (0, 0))

# topleft = m.addSprite(num["0"], (2,0))
# topright = m.addSprite(num["1"], (7,0))
# bottomleft = m.addSprite(num["2"], (2,7))
# bottomright = m.addSprite(num["3"], (7,7))

# every second, overwrite the bitmap of each sprite correpsonding with the hour and minute of the current time
# create a named tuple to represent the time returned by time.localtime()
# year includes the century (for example 2014).
# month is 1-12
# mday is 1-31
# hour is 0-23
# minute is 0-59
# second is 0-59
# weekday is 0-6 for Mon-Sun
# yearday is 1-366
# set time to current time


# Time = namedtuple("Time", "year month mday hour minute second weekday yearday")

# while True:
#     now = Time(*time.localtime())
#     # topleft.bitmap = num[str((now.hour or 12) // 10)]
#     topleft.bitmap = num[str(now.minute % 10)]
#     topleft.show()
#     # topright.bitmap = num[str((now.hour or 12) % 10)]
#     topright.bitmap = num[str(now.minute % 10)]
#     topright.show()
#     bottomleft.bitmap = num[str(now.second//10)]
#     bottomleft.show()
#     bottomright.bitmap = num[str(now.second%10)]
#     bottomright.show()
#     m.show()
#     time.sleep(1)