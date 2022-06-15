# pixelpie
2D Graphics Framework for RP2040 powered NeoPixel Matrix

A virtual framebuffer approach to managing sprites on a 2D grid consisting of a single NeoPixel strip.

The only primative here is a "Sprite" class, which is specified as a 2D array of None and True (monochrome sprites only for now)

Sprites can have their position and color (and pixels) updated any number of times before writing these changes to the display.

Matrix has a Sprite constructor as a method so that the Sprite instance can have a reference to the matrix it belonds to. All modifications to the Sprite are passed onto the virtual buffer, and can then be applied to the output device by calling matrix.show() 

Both the virtual buffer and the physical buffer can be 'queried' by the usual 2D array syntax, so matrix.virtual[0][0] and matrix.physical[0][0] return the virtual and physical "state" of the pixel at coordinate 0,0. 

The virtual and physical buffers start out as grids of empty pixels. 

When a sprite is added to the matrix, the pixels it occupies are set to object references back to the sprite. In this way, the program may check "what sprite occupies this space", enabling collision detection or various behavoir when overlapping.

TODO: instead of an object reference to a single sprite in each pixel, each pixel can be a Set of sprites occupying that space, allowing for overlap, transparency, color mixing etc.  

```
from NeoPixelPie import Matrix

matrix = Matrix(13, 13, zigzag=True) # optionally specify bg-color and fg-color, defaults to blank and white.

square = matrix.Sprite(pixels, origin=(x,y), color=(255, 0, 0))



matrix.show() # compares physical buffer (representing the old state) with virtual buffer (representing the new state)
