/*
 *  Opus seat q2r -- targeted differential for the four "dominating predicate outside the list" variants
 *  (the head idata load, the timer-fold range test).  Their effect lands on addresses or widths outside
 *  wit_main.c's alphabet, so they get hand-written sequences from RESET here.  Links the same two
 *  wit_tu.c units (base_ = frozen, var_ = variant).
 */
#include <inttypes.h>
#include <stdarg.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "include/misc.h"
#include "include/memory.h"
#include "include/machine.h"
#include "include/cpu.h"

bool single_step = false;
bool about_to_enter_single_step = false;
static int verb[16];
int *debugmsg_current_verbosity = verb;
static int fatal_calls;
void fatal(const char *fmt, ...) { (void) fmt; fatal_calls++; }
void debug(const char *fmt, ...) { (void) fmt; }
static double last_freq;
struct timer;
struct timer *timer_add(double freq, void (*f)(struct timer *, void *), void *extra)
{ (void) f; (void) extra; last_freq = freq; return (struct timer *) (void *) &last_freq; }
void timer_update_frequency(struct timer *t, double freq) { (void) t; last_freq = freq; }
uint64_t memory_readmax64(struct cpu *cpu, unsigned char *buf, int len)
{ uint64_t x = 0; int i; (void) cpu; for (i = 0; i < len; i++) x |= (uint64_t) buf[i] << (8*i); return x; }
void memory_writemax64(struct cpu *cpu, unsigned char *buf, int len, uint64_t data)
{ int i; (void) cpu; for (i = 0; i < len; i++) buf[i] = (data >> (8*i)) & 255; }
void console_putchar(int handle, int ch) { (void) handle; (void) ch; }
static int irq_asserts, irq_deasserts;
static void *irq_b, *irq_v;
static int lvl_b, lvl_v;
static void noop_assert(struct interrupt *i)
{ irq_asserts++; if ((void *) i == irq_b) lvl_b = 1; else if ((void *) i == irq_v) lvl_v = 1; }
static void noop_deassert(struct interrupt *i)
{ irq_deasserts++; if ((void *) i == irq_b) lvl_b = 0; else if ((void *) i == irq_v) lvl_v = 0; }
typedef void (*irqf)(struct interrupt *);
extern void *base_new(irqf, irqf), *var_new(irqf, irqf);
extern int base_acc(struct cpu *, void *, uint64_t, unsigned char *, size_t, int);
extern int var_acc(struct cpu *, void *, uint64_t, unsigned char *, size_t, int);
extern void base_line(void *, int, int), var_line(void *, int, int);
extern void *base_irqptr(void *), *var_irqptr(void *);

/*  op: 'R' addr len | 'W' addr len data | 'L' line on  */
typedef struct { char k; uint32_t a; int len; uint32_t data; } op_t;
static struct cpu *cpu;

static int step(int var, void *d, const op_t *o, uint64_t *val, int *ann, int *lvl)
{
	unsigned char b[8];
	int f0 = fatal_calls, rv = -1;
	*val = 0;
	if (o->k == 'L')
		(var ? var_line : base_line)(d, (int) o->a, o->len);
	else {
		memset(b, 0xa5, sizeof(b));
		if (o->k == 'W')
			memory_writemax64(NULL, b, o->len, o->data);
		rv = (var ? var_acc : base_acc)(cpu, d, o->a, b, o->len, o->k == 'W' ? MEM_WRITE : MEM_READ);
		if (o->k == 'R')
			*val = memory_readmax64(NULL, b, o->len);
	}
	*ann = fatal_calls - f0;
	*lvl = var ? lvl_v : lvl_b;
	return rv;
}

