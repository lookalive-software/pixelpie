# import the named tuple class from collections
from collections import namedtuple

# define the ColorRGB named tuple
ColorRGB = namedtuple('ColorRGB', ['r', 'g', 'b'])

class Palette:
    """
    A Palette class that maintains a dictionary of named colors.
    Each color is a named tuple (r, g, b).
    Allows adding and deleting colors that can be referenced by name.
    """

    def __init__(self):
        self.colors = {
            'BLACK': ColorRGB(0, 0, 0),
            'RED': ColorRGB(255, 0, 0),
            'GREEN': ColorRGB(0, 255, 0),
            'BLUE': ColorRGB(0, 0, 255),
            'MAGENTA': ColorRGB(255, 0, 255),
            'YELLOW': ColorRGB(255, 255, 0),
            'CYAN': ColorRGB(0, 255, 255),
            'WHITE': ColorRGB(255, 255, 255),
        }

# rest of your class implementation
        

    def add(self, name, color):
        """
        Adds a color to the palette.
        Arguments:
        - name: a string, the name of the color.
        - color: a ColorRGB named tuple defining the color.
        """
        self.colors[name] = color

    def delete(self, name):
        """
        Deletes a color from the palette.
        Arguments:
        - name: a string, the name of the color to delete.
        """
        if name in self.colors:
            del self.colors[name]
        else:
            print(f"Color {name} is not in the palette.")

    def __getattr__(self, name):
        """
        Overrides the default attribute access behavior to return colors by name.
        If the attribute name matches a color in the palette, returns that color.
        If the attribute name does not match a color or a class attribute, raises an AttributeError.
        """
        if name in self.colors:
            return self.colors[name]
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")