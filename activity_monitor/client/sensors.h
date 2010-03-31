#ifndef _SENSORS_H_
#define _SENSORS_H_ 

#include <stdio.h>

typedef struct sensors_packet_t
{
    uint16_t adxl_x;
    uint16_t adxl_y;
    uint16_t adxl_z;
    uint16_t mic;
    uint16_t light;
    uint16_t temp;
    uint16_t bat;
} sensors_packet_t;

void sensors_register_drivers(void);
void sensors_read(sensors_packet_t*);
void sensors_print(const sensors_packet_t*);

#endif // _SENSORS_H_
