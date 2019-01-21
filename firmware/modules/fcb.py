from machine import Pin, I2C, EPSPI
from _capt import CAP1296
from _epd import EPD, RESOLUTION
from _gfx import GFX


class FCB:
    def __init__(self):
        self._i2c = I2C(cl=Pin(5), sda=Pin(4), freq=100000)
        self._capt = CAP1296(i2c=self._i2c, alert_pin=Pin(10, Pin.In), intr=self.handle_touch_intr)
        self._epd = EPD(spi=EPSPI(), cs_pin=Pin(15, Pin.OUT), reset_pin=Pin(0, Pin.OUT), busy_pin=Pin(16, Pin.IN))
        self._gfx = GFX(RESOLUTION[0][0], RESOLUTION[0][1], self._epd.set_pixel)

    def start(self):
        self.clear_disp()
        self._epd.show()

    def clear_disp(self):
        self._gfx.fill_rect(0, 0, RESOLUTION[0][0], RESOLUTION[0][1], 0)

    def handle_touch_intr(self, keys):
        pass
