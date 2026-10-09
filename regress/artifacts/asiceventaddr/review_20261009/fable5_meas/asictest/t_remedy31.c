#include <stdint.h>
#include "dreamcast_sysasicvar.h"
#define BITMASK_WITH_RANGE_OK(e) ((1 << ((e) & 31)) + SYSASIC_EVENT_RANGE_OK(e))
int main(void) { uint64_t t = BITMASK_WITH_RANGE_OK(31); return (int)(t & 1); }
