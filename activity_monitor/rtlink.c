#include <stdio.h>
#include <nrk_error.h>
#include <rt_link.h>
#include "rtlink.h"

uint8_t tx_buf[MAX_RTL_PKT_SIZE];
uint8_t rx_buf[MAX_RTL_PKT_SIZE];

void rtlink_init(void)
{
    rtl_task_config();
}

void rtlink_task(void)
{
    int8_t rssi;
    uint8_t length, slot;
    uint8_t *local_rx_buf;

    _rtlink_setup();

    while(1) {
        nrk_gpio_toggle(NRK_DEBUG_1);
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

void _rtlink_setup(void) 
{
#ifdef COORDINATOR
    nrk_kprintf( PSTR( "rtl: Coordinator\r\n") ); 
    rtl_init(RTL_COORDINATOR);
    nrk_led_set(RED_LED);  
#else
    nrk_kprintf( PSTR( "rtl: Mobile\r\n") ); 
    rtl_init(RTL_MOBILE);
#endif

    printf( "rtl: TX %d  RX %d\r\n", RTL_TX_SLOT, RTL_RX_SLOT);

    rtl_set_channel(15);
    rtl_set_schedule( RTL_TX, RTL_TX_SLOT, 1 ); 
    rtl_set_schedule( RTL_RX, RTL_RX_SLOT, 1 ); 
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
}



