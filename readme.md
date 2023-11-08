### Summary
A 2D game engine for low-res neopixel matrices for the RP2040. Tools to define Sprite as bitmaps, move them around the display while throwing exceptions colliding with another Sprite or hitting the edge of the play area.

### How It Works

The classes you'll be working with exist in the pixelpie/pixel.py file, they are: Matrix & Sprite, an RGB tuple called ColorRGB, and the exceptions SpriteCollision and OutOfBounds.

The Matrix represents the physical state of the neopixel matrix and the virtual state of the playfield as two separate lists-of-lists: self.pixels and self.buffer, respectively. self.pixels holds a ColorRGB value in each cell reflecting the last color to be written to the physical neopixel strip. Modifications to self.pixels should only ever be performed through matrix.setPixel, which updates both the list and the neopixel strip so that they are kept in sync. On the other hand, self.buffer is used by Sprites to update the state of the board - each cell is either None or a reference to a Sprite object - and check for collisions with other Sprites, only updating the pixels list once game logic has been completed and the display needs to be updated to the current game state, accomplished by calling matrix.show(). The matrix can also be reset with matrix.clear() which resets the buffer to be empty and sets the color of the pixels to the 0th RGBColor of self.palette.


To begin, you instantiate a Matrix with the width and height of your grid of neopixels. There is a zigzag arg that defaults to true, assuming that your grid of neopixels is constructed with the rope right to left, then left to right and so on, but if your grid has segments of neopixels all going the same direction you can pass zigzag=False. 

Subject to change: The constructor of the matrix class also has a "palette" argument that can override the default color palette, which is a list of "ColorRGB" (a named tuple defined in pixel.py) that defaults to black and white [ColorRGB(0,0,0),ColorRGB(255,255,255)]. The reason color is handled like this is so, when updating 

### Hardware
a Plasma2040, neopixel strands, and modified Nunchuk

### Examples
flash.py is a hello world just to test the board is connected

print_joystick.py is for testing the connectivity of a nunchuk, prints state to terminal or throws a "no device" error if there's nothing plugged in.

Sin & Disco demonstrate writing directly to the neopixel grids within an update function that is set on a periodic timer, and can use the current time as part of an expression to set the color for each cell.

Game of Life has a refresh rate which reads the state of its neighbors to update each cell

Rain can be written as an automata

Clock will be implemented with sprites and demonstrate joystick control of state with multiple timers

Pong, Tetris, Chess tbd
