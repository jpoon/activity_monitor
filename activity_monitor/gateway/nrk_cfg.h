/***************************************************************
*                            NanoRK CONFIG                     *
***************************************************************/
#ifndef __nrk_cfg_h	
#define __nrk_cfg_h

#define NRK_REPORT_ERRORS

#define NRK_HALT_AND_LOOP_ON_ERROR
//#define NRK_HALT_ON_ERROR

#define IGNORE_BROWN_OUT_ERROR
#define IGNORE_EXT_RST_ERROR
#define NRK_NO_POWER_DOWN

#define NRK_STATS_TRACKER

#define NRK_STACK_CHECK

#define NRK_MAX_TASKS                   5

#define SLIP_PCP_CEILING		        18	

// Enable buffered and signal controlled serial RX
#define NRK_UART_BUF                    1
// Set buffer to MAX slip packet size
#define MAX_RX_UART_BUF                 128 

#define NRK_MAX_RESOURCE_CNT            4

#define NRK_MAX_DRIVER_CNT              1    

#define NRK_TASK_IDLE_STK_SIZE          128 // Idle task stack size min=32 
#define NRK_APP_STACKSIZE               256
#define NRK_KERNEL_STACKSIZE            128 

// Radio can interact with battery voltage monitoring
#define RADIO_PRIORITY_CEILING          20

#endif
