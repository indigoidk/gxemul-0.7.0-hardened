"""Is the ring residue really UNRECOVERABLE?  Premise 5 of the #479 brief says yes.
A packet-fed seat spotted that the brief's OWN inlined facts admit a drain path that
clears it, and asked for it to be examined.

The candidate recovery: residue R sits in the ring; the guest issues WRITE SECTORS and
streams (512 - R) bytes; occupancy reaches 512, the drain fires, and the tail advances
512 -- leaving the ring empty.

If that works, `wdcringnoflush` is recoverable and its severity drops.  BUT the drain
writes the ring's FIRST 512 bytes, and the first R of those are the residue -- so the
"recovery" would hand the guest's own sector R bytes of someone else's data.

Recoverable-but-corrupting and unrecoverable are different dispositions, and neither is
what the brief claims.  Measured rather than argued.
"""
import io

NL = chr(10)
DET = (r"C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-CC-GXEMUL"
       r"\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\wip\regress"
       r"\diff_wdc_identify.c")

ROW = r'''

/*  PREMISE 5 UNDER TEST: is the ring residue actually UNRECOVERABLE?
 *
 *  The #479 brief asserts it is, having measured that neither ATAPI_PKT_CMD nor
 *  ATAPI_SOFT_RESET flushes.  A packet-fed seat pointed out that the brief's own
 *  inlined facts admit a third path nobody examined: the DRAIN advances the tail.
 *
 *  So: leave 20 bytes of residue, arm a WRITE, and stream 492 bytes.  Occupancy
 *  reaches 512, the drain fires, the tail advances 512 -- and the ring is empty.
 *
 *  If that is what happens, "unrecoverable" is wrong.  But the drain writes the
 *  ring's FIRST 512 bytes, and the first 20 of those are the residue, so the
 *  guest's sector is handed 20 bytes of a previous transfer's data.  The row
 *  therefore checks BOTH: that the ring clears, and what reached the disk.
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

	/*  residue from an under-drained transfer, marked 0xAA  */
	for (i = 0; i < 20; i++)
		wdc_addtoinbuf(&d, 0xaa);

	/*  the guest arms an ordinary sector write and streams its OWN data, 0x55  */
	d.seccnt = 1;
	d.sector = 1;
	wdc_command(fake_cpu(), &d, WDCC_WRITE);

	stub_disk_writes = 0;
	stub_disk_bytes = 0;
	stub_disk_first = -1;
	for (i = 0; i < 246; i++) {		/*  246 * 2 = 492 bytes  */
		buf[0] = 0x55; buf[1] = 0x55;
		buf[2] = 0; buf[3] = 0;
		dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_WRITE, &d);
	}

	occ = d.inbuf_head - d.inbuf_tail;
	while (occ < 0)
		occ += WDC_INBUF_SIZE;

	/*  Q1: did the ring clear?  If it did, "unrecoverable" is FALSE.  */
	rows ++;
	if (occ != 0) {
		printf("  FAIL %-38s occupancy %i after the drain\n",
		    "P5: a write drains the residue", occ);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "P5: a write drains the residue", occ);
	}

	/*  Q2: and WHAT reached the disk?  0xaa is the residue; 0x55 is the guest's
	    own byte.  If the first byte written is 0xaa, the recovery contaminated
	    a legitimate sector -- which is a different defect, not a recovery.  */
	rows ++;
	if (stub_disk_first != 0x55) {
		printf("  FAIL %-38s first=0x%02x, guest wrote 0x55\n",
		    "P5: recovered sector is the guest's",
		    stub_disk_first);
		failures ++;
	} else {
		printf("  ok   %-38s first=0x%02x\n",
		    "P5: recovered sector is the guest's",
		    stub_disk_first);
	}

	stub_disk_exists = 0;
	if (d.atapi_st != NULL) {
		free(d.atapi_st->data_in);
		free(d.atapi_st->cmd);
		free(d.atapi_st);
	}
	free(d.inbuf);
}

'''

s = io.open(DET, encoding="utf-8", newline="").read()

anchor = NL + NL + "static void row_arm_overrun(void)"
assert s.count(anchor) == 1, "anchor %d" % s.count(anchor)
s = s.replace(anchor, ROW + NL + "static void row_arm_overrun(void)", 1)

reg = chr(9) + "row_ring_not_flushed();" + NL
assert s.count(reg) == 1, "reg %d" % s.count(reg)
s = s.replace(reg, reg + chr(9) + "row_residue_recovery();" + NL, 1)

for a, b in [("if (rows != 57) {", "if (rows != 59) {"),
             ("rows = %i, want 57", "rows = %i, want 59")]:
    assert s.count(a) == 1, "%r %d" % (a, s.count(a))
    s = s.replace(a, b, 1)

for lbl in ("P5: a write drains the residue",
            "P5: recovered sector is the guest's"):
    assert len(lbl) < 38, "label %d chars: %s" % (len(lbl), lbl)
    print("  label ok (%2d < 38): %s" % (len(lbl), lbl))

io.open(DET, "w", encoding="utf-8", newline="").write(s)
print("  P5 rows appended to the wip tree, pin -> 59")
