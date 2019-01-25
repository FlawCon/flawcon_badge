//
// Created by benjamin on 21/01/19.
//

#include <string.h>
#include "py/runtime.h"
#include "py/gc.h"
#include "py/obj.h"

const mp_obj_type_t framegen_type;

typedef struct _framegen_obj_t {
    mp_obj_base_t base;
    unsigned int rows;
    unsigned int cols;
    unsigned int curRow;
    unsigned int curCol;
    mp_obj_t comp_obj;
    mp_obj_t pixel_func;
} framegen_obj_t;

STATIC mp_obj_t framegen_next(mp_obj_t self_in) {
    mp_check_self(MP_OBJ_IS_TYPE(self_in, &framegen_type));
    framegen_obj_t *self = MP_OBJ_TO_PTR(self_in);

    uint8_t out = 0;
    for (uint8_t i = 0; i < 8; i++) {
        mp_obj_t pix_val = mp_call_function_2(self->pixel_func, mp_obj_new_int(self->curCol+i), mp_obj_new_int(self->curRow));
        if (mp_obj_equal(pix_val, self->comp_obj)) {
            out += 1 << (7-i);
        }
    }
    self->curCol += 8;
    if (self->curCol >= self->cols) {
        self->curRow += 1;
        self->curCol = 0;
        if (self->curRow >= self->rows) {
            return MP_OBJ_STOP_ITERATION;
        }
    }

    return mp_obj_new_int(out);
}

STATIC void framegen_print(const mp_print_t *print, mp_obj_t self_in, mp_print_kind_t kind) {
    mp_printf(print, "FrameGen()");
}

mp_obj_t framegen_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args) {
    mp_arg_check_num(n_args, n_kw, 4, 4, false);

    framegen_obj_t *self = m_new_obj(framegen_obj_t);
    self->base.type = &framegen_type;
    self->cols = mp_obj_int_get_checked(args[0]);
    self->rows = mp_obj_int_get_checked(args[1]);
    self->curCol = 0;
    self->curRow = 0;
    self->comp_obj = args[2];
    self->pixel_func = args[3];

    return MP_OBJ_FROM_PTR(self);
}

const mp_obj_type_t framegen_type = {
        { &mp_type_type },
        .name = MP_QSTR_FrameGen,
        .print = framegen_print,
        .make_new = framegen_make_new,
        .getiter = mp_identity_getiter,
        .iternext = framegen_next,
};

STATIC const mp_rom_map_elem_t framegen_module_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_framegen) },
    { MP_ROM_QSTR(MP_QSTR_FrameGen), MP_ROM_PTR(&framegen_type) },
};

STATIC MP_DEFINE_CONST_DICT(framegen_module_globals, framegen_module_globals_table);

const mp_obj_module_t framegen_module = {
        .base = { &mp_type_module },
        .globals = (mp_obj_dict_t*)&framegen_module_globals,
};
