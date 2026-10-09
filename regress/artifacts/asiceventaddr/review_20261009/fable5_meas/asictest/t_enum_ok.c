#include "dreamcast_sysasicvar.h"
enum { EV_LAST_LEGAL = 95 };
int main(void) { int a = SYSASIC_EVENT_TO_ADDR(EV_LAST_LEGAL); return a == 0x5f6908 ? 0 : 1; }
