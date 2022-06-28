from neopixel import OutOfBounds, Sprite, SpriteCollision
from machine import Timer
import random
import json
from math import copysign, ceil

# load numbers from json file
numbers = json.load(open("numbers4x6.json"))
maxYmag = 10
minYmag = 2
magStep = 3
minXmag = 3


# should have an overflow value and a number of digits
class Number(Sprite):
    def __init__(self, matrix, origin, overflow = 10):
        super().__init__(matrix, numbers["0"], origin)
        self.value = 0
        self.overflow = overflow

    def setValue(self, value):
        self.value = value
        self.hide()
        self.bitmap = numbers[str(value)]
        self.show()

    def inc(self):
        self.setValue((self.value + 1) % self.overflow)

class Ball(Sprite):
    def __init__(self, matrix, bitmap, origin, colorIndex):
        super().__init__(matrix, bitmap, origin, colorIndex)

        # self.score = {
        #     "player": Number(matrix, (0,3)),
        #     "computer": Number(matrix, (8,3)),
        #     "dash": Sprite(matrix, [[True, True, True]], (5,6))
        # }

        # self.hideScore()
        self.vx = 0
        self.vy = 0
        self.xtimer = Timer()
        self.ytimer = Timer()
        self.setVelocity(random.choice([-minXmag,minXmag]), random.randint(-minYmag,minYmag))
    
    def hideScore():
        self.score["player"].hide()
        self.score["computer"].hide()
        self.score["dash"].hide()
        # will have to have a reference to the paddles and ball to hide them

    def showScore():
        self.matrix.clear()
        self.score["player"].show()
        self.score["computer"].show()
        self.score["dash"].show()
        
    # setting velocity x and y will set up a one-shot timer to move the missile
    # if velocity is 0, no timer is necessary, call deinit
    # a velocity of 1 is minimum, let's say 500 milliseconds
    # so a velocity of 500 would be to update in 1 millisecond
    def setVelocity(self, newX, newY):
        newX = ceil(newX)
        newY = ceil(newY)
        # if the old velocity was 0, we need to set up a timer
        print("newX: " + str(newX) + " newY: " + str(newY))

        if(self.vx != 0 and newX == 0):
            self.xtimer.deinit()
            print("deinit X timer")
        elif(self.vx == 0 and newX != 0):
            self.xtimer.init(period=abs(500//newX), mode=Timer.ONE_SHOT, callback=self.updateX)
            print("start X timer")

        if(self.vy != 0 and newY == 0):
            self.ytimer.deinit()
            print("deinit Y timer")
        elif(self.vy == 0 and newY != 0):
            self.ytimer.init(period=abs(500//newY), mode=Timer.ONE_SHOT, callback=self.updateY)
            print("start Y timer")
        
        self.vx = newX
        self.vy = newY

    def updateX(self, oldTimer):
        try:
            self.translate(1, 0) if self.vx > 0 else self.translate(-1, 0)

        except OutOfBounds as OOB:
            # if we reach out of bounds on an x update, someone wins a point
            # check if we are on the left or right side
            (xoverflow, yoverflow) = OOB.value
            if(xoverflow < 0):
                # we are on the left side, so the computer wins
                print("computer wins")
                # self.score["computer"].inc()
            else:
                # we are on the right side, so the player wins
                print("player wins")
                # self.score["player"].inc()
            
            # reset the ball
            self.setOrigin(6,6)
            # randomly choose a new velocity between -5 and 5 both directions
            self.setVelocity(random.choice([-minXmag,minXmag]), random.choice([-minYmag,minYmag]))
            
        except SpriteCollision as sprite:

            # calculate whether the ball collided dead center with a paddle or closer to the edge
            # subtract the paddle's x position from the ball's x position
            # there are 6 possible positions from -1 to 4, I want to know how close to the midpoint of 1.5
            hit = abs(self.offsetY - sprite.value.offsetY - 1.5)

            # in all cases I want to reverse the X directino of the ball, but I want to recalculate Y based on the distance
            # if the distance is less than 1, we collided dead center, zero out my Y velocity
            if(hit < 1):
                self.setVelocity(-self.vx, copysign(max(abs(self.vy) // magStep, minYmag), self.vy))
            # if the distance is less than 2, we collided closer to the edge, don't change Y velocity
            # if distance is greater than 2, then the ball collided just on the edge, let's double Y velocity
            else:
                self.setVelocity(-self.vx, copysign(min(abs(self.vy) * magStep, maxYmag), self.vy))

            # if we collide with a sprite while updating x, just bounce back
            self.updateX(oldTimer)
        finally:
            oldTimer.init(period=abs(500//self.vx), mode=Timer.ONE_SHOT, callback=self.updateX)


    def updateY(self, oldTimer):
        try:
            self.translate(0, 1) if self.vy > 0 else self.translate(0, -1)
        except OutOfBounds as OOB:
            # when moving in the y direction, we can only bounce off the top or bottom
            self.setVelocity(self.vx, -self.vy)
            self.updateY(oldTimer)
        except SpriteCollision:
            # if we collide with a sprite while updating y, ignore it, wait til next update
            pass
        except ZeroDivisionError:
            pass
        finally:
            if self.vy != 0:
                oldTimer.init(period=abs(500//self.vy), mode=Timer.ONE_SHOT, callback=self.updateY)