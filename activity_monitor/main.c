#include <nrk.h>
#include <include.h>
#include <ulib.h>
#include <stdio.h>
#include <avr/sleep.h>
#include <hal.h>
#include "sensors.h"
#include "rtlink.h"

void _create_taskset();
void sensors_task(void);
void rtlink_task(void);

NRK_STK Stack1[NRK_APP_STACKSIZE];
nrk_task_type TaskOne;

NRK_STK Stack2[NRK_APP_STACKSIZE];
nrk_task_type TaskTwo;

sensors_packet_t sensor_buf;
rtlink_packet_t rtlink_buf;

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


void sensors_task(void)
{
    sensors_register_drivers();
    while(1) {
        nrk_gpio_toggle(NRK_DEBUG_0);
        sensors_read(&sensor_buf);
        nrk_wait_until_next_period();
    }
}

void rtlink_task(void)
{
    int8_t rssi;
    uint8_t length, slot;
    uint8_t *local_rx_buf;

    rtlink_setup();

    while(1) {
        nrk_gpio_toggle(NRK_DEBUG_1);
#ifdef COORDINATOR
        rtlink_rx(&rtlink_buf);
        if (rtlink_buf.len != 0) {
            rtlink_print_packet(&rtlink_buf);
        }
        rtlink_rx_cleanup(&rtlink_buf);
#else

#include <rt_link.h>

uint8_t tx_buf[MAX_RTL_PKT_SIZE];
        if( rtl_tx_pkt_check( RTL_TX_SLOT ) != 0 ) {
            printf( "rtl: pending packet on slot %d\r\n", RTL_TX_SLOT );
        } else {
            nrk_led_set(GREEN_LED);

            uint8_t i = 1;
            sprintf( &tx_buf[PKT_DATA_START], "test %d", i);
            length = strlen(&tx_buf[PKT_DATA_START])+PKT_DATA_START;
            rtl_tx_pkt( tx_buf, length, RTL_TX_SLOT );
            printf( "rtl: tx packet on slot %d\r\n",RTL_TX_SLOT );

            nrk_led_clr(GREEN_LED);
        }
#endif
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
    TaskOne.cpu_reserve.secs = 0;
    TaskOne.cpu_reserve.nano_secs = 100*NANOS_PER_MS;
    TaskOne.offset.secs = 0;
    TaskOne.offset.nano_secs= 0;
    nrk_activate_task (&TaskOne);

#if NODE_ID != 1
    nrk_kprintf ( PSTR("taskset: creating sensors\r\n") );
    TaskTwo.task = sensors_task;
    nrk_task_set_stk( &TaskTwo, Stack2, NRK_APP_STACKSIZE);
    TaskTwo.prio = 2;
    TaskTwo.FirstActivation = TRUE;
    TaskTwo.Type = BASIC_TASK;
    TaskTwo.SchType = PREEMPTIVE;
    TaskTwo.period.secs = 1;
    TaskTwo.period.nano_secs = 100*NANOS_PER_MS;
    TaskTwo.cpu_reserve.secs = 1;
    TaskTwo.cpu_reserve.nano_secs = 50*NANOS_PER_MS;
    TaskTwo.offset.secs = 0;
    TaskTwo.offset.nano_secs= 0;
    nrk_activate_task (&TaskTwo);
#endif
}

