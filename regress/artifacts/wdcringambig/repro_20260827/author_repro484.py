"""#484 REPRODUCTION, test-first, against the COMMITTED build.  REPO IS NOT TOUCHED.

The candidate round is `wdcringambig` + `wdcaddtoinbufbound`, taken together: the ring's
`head == tail` encodes BOTH empty and full, and `wdc_addtoinbuf()` has no capacity check.

*** THIS IS A RUNG-1 ARTEFACT AND THEREFORE A DETECTOR, NEVER A REPRODUCTION, whatever it
measures.  It is built FIRST because the lifecycle requires a red-before-green measurement
on the committed build, and a rung-3 witness is being asked for separately. ***

THREE LEGS, and the first is the one that makes the other two mean anything:

  LEG 1  LIVENESS -- SIZE-1 pushes.  Occupancy must read SIZE-1 and DRQ must be SET.
         Without it a red result is equally explained by "the ring never worked at all",
         which is not the claim.

  LEG 2  THE AMBIGUITY -- exactly SIZE pushes.  head wraps onto tail.  Occupancy reads 0
         and DRQ goes CLEAR while 262656 staged bytes sit in the buffer.  Nothing is
         destroyed YET: index 0 still holds push #0.  This leg isolates the AMBIGUITY from
         the CORRUPTION, which the queue entry conflates.

  LEG 3  THE CORRUPTION -- SIZE+1 pushes.  Push #SIZE lands on index 0 and destroys push
         #0's byte.  The marker is asymmetric on purpose (0x11 first, 0x22 for the rest),
         so the row cannot pass by reading back a value that was never different.

  LEG 4  REACHABILITY -- the same wrap driven through `dev_wdc_access(wd_data, MEM_WRITE)`
         with NO tenant armed at all, which is the orphan-ring route #483 measured.  It
         asserts the guest path reaches the primitive with no capacity check anywhere
         between them.

  Each leg reports its own numbers.  A leg that cannot allocate says SETUP and returns --
  it never `continue`s past a failed fixture, which is the vacuity shape this file has
  already shipped once.
"""
import io
import os
import shutil

NL, T, BS = chr(10), chr(9), chr(92)
N = BS + "n"
ROOT = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC"
OUT = (r"C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-CC-GXEMUL"
       r"\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\r484")

src = io.open(os.path.join(ROOT, "regress", "diff_wdc_identify.c"),
              encoding="utf-8", newline="").read()

