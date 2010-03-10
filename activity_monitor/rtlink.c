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

void rtlink_setup(void) 
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

void rtlink_rx(rtlink_packet_t *pkt) {
    if( rtl_rx_pkt_check()!=0 ) {
        nrk_led_set(GREEN_LED);
        pkt->payload = rtl_rx_pkt_get(&pkt->len, &pkt->rssi, &pkt->slot);
   }
}

void rtlink_rx_cleanup(rtlink_packet_t *pkt) {
    pkt->payload = NULL;
    pkt->len = 0;
    pkt->rssi = 0;
    pkt->slot = 0;
    rtl_rx_pkt_release();
    nrk_led_clr(GREEN_LED);
}

void rtlink_print_packet(const rtlink_packet_t *pkt) {
    printf( "rtl: rx slot %d, rssi %d, length %d: ", 
        pkt->slot, pkt->rssi, pkt->len );
    for(uint8_t i=PKT_DATA_START; i<pkt->len; i++ ) {
        printf( "%c",pkt->payload[i] );
    }
    nrk_kprintf( PSTR("\r\n") );
}
