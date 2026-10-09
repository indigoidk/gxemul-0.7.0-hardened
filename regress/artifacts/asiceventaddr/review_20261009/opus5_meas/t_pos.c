/*  opus5 measurement, POSITIVE leg: the 21 real events through the SHIPPED
    header (included read-only from GXEMUL-SEC via -I), compared against a
    reference formula written independently (division, not shift), and the
    full SYSASIC_TRIGGER_EVENT expansion captured through a stub cpu.  */
#include <stdio.h>
#include <stdint.h>
#include <string.h>

#define	MEM_WRITE	1
#define	PHYSICAL	1
struct cpu;
typedef int (*rwfn)(struct cpu *, void *, uint64_t, unsigned char *, size_t,
    int, int);
struct cpu { rwfn memory_rw; void *mem; };

/*  little-endian, as the SH4 Dreamcast guest is  */
static void memory_writemax64(struct cpu *c, unsigned char *b, int len,
    uint64_t v)
{
	int i;
	(void)c;
	for (i = 0; i < len; i++)
		b[i] = (unsigned char)(v >> (8 * i));
}

static uint64_t last_addr, last_payload;
static int calls;
static int rec_rw(struct cpu *c, void *m, uint64_t a, unsigned char *b,
    size_t len, int wf, int fl)
{
	uint64_t v = 0;
	size_t i;
	(void)c; (void)m; (void)wf; (void)fl;
	for (i = 0; i < len; i++)
		v |= (uint64_t)b[i] << (8 * i);
	last_addr = a; last_payload = v; calls++;
	return 1;
}

#include "thirdparty/dreamcast_sysasicvar.h"

#define	REF_ADDR(e)	(0x5f6900L + 4L * ((long)(e) / 32))
#define	REF_PAYLOAD(e)	((((uint64_t)1) << ((e) % 32)) | 0x100000000ULL)

static int n, same, bad;

#define	ROW(x) do {							\
	struct cpu cpu_s;						\
	struct cpu *cpu = &cpu_s;					\
	long a;								\
	int ok;								\
	cpu_s.memory_rw = rec_rw; cpu_s.mem = NULL;			\
	a = (long)SYSASIC_EVENT_TO_ADDR(x);				\
	SYSASIC_TRIGGER_EVENT(x);					\
	ok = a == REF_ADDR(x) && (long)last_addr == REF_ADDR(x) &&	\
	    last_payload == REF_PAYLOAD(x);				\
	n++; if (ok) same++; else bad++;				\
	printf("  %-28s e=%2d addr=0x%06lx ref=0x%06lx raise@0x%06lx"	\
	    " payload=0x%010llx %s\n", #x, (int)(x), a, REF_ADDR(x),	\
	    (long)last_addr, (unsigned long long)last_payload,		\
	    ok ? "SAME" : "DIFF");					\
	} while (0)

int main(void)
{
	ROW(SYSASIC_EVENT_RENDERDONE);
	ROW(SYSASIC_EVENT_PVR_SCANINT1);
	ROW(SYSASIC_EVENT_PVR_SCANINT2);
	ROW(SYSASIC_EVENT_VBLINT);
	ROW(SYSASIC_EVENT_OPAQUEDONE);
	ROW(SYSASIC_EVENT_OPAQUEMODDONE);
	ROW(SYSASIC_EVENT_TRANSDONE);
	ROW(SYSASIC_EVENT_TRANSMODDONE);
	ROW(SYSASIC_EVENT_MAPLE_DMADONE);
	ROW(SYSASIC_EVENT_MAPLE_ERROR);
	ROW(SYSASIC_EVENT_GDROM_DMA);
	ROW(SYSASIC_EVENT_SPU_DMA);
	ROW(SYSASIC_EVENT_SPU_IRQ);
	ROW(SYSASIC_EVENT_PVR_DMA);
	ROW(SYSASIC_EVENT_PVR_PTDONE);
	ROW(SYSASIC_EVENT_GDROM);
	ROW(SYSASIC_EVENT_AICA);
	ROW(SYSASIC_EVENT_8BIT);
	ROW(SYSASIC_EVENT_EXT);
	ROW(SYSASIC_EVENT_PRIMOUTOFMEM);
	ROW(SYSASIC_EVENT_MATOUTOFMEM);
	printf("POS rows=%d same=%d diff=%d raises=%d\n", n, same, bad, calls);
	return bad != 0;
}
