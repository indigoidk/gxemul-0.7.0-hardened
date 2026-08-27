"""The WRITEMULTI rows, and the second-bad-len row.

*** `WRITEMULTI` APPEARED ZERO TIMES IN THE DETECTOR. ***  Every drain row used
`WDCC_WRITE` with `write_count = 1`, so the multi-sector half of BOTH the guard and the
announce arm -- code #478 itself added -- had no row at all.  Four mutants swept all 60
rows on that one gap.

AND A SHAPE-ONLY ROW DOES NOT CLOSE IT.  A seat's first attempt asserted "one write, 1024
bytes" and a mutant PASSED it: with the modulus weakened to 512 the drain fires at
occupancy 512 with count=2, which is the right SHAPE at the wrong MOMENT.  That is
`row_partial_sector`'s lesson, which the WRITEMULTI arm never received.

So the row pins the MOMENT: 511 stores must produce ZERO writes at occupancy 1022, and
the 512th must produce exactly one write of 1024.
"""
import io

NL = chr(10)
DET = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\diff_wdc_identify.c"

ROW = r'''

/*  WRITEMULTI -- the arm that had NO ROW AT ALL.
 *
 *  Every drain row in this file used WDCC_WRITE with write_count = 1, so the
 *  multi-sector half of the guard AND of the announce arm `#478` added was
 *  untested.  A seat measured FOUR mutants sweeping all 60 rows on that one gap,
 *  including one that reads as pure de-duplication -- folding the two arms, since
 *  they differ only in a modulus -- and writes 131,072 bytes.
 *
 *  THE MOMENT IS PINNED, NOT JUST THE SHAPE.  A first attempt asserted "one write,
 *  1024 bytes" and a mutant passed it by draining at occupancy 512 with count=2:
 *  the right shape at the wrong moment.  511 stores must drain NOTHING.
 */
static void row_writemulti_moment(void)
{
	struct wdc_data d;
	unsigned char buf[8];
	int i;

	memset(&d, 0, sizeof(d));
	d.addr_mult  = 1;
	d.io_enabled = 1;
	d.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
	d.irq.interrupt_assert = arm_sink;
	if (d.inbuf == NULL) {
		printf("  SETUP writemulti inbuf failed\n");
		return;
	}

	d.write_in_progress = WDCC_WRITEMULTI;
	d.write_count  = 2;
	d.write_offset = 0xf000;

	stub_disk_writes = 0;
	stub_disk_bytes = 0;
	stub_disk_first = -1;

	/*  511 two-byte stores = 1022 bytes: two bytes short of two sectors.  */
	for (i = 0; i < 511; i++) {
		buf[0] = 0x7c; buf[1] = 0x7c;
		buf[2] = 0; buf[3] = 0;
		dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_WRITE, &d);
	}

	rows ++;
	if (stub_disk_writes != 0) {
		printf("  FAIL %-38s %i w at occupancy 1022\n",
		    "WRITEMULTI partial does not drain", stub_disk_writes);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "WRITEMULTI partial does not drain", stub_disk_writes);
	}

	/*  the completing store: exactly one write of BOTH sectors, guest bytes.  */
	buf[0] = 0x7c; buf[1] = 0x7c;
	buf[2] = 0; buf[3] = 0;
	dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_WRITE, &d);

	rows ++;
	if (stub_disk_writes != 1 || stub_disk_bytes != 1024 ||
	    stub_disk_first != 0x7c) {
		printf("  FAIL %-38s %i w, %i b, first=0x%02x\n",
		    "WRITEMULTI drains both sectors once",
		    stub_disk_writes, stub_disk_bytes, stub_disk_first);
		failures ++;
	} else {
		printf("  ok   %-38s %i w, %i b\n",
		    "WRITEMULTI drains both sectors once",
		    stub_disk_writes, stub_disk_bytes);
	}

	free(d.inbuf);
}


/*  THE LEFTOVER DOOR MUST STAY SHUT ON THE SECOND BAD-LEN STORE TOO.
 *
 *  Named by a seat as the highest-plausibility slip: move `badlen_this = 1;`
 *  inside the `if (!d->warned_badlen)` block -- one line, and it looks like
 *  tidying the latch.  Because `warned_badlen` latches for the device's life,
 *  EVERY bad-length store after the first then drains 512 bytes of unread payload
 *  to the guest's LBA.
 *
 *  The existing leftover row uses ONE bad-len store and cannot see it.
 */
static void row_leftover_second_badlen(void)
{
	struct wdc_data d;
	unsigned char buf[8];
	int i;

	memset(&d, 0, sizeof(d));
	d.addr_mult  = 1;
	d.io_enabled = 1;
	d.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
	d.irq.interrupt_assert = arm_sink;
	if (d.inbuf == NULL) {
		printf("  SETUP second_badlen inbuf failed\n");
		return;
	}

	/*  an unread payload, marked so the oracle names WHICH bytes escaped  */
	for (i = 0; i < 512; i++)
		wdc_addtoinbuf(&d, 0xbe);

	d.write_in_progress = WDCC_WRITE;
	d.write_count  = 1;
	d.write_offset = 0x11000;

	/*  the FIRST bad-len store also arms #337's latch  */
	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 8, MEM_WRITE, &d);

	/*  the SECOND is the one under test: the latch is now set, so a fix that
	    ties badlen_this to it stops declining here.  */
	stub_disk_writes = 0;
	stub_disk_first = -1;
	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 8, MEM_WRITE, &d);

	rows ++;
	if (stub_disk_writes != 0) {
		printf("  FAIL %-38s %i write(s), first=0x%02x\n",
		    "leftover safe on the 2nd bad-len too",
		    stub_disk_writes, stub_disk_first);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "leftover safe on the 2nd bad-len too", stub_disk_writes);
	}

	free(d.inbuf);
}

'''

s = io.open(DET, encoding="utf-8", newline="").read()
anchor = NL + NL + "static void row_arm_overrun(void)"
assert s.count(anchor) == 1, "anchor %d" % s.count(anchor)
reg = chr(9) + "row_badlen_no_dispatch();" + NL
assert s.count(reg) == 1, "reg %d" % s.count(reg)

for lbl in ("WRITEMULTI partial does not drain", "WRITEMULTI drains both sectors once",
            "leftover safe on the 2nd bad-len too"):
    assert len(lbl) < 38, "label %d chars: %s" % (len(lbl), lbl)
    print("  label ok (%2d < 38): %s" % (len(lbl), lbl))

s = s.replace(anchor, ROW + NL + "static void row_arm_overrun(void)", 1)
s = s.replace(reg, reg + chr(9) + "row_writemulti_moment();" + NL +
              chr(9) + "row_leftover_second_badlen();" + NL, 1)
for a, b in [("if (rows != 75) {", "if (rows != 78) {"),
             ("rows = %i, want 75", "rows = %i, want 78")]:
    assert s.count(a) == 1, "%r %d" % (a, s.count(a))
    s = s.replace(a, b, 1)
io.open(DET, "w", encoding="utf-8", newline="").write(s)
print("  three rows appended, pin -> 78")
