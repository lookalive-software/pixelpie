# neopixelpie
# 2D Graphics Framework for RP2040 powered NeoPixel Matrix

from collections import namedtuple
import plasma
from machine import Timer

ColorRGB = namedtuple('ColorRGB', 'r g b')

# an out of bounds exception is thrown when proposed coordinates overflow the dimensions of self.matrix
# the exception should contain an xy tuple of how far and in what direction the overflow occurred

class OutOfBounds(Exception):
    pass

class SpriteCollision(Exception):
    pass

class Sprite(object):
    """
    bitmap is a two-dimensional tuple of True and None, defaulting to a single pixel of True.
    Sprite may be given a color index into the matrix palette.

    Sprites are created with a method of Matrix, called addSprite which passes a reference to the sprite to the matrix.
    By default, colorIndex is 1 to correspond with the default foreground color (white).

    When applying the bitmap to the virtual buffer,
    the coordinates to be modified are determined by summing the offset X/Y with each X/Y coordinate of the bitmap.
    If the bitmap contains None, the buffer isn't modified.
    If the bitmap contains True, a reference to the sprite is written to that coordinate of the virtual buffer.
    
    Anytime a sprite is translated or rotated, it first looks at the elements of the buffer it's going to replace
    to check if it will be blocked by a boundary or another sprite.
    For this to be true, every element of the buffer about to be occupied by the updated sprite must contain either None or a reference to itself.
    If any other sprite appears in a pixel, the modification is ignored and that modify function returns false.
    If the modification is allowed, first the old pixels are set to None and then the new pixels are set to reference self.

    """
    def __init__(self, matrix, bitmap=[[True]], origin=(0,0), colorIndex=1):
        
        self.matrix = matrix
        self.bitmap = bitmap
        self.colorIndex = colorIndex # monochrome only to start, later the bitmap will consist of references to color objects
        self.offsetX = origin[0]
        self.offsetY = origin[1]
        self.spin = 0

        self.show()
    
    def setOrigin(self, x, y):
        """
        Sets the origin of the sprite to the given x and y coordinates.
        """
        self.hide()
        self.offsetX = x
        self.offsetY = y
        self.show()

    def getShape(self):
        """
        Returns a tuple of the width and height of the bitmap, swapping x and y for odd values of self.spin
        """
        if self.spin % 2 == 0:
            return (len(self.bitmap[0]), len(self.bitmap))
        else:
            return (len(self.bitmap), len(self.bitmap[0]))

    def getBit(self, x, y):
        """
        Given an x and y coordinate, return the value of the bitmap at that coordinate corrected for spin.
        Spin is a number of quarterturns, between 0 and 3 inclusive.
        If spin is 0, x and y are accessed from the top left corner as usual.
        If spin is 1, access the matrix as if it were rotated 90 degrees clockwise, from an origin of the top right corner.
        If spin is 2, access the matrix as if it were rotated 180 degrees clockwise, from an origin of the bottom right corner.
        If spin is 3, access the matrix as if it were rotated 270 degrees clockwise, from an origin of the bottom left corner.
        """
        (width, height) = self.getShape()

        if self.spin == 0:
            return self.bitmap[y][x]
        elif self.spin == 1:
            return self.bitmap[width-x-1][y]
        elif self.spin == 2:
            return self.bitmap[height-y-1][width-x-1]
        elif self.spin == 3:
            return self.bitmap[x][height-y-1]

    def translate(self, tx, ty):
        """
        After hiding the current coordinates, the offsetX and offsetY are updated.
        Iterate through the buffer at the new coordinates, checking for collisions.
        As soon as a collision is found, exit the nested for loop and reset the offsetX and offsetY.
        """
        self.hide()
        self.offsetX += tx
        self.offsetY += ty
        
        (width, height) = self.getShape()

        for y in range(height):
            for x in range(width):
                if self.getBit(x, y):
                    # if x or y is out of bounds, reset the offsetX and offsetY and raise an OutOfBounds exception
                    if self.offsetX+x < 0 or self.offsetX+x >= self.matrix.width or self.offsetY+y < 0 or self.offsetY+y >= self.matrix.height:
                        # set h and v to -1, 0, or 1 to indicate if the overflow occured in the positive or negative direction
                        h = -1 if self.offsetX+x < 0 else 1 if self.offsetX+x >= self.matrix.width else 0
                        v = -1 if self.offsetY+y < 0 else 1 if self.offsetY+y >= self.matrix.height else 0
    
                        self.offsetX -= tx
                        self.offsetY -= ty
                        self.show()
                        raise OutOfBounds((h, v))

                    # if the buffer at the new coordinates contains a sprite, raise a SpriteCollision exception
                    if self.matrix.buffer[y+self.offsetY][x+self.offsetX] is not None:
                        self.offsetX -= tx
                        self.offsetY -= ty
                        self.show()
                        raise SpriteCollision(self.matrix.buffer[y+self.offsetY+ty][x+self.offsetX+tx])

        # if we haven't returned yet, no collision was found, so the new coordinates are accepted
        self.show()
        return True


    def rotate(self, quarterturns):
        """
        Updates the spin property mod 4,
        iterates through the bitmap with the new spin, checking for collisions
        if a collision if found, undo the update to self.spin and redraw the sprite
        if no collision is found, update the buffer with the new bitmap
        """
        self.hide()
        self.spin = (self.spin + quarterturns) % 4

        (width, height) = self.getShape()

        for y in range(height):
            for x in range(width):
                if self.getBit(x, y):
                    # if x or y is out of bounds, reset the spin and redraw the sprite
                    if self.offsetX+x < 0 or self.offsetX+x >= self.matrix.width or self.offsetY+y < 0 or self.offsetY+y >= self.matrix.height:
                        self.spin = (self.spin - quarterturns) % 4
                        self.show()
                        # set h and v to -1, 0, or 1 to indicate if the overflow occured in the positive or negative direction
                        h = -1 if self.offsetX+x < 0 else 1 if self.offsetX+x >= self.matrix.width else 0
                        v = -1 if self.offsetY+y < 0 else 1 if self.offsetY+y >= self.matrix.height else 0

                        raise OutOfBounds((h, v))

                    # if the buffer at the new coordinates contains a sprite, raise a SpriteCollision exception
                    if self.matrix.buffer[y+self.offsetY][x+self.offsetX] is not None:
                        self.spin = (self.spin - quarterturns) % 4
                        self.show()
                        raise SpriteCollision(self.matrix.buffer[y+self.offsetY][x+self.offsetX])

        self.show()
        return True

    def hide(self):
        """
        Goes through the non-empty pixels of the bitmap and sets them to None in the buffer.
        """
        (width, height) = self.getShape()
        
        for y in range(height):
            for x in range(width):
                if self.getBit(x, y) is not None:
                    self.matrix.buffer[y+self.offsetY][x+self.offsetX] = None


    def show(self):
        """
        Updates the buffer matrix with the current bitmap, offset by the current offsetX and offsetY.
        If the bitmap contains True, the buffer is updated with the reference to the sprite.
        """
        (width, height) = self.getShape()
        
        for y in range(height):
            for x in range(width):
                if self.getBit(x, y):
                    self.matrix.buffer[y+self.offsetY][x+self.offsetX] = self
                # I actually don't want to overwrite pixels that I don't occupy.
                # else:
                #     self.matrix.buffer[y+self.offsetY][x+self.offsetX] = None

        self.matrix.show()

