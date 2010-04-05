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

#define NRK_STATS_TRACKER

#define NRK_STACK_CHECK

#define NRK_MAX_TASKS                   4

#define NRK_MAX_RESOURCE_CNT            3

#define NRK_MAX_DRIVER_CNT              1    

//#define	NRK_N_RES                       0

#define NRK_TASK_IDLE_STK_SIZE          128 // Idle task stack size min=32 
#define NRK_APP_STACKSIZE               256
#define NRK_KERNEL_STACKSIZE            128 

// Radio can interact with battery voltage monitoring
#define RADIO_PRIORITY_CEILING          20

#endif
