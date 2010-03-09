#ifndef _SENSORS_H_
#define _SENSORS_H_ 

#include <stdio.h>

typedef struct ff_sensor_packet
{
    uint16_t adxl_x;
    uint16_t adxl_y;
    uint16_t adxl_z;
    uint16_t mic;
    uint16_t light;
    uint16_t temp;
    uint16_t bat;
} ff_sensor_packet;

void ff_register_drivers(void);

#endif // _SENSORS_H_
