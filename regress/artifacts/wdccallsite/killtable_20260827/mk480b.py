"""#480 L2: two rows the opus seat costed and measured, closing 9 of 14 escapes.

The round's own restated clause (d) says a detector owes a row that reds if the call is
"conditioned, OR MOVED BELOW A DECISION POINT".  wdc_command() has TWO early returns and
this round covered ONE.  Moving the call below the FIRST (the no-disk guard) escapes all
85 rows and is WORSE THAN PRE-#479 -- so the round breaches the clause it just wrote.
That is L2: fix in-round however late.

  row_absent_drive_resets   MEASURED CAUSE: every one of the 17 wdc_command() calls in
                            all 85 rows runs with stub_disk_exists = 1, so the no-disk
                            guard fires in NO ROW ANYWHERE.  A driver probing an absent
                            drive -- every ATA bus scan does -- leaves an abandoned CDB
                            live, stray bytes complete it, and a SCSI command is
                            dispatched on a command the device just aborted.

  row_every_opcode_resets   M23_exemptfill is scored KILLED, and three of its four
                            conjuncts ESCAPE ALONE.  `if (idata != ATAPI_IDENTIFY_DEVICE)`
                            sweeps all 85 rows and reproduces pre-#479 byte-for-byte --
                            and it is the MORE reachable half, being the standard ATAPI
                            probe.  One row over the dispatched opcodes kills all eight
                            opcode-exemption escapes.

THE ORACLE IS `occ % 512 == 0`, which is what makes one row cover every opcode: commands
that FILL the ring legitimately (IDENTIFY, READ) leave exactly 512, commands that do not
leave 0, and an unflushed 100-byte residue makes both impossible.

STOPPING HERE.  The four state guards and the ring-pointer form are FILED, not fixed --
the seat that found them states plainly that these two rows do not touch them, and one of
them it could not establish as non-equivalent.
"""
import io, os, shutil

NL, T, BS = chr(10), chr(9), chr(92)
N = BS + "n"
ROOT = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC"
OUT = (r"C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-CC-GXEMUL"
       r"\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\r480b")

s = io.open(os.path.join(ROOT, "regress", "diff_wdc_identify.c"),
            encoding="utf-8", newline="").read()

