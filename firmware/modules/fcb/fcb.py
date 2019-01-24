import time
from micropython import const
from machine import Pin, I2C, EPSPI, UART
from fcb._capt import CAP1296
from fcb._adt import ADT75
from fcb._epd import EPD, RESOLUTION
from fcb._gfx import GFX
from fcb._font import Font

DISP_RESOLUTION = RESOLUTION[0]


class Event:
    """
    Storage class for event that is to be passed to an app

    :ivar is_special: Weather this is a character or special event
    :ivar val: The event value, a character if `is_special == False`, event dependent otherwise
    """

    #: Special event type for when the UP capacitive button is pressed
    UP = const(0)
    #: Special event type for when the DOWN capacitive button is pressed
    DOWN = const(1)
    #: Special event type for when the LEFT capacitive button is pressed
    LEFT = const(2)
    #: Special event type for when the RIGHT capacitive button is pressed
    RIGHT = const(3)
    #: Special event type for when the A capacitive button is pressed
    BUTTON_A = const(4)
    #: Special event type for when the B capacitive button is pressed
    BUTTON_B = const(5)

    def __init__(self, char=None, special=None):
        """
        :param char: Character that has been input, don't specify if event is special (i.e. not a character input)
        :param special: A special event that has occurred
        """
        if char is None and special is None:
            raise ValueError("Must specify either char or special")

        self.is_special = char is None
        self.val = char if char is not None else special


_CAPT_MAPPING = (Event.LEFT, Event.RIGHT, Event.UP, Event.DOWN, Event.BUTTON_A, Event.BUTTON_B)


class FCB:
    """
    The main OS class

    An instance of this is passed to the `__init__` of each app. Every app is expected to store this and use it when
    accessing the badge hardware.
    """

    def __init__(self):
        self._uart = UART(0, 115200)
        self._i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
        self._capt = CAP1296(i2c=self._i2c, alert_pin=Pin(10, Pin.IN), intr=self._handle_touch_intr)
        self._adt = ADT75(i2c=self._i2c)
        self._epd = EPD(spi=EPSPI(), cs_pin=Pin(15, Pin.OUT), reset_pin=Pin(0, Pin.OUT), busy_pin=Pin(16, Pin.IN))
        self._gfx = GFX(RESOLUTION[0][0], RESOLUTION[0][1], self._epd.set_pixel, self._epd.hline, self._epd.vline)
        self._font = Font(RESOLUTION[0][0], RESOLUTION[0][1], self._epd.set_pixel)

        self._event_queue = []
        self._app = None

    @property
    def i2c(self):
        """
        An instance of the :class:`I2C class <machine.I2C>` from micropython
        """
        return self._i2c

    @property
    def capt(self):
        """
        An instance of the :class:`CAPT1296 class <fcb._capt.CAP1296>` for accessing the capacitive touch chip\
        on the badge
        """
        return self._capt

    @property
    def adt(self):
        """
        An instance of the :class:`ADT75 class <fcb._adt.ADT75>` for accessing the temperature sensor  on the\
        badge
        """
        return self._adt

    @property
    def epd(self):
        """
        An instance of the :class:`EPD class <fcb._epd.EPD>` for accessing the e-paper display on the badge
        """
        return self._epd

    @property
    def gfx(self):
        return self._gfx

    @property
    def font(self):
        return self._font

    def write_i2c(self, addr, register, data):
        self._i2c.writeto_mem(addr, register, data)

    def read_i2c(self, addr, register, num):
        return self._i2c.readfrom_mem(addr, register, num)

    def start(self):
        self.clear_disp()
        self._epd.show()

        if self._app is None:
            app_mod = __import__('fcb.default_apps.circle_test')
            self._app = app_mod.App(self)

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
