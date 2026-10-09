#include "dreamcast_sysasicvar.h"
#define SYSASIC_EVENT_FOO 96
int main(void) { int a = SYSASIC_EVENT_TO_ADDR(SYSASIC_EVENT_FOO); return a; }
