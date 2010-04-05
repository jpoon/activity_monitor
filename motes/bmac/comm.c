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

    // initializes bmac on a specific radio channel
    bmac_init(COMM_CHANNEL);

    bmac_addr_decode_disable();
    bmac_auto_ack_disable();

    bmac_rx_pkt_set_buffer(rx_buf.payload, RF_MAX_PAYLOAD_SIZE);

    while(!bmac_started()) {
        nrk_kprintf( PSTR("comm: waiting for bmac to start\r\n") );
        nrk_wait_until_next_period();
    }

    nrk_kprintf( PSTR("comm: ready\r\n") );
}

comm_packet_t* comm_rx(void) {
    // blocking read
    if( bmac_rx_pkt_ready()==0 ) 
        bmac_wait_until_rx_pkt();

    nrk_led_set(ORANGE_LED);
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
    nrk_led_clr(ORANGE_LED);
}

// blocks until sent
int8_t comm_tx(comm_packet_t *pkt) {
    int8_t err;
    nrk_led_set(ORANGE_LED);

    // shift array
    for (int8_t i = pkt->len; i >= 0; i--) {
        pkt->payload[i+2] = pkt->payload[i];
    }
    pkt->payload[0] = (mac_addr >> 8) & 0xFF;
    pkt->payload[1] = mac_addr & 0xFF;
    pkt->len += sizeof(pkt->addr);

    // blocks until sent
    err = bmac_tx_pkt( pkt->payload, pkt->len );

    nrk_led_clr(ORANGE_LED);
    return err;
}

void comm_printPacket(const comm_packet_t *pkt) {
    if (pkt->len > 0) {

        nrk_kprintf( PSTR("comm: ") );
        printf( "addr=%d rssi=%d contents=[ ", pkt->addr, pkt->rssi );

        for(uint8_t i=0; i < pkt->len; i++ ) {
            printf( "%c", pkt->payload[i] );
        }
        nrk_kprintf( PSTR(" ]\r\n") );
    }     
}
