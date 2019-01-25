import esp
esp.osdebug(None)
esp.sleep_type(esp.SLEEP_MODEM)

import gc
gc.threshold((gc.mem_free() + gc.mem_alloc()) // 4)
import uos
from flashbdev import bdev

try:
    if bdev:
        uos.mount(bdev, '/')
except OSError:
    import inisetup
    inisetup.setup()

gc.collect()

import webrepl
webrepl.start(password="HackWorld")

import fcb
with fcb.FCB(True) as fc:
    fc._start()
