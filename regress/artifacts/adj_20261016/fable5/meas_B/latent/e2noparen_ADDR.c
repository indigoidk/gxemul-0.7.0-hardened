#include <stdint.h>
#include <stddef.h>
struct memory; struct cpu { struct memory *mem; int (*memory_rw)(struct cpu *, struct memory *, uint64_t, unsigned char *, size_t, int, int); };
#define MEM_WRITE 1
#define PHYSICAL 32
void memory_writemax64(struct cpu *cpu, unsigned char *buf, int len, uint64_t data);
#include "thirdparty/dreamcast_sysasicvar.h"
unsigned long f(void); unsigned long f(void) { return SYSASIC_EVENT_TO_ADDR(1 ? 200 : 5); }
