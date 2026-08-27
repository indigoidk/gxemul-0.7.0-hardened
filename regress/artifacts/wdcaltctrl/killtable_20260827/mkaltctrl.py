"""ALT-CTRL round: the PRE-FIX reproduction, re-cut from the panel's findings.

*** THIS IS STEP ONE OF THE ORACLE-CORRECTION ORDER.  R2 is re-pinned HERE, and the
COMMITTED build is measured RED under the new expectation, BEFORE any product code
changes.  Same scripts, opposite colour.  Without that red, a re-pin is observationally
identical to fitting the test to the binary. ***

FOUR CHANGES FROM THE FIRST DRAFT, every one from a measurement a seat made:

  1. R2 RE-PINNED.  It read `cur_command != COMMAND_RESET`, which conflates "0x08 did not
     latch a reset" with "the device is not in the reset state".  Those differ the instant
     a power-on signature exists -- and the opus seat MEASURED the old form going RED on
     CORRECT code once A4 is adopted.  The delta form states the actual harm:
     `0xec -> 0x100`, a routine control write DESTROYING the record of which command is
     executing.

  2. FRESH STATE PER ROW.  The first draft ran all three rows off ONE struct, so row 2's
     0x08 arrived after row 1's 0x06 and read as a release edge -- its independence was
     compromised by its neighbour.  Named by the fable seat.  Each row now builds its own
     device.

  3. A ROW FOR THE `m1` ESCAPE.  0x0a is libata's polled-mode staple and 0x02 is a bare
     nIEN write; both have bit 3 SET, so both latch a reset TODAY.  Neither has bit 2, so
     neither should.  Measured escape of a mask widened to (WDCTL_RST | WDCTL_IDS).

  4. THE POWER-ON SIGNATURE ROWS, folded in.  `wdcatapisig` is not scope creep here: the
     round CHANGES WHEN THE SIGNATURE APPEARS, so the de-escalation clause's accept rows
     ARE its coverage.  Three independent routes agreed on that.

EXPECTED: five RED on the committed build, and the two controls GREEN.  A control that
reds means the harness is broken, not the device.
"""
import io, os, shutil

NL, T, BS = chr(10), chr(9), chr(92)
N = BS + "n"
ROOT = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC"
OUT = (r"C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-CC-GXEMUL"
       r"\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\alt")

s = io.open(os.path.join(ROOT, "regress", "diff_wdc_identify.c"),
            encoding="utf-8", newline="").read()

