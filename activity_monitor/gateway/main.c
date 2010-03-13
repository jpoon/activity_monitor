#include <nrk.h>
#include <include.h>
#include <ulib.h>
#include <stdio.h>
#include <avr/sleep.h>
#include <hal.h>
#include "rtlink.h"

#define RTL_TX_SLOT 6
#define RTL_RX_SLOT 8

void _create_taskset();
void rtlink_task(void);

NRK_STK Stack1[NRK_APP_STACKSIZE];
nrk_task_type TaskOne;

NRK_STK Stack2[NRK_APP_STACKSIZE];
nrk_task_type TaskTwo;

uint8_t rtlink_tx_buf[RTL_MAX_BUF_SIZE];

int main(void)
{
    nrk_setup_ports();
    nrk_setup_uart(UART_BAUDRATE_115K2);

    nrk_kprintf( PSTR("Starting up...\r\n") );

    nrk_init();

    nrk_led_clr(ORANGE_LED);
    nrk_led_clr(GREEN_LED);
    nrk_led_clr(RED_LED);
    nrk_led_clr(BLUE_LED);

    nrk_time_set(0,0);
    rtlink_init();
    _create_taskset();

    nrk_start();
  
    return 0;
}

void rtlink_task(void)
{
    rtlink_setup(RTL_COORDINATOR, RTL_TX_SLOT, RTL_RX_SLOT);
    rtlink_packet_t *pRxBuf;
    int8_t v;

    while(1) {
        nrk_gpio_toggle(NRK_DEBUG_1);

        if (rtl_rx_pkt_check() == 0)
            rtl_wait_until_rx_pkt();

        pRxBuf = rtlink_rx();
        if (pRxBuf != NULL) {
            rtlink_print_packet(pRxBuf);
            rtlink_rx_cleanup(pRxBuf);
        }

        nrk_wait_until_next_period();
    }
}


void _create_taskset()
{
    nrk_kprintf ( PSTR("taskset: creating rtlink\r\n") );
    TaskOne.task = rtlink_task;
    nrk_task_set_stk( &TaskOne, Stack1, NRK_APP_STACKSIZE);
    TaskOne.prio = 1;
    TaskOne.FirstActivation = TRUE;
    TaskOne.Type = BASIC_TASK;
    TaskOne.SchType = PREEMPTIVE;
    TaskOne.period.secs = 1;
    TaskOne.period.nano_secs = 0;
    TaskOne.cpu_reserve.secs = 500*NANOS_PER_MS;
    TaskOne.cpu_reserve.nano_secs = 0;
    TaskOne.offset.secs = 0;
    TaskOne.offset.nano_secs= 0;
    nrk_activate_task (&TaskOne);
}

