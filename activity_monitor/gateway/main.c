#include <nrk.h>
#include <include.h>
#include <ulib.h>
#include <stdio.h>
#include <avr/sleep.h>
#include <hal.h>
#include <slip.h>
#include "comm.h"

#define MAC_ADDR        0x0001

static void createTaskset(void);
static void comm_task(void);
static void slipstream_tx_task(void);
static void slipstream_rx_task(void);

// Task Stacks
NRK_STK Stack1[NRK_APP_STACKSIZE];
nrk_task_type TaskOne;

NRK_STK Stack2[NRK_APP_STACKSIZE];
nrk_task_type TaskTwo;

NRK_STK Stack3[NRK_APP_STACKSIZE];
nrk_task_type TaskThree;

// Semaphores
bool slipTxReady = false;
nrk_sem_t *slipTxSemaphore;

// Buffers
uint8_t comm_tx_buf[RF_MAX_PAYLOAD_SIZE];
uint8_t slip_rx_buf[RF_MAX_PAYLOAD_SIZE];
uint8_t slip_tx_buf[RF_MAX_PAYLOAD_SIZE];

int main(void)
{
    nrk_setup_ports();
    nrk_setup_uart(UART_BAUDRATE_115K2);

    nrk_kprintf( PSTR("Starting up...\r\n") );

    nrk_init();

    nrk_led_clr(ORANGE_LED);
    nrk_led_clr(GREEN_LED);
    nrk_led_clr(BLUE_LED);
    nrk_led_set(RED_LED);

    nrk_time_set(0,0);
    comm_init();
    createTaskset();

    slipTxSemaphore = nrk_sem_create(1,2);
    if( slipTxSemaphore==NULL ) {
        nrk_kprintf( PSTR("Error creating sem\r\n" ));
    }

    nrk_start();
  
    return 0;
}

static void comm_task(void)
{
    comm_setup(MAC_ADDR);
    comm_packet_t *pRxBuf;

    while(1) {
        nrk_gpio_toggle(NRK_DEBUG_0);

        pRxBuf = comm_rx();
        if (pRxBuf != NULL) {
            nrk_sem_pend(slipTxSemaphore);
            sprintf( slip_tx_buf, "%d %s", pRxBuf->addr, pRxBuf->payload );
            slipTxReady = true;
            nrk_sem_post(slipTxSemaphore);

            comm_printPacket(pRxBuf);
            comm_rxCleanup(pRxBuf);
        }
    }
}

static void slipstream_tx_task() {
    slip_init(stdin, stdout, 0, 0);
    while( !slip_started () ) {
        nrk_kprintf( PSTR("slipstream: waiting slip to start\r\n") );
        nrk_wait_until_next_period ();
    }

    while(1) {
        nrk_gpio_toggle(NRK_DEBUG_1);

        nrk_sem_pend(slipTxSemaphore);
        if (slipTxReady) {
            slip_tx (slip_tx_buf, strlen(slip_tx_buf));
            memset( &slip_tx_buf, 0, RF_MAX_PAYLOAD_SIZE );
            slipTxReady = false;
        }
        nrk_sem_post(slipTxSemaphore);

        nrk_wait_until_next_period();
    }
}

static void slipstream_rx_task() {
    while( !slip_started () ) {
        nrk_kprintf( PSTR("slipstream: waiting slip to start\r\n") );
        nrk_wait_until_next_period ();
    }

    while(1) {
        nrk_gpio_toggle(NRK_DEBUG_2);

        // blocks until slip message received
        int8_t v = slip_rx(slip_rx_buf, RF_MAX_PAYLOAD_SIZE);
        if (v > 0) {
            nrk_kprintf (PSTR ("slipstream: "));
            for (uint8_t i = 0; i < v; i++)
                printf ("%c", slip_rx_buf[i]);
        }
    }  
}

static void createTaskset(void)
{
    nrk_kprintf ( PSTR("taskset: creating comm\r\n") );
    TaskOne.task = comm_task;
    nrk_task_set_stk( &TaskOne, Stack1, NRK_APP_STACKSIZE);
    TaskOne.prio = 3;
    TaskOne.FirstActivation = TRUE;
    TaskOne.Type = BASIC_TASK;
    TaskOne.SchType = PREEMPTIVE;
    TaskOne.period.secs = 0;
    TaskOne.period.nano_secs = 200 * NANOS_PER_MS;
    TaskOne.cpu_reserve.secs = 0;
    TaskOne.cpu_reserve.nano_secs = 0;
    TaskOne.offset.secs = 0;
    TaskOne.offset.nano_secs= 0;
    nrk_activate_task (&TaskOne);

    TaskTwo.task = slipstream_tx_task;
    nrk_task_set_stk( &TaskTwo, Stack2, NRK_APP_STACKSIZE);
    TaskTwo.prio = 2;
    TaskTwo.FirstActivation = TRUE;
    TaskTwo.Type = BASIC_TASK;
    TaskTwo.SchType = PREEMPTIVE;
    TaskTwo.period.secs = 0;
    TaskTwo.period.nano_secs = 200 * NANOS_PER_MS;
    TaskTwo.cpu_reserve.secs = 0;
    TaskTwo.cpu_reserve.nano_secs = 0;
    TaskTwo.offset.secs = 0;
    TaskTwo.offset.nano_secs = 0;
    nrk_activate_task (&TaskTwo);

    TaskThree.task = slipstream_rx_task;
    nrk_task_set_stk( &TaskThree, Stack3, NRK_APP_STACKSIZE);
    TaskThree.prio = 3;
    TaskThree.FirstActivation = TRUE;
    TaskThree.Type = BASIC_TASK;
    TaskThree.SchType = PREEMPTIVE;
    TaskThree.period.secs = 1;
    TaskThree.period.nano_secs = 0;
    TaskThree.cpu_reserve.secs = 0;
    TaskThree.cpu_reserve.nano_secs = 0;
    TaskThree.offset.secs = 0;
    TaskThree.offset.nano_secs = 0;
    nrk_activate_task (&TaskThree);
}