ROW = '''

/*  THE ALT-CTRL HANDLER: FOUR LINES, AND THE PANEL MEASURED THREE DEFECTS AND A
 *  MISSING FEATURE BEHIND THEM.
 *
 *      if (idata & WDCTL_4BIT)
 *              d->cur_command = COMMAND_RESET;
 *
 *  WDCTL_4BIT is 0x08, "use four head bits (wd1003)".  The reset bit is WDCTL_RST,
 *  0x04.  And COMMAND_RESET is not a reset ACTION at all -- it is read at exactly
 *  two sites and both make the cylinder registers return the ATAPI signature
 *  0xEB14 for a CD-ROM.  IT IS THE SIGNATURE LATCH.
 *
 *  Because it triggers on bit 3, which Linux libata holds as its steady-state
 *  ap->ctl, the signature is on almost always and the defect has never shown.
 *
 *  EACH ROW BUILDS ITS OWN DEVICE.  An earlier draft ran three rows off one
 *  struct and row 2's control write arrived carrying row 1's state -- its
 *  independence compromised by its neighbour.  Named by a panel seat.
 */
static void altctl_fresh(struct wdc_data *d)
{
	memset(d, 0, sizeof(*d));
	d->addr_mult  = 1;
	d->io_enabled = 1;
	d->inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
	d->irq.interrupt_assert = arm_sink;
}


static void altctl_free(struct wdc_data *d)
{
	if (d->atapi_st != NULL) {
		free(d->atapi_st->data_in);
		free(d->atapi_st->cmd);
		free(d->atapi_st);
	}
	free(d->inbuf);
}


static void row_srst_is_a_reset(void)
{
	struct wdc_data d;
	unsigned char buf[8];

	altctl_fresh(&d);
	if (d.inbuf == NULL) {
		printf("  SETUP srst_is_a_reset@N@");
		return;
	}

	/*  0x06 = WDCTL_RST | WDCTL_IDS -- what older OpenBSD writes to assert a
	    soft reset.  BIT 3 IS CLEAR, so today's handler does not see it.  */
	memset(buf, 0, sizeof(buf));
	buf[0] = WDCTL_RST | WDCTL_IDS;
	dev_wdc_altstatus_access(fake_cpu(), NULL, 0, buf, 1, MEM_WRITE, &d);

	rows ++;
	if (d.cur_command != COMMAND_RESET) {
		printf("  FAIL %-38s cur_command 0x%x@N@",
		    "a real SRST (0x06) is a reset", d.cur_command);
		failures ++;
	} else {
		printf("  ok   %-38s 0x%x@N@",
		    "a real SRST (0x06) is a reset", d.cur_command);
	}
	altctl_free(&d);
}


/*  *** THIS ROW IS THE ORACLE CORRECTION, and the reason is worth the space.
 *
 *  It first read `cur_command != COMMAND_RESET` -- "a routine 0x08 must not leave
 *  the device in the reset state".  A seat MEASURED that going RED on CORRECT code
 *  the moment a power-on signature is modelled, because then the device legitimately
 *  IS in the reset state before any command runs.  The old oracle conflated "this
 *  write did not latch" with "the device is not latched".
 *
 *  The delta form asks the question that actually matters and is robust to A4: DID
 *  THIS WRITE CHANGE cur_command?  And the harm it states is the sharper one the
 *  brief had understated -- `cur_command` is also the value assigned into
 *  write_in_progress, so a routine Device Control write DESTROYS THE RECORD OF WHICH
 *  COMMAND IS EXECUTING.  That is safe today only because wdc__write() has exactly
 *  one caller, immediately after the assignment: an accident, not an invariant.  ***
 */
static void row_routine_ctl_preserves_cmd(void)
{
	struct wdc_data d;
	unsigned char buf[8];
	int before;

	altctl_fresh(&d);
	if (d.inbuf == NULL) {
		printf("  SETUP routine_ctl@N@");
		return;
	}

	/*  A command is executing.  0xec is IDENTIFY -- an ordinary one.  */
	d.cur_command = WDCC_IDENTIFY;
	before = d.cur_command;

	/*  ...and the driver writes its steady-state Device Control byte.  libata
	    does this constantly; it is not a reset and must change nothing.  */
	memset(buf, 0, sizeof(buf));
	buf[0] = WDCTL_4BIT;
	dev_wdc_altstatus_access(fake_cpu(), NULL, 0, buf, 1, MEM_WRITE, &d);

	rows ++;
	if (d.cur_command != before) {
		printf("  FAIL %-38s 0x%x -> 0x%x@N@",
		    "a routine 0x08 preserves the command",
		    before, d.cur_command);
		failures ++;
	} else {
		printf("  ok   %-38s 0x%x@N@",
		    "a routine 0x08 preserves the command", d.cur_command);
	}
	altctl_free(&d);
}


/*  The `m1` escape, built as a row before the fix exists.  A mask widened to
 *  (WDCTL_RST | WDCTL_IDS) escaped every row a seat could throw at it -- because the
 *  rows' entire control vocabulary was {0x06, 0x08, 0x0c} and nothing wrote an
 *  IDS-without-RST value.  0x0a is libata's polled-mode staple and 0x02 is a bare
 *  nIEN write; both carry bit 3 and so latch TODAY, and neither carries bit 2.
 */
static void row_nien_is_not_a_reset(void)
{
	struct wdc_data d;
	unsigned char buf[8];
	int a, b;

	altctl_fresh(&d);
	if (d.inbuf == NULL) {
		printf("  SETUP nien@N@");
		return;
	}

	d.cur_command = WDCC_IDENTIFY;
	memset(buf, 0, sizeof(buf));
	buf[0] = WDCTL_IDS | WDCTL_4BIT;		/*  0x0a  */
	dev_wdc_altstatus_access(fake_cpu(), NULL, 0, buf, 1, MEM_WRITE, &d);
	a = d.cur_command;

	altctl_free(&d);
	altctl_fresh(&d);
	if (d.inbuf == NULL)
		return;
	d.cur_command = WDCC_IDENTIFY;
	memset(buf, 0, sizeof(buf));
	buf[0] = WDCTL_IDS;				/*  0x02  */
	dev_wdc_altstatus_access(fake_cpu(), NULL, 0, buf, 1, MEM_WRITE, &d);
	b = d.cur_command;

	rows ++;
	if (a == COMMAND_RESET || b == COMMAND_RESET) {
		printf("  FAIL %-38s 0x0a->0x%x 0x02->0x%x@N@",
		    "an nIEN write is not a reset", a, b);
		failures ++;
	} else {
		printf("  ok   %-38s 0x%x 0x%x@N@",
		    "an nIEN write is not a reset", a, b);
	}
	altctl_free(&d);
}


static void row_srst_aborts(void)
{
	struct wdc_data d;
	unsigned char buf[8];
	int i, occ;

	altctl_fresh(&d);
	if (d.inbuf == NULL) {
		printf("  SETUP srst_aborts@N@");
		return;
	}

	/*  A write is armed, a packet is mid-CDB, and the ring holds 40 bytes.  */
	d.write_in_progress = WDCC_WRITE;
	d.write_count  = 1;
	d.atapi_cmd_in_progress = 1;
	d.atapi_phase = PHASE_CMDOUT;
	for (i = 0; i < 40; i++)
		wdc_addtoinbuf(&d, 0x5a);

	memset(buf, 0, sizeof(buf));
	buf[0] = WDCTL_RST | WDCTL_4BIT;		/*  0x0c -- assert  */
	dev_wdc_altstatus_access(fake_cpu(), NULL, 0, buf, 1, MEM_WRITE, &d);

	occ = d.inbuf_head - d.inbuf_tail;
	while (occ < 0)
		occ += WDC_INBUF_SIZE;

	rows ++;
	if (d.write_in_progress != 0 || d.atapi_cmd_in_progress != 0 || occ != 0) {
		printf("  FAIL %-38s wip 0x%x flag %i occ %i@N@",
		    "an SRST aborts what was in flight",
		    d.write_in_progress, d.atapi_cmd_in_progress, occ);
		failures ++;
	} else {
		printf("  ok   %-38s %i@N@",
		    "an SRST aborts what was in flight", occ);
	}
	altctl_free(&d);
}


/*  THE POWER-ON SIGNATURE, folded in rather than filed.
 *
 *  ATA/ATAPI-4 has an ATAPI device post 0x14/0xEB after POWER-ON OR RESET.  This
 *  model implements only the reset half, on the wrong bit -- and because that bit is
 *  libata's steady state, the accident has covered the gap.  Correcting the bit
 *  REMOVES THE ACCIDENT, so this round must supply the real thing or it ships a
 *  regression.  That is the de-escalation clause exactly, and these rows are the
 *  accept side it demands.
 *
 *  *** THE COMMENTS PIN THE MODEL'S OWN CONSTANTS, NOT A SPECIFICATION.  There is no
 *  ATA document in this tree -- fifteen PDFs and none of them ATA -- and this project
 *  shipped manual page numbers from panel output three times in #357/#362/#365 and
 *  got away with it on luck.  The claim here is change-detection, not conformance. ***
 */
static void row_srst_signature(void)
{
	struct wdc_data d;
	unsigned char buf[8];
	int lo, hi;

	altctl_fresh(&d);
	if (d.inbuf == NULL) {
		printf("  SETUP srst_sig@N@");
		return;
	}
	stub_disk_exists = 1;
	stub_cdrom_poison = 1;

	/*  ACCEPT ROW.  A REAL soft reset must still produce the signature after
	    the bit is corrected -- this is the de-escalation clause's accept side,
	    and it is the row wdcatapisig was filed for.  0x06 is OpenBSD's assert
	    value; the 0x0c form is covered by the abort row above.  */
	memset(buf, 0, sizeof(buf));
	buf[0] = WDCTL_RST | WDCTL_IDS;
	dev_wdc_altstatus_access(fake_cpu(), NULL, 0, buf, 1, MEM_WRITE, &d);
	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_cyl_lo, buf, 1, MEM_READ, &d);
	lo = buf[0];
	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_cyl_hi, buf, 1, MEM_READ, &d);
	hi = buf[0];

	rows ++;
	if (lo != 0x14 || hi != 0xeb) {
		printf("  FAIL %-38s 0x%02x%02x want 0xeb14@N@",
		    "a real SRST still signs the CD-ROM", hi, lo);
		failures ++;
	} else {
		printf("  ok   %-38s 0x%02x%02x@N@",
		    "a real SRST still signs the CD-ROM", hi, lo);
	}

	/*  CONTROL: the same registers on a NON-CD-ROM must not sign.  Without this
	    a row demanding 0xeb14 is satisfied by a device that signs
	    unconditionally -- a different defect wearing this one's clothes.  */
	stub_cdrom_poison = 0;
	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_cyl_lo, buf, 1, MEM_READ, &d);
	lo = buf[0];
	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_cyl_hi, buf, 1, MEM_READ, &d);
	hi = buf[0];

	rows ++;
	if (lo == 0x14 && hi == 0xeb) {
		printf("  FAIL %-38s an ATA disk signed 0xeb14@N@",
		    "control: a non-CD-ROM does not sign");
		failures ++;
	} else {
		printf("  ok   %-38s 0x%02x%02x@N@",
		    "control: a non-CD-ROM does not sign", hi, lo);
	}

	/*  CONTROL: the signature the device DOES produce still works, so a failure
	    above reads as "the power-on half is missing" and not "the signature is
	    broken".  Two different repairs; the row has to say which.  */
	stub_cdrom_poison = 1;
	d.cur_command = COMMAND_RESET;
	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_cyl_lo, buf, 1, MEM_READ, &d);
	lo = buf[0];
	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_cyl_hi, buf, 1, MEM_READ, &d);
	hi = buf[0];

	rows ++;
	if (lo != 0x14 || hi != 0xeb) {
		printf("  FAIL %-38s 0x%02x%02x want 0xeb14@N@",
		    "control: the reset signature works", hi, lo);
		failures ++;
	} else {
		printf("  ok   %-38s 0x%02x%02x@N@",
		    "control: the reset signature works", hi, lo);
	}

	stub_cdrom_poison = 0;
	stub_disk_exists = 0;
	altctl_free(&d);
}

'''.replace("@N@", N)

