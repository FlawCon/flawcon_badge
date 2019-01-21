/*
 * This file is part of the MicroPython project, http://micropython.org/
 *
 * The MIT License (MIT)
 *
 * Copyright (c) 2016 Damien P. George
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

#include <stdio.h>
#include <stdint.h>
#include <string.h>

#include "ets_sys.h"
#include "etshal.h"
#include "ets_alt_task.h"

#include "py/runtime.h"
#include "py/stream.h"
#include "py/mphal.h"
#include "extmod/machine_spi.h"
#include "modmachine.h"
#include "hspi.h"

#if MICROPY_PY_MACHINE_EP_SPI

typedef struct _machine_ep_spi_obj_t {
    mp_obj_base_t base;
} machine_ep_spi_obj_t;

STATIC mp_obj_t mp_machine_ep_spi_write(mp_obj_t self, mp_obj_t data, mp_obj_t dc) {
    spi_transaction(HSPI, 0, 0, 0, 0, 1, mp_obj_int_get_checked(dc), 0, 0);
    spi_tx8fast(HSPI, mp_obj_int_get_checked();
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_3(mp_machine_ep_spi_write_obj, mp_machine_ep_spi_write);

/******************************************************************************/
// MicroPython bindings for HSPI

STATIC void machine_ep_spi_print(const mp_print_t *print, mp_obj_t self_in, mp_print_kind_t kind) {
    mp_printf(print, "EP_SPI()");
}

STATIC mp_obj_t machine_ep_spi_init(mp_obj_t self) {
    spi_init_gpio(HSPI, SPI_CLK_80MHZ_NODIV);
    spi_clock(HSPI, 0, 0);
    spi_tx_byte_order(HSPI, SPI_BYTE_ORDER_HIGH_TO_LOW);
    spi_rx_byte_order(HSPI, SPI_BYTE_ORDER_HIGH_TO_LOW);
    CLEAR_PERI_REG_MASK(SPI_USER(HSPI), SPI_FLASH_MODE | SPI_USR_MISO |
                        SPI_USR_ADDR | SPI_USR_COMMAND | SPI_USR_DUMMY);
    CLEAR_PERI_REG_MASK(SPI_CTRL(HSPI), SPI_QIO_MODE | SPI_DIO_MODE |
                        SPI_DOUT_MODE | SPI_QOUT_MODE);
    spi_mode(HSPI, 0, 0);
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(machine_ep_spi_init_obj, machine_ep_spi_init);

mp_obj_t machine_ep_spi_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args) {
    mp_arg_check_num(n_args, n_kw, 0, 0, false);

    machine_ep_spi_obj_t *self = m_new_obj(machine_ep_spi_obj_t);
    self->base.type = &machine_ep_spi_type;
    machine_ep_spi_init(NULL);
    return MP_OBJ_FROM_PTR(self);
}

STATIC const mp_rom_map_elem_t machine_ep_spi_locals_dict_table[] = {
    { MP_ROM_QSTR(MP_QSTR_init), MP_ROM_PTR(&machine_ep_spi_init_obj) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&mp_machine_ep_spi_write_obj) },
};

MP_DEFINE_CONST_DICT(mp_machine_ep_spi_locals_dict, machine_ep_spi_locals_dict_table);

const mp_obj_type_t machine_ep_spi_type = {
    { &mp_type_type },
    .name = MP_QSTR_EPSPI,
    .print = machine_ep_spi_print,
    .make_new = machine_ep_spi_make_new,
    .locals_dict = (mp_obj_dict_t*)&mp_machine_ep_spi_locals_dict,
};

#endif // MICROPY_PY_MACHINE_EP_SPI
