/*  Does option (A) -- `inbuf_len > 0 &&` -- refuse a LEGITIMATE drain?
 *
 *  `#265` fixed exactly this ambiguity in dev_asc: head==tail is true both when the
 *  FIFO is EMPTY and when it is exactly FULL.  wdc still has it, and `#473`'s own
 *  comment in dev_wdc.c admits so.  If a FULL ring is constructible with a WRITE in
 *  progress, then:
 *
 *      today          inbuf_len == 0, `0 % 512 == 0` -> DRAINS (correct, by accident)
 *      option (A)     inbuf_len == 0 fails `> 0`     -> REFUSES a legitimate drain
 *
 *  which would make (A) a regression on that state -- the same shape that rejected
 *  option A in #477 and that the Fable seat measured in #477's own phase guard.
 *
 *  This asks TWO questions and keeps them separate:
 *    1. is the full-ring state CONSTRUCTIBLE at all?
 *    2. if so, what does each variant DO with it?
 *
 *  A "not constructible" answer is a RESULT, not a failure: it would mean (A) is safe
 *  and the ambiguity is latent rather than live.
 */
#include <stdio.h>
#include <string.h>

#define WDC_MAX_SECTORS   512
#define WDC_INBUF_SIZE    (512 * (WDC_MAX_SECTORS + 1))

/*  the device's own arithmetic, transcribed from dev_wdc.c so this file can be read
 *  against it -- head/tail advance modulo the ring, occupancy is head-tail normalised  */
static int occupancy(int head, int tail)
{
	int n = head - tail;
	while (n < 0)
		n += WDC_INBUF_SIZE;
	return n;
}

int main(void)
{
	int head, tail, i, n;

	printf("  WDC_INBUF_SIZE = %d = 512 * %d\n",
	    WDC_INBUF_SIZE, WDC_INBUF_SIZE / 512);
	printf("  %d %% 512 = %d\n\n", WDC_INBUF_SIZE, WDC_INBUF_SIZE % 512);

	/*  Q1: after exactly WDC_INBUF_SIZE pushes, where are head and tail?  */
	head = tail = 0;
	for (i = 0; i < WDC_INBUF_SIZE; i++)
		head = (head + 1) % WDC_INBUF_SIZE;
	n = occupancy(head, tail);
	printf("  after a FULL ring of %d pushes: head=%d tail=%d occupancy=%d\n",
	    WDC_INBUF_SIZE, head, tail, n);
	printf("    today   `%d %% 512 == 0` -> %s\n", n, (n % 512) == 0 ? "DRAINS" : "no drain");
	printf("    opt (A) `%d > 0`         -> %s\n\n", n, n > 0 ? "DRAINS" : "REFUSES");

	/*  Q2: is that state REACHABLE while a WDCC_WRITE is in progress?  The drain
	    fires at EVERY multiple of 512, so the ring cannot climb past 512 without
	    being emptied.  Walk it and report the highest occupancy actually seen.  */
	head = tail = 0;
	{
		int maxocc = 0, drains = 0;
		for (i = 0; i < WDC_INBUF_SIZE + 4096; i++) {
			head = (head + 1) % WDC_INBUF_SIZE;      /*  one guest byte  */
			n = occupancy(head, tail);
			if (n > maxocc)
				maxocc = n;
			if ((n % 512) == 0) {                    /*  the drain condition  */
				tail = (tail + 512) % WDC_INBUF_SIZE;
				drains++;
			}
		}
		printf("  one-byte writes, WDCC_WRITE live, %d pushes:\n",
		    WDC_INBUF_SIZE + 4096);
		printf("    highest occupancy reached = %d   (ring holds %d)\n",
		    maxocc, WDC_INBUF_SIZE);
		printf("    drains fired = %d\n", drains);
		printf("    full-ring state reached? %s\n",
		    maxocc >= WDC_INBUF_SIZE ? "YES" : "NO");
	}
	return 0;
}
