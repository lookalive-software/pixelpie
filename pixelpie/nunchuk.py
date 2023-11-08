import machine
import utime

class Nunchuk(object):
    """The Nunchuk object presents the sensor readings in a polling way.
    Based on the fact that the controller does communicate using I2C we
    cannot make it push sensor changes by using interrupts or similar
    facilities. Instead a polling mechanism is implemented, which updates
    the sensor readings based on "intent-driven" regular updates.

    If the "polling" way of updating the sensor readings is not sufficient
    a timer interrupt could be used to poll the controller. The
    corresponding update() method does not allocate memory and thereby
    could directly be used as an callback method for a timer interrupt."""

    def __init__(self, i2c):
        """Initialize the Nunchuk controller. If no polling is desired it
        can be disabled. Only one controller is possible on one I2C bus,
        because the address of the controller is fixed.
        The maximum stable I2C bus rate is 100kHz (200kHz seem to work on
        mine as well, 400kHz does not)."""
        self.i2c = i2c
        self.address = 0x52
        self.buffer = bytearray(b'\x00\x00\x00\x00\x00\x00')
 
        self.i2c.writeto(self.address, b'\xf0\x55')
        utime.sleep_ms(100)
        self.i2c.writeto(self.address, b'\xfb\x00')
        utime.sleep_ms(100)

    def __str__(self):
        self.update()
        C, Z = self.buttons()
        X, Y = self.joystick()

        return f'''
        Buttons: {("C" if C else "")} {("Z" if Z else "")}
        Joystick X: {X} Y: {Y}
        '''

    def update(self):
        """Requests a sensor readout from the controller and receives the
        six data bits afterwards."""
        try:
            self.i2c.writeto(self.address, b'\x00')
            utime.sleep_ms(5)
            self.i2c.readfrom_into(self.address, self.buffer)
        except:
            print("skipped update, EIO error")

    def accelerator(self):
        """Retrieve the three axis of the last accelerometer reading.
        Returns a tuple of three elements: The x, y and z axis"""
        return ((self.buffer[2] << 2) + ((self.buffer[5] << 4) >> 6),
            (self.buffer[3] << 2) + ((self.buffer[5] << 2 ) >> 6),
            (self.buffer[4] << 2) + (self.buffer[5] >> 6))

    def buttons(self):
        """Returns a tuple representing the states of the button C and Z
        (in this order). The values are True if the corresponding button
        is being pressed and False otherwise."""
        return (not (self.buffer[5] & 2 == 2), not (self.buffer[5] & 1 == 1))

    def joystick(self):
        """Get the X and Y positions of the thumb joystick. For both axis
        a value of 0 means left, ~136 center and 255 right position."""
        return (self.buffer[0], self.buffer[1])

    def joystick_left(self):
        """Returns True if the joystick is being held to the left side."""
        return self.buffer[0] < 55

    def joystick_right(self):
        """Returns True if the joystick is being held to the right side."""
        return self.buffer[0] > 200

    def joystick_up(self):
        """Returns True if the joystick is being held to the upper side."""
        return self.buffer[1] > 200

    def joystick_down(self):
        """Returns True if the joystick is being held to the lower side."""
        return self.buffer[1] < 55

    def joystick_center(self):
        """Returns True if the joystick is not moved away fromthe center
        position."""
        return self.buffer[0] > 100 and self.buffer[0] < 155 and self.buffer[1] > 100 and self.buffer[1] < 155

    def joystick_x(self):
        # Returns "normalized" x axis values
        return (self.buffer[0] >> 2) - 34

    def joystick_y(self):
        # Returns "normalized" x axis values
        return (self.buffer[1] >> 2) - 34