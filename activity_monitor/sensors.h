#ifndef _SENSORS_H_
#define _SENSORS_H_ 

#include <stdio.h>

typedef struct sensors_packet_t
{
    uint8_t adxl_x;
    uint8_t adxl_y;
    uint8_t adxl_z;
    uint8_t mic;
    uint8_t light;
    uint8_t temp;
    uint8_t bat;
} sensors_packet_t;

void sensors_task(void);
void sensors_read(sensors_packet_t*);

#endif // _SENSORS_H_
