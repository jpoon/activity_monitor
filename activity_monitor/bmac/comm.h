#ifndef _COMM_H_
#define _COMM_H_ 

#define COMM_CHANNEL    25

#define COMM_BROADCAST  0xFFFF

typedef struct comm_packet_t {
    uint8_t payload[RF_MAX_PAYLOAD_SIZE];
    uint8_t len;
    int8_t rssi;
} comm_packet_t;

void comm_init(void);
void comm_setup(uint16_t addr);
comm_packet_t* comm_rx(void);
void comm_tx(uint16_t, uint8_t *, uint8_t);
void comm_rxCleanup(comm_packet_t *);
void comm_printPacket(const comm_packet_t *);

#endif // _COMM_H_
