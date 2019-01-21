from micropython import const
from machine import Pin, I2C

CAP1296_I2C_ADDRESS = const(0x28)

MAIN_CONTROL = const(0x00)
SENSOR_INPUT_STATUS = const(0x03)
SENSOR_INPUT_ENABLE = const(0x21)
INTERRUPT_ENABLE = const(0x27)
MULTIPLE_TOUCH_CONFIG = const(0x2A)


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


class _CAP1296:
    def __init__(self, i2c, alert_pin):
        self.i2c = i2c
        self._addr = CAP1296_I2C_ADDRESS

        self.write = lambda r, b: self.i2c.writeto_mem(self._addr, r, b)
        self.read = lambda r, n: self.i2c.readfrom_mem(self._addr, r, n)
        self.enable_interrupt([])

    def enable_interrupt(self, keys):
        self.write(INTERRUPT_ENABLE, _keys_to_byte(keys))

    def enable_multitouch(self, enable, simultaneous_touches=1):
        b_mult_t = (simultaneous_touches - 1) << 2
        multi_touch_config = 0x00 if enable else 0x80 | b_mult_t
        self.write(MULTIPLE_TOUCH_CONFIG, bytes([multi_touch_config]))

    def enable_keys(self, keys):
        self.write(SENSOR_INPUT_ENABLE, _keys_to_byte(keys, default=b'\x3f'))

    def read_keys(self, as_list=False):
        status = self.read(SENSOR_INPUT_STATUS, 1)
        self.write(MAIN_CONTROL, b'\x00')  # enables next touch reading

        return _byte_to_keys(status, num_keys=5) if as_list else status


capt = _CAP1296(i2c=I2C(cl=Pin(5), sda=Pin(4), freq=100000), alert_pin=Pin(10))
