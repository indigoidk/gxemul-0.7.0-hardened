/*
 *  Opus seat, #545 q2r -- in-process DIFFERENTIAL between the frozen dev_footbridge.c ("base_")
 *  and one variant ("var_"), both compiled from their own copies into this one binary.
 *
 *  Every sequence is run on a fresh instance of EACH copy, step by step, and after every step the
 *  observables are compared:
 *      guest-visible : handler return, the read buffer (all 8 bytes), the CPU irq LINE LEVEL
 *      host-visible  : announces (fatal() calls) -- the warn-once channel
 *      harness-only  : ASSERT/DEASSERT CALL COUNTS that leave the line level unchanged (redundant calls)
 *  and after the last step the internal fields (four registers, five latches, irq_asserted).
 *
 *  Search: EXHAUSTIVE over every sequence of length 1..MAXL from each start state, so the first
 *  divergence found is the SHORTEST; then random sequences of length 4..6 from reset.
 *  Start "reset" is the device after DEVINIT (all zero, latches clear) and its only irq_status
 *  writer is a device line (footbridge_interrupt_assert) -- lines 4 (timer 1), 10 (cats ISA),
 *  11 (netwinder ISA) and 18 (cats PCI, dec21143) are the ones something in the tree drives.
 *  fiq_status has NO writer in the product, so it is 0 in every reachable state.
 *  Starts "seeded" and "wide" are the harness's own (NOT reachable: fiq_status != 0).
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

/*  The CPU interrupt LINE LEVEL per instance is the guest-visible quantity; the call counts are what the
    harness rows count.  A redundant ASSERT on a high line (or DEASSERT on a low one) changes no level.  */
static int irq_asserts, irq_deasserts;
static void *irq_b, *irq_v;
static int lvl_b, lvl_v;
static void noop_assert(struct interrupt *i)
{ irq_asserts++; if ((void *) i == irq_b) lvl_b = 1; else if ((void *) i == irq_v) lvl_v = 1; }
static void noop_deassert(struct interrupt *i)
{ irq_deasserts++; if ((void *) i == irq_b) lvl_b = 0; else if ((void *) i == irq_v) lvl_v = 0; }

typedef void (*irqf)(struct interrupt *);
extern void *base_new(irqf, irqf), *var_new(irqf, irqf);
extern void base_set(void *, uint32_t, uint32_t, uint32_t, uint32_t), var_set(void *, uint32_t, uint32_t, uint32_t, uint32_t);
extern void base_get(void *, uint32_t *), var_get(void *, uint32_t *);
extern int base_acc(struct cpu *, void *, uint64_t, unsigned char *, size_t, int);
extern int var_acc(struct cpu *, void *, uint64_t, unsigned char *, size_t, int);
extern void base_line(void *, int, int), var_line(void *, int, int);
extern void *base_irqptr(void *), *var_irqptr(void *);

typedef struct { int kind; uint32_t addr; int len; uint32_t data; int line, on; } op_t;	/*  kind 0 R, 1 W, 2 line  */
static op_t AL[256];
static int NA;
static struct cpu *cpu;

static void build_alpha(void)
{
	static const uint32_t A8[8] = { 0x180, 0x184, 0x188, 0x18c, 0x280, 0x284, 0x288, 0x28c };
	static const int LN[3] = { 1, 2, 4 };
	static const uint32_t D7[7] = { 0, 0x10, 0x70, 0x400, 0x10000, 0x80000000u, 0xffffffffu };
	static const int LINES[4] = { 4, 10, 11, 18 };
	int a, l, k, o;
	for (a = 0; a < 8; a++)
		for (l = 0; l < 3; l++) { AL[NA].kind = 0; AL[NA].addr = A8[a]; AL[NA].len = LN[l]; NA++; }
	for (a = 0; a < 8; a++)
		for (l = 0; l < 3; l++)
			for (k = 0; k < 7; k++) { AL[NA].kind = 1; AL[NA].addr = A8[a]; AL[NA].len = LN[l]; AL[NA].data = D7[k]; NA++; }
	for (k = 0; k < 4; k++)
		for (o = 1; o >= 0; o--) { AL[NA].kind = 2; AL[NA].line = LINES[k]; AL[NA].on = o; NA++; }
}

