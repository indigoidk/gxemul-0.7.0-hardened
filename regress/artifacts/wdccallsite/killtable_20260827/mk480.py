"""#480: close the CALL-SITE floor breach the opus seat measured on #479's pass 2.

#479 shipped a detector that kills 13 of 13 mutants of the helper's BODY and cannot
see the helper's CALL become CONDITIONAL.  Three one-line edits at the call site --
each reading as an improvement -- escape with BYTE-IDENTICAL output:

  M11_sameop      `if (!same_cmd) wdc_new_command_reset(d);`
  M4_afterguard   move the call below the two early-return guards
  M23_exemptfill  exempt IDENTIFY/READ/READMULTI/ATAPI_IDENTIFY_DEVICE

They are NOT equivalent mutants; a register-level witness measured real damage
behind each.  The structural reason they escape: every #479 reproduction row calls
wdc_command() DIRECTLY, with stub_disk_exists = 1, using two DIFFERENT opcodes --
so no row can observe the call being made conditional.

    A DETECTOR FOR A FIX THAT ADDS AN UNCONDITIONAL CALL MUST CONTAIN AT LEAST ONE
    ROW THAT REDS IF THAT CALL BECOMES CONDITIONAL.

which is clause (d) aimed at the CALL SITE rather than at a predicate -- the
DEPENDS-ON reading the carrier adopted 2026-08-24.
"""
import io, os, shutil

NL, T, BS = chr(10), chr(9), chr(92)
N = BS + "n"
ROOT = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC"
OUT = (r"C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-CC-GXEMUL"
       r"\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\r480")

s = io.open(os.path.join(ROOT, "regress", "diff_wdc_identify.c"),
            encoding="utf-8", newline="").read()