anchor = NL + NL + "static void row_arm_overrun(void)"
assert s.count(anchor) == 1, "anchor %d" % s.count(anchor)
reg = T + "row_every_opcode_resets();" + NL
assert s.count(reg) == 1, "reg %d" % s.count(reg)

LBL = ("a real SRST (0x06) is a reset", "a routine 0x08 preserves the command",
       "an nIEN write is not a reset", "an SRST aborts what was in flight",
       "a real SRST still signs the CD-ROM", "control: a non-CD-ROM does not sign",
       "control: the reset signature works")
for lbl in LBL:
    assert len(lbl) < 38, "label %d: %s" % (len(lbl), lbl)
    print("  label ok (%2d < 38): %s" % (len(lbl), lbl))

s = s.replace(anchor, ROW + NL + "static void row_arm_overrun(void)", 1)
s = s.replace(reg, reg +
              T + "row_srst_is_a_reset();" + NL +
              T + "row_routine_ctl_preserves_cmd();" + NL +
              T + "row_nien_is_not_a_reset();" + NL +
              T + "row_srst_aborts();" + NL +
              T + "row_srst_signature();" + NL, 1)
for a, b in [("if (rows != 87) {", "if (rows != 94) {"),
             ("rows = %i, want 87", "rows = %i, want 94")]:
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
print("  ALT-CTRL pre-fix reproduction written; REPO NOT TOUCHED")
