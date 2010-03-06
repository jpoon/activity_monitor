#include <nrk.h>
#include <include.h>
#include <ulib.h>
#include <stdio.h>
#include <avr/sleep.h>
#include <hal.h>
#include <rt_link.h>
#include <nrk_error.h>
#include <nrk_timer.h>
#include <nrk_driver_list.h>
#include <nrk_driver.h>
#include <ff_basic_sensor.h>

#define MY_TX_SLOT  8
#define MY_RX_SLOT  0

NRK_STK Stack1[NRK_APP_STACKSIZE];
nrk_task_type TaskOne;
void tx_handler(void);

void nrk_create_taskset();
void nrk_register_drivers();

// tx, rx buffers
uint8_t tx_buf[MAX_RTL_PKT_SIZE];
uint8_t rx_buf[MAX_RTL_PKT_SIZE];

int main(void)
{
    nrk_setup_ports();
    nrk_setup_uart(UART_BAUDRATE_115K2);

    nrk_kprintf( PSTR("Starting up...\r\n") );

    nrk_init();

    nrk_led_clr(ORANGE_LED);
    nrk_led_clr(GREEN_LED);
    nrk_led_clr(RED_LED);
    nrk_led_clr(BLUE_LED);

    nrk_time_set(0,0);
    rtl_task_config();
    nrk_register_drivers();
    nrk_create_taskset();
    nrk_start();
  
    return 0;
}

void tx_handler()
{
    uint8_t fd, val;
    uint8_t *local_rx_buf;
    uint8_t cnt = 0;
    uint8_t length;
    uint8_t adxl_x, adxl_y, adxl_z, mic, light, temp, bat;

    printf( "TX: pid %d\r\n", nrk_get_pid());

    nrk_kprintf( PSTR("RT-Link: RTL_MOBILE\r\n") );
    rtl_init(RTL_MOBILE);
    rtl_set_channel(15);
    rtl_set_schedule( RTL_TX, MY_TX_SLOT, 1 ); 
    rtl_set_schedule( RTL_RX, MY_RX_SLOT, 1 ); 
//    rtl_set_contention( 8,1 );
    rtl_start();
  
    rtl_rx_pkt_set_buffer(rx_buf, RF_MAX_PAYLOAD_SIZE);

    while(!rtl_ready()) {
        nrk_led_set(RED_LED);
        nrk_kprintf( PSTR("RT-Link: waiting...\r\n") );
        nrk_wait_until_next_period();
        nrk_led_clr(RED_LED);
    }

    while(!rtl_sync_status()) {
        nrk_led_set(RED_LED);
        nrk_kprintf( PSTR("RT-Link: out-of-sync\r\n") );
        nrk_wait_until_next_period();
        nrk_led_clr(RED_LED);
    }

    nrk_kprintf( PSTR("RT-Link: ready\r\n") );

    while(1) {
        if(!rtl_sync_status()) {
            nrk_led_set(RED_LED);
        } else {
            nrk_led_clr(RED_LED);
        }


        if( rtl_tx_pkt_check( MY_TX_SLOT ) != 0 ) {
            nrk_kprintf( PSTR("TX: pending packet on slot ") );
            printf( "%d\r\n", MY_TX_SLOT );
        } else {
            // Open ADC device as read 
            fd = nrk_open(FIREFLY_SENSOR_BASIC,READ);
            if( fd==NRK_ERROR ) {
                nrk_kprintf( PSTR("Sensors: Failed to open sensor driver\r\n"));
            }

            val=nrk_set_status(fd,SENSOR_SELECT,BAT);
            val=nrk_read(fd,&bat,2);
            val=nrk_set_status(fd,SENSOR_SELECT,LIGHT);
            val=nrk_read(fd,&light,2);
            val=nrk_set_status(fd,SENSOR_SELECT,TEMP);
            val=nrk_read(fd,&temp,2);
            val=nrk_set_status(fd,SENSOR_SELECT,AUDIO);
            val=nrk_read(fd,&mic,2);
            val=nrk_set_status(fd,SENSOR_SELECT,ACC_X);
            val=nrk_read(fd,&adxl_x,2);
            val=nrk_set_status(fd,SENSOR_SELECT,ACC_Y);
            val=nrk_read(fd,&adxl_y,2);
            val=nrk_set_status(fd,SENSOR_SELECT,ACC_Z);
            val=nrk_read(fd,&adxl_z,2);

            nrk_close(fd);

            // Build a sensor packet
            sprintf (tx_buf, "bat=%d light=%d temp=%d accel=%d %d %d %d\r\n", bat, light, temp, mic, adxl_x, adxl_y, adxl_z);
 
            nrk_kprintf( PSTR("TX: sending packet on slot "));
            printf( "%d\r\n", MY_TX_SLOT );

            nrk_led_set(GREEN_LED);
            length = strlen(tx_buf);
            rtl_tx_pkt( tx_buf, length, MY_TX_SLOT );
            rtl_wait_until_rx_or_tx();
            nrk_led_clr(GREEN_LED);

            nrk_wait_until_next_period();
        }
    }
}

void nrk_create_taskset()
{
    nrk_kprintf ( PSTR("Creating Taskset: ") );

    TaskOne.task = tx_handler;
    nrk_task_set_stk( &TaskOne, Stack1, NRK_APP_STACKSIZE);
    TaskOne.prio = 1;
    TaskOne.FirstActivation = TRUE;
    TaskOne.Type = BASIC_TASK;
    TaskOne.SchType = PREEMPTIVE;
    TaskOne.period.secs = 5;
    TaskOne.period.nano_secs = 100*NANOS_PER_MS;
    TaskOne.cpu_reserve.secs = 1;
    TaskOne.cpu_reserve.nano_secs = 50*NANOS_PER_MS;
    TaskOne.offset.secs = 0;
    TaskOne.offset.nano_secs= 0;
    nrk_activate_task (&TaskOne);

    nrk_kprintf ( PSTR("Done\r\n") );
}

void nrk_register_drivers()
{
    int8_t val;

// Register the Basic FireFly Sensor device driver
// Make sure to add: 
//     #define NRK_MAX_DRIVER_CNT  
//     in nrk_cfg.h
// Make sure to add: 
//     SRC += $(ROOT_DIR)/src/drivers/platform/$(PLATFORM_TYPE)/source/ff_basic_sensor.c
//     in makefile
    val = nrk_register_driver( &dev_manager_ff_sensors,FIREFLY_SENSOR_BASIC);
    if( val==NRK_ERROR ) {
        nrk_kprintf( PSTR("Drivers: Failed to load ADC driver\r\n") );
    } else {
        nrk_kprintf( PSTR("Drivers: Loaded Successfully\r\n") );
    }
}
