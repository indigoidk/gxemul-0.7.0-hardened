/*  opus5 measurement, ENUMERATION leg: what the UNGUARDED formula 4*(e>>5)
    would do for e in [0,8192), classified against dev_dreamcast_asic.c's
    write switch.  The case labels are TRANSCRIBED from that file (READ, not
    compiled from it): case 0/4/8 -> pending_irq[r] (hack-bit OR);
    0x10/14/18 -> mask_13[r] = idata; 0x20/24/28 -> mask_11[r];
    0x30/34/38 -> mask_9[r]; default: -> debug() only.  memory_rw.c clamps a
    straddling access to the device end and still dispatches it.  */
#include <stdio.h>
#include "thirdparty/dreamcast_sysasicvar.h"

enum cls { CORRECT, CLOB13, CLOB11, CLOB9, DROP_R3, DROP_NOCASE, OUTSIDE, NCLS };
static const char *name[NCLS] = { "CORRECT pending_irq", "CLOBBER mask_13",
    "CLOBBER mask_11", "CLOBBER mask_9", "DROPPED (r==3)", "DROPPED (no case)",
    "OUTSIDE window" };

static enum cls classify(unsigned long rel)
{
	if (rel >= SYSASIC_SIZE)
		return OUTSIDE;
	switch (rel) {
	case 0: case 4: case 8:		return CORRECT;
	case 0x10: case 0x14: case 0x18: return CLOB13;
	case 0x20: case 0x24: case 0x28: return CLOB11;
	case 0x30: case 0x34: case 0x38: return CLOB9;
	default:	return ((rel / 4) & 3) == 3 ? DROP_R3 : DROP_NOCASE;
	}
}

int main(void)
{
	unsigned long cnt[NCLS] = { 0 }, clob_words = 0, straddle = 0, maple = 0;
	unsigned long seen_off[64] = { 0 };
	long e, lo = 0;
	enum cls cur = CORRECT, c;

	for (e = 0; e <= 8192; e++) {
		unsigned long rel = 4UL * ((unsigned long)e >> 5);
		c = e < 8192 ? classify(rel) : NCLS;
		if (e == 8192 || (e > 0 && c != cur)) {
			printf("  %5ld..%-5ld %-20s n=%ld\n", lo, e - 1, name[cur],
			    e - lo);
			lo = e;
		}
		if (e == 8192)
			break;
		cur = c;
		cnt[c]++;
		if ((c == CLOB13 || c == CLOB11 || c == CLOB9) &&
		    !seen_off[rel / 4]++)
			clob_words++;
		if (rel < SYSASIC_SIZE && rel + 8 > SYSASIC_SIZE)
			straddle++;
		if (SYSASIC_BASE + rel >= 0x5f6c00 && SYSASIC_BASE + rel < 0x5f6d00)
			maple++;
	}
	printf("CLOBBER total=%lu across %lu distinct mask words"
	    " (13:%lu 11:%lu 9:%lu)\n", cnt[CLOB13] + cnt[CLOB11] + cnt[CLOB9],
	    clob_words, cnt[CLOB13], cnt[CLOB11], cnt[CLOB9]);
	printf("CORRECT=%lu DROPPED=%lu (r==3:%lu nocase:%lu) OUTSIDE=%lu\n",
	    cnt[CORRECT], cnt[DROP_R3] + cnt[DROP_NOCASE], cnt[DROP_R3],
	    cnt[DROP_NOCASE], cnt[OUTSIDE]);
	printf("straddling the device end (clamped, dispatched)=%lu;"
	    " landing in Maple's window 0x5f6c00..0x5f6cff=%lu\n", straddle, maple);
	printf("the header comment's own [128,479] span = %d values\n",
	    479 - 128 + 1);
	return 0;
}
