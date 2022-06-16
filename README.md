# neopixelpie
2D Graphics Framework for RP2040 powered NeoPixel Matrix

A virtual framebuffer approach to managing sprites on a 2D grid consisting of a single NeoPixel strip:

An instance of the Matrix class contains a buffer property and a pixels property, both the same dimension. The pixels matrix represents the state of the neopixel strip and each element contains an RGB color tuple defaulting to blank. The pixels matrix should never be accessed directly, instead matrix.setPixel(x, y, Color) is used to write to the physical neopixel strip and update the internal state. The buffer property represents the placement of sprites in the 2D space, each element is either empty or contains a reference to a sprite object.

The sprite class consists of a bitmap property (a 2D array of True and None), and an X/Y origin which provides an offset to the coordinates of the bitmap. When applying the bitmap to the virtual buffer, the coordinates to be modified are determined by summing the origin with each X/Y coordinate of the bitmap. If the bitmap contains None, the buffer isn't modified. If the bitmap contains True, a reference to the sprite is written to that coordinate of the virtual buffer.

Anytime a sprite is moved or rotated, it first looks at the pixels it's moving INTO to check if it will be blocked by a boundary of another sprite. For this to be true, every pixel (in the buffer) about to be occupied by the updated sprite must contain either None or a reference to itself. If any other sprite appears in a pixel, the modification is ignored and that modify function returns false. If the modification is allowed, first the old pixels are set to None and then the new pixels are set to reference self.

Once sprites are in place and all modifications have been made, a matrix.show() method performs a diff between the buffer matrix and the pixels matrix, skipping any elements that don't require modification.

Both the virtual buffer and the state of the pixels can be 'queried' by the usual 2D array syntax, so matrix.buffer[0][0] and matrix.pixels[0][0] return the virtual and physical "state" of the pixel at coordinate 0,0. The type returns by buffer is None or Sprite (obj ref). The type returned by pixels is always a Color.
