#include "user_interface.h"

void init_done(void) {
    wifi_fpm_set_sleep_type(MODEM_SLEEP_T);
    if (wifi_get_opmode() == NULL_MODE) {
        wifi_fpm_open();
        wifi_fpm_do_sleep(0xfffffff);
    }

//#if MICROPY_REPL_EVENT_DRIVEN
//    uart_task_init();
//#endif
//    mp_reset();
//    mp_hal_stdout_tx_str("\r\n");
//#if MICROPY_REPL_EVENT_DRIVEN
//    pyexec_event_repl_init();
//#endif
//
//#if !MICROPY_REPL_EVENT_DRIVEN
//    soft_reset:
//    for (;;) {
//        if (pyexec_mode_kind == PYEXEC_MODE_RAW_REPL) {
//            if (pyexec_raw_repl() != 0) {
//                break;
//            }
//        } else {
//            if (pyexec_friendly_repl() != 0) {
//                break;
//            }
//        }
//    }
//    soft_reset();
//    goto soft_reset;
//#endif
}

void user_init(void) {
    system_timer_reinit();
    system_init_done_cb(init_done);
}

