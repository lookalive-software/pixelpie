# create ColorHSV and ColorRGB as named tuples from col
from collections import namedtuple
ColorRGB = namedtuple("ColorRGB", ("r","g","b"))
ColorHSV = namedtuple("ColorHSV", ("h","s","v"))
# Position = namedtuple("Position", ("x","y"))
# thought about making a class for X Y coordinates, but I'm going to be mutating them so much it might be leaner to just treat them as numbers
# speaking of lean, I'll be creating and destroying a lot of arrays, on the order of 500 bytes. Only 260kb RAM.
# Hm, first thing, Sprites are 2D arrays of object references, so maybe 4 bytes per pixel, so a 5x5 sprite will be 100 bytes RAM
# if the garbage collector can't keep up, I might make the CPU trade-off to have a "scratch" buffer for rearranging arrays without re-allocating

black = ColorHSV(0,0,0)
white = ColorHSV(0,0,1)
    
class Sprite:
    def __init__(self, matrix, bitmap, origin = (0,0), color = None)
        self.matrix = matrix
        self.bitmap = bitmap
        self.color = color
        self.x = origin[0]
        self.y = origin[1]
        
    def hide(self):
        for (x,y) in self.getPixels():
            self.matrix.setVirtualPixel(x, y, None)
            
    def show(self):
        for (x, y) in self.getPixels():
            self.matrix.setVirtualPixel(x, y, self)
        
        
    def setOrigin(self, x, y):
        self.hide()
        self.x = x
        self.y = y
        self.show()            
        
    def translate(self, x, y):
        self.hide()
        self.x += x
        self.y += y
        self.show()
        
    def rotate():
        pass

    def vmirror():
        # 
        pass
    
    def hmirror():
        pass
    
    # maybe better to pass a function here, applying a new state to each pixel of the virtualbuffer
    # avoiding the creation of a new array of coordinates
    # if pixel is None, continue, else apply new state to target pixel
    def getPixels():
        xs = range(len(self.bitmap[0])) # length of inner array, x dimension
        ys = range(len(self.bitmap))    # length of outer array, y dimension
        
        # tricky, I can get a list of 'x y' coordinates this way
        # but to access the value of bitmap[x][y], I actually need to select the y dimension, then the x dimension: self.bitmap[y][x]
        # this gives me X,Y tuples correc
        for row, y in enumerate(self.bitmap):
            for pixel, x in enumerate(row):
                if pixel is not None:
                    self.matrix.writePixel(self.x + x, self.y + y, newColor)
                
        
        return [(x+self.x, y+self.y) for x in xs for y in ys if self.bitmap[y][x] is not None]
    
        # either way works, [for x in xs for y in ys] is column oriented, [for y in ys for x in xs] is row oriented
        # for row in column for column in matrix
        # for pixel in row for row in matrix
        

class Matrix:
    """
    TODO: add row oriented / column oriented option
    """
    def __init__(self, width, height, zigzag = False, backgroud = black, foreground = white):
        self.width = width
        self.height = height
        self.zigzag = zigzag
        
        self.background = background
        self.foreground = foreground
        
        self.virtual = [[None] * width] * height
        self.physical = [[None] * width] * height
    
    def getVirtualPixel(self, x, y):
        return self.virtual[x][y]
    
    def getPhysicalPixel(self, x, y):
        return self.physical[x][y]
    
    def setVirtualPixel(self, x, y, ref):
        self.virtual[x][y] = ref
        
    def setPhysicalPixel(self, x, y, color):
        # color can be None, pixel will be overwritten with self.background_color
        x = x % self.W
        y = y % self.H
        
        # mirror x on odd rows if zigzag
        # if isOdd(y) and self.ZIGZAG:
        if self.ZIGZAG and not y % 2 == 0:
            x = self.W - 1 - x
            
        # now get the index of the addressed pixel by multiplying Y by row-length and adding X dimension
        i = y * self.W + x
        
        if isinstance(color, HSVcolor):
            # wonder what the cpu/mem difference is for unpacking a positional *args and calling the props directly
            self.LED.set_hsv(i, *HSVcolor)
          # self.LED.set_hsv(i, HSVcolor.h, HSVcolor.s, HSVcolor.v)
        elif isinstance(color, RGBcolor):
            self.LED.set_rgb(i, *RGBcolor)
          # self.LED.set_hsv(i, RGBcolor.r, RGBcolor.g, RGBcolor.b)


    def show(self):
        # get a list of coordinates that need to be modified, plus the new value
        # if the new value is None, set coordinate
        # this will be a (x, y, color) tuple
        # last step is to convert x & y into an index for the strip, 
        
        # if pixel is a Sprite, lookup pixel.color, fallback to self.foreground
    
    # any modifications and state queries go off the virtual buffer
    def isPixelEmpty(self, x, y):
        return self.virtual[x][y] == None

        