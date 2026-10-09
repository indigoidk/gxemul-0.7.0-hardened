#include <stdio.h>
#include <stdint.h>
#include "dreamcast_sysasicvar.h"
int main(int argc, char **argv) {
  volatile int k = 31; (void)argv; if (argc > 5) k = 0;
  uint64_t c = SYSASIC_EVENT_TO_BITMASK(31);            /* constant e, the shipped macro */
  uint64_t v = (1 << ((k) & 31));                       /* same expression, non-constant e */
  uint64_t u = (1U << ((k) & 31));                      /* the one-token repair */
  c |= 0x100000000ULL; v |= 0x100000000ULL; u |= 0x100000000ULL;
  printf("tmp2 shipped(const 31)=0x%016llx  shipped(volatile 31)=0x%016llx  1U-form=0x%016llx  low32: 0x%08x 0x%08x 0x%08x\n",
    (unsigned long long)c, (unsigned long long)v, (unsigned long long)u, (unsigned)c, (unsigned)v, (unsigned)u);
  return 0;
}
