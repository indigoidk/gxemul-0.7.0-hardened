"""The PARTIAL-SECTOR row, named by the codex seat and MEASURED necessary.

`M10_modinv` inverts the modulus (`== 0` -> `!= 0`) and swept all 50 rows.  The accept
row cannot see it: with `!= 0` the drain fires at occupancy 2 rather than 512, and the
accept row still observes exactly one write of 512 bytes -- the right shape at the wrong
moment.

codex's prescription, verbatim in effect: occupancy 0, 1 and needed-1 must produce ZERO
writes, and exactly `needed` must produce ONE write of exactly `needed` bytes at the
expected offset.  Row 0 exists (the empty rows); this adds the partial cases and pins
the offset on the accept side.
"""
import io, os

NL = chr(10)
SCR = (r"C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-CC-GXEMUL"
       r"\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad")
DET = os.path.join(SCR, "drain", "regress", "diff_wdc_identify.c")

ROW = r'''

/*  THE PARTIAL-SECTOR ROW.  Named by the codex seat after `M10_modinv` -- the
 *  modulus inverted from `== 0` to `!= 0` -- swept a 50-row table clean.
 *
 *  That mutant does not open the empty-ring door (the `inbuf_len > 0` half still
 *  holds), so every corruption row stays green.  What it does is authorise a
 *  512-byte disk write on ONE buffered byte, while exactly 512 bytes fail to
 *  drain.  The accept row cannot see it either: it observes one write of 512
 *  bytes, which is the right SHAPE at the wrong MOMENT.
 *
 *  So the sufficiency condition needs pinning from below as well as at the
 *  boundary: occupancy 1 and needed-1 must write NOTHING.
 */
static void row_partial_sector(void)
{
	struct wdc_data j;
	unsigned char buf[8];
	int i;

	memset(&j, 0, sizeof(j));
	j.addr_mult  = 1;
	j.io_enabled = 1;
	j.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
	j.irq.interrupt_assert = arm_sink;
	if (j.inbuf == NULL) {
		printf("  SETUP partial_sector inbuf failed\n");
		return;
	}

	j.write_in_progress = WDCC_WRITE;
	j.write_count  = 1;
	j.write_offset = 0xc000;

	stub_disk_writes = 0;
	stub_disk_bytes = 0;

	/*  255 two-byte stores: occupancy climbs 2..510, one short of a sector.
	    NOT ONE of them may reach the disk.  */
	for (i = 0; i < 255; i++) {
		buf[0] = 0x33; buf[1] = 0x33;
		buf[2] = 0; buf[3] = 0;
		dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_WRITE, &j);
	}

	rows ++;
	if (stub_disk_writes != 0) {
		printf("  FAIL %-38s %i write(s) at occupancy < 512\n",
		    "a partial sector does not drain", stub_disk_writes);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "a partial sector does not drain", stub_disk_writes);
	}

	/*  the 256th store completes the sector: exactly one write, exactly 512
	    bytes, at exactly the offset the command named.  */
	buf[0] = 0x33; buf[1] = 0x33;
	buf[2] = 0; buf[3] = 0;
	dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_WRITE, &j);

	rows ++;
	if (stub_disk_writes != 1 || stub_disk_bytes != 512 ||
	    stub_disk_offset != 0xc000) {
		printf("  FAIL %-38s %i w, %i b, off 0x%lx\n",
		    "completing store drains one sector",
		    stub_disk_writes, stub_disk_bytes, stub_disk_offset);
		failures ++;
	} else {
		printf("  ok   %-38s %i w, %i b\n",
		    "completing store drains one sector",
		    stub_disk_writes, stub_disk_bytes);
	}

	free(j.inbuf);
}

'''

s = io.open(DET, encoding="utf-8", newline="").read()

anchor = NL + NL + "static void row_arm_overrun(void)"
assert s.count(anchor) == 1, "anchor %d" % s.count(anchor)
s = s.replace(anchor, ROW + NL + "static void row_arm_overrun(void)", 1)

reg = chr(9) + "row_badlen_then_legal();" + NL
assert s.count(reg) == 1, "reg %d" % s.count(reg)
s = s.replace(reg, reg + chr(9) + "row_partial_sector();" + NL, 1)

for a, b in [("if (rows != 50) {", "if (rows != 52) {"),
             ("rows = %i, want 50", "rows = %i, want 52")]:
    assert s.count(a) == 1, "%r %d" % (a, s.count(a))
    s = s.replace(a, b, 1)

for lbl in ("a partial sector does not drain",
            "completing store drains one sector"):
    assert len(lbl) < 38, "label %d chars: %s" % (len(lbl), lbl)
    print("  label ok (%2d < 38): %s" % (len(lbl), lbl))

#  ASSERT BEFORE WRITING -- the first version wrote the file and THEN checked,
#  so a 38-char label landed in the detector before the guard fired.
io.open(DET, "w", encoding="utf-8", newline="").write(s)
print("  partial-sector rows appended, pin -> 52")