ROW = '''

/*  #480: THREE ROWS THAT WATCH THE HELPER'S CALL, NOT ITS BODY.
 *
 *  #479's thirteen mutants all edit what wdc_new_command_reset() DOES.  Every one
 *  dies.  Three edits to WHETHER IT IS CALLED escape with byte-identical output,
 *  because every #479 row calls wdc_command() directly with two DIFFERENT opcodes
 *  and a disk that exists -- so no row is in a position to notice a condition
 *  appearing in front of the call.
 *
 *  Each row below is aimed at one of them, and each asserts a value MEASURED on
 *  the committed build by a register-level witness probe.
 */
static void row_same_opcode_resets(void)
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
		printf("  SETUP same_opcode inbuf failed@N@");
		return;
	}
	stub_disk_exists = 1;

	/*  A WRITE is armed and the guest streams 100 bytes, then gives up.  */
	d.write_in_progress = WDCC_WRITE;
	d.write_count  = 1;
	d.write_offset = 0xc000;
	for (i = 0; i < 50; i++) {
		buf[0] = 0xaa; buf[1] = 0xaa;
		dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_WRITE, &d);
	}

	/*  It re-issues THE SAME OPCODE.  A retry is a new command: the abandoned
	    100 bytes are not part of it.  M11 reads this as "a repeated opcode is
	    a retry, not a new command" and skips the reset.  */
	stub_disk_writes = 0;
	stub_disk_bytes = 0;
	stub_disk_first = -1;
	d.cur_command = WDCC_WRITE;
	wdc_command(fake_cpu(), &d, WDCC_WRITE);

	/*  Now a full, legal sector of its own.  */
	for (i = 0; i < 256; i++) {
		buf[0] = 0xbb; buf[1] = 0xbb;
		dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_WRITE, &d);
	}

	occ = d.inbuf_head - d.inbuf_tail;
	while (occ < 0)
		occ += WDC_INBUF_SIZE;

	rows ++;
	if (stub_disk_first != 0xbb || occ != 0) {
		printf("  FAIL %-38s first 0x%02x residue %i@N@",
		    "a same-opcode reissue resets the ring",
		    stub_disk_first, occ);
		failures ++;
	} else {
		printf("  ok   %-38s first 0x%02x residue %i@N@",
		    "a same-opcode reissue resets the ring",
		    stub_disk_first, occ);
	}

	stub_disk_exists = 0;
	free(d.inbuf);
}


static void row_rejected_cmd_resets(void)
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
		printf("  SETUP rejected_cmd inbuf failed@N@");
		return;
	}
	stub_disk_exists = 1;
	stub_cdrom_poison = 1;		/*  an ATAPI-only controller  */

	/*  A packet command collects EIGHT of its twelve CDB bytes...  */
	d.cur_command = ATAPI_PKT_CMD;
	wdc_command(fake_cpu(), &d, ATAPI_PKT_CMD);
	for (i = 0; i < 4; i++) {
		buf[0] = 0x28; buf[1] = 0x00;
		dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_WRITE, &d);
	}

	/*  ...and the guest then issues IDENTIFY, which an ATAPI drive ABORTS.
	    That is the single most routine probe any ATA driver makes, and ABRT
	    is the correct answer -- but the command still HAPPENED, so the
	    abandoned CDB must not survive it.  M4 moves the reset below the
	    early-return guards, so a rejected command clears nothing.  */
	before = stub_scsi_cmds;
	d.cur_command = WDCC_IDENTIFY;
	wdc_command(fake_cpu(), &d, WDCC_IDENTIFY);

	/*  Four more stray bytes.  Under M4 these COMPLETE the abandoned CDB and
	    the device issues a SCSI command assembled from it -- on a command it
	    has just told the guest was aborted.  */
	for (i = 0; i < 2; i++) {
		buf[0] = 0xff; buf[1] = 0xff;
		dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_WRITE, &d);
	}

	rows ++;
	if (stub_scsi_cmds != before || d.atapi_cmd_in_progress != 0) {
		printf("  FAIL %-38s %i cmd(s) flag %i@N@",
		    "a rejected command still resets",
		    stub_scsi_cmds - before, d.atapi_cmd_in_progress);
		failures ++;
	} else {
		printf("  ok   %-38s %i cmd(s) flag %i@N@",
		    "a rejected command still resets",
		    stub_scsi_cmds - before, d.atapi_cmd_in_progress);
	}

	stub_cdrom_poison = 0;
	stub_disk_exists = 0;
	if (d.atapi_st != NULL) {
		free(d.atapi_st->data_in);
		free(d.atapi_st->cmd);
		free(d.atapi_st);
	}
	free(d.inbuf);
}


static void row_refill_cmd_resets(void)
{
	struct wdc_data d;
	unsigned char buf[8];
	int occ;

	memset(&d, 0, sizeof(d));
	d.addr_mult  = 1;
	d.io_enabled = 1;
	d.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
	d.irq.interrupt_assert = arm_sink;
	if (d.inbuf == NULL) {
		printf("  SETUP refill_cmd inbuf failed@N@");
		return;
	}
	stub_disk_exists = 1;

	/*  IDENTIFY fills the ring with its 512-byte answer...  */
	d.cur_command = WDCC_IDENTIFY;
	wdc_command(fake_cpu(), &d, WDCC_IDENTIFY);

	/*  ...the guest reads one word and abandons it...  */
	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_READ, &d);

	/*  ...and re-issues IDENTIFY.  The answer must be a FRESH block, not the
	    old tail with a new block queued behind it.  M23 exempts exactly these
	    refilling commands from the reset -- "they load their answer INTO the
	    ring, so do not flush for them" -- which is a direct misreading of the
	    round's own comment about why the helper runs at the TOP.  */
	d.cur_command = WDCC_IDENTIFY;
	wdc_command(fake_cpu(), &d, WDCC_IDENTIFY);

	occ = d.inbuf_head - d.inbuf_tail;
	while (occ < 0)
		occ += WDC_INBUF_SIZE;

	rows ++;
	if (occ != 512) {
		printf("  FAIL %-38s occupancy %i@N@",
		    "a refill command starts from empty", occ);
		failures ++;
	} else {
		printf("  ok   %-38s occupancy %i@N@",
		    "a refill command starts from empty", occ);
	}

	stub_disk_exists = 0;
	free(d.inbuf);
}

'''.replace("@N@", N)

anchor = NL + NL + "static void row_arm_overrun(void)"
assert s.count(anchor) == 1, "anchor %d" % s.count(anchor)
reg = T + "row_little_endian_arm();" + NL
assert s.count(reg) == 1, "reg %d" % s.count(reg)

LBL = ("a same-opcode reissue resets the ring", "a rejected command still resets",
       "a refill command starts from empty")
for lbl in LBL:
    assert len(lbl) < 38, "label %d chars: %s" % (len(lbl), lbl)
    print("  label ok (%2d < 38): %s" % (len(lbl), lbl))

s = s.replace(anchor, ROW + NL + "static void row_arm_overrun(void)", 1)
s = s.replace(reg, reg + T + "row_same_opcode_resets();" + NL +
                        T + "row_rejected_cmd_resets();" + NL +
                        T + "row_refill_cmd_resets();" + NL, 1)
for a, b in [("if (rows != 80) {", "if (rows != 83) {"),
             ("rows = %i, want 80", "rows = %i, want 83")]:
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
print("  #480 candidate tree written; REPO NOT TOUCHED")
