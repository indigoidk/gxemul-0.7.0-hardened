/*
 *  Opus seat, #545 q2c -- in-process DIFFERENTIAL between the frozen dev_footbridge.c ("base_") and one variant ("var_").
 *
 *  Each sequence is run on BOTH copies from the same start; after every step it compares
 *      guest-visible : handler return, the read buffer (all 8 bytes), the CPU irq LINE LEVEL
 *      host-visible  : announces (fatal() calls) -- the warn-once channel
 *      harness-only  : CPU ASSERT/DEASSERT call counts that leave the line level unchanged
 *  and after the last step 26 internal words (four registers, five latches, irq_asserted, the timer arrays).
 *
 *  Starts: "devinit" = the device after DEVINIT (timer_control PERIODIC, timer_load MAX, pending_bound 1, the timer
 *  interrupts wired to footbridge_interrupt_assert on lines 4..7 as DEVINIT's INTERRUPT_CONNECT does); "calloc" = the
 *  offline harness's all-zero instance, for comparison.
 *  Alphabet (304 ops): reads of 0x180/184/188/18c/280/284/288/28c at len 1, 2, 4 and 8 (8 is reachable: LDRD/STRD
 *  decode with no architecture check); writes of the same at the same widths with data 0, 0x10, 0x70, 0x400, 0x10000,
 *  0x80000000, 0xffffffff, 0x55; device lines 4 (timer 1), 10 (cats ISA), 11 (netwinder ISA), 18 (cats PCI) + and -;
 *  timer 1: control = ENABLE|PERIODIC, control = 0, a CLEAR write, a host-timer tick (footbridge_pending), DEVICE_TICK;
 *  and three alias probes (R1a0, W1ac=0x10, W2a0=0x70) that a widened fold or an added case label would redirect.
 *  Search: EXHAUSTIVE to length MAXL from "devinit" (first divergence = shortest), to length 2 from "calloc", then NRAND
 *  random sequences of length 4..6 from "devinit".  Prefixes are snapshotted in place, so a length-3 sequence costs one
 *  step; a sequence counts at the FIRST length at which it diverges.
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

/*  The CPU interrupt LINE: level per instance (guest-visible) and call counts (what the harness rows count).  */
static int irq_asserts, irq_deasserts;
static void *irq_b, *irq_v;
static int lvl_b, lvl_v;
static void cpu_assert(struct interrupt *i)
{ irq_asserts++; if ((void *) i == irq_b) lvl_b = 1; else if ((void *) i == irq_v) lvl_v = 1; }
static void cpu_deassert(struct interrupt *i)
{ irq_deasserts++; if ((void *) i == irq_b) lvl_b = 0; else if ((void *) i == irq_v) lvl_v = 0; }

typedef void (*irqf)(struct interrupt *);
#define DECL(p) \
	extern void p##reinit(void *, int, irqf, irqf); extern void *p##alloc(void); extern void *p##irqptr(void *); \
	extern void p##get(void *, uint32_t *); extern int p##acc(struct cpu *, void *, uint64_t, unsigned char *, size_t, int); \
	extern void p##line(void *, int, int); extern void p##pend(void *, int); extern void p##dtick(struct cpu *, void *);
DECL(base_)
DECL(var_)

enum { K_R, K_W, K_LINE, K_PEND, K_TICK };
typedef struct { int kind; uint32_t addr; int len; uint64_t data; int line, on; } op_t;
static op_t AL[400];
static int NA;
static struct cpu *cpu;

