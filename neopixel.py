# create ColorHSV and ColorRGB as named tuples from col
from collections import namedtuple
ColorRGB = namedtuple("ColorRGB", ("r","g","b"))
ColorHSV = namedtuple("ColorHSV", ("h","s","v"))
Position = namedtuple("Position", ("x","y"))

black = ColorHSV(0,0,0)
white = ColorHSV(0,0,1)
    
class Sprite:
    def __init__(bitmap, origin = (0,0), color = None)
        self.bitmap = bitmap
        self.color = color
        self.x = origin[0]
        self.y = origin[1]
        
    def setOrigin(x, y):
        self.x = x
        self.y = y
        
    def translate(x, y):
        self.x += x
        self.y += y
    
    def getPixels():
        

class Matrix:
    def __init__(width, height, zigzag = False, backgroud = black, foreground = white):
        self.width = width
        self.height = height
        self.zigzag = zigzag
        
        self.background = background
        self.foreground = foreground
        
        self.virtual = [[None] * width] * height
        self.physical = [[None] * width] * height
    
    def getVirtualPixel(x, y):
        return self.virtual[x][y]
    
    def getPhysicalPixel(x, y):
        return self.physical[x][y]
    
    def setVirtualPixel(x, y, ref):
        self.virtual[x][y] = ref
        
    def setPhysicalPixel(x, y, color):
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
            self.LED.set_hsv(i, *HSVcolor)
        elif isinstance(color, RGBcolor):
            self.LED.set_rgb(i, *RGBcolor)

    def show():
        # get a list of coordinates that need to be modified, plus the new value
        # if the new value is None, set coordinate
        # this will be a (x, y, color) tuple
        # last step is to convert x & y into an index for the strip, 
        
        # if pixel is a Sprite, lookup pixel.color, fallback to self.foreground
    
    # any modifications and state queries go off the virtual buffer
    def isPixelEmpty(x, y):
        return self.virtual[x][y] == None

        