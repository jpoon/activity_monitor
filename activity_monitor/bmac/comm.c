#include <stdio.h>
#include <nrk_error.h>
#include <bmac.h>
#include <comm.h>

static comm_packet_t rx_buf;
static uint16_t mac_addr;

void comm_init(void)
{
    bmac_task_config();
}

void comm_setup(uint16_t addr) 
{
    mac_addr = addr;

    bmac_init(COMM_CHANNEL);

    bmac_addr_decode_set_my_mac(mac_addr);
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

    rx_buf.addr |= (rx_buf.payload[0] & 0xFF) << 8;
    rx_buf.addr |= rx_buf.payload[1] & 0xFF;
    for (uint8_t i = 0; i <= rx_buf.len; i++) {
        rx_buf.payload[i] = rx_buf.payload[i+sizeof(rx_buf.addr)];
    }
    rx_buf.len = rx_buf.len - sizeof(rx_buf.addr);

    return &rx_buf;
}

void comm_rxCleanup(comm_packet_t *pkt) {
    bmac_rx_pkt_release();
    memset(pkt->payload, 0, RF_MAX_PAYLOAD_SIZE); 
    pkt->len = 0;
    pkt->rssi = 0;
    pkt->addr = 0;
    nrk_led_clr(GREEN_LED);
}

/*
 * block until sent
 */
void comm_tx(comm_packet_t *pkt) {
    int8_t err;
    nrk_led_set(GREEN_LED);

    bmac_addr_decode_dest_mac(pkt->addr);

    for (int8_t i = pkt->len; i >= 0; i--) {
        pkt->payload[i+2] = pkt->payload[i];
    }
    pkt->payload[0] = (mac_addr >> 8) & 0xFF;
    pkt->payload[1] = mac_addr & 0xFF;
    pkt->len += sizeof(pkt->addr);

    err = bmac_tx_pkt( pkt->payload, pkt->len );
    if (err == NRK_ERROR) {
        // possibly do some power optimization here
        printf( "comm: tx packet -- no ack\r\n" );
    } else {
        printf( "comm: tx packet -- acked\r\n" );
    }

    nrk_led_clr(GREEN_LED);
}

void comm_printPacket(const comm_packet_t *pkt) {
    if (pkt->len > 0) {
        printf( "comm: addr %d rssi %d -- ", pkt->addr, pkt->rssi);

        for(uint8_t i=0; i < pkt->len; i++ ) {
            printf( "%c", pkt->payload[i] );
        }
        nrk_kprintf( PSTR("\r\n") );
    }     
}