static void build_alpha(void)
{
	static const uint32_t A8[8] = { 0x180, 0x184, 0x188, 0x18c, 0x280, 0x284, 0x288, 0x28c };
	static const int LN[4] = { 1, 2, 4, 8 };
	static const uint64_t D8[8] = { 0, 0x10, 0x70, 0x400, 0x10000, 0x80000000u, 0xffffffffu, 0x55 };
	static const int LINES[4] = { 4, 10, 11, 18 };
	int a, l, k, o;
	/*  WIT2_ALIGN8: an ARM guest's only 8-byte access (LDRD/STRD) is aligned DOWN to 8 before memory_rw
	    (cpu_arm_instr_loadstore.c, `addr &= ~(datalen - 1)`), so len 8 reaches only 0x180/0x188/0x280/0x288.  */
	int align8 = getenv("WIT2_ALIGN8") != NULL;
	for (a = 0; a < 8; a++)
		for (l = 0; l < 4; l++) {
			if (align8 && LN[l] == 8 && (A8[a] & 7))
				continue;
			AL[NA].kind = K_R; AL[NA].addr = A8[a]; AL[NA].len = LN[l]; NA++;
		}
	for (a = 0; a < 8; a++)
		for (l = 0; l < 4; l++)
			for (k = 0; k < 8; k++) {
				if (align8 && LN[l] == 8 && (A8[a] & 7))
					continue;
				AL[NA].kind = K_W; AL[NA].addr = A8[a]; AL[NA].len = LN[l]; AL[NA].data = D8[k]; NA++;
			}
	for (k = 0; k < 4; k++)
		for (o = 1; o >= 0; o--) { AL[NA].kind = K_LINE; AL[NA].line = LINES[k]; AL[NA].on = o; NA++; }
	AL[NA].kind = K_W; AL[NA].addr = 0x308; AL[NA].len = 4; AL[NA].data = 0xc0; NA++;	/*  timer 1 ENABLE|PERIODIC  */
	AL[NA].kind = K_W; AL[NA].addr = 0x308; AL[NA].len = 4; AL[NA].data = 0; NA++;	/*  timer 1 disabled  */
	AL[NA].kind = K_W; AL[NA].addr = 0x30c; AL[NA].len = 4; AL[NA].data = 0; NA++;	/*  timer 1 CLEAR  */
	AL[NA].kind = K_PEND; AL[NA].line = 0; NA++;					/*  timer 1's host tick  */
	AL[NA].kind = K_TICK; NA++;
	AL[NA].kind = K_W; AL[NA].addr = 0x328; AL[NA].len = 4; AL[NA].data = 0xc0; NA++;	/*  q2e: timer 2 ENABLE|PERIODIC  */
	AL[NA].kind = K_PEND; AL[NA].line = 1; NA++;					/*  q2e: timer 2's host tick  */
	if (getenv("WIT2_NOALIAS") != NULL)	/*  Q1(c): the five offsets (and 0x188/0x288/0x28c/timer 1) only  */
		return;
	AL[NA].kind = K_R; AL[NA].addr = 0x1a0; AL[NA].len = 4; NA++;			/*  alias probes  */
	AL[NA].kind = K_W; AL[NA].addr = 0x1ac; AL[NA].len = 4; AL[NA].data = 0x10; NA++;
	AL[NA].kind = K_W; AL[NA].addr = 0x2a0; AL[NA].len = 4; AL[NA].data = 0x70; NA++;
}

static const char *opname(const op_t *o, char *s)
{
	if (o->kind == K_R) sprintf(s, "R%03x/%d", o->addr, o->len);
	else if (o->kind == K_W) sprintf(s, "W%03x/%d=0x%" PRIx64, o->addr, o->len, o->data);
	else if (o->kind == K_LINE) sprintf(s, "line%d%s", o->line, o->on ? "+" : "-");
	else if (o->kind == K_PEND) sprintf(s, "t%d-hosttick", o->line + 1);
	else sprintf(s, "DEVICE_TICK");
	return s;
}

typedef struct { int rv; uint64_t val; int ann, as, ds, lvl; } obs_t;

