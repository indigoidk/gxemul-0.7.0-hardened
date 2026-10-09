#include "dreamcast_sysasicvar.h"
enum { EV_FIRST_ILLEGAL = 96 };
int main(void) { int a = SYSASIC_EVENT_TO_ADDR(EV_FIRST_ILLEGAL); return a; }
