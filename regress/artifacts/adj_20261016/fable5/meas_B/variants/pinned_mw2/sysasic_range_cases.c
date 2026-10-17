/*
 *  sysasic_range_cases.c -- the NAMED rows of regress/sysasic_range_check.py, the
 *  asiceventaddr detector for the compile-time event-domain guard in
 *  src/include/thirdparty/dreamcast_sysasicvar.h.
 *
 *  NOT A PROGRAM, AND DELIBERATELY NOT A diff_*.c.  Each row is ONE translation unit,
 *  selected by -DSYSASIC_CASE=<n>, and most of them are SUPPOSED TO FAIL TO COMPILE: a
 *  refusal cannot live in a program that has to build, which is why this is not a
 *  differential.  The driver compiles every block below against a COPY of the header
 *  under test and scores the compiler's own diagnostics; see its docstring for the oracle.
 *  Fifteen case blocks live here; the driver builds its other two rows, SWEEP and CENSUS,
 *  itself, and appends TSWEEP's swept raises after block 14.
 *
 *  THE DRIVER CHECKS THIS FILE'S SHAPE BEFORE IT TRUSTS IT: every row is one line of the
 *  exact form "#if SYSASIC_CASE == <n>" + its row name in a comment, and the set of those
 *  lines must equal the driver's row table -- a missing, duplicated or renumbered block
 *  makes the run VOID rather than quietly green.  An emptied block is caught by the
 *  null-medium control in gate 2 (every row must red on a comment-only header, which an
 *  empty block cannot do).
 *
 *  C89 COMMENTS ONLY, in every block: row C89 preprocesses this whole file under
 *  -std=c89 -pedantic-errors -Werror, excluded blocks included.
 */

#if SYSASIC_CASE == 9 || SYSASIC_CASE == 10 || SYSASIC_CASE == 11 || SYSASIC_CASE == 12 || \
    SYSASIC_CASE == 14 || SYSASIC_CASE == 15
/*  SYSASIC_TRIGGER_EVENT() expands against a `cpu' in scope; this is the minimum of GXemul's
    surface it names (rows XT96, XTm1, RTT, ID, TSWEEP and TVAL), placed BEFORE the include as
    the product TUs have it.  ID and TVAL define memory_writemax64() and a recording memory_rw
    below.

    MEM_WRITE AND PHYSICAL ARE THE PRODUCT'S VALUES, NOT THE STUB'S CHOICE: src/include/memory.h
    defines MEM_WRITE 1 and PHYSICAL 32 -- 2 is CACHE_NONE there.  The driver makes the run VOID
    unless memory.h carries exactly one `#define MEM_WRITE 1' and one `#define PHYSICAL 32', and
    ID and TVAL require the flags TRIGGER passes to be 32, so a stub that drifted from these two
    lines reds the committed header and a memory.h that moved stops the run.  (The pass-2
    prototype defined PHYSICAL as 2, and a TRIGGER passing the literal 2, or `PHYSICAL & 2',
    matched it.)  */
#include <stdint.h>
#include <stddef.h>
struct memory;
struct cpu {
	struct memory	*mem;
	int		(*memory_rw)(struct cpu *cpu, struct memory *mem,
			    uint64_t vaddr, unsigned char *data, size_t len,
			    int writeflag, int cache_flags);
};
#define	MEM_WRITE	2
#define	PHYSICAL	32
void memory_writemax64(struct cpu *cpu, unsigned char *buf, int len, uint64_t data);
#endif

#if SYSASIC_CASE == 8 || SYSASIC_CASE == 11
/*  RT and RTT are compiled once per runtime type of e -- an int, a long long and an unsigned
    long long, -DSYSASIC_RT_TYPE from the driver.  A constancy test keyed on the 8-byte rank (the
    width `__builtin_constant_p(e) ? <the guard> : (sizeof(e) == 8 ? 1 : (e))') refuses a runtime
    int and ACCEPTS a runtime 8-byte e at -O0, measured on the F2 pass: an int-only row cannot see
    it.  */
#ifndef SYSASIC_RT_TYPE
#define	SYSASIC_RT_TYPE	int
#endif
#endif

#include "thirdparty/dreamcast_sysasicvar.h"


/*  ---- ACCEPT, value ANCHORED: the domain's two edges, asserted INSIDE the TU so a value
    leak is a compile error of a DIFFERENT class ("size of array ... is negative") and can
    never be mistaken for a refusal.  C99 idiom, not _Static_assert: the tree is C99 by
    policy.  ----  */

#if SYSASIC_CASE == 1	/* A0 */
/*  the lower edge (e >= 0, the "at" member) lands on the FIRST word, pending_irq[0]  */
typedef char sysasic_a0_value_holds[(SYSASIC_EVENT_TO_ADDR(0)) == 0x5f6900 ? 1 : -1];
#endif

