//
// Created by benjamin on 21/01/19.
//

#include "py/runtime.h"
#include "py/gc.h"
#include "py/obj.h"
#include "qrcode.h"
#include "modqr.h"

const mp_obj_type_t qr_type;

typedef struct _qr_obj_t {
    mp_obj_base_t base;
    uint8_t qr_version;
    QRCode qrCode;
    uint8_t* qrCodeBytes;
} qr_obj_t;

STATIC mp_obj_t qr_write(mp_obj_t self_in, mp_obj_t data, mp_obj_t ecc_in) {
    qr_obj_t *self = MP_OBJ_TO_PTR(self_in);
    uint8_t ecc = mp_obj_int_get_checked(ecc_in);
    if (0 > ecc || ecc > 3) {
        nlr_raise(mp_obj_new_exception_msg(&mp_type_ValueError, "QR ECC must be between 0 and 3"));
    }
    size_t len;
    qrcode_initBytes(&self->qrCode, self->qrCodeBytes, self->qr_version, ecc, (uint8_t*)mp_obj_str_get_data(data, &len), len);
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_3(qr_write_obj, qr_write);

STATIC mp_obj_t qr_matrix(mp_obj_t self_in, mp_obj_t data, mp_obj_t ecc_in) {
    qr_obj_t *self = MP_OBJ_TO_PTR(self_in);
    mp_obj_t out = mp_obj_new_list(self->qrCode.size, NULL);
    for (uint8_t y = 0; y < self->qrCode.size; y++) {
        mp_obj_t row = mp_obj_new_list(self->qrCode.size, NULL);
        mp_obj_list_store(out, mp_obj_new_int(y), row);
        for (uint8_t x = 0; x < self->qrCode.size; x++) {
            if (qrcode_getModule(&self->qrCode, x, y)) {
                mp_obj_list_store(row, mp_obj_new_int(x), mp_const_true);
            } else {
                mp_obj_list_store(row, mp_obj_new_int(x), mp_const_false);
            }
        }
    }
    return out;
}
MP_DEFINE_CONST_FUN_OBJ_3(qr_matrix_obj, qr_matrix);


STATIC void qr_print(const mp_print_t *print, mp_obj_t self_in, mp_print_kind_t kind) {
    qr_obj_t *self = MP_OBJ_TO_PTR(self_in);
    mp_printf(print, "EP_SPI(%u)", self->qr_version);
}

mp_obj_t qr_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args) {
    mp_arg_check_num(n_args, n_kw, 1, 1, false);

    uint8_t qr_version = mp_obj_get_int(args[0]);
    if (1 > qr_version || qr_version > 40) {
        nlr_raise(mp_obj_new_exception_msg(&mp_type_ValueError, "QR Version must be between 1 and 40"));
    }

    qr_obj_t *self = m_new_obj(qr_obj_t);
    self->base.type = &qr_type;
    self->qr_version = qr_version;
    self->qrCodeBytes = gc_alloc(qrcode_getBufferSize(qr_version), false);
    return MP_OBJ_FROM_PTR(self);
}

STATIC const mp_rom_map_elem_t qr_locals_dict_table[] = {
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&qr_write_obj) },
    { MP_ROM_QSTR(MP_QSTR_matrix), MP_ROM_PTR(&qr_matrix_obj) },
};

MP_DEFINE_CONST_DICT(qr_locals_dict, qr_locals_dict_table);

const mp_obj_type_t qr_type = {
        { &mp_type_type },
        .name = MP_QSTR_QR,
        .print = qr_print,
        .make_new = qr_make_new,
        .locals_dict = (mp_obj_dict_t*)&qr_locals_dict,
};

STATIC const mp_rom_map_elem_t qr_module_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_qr) },
    { MP_ROM_QSTR(MP_QSTR_QR), MP_ROM_PTR(&qr_type) },
    { MP_ROM_QSTR(MP_QSTR_ECC_LOW), MP_ROM_INT(ECC_LOW) },
    { MP_ROM_QSTR(MP_QSTR_ECC_MEDIUM), MP_ROM_INT(ECC_MEDIUM) },
    { MP_ROM_QSTR(MP_QSTR_ECC_QUARTILE), MP_ROM_INT(ECC_QUARTILE) },
    { MP_ROM_QSTR(MP_QSTR_ECC_HIGH), MP_ROM_INT(ECC_HIGH) },
};

STATIC MP_DEFINE_CONST_DICT(qr_module_globals, qr_module_globals_table);

const mp_obj_module_t qr_module = {
        .base = { &mp_type_module },
        .globals = (mp_obj_dict_t*)&qr_module_globals,
};
