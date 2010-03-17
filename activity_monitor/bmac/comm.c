#include <stdio.h>
#include <nrk_error.h>
#include <bmac.h>
#include <comm.h>

static comm_packet_t rx_buf;

void comm_init(void)
{
    bmac_task_config();
}

void comm_setup(uint16_t addr) 
{
    bmac_init(COMM_CHANNEL);

    bmac_addr_decode_set_my_mac(addr);
    bmac_addr_decode_enable();
    bmac_auto_ack_enable();

    bmac_rx_pkt_set_buffer(rx_buf.payload, RF_MAX_PAYLOAD_SIZE);

    while(!bmac_started()) {
        nrk_kprintf( PSTR("comm: waiting for bmac to start\r\n") );
        nrk_wait_until_next_period();
    }

    nrk_kprintf( PSTR("comm: ready\r\n") );
}

comm_packet_t* comm_rx(void) {
    if( bmac_rx_pkt_ready()==0 ) 
        bmac_wait_until_rx_pkt();

    nrk_led_set(GREEN_LED);
    bmac_rx_pkt_get(&rx_buf.len, &rx_buf.rssi);
    return &rx_buf;
}

void comm_rxCleanup(comm_packet_t *pkt) {
    bmac_rx_pkt_release();
    memset(pkt->payload, 0, RF_MAX_PAYLOAD_SIZE); 
    pkt->len = 0;
    pkt->rssi = 0;
    nrk_led_clr(GREEN_LED);
}

void comm_tx(uint16_t dst, uint8_t *pPayload, uint8_t len) {
    int8_t err;
    nrk_led_set(GREEN_LED);

    bmac_addr_decode_dest_mac(dst);
    err = bmac_tx_pkt( pPayload, len+1 );

    if (err == NRK_ERROR) {
        // possibly do some power optimization here
        printf( "comm: tx packet -- no ack\r\n" );
    } else {
        printf( "comm: tx packet -- acked\r\n" );
    }

    // block until sent
    nrk_led_clr(GREEN_LED);
}

void comm_printPacket(const comm_packet_t *pkt) {
    if (pkt->len > 0) {
        printf( "comm: len %d, rssi %d -- ", pkt->len, pkt->rssi);

        for(uint8_t i=0; i < pkt->len; i++ ) {
            printf( "%c", pkt->payload[i] );
        }
        nrk_kprintf( PSTR("\r\n") );
    }     
}