static obs_t apply(int var, void *d, const op_t *o)
{
	obs_t r;
	unsigned char b[8];
	int f0 = fatal_calls, a0 = irq_asserts, d0 = irq_deasserts;
	memset(&r, 0, sizeof(r));
	r.rv = -1;
	if (o->kind == K_LINE)
		(var ? var_line : base_line)(d, o->line, o->on);
	else if (o->kind == K_PEND)
		(var ? var_pend : base_pend)(d, o->line);	/*  q2e: .line holds the timer index  */
	else if (o->kind == K_TICK)
		(var ? var_dtick : base_dtick)(cpu, d);
	else {
		memset(b, 0xa5, sizeof(b));
		if (o->kind == K_W)
			memory_writemax64(NULL, b, o->len, o->data);
		r.rv = (var ? var_acc : base_acc)(cpu, d, o->addr, b, o->len, o->kind == K_W ? MEM_WRITE : MEM_READ);
		r.val = o->kind == K_R ? memory_readmax64(NULL, b, 8) : 0;
	}
	r.ann = fatal_calls - f0; r.as = irq_asserts - a0; r.ds = irq_deasserts - d0;
	r.lvl = var ? lvl_v : lvl_b;
	return r;
}

/*  flag bits: 1 guest-visible (return, read buffer, CPU line level), 2 announce, 4 internal state at the end,
    8 CPU irq call count only (same level)  */
static int step(void *b, void *v, int op, int verbose)
{
	char s[64];
	obs_t ob = apply(0, b, &AL[op]), ov = apply(1, v, &AL[op]);
	int g = ob.rv != ov.rv || ob.val != ov.val || ob.lvl != ov.lvl;
	int a = ob.ann != ov.ann;
	int c = !g && (ob.as != ov.as || ob.ds != ov.ds);
	if (verbose)
		printf("      %-16s base: rv=%d val=%016" PRIx64 " ann=%d A=%d D=%d line=%d | var: rv=%d val=%016" PRIx64
		    " ann=%d A=%d D=%d line=%d%s\n", opname(&AL[op], s), ob.rv, ob.val, ob.ann, ob.as, ob.ds, ob.lvl,
		    ov.rv, ov.val, ov.ann, ov.as, ov.ds, ov.lvl, g ? "   <-- GUEST-VISIBLE" : a ? "   <-- ANNOUNCE"
		    : c ? "   <-- irq call count only" : "");
	return (g ? 1 : 0) | (a ? 2 : 0) | (c ? 8 : 0);
}

static int endcmp(void *b, void *v, int verbose)
{
	uint32_t gb[26], gv[26];
	int i;
	base_get(b, gb); var_get(v, gv);
	if (verbose) {
		printf("      end state base:");
		for (i = 0; i < 26; i++) printf(" %x", gb[i]);
		printf("\n      end state var: ");
		for (i = 0; i < 26; i++) printf(" %x", gv[i]);
		printf("\n");
	}
	return memcmp(gb, gv, sizeof(gb)) != 0 ? 4 : 0;
}

static void *B, *V;
static size_t SZ;
/*  q2f: the CALLER context.  "devinit" runs as a real caller does -- a non-NULL mem and the machine type of the machine
    that has a footbridge (MACHINE_CATS by default, WIT2_MACHINE=netwinder for MACHINE_NETWINDER); "calloc" runs as the
    offline harness does -- mem NULL and MACHINE_NONE.  */
void *wit_mem;
static int wit_machine = MACHINE_CATS;
static void start(int mode)
{
	cpu->machine->machine_type = mode == 1 ? wit_machine : MACHINE_NONE;
	wit_mem = mode == 1 ? (void *) cpu->machine : NULL;
	base_reinit(B, mode, cpu_assert, cpu_deassert);
	var_reinit(V, mode, cpu_assert, cpu_deassert);
	irq_b = base_irqptr(B); irq_v = var_irqptr(V);
	lvl_b = lvl_v = 0;
}

static int run_seq(const int *seq, int n, int mode, int verbose)
{
	int i, f = 0;
	start(mode);
	for (i = 0; i < n; i++)
		f |= step(B, V, seq[i], verbose);
	f |= endcmp(B, V, verbose);
	return f;
}

static const char *MODE[2] = { "calloc", "devinit" };

