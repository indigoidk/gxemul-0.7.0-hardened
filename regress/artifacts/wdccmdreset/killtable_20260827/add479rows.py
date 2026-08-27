"""The three rows #479's own mutants require, each named by the Opus seat.

Added BEFORE the kill table, not after: a mutant scored as an escape because no row
was built for it is not a measurement, it is a gap wearing a result's clothes.

  IDENTIFY / READ  the helper flushes the ring, and BOTH commands load their answer
                   INTO that ring afterwards.  Move only the RING FLUSH to the end of
                   wdc_command and all three pinned reproductions stay GREEN while the
                   guest's IDENTIFY response and freshly-read sector are destroyed.
                   READ is the hot path -- a boot issues it more often than IDENTIFY.

  latch survival   the helper invites "also clear the warned_* flags" as a completion.
                   That undoes #337/#464, and is strictly worse than the same mistake
                   in dev_asc.c because wdc_command runs far more often than a chip
                   reset.  dev_asc.c says so at its own latch declarations.
"""
import io

NL = chr(10)
DET = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\diff_wdc_identify.c"

ROW = r'''

/*  THE THREE ROWS `#479`'s OWN MUTANTS REQUIRE.  Each was named by a seat that
 *  built the mutant and found the existing suite blind to it.
 *
 *  `#479` flushes the ring at the TOP of wdc_command() -- and IDENTIFY and READ
 *  both load their answer INTO that ring further down the same function.  Move
 *  only the RING FLUSH to the end and all three pinned reproductions stay GREEN
 *  while the guest's data is destroyed.  That mutant reads as the more principled
 *  placement, which is what makes it worth a row.
 *
 *  READ is deliberately here as well as IDENTIFY: a boot issues WDCC_READ far
 *  more often than WDCC_IDENTIFY, so a round that rows only IDENTIFY has pinned
 *  the rarer path.
 */
static void row_command_fills_ring(void)
{
	struct wdc_data d;
	int occ;

	memset(&d, 0, sizeof(d));
	d.addr_mult  = 1;
	d.io_enabled = 1;
	d.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
	d.irq.interrupt_assert = arm_sink;
	if (d.inbuf == NULL) {
		printf("  SETUP fills_ring inbuf failed\n");
		return;
	}

	stub_disk_exists = 1;

	/*  IDENTIFY must leave its response queued for the guest to read back.  */
	wdc_command(fake_cpu(), &d, WDCC_IDENTIFY);
	occ = d.inbuf_head - d.inbuf_tail;
	while (occ < 0)
		occ += WDC_INBUF_SIZE;

	rows ++;
	if (occ != 512) {
		printf("  FAIL %-38s %i queued, want 512\n",
		    "IDENTIFY leaves its answer queued", occ);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "IDENTIFY leaves its answer queued", occ);
	}

	/*  and the HOT path: an ordinary READ fills the ring the same way.  */
	d.inbuf_head = d.inbuf_tail = 0;
	d.seccnt = 1;
	d.sector = 1;
	wdc_command(fake_cpu(), &d, WDCC_READ);
	occ = d.inbuf_head - d.inbuf_tail;
	while (occ < 0)
		occ += WDC_INBUF_SIZE;

	rows ++;
	if (occ != 512) {
		printf("  FAIL %-38s %i queued, want 512\n",
		    "READ leaves a sector queued", occ);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "READ leaves a sector queued", occ);
	}

	stub_disk_exists = 0;
	free(d.inbuf);
}


/*  A LATCH MUST SURVIVE THE NEXT COMMAND.
 *
 *  `#479`'s helper clears three things a new command must not inherit.  Adding the
 *  `warned_*` flags to that list reads as COMPLETING it -- and undoes `#337` and
 *  `#464`, because those latches exist to stop a guest-drivable log flood.
 *
 *  It is strictly worse here than the equivalent mistake would be in dev_asc.c,
 *  which states the rule outright at its own latch declarations: the latches are
 *  "Deliberately NOT cleared by dev_asc_reset() or dev_asc_fifo_flush(): a guest
 *  could otherwise re-arm the flood."  `wdc_command()` runs far more often than a
 *  chip reset, so a guest alternating two opcodes would flood forever.
 *
 *  The oracle counts EMISSIONS, not the flag: a mutant that clears the latch while
 *  something else happens to suppress the message would pass a flag check.
 */
static void row_latch_survives_command(void)
{
	struct wdc_data d;
	unsigned char buf[8];
	int first, second;

	memset(&d, 0, sizeof(d));
	d.addr_mult  = 1;
	d.io_enabled = 1;
	d.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
	d.irq.interrupt_assert = arm_sink;
	if (d.inbuf == NULL) {
		printf("  SETUP latch inbuf failed\n");
		return;
	}
	d.write_in_progress = WDCC_WRITE;
	d.write_count  = 1;
	d.write_offset = 0xe000;

	/*  fire the drain announce once  */
	stub_fatals = 0; stub_drain_msgs = 0;
	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 8, MEM_WRITE, &d);
	first = stub_drain_msgs;

	/*  a new command arrives, then the same provoking access again.  The latch
	    must NOT have been re-armed by the command.  */
	stub_disk_exists = 1;
	d.seccnt = 1;
	d.sector = 1;
	wdc_command(fake_cpu(), &d, WDCC_WRITE);
	stub_disk_exists = 0;

	stub_fatals = 0; stub_drain_msgs = 0;
	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 8, MEM_WRITE, &d);
	second = stub_drain_msgs;

	rows ++;
	if (first < 1) {
		printf("  FAIL %-38s never armed (%i)\n",
		    "LIVENESS: the announce fired once", first);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "LIVENESS: the announce fired once", first);
	}

	rows ++;
	if (second != 0) {
		printf("  FAIL %-38s re-armed by a command (%i)\n",
		    "a latch survives the next command", second);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "a latch survives the next command", second);
	}

	free(d.inbuf);
}

'''

s = io.open(DET, encoding="utf-8", newline="").read()

anchor = NL + NL + "static void row_arm_overrun(void)"
assert s.count(anchor) == 1, "anchor %d" % s.count(anchor)
reg = chr(9) + "row_devctl_preserves_write();" + NL
assert s.count(reg) == 1, "reg %d" % s.count(reg)

for lbl in ("IDENTIFY leaves its answer queued", "READ leaves a sector queued",
            "LIVENESS: the announce fired once", "a latch survives the next command"):
    assert len(lbl) < 38, "label %d chars: %s" % (len(lbl), lbl)
    print("  label ok (%2d < 38): %s" % (len(lbl), lbl))

s = s.replace(anchor, ROW + NL + "static void row_arm_overrun(void)", 1)
s = s.replace(reg, reg + chr(9) + "row_command_fills_ring();" + NL +
              chr(9) + "row_latch_survives_command();" + NL, 1)

for a, b in [("if (rows != 62) {", "if (rows != 66) {"),
             ("rows = %i, want 62", "rows = %i, want 66")]:
    assert s.count(a) == 1, "%r %d" % (a, s.count(a))
    s = s.replace(a, b, 1)

io.open(DET, "w", encoding="utf-8", newline="").write(s)
print("  four rows appended, pin -> 66")
