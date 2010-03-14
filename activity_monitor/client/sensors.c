#include <nrk.h>
#include <ff_basic_sensor.h>
#include <nrk_driver_list.h>
#include <nrk_driver.h>
#include <nrk_error.h>
#include "sensors.h"

sensors_packet_t sensor_buf;

void _sensors_print(const sensors_packet_t *);

void sensors_register_drivers(void)
{
    int8_t val;

    val = nrk_register_driver( &dev_manager_ff_sensors,FIREFLY_SENSOR_BASIC);
    if( val == NRK_ERROR ) {
        nrk_kprintf( PSTR("sensors: failed to load ADC driver\r\n") );
    } else {
        nrk_kprintf( PSTR("sensors: loaded ADC drivers successfully\r\n") );
    }
}

void sensors_read(sensors_packet_t *pkt)
{
    int8_t val, fd;

    fd = nrk_open(FIREFLY_SENSOR_BASIC, READ);
    if( fd == NRK_ERROR ) {
        nrk_kprintf( PSTR("sensors: failed to open sensor driver\r\n"));
    } else {
        val = nrk_set_status(fd, SENSOR_SELECT, BAT);
        val = nrk_read(fd, &(pkt->bat), 2);
        val = nrk_set_status(fd, SENSOR_SELECT, LIGHT);
        val = nrk_read(fd, &(pkt->light), 2);
        val = nrk_set_status(fd, SENSOR_SELECT, TEMP);
        val = nrk_read(fd, &(pkt->temp), 2);
        val = nrk_set_status(fd, SENSOR_SELECT, AUDIO);
        val = nrk_read(fd, &(pkt->mic), 2);
        val = nrk_set_status(fd, SENSOR_SELECT, ACC_X);
        val = nrk_read(fd, &(pkt->adxl_x), 2);
        val = nrk_set_status(fd, SENSOR_SELECT, ACC_Y);
        val = nrk_read(fd, &(pkt->adxl_y), 2);
        val = nrk_set_status(fd,SENSOR_SELECT, ACC_Z);
        val = nrk_read(fd, &pkt->adxl_z, 2);

        _sensors_print(pkt);
    }
    nrk_close(fd);
}

void _sensors_print(const sensors_packet_t *pPkt) {
    printf("Sensor Packet: bat=%d, temp=%d, light=%d, mic=%d, acc_x=%d, acc_y=%d, acc_z=%d\r\n", pPkt->bat, pPkt->temp, pPkt->light, pPkt->mic, pPkt->adxl_x, pPkt->adxl_y, pPkt->adxl_z);
}