#if SYSASIC_CASE == 2	/* A95 */
/*  the upper edge's last legal slot (e < 96, the member below) lands on the THIRD word.
    ADDR only: TRIGGER at 95 meets the separately filed 1 << 31 (sysasicbitmask31).  */
typedef char sysasic_a95_value_holds[(SYSASIC_EVENT_TO_ADDR(95)) == 0x5f6908 ? 1 : -1];
#endif


/*  ---- REFUSE through ADDR.  Each must fail with exactly ONE bit-field-width error inside
    SYSASIC_EVENT_RANGE_OK's expansion.  Ordinary expressions in a function body -- never a
    static assert, an enum initializer or a file-scope array, which would refuse an
    array-based guard because of the FIXTURE and manufacture a kill.  ----  */

#if SYSASIC_CASE == 3	/* X96 */
/*  the header's own example: a NEW event name, one past the domain (the upper edge's
    "at" member).  The define lives HERE, so editing the header's prose cannot orphan it.  */
#define	SYSASIC_EVENT_FOO	96
unsigned long sysasic_x96(void);
unsigned long sysasic_x96(void)
{
	return SYSASIC_EVENT_TO_ADDR(SYSASIC_EVENT_FOO);
}
#endif

#if SYSASIC_CASE == 4	/* X97 */
/*  one past the edge: the only fixed row that sees a gap opened FURTHER out
    (`< 128 && != 96'), measured on the closure round's pass 1  */
unsigned long sysasic_x97(void);
unsigned long sysasic_x97(void)
{
	return SYSASIC_EVENT_TO_ADDR(97);
}
#endif

#if SYSASIC_CASE == 5	/* X128 */
/*  the first CLOBBER address (mask_13[0]); a documentation row, not a floor row  */
unsigned long sysasic_x128(void);
unsigned long sysasic_x128(void)
{
	return SYSASIC_EVENT_TO_ADDR(128);
}
#endif

#if SYSASIC_CASE == 6	/* Xm1 */
/*  the lower edge's member below: -1 lands at 0x5f68fc, BELOW the base, in pvr_dma's
    window -- #469's own defect, carried by this row and by XTm1  */
unsigned long sysasic_xm1(void);
unsigned long sysasic_xm1(void)
{
	return SYSASIC_EVENT_TO_ADDR(-1);
}
#endif

#if SYSASIC_CASE == 7	/* X2p32 */
/*  2^32: one named row for five measured weakenings -- an operand mask, an unsigned compare, a
    narrowing (int) cast, a far disjunct and an operand modulo.  It is the FIRST value only the
    compare and the cast admit: `& 0xff' first admits 256, `> 128' and `% 129' first admit 129,
    and the sweeps see those three in range as well.  */
unsigned long sysasic_x2p32(void);
unsigned long sysasic_x2p32(void)
{
	return SYSASIC_EVENT_TO_ADDR(0x100000000LL);
}
#endif

#if SYSASIC_CASE == 8	/* RT */
/*  a RUNTIME e: the width must be an integer constant.  An array-based guard would
    silently become a VLA here and compile; the bit-field hard-errors.  */
unsigned long sysasic_rt(int argc);
unsigned long sysasic_rt(int argc)
{
	SYSASIC_RT_TYPE e = argc;

	return SYSASIC_EVENT_TO_ADDR(e);
}
#endif


/*  ---- REFUSE through TRIGGER -- the only road the product uses.  A TRIGGER that stops
    calling ADDR keeps every ADDR row above green; these rows, TSWEEP and CENSUS see it.  ----  */

#if SYSASIC_CASE == 9	/* XT96 */
/*  the header's claim, verbatim in spirit: a new name plus a RAISE is a compile error  */
#define	SYSASIC_EVENT_FOO	96
void sysasic_xt96(struct cpu *cpu);
void sysasic_xt96(struct cpu *cpu)
{
	SYSASIC_TRIGGER_EVENT(SYSASIC_EVENT_FOO);
}
#endif

#if SYSASIC_CASE == 10	/* XTm1 */
void sysasic_xtm1(struct cpu *cpu);
void sysasic_xtm1(struct cpu *cpu)
{
	SYSASIC_TRIGGER_EVENT(-1);
}
#endif

#if SYSASIC_CASE == 11	/* RTT */
void sysasic_rtt(struct cpu *cpu, SYSASIC_RT_TYPE e);
void sysasic_rtt(struct cpu *cpu, SYSASIC_RT_TYPE e)
{
	SYSASIC_TRIGGER_EVENT(e);
}
#endif


/*  ---- RUN: real raises through TRIGGER, compiled, linked and EXECUTED.  The driver checks
    every printed address and payload against a reference it computes itself, outside the
    macro, and every argument TRIGGER passed against the values recorded here.  ----  */

