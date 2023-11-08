import plasma
from pixelpie import ColorRGB, Palette

colors = Palette()

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
    def __init__(self, width, height, zigzag=True, palette=[colors.BLACK, colors.WHITE]):
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
    
    

    def setPixel(self, x, y, color):
        """
        Takes an XY coordinate and converts it to the index of a pixel on the physical neopixel strip.
        If the zigzag option is true, then the x coordinate of odd rows is inverted.
        """
        if self.zigzag and y % 2 == 1:
            x = self.width - x - 1
        
        self.pixels[y][x] = color
        self.LED.set_rgb(x + y * self.width, color.r, color.g, color.b)

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