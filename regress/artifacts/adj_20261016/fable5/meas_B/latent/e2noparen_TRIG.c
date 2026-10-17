#include <stdint.h>
#include <stddef.h>
struct memory; struct cpu { struct memory *mem; int (*memory_rw)(struct cpu *, struct memory *, uint64_t, unsigned char *, size_t, int, int); };
#define MEM_WRITE 1
#define PHYSICAL 32
void memory_writemax64(struct cpu *cpu, unsigned char *buf, int len, uint64_t data);
#include "thirdparty/dreamcast_sysasicvar.h"
void g(struct cpu *cpu); void g(struct cpu *cpu) { SYSASIC_TRIGGER_EVENT(1 ? 200 : 5); }
