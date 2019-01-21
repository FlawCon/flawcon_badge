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

import esp
esp.sleep_type(esp.SLEEP_MODEM)

import fcb
fc = fcb.FCB()
fc.start()
