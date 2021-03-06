#include <nrk.h>
#include <include.h>
#include <ulib.h>
#include <stdio.h>
#include <avr/sleep.h>
#include <hal.h>
#include <nrk_error.h>
#include "sensors.h"
#include "comm.h"
#include <math.h>

#define MAC_ADDR            0x0013
#define NUM_SAMPLES         50

static void createTaskset(void);
static void sensors_task(void);
static void comm_task(void);

NRK_STK Stack1[NRK_APP_STACKSIZE];
nrk_task_type TaskOne;

NRK_STK Stack2[NRK_APP_STACKSIZE];
nrk_task_type TaskTwo;

comm_packet_t tx_buf;
bool txPktReady = false;
nrk_sem_t *txPktSemaphore;

int main(void)
{
    nrk_setup_ports();
    nrk_setup_uart(UART_BAUDRATE_115K2);

    nrk_kprintf( PSTR("Starting up...\r\n") );

    nrk_init();

    nrk_led_clr(ORANGE_LED);
    nrk_led_clr(GREEN_LED);
    nrk_led_clr(BLUE_LED);
    nrk_led_clr(RED_LED);

    switch (MAC_ADDR) {
        case 0x0010:
        case 0x0011:
            nrk_led_set(RED_LED);
            break;

        case 0x0012:
        case 0x0013:
            nrk_led_set(GREEN_LED);
            break;
    }

    nrk_time_set(0,0);
    comm_init();
    createTaskset();
    
    txPktSemaphore = nrk_sem_create(1,2);
    if( txPktSemaphore==NULL ) {
        nrk_kprintf( PSTR("Error creating sem\r\n" ));
    }

    nrk_start();
  
    return 0;
}

static void sensors_task(void)
{
    uint8_t num_samples = 0;
    sensors_packet_t sample, total;

    sensors_register_drivers();

    memset( &total, 0, sizeof(sensors_packet_t));
    while(1) {
        nrk_gpio_toggle(NRK_DEBUG_0);

        sensors_read(&sample);
//        sensors_print(&sample);

        total.adxl_x += sample.adxl_x;
        total.adxl_y += sample.adxl_y;
        total.adxl_z += sample.adxl_z;

        num_samples++;
        if ( num_samples == NUM_SAMPLES ) {
            total.adxl_x = total.adxl_x/NUM_SAMPLES; 
            total.adxl_y = total.adxl_y/NUM_SAMPLES;
            total.adxl_z = total.adxl_z/NUM_SAMPLES;

            nrk_sem_pend(txPktSemaphore);
            sprintf(tx_buf.payload, "x=%d y=%d z=%d", total.adxl_x, total.adxl_y, total.adxl_z);
            txPktReady = true;
            nrk_sem_post(txPktSemaphore);

            num_samples = 0;
            memset( &total, 0, sizeof(sensors_packet_t));
        }

        nrk_wait_until_next_period();
    }
}

static void comm_task(void)
{
    int8_t err;
    comm_setup(MAC_ADDR);

    while(1) {
        nrk_gpio_toggle(NRK_DEBUG_1);

        nrk_sem_pend(txPktSemaphore);
        if (txPktReady) {
            tx_buf.len = strlen(tx_buf.payload);

            // print contents of packet
            nrk_kprintf( PSTR("comm: contents=[ ") );
            for(uint8_t i=0; i < tx_buf.len; i++ ) {
                printf( "%c", tx_buf.payload[i] );
            }
            nrk_kprintf( PSTR(" ]\r\n"));

            comm_tx( &tx_buf );

            memset(&tx_buf, 0, sizeof(comm_packet_t));
            txPktReady = false;
        }
        nrk_sem_post(txPktSemaphore);

        nrk_wait_until_next_period();
    }
}


static void createTaskset(void)
{
    nrk_kprintf ( PSTR("taskset: creating comm\r\n") );
    TaskOne.task = comm_task;
    nrk_task_set_stk( &TaskOne, Stack1, NRK_APP_STACKSIZE);
    TaskOne.prio = 2;
    TaskOne.FirstActivation = TRUE;
    TaskOne.Type = BASIC_TASK;
    TaskOne.SchType = PREEMPTIVE;
    TaskOne.period.secs = 0;
    TaskOne.period.nano_secs = 100*NANOS_PER_MS;
    TaskOne.cpu_reserve.nano_secs = 0;
    TaskOne.offset.secs = 0;
    TaskOne.offset.nano_secs= 0;
    nrk_activate_task (&TaskOne);

    nrk_kprintf ( PSTR("taskset: creating sensors\r\n") );
    TaskTwo.task = sensors_task;
    nrk_task_set_stk( &TaskTwo, Stack2, NRK_APP_STACKSIZE);
    TaskTwo.prio = 1;
    TaskTwo.FirstActivation = TRUE;
    TaskTwo.Type = BASIC_TASK;
    TaskTwo.SchType = PREEMPTIVE;
    TaskTwo.period.secs = 0;
    TaskTwo.period.nano_secs = 5*NANOS_PER_MS;
    TaskTwo.cpu_reserve.secs = 0;
    TaskTwo.cpu_reserve.nano_secs = 0;
    TaskTwo.offset.secs = 0;
    TaskTwo.offset.nano_secs= 0;
    nrk_activate_task (&TaskTwo);
}

