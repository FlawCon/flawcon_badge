import time
from micropython import const
from machine import Pin, I2C, EPSPI, UART
from fcb._capt import CAP1296
from fcb._adt import ADT75
from fcb._epd import EPD, RESOLUTION
from fcb._gfx import GFX
from fcb._font import Font


class Event:
    UP = const(0)
    DOWN = const(1)
    LEFT = const(2)
    RIGHT = const(3)
    BUTTON_A = const(4)
    BUTTON_B = const(5)

    def __init__(self, char=None, special=None):
        if char is None and special is None:
            raise ValueError("Must specify either char or special")

        self.is_special = char is None
        self.val = char if char is not None else special


_CAPT_MAPPING = (Event.LEFT, Event.RIGHT, Event.UP, Event.DOWN, Event.BUTTON_A, Event.BUTTON_B)


class FCB:
    def __init__(self):
        self._uart = UART(0, 115200)
        self._i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
        self._capt = CAP1296(i2c=self._i2c, alert_pin=Pin(10, Pin.IN), intr=self._handle_touch_intr)
        self._adt = ADT75(i2c=self._i2c)
        self._epd = EPD(spi=EPSPI(), cs_pin=Pin(15, Pin.OUT), reset_pin=Pin(0, Pin.OUT), busy_pin=Pin(16, Pin.IN))
        self._gfx = GFX(RESOLUTION[0][0], RESOLUTION[0][1], self._epd.set_pixel)
        self._font = Font(RESOLUTION[0][0], RESOLUTION[0][1], self._epd.set_pixel)

        self._event_queue = []
        self._app = None

    def start(self):
        self.clear_disp()
        self._epd.show()

        if self._app is None:
            app_mod = __import__('fcb.default_apps.circle_test')
            self._app = app_mod.App()

        while True:
            if not self._event_waiting() and self._uart.any() == 0:
                time.sleep_ms(10)
                continue
            if self._uart.any() != 0:
                self._handle_uart()
            if self._event_waiting():
                while self._event_waiting():
                    self._app.handle_event(self._event_queue.popleft())
            self._app.redraw()
            if self._epd.dirty:
                self._epd.show()

    def clear_disp(self):
        self._gfx.fill_rect(0, 0, RESOLUTION[0][0], RESOLUTION[0][1], 0)

    def _event_waiting(self):
        return bool(len(self._event_queue))

    def _handle_touch_intr(self, keys):
        for k in keys:
            self._event_queue.append(Event(special=_CAPT_MAPPING[k]))

    def _handle_uart(self):
        while self._uart.any() != 0:
            self._event_queue.append(Event(char=self._uart.read(1)))
