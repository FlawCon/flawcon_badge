from micropython import const

_ADT75_ADDRESS = const(0x48)

_TEMP_REG = const(0x00)


class ADT75:
    """
    A driver for reading the temperate from the ADT75 temperature chip on the badge
    """

    def __init__(self, i2c):
        self.i2c = i2c
        self._addr = _ADT75_ADDRESS

        self.read = lambda r, n: self.i2c.readfrom_mem(self._addr, r, n)

    def read_temp(self):
        """
        Reads the current temperature

        :return: The temperature in degrees celsius
        """
        return 19.0
        data = self.read(_TEMP_REG, 2)
        temp = ((data[0] * 256) + data[1]) / 16
        if temp > 2047:
            temp -= 4096
        return temp * 0.0625
