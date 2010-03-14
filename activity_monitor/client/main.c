#include <nrk.h>
#include <include.h>
#include <ulib.h>
#include <stdio.h>
#include <avr/sleep.h>
#include <hal.h>
#include "sensors.h"
#include "rtlink.h"

#define NODE_ID         1

#if NODE_ID == 1
    #define RTL_TX_SLOT  8
    #define RTL_RX_SLOT  6
#else
    #error Invalid Node ID
#endif /* NODE_ID */



void _create_taskset();
void sensors_task(void);
void rtlink_task(void);

NRK_STK Stack1[NRK_APP_STACKSIZE];
nrk_task_type TaskOne;

NRK_STK Stack2[NRK_APP_STACKSIZE];
nrk_task_type TaskTwo;

sensors_packet_t sensor_buf;
uint8_t rtlink_tx_buf[RTL_MAX_BUF_SIZE];

nrk_sem_t *sensorPktSemaphore;

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

    sensorPktSemaphore = nrk_sem_create(1,2);
    if( sensorPktSemaphore==NULL ) {
        nrk_kprintf( PSTR("Error creating sem\r\n" ));
    }

    nrk_start();
  
    return 0;
}

void sensors_task(void)
{
    int8_t v;
    uint8_t i = 1;

    sensors_register_drivers();
    while(1) {
        nrk_gpio_toggle(NRK_DEBUG_0);
        sensors_read(&sensor_buf);

        v = nrk_sem_pend(sensorPktSemaphore);

        sprintf(rtlink_tx_buf, "[%d] bat=%d, temp=%d, light=%d, mic=%d, acc_x=%d, acc_y=%d, acc_z=%d", i++, sensor_buf.bat, sensor_buf.temp, sensor_buf.light, sensor_buf.mic, sensor_buf.adxl_x, sensor_buf.adxl_y, sensor_buf.adxl_z);

        v = nrk_sem_post(sensorPktSemaphore);
        nrk_wait_until_next_period();
    }
}

void rtlink_task(void)
{
    rtlink_setup(RTL_MOBILE, RTL_TX_SLOT, RTL_RX_SLOT);
    rtlink_packet_t *pRxBuf;
    int8_t v;

    while(1) {
        nrk_gpio_toggle(NRK_DEBUG_1);

/*
        if (rtl_rx_pkt_check() == 0)
            rtl_wait_until_rx_pkt();

        pRxBuf = rtlink_rx();
        if (pRxBuf != NULL) {
            rtlink_print_packet(pRxBuf);
            rtlink_rx_cleanup(pRxBuf);
        }
*/
        v = nrk_sem_pend(sensorPktSemaphore);
        rtlink_tx( &rtlink_tx_buf[0], strlen(&rtlink_tx_buf[0]) );
        v = nrk_sem_post(sensorPktSemaphore);

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
    TaskOne.period.nano_secs = 500*NANOS_PER_MS;
    TaskOne.cpu_reserve.nano_secs = 100*NANOS_PER_MS;
    TaskOne.offset.secs = 0;
    TaskOne.offset.nano_secs= 0;
    nrk_activate_task (&TaskOne);

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
    TaskTwo.cpu_reserve.nano_secs = 0;
    TaskTwo.offset.secs = 0;
    TaskTwo.offset.nano_secs= 0;
    nrk_activate_task (&TaskTwo);
}

