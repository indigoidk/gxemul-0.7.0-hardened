#include <stdint.h>
#include "dreamcast_sysasicvar.h"
int main() { uint64_t a = SYSASIC_EVENT_TO_ADDR(95); return (int)(a & 1); }