#if SYSASIC_CASE == 12 || SYSASIC_CASE == 15
/*  the recording stub, shared by ID and TVAL.  THE STUB IS AN ORACLE HERE, so it is built not
    to hide a wrong argument.  The cpu and the memory handle are DISTINCT objects -- the pass-2
    prototype set c.mem = &c, so a TRIGGER passing the cpu as the handle matched -- and the
    pointers TRIGGER must pass are RETAINED here, apart from the struct it reads: the handle is
    compared with the object rec_install() made, never with cpu->mem as passed.  Both callees
    record the cpu they were given; memory_writemax64 records its length and the buffer it
    filled; memory_rw records EVERY call, whatever the writeflag, so `one call' and `one write'
    are separate facts -- a read before the write would refill the buffer in the product.  The
    driver asserts every recorded value.  */
#include <stdio.h>
static struct cpu	*want_cpu;
static struct memory	*want_mem;
static int		sysasic_memobj;
static unsigned char	*ser_buf;
static int		ser_calls, ser_cpu_ok, ser_len;
static int		rw_calls, rw_writes, rw_cpu_ok, rw_mem_ok, rw_buf_ok, rw_flags, rw_wflag;
static unsigned long long	rw_len;	/*  PIN A: memory_rw's size_t length, recorded at full width  */
static uint64_t	rw_addr, rw_pay;