ROW = '''

/*  #480: THE CALL CAN STOP RUNNING ON A PATH WITHOUT BEING "CONDITIONED".
 *
 *  wdc_command() has TWO early returns.  This round's first three rows covered the
 *  second (the CD-ROM/IDENTIFY abort) and left the first -- the no-disk guard --
 *  reachable by no row at all: every one of the seventeen wdc_command() calls in
 *  the file runs with stub_disk_exists = 1.
 *
 *  So moving the helper call below the FIRST guard only, which is strictly smaller
 *  than the M4 mutant this round was built for, escaped every row.  Measured worse
 *  than pre-#479: a driver probing an absent drive -- which every ATA bus scan does
 *  -- leaves an abandoned CDB live, and stray bytes then complete it into a SCSI
 *  command on a command the device has just aborted.
 */
static void row_absent_drive_resets(void)
{
	struct wdc_data d;
	unsigned char buf[8];
	int i, before;

	memset(&d, 0, sizeof(d));
	d.addr_mult  = 1;
	d.io_enabled = 1;
	d.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
	d.irq.interrupt_assert = arm_sink;
	if (d.inbuf == NULL) {
		printf("  SETUP absent_drive inbuf failed@N@");
		return;
	}

	/*  A packet command is in flight and has collected eight of twelve bytes.  */
	stub_disk_exists = 1;
	stub_cdrom_poison = 1;
	wdc_command(fake_cpu(), &d, ATAPI_PKT_CMD);
	for (i = 0; i < 4; i++) {
		buf[0] = 0x28; buf[1] = 0x00;
		dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_WRITE, &d);
	}

	/*  The guest now addresses a drive that is not there.  The command is
	    aborted at the FIRST guard -- but it still happened, so the abandoned
	    CDB must not survive it.  */
	before = stub_scsi_cmds;
	stub_disk_exists = 0;
	wdc_command(fake_cpu(), &d, WDCC_IDENTIFY);

	/*  Stray bytes that would complete the abandoned CDB.  */
	for (i = 0; i < 2; i++) {
		buf[0] = 0xff; buf[1] = 0xff;
		dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_WRITE, &d);
	}

	rows ++;
	if (stub_scsi_cmds != before || d.atapi_cmd_in_progress != 0 ||
	    !(d.error & WDCE_ABRT)) {
		printf("  FAIL %-38s %i cmd(s) flag %i abrt %i@N@",
		    "an absent-drive command still resets",
		    stub_scsi_cmds - before, d.atapi_cmd_in_progress,
		    !!(d.error & WDCE_ABRT));
		failures ++;
	} else {
		printf("  ok   %-38s %i cmd(s) flag %i abrt %i@N@",
		    "an absent-drive command still resets",
		    stub_scsi_cmds - before, d.atapi_cmd_in_progress,
		    !!(d.error & WDCE_ABRT));
	}

	stub_cdrom_poison = 0;
	if (d.atapi_st != NULL) {
		free(d.atapi_st->data_in);
		free(d.atapi_st->cmd);
		free(d.atapi_st);
	}
	free(d.inbuf);
}


/*  #480: ONE ROW OVER EVERY DISPATCHED OPCODE, because a four-token exemption is
 *  killed by a row that only exercises one of its tokens.
 *
 *  M23_exemptfill exempts IDENTIFY, READ, READMULTI and ATAPI_IDENTIFY_DEVICE and
 *  is scored KILLED -- yet THREE OF ITS FOUR CONJUNCTS ESCAPE ON THEIR OWN.  The
 *  sharpest is ATAPI_IDENTIFY_DEVICE, which shares a case label with WDCC_IDENTIFY
 *  and fills the ring identically: it is the standard ATAPI probe, so it is the
 *  MORE reachable half, and `row_refill_cmd_resets` uses WDCC_IDENTIFY only.
 *
 *  A row per opcode would be twenty rows.  The oracle that collapses them to one is
 *  `occ % 512 == 0`: a command that legitimately FILLS the ring leaves exactly 512,
 *  a command that does not leaves 0, and an unflushed 100-byte residue makes both
 *  impossible whatever the opcode does afterwards.
 *
 *  The enumeration is the function's own switch arms, read off the source -- not the
 *  opcodes some row happens to use.  That is what keeps it closed.
 */
static void row_every_opcode_resets(void)
{
	static const int op[] = {
		WDCC_READ, WDCC_READMULTI, WDCC_WRITE, WDCC_WRITEMULTI,
		WDCC_IDP, SET_FEATURES, WDCC_RECAL, WDCC_IDENTIFY,
		ATAPI_IDENTIFY_DEVICE, WDCC_IDLE_IMMED, WDCC_SETMULTI,
		ATAPI_SOFT_RESET, ATAPI_PKT_CMD
	};
	int k, bad = 0, firstbad = -1, badocc = -1;

	for (k = 0; k < (int) (sizeof(op) / sizeof(op[0])); k++) {
		struct wdc_data d;
		unsigned char buf[8];
		int i, occ;

		memset(&d, 0, sizeof(d));
		d.addr_mult  = 1;
		d.io_enabled = 1;
		d.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
		d.irq.interrupt_assert = arm_sink;
		if (d.inbuf == NULL)
			continue;
		stub_disk_exists = 1;

		/*  An abandoned WRITE with a 100-byte residue -- the exact state
		    #479 exists to clear.  */
		d.seccnt = 1;
		wdc_command(fake_cpu(), &d, WDCC_WRITE);
		for (i = 0; i < 50; i++) {
			buf[0] = 0xaa; buf[1] = 0xaa;
			dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2,
			    MEM_WRITE, &d);
		}

		/*  ...and then THIS opcode arrives.  */
		d.seccnt = 1;
		wdc_command(fake_cpu(), &d, op[k]);

		occ = d.inbuf_head - d.inbuf_tail;
		while (occ < 0)
			occ += WDC_INBUF_SIZE;

		if ((occ % 512) != 0) {
			bad ++;
			if (firstbad < 0) {
				firstbad = op[k];
				badocc = occ;
			}
		}

		if (d.atapi_st != NULL) {
			free(d.atapi_st->data_in);
			free(d.atapi_st->cmd);
			free(d.atapi_st);
		}
		free(d.inbuf);
		stub_disk_exists = 0;
	}

	rows ++;
	if (bad != 0) {
		printf("  FAIL %-38s %i of 13, first 0x%02x occ %i@N@",
		    "every opcode clears the residue", bad, firstbad, badocc);
		failures ++;
	} else {
		printf("  ok   %-38s %i of 13@N@",
		    "every opcode clears the residue", bad);
	}
}

'''.replace("@N@", N)

anchor = NL + NL + "static void row_arm_overrun(void)"
assert s.count(anchor) == 1, "anchor %d" % s.count(anchor)
reg = T + "row_refill_cmd_resets();" + NL
assert s.count(reg) == 1, "reg %d" % s.count(reg)

for lbl in ("an absent-drive command still resets",
            "every opcode clears the residue"):
    assert len(lbl) < 38, "label %d: %s" % (len(lbl), lbl)
    print("  label ok (%2d < 38): %s" % (len(lbl), lbl))

s = s.replace(anchor, ROW + NL + "static void row_arm_overrun(void)", 1)
s = s.replace(reg, reg + T + "row_absent_drive_resets();" + NL +
                        T + "row_every_opcode_resets();" + NL, 1)
for a, b in [("if (rows != 85) {", "if (rows != 87) {"),
             ("rows = %i, want 85", "rows = %i, want 87")]:
    assert s.count(a) == 1, "%r %d" % (a, s.count(a))
    s = s.replace(a, b, 1)

if os.path.isdir(OUT):
    shutil.rmtree(OUT)
os.makedirs(os.path.join(OUT, "regress"))
os.makedirs(os.path.join(OUT, "src", "devices"))
io.open(os.path.join(OUT, "regress", "diff_wdc_identify.c"),
        "w", encoding="utf-8", newline="").write(s)
shutil.copy(os.path.join(ROOT, "src", "devices", "dev_wdc.c"),
            os.path.join(OUT, "src", "devices", "dev_wdc.c"))
print("  #480b candidate written; REPO NOT TOUCHED")