static void show(const char *what, const int *seq, int n, int mode)
{
	char s[64];
	int i;
	printf("    shortest %s (start %s, %d step%s):", what, MODE[mode], n, n == 1 ? "" : "s");
	for (i = 0; i < n; i++)
		printf(" %s", opname(&AL[seq[i]], s));
	printf("\n");
	run_seq(seq, n, mode, 1);
}

/*  Exhaustive search with in-place prefix snapshots (restoring a snapshot INTO THE SAME instance keeps its
    self-pointers -- timer_irq[i].extra -- valid).  A class is counted at the node where it FIRST appears along the
    path.  A path is extended past a divergence unless it is already GUEST-visible, so a silent internal divergence
    (a latch consumed, a field changed) that turns guest-visible later is still found, at its shortest length.  */
static unsigned char *snapB[4], *snapV[4];
static int snapLB[4], snapLV[4];
static int xfound[4], xfl[4], xseq[4][4], cur[4];
static long xcnt[4], xtotal;

/*  ITERATIVE DEEPENING: pass L visits every sequence of exactly length L (prefixes are re-executed but not
    re-counted), so the first witness recorded for a class is a SHORTEST one.  (The first version of this search was
    depth-first and reported the first witness in depth-first order as "shortest" -- the class verdicts were right,
    the witness lengths were not.)  */
static void rec(int depth, int L, int obs_acc, int int_prev)
{
	int op, k;
	memcpy(snapB[depth], B, SZ); memcpy(snapV[depth], V, SZ); snapLB[depth] = lvl_b; snapLV[depth] = lvl_v;
	for (op = 0; op < NA; op++) {
		int f, in, acc;
		memcpy(B, snapB[depth], SZ); memcpy(V, snapV[depth], SZ); lvl_b = snapLB[depth]; lvl_v = snapLV[depth];
		f = step(B, V, op, 0);
		in = endcmp(B, V, 0);
		cur[depth] = op;
		acc = obs_acc | f;
		if (depth + 1 == L) {
			xtotal++;
			for (k = 0; k < 4; k++) {
				int bit = 1 << k, first;
				if (k == 2)
					first = in && !acc && !int_prev;	/*  internal only: nothing observable on the path yet  */
				else
					first = (f & bit) && !(obs_acc & bit);
				if (first) {
					xcnt[k]++;
					if (!xfound[k]) { xfound[k] = 1; xfl[k] = depth + 1; memcpy(xseq[k], cur, sizeof(cur)); }
				}
			}
		} else if (!(acc & 1))
			rec(depth + 1, L, acc, in);
	}
}

static void exhaust(int mode, int maxl)
{
	int k, L;
	for (k = 0; k < 4; k++) { xfound[k] = 0; xcnt[k] = 0; }
	xtotal = 0;
	for (L = 1; L <= maxl; L++) {
		start(mode);
		rec(0, L, 0, 0);
	}
	printf("START %-7s exhaustive len 1..%d: %ld nodes; first appearance of a divergence: guest-visible %ld,"
	    " announce %ld, internal-only %ld, irq-call-count-only %ld\n", MODE[mode], maxl, xtotal, xcnt[0], xcnt[1],
	    xcnt[2], xcnt[3]);
	if (xfound[0]) show("GUEST-VISIBLE divergence", xseq[0], xfl[0], mode);
	if (xfound[1]) show("ANNOUNCE divergence", xseq[1], xfl[1], mode);
	if (xfound[3] && !xfound[0]) show("IRQ-CALL-COUNT-ONLY divergence", xseq[3], xfl[3], mode);
	if (xfound[2] && !xfound[0] && !xfound[1]) show("INTERNAL-ONLY divergence", xseq[2], xfl[2], mode);
	if (!xfound[0] && !xfound[1] && !xfound[2] && !xfound[3])
		printf("    no divergence of any kind from %s to length %d\n", MODE[mode], maxl);
}

