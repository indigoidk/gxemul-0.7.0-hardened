/*  opus5 measurement, BITMASK leg.  SYSASIC_EVENT_TO_BITMASK(e) is
    (1 << ((e) & 31)) -- a signed int shift.  Inside the guarded domain
    [0,95], e = 31, 63 and 95 all give 1 << 31.  Questions:
      1. what value does the shipped macro produce there, under the build compiler;
      2. does UBSan call it undefined;
      3. does the ledger's proposed remedy (add + SYSASIC_EVENT_RANGE_OK(e) to
         BITMASK) remove it -- i.e. does that remedy even REJECT 31/63/95;
      4. is a 1u form device-equivalent (the device ORs into a uint32_t).  */
#include <stdio.h>
#include <stdint.h>
#include "thirdparty/dreamcast_sysasicvar.h"

#define	BITMASK_LEDGER_REMEDY(e) \
	(SYSASIC_EVENT_TO_BITMASK(e) + SYSASIC_EVENT_RANGE_OK(e))
#define	BITMASK_UNSIGNED(e)	(1u << ((e) & 31))

int main(void)
{
	volatile int ve = 31;
	uint64_t a31 = SYSASIC_EVENT_TO_BITMASK(31);
	uint64_t a63 = SYSASIC_EVENT_TO_BITMASK(63);
	uint64_t a95 = SYSASIC_EVENT_TO_BITMASK(95);
	uint64_t r31 = BITMASK_LEDGER_REMEDY(31);
	uint64_t r63 = BITMASK_LEDGER_REMEDY(63);
	uint64_t r95 = BITMASK_LEDGER_REMEDY(95);
	uint64_t u31 = BITMASK_UNSIGNED(31);
	uint64_t rt = SYSASIC_EVENT_TO_BITMASK(ve);
	uint64_t p_now = a31 | 0x100000000ULL;
	uint64_t p_uns = u31 | 0x100000000ULL;
	uint32_t pend_now = 0, pend_uns = 0;
	int e, nsame = 0;

	printf("shipped BITMASK(31)=0x%016llx (63)=0x%016llx (95)=0x%016llx\n",
	    (unsigned long long)a31, (unsigned long long)a63,
	    (unsigned long long)a95);
	printf("ledger remedy COMPILED for 31/63/95: (31)=0x%016llx (63)=0x%016llx"
	    " (95)=0x%016llx\n", (unsigned long long)r31,
	    (unsigned long long)r63, (unsigned long long)r95);
	printf("1u form (31)=0x%016llx\n", (unsigned long long)u31);
	printf("runtime shipped BITMASK(ve=31)=0x%016llx\n",
	    (unsigned long long)rt);
	printf("raise payload: shipped=0x%016llx 1u=0x%016llx\n",
	    (unsigned long long)p_now, (unsigned long long)p_uns);
	/*  dev_dreamcast_asic.c case 0/4/8: if (idata & 0x100000000ULL)
	    d->pending_irq[r] |= idata;  with pending_irq a uint32_t[3]  */
	if (p_now & 0x100000000ULL) pend_now |= p_now;
	if (p_uns & 0x100000000ULL) pend_uns |= p_uns;
	printf("device pending_irq after the raise: shipped=0x%08x 1u=0x%08x %s\n",
	    pend_now, pend_uns, pend_now == pend_uns ? "IDENTICAL" : "DIFFERENT");
	/*  and over the whole guarded domain  */
	for (e = 0; e < 96; e++) {
		uint32_t a = 0, b = 0;
		uint64_t ps = ((uint64_t)(int)(e % 32 == 31 ? (int)0x80000000u
		    : (1 << (e % 32)))) | 0x100000000ULL;
		uint64_t pu = ((uint64_t)(1u << (e & 31))) | 0x100000000ULL;
		a |= ps; b |= pu;
		if (a == b) nsame++;
	}
	printf("pending word identical for %d/96 events in [0,95]\n", nsame);
	return 0;
}