static void seq(const char *title, const op_t *ops, int n)
{
	void *b = base_new(noop_assert, noop_deassert), *v = var_new(noop_assert, noop_deassert);
	int i, any = 0;
	irq_b = base_irqptr(b); irq_v = var_irqptr(v); lvl_b = lvl_v = 0;
	printf("  %s\n", title);
	for (i = 0; i < n; i++) {
		uint64_t vb, vv;
		int ab, av, lb, lv, rb, rvv, g, a;
		rb = step(0, b, &ops[i], &vb, &ab, &lb);
		rvv = step(1, v, &ops[i], &vv, &av, &lv);
		g = rb != rvv || vb != vv || lb != lv;
		a = ab != av;
		any |= g || a;
		if (ops[i].k == 'L')
			printf("    line%u%s", ops[i].a, ops[i].len ? "+" : "-");
		else
			printf("    %c%03x/%d%s", ops[i].k, ops[i].a, ops[i].len, ops[i].k == 'W' ? "" : "");
		if (ops[i].k == 'W')
			printf("=0x%x", ops[i].data);
		printf("\t base: val=0x%" PRIx64 " ann=%d line=%d | var: val=0x%" PRIx64 " ann=%d line=%d%s\n",
		    vb, ab, lb, vv, av, lv, g ? "   <-- GUEST-VISIBLE" : a ? "   <-- ANNOUNCE" : "");
	}
	printf("    => %s\n", any ? "DIVERGES" : "same");
	free(b); free(v);
}

int main(void)
{
	cpu = calloc(1, sizeof(struct cpu));
	cpu->machine = calloc(1, sizeof(struct machine));
	cpu->machine->emulated_hz = 100000000;
	{
		op_t s[] = { { 'W', 0x188, 4, 0x70 }, { 'W', 0x18c, 1, 0x70 }, { 'R', 0x188, 4, 0 } };
		seq("narrow legal Clear write from reset: Set 0x70, byte Clear 0x70, read IRQEnable", s, 3);
	}
	{
		op_t s[] = { { 'W', 0x188, 4, 0x400 }, { 'L', 10, 1, 0 }, { 'R', 0x1a0, 4, 0 } };
		seq("unmodelled 0x1a0 read from reset (cats ISA line 10 pending and enabled)", s, 3);
	}
	{
		op_t s[] = { { 'R', 0x1ac, 4, 0 }, { 'R', 0x18c, 4, 0 } };
		seq("unmodelled 0x1ac read, then the real +0x18c declined read", s, 2);
	}
	{
		op_t s[] = { { 'W', 0x188, 4, 0x400 }, { 'L', 10, 1, 0 }, { 'W', 0x1ac, 4, 0x400 }, { 'R', 0x188, 4, 0 } };
		seq("unmodelled 0x1ac write of 0x400 (would clear IRQEnable bit 10 if it aliased +0x18c)", s, 4);
	}
	{
		op_t s[] = { { 'L', 10, 1, 0 }, { 'R', 0x1a4, 4, 0 } };
		seq("unmodelled 0x1a4 read with cats ISA line 10 pending", s, 2);
	}
	{
		op_t s[] = { { 'W', 0x2a0, 4, 0x70 }, { 'W', 0x280, 4, 0x70 }, { 'W', 0x2a4, 4, 0x70 }, { 'W', 0x284, 4, 0x70 } };
		seq("unmodelled 0x2a0 / 0x2a4 writes, then the real +0x280 / +0x284 declined writes", s, 4);
	}
	{
		op_t s[] = { { 'W', 0x188, 4, 0x20 }, { 'W', 0x18c, 4, 0x20 }, { 'R', 0x188, 4, 0 } };
		seq("Clear write of 0x20 from reset: Set 0x20, Clear 0x20, read IRQEnable", s, 3);
	}
	{
		/*  NOT a variant question: the frozen model's own irq line after (device line up while disabled,
		    guest enables it, device line drops).  The enable arms assert without setting irq_asserted,
		    and footbridge_interrupt_deassert() only deasserts when irq_asserted is set.  */
		op_t s[] = { { 'L', 10, 1, 0 }, { 'W', 0x188, 4, 0x400 }, { 'L', 10, 0, 0 }, { 'R', 0x180, 4, 0 } };
		seq("model check: line10 up while disabled, enable it, line10 down, read IRQ_STATUS", s, 4);
	}
	{
		/*  NO READ of 0x100 or 0x104 here: SDRAM_BA_MASK/OFFSET reads still end the process (fatal+exit)  */
		op_t s[] = { { 'W', 0x160, 4, 0x41 } };
		seq("UART_DATA write at 0x160 (folds onto SDRAM_BA_MASK 0x100 when the fold starts at 0x100)", s, 1);
	}
	printf("DOM_DONE\n");
	return 0;
}