/*  REPLAY: wit2 replay <devinit|calloc> <op> <op> ...   ops: R180/4  W18c/4=0x10  line4+  line10-  pend  tick  */
static int parse_op(const char *s)
{
	op_t o;
	int i;
	unsigned a, l;
	unsigned long long dv;
	memset(&o, 0, sizeof(o));
	if (sscanf(s, "R%x/%u", &a, &l) == 2) { o.kind = K_R; o.addr = a; o.len = (int) l; }
	else if (sscanf(s, "W%x/%u=%llx", &a, &l, &dv) == 3) { o.kind = K_W; o.addr = a; o.len = (int) l; o.data = dv; }
	else if (strncmp(s, "line", 4) == 0) { o.kind = K_LINE; o.line = atoi(s + 4); o.on = s[strlen(s) - 1] == '+'; }
	else if (strcmp(s, "pend") == 0) o.kind = K_PEND;
	else if (strcmp(s, "pend2") == 0) { o.kind = K_PEND; o.line = 1; }
	else if (strcmp(s, "tick") == 0) o.kind = K_TICK;
	else { fprintf(stderr, "bad op %s\n", s); exit(2); }
	for (i = 0; i < NA; i++)
		if (AL[i].kind == o.kind && AL[i].addr == o.addr && AL[i].len == o.len && AL[i].data == o.data
		    && AL[i].line == o.line && AL[i].on == o.on)
			return i;
	AL[NA] = o;
	return NA++;
}

int main(int argc, char **argv)
{
	int maxl = argc > 1 ? atoi(argv[1]) : 3;
	long nrand = argc > 2 ? atol(argv[2]) : 1000000;
	cpu = calloc(1, sizeof(struct cpu));
	cpu->machine = calloc(1, sizeof(struct machine));
	cpu->machine->emulated_hz = 100000000;
	if (getenv("WIT2_MACHINE") != NULL && strcmp(getenv("WIT2_MACHINE"), "netwinder") == 0)
		wit_machine = MACHINE_NETWINDER;
	printf("machine for the devinit start: %s\n", wit_machine == MACHINE_NETWINDER ? "netwinder" : "cats");
	B = base_alloc(); V = var_alloc();
	{
		extern size_t base_size(void);
		int k;
		SZ = base_size();
		for (k = 0; k < 4; k++) { snapB[k] = malloc(SZ); snapV[k] = malloc(SZ); }
	}
	build_alpha();
	if (argc > 2 && strcmp(argv[1], "replay") == 0) {
		int seq[64], n = 0, i, mode = strcmp(argv[2], "calloc") == 0 ? 0 : 1, f;
		for (i = 3; i < argc && n < 64; i++)
			seq[n++] = parse_op(argv[i]);
		printf("REPLAY from %s:", MODE[mode]);
		for (i = 3; i < argc; i++)
			printf(" %s", argv[i]);
		printf("\n");
		f = run_seq(seq, n, mode, 1);
		printf("REPLAY flags: guest-visible %d, announce %d, internal %d, irq-call-count-only %d\nWIT2_DONE\n",
		    !!(f & 1), !!(f & 2), !!(f & 4), !!(f & 8));
		return 0;
	}
	printf("alphabet %d ops\n", NA);
	exhaust(1, maxl);
	exhaust(0, maxl < 2 ? maxl : 2);
	{
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
			f = run_seq(seq, n, 1, 0);
			if (f & 1) { cg++; if (n < bestg) { bestg = n; memcpy(gs, seq, sizeof(int) * n); } }
			if (f & 2) { ca++; if (n < besta) { besta = n; memcpy(as, seq, sizeof(int) * n); } }
			if (f & 4) ci++;
			if (f & 8) cc++;
		}
		printf("RANDOM devinit len 4..6: %ld sequences; diverging: guest-visible %ld, announce %ld, internal %ld,"
		    " irq-call-count-only %ld\n", nrand, cg, ca, ci, cc);
		if (cg) show("random GUEST-VISIBLE divergence", gs, bestg, 1);
		else if (ca) show("random ANNOUNCE divergence", as, besta, 1);
	}
	printf("WIT2_DONE\n");
	return 0;
}
