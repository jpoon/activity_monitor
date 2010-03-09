#ifndef _RTLINK_H_
#define _RTLINK_H_ 

#define NODE_ID	    1

#if NODE_ID == 1
	#define RTL_TX_SLOT  6
	#define RTL_RX_SLOT  8
    #define COORDINATOR
#elif NODE_ID == 2
	#define RTL_TX_SLOT  8
	#define RTL_RX_SLOT  6
#else
    #error Invalid Node ID
#endif

void rtlink_setup(void);
void rtlink_task(void);

#endif // _RTLINK_H_
