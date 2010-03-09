#include <nrk.h>
#include <include.h>
#include <ulib.h>
#include <stdio.h>
#include <avr/sleep.h>
#include <hal.h>
#include <nrk_error.h>
#include <nrk_timer.h>
#include "sensors.h"
#include "rtlink.h"

NRK_STK Stack1[NRK_APP_STACKSIZE];
nrk_task_type TaskOne;

NRK_STK Stack2[NRK_APP_STACKSIZE];
nrk_task_type TaskTwo;

void nrk_create_taskset();

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
    rtlink_init();
    nrk_create_taskset();
    nrk_start();
  
    return 0;
}
/*
void sensor_task()
{
    ff_register_drivers();
    while(1) {
      printf( "sensor task\r\n");
      nrk_wait_until_next_period();
    }
//    ff_read_sensors();
}
*/
void nrk_create_taskset()
{
    nrk_kprintf ( PSTR("Creating Taskset: ") );

    TaskOne.task = rtlink_task;
    TaskOne.Ptos = (void *) &Stack1[NRK_APP_STACKSIZE-1];
    TaskOne.Pbos = (void *) &Stack1[0];
    TaskOne.prio = 2;
    TaskOne.FirstActivation = TRUE;
    TaskOne.Type = BASIC_TASK;
    TaskOne.SchType = PREEMPTIVE;
    TaskOne.period.secs = 1;
    TaskOne.period.nano_secs = 0;
    TaskOne.cpu_reserve.secs = 0;
    TaskOne.cpu_reserve.nano_secs = 100*NANOS_PER_MS;
    TaskOne.offset.secs = 0;
    TaskOne.offset.nano_secs= 0;
    nrk_activate_task (&TaskOne);
/*
    TaskTwo.task = sensor_task;
    nrk_task_set_stk( &TaskTwo, Stack2, NRK_APP_STACKSIZE);
    TaskTwo.prio = 3;
    TaskTwo.FirstActivation = TRUE;
    TaskTwo.Type = BASIC_TASK;
    TaskTwo.SchType = PREEMPTIVE;
    TaskTwo.period.secs = 5;
    TaskTwo.period.nano_secs = 0;
    TaskTwo.cpu_reserve.secs = 0;
    TaskTwo.cpu_reserve.nano_secs = 0;
    TaskTwo.offset.secs = 0;
    TaskTwo.offset.nano_secs= 0;
    nrk_activate_task (&TaskTwo);
*/
    nrk_kprintf ( PSTR("Done\r\n") );
}

