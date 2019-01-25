from micropython import const
from machine import Pin

_CAP1296_I2C_ADDRESS = const(0x28)

_MAIN_CONTROL = const(0x00)
_SENSOR_INPUT_STATUS = const(0x03)
_SENSOR_INPUT_ENABLE = const(0x21)
_INTERRUPT_ENABLE = const(0x27)
_MULTIPLE_TOUCH_CONFIG = const(0x2A)


def _keys_to_byte(keys, default=b'\x00'):
    """Return a byte in which the bits X are 1 for each X in the list keys."""
    return bytes([sum(map(lambda b: 1 << b, keys))]) if keys else default


def _byte_to_keys(keys_as_byte, num_keys=6):
    """Return a list of key (bit) numbers for each 1 in keys_as_byte."""
    keys_as_int = int.from_bytes(keys_as_byte, 'little')
    return [
        key
        for key in range(num_keys)
        if keys_as_int & (1 << key)
    ]


class CAP1296:
    """
    A driver for accessing the CAP1296 capacitive touch IC on the badge
    """

    def __init__(self, i2c, alert_pin, intr):
        self.i2c = i2c
        self.alert = alert_pin
        self.intr = intr
        self._addr = _CAP1296_I2C_ADDRESS

        self.write = lambda r, b: self.i2c.writeto_mem(self._addr, r, b)
        self.read = lambda r, n: self.i2c.readfrom_mem(self._addr, r, n)
        self.alert.irq(handler=self._handle_interrupt, trigger=Pin.IRQ_FALLING)

    def _handle_interrupt(self):
        self.intr(self.read_keys(True))

    def enable_interrupt(self, keys):
        """
        Enables interrupts for the specified keys. Enabling interrupts results in the touch event being passed to the
        ``handle_event`` function of the current app
        
        :param keys: A list of key numbers in the range 0-5
        """
        self.write(_INTERRUPT_ENABLE, _keys_to_byte(keys, default=b'\x3f'))

    def enable_multitouch(self, enable, simultaneous_touches=1):
        """
        Sets weather to enable multitouch and how many simultaneous touches to allow

        :param enable: Weather to enable multitouch
        :param simultaneous_touches: The number of simuntanious touches to register
        """

        b_mult_t = (simultaneous_touches - 1) << 2
        multi_touch_config = 0x00 if enable else 0x80 | b_mult_t
        self.write(_MULTIPLE_TOUCH_CONFIG, bytes([multi_touch_config]))

    def enable_keys(self, keys):
        """
        Sets which keys have sensing enabled

        :param keys: A list of the key numbers to enable in the range 0-5
        """

        self.write(_SENSOR_INPUT_ENABLE, _keys_to_byte(keys, default=b'\x3f'))

    def read_keys(self, as_list=False):
        """
        Read which keys are currently pressed

        :param as_list: Weather to return the raw register value from the IC or the key numbers in a list
        :return: The pressed keys in the format requested
        """

        status = self.read(_SENSOR_INPUT_STATUS, 1)
        self.write(_MAIN_CONTROL, b'\x00')  # enables next touch reading

        return _byte_to_keys(status, num_keys=5) if as_list else status

