#include <stdint.h>
#include <stddef.h>
struct memory;
struct cpu {
	struct memory	*mem;
	int		(*memory_rw)(struct cpu *cpu, struct memory *mem,
			    uint64_t vaddr, unsigned char *data, size_t len,
			    int writeflag, int cache_flags);
};
#define	MEM_WRITE	1
#define	PHYSICAL	32
void memory_writemax64(struct cpu *cpu, unsigned char *buf, int len, uint64_t data);
#include "thirdparty/dreamcast_sysasicvar.h"
#include <stdio.h>
static struct cpu	*want_cpu;
static struct memory	*want_mem;
static int		sysasic_memobj;
static unsigned char	*ser_buf;
static int		ser_calls, ser_cpu_ok, ser_len;
static int		rw_calls, rw_writes, rw_cpu_ok, rw_mem_ok, rw_buf_ok, rw_flags, rw_len;
static uint64_t	rw_addr, rw_pay;

static void rec_reset(void)
{
	ser_buf = NULL;
	ser_calls = ser_cpu_ok = 0;
	ser_len = -1;
	rw_calls = rw_writes = rw_cpu_ok = rw_mem_ok = rw_buf_ok = 0;
	rw_flags = rw_len = -1;
	rw_addr = rw_pay = 0;
}

void memory_writemax64(struct cpu *cpu, unsigned char *buf, int len, uint64_t data)
{
	int i;

	ser_calls++;
	ser_cpu_ok = (cpu == want_cpu);
	ser_len = len;
	ser_buf = buf;
	for (i = 0; i < len && i < 8; i++) {
		buf[i] = (unsigned char)(data & 255);
		data >>= 8;
	}
}

static int id_rw(struct cpu *cpu, struct memory *mem, uint64_t vaddr,
    unsigned char *data, size_t len, int writeflag, int cache_flags)
{
	size_t i, n = len < 8 ? len : 8;

	rw_calls++;
	if (writeflag != MEM_WRITE)
		return 1;
	rw_writes++;
	rw_cpu_ok = (cpu == want_cpu);
	rw_mem_ok = (mem == want_mem);
	rw_buf_ok = (data == ser_buf);
	rw_flags = cache_flags;
	rw_len = (int)len;
	rw_addr = vaddr;
	rw_pay = 0;
	for (i = n; i > 0; i--)
		rw_pay = (rw_pay << 8) | data[i - 1];
	return 1;
}

static void rec_install(struct cpu *c)
{
	want_cpu = c;
	want_mem = (struct memory *)&sysasic_memobj;	/*  a DISTINCT object, never c  */
	c->mem = want_mem;
	c->memory_rw = id_rw;
}

#define	REC_FMT	"addr=0x%llx pay=0x%llx calls=%d writes=%d cpu=%s mem=%s buf=%s "	\
		"flags=%d len=%d ser=%d scpu=%s slen=%d\n"
#define	REC_ARGS	(unsigned long long)rw_addr, (unsigned long long)rw_pay,	\
		rw_calls, rw_writes, rw_cpu_ok ? "ok" : "BAD", rw_mem_ok ? "ok" : "BAD",	\
		rw_buf_ok ? "ok" : "BAD", rw_flags, rw_len, ser_calls,		\
		ser_cpu_ok ? "ok" : "BAD", ser_len
int main(void)
{
	struct cpu c;
	struct cpu *cpu = &c;
	rec_install(&c);
	rec_reset();
	SYSASIC_TRIGGER_EVENT(1 ? 33 : 0);
	printf("TV[1 ? 33 : 0] e=%d " REC_FMT, 33, REC_ARGS);
	rec_reset();
	SYSASIC_TRIGGER_EVENT(0 ? 0 : 33);
	printf("TV[0 ? 0 : 33] e=%d " REC_FMT, 33, REC_ARGS);
	rec_reset();
	SYSASIC_TRIGGER_EVENT(32 | 1);
	printf("TV[32 | 1] e=%d " REC_FMT, 33, REC_ARGS);
	return 0;
}
