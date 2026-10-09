#include "dreamcast_sysasicvar.h"
int main(void) { int a = SYSASIC_EVENT_TO_ADDR(95); int b = SYSASIC_EVENT_TO_ADDR(0);
  return (a == 0x5f6908 && b == 0x5f6900) ? 0 : 1; }
