"""The Device-Control ACCEPT ROW -- the one obligation BOTH sides of the split agree on.

The panel divided: three seats for F-narrow (ALT-CTRL is a separate round), codex for a
seventh option G (F-wide plus this row, with the helper hung off a CORRECTED WDCTL_RST).
They differ on SCOPE and agree on this row, so it is built first and the choice is made
with the instrument in place rather than before it.

*** AND IT IS THE ONLY INSTRUMENT THAT COULD EVER SEE THE REGRESSION. ***  Measured: no
gate in this tree arms a CDROM, so the COMMAND_RESET -> ATAPI-signature path is never
exercised by the battery.  A fix that cancels a pending write on an ordinary Device
Control write would be INVISIBLE to every rig.  That is an argument for the row existing
regardless of which option ships.

WHY 0x08 SPECIFICALLY, from cited driver source (grok seat):

    Linux libata        ap->ctl initialised to ATA_DEVCTL_OBS = 0x08, held as the
                        STEADY STATE between commands
    older OpenBSD       resets with 0x06 (bit 3 CLEAR), then writes 0x08 separately

So 0x08 is not an exotic value.  It is what the register spends most of its life holding,
and a guest may write it at any time -- including in the middle of a sector transfer.
"""
import io

NL = chr(10)
DET = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\diff_wdc_identify.c"

ROW = r'''

/*  THE DEVICE-CONTROL ACCEPT ROW.
 *
 *  A pending sector write must SURVIVE an ordinary Device Control write.  This row
 *  exists before the fix that needs it, because it is the only instrument in the
 *  tree that can see the regression it guards against: MEASURED, no gate arms a
 *  CDROM, so the ALT-CTRL/COMMAND_RESET path is never exercised by any rig.
 *
 *  0x08 is not an exotic value.  From cited driver source: Linux libata holds
 *  ATA_DEVCTL_OBS (0x08) as `ap->ctl`, the STEADY STATE between commands, and older
 *  OpenBSD resets with 0x06 (bit 3 clear) and then writes 0x08 separately.  A guest
 *  may write it at any moment, including mid-transfer.
 *
 *  So a future round that hangs a ring-flush or a writer-cancel off the ALT-CTRL arm
 *  -- which currently triggers on WDCTL_4BIT (0x08) rather than WDCTL_RST (0x04) --
 *  would cancel a legal transfer on a routine register write.  This row reds on that
 *  edit.  It is the de-escalation clause's accept side, built for a fix that has not
 *  shipped yet.
 */
static void row_devctl_preserves_write(void)
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
		printf("  SETUP devctl inbuf failed\n");
		return;
	}

	stub_disk_exists = 1;
	d.seccnt = 1;
	d.sector = 1;
	wdc_command(fake_cpu(), &d, WDCC_WRITE);

	/*  half the sector, then a perfectly ordinary Device Control write  */
	stub_disk_writes = 0;
	stub_disk_bytes = 0;
	stub_disk_first = -1;
	for (i = 0; i < 128; i++) {
		buf[0] = 0x6d; buf[1] = 0x6d;
		buf[2] = 0; buf[3] = 0;
		dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_WRITE, &d);
	}

	memset(buf, 0, sizeof(buf));
	buf[0] = WDCTL_4BIT;		/*  0x08 -- libata's steady state  */
	dev_wdc_altstatus_access(fake_cpu(), NULL, 0, buf, 1, MEM_WRITE, &d);

	/*  the transfer must still be armed and the queued bytes still queued  */
	rows ++;
	if (d.write_in_progress == 0) {
		printf("  FAIL %-38s writer cancelled by 0x08\n",
		    "a devctl write keeps the writer");
		failures ++;
	} else {
		printf("  ok   %-38s 0x%x\n",
		    "a devctl write keeps the writer", d.write_in_progress);
	}

	/*  finish the sector: it must land, and it must be the GUEST'S bytes  */
	for (i = 0; i < 128; i++) {
		buf[0] = 0x6d; buf[1] = 0x6d;
		buf[2] = 0; buf[3] = 0;
		dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_WRITE, &d);
	}

	rows ++;
	if (stub_disk_writes != 1 || stub_disk_bytes != 512 ||
	    stub_disk_first != 0x6d) {
		printf("  FAIL %-38s %i w, %i b, first=0x%02x\n",
		    "a devctl write does not lose bytes",
		    stub_disk_writes, stub_disk_bytes, stub_disk_first);
		failures ++;
	} else {
		printf("  ok   %-38s %i w, %i b\n",
		    "a devctl write does not lose bytes",
		    stub_disk_writes, stub_disk_bytes);
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

reg = chr(9) + "row_drain_announce();" + NL
assert s.count(reg) == 1, "reg %d" % s.count(reg)

for lbl in ("a devctl write keeps the writer",
            "a devctl write does not lose bytes"):
    assert len(lbl) < 38, "label %d chars: %s" % (len(lbl), lbl)
    print("  label ok (%2d < 38): %s" % (len(lbl), lbl))

s = s.replace(anchor, ROW + NL + "static void row_arm_overrun(void)", 1)
s = s.replace(reg, reg + chr(9) + "row_devctl_preserves_write();" + NL, 1)

for a, b in [("if (rows != 60) {", "if (rows != 62) {"),
             ("rows = %i, want 60", "rows = %i, want 62")]:
    assert s.count(a) == 1, "%r %d" % (a, s.count(a))
    s = s.replace(a, b, 1)

io.open(DET, "w", encoding="utf-8", newline="").write(s)
print("  row_devctl_preserves_write appended, pin -> 62")
