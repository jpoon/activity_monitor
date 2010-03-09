#include <nrk.h>
#include <include.h>
#include <ulib.h>
#include <stdio.h>
#include <avr/sleep.h>
#include <hal.h>
#include <rt_link.h>
#include <nrk_error.h>
#include <nrk_timer.h>
#include "sensors.h"

#define NODE_ID	    2

#if NODE_ID == 1
	#define MY_TX_SLOT  6
	#define MY_RX_SLOT  8
    #define COORDINATOR
#elif NODE_ID == 2
	#define MY_TX_SLOT  8
	#define MY_RX_SLOT  0
#endif

NRK_STK Stack1[NRK_APP_STACKSIZE];
nrk_task_type TaskOne;
void communicate_task(void);

NRK_STK Stack2[NRK_APP_STACKSIZE];
nrk_task_type TaskTwo;
void sensor_task(void);

void nrk_create_taskset();

// tx, rx buffers
uint8_t tx_buf[MAX_RTL_PKT_SIZE];
uint8_t rx_buf[MAX_RTL_PKT_SIZE];

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
    rtl_task_config();
    nrk_create_taskset();
    nrk_start();
  
    return 0;
}

void communicate_task (void)
{
    int8_t rssi;
    uint8_t length, slot;
    uint8_t *local_rx_buf;

#ifdef COORDINATOR
    nrk_kprintf( PSTR( "rtl: Coordinator\r\n") ); 
    rtl_init(RTL_COORDINATOR);
    nrk_led_set(RED_LED);  
#else
    nrk_kprintf( PSTR( "rtl: Mobile\r\n") ); 
    rtl_init(RTL_MOBILE);
#endif

    printf( "rtl: TX %d  RX %d\r\n", MY_TX_SLOT, MY_RX_SLOT);

    rtl_set_channel(15);
    rtl_set_schedule( RTL_TX, MY_TX_SLOT, 1 ); 
    rtl_set_schedule( RTL_RX, MY_RX_SLOT, 1 ); 
    rtl_start();
    rtl_rx_pkt_set_buffer(rx_buf, RF_MAX_PAYLOAD_SIZE);

    while(!rtl_ready()) {
        nrk_kprintf( PSTR("rtl: waiting for rtl to be ready\r\n") );
        nrk_wait_until_next_period();
    }
    while(!rtl_sync_status()) {
        nrk_kprintf( PSTR("rtl: out-of-sync\r\n") );
        nrk_wait_until_next_period();
    }

    nrk_kprintf( PSTR("rtl: ready\r\n") );

    while(1) {
#ifdef COORDINATOR
        if( rtl_rx_pkt_check()!=0 ) {
            nrk_led_set(GREEN_LED);
            local_rx_buf = rtl_rx_pkt_get(&length, &rssi, &slot);
            printf( "rtl: rx slot %d, rssi %d, length %d: ", slot, rssi, length );
            for(uint8_t i=PKT_DATA_START; i<length; i++ )
            {
                printf( "%c",local_rx_buf[i] );
            }
            nrk_kprintf( PSTR("\r\n") );
            rtl_rx_pkt_release();
            nrk_led_clr(GREEN_LED);
        }
#else
        if( rtl_tx_pkt_check( MY_TX_SLOT ) != 0 ) {
            printf( "rtl: pending packet on slot %d\r\n", MY_TX_SLOT );
        } else {
            nrk_led_set(GREEN_LED);

            uint8_t i = 1;
            sprintf( &tx_buf[PKT_DATA_START], "test %d", i);
            length = strlen(&tx_buf[PKT_DATA_START])+PKT_DATA_START;
//            length = strlen(tx_buf);
            for(uint8_t i=PKT_DATA_START; i<length; i++ )
            {
                printf( "%c",tx_buf[i] );
            }
 
            rtl_tx_pkt( tx_buf, length, MY_TX_SLOT );
            printf( "rtl: tx packet on slot %d\r\n",MY_TX_SLOT );

            nrk_led_clr(GREEN_LED);
        }
#endif
        rtl_wait_until_rx_or_tx();
    }
}

void sensor_task()
{
    ff_register_drivers();
    while(1) {
      printf( "sensor task\r\n");
      nrk_wait_until_next_period();
    }
//    ff_read_sensors();
}

void nrk_create_taskset()
{
    nrk_kprintf ( PSTR("Creating Taskset: ") );

    TaskOne.task = communicate_task;
    TaskOne.Ptos = (void *) &Stack1[NRK_APP_STACKSIZE-1];
    TaskOne.Pbos = (void *) &Stack1[0];
    TaskOne.prio = 2;
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
/*
    TaskTwo.task = sensor_task;
    nrk_task_set_stk( &TaskTwo, Stack2, NRK_APP_STACKSIZE);
    TaskTwo.prio = 3;
    TaskTwo.FirstActivation = TRUE;
    TaskTwo.Type = BASIC_TASK;
    TaskTwo.SchType = PREEMPTIVE;
    TaskTwo.period.secs = 5;
    TaskTwo.period.nano_secs = 0;
    TaskTwo.cpu_reserve.secs = 0;
    TaskTwo.cpu_reserve.nano_secs = 0;
    TaskTwo.offset.secs = 0;
    TaskTwo.offset.nano_secs= 0;
    nrk_activate_task (&TaskTwo);
*/
    nrk_kprintf ( PSTR("Done\r\n") );
}

