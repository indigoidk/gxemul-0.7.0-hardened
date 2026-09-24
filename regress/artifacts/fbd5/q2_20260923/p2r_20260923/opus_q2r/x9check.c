/*
 *  Opus seat, #545 q2r -- Q1(b): what the FROZEN handler does for X9's eight enable writes in its three
 *  states, next to (1) the expectation X9 computes and (2) the one derived by hand from the handler text
 *  (hard-coded below BEFORE this was run).  Same stubs as diff_footbridge.c.
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
static void noop_assert(struct interrupt *i) { (void) i; irq_asserts++; }
static void noop_deassert(struct interrupt *i) { (void) i; irq_deasserts++; }

#include "base/dev_footbridge.c"

static void arm_irqs(struct footbridge_data *d)
{
	int i;
	for (i = 0; i < N_FOOTBRIDGE_TIMERS; i++) {
		d->timer_irq[i].interrupt_assert = noop_assert;
		d->timer_irq[i].interrupt_deassert = noop_deassert;
	}
}

int main(void)
{
	static const struct { uint32_t is, ie, fs, fe; const char *nm; } S9[3] = {
		{ 0x18, 0x30, 0x60, 0xc0, "seeded" }, { 0, 0, 0, 0, "all-zero" },
		{ 0x80010018, 0x00010030, 0x40020060, 0x000200c0, "wide" } };
	static const struct { uint64_t addr; int fiq, set; uint32_t data; const char *nm; } W8[8] = {
		{ IRQ_ENABLE_SET, 0, 1, 0, "IRQ Set write 0" }, { IRQ_ENABLE_SET, 0, 1, 0x70, "IRQ Set write 0x70" },
		{ IRQ_ENABLE_CLEAR, 0, 0, 0, "IRQ Clear write 0" }, { IRQ_ENABLE_CLEAR, 0, 0, 0x70, "IRQ Clear write 0x70" },
		{ FIQ_ENABLE_SET, 1, 1, 0, "FIQ Set write 0" }, { FIQ_ENABLE_SET, 1, 1, 0x70, "FIQ Set write 0x70" },
		{ FIQ_ENABLE_CLEAR, 1, 0, 0, "FIQ Clear write 0" }, { FIQ_ENABLE_CLEAR, 1, 0, 0x70, "FIQ Clear write 0x70" } };
	/*  HAND DERIVATION from the handler text (written before running): resulting targeted enable, and
	    'A' = INTERRUPT_ASSERT, 'D' = INTERRUPT_DEASSERT, '-' = neither.  Rows: state; columns: W8 order.  */
	static const uint32_t HAND_NE[3][8] = {
		{ 0x30, 0x70, 0x30, 0x00, 0xc0, 0xf0, 0xc0, 0x80 },
		{ 0x00, 0x70, 0x00, 0x00, 0x00, 0x70, 0x00, 0x00 },
		{ 0x10030, 0x10070, 0x10030, 0x10000, 0x200c0, 0x200f0, 0x200c0, 0x20080 } };
	static const char HAND_IRQ[3][9] = { "AAAD----", "DDDD----", "AAAA----" };
	struct cpu *cpu = calloc(1, sizeof(struct cpu));
	int st, j, disagree = 0;
	cpu->machine = calloc(1, sizeof(struct machine));
	printf("%-9s %-22s %-10s %-4s %-7s | %-8s %-10s | %-10s %-5s | %s\n", "state", "write", "new enable",
	    "call", "fatal()", "X9 want", "X9 enable", "hand enbl", "hand", "agree");
	for (st = 0; st < 3; st++)
		for (j = 0; j < 8; j++) {
			struct footbridge_data *x = calloc(1, sizeof(*x));
			unsigned char b[8];
			uint32_t is = S9[st].is, ie = S9[st].ie, fs = S9[st].fs, fe = S9[st].fe;
			uint32_t old = W8[j].fiq ? fe : ie;
			uint32_t ne = W8[j].set ? (old | W8[j].data) : (old & ~W8[j].data);	/*  X9's own formula  */
			const char *x9 = W8[j].fiq ? "neither" : (is & ne) ? "ASSERT" : "DEASSERT";
			int a0, d0, rv, ok;
			uint32_t got;
			char call;
			arm_irqs(x);
			x->irq.interrupt_assert = noop_assert;
			x->irq.interrupt_deassert = noop_deassert;
			x->irq_status = is; x->irq_enable = ie; x->fiq_status = fs; x->fiq_enable = fe;
			fatal_calls = 0; a0 = irq_asserts; d0 = irq_deasserts;
			memory_writemax64(cpu, b, 4, W8[j].data);
			rv = dev_footbridge_access(cpu, NULL, W8[j].addr, b, 4, MEM_WRITE, x);
			got = W8[j].fiq ? x->fiq_enable : x->irq_enable;
			call = (irq_asserts - a0 == 1 && irq_deasserts == d0) ? 'A'
			    : (irq_deasserts - d0 == 1 && irq_asserts == a0) ? 'D'
			    : (irq_asserts == a0 && irq_deasserts == d0) ? '-' : '?';
			ok = rv == 1 && got == ne && got == HAND_NE[st][j] && call == HAND_IRQ[st][j]
			    && call == (W8[j].fiq ? '-' : (is & ne) ? 'A' : 'D');
			if (!ok) disagree++;
			printf("%-9s %-22s 0x%-8x %-4c %-7d | %-8s 0x%-8x | 0x%-8x %-5c | %s\n", S9[st].nm, W8[j].nm, got, call,
			    fatal_calls, x9, ne, HAND_NE[st][j], HAND_IRQ[st][j], ok ? "yes" : "NO");
			free(x);
		}
	printf("X9CHECK %s (%d disagreements)\n", disagree ? "MISMATCH" : "ALL AGREE", disagree);
	return 0;
}
