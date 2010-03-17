#include <nrk.h>
#include <include.h>
#include <ulib.h>
#include <stdio.h>
#include <avr/sleep.h>
#include <hal.h>
#include "sensors.h"
#include "comm.h"

#define MAC_ADDR         0x0010

static void createTaskset(void);
static void sensors_task(void);
static void comm_task(void);

NRK_STK Stack1[NRK_APP_STACKSIZE];
nrk_task_type TaskOne;

NRK_STK Stack2[NRK_APP_STACKSIZE];
nrk_task_type TaskTwo;

sensors_packet_t sensor_buf;
bool sensorPktReady = false;
nrk_sem_t *sensorPktSemaphore;

int main(void)
{
    nrk_setup_ports();
    nrk_setup_uart(UART_BAUDRATE_115K2);

    nrk_kprintf( PSTR("Starting up...\r\n") );

    nrk_init();

    nrk_led_clr(ORANGE_LED);
    nrk_led_clr(GREEN_LED);
    nrk_led_clr(BLUE_LED);
    nrk_led_set(RED_LED);

    nrk_time_set(0,0);
    comm_init();
    createTaskset();
    

    sensorPktSemaphore = nrk_sem_create(1,2);
    if( sensorPktSemaphore==NULL ) {
        nrk_kprintf( PSTR("Error creating sem\r\n" ));
    }

    nrk_start();
  
    return 0;
}

static void sensors_task(void)
{
    int8_t v;

    sensors_register_drivers();
    while(1) {
        nrk_gpio_toggle(NRK_DEBUG_0);

        v = nrk_sem_pend(sensorPktSemaphore);
        sensors_read(&sensor_buf);
        sensorPktReady = true;
        v = nrk_sem_post(sensorPktSemaphore);

        nrk_wait_until_next_period();
    }
}

static void comm_task(void)
{
    comm_packet_t tx_buf;
    uint8_t i = 1;

    comm_setup(MAC_ADDR);
    int8_t v;

    while(1) {
        nrk_gpio_toggle(NRK_DEBUG_1);

        v = nrk_sem_pend(sensorPktSemaphore);
        if (sensorPktReady) {
            sprintf(tx_buf.payload, "[%d] bat=%d, temp=%d, light=%d, mic=%d, acc_x=%d, acc_y=%d, acc_z=%d", i++, sensor_buf.bat, sensor_buf.temp, sensor_buf.light, sensor_buf.mic, sensor_buf.adxl_x, sensor_buf.adxl_y, sensor_buf.adxl_z);
            tx_buf.len = strlen(tx_buf.payload);
            tx_buf.addr = COMM_BROADCAST;
            comm_tx( &tx_buf );
            sensorPktReady = false;
        }
        v = nrk_sem_post(sensorPktSemaphore);

        nrk_wait_until_next_period();
    }
}


static void createTaskset(void)
{
    nrk_kprintf ( PSTR("taskset: creating comm\r\n") );
    TaskOne.task = comm_task;
    nrk_task_set_stk( &TaskOne, Stack1, NRK_APP_STACKSIZE);
    TaskOne.prio = 1;
    TaskOne.FirstActivation = TRUE;
    TaskOne.Type = BASIC_TASK;
    TaskOne.SchType = PREEMPTIVE;
    TaskOne.period.secs = 1;
    TaskOne.period.nano_secs = 0;
    TaskOne.cpu_reserve.nano_secs = 250*NANOS_PER_MS;
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
    TaskTwo.period.nano_secs = 0;
    TaskTwo.cpu_reserve.secs = 0;
    TaskTwo.cpu_reserve.nano_secs = 500*NANOS_PER_MS;
    TaskTwo.offset.secs = 0;
    TaskTwo.offset.nano_secs= 0;
    nrk_activate_task (&TaskTwo);
}