class Matrix():
    """
    pixels and buffer are 2 dimensional arrays

    A virtual framebuffer approach to managing sprites on a 2D grid consisting of a single NeoPixel strip:
    An instance of the Matrix class contains a buffer property and a pixels property, both the same dimension.
    The pixels matrix represents the state of the neopixel strip and each element contains a reference to a ColorRGB namedtuple defaulting to blank.
    The pixels matrix should never be accessed directly, instead matrix.setPixel(x, y, Color) is used to write to the physical neopixel strip and update the internal state.
    The buffer property represents the placement of sprites in the 2D space, each element is either empty or contains a reference to a sprite object.

    Matrix contains a color palette, which is a list of ColorRGB objects, defaults to black and white.
    This way, any time I change the color palette (update foreground/background etc), I can call matrix.show() and all pixels will be updated with new palette.

    Matrix contains a method called addSprite which takes a reference to a Sprite object and adds it to the buffer.

    Matrix is initialized with width, height, and a zigzag option which defaults to false
    """
    def __init__(self, width, height, zigzag=True, palette=[ColorRGB(0,0,0), ColorRGB(255,255,255)]):
        self.width = width
        self.height = height
        self.zigzag = zigzag
        self.palette = palette

        # how do you spell "palette"?

        self.pixels = [[self.palette[0] for x in range(width)] for y in range(height)]
        self.buffer = [[None for x in range(width)] for y in range(height)]

        self.LED = plasma.WS2812(width * height, 0, 0, plasma.plasma2040.DAT)
        self.LED.start()
        # set the color of each pixel on the strip to background color
        for i in range(width * height):
            self.LED.set_rgb(i, self.palette[0].r, self.palette[0].g, self.palette[0].b)

    # create a clear method
    def clear(self):
        """
        Clears the buffer and the neopixel strip.
        """
        self.buffer = [[None for x in range(self.width)] for y in range(self.height)]
        # use setPixel to update both the pixels array and the neopixel strip
        for y in range(self.height):
            for x in range(self.width):
                self.setPixel(x, y, self.palette[0])

    def setBackground(self, color):
        self.palette[0] = color
        self.show()

    def setForeground(self, color):
        self.palette[1] = color
        self.show()

    def setPixel(self, x, y, color):
        """
        Takes an XY coordinate and converts it to the index of a pixel on the physical neopixel strip.
        If the zigzag option is true, then the x coordinate of odd rows is inverted.
        """
        if self.zigzag and y % 2 == 1:
            x = self.width - x - 1
        
        self.pixels[y][x] = color
        self.LED.set_rgb(x + y * self.width, color.r, color.g, color.b)

    def show(self):
        """
        Once sprites are in place and all modifications have been made, a matrix.show() method
        performs a diff between the buffer matrix and the pixels matrix, skipping any elements that don't require modification.
        To do so, it maps over the indexes of the grid, and compares the elements from the buffer and the pixels.

        If the buffer element is None, I make sure the pixel element is background color (matrix.palette[0]). If it already is, continue.
        If the buffer element is an Sprite reference, I check that that the pixel is matrix.palette[sprite.colorIndex]. Since the colors of the pixel matrix are references to the color objects in the palette, this is an identity operation, 'object is object'

        There's four casing for the diff:
        1. The buffer element is None, which means the pixel is blank.
            1a. The pixel is already blank, so no work needed
            1b. the pixel is not blank, so I set it to background color.
        2. The buffer element is an Sprite reference, which means the pixel should be the color of the sprite.
            2a. The pixel is already the color of the sprite, so no work needed
            2b. The pixel is not the color of the sprite, so I set it to the color of the sprite.

        I never directly modify the pixels array, I use the setPixel method.
        """
        for y in range(self.height):
            for x in range(self.width):
                maybeSprite = self.buffer[y][x]
                currentColor = self.pixels[y][x]
                # just rewrite the whole display for now
                if maybeSprite is None:
                    self.setPixel(x, y, self.palette[0])
                else:
                    self.setPixel(x, y, self.palette[maybeSprite.colorIndex])

                # if maybeSprite is None:
                #     if currentColor is not self.palette[0]:
                #         self.setPixel(x, y, self.palette[0])
                # else:
                #     nextColor = self.palette[maybeSprite.colorIndex]
                #     if currentColor is not nextColor:
                #         self.setPixel(x, y, nextColor)