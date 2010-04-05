#ifndef _RTLINK_H_
#define _RTLINK_H_ 

#include <rt_link.h>

#define RTL_MAX_BUF_SIZE (MAX_RTL_PKT_SIZE-PKT_DATA_START)

typedef struct rtlink_packet_t {
    uint8_t payload[MAX_RTL_PKT_SIZE];
    uint8_t len;
    int8_t rssi;
    uint8_t slot;
} rtlink_packet_t;

void rtlink_init(void);
void rtlink_setup(rtl_node_mode_t type, uint8_t tx_slot, uint8_t rx_slot);
rtlink_packet_t* rtlink_rx(void);
void rtlink_tx(uint8_t *, uint8_t);
void rtlink_rx_cleanup(rtlink_packet_t *);
void rtlink_print_packet(const rtlink_packet_t *);

#endif // _RTLINK_H_