ROW = '''

/*  #484 REPRO: the ring's `head == tail` means BOTH empty and full, and the
 *  primitive has no capacity check.
 *
 *  WDC_INBUF_SIZE is 512*(WDC_MAX_SECTORS+1) = 262656.  `wdc_addtoinbuf()`
 *  masks the index, so there is NO out-of-bounds write -- the harm is that a
 *  FULL ring is arithmetically indistinguishable from an EMPTY one, and that
 *  the next push silently destroys an unread byte.
 *
 *  FOUR CONSUMERS of that ambiguity, all reading the same predicate:
 *      the post-hoc overrun latch in wdc_addtoinbuf()
 *      the pop guard in wdc_get_inbuf(), which returns -1
 *      status_byte()'s DRQ bit -- the guest is told there is no data
 *      the modular occupancy that feeds the ATAPI CDB dispatch
 */
static void repro_ring_ambiguity(void)
{
	struct wdc_data d;
	unsigned char buf[8];
	int i, occ, drq, tailb;
	int occ1 = -1, drq1 = -1;		/*  leg 1, liveness   */
	int occ2 = -1, drq2 = -1, tail2 = -1;	/*  leg 2, ambiguity  */
	int occ3 = -1, tail3 = -1;		/*  leg 3, corruption */
	int occ4 = -1, drq4 = -1;		/*  leg 4, guest path */

	/*  LEG 1 -- LIVENESS.  One short of full.  Everything must be correct
	    here, or a red result below is equally explained by a ring that never
	    worked.  */
	altctl_fresh(&d);
	if (d.inbuf == NULL) { printf("  SETUP repro leg1@N@"); return; }
	for (i = 0; i < WDC_INBUF_SIZE - 1; i++)
		wdc_addtoinbuf(&d, 0x22);
	occ = d.inbuf_head - d.inbuf_tail;
	while (occ < 0)
		occ += WDC_INBUF_SIZE;
	occ1 = occ;
	drq1 = (status_byte(&d, fake_cpu()) & WDCS_DRQ) ? 1 : 0;
	altctl_free(&d);

	/*  LEG 2 -- THE AMBIGUITY, isolated from the corruption.  Exactly SIZE
	    pushes: head wraps onto tail.  Index 0 still holds push #0, so
	    NOTHING IS DESTROYED YET -- only the arithmetic has collapsed.  */
	altctl_fresh(&d);
	if (d.inbuf == NULL) { printf("  SETUP repro leg2@N@"); return; }
	wdc_addtoinbuf(&d, 0x11);
	for (i = 1; i < WDC_INBUF_SIZE; i++)
		wdc_addtoinbuf(&d, 0x22);
	occ = d.inbuf_head - d.inbuf_tail;
	while (occ < 0)
		occ += WDC_INBUF_SIZE;
	occ2 = occ;
	drq2 = (status_byte(&d, fake_cpu()) & WDCS_DRQ) ? 1 : 0;
	tail2 = d.inbuf[d.inbuf_tail];
	altctl_free(&d);

	/*  LEG 3 -- THE CORRUPTION.  One more push.  #SIZE lands on index 0 and
	    replaces push #0's byte.  The marker is ASYMMETRIC (0x11 then 0x22)
	    so this cannot pass by reading back a value that never differed.  */
	altctl_fresh(&d);
	if (d.inbuf == NULL) { printf("  SETUP repro leg3@N@"); return; }
	wdc_addtoinbuf(&d, 0x11);
	for (i = 1; i < WDC_INBUF_SIZE + 1; i++)
		wdc_addtoinbuf(&d, 0x22);
	occ = d.inbuf_head - d.inbuf_tail;
	while (occ < 0)
		occ += WDC_INBUF_SIZE;
	occ3 = occ;
	tail3 = d.inbuf[0];
	altctl_free(&d);

	/*  LEG 4 -- REACHABILITY.  The same wrap driven entirely through the
	    guest data-port write arm with NO TENANT ARMED -- the orphan-ring
	    route #483 measured: the #464 unexpected-write test gates only the
	    diagnostic, and the wdc_addtoinbuf() calls sit outside it.
	    131328 two-byte stores is exactly SIZE bytes.  */
	altctl_fresh(&d);
	if (d.inbuf == NULL) { printf("  SETUP repro leg4@N@"); return; }
	for (i = 0; i < WDC_INBUF_SIZE / 2; i++) {
		buf[0] = 0x22; buf[1] = 0x22;
		dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_WRITE, &d);
	}
	occ = d.inbuf_head - d.inbuf_tail;
	while (occ < 0)
		occ += WDC_INBUF_SIZE;
	occ4 = occ;
	drq4 = (status_byte(&d, fake_cpu()) & WDCS_DRQ) ? 1 : 0;
	altctl_free(&d);

	(void) tailb;
	rows ++;
	printf("  REPRO leg1 occ=%i drq=%i | leg2 occ=%i drq=%i tail=0x%02x |"
	    " leg3 occ=%i inbuf[0]=0x%02x | leg4 occ=%i drq=%i@N@",
	    occ1, drq1, occ2, drq2, tail2, occ3, tail3, occ4, drq4);
	printf("  REPRO want   leg1 occ=%i drq=1 | leg2 occ!=0 drq=1 tail=0x11 |"
	    " leg3 inbuf[0]=0x11 | leg4 occ!=0 drq=1@N@", WDC_INBUF_SIZE - 1);
	if (occ1 != WDC_INBUF_SIZE - 1 || drq1 != 1 ||
	    occ2 == 0 || drq2 != 1 || tail2 != 0x11 ||
	    tail3 != 0x11 || occ4 == 0 || drq4 != 1) {
		printf("  FAIL %-38s see REPRO lines above@N@",
		    "the ring distinguishes full from empty");
		failures ++;
	} else {
		printf("  ok   %-38s full != empty@N@",
		    "the ring distinguishes full from empty");
	}
}

'''.replace("@N@", N)

anchor = NL + NL + "static void row_arm_overrun(void)"
assert src.count(anchor) == 1, "anchor %d" % src.count(anchor)
reg = T + "row_reset_bit_iff();" + NL
assert src.count(reg) == 1, "reg %d" % src.count(reg)

s = src.replace(anchor, ROW + NL + "static void row_arm_overrun(void)", 1)
s = s.replace(reg, reg + T + "repro_ring_ambiguity();" + NL, 1)
for a, b in [("if (rows != 103) {", "if (rows != 104) {"),
             ("rows = %i, want 103", "rows = %i, want 104")]:
    assert s.count(a) == 1, "%r %d" % (a, s.count(a))
    s = s.replace(a, b, 1)

if os.path.isdir(OUT):
    shutil.rmtree(OUT)
os.makedirs(os.path.join(OUT, "regress"))
io.open(os.path.join(OUT, "regress", "diff_wdc_identify.c"),
        "w", encoding="utf-8", newline="").write(s)
print("  #484 reproduction written to r484/regress/; REPO NOT TOUCHED")
