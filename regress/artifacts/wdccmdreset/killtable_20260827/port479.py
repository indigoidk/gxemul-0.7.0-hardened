"""Port #479's REPRODUCTION rows from the scratchpad into the repo detector.

*** THE KILL TABLE CAUGHT THIS, WHICH IS WHAT IT IS FOR. ***  `MdNoRing` -- simply
deleting the ring flush -- swept a clean 66 rows.  The reason was not a subtle mutant:
the rows that reproduce the three defects F-narrow fixes were still in the scratchpad
tree, never ported.  The round was about to ship a fix whose own reproductions lived
outside the repository, testing its CONSEQUENCES (phase, announce, accept) but not its
SUBJECT.

Two rows are copied verbatim.  `row_residue_recovery` is NOT: it pinned the defect's
shape and would go red under the fix, so it is re-cut here to pin what the round
actually establishes -- L1 construction, since it never shipped.
"""
import io, re

NL, T = chr(10), chr(9)
SRC = (r"C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-CC-GXEMUL"
       r"\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\wip\regress"
       r"\diff_wdc_identify.c")
DST = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\diff_wdc_identify.c"

src = io.open(SRC, encoding="utf-8", newline="").read().split(NL)
dst = io.open(DST, encoding="utf-8", newline="").read()


def lift(name):
    """Copy a whole function plus its leading comment block, verbatim."""
    i = next(k for k, l in enumerate(src) if l.startswith("static void %s(" % name))
    j = next(k for k in range(i + 1, len(src)) if src[k] == "}")
    head = i
    while head > 0 and (src[head - 1].startswith(" *") or src[head - 1].startswith("/*")):
        head -= 1
    return NL.join(src[head:j + 1])


blocks = []
for n in ("row_wip_not_cleared", "row_ring_not_flushed"):
    b = lift(n)
    assert "stub_disk_exists" in b, "%s does not use the exists control" % n
    blocks.append(b)
    print("  lifted %s (%d lines)" % (n, b.count(NL) + 1))

RECUT = r'''/*  THE RESIDUE ROW, RE-CUT.  L1 construction: this never shipped.
 *
 *  Its scratchpad form pinned the DEFECT'S SHAPE -- that a residue-contaminated
 *  drain fires, leaving occupancy 0 with `first=0xaa`.  That form earned its keep:
 *  it refuted this round's own "the residue is unrecoverable" premise and turned a
 *  denial-of-service claim into a data-integrity one.
 *
 *  But it goes red under every candidate fix, for the FIXTURE's reason rather than
 *  the code's, so it is replaced rather than kept alongside -- two rows disagreeing
 *  about one behaviour is how a suite stops meaning anything.
 *
 *  The new pin is the round's actual claim: after a new command the residue is gone,
 *  and the guest's next sector reaches the disk as the guest wrote it.
 */
static void row_residue_recovery(void)
{
	struct wdc_data d;
	unsigned char buf[8];
	int i, occ;

	memset(&d, 0, sizeof(d));
	d.addr_mult  = 1;
	d.io_enabled = 1;
	d.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
	d.irq.interrupt_assert = arm_sink;
	if (d.inbuf == NULL) {
		printf("  SETUP residue inbuf failed\n");
		return;
	}

	stub_disk_exists = 1;
	for (i = 0; i < 20; i++)
		wdc_addtoinbuf(&d, 0xaa);

	d.seccnt = 1;
	d.sector = 1;
	wdc_command(fake_cpu(), &d, WDCC_WRITE);

	occ = d.inbuf_head - d.inbuf_tail;
	while (occ < 0)
		occ += WDC_INBUF_SIZE;

	rows ++;
	if (occ != 0) {
		printf("  FAIL %-38s %i bytes survive the command\n",
		    "a new command leaves an empty ring", occ);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "a new command leaves an empty ring", occ);
	}

	/*  the guest-visible consequence: one sector, its OWN bytes.  A tree that
	    keeps the residue drains 20 bytes early and puts 0xaa at the head.  */
	stub_disk_writes = 0;
	stub_disk_bytes = 0;
	stub_disk_first = -1;
	for (i = 0; i < 256; i++) {
		buf[0] = 0x55; buf[1] = 0x55;
		buf[2] = 0; buf[3] = 0;
		dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_WRITE, &d);
	}

	rows ++;
	if (stub_disk_writes != 1 || stub_disk_bytes != 512 ||
	    stub_disk_first != 0x55) {
		printf("  FAIL %-38s %i w, %i b, first=0x%02x\n",
		    "the sector after a command is guest's",
		    stub_disk_writes, stub_disk_bytes, stub_disk_first);
		failures ++;
	} else {
		printf("  ok   %-38s %i w, %i b\n",
		    "the sector after a command is guest's",
		    stub_disk_writes, stub_disk_bytes);
	}

	stub_disk_exists = 0;
	if (d.atapi_st != NULL) {
		free(d.atapi_st->data_in);
		free(d.atapi_st->cmd);
		free(d.atapi_st);
	}
	free(d.inbuf);
}'''
blocks.append(RECUT)

for lbl in ("a new command leaves an empty ring",
            "the sector after a command is guest's"):
    assert len(lbl) < 38, "label %d chars: %s" % (len(lbl), lbl)
    print("  label ok (%2d < 38): %s" % (len(lbl), lbl))

anchor = NL + NL + "static void row_arm_overrun(void)"
assert dst.count(anchor) == 1, "anchor %d" % dst.count(anchor)
dst = dst.replace(anchor, NL + NL + (NL + NL).join(blocks) + NL + NL +
                  "static void row_arm_overrun(void)", 1)

reg = T + "row_latch_survives_command();" + NL
assert dst.count(reg) == 1, "reg %d" % dst.count(reg)
dst = dst.replace(reg, reg + T + "row_wip_not_cleared();" + NL +
                  T + "row_ring_not_flushed();" + NL +
                  T + "row_residue_recovery();" + NL, 1)

#  2 + 3 + 2 = 7 new assertions
for a, b in [("if (rows != 66) {", "if (rows != 73) {"),
             ("rows = %i, want 66", "rows = %i, want 73")]:
    assert dst.count(a) == 1, "%r %d" % (a, dst.count(a))
    dst = dst.replace(a, b, 1)

io.open(DST, "w", encoding="utf-8", newline="").write(dst)
print("  ported into the repo detector, pin -> 73")
