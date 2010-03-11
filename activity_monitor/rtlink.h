#ifndef _RTLINK_H_
#define _RTLINK_H_ 

#include <rt_link.h>

#define NODE_ID	    1

#if NODE_ID == 1
	#define RTL_TX_SLOT  6
	#define RTL_RX_SLOT  8
    #define COORDINATOR
#elif NODE_ID == 2
	#define RTL_TX_SLOT  8
	#define RTL_RX_SLOT  6
#else
    #error Invalid Node ID
#endif

typedef struct rtlink_packet_t {
    uint8_t payload[MAX_RTL_PKT_SIZE];
    uint8_t len;
    int8_t rssi;
    uint8_t slot;
} rtlink_packet_t;

void rtlink_init(void);
void rtlink_setup(void);
rtlink_packet_t* rtlink_rx(void);
void rtlink_tx(rtlink_packet_t *);
void rtlink_rx_cleanup(rtlink_packet_t *);
void rtlink_print_packet(const rtlink_packet_t *);
#endif // _RTLINK_H_
