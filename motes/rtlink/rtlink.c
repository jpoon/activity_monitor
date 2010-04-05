#include <stdio.h>
#include <nrk_error.h>
#include "rtlink.h"

rtlink_packet_t rtlink_rx_buf;
void _print_packet(const rtlink_packet_t *);

uint8_t RTL_RX_SLOT;
uint8_t RTL_TX_SLOT;

void rtlink_init(void)
{
    rtl_task_config();
}

void rtlink_setup(rtl_node_mode_t type, uint8_t tx_slot, uint8_t rx_slot) 
{
    if (type == RTL_COORDINATOR) {
        nrk_kprintf( PSTR( "rtl: Coordinator\r\n") ); 
        rtl_init(RTL_COORDINATOR);
        nrk_led_set(RED_LED);  
    } else {
        nrk_kprintf( PSTR( "rtl: Mobile\r\n") ); 
        rtl_init(RTL_MOBILE);
    }

    RTL_RX_SLOT = rx_slot;
    RTL_TX_SLOT = tx_slot;

    printf( "rtl: TX %d  RX %d\r\n", RTL_TX_SLOT, RTL_RX_SLOT);

    rtl_set_channel(15);
    rtl_set_schedule( RTL_TX, RTL_TX_SLOT, 1 ); 
    rtl_set_schedule( RTL_RX, RTL_RX_SLOT, 1 ); 

    rtl_rx_pkt_set_buffer(rtlink_rx_buf.payload, RF_MAX_PAYLOAD_SIZE);

    rtl_start();

    while(!rtl_ready()) {
        nrk_kprintf( PSTR("rtl: waiting for rtl to be ready\r\n") );
        nrk_wait_until_next_period();
    }
    while(!rtl_sync_status()) {
        nrk_kprintf( PSTR("rtl: out of sync\r\n") );
        nrk_wait_until_next_period();
    }

    nrk_kprintf( PSTR("rtl: ready\r\n") );
}

rtlink_packet_t* rtlink_rx(void) {
    if( rtl_rx_pkt_check()!=0 ) {
        nrk_led_set(GREEN_LED);
        rtl_rx_pkt_get(&rtlink_rx_buf.len, &rtlink_rx_buf.rssi, &rtlink_rx_buf.slot);
        return &rtlink_rx_buf;
    }
    return NULL; 
}

void rtlink_rx_cleanup(rtlink_packet_t *pkt) {
    rtl_rx_pkt_release();
    memset(pkt->payload, 0, MAX_RTL_PKT_SIZE); 
    pkt->len = 0;
    pkt->rssi = 0;
    pkt->slot = 0;
    nrk_led_clr(GREEN_LED);
}

void rtlink_tx(uint8_t *pPayload, uint8_t len) {
    nrk_led_set(GREEN_LED);

    // first couple slots of buffer reserved
    for(uint8_t i = len; i > 0; i--) {
        *(pPayload+i+PKT_DATA_START-1) = *(pPayload+i-1);
    }

    rtl_tx_pkt( pPayload, len+PKT_DATA_START, RTL_TX_SLOT );
    printf( "rtl: tx packet on slot %d\r\n",RTL_TX_SLOT );

    // block until sent
    rtl_wait_until_tx_done( RTL_TX_SLOT );
    nrk_led_clr(GREEN_LED);
}

void rtlink_print_packet(const rtlink_packet_t *pkt) {
    if (pkt->len > 0) {
        printf( "rtl: slot %d, len %d, rssi %d -- ", pkt->slot, pkt->len, pkt->rssi);

        for(uint8_t i=PKT_DATA_START; i < pkt->len; i++ ) {
            printf( "%c", pkt->payload[i] );
        }
 
        nrk_kprintf( PSTR("\r\n") );
    }     
}
