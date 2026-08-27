"""wdcringnoflush -- REPRODUCTION, appended to the SAME tree as wdcwipclear.

Both defects are "a new command does not reset the state the old one left", both live in
`wdc_command()`, and both are observable through the same detector with no new oracle --
which is exactly the round-scope rule's test for whether two sites may share a round.
Building them against one detector is how that question gets ANSWERED rather than assumed.

Measured by the Opus seat: ATAPI_PKT_CMD never flushes the input ring, and neither reset
path does either, so an under-drained DATA-IN leaves occupancy climbing 32 -> 44 -> 56 ->
68 and every later CDB is dropped forever.  The guest has no recovery.
"""
import io, os

NL, T = chr(10), chr(9)
DET = (r"C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-CC-GXEMUL"
       r"\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\wip\regress"
       r"\diff_wdc_identify.c")

ROW = r'''

/*  wdcringnoflush -- REPRODUCTION.  A new command does not flush the input ring.
 *
 *  MEASURED by a seat: under-drain a DATA-IN transfer and the residue is never
 *  cleared.  ATAPI_PKT_CMD does not flush it, ATAPI_SOFT_RESET does not flush it,
 *  and the ALT-CTRL device reset does not flush it -- so occupancy only ever
 *  climbs, and once it can no longer EQUAL 12 the CDB dispatch is dead for the
 *  life of the device.  There is no sequence a guest can issue to recover.
 *
 *  Same function and same semantic class as `wdcwipclear` -- "a new command must
 *  reset what the old one left" -- and observable through the same oracle, which
 *  is why both are built against one detector.
 *
 *  The in-tree idiom for the fix already exists: dev_asc.c's dev_asc_fifo_flush(),
 *  called from NCRCMD_FLUSH and NCRCMD_RSTCHIP.
 */
static void row_ring_not_flushed(void)
{
	struct wdc_data d;
	int occ;

	memset(&d, 0, sizeof(d));
	d.addr_mult  = 1;
	d.io_enabled = 1;
	d.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
	d.irq.interrupt_assert = arm_sink;
	if (d.inbuf == NULL) {
		printf("  SETUP flush inbuf failed\n");
		return;
	}

	stub_disk_exists = 1;

	/*  an under-drained transfer: 20 bytes the guest never read back  */
	{
		int i;
		for (i = 0; i < 20; i++)
			wdc_addtoinbuf(&d, 0x5a);
	}

	occ = d.inbuf_head - d.inbuf_tail;
	while (occ < 0)
		occ += WDC_INBUF_SIZE;
	rows ++;
	if (occ != 20) {
		printf("  FAIL %-38s occupancy %i, want 20\n",
		    "LIVENESS: the residue is really there", occ);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "LIVENESS: the residue is really there", occ);
	}

	/*  a fresh packet command.  A device that resets its command state must not
	    carry the previous transfer's residue into the new CDB.  */
	wdc_command(fake_cpu(), &d, ATAPI_PKT_CMD);

	occ = d.inbuf_head - d.inbuf_tail;
	while (occ < 0)
		occ += WDC_INBUF_SIZE;
	rows ++;
	if (occ != 0) {
		printf("  FAIL %-38s %i bytes survive the command\n",
		    "a packet command flushes the ring", occ);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "a packet command flushes the ring", occ);
	}

	/*  and a SOFT RESET is the guest's documented recovery.  If neither the
	    command nor the reset clears it, nothing does.  */
	wdc_command(fake_cpu(), &d, ATAPI_SOFT_RESET);

	occ = d.inbuf_head - d.inbuf_tail;
	while (occ < 0)
		occ += WDC_INBUF_SIZE;
	rows ++;
	if (occ != 0) {
		printf("  FAIL %-38s %i bytes survive a soft reset\n",
		    "a soft reset flushes the ring", occ);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "a soft reset flushes the ring", occ);
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

reg = T + "row_wip_not_cleared();" + NL
assert s.count(reg) == 1, "reg %d" % s.count(reg)
s = s.replace(reg, reg + T + "row_ring_not_flushed();" + NL, 1)

for a, b in [("if (rows != 54) {", "if (rows != 57) {"),
             ("rows = %i, want 54", "rows = %i, want 57")]:
    assert s.count(a) == 1, "%r %d" % (a, s.count(a))
    s = s.replace(a, b, 1)

for lbl in ("LIVENESS: the residue is really there",
            "a packet command flushes the ring",
            "a soft reset flushes the ring"):
    assert len(lbl) < 38, "label %d chars: %s" % (len(lbl), lbl)
    print("  label ok (%2d < 38): %s" % (len(lbl), lbl))

io.open(DET, "w", encoding="utf-8", newline="").write(s)
print("  ring-flush rows appended, pin -> 57")