static const char *opname(const op_t *o, char *s)
{
	if (o->kind == 0) sprintf(s, "R%03x/%d", o->addr, o->len);
	else if (o->kind == 1) sprintf(s, "W%03x/%d=0x%x", o->addr, o->len, o->data);
	else sprintf(s, "line%d%s", o->line, o->on ? "+" : "-");
	return s;
}

typedef struct { int rv; uint64_t val; int ann, as, ds, lvl; } obs_t;

static obs_t apply(int var, void *d, const op_t *o)
{
	obs_t r;
	unsigned char b[8];
	int f0 = fatal_calls, a0 = irq_asserts, d0 = irq_deasserts;
	memset(&r, 0, sizeof(r));
	if (o->kind == 2) {
		(var ? var_line : base_line)(d, o->line, o->on);
		r.rv = -1;
	} else {
		memset(b, 0xa5, sizeof(b));
		if (o->kind == 1)
			memory_writemax64(NULL, b, o->len, o->data);
		r.rv = (var ? var_acc : base_acc)(cpu, d, o->addr, b, o->len, o->kind == 1 ? MEM_WRITE : MEM_READ);
		r.val = o->kind == 0 ? memory_readmax64(NULL, b, 8) : 0;
	}
	r.ann = fatal_calls - f0; r.as = irq_asserts - a0; r.ds = irq_deasserts - d0;
	r.lvl = var ? lvl_v : lvl_b;
	return r;
}

static const struct { const char *nm; uint32_t is, ie, fs, fe; } ST[3] = {
	{ "reset", 0, 0, 0, 0 }, { "seeded", 0x18, 0x30, 0x60, 0xc0 },
	{ "wide", 0x80010018, 0x00010030, 0x40020060, 0x000200c0 } };

/*  returns bit0 = some step differs GUEST-visibly (return, read buffer, CPU irq line LEVEL),
    bit1 = some step differs in announces, bit2 = internal state differs at the end,
    bit3 = some step differs only in irq CALL COUNTS (same level: a redundant call)  */
static int run(const int *seq, int n, int st, int verbose)
{
	void *b = base_new(noop_assert, noop_deassert), *v = var_new(noop_assert, noop_deassert);
	uint32_t gb[10], gv[10];
	int i, flags = 0;
	char s[64];
	irq_b = base_irqptr(b); irq_v = var_irqptr(v);
	lvl_b = lvl_v = 0;
	base_set(b, ST[st].is, ST[st].ie, ST[st].fs, ST[st].fe);
	var_set(v, ST[st].is, ST[st].ie, ST[st].fs, ST[st].fe);
	for (i = 0; i < n; i++) {
		obs_t ob = apply(0, b, &AL[seq[i]]), ov = apply(1, v, &AL[seq[i]]);
		int g = ob.rv != ov.rv || ob.val != ov.val || ob.lvl != ov.lvl;
		int a = ob.ann != ov.ann;
		int c = !g && (ob.as != ov.as || ob.ds != ov.ds);
		flags |= (g ? 1 : 0) | (a ? 2 : 0) | (c ? 8 : 0);
		if (verbose) {
			printf("      %-16s base: rv=%d val=%016" PRIx64 " ann=%d A=%d D=%d line=%d | var: rv=%d val=%016" PRIx64
			    " ann=%d A=%d D=%d line=%d%s\n", opname(&AL[seq[i]], s), ob.rv, ob.val, ob.ann, ob.as, ob.ds, ob.lvl,
			    ov.rv, ov.val, ov.ann, ov.as, ov.ds, ov.lvl, g ? "   <-- GUEST-VISIBLE" : a ? "   <-- ANNOUNCE"
			    : c ? "   <-- irq call count only" : "");
		}
	}
	base_get(b, gb); var_get(v, gv);
	if (memcmp(gb, gv, sizeof(gb)) != 0)
		flags |= 4;
	if (verbose)
		printf("      end state base: is=%x ie=%x fs=%x fe=%x latches=%u%u%u%u%u asserted=%u | var: is=%x ie=%x fs=%x"
		    " fe=%x latches=%u%u%u%u%u asserted=%u\n", gb[0], gb[1], gb[2], gb[3], gb[4], gb[5], gb[6], gb[7], gb[8],
		    gb[9], gv[0], gv[1], gv[2], gv[3], gv[4], gv[5], gv[6], gv[7], gv[8], gv[9]);
	free(b); free(v);
	return flags;
}

