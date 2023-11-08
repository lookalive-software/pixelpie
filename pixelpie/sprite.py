# neopixelpie
# 2D Graphics Framework for RP2040 powered NeoPixel Matrix

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

    def __str__(self):
        w,h = self.getShape()
        print('''
        color:{self.matrix.palette[self.colorIndex]},
        origin:{self.offsetX},{self.offsetY},
        shape:{w},{h},
        spin: {self.spin}
        ''')
    
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

    def getBit(self, x, y, width, height):
        """
        Given an x and y coordinate, return the value of the bitmap at that coordinate corrected for spin.
        Spin is a number of quarterturns, between 0 and 3 inclusive.
        If spin is 0, x and y are accessed from the top left corner as usual.
        If spin is 1, access the matrix as if it were rotated 90 degrees clockwise, from an origin of the top right corner.
        If spin is 2, access the matrix as if it were rotated 180 degrees clockwise, from an origin of the bottom right corner.
        If spin is 3, access the matrix as if it were rotated 270 degrees clockwise, from an origin of the bottom left corner.
        """

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
                if self.getBit(x, y, width, height):
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
                if self.getBit(x, y, width, height):
                    # if x or y is out of jbounds, reset the spin and redraw the sprite
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
                if self.getBit(x, y, width, height) is not None:
                    self.matrix.buffer[y+self.offsetY][x+self.offsetX] = None


    def show(self):
        """
        Updates the buffer matrix with the current bitmap, offset by the current offsetX and offsetY.
        If the bitmap contains True, the buffer is updated with the reference to the sprite.
        """
        (width, height) = self.getShape()
        
        for y in range(height):
            for x in range(width):
                if self.getBit(x, y, width, height):
                    self.matrix.buffer[y+self.offsetY][x+self.offsetX] = self
                # I actually don't want to overwrite pixels that I don't occupy.
                # else:
                #     self.matrix.buffer[y+self.offsetY][x+self.offsetX] = None

        self.matrix.show()