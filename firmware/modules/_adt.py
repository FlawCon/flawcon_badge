from micropython import const

ADT75_ADDRESS = const(0x48)

TEMP_REG = const(0x00)

class ADT75:
    def __init__(self, i2c,):
        self.i2c = i2c
        self._addr = ADT75

        self.read = lambda r, n: self.i2c.readfrom_mem(self._addr, r, n)

    def read_temp(self):
        data = self.read(TEMP_REG, 2)
        temp = ((data[0] * 256) + data[1]) / 16
        if temp > 2047:
            temp -= 4096
        return temp * 0.0625