static void rec_reset(void)
{
	ser_buf = NULL;
	ser_calls = ser_cpu_ok = 0;
	ser_len = -1;
	rw_calls = rw_writes = rw_cpu_ok = rw_mem_ok = rw_buf_ok = 0;
	rw_flags = rw_wflag = -1;
	rw_len = ~0ULL;
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
	rw_wflag = writeflag;	/*  PIN C: the int the function received  */
	rw_len = (unsigned long long)len;
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
		"flags=%d wflag=%d len=%llu ser=%d scpu=%s slen=%d\n"
#define	REC_ARGS	(unsigned long long)rw_addr, (unsigned long long)rw_pay,	\
		rw_calls, rw_writes, rw_cpu_ok ? "ok" : "BAD", rw_mem_ok ? "ok" : "BAD",	\
		rw_buf_ok ? "ok" : "BAD", rw_flags, rw_wflag, rw_len, ser_calls,		\
		ser_cpu_ok ? "ok" : "BAD", ser_len

#define	ID_RAISE(name)	do {							\
		rec_reset();							\
		SYSASIC_TRIGGER_EVENT(SYSASIC_EVENT_ ## name);			\
		printf("ID %s e=%d " REC_FMT, #name,				\
		    (int)(SYSASIC_EVENT_ ## name), REC_ARGS);			\
	} while (0)

#endif

#if SYSASIC_CASE == 12	/* ID */
int main(void)
{
	struct cpu c;
	struct cpu *cpu = &c;

	rec_install(&c);
	ID_RAISE(RENDERDONE);
	ID_RAISE(PVR_SCANINT1);
	ID_RAISE(PVR_SCANINT2);
	ID_RAISE(VBLINT);
	ID_RAISE(OPAQUEDONE);
	ID_RAISE(OPAQUEMODDONE);
	ID_RAISE(TRANSDONE);
	ID_RAISE(TRANSMODDONE);
	ID_RAISE(MAPLE_DMADONE);
	ID_RAISE(MAPLE_ERROR);
	ID_RAISE(GDROM_DMA);
	ID_RAISE(SPU_DMA);
	ID_RAISE(SPU_IRQ);
	ID_RAISE(PVR_DMA);
	ID_RAISE(PVR_PTDONE);
	ID_RAISE(GDROM);
	ID_RAISE(AICA);
	ID_RAISE(8BIT);
	ID_RAISE(EXT);
	ID_RAISE(PRIMOUTOFMEM);
	ID_RAISE(MATOUTOFMEM);
	printf("ID_DONE\n");
	return 0;
}
#endif


/*  ---- TRIGGER over the WHOLE domain.  ID raises only the 21 real events; these two rows give
    the RAISE route what SWEEP gives ADDR.  TSWEEP: the driver appends one SYSASIC_TRIGGER_EVENT()
    per line for every e it sweeps and compiles it -fsyntax-only, and the erroring lines must be
    exactly the out-of-domain ones -- an operand transform or exemption applied only on the raise
    route (`ADDR((e) & 0xff)', `ADDR((e) % 129)', `(e) == 100 ? 0 : (e)') passes every ADDR row
    and is visible here.  TVAL: every e in [0,95] raised as an int, and the two in-domain edges
    0 and 95 raised in each of the eight sizeof/sign classes, all checked -- the address, the
    device-visible payload (the low 32 bits and bit 32: at 31, 63 and 95 the raw payload is the
    filed sysasicbitmask31) and every argument pin.  The typed raises are there because a
    statement macro cannot value-assert inside TSWEEP: `tmp1 + 4*(sizeof(e) == 8 && (e) == 95)'
    passed every row of the pass-2 prototype (measured on the F2 pass).  ----  */

#if SYSASIC_CASE == 14	/* TSWEEP */
/*  the stub above and the header only; the driver appends the swept raises after this file  */
#endif

#if SYSASIC_CASE == 15	/* TVAL */
#define	TV(x)	do {								\
		rec_reset();							\
		SYSASIC_TRIGGER_EVENT(x);					\
		printf("TV e=%d " REC_FMT, (int)(x), REC_ARGS);			\
	} while (0)
#define	TV4(b)	TV((b)); TV((b) + 1); TV((b) + 2); TV((b) + 3)
#define	TV16(b)	TV4(b); TV4((b) + 4); TV4((b) + 8); TV4((b) + 12)
#define	TV32(b)	TV16(b); TV16((b) + 16)
/*  one typed raise: the class tag, the type, the in-domain value  */
#define	TT(tag, t, x)	do {						\
		rec_reset();							\
		SYSASIC_TRIGGER_EVENT((t)(x));				\
		printf("TT " #tag " e=%d " REC_FMT, (int)(x), REC_ARGS);	\
	} while (0)
#define	TT2(tag, t)	TT(tag, t, 0); TT(tag, t, 95)
int main(void)
{
	struct cpu c;
	struct cpu *cpu = &c;

	rec_install(&c);
	TV32(0);
	TV32(32);
	TV32(64);
	TT2(s8, signed char);
	TT2(u8, unsigned char);
	TT2(s16, short);
	TT2(u16, unsigned short);
	TT2(s32, int);
	TT2(u32, unsigned int);
	TT2(s64, long long);
	TT2(u64, unsigned long long);
	printf("TVAL_DONE\n");
	return 0;
}
#endif


/*  ---- the header's own C89 sentence ("needs only C89, and is clean under -std=c89
    -pedantic-errors -Wall -Wextra"), compiled under exactly that plus -Werror.  ADDR only:
    TRIGGER uses 0x100000000ULL, a C99 constant, and the sentence does not claim it.  ----  */

#if SYSASIC_CASE == 13	/* C89 */
unsigned long sysasic_c89(void);
unsigned long sysasic_c89(void)
{
	unsigned long s = 0;

	s += SYSASIC_EVENT_TO_ADDR(SYSASIC_EVENT_RENDERDONE);
	s += SYSASIC_EVENT_TO_ADDR(SYSASIC_EVENT_PVR_SCANINT1);
	s += SYSASIC_EVENT_TO_ADDR(SYSASIC_EVENT_PVR_SCANINT2);
	s += SYSASIC_EVENT_TO_ADDR(SYSASIC_EVENT_VBLINT);
	s += SYSASIC_EVENT_TO_ADDR(SYSASIC_EVENT_OPAQUEDONE);
	s += SYSASIC_EVENT_TO_ADDR(SYSASIC_EVENT_OPAQUEMODDONE);
	s += SYSASIC_EVENT_TO_ADDR(SYSASIC_EVENT_TRANSDONE);
	s += SYSASIC_EVENT_TO_ADDR(SYSASIC_EVENT_TRANSMODDONE);
	s += SYSASIC_EVENT_TO_ADDR(SYSASIC_EVENT_MAPLE_DMADONE);
	s += SYSASIC_EVENT_TO_ADDR(SYSASIC_EVENT_MAPLE_ERROR);
	s += SYSASIC_EVENT_TO_ADDR(SYSASIC_EVENT_GDROM_DMA);
	s += SYSASIC_EVENT_TO_ADDR(SYSASIC_EVENT_SPU_DMA);
	s += SYSASIC_EVENT_TO_ADDR(SYSASIC_EVENT_SPU_IRQ);
	s += SYSASIC_EVENT_TO_ADDR(SYSASIC_EVENT_PVR_DMA);
	s += SYSASIC_EVENT_TO_ADDR(SYSASIC_EVENT_PVR_PTDONE);
	s += SYSASIC_EVENT_TO_ADDR(SYSASIC_EVENT_GDROM);
	s += SYSASIC_EVENT_TO_ADDR(SYSASIC_EVENT_AICA);
	s += SYSASIC_EVENT_TO_ADDR(SYSASIC_EVENT_8BIT);
	s += SYSASIC_EVENT_TO_ADDR(SYSASIC_EVENT_EXT);
	s += SYSASIC_EVENT_TO_ADDR(SYSASIC_EVENT_PRIMOUTOFMEM);
	s += SYSASIC_EVENT_TO_ADDR(SYSASIC_EVENT_MATOUTOFMEM);
	s += SYSASIC_EVENT_TO_ADDR(0);
	s += SYSASIC_EVENT_TO_ADDR(95);
	return s;
}
#endif
