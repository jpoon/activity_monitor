#include <nrk.h>
#include <include.h>
#include <ulib.h>
#include <stdio.h>
#include <avr/sleep.h>
#include <hal.h>
#include <rt_link.h>
#include <nrk_error.h>

#define MY_TX_SLOT  6
#define MY_RX_SLOT  8

NRK_STK Stack1[NRK_APP_STACKSIZE];
nrk_task_type TaskOne;
void Task1(void);

void nrk_create_taskset();

// tx, rx buffers
uint8_t tx_buf[RF_MAX_PAYLOAD_SIZE];
uint8_t rx_buf[RF_MAX_PAYLOAD_SIZE];

int main(void)
{
    nrk_setup_ports();
    nrk_setup_uart(UART_BAUDRATE_115K2);

    nrk_kprintf( PSTR("Starting up...\r\n") );
    
    nrk_gpio_clr(NRK_DEBUG_0);
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


void Task1()
{
    uint8_t i;
    uint8_t *local_rx_buf;
    uint8_t length,slot;
    int8_t rssi;
    nrk_status_t ret = NRK_OK;

    printf( "RX: pid %d\r\n", nrk_get_pid());

    rtl_init(RTL_COORDINATOR);
    nrk_kprintf( PSTR("RT-Link: RTL_COORDINATOR\r\n") );

    rtl_set_channel(15);
    ret |= rtl_set_schedule( RTL_TX, MY_TX_SLOT, 1 );
    ret |= rtl_set_schedule( RTL_RX, MY_RX_SLOT, 1 );
    if ( ret != NRK_OK ) {
        nrk_kprintf( PSTR("RT-Link: Error setting schedule") );
    }

//    rtl_set_contention( 8, 1 );
    rtl_start();
  
    rtl_rx_pkt_set_buffer(rx_buf, RF_MAX_PAYLOAD_SIZE);
 
    while(!rtl_ready()) {
        nrk_led_set(RED_LED);
        nrk_kprintf( PSTR("RT-LINK: waiting...\r\n" ));
        nrk_wait_until_next_period(); 
        nrk_led_clr(RED_LED);
    }

    while(!rtl_sync_status()) {
        nrk_led_set(RED_LED);
        nrk_kprintf( PSTR("RT-LINK: out-of-sync\r\n" ));
        nrk_wait_until_next_period(); 
        nrk_led_clr(RED_LED);
    }

    nrk_kprintf( PSTR("RT-LINK: ready\r\n" ));

    sprintf( &tx_buf[PKT_DATA_START], "Start");
    length = strlen( &tx_buf[PKT_DATA_START])+PKT_DATA_START;
    rtl_tx_pkt( tx_buf, length, MY_TX_SLOT );
    rtl_wait_until_tx_done( MY_TX_SLOT );

    while(1) {
        rtl_wait_until_rx_or_tx();
        nrk_led_set(GREEN_LED);
        local_rx_buf = rtl_rx_pkt_get(&length, &rssi, &slot);
        printf( "RX: slot %d, rssi %d, length %d: ", slot, rssi, length );
        for(i=PKT_DATA_START; i<length; i++ )
        {
            printf( "%c",local_rx_buf[i] );
        }
        nrk_kprintf( PSTR("\r\n") );
        rtl_rx_pkt_release();
        nrk_led_clr(GREEN_LED);
    }
}

void nrk_create_taskset()
{
    nrk_kprintf( PSTR("Creating Taskset: ") );

    TaskOne.task = Task1;
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

    nrk_kprintf( PSTR(" Done\r\n") );
}
