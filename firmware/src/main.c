#ifdef BUILD_esp12e
#include "user_interface.h"
#endif

#include <stdint.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

#include "py/compile.h"
#include "py/runtime.h"
#include "py/gc.h"
#include "py/stackctrl.h"
#include "flawcon_mpe.h"

int main(void);

#ifdef BUILD_esp12e

uint32_t ICACHE_FLASH_ATTR user_rf_cal_sector_set(void) {
    enum flash_size_map size_map = system_get_flash_size_map();
    uint32 rf_cal_sec = 0;

    switch (size_map) {
        case FLASH_SIZE_4M_MAP_256_256:
            rf_cal_sec = 128 - 5;
            break;

        case FLASH_SIZE_8M_MAP_512_512:
            rf_cal_sec = 256 - 5;
            break;

        case FLASH_SIZE_16M_MAP_512_512:
        case FLASH_SIZE_16M_MAP_1024_1024:
            rf_cal_sec = 512 - 5;
            break;

        case FLASH_SIZE_32M_MAP_512_512:
        case FLASH_SIZE_32M_MAP_1024_1024:
            rf_cal_sec = 1024 - 5;
            break;

        default:
            rf_cal_sec = 0;
            break;
    }

    return rf_cal_sec;
}

void user_init(void) {
    system_init_done_cb((init_done_cb_t)main);
}

#endif

static char heap[2048];

int main() {
    gc_init(heap, heap + sizeof(heap));
    mp_init();

    const char str[] = "print('Hello world of easy embedding!')";
    mpe_do_str(str, MP_PARSE_SINGLE_INPUT);
}

