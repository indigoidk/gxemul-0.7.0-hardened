"""The ACCEPT ROW that inverts `M2_curcmd`'s disposition.

`#477` recorded that escape as REAL COVERAGE DEBT, on the warrant that the ALT-CTRL arm
sets `cur_command = COMMAND_RESET` without clearing the flag, so the discriminating state
is reachable.  The warrant is CORRECT and the CONCLUSION IS INVERTED, which the Opus seat
measured on `#477`'s pass 2:

    L3   PKT + ALTCTL + CDB     shipped: dispatches=1  M_curcmd: dispatches=0, occ=12
    L3b  a second CDB           shipped: dispatches=2  M_curcmd: dispatches=0, occ=24
    L3c  a third CDB            shipped: dispatches=3  M_curcmd: dispatches=0, occ=36

Zero of three LEGAL packet commands dispatch, and the wedge survives `cur_command`
returning to 0xA0 because the 12-byte residue then blocks it forever.

So the reachability of that state is what makes the conjunct DANGEROUS, not what makes it
valuable.  Filing it as "coverage debt" invites a future round to discharge the debt by
ADDING the conjunct -- which ships a permanent wedge.  The correct disposition is an
ACCEPT ROW, which the de-escalation clause calls part of the fix's cost.
"""
import io

NL = chr(10)
DET = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\diff_wdc_identify.c"

ROW = r'''

/*  THE ACCEPT ROW FOR THE `cur_command` ESCAPE -- and it exists because the round's
 *  own disposition was INVERTED.
 *
 *  `#477` filed that escape as REAL COVERAGE DEBT: the ALT-CTRL arm sets
 *  `cur_command = COMMAND_RESET` without clearing `atapi_cmd_in_progress`, so the
 *  state that distinguishes the mutant is reachable.  That warrant is right.  The
 *  conclusion drawn from it was backwards.
 *
 *  MEASURED by a seat, through real register accesses: adding
 *  `&& cur_command == ATAPI_PKT_CMD` makes ZERO OF THREE legal packet commands
 *  dispatch, and the wedge is permanent -- the 12-byte residue blocks the dispatch
 *  even after `cur_command` returns to 0xA0.  The reachability is what makes that
 *  conjunct DANGEROUS.
 *
 *  A "coverage debt" filing invites a future round to close the debt by ADDING the
 *  conjunct.  This row makes that edit RED instead: a legal CDB delivered after an
 *  ALT-CTRL write must still dispatch.
 */
static void row_altctl_cdb_accept(void)
{
	struct wdc_data d;
	unsigned char buf[4];
	int i;

	memset(&d, 0, sizeof(d));
	d.addr_mult  = 1;
	d.io_enabled = 1;
	d.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
	d.irq.interrupt_assert = arm_sink;
	if (d.inbuf == NULL) {
		printf("  SETUP altctl inbuf failed\n");
		return;
	}

	stub_disk_exists = 1;
	stub_datain_len = 64;

	/*  a real packet command  */
	wdc_command(fake_cpu(), &d, ATAPI_PKT_CMD);

	/*  an ALT-CTRL write with WDCTL_4BIT, which this device treats as a reset
	    latch: it sets cur_command = COMMAND_RESET and clears NOTHING else.
	    Guest-reachable with one ordinary register write.  */
	memset(buf, 0, sizeof(buf));
	buf[0] = WDCTL_4BIT;
	/*  *** THE ALT-CTRL REGISTER IS A SEPARATE REGISTERED DEVICE, and the first
	    version of this row wrote to `dev_wdc_access` at relative_addr 0 -- which
	    is `wd_data`.  It pushed a byte into the RING, so occupancy reached 13
	    instead of 12 and the CDB never dispatched.  The row RED on the shipped
	    build, which is a mis-cut row and not a defect. ***  */
	dev_wdc_altstatus_access(fake_cpu(), NULL, 0, buf, 1, MEM_WRITE, &d);

	rows ++;
	if (d.atapi_cmd_in_progress != 1 || d.atapi_phase != PHASE_CMDOUT) {
		printf("  FAIL %-38s flag %i phase 0x%x\n",
		    "LIVENESS: altctl keeps packet live",
		    d.atapi_cmd_in_progress, d.atapi_phase);
		failures ++;
	} else {
		printf("  ok   %-38s flag %i\n",
		    "LIVENESS: altctl keeps packet live",
		    d.atapi_cmd_in_progress);
	}

	/*  the CDB the guest was always entitled to send  */
	stub_scsi_cmds = 0;
	for (i = 0; i < 6; i++) {
		buf[0] = 0x12; buf[1] = 0x00;
		buf[2] = 0; buf[3] = 0;
		dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_WRITE, &d);
	}

	rows ++;
	if (stub_scsi_cmds != 1) {
		printf("  FAIL %-38s dispatched %i, want 1\n",
		    "a CDB after altctl still dispatches", stub_scsi_cmds);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "a CDB after altctl still dispatches", stub_scsi_cmds);
	}

	stub_datain_len = 0;
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

reg = chr(9) + "row_stale_phase_write();" + NL
assert s.count(reg) == 1, "reg %d" % s.count(reg)
s = s.replace(reg, reg + chr(9) + "row_altctl_cdb_accept();" + NL, 1)

for a, b in [("if (rows != 55) {", "if (rows != 57) {"),
             ("rows = %i, want 55", "rows = %i, want 57")]:
    assert s.count(a) == 1, "%r %d" % (a, s.count(a))
    s = s.replace(a, b, 1)

for lbl in ("LIVENESS: altctl keeps packet live",
            "a CDB after altctl still dispatches"):
    assert len(lbl) < 38, "label %d chars: %s" % (len(lbl), lbl)
    print("  label ok (%2d < 38): %s" % (len(lbl), lbl))

io.open(DET, "w", encoding="utf-8", newline="").write(s)
print("  row_altctl_cdb_accept appended, pin -> 57")