static void show(const char *what, const int *seq, int n, int st)
{
	char s[64];
	int i;
	printf("    shortest %s (start %s, %d step%s):", what, ST[st].nm, n, n == 1 ? "" : "s");
	for (i = 0; i < n; i++)
		printf(" %s", opname(&AL[seq[i]], s));
	printf("\n");
	run(seq, n, st, 1);
}

int main(int argc, char **argv)
{
	int maxl = argc > 1 ? atoi(argv[1]) : 3;
	long nrand = argc > 2 ? atol(argv[2]) : 2000000;
	int st;
	cpu = calloc(1, sizeof(struct cpu));
	cpu->machine = calloc(1, sizeof(struct machine));
	cpu->machine->emulated_hz = 100000000;
	build_alpha();
	printf("alphabet %d ops (24 reads, 168 writes, 8 line ops)\n", NA);
	for (st = 0; st < 3; st++) {
		int found[4] = { 0, 0, 0, 0 }, fl[4] = { 0, 0, 0, 0 }, fseq[4][8];
		long cnt[4] = { 0, 0, 0, 0 }, total = 0;
		int n, seq[8], i, k;
		/*  reset (the reachable start) to maxl; the two harness starts to 2, for comparison only  */
		int lmax = st == 0 ? maxl : (maxl < 2 ? maxl : 2);
		for (n = 1; n <= lmax; n++) {
			long lim = 1, idx;
			for (i = 0; i < n; i++)
				lim *= NA;
			for (idx = 0; idx < lim; idx++) {
				long t = idx;
				int f;
				for (i = n - 1; i >= 0; i--) { seq[i] = (int) (t % NA); t /= NA; }
				f = run(seq, n, st, 0);
				total++;
				for (k = 0; k < 4; k++)
					if (f & (1 << k)) {
						cnt[k]++;
						if (!found[k]) { found[k] = 1; fl[k] = n; memcpy(fseq[k], seq, sizeof(int) * n); }
					}
			}
		}
		printf("START %-6s exhaustive len 1..%d: %ld sequences; diverging: guest-visible %ld, announce %ld, internal %ld,"
		    " irq-call-count-only %ld\n", ST[st].nm, lmax, total, cnt[0], cnt[1], cnt[2], cnt[3]);
		if (found[0]) show("GUEST-VISIBLE divergence", fseq[0], fl[0], st);
		if (found[1]) show("ANNOUNCE divergence", fseq[1], fl[1], st);
		if (found[3] && !found[0]) show("IRQ-CALL-COUNT-ONLY divergence", fseq[3], fl[3], st);
		if (found[2] && !found[0] && !found[1]) show("INTERNAL-ONLY divergence", fseq[2], fl[2], st);
	}
	{
		/*  random, reset only, lengths 4..6  */
		uint64_t x = 0x9e3779b97f4a7c15ULL;
		long r, cg = 0, ca = 0, ci = 0, cc = 0;
		int seq[8], n, i, bestg = 99, besta = 99, gs[8], as[8];
		for (r = 0; r < nrand; r++) {
			int f;
			x ^= x << 13; x ^= x >> 7; x ^= x << 17;
			n = 4 + (int) (x % 3);
			for (i = 0; i < n; i++) {
				x ^= x << 13; x ^= x >> 7; x ^= x << 17;
				seq[i] = (int) (x % (uint64_t) NA);
			}
			f = run(seq, n, 0, 0);
			if (f & 1) { cg++; if (n < bestg) { bestg = n; memcpy(gs, seq, sizeof(int) * n); } }
			if (f & 2) { ca++; if (n < besta) { besta = n; memcpy(as, seq, sizeof(int) * n); } }
			if (f & 4) ci++;
			if (f & 8) cc++;
		}
		printf("RANDOM reset len 4..6: %ld sequences; diverging: guest-visible %ld, announce %ld, internal %ld,"
		    " irq-call-count-only %ld\n", nrand, cg, ca, ci, cc);
		if (cg) show("random GUEST-VISIBLE divergence", gs, bestg, 0);
		else if (ca) show("random ANNOUNCE divergence", as, besta, 0);
	}
	printf("WIT_DONE\n");
	return 0;
}
