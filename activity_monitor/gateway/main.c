#include <nrk.h>
#include <include.h>
#include <ulib.h>
#include <stdio.h>
#include <avr/sleep.h>
#include <hal.h>
#include <slip.h>
#include "rtlink.h"

#define RTL_TX_SLOT 6
#define RTL_RX_SLOT 8

#define MAX_SLIP_BUF 48

static void createTaskset(void);
static void rtlink_task(void);
static void slipstream_task(void);

NRK_STK Stack1[NRK_APP_STACKSIZE];
nrk_task_type TaskOne;

NRK_STK Stack2[NRK_APP_STACKSIZE];
nrk_task_type TaskTwo;

uint8_t rtlink_tx_buf[RTL_MAX_BUF_SIZE];
uint8_t slip_rx_buf[MAX_SLIP_BUF];
uint8_t slip_tx_buf[MAX_SLIP_BUF];

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
    createTaskset();

    nrk_start();
  
    return 0;
}

static void rtlink_task(void)
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

static void slipstream_task() {
    int8_t v;

    slip_init(stdin, stdout, 0, 0);
    while (slip_started () != 1)
        nrk_wait_until_next_period ();

    while(1) {
        nrk_gpio_toggle(NRK_DEBUG_2);

        int8_t cnt = 1;
        sprintf (slip_tx_buf, "Hello %d", cnt);
        slip_tx (slip_tx_buf, strlen (slip_tx_buf));
 
        v = slip_rx(slip_rx_buf, MAX_SLIP_BUF);
        if (v > 0) {
            nrk_kprintf (PSTR ("slipstream: "));
            for (uint8_t i = 0; i < v; i++)
                printf ("%c", slip_rx_buf[i]);
        }

        nrk_wait_until_next_period();
    }
}

static void createTaskset(void)
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

    TaskTwo.task = slipstream_task;
    nrk_task_set_stk( &TaskTwo, Stack2, NRK_APP_STACKSIZE);
    TaskTwo.prio = 2;
    TaskTwo.FirstActivation = TRUE;
    TaskTwo.Type = BASIC_TASK;
    TaskTwo.SchType = PREEMPTIVE;
    TaskTwo.period.secs = 0;
    TaskTwo.period.nano_secs = 250 * NANOS_PER_MS;
    TaskTwo.cpu_reserve.secs = 0;
    TaskTwo.cpu_reserve.nano_secs = 0;
    TaskTwo.offset.secs = 0;
    TaskTwo.offset.nano_secs = 0;
    nrk_activate_task (&TaskTwo);
}

