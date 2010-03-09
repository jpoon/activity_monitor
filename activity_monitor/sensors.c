#include <ff_basic_sensor.h>
#include <nrk_driver_list.h>
#include <nrk_driver.h>
#include <nrk_error.h>
#include "sensors.h"

void ff_register_drivers(void)
{
    int8_t val;

    val = nrk_register_driver( &dev_manager_ff_sensors,FIREFLY_SENSOR_BASIC);
    if( val == NRK_ERROR ) {
        nrk_kprintf( PSTR("Sensors: Failed to load ADC driver\r\n") );
    } else {
        nrk_kprintf( PSTR("Sensors: Loaded Successfully\r\n") );
    }
}

void ff_read_sensors(ff_sensor_packet *pkt)
{
    uint8_t fd, val;

    // Open ADC device as read 
    fd = nrk_open(FIREFLY_SENSOR_BASIC, READ);
    if( fd==NRK_ERROR ) {
        nrk_kprintf( PSTR("Sensors: Failed to open sensor driver\r\n"));
    }

    val = nrk_set_status(fd,SENSOR_SELECT, BAT);
    val = nrk_read(fd, &pkt->bat, 2);
    val = nrk_set_status(fd, SENSOR_SELECT, LIGHT);
    val = nrk_read(fd, &pkt->light, 2);
    val = nrk_set_status(fd, SENSOR_SELECT, TEMP);
    val = nrk_read(fd, &pkt->temp, 2);
    val = nrk_set_status(fd, SENSOR_SELECT, AUDIO);
    val = nrk_read(fd, &pkt->mic, 2);
    val = nrk_set_status(fd, SENSOR_SELECT, ACC_X);
    val = nrk_read(fd, &pkt->adxl_x, 2);
    val = nrk_set_status(fd,SENSOR_SELECT, ACC_Y);
    val = nrk_read(fd, &pkt->adxl_y, 2);
    val = nrk_set_status(fd,SENSOR_SELECT, ACC_Z);
    val = nrk_read(fd, &pkt->adxl_z, 2);

    nrk_close(fd);
}

