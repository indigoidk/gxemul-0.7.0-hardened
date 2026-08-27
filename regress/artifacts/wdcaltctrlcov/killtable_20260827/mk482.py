"""#482: the abort row could not say WHICH state gates the abort.

#481's sole-carrier row sets write_in_progress, atapi_cmd_in_progress, the phase AND the
ring SIMULTANEOUSLY, then asserts all four are cleared. Both flagship seats measured the
same consequence independently: ANY SINGLE-CONJUNCT QUALIFICATION OF THE HELPER CALL still
passes it.

    Mo_abt_atapi / Mq_flag   `if (d->atapi_cmd_in_progress)` before the call
                             -> SRST NO LONGER ABORTS A PLAIN ATA WRITE.  wip 0x30 and
                                occ 16 survive the reset.  THE MAJORITY PATH.
    Mo_abt_wip  / Mq_wip     `if (d->write_in_progress)` instead
                             -> SRST no longer aborts a packet CDB: flag 1, occ 12 survive
    Mo_abt_ring              gated on ring occupancy -> the writer survives

The repair is not a better assertion; it is SEPARATE ROWS THAT ARM ONE TENANT EACH.  A row
that establishes every conjunct at once cannot tell you which one the guard reads -- that
is the pre-table check's guard-field/body-field clause, arriving from the mutant side.

AND ONE ACCEPT ROW, for a different escape family: the mask.  #481's predicate must contain
bit 2 and exclude bits 1 and 3; bits 0, 4, 5, 6 and 7 are entirely FREE, because the whole
control vocabulary of the detector is {0x02, 0x06, 0x08, 0x0a, 0x0c}.  0x80 is the one with
a real driver behind it -- libata ORs an HOB bit into the control byte on 48-bit taskfile
reads -- and `0x88` was measured latching a reset and destroying cur_command.

    (The 0x3f7/HOB identifications are READ from general ATA knowledge; THIS TREE HAS NO
    ATA DOCUMENT, fifteen PDFs and none of them ATA.  What is MEASURED is that 0x88 escapes
    every row and destroys the command record.  The row pins the MODEL'S behaviour, and its
    comment says so rather than citing a specification nobody here can open.)

EXPECTED: three RED on the committed build for the two abort rows and the HOB row... EXCEPT
the abort rows are ACCEPT-SIDE: they must be GREEN on the committed build (which does abort
correctly) and RED only under the qualifying mutants.  That is the de-escalation clause's
accept side, and it is why this round's reproduction is a MUTANT TABLE rather than a red row
-- stated plainly because a round whose "reproduction" is green needs to say why.
"""
import io, os, shutil

NL, T, BS = chr(10), chr(9), chr(92)
N = BS + "n"
ROOT = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC"
OUT = (r"C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-CC-GXEMUL"
       r"\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\r482")

s = io.open(os.path.join(ROOT, "regress", "diff_wdc_identify.c"),
            encoding="utf-8", newline="").read()

ROW = '''

/*  #482: ONE TENANT EACH, because a row that arms them all cannot say which one
 *  the guard reads.
 *
 *  #481's abort row sets write_in_progress, atapi_cmd_in_progress, the phase and
 *  the ring together and asserts all four are cleared.  Both flagship seats
 *  measured the same hole independently: putting ANY ONE of those fields in front
 *  of the helper call still passes it.  The worst is the first -- a plain ATA
 *  write is the majority reset path, and `if (d->atapi_cmd_in_progress)` leaves
 *  its writer and 16 staged bytes alive across the reset.
 *
 *  These rows are ACCEPT-SIDE: green on the committed build, which aborts
 *  correctly, and red under the qualifying mutants.  Said out loud because a
 *  round whose reproduction is GREEN owes an explanation -- the defect here is
 *  a COVERAGE hole measured by mutants, not a live misbehaviour.
 */
static void row_srst_aborts_ata_only(void)
{
	struct wdc_data d;
	unsigned char buf[8];
	int i, occ;

	altctl_fresh(&d);
	if (d.inbuf == NULL) {
		printf("  SETUP ata_only@N@");
		return;
	}

	/*  ONLY an ATA write is in flight.  No packet, no phase, and the ring
	    holds a partial sector -- the commonest thing a guest resets out of.  */
	d.write_in_progress = WDCC_WRITE;
	d.write_count = 1;
	for (i = 0; i < 16; i++)
		wdc_addtoinbuf(&d, 0x5a);

	memset(buf, 0, sizeof(buf));
	buf[0] = WDCTL_RST | WDCTL_4BIT;
	dev_wdc_altstatus_access(fake_cpu(), NULL, 0, buf, 1, MEM_WRITE, &d);

	occ = d.inbuf_head - d.inbuf_tail;
	while (occ < 0)
		occ += WDC_INBUF_SIZE;

	rows ++;
	if (d.write_in_progress != 0 || occ != 0) {
		printf("  FAIL %-38s wip 0x%x occ %i@N@",
		    "an SRST aborts an ATA write alone",
		    d.write_in_progress, occ);
		failures ++;
	} else {
		printf("  ok   %-38s %i@N@",
		    "an SRST aborts an ATA write alone", occ);
	}
	altctl_free(&d);
}


static void row_srst_aborts_pkt_only(void)
{
	struct wdc_data d;
	unsigned char buf[8];
	int i, occ;

	altctl_fresh(&d);
	if (d.inbuf == NULL) {
		printf("  SETUP pkt_only@N@");
		return;
	}

	/*  ONLY a packet is in flight -- no ATA writer at all.  The mirror of the
	    row above, and it is the one `if (d->write_in_progress)` walks past.  */
	d.atapi_cmd_in_progress = 1;
	d.atapi_phase = PHASE_CMDOUT;
	for (i = 0; i < 12; i++)
		wdc_addtoinbuf(&d, 0x28);

	memset(buf, 0, sizeof(buf));
	buf[0] = WDCTL_RST | WDCTL_4BIT;
	dev_wdc_altstatus_access(fake_cpu(), NULL, 0, buf, 1, MEM_WRITE, &d);

	occ = d.inbuf_head - d.inbuf_tail;
	while (occ < 0)
		occ += WDC_INBUF_SIZE;

	rows ++;
	if (d.atapi_cmd_in_progress != 0 || occ != 0) {
		printf("  FAIL %-38s flag %i occ %i@N@",
		    "an SRST aborts a packet alone",
		    d.atapi_cmd_in_progress, occ);
		failures ++;
	} else {
		printf("  ok   %-38s %i@N@",
		    "an SRST aborts a packet alone", occ);
	}
	altctl_free(&d);
}


/*  #482: THE THIRD TENANT IS THE RING ITSELF, and the first draft of this round
 *  missed it -- measured, not noticed.
 *
 *  The two rows above isolate the ATA writer and the packet flag, and they kill
 *  the two mutants that gate the abort on those.  A THIRD mutant gates it on ring
 *  OCCUPANCY -- and both rows above STAGE BYTES, so a non-empty ring satisfies it
 *  and the mutant walked past them.
 *
 *  *** THAT IS THE SAME DEFECT THIS ROUND EXISTS TO FIX, ONE LEVEL DOWN: a row set
 *  more state than the property needed, and so could not tell which piece the
 *  guard read.  It was caught by running the table rather than by inspection. ***
 *
 *  An ARMED WRITER WITH AN EMPTY RING is a real state -- a guest issues WRITE and
 *  resets before streaming a single byte -- and it is the only shape that pins
 *  "the reset clears the writer even when there is nothing to purge".
 */
static void row_srst_aborts_empty_ring(void)
{
	struct wdc_data d;
	unsigned char buf[8];

	altctl_fresh(&d);
	if (d.inbuf == NULL) {
		printf("  SETUP empty_ring@N@");
		return;
	}

	/*  Armed, and NOTHING staged.  */
	d.write_in_progress = WDCC_WRITE;
	d.write_count = 1;

	memset(buf, 0, sizeof(buf));
	buf[0] = WDCTL_RST | WDCTL_4BIT;
	dev_wdc_altstatus_access(fake_cpu(), NULL, 0, buf, 1, MEM_WRITE, &d);

	rows ++;
	if (d.write_in_progress != 0) {
		printf("  FAIL %-38s wip 0x%x@N@",
		    "an SRST clears a writer with no bytes",
		    d.write_in_progress);
		failures ++;
	} else {
		printf("  ok   %-38s 0x%x@N@",
		    "an SRST clears a writer with no bytes",
		    d.write_in_progress);
	}
	altctl_free(&d);
}


/*  #482: THE MASK'S FREE BITS.  The predicate must contain bit 2 and exclude bits
 *  1 and 3; bits 0, 4, 5, 6 and 7 are unconstrained by every row in this file,
 *  because the whole control vocabulary here is {0x02, 0x06, 0x08, 0x0a, 0x0c}.
 *
 *  0x80 is the one with a real driver behind it, and a seat MEASURED `0x88`
 *  latching a reset and destroying cur_command while escaping all 96 rows.
 *
 *  *** THIS ROW PINS THE MODEL, NOT A SPECIFICATION.  The identification of 0x80
 *  as an HOB-style control bit is READ from general ATA knowledge and THERE IS NO
 *  ATA DOCUMENT IN THIS TREE -- fifteen PDFs and not one of them covers it.  What
 *  is measured is that a control byte carrying bit 7 must not be a reset, which
 *  follows from the bit the round chose regardless of what 0x80 means. ***
 */
static void row_hob_is_not_a_reset(void)
{
	struct wdc_data d;
	unsigned char buf[8];
	int i, occ, before;

	altctl_fresh(&d);
	if (d.inbuf == NULL) {
		printf("  SETUP hob@N@");
		return;
	}

	d.cur_command = WDCC_IDENTIFY;
	before = d.cur_command;
	d.write_in_progress = WDCC_WRITE;
	d.write_count = 1;
	for (i = 0; i < 40; i++)
		wdc_addtoinbuf(&d, 0x5a);

	memset(buf, 0, sizeof(buf));
	buf[0] = 0x80 | WDCTL_4BIT;			/*  0x88  */
	dev_wdc_altstatus_access(fake_cpu(), NULL, 0, buf, 1, MEM_WRITE, &d);

	occ = d.inbuf_head - d.inbuf_tail;
	while (occ < 0)
		occ += WDC_INBUF_SIZE;

	rows ++;
	if (d.cur_command != before || d.write_in_progress == 0 || occ != 40) {
		printf("  FAIL %-38s 0x%x->0x%x wip 0x%x occ %i@N@",
		    "a 0x88 control write is not a reset",
		    before, d.cur_command, d.write_in_progress, occ);
		failures ++;
	} else {
		printf("  ok   %-38s 0x%x occ %i@N@",
		    "a 0x88 control write is not a reset", d.cur_command, occ);
	}
	altctl_free(&d);
}

'''.replace("@N@", N)

anchor = NL + NL + "static void row_arm_overrun(void)"
assert s.count(anchor) == 1, "anchor %d" % s.count(anchor)
reg = T + "row_srst_signature();" + NL
assert s.count(reg) == 1, "reg %d" % s.count(reg)

LBL = ("an SRST aborts an ATA write alone", "an SRST aborts a packet alone",
       "an SRST clears a writer with no bytes",
       "a 0x88 control write is not a reset")
for lbl in LBL:
    assert len(lbl) < 38, "label %d: %s" % (len(lbl), lbl)
    print("  label ok (%2d < 38): %s" % (len(lbl), lbl))

s = s.replace(anchor, ROW + NL + "static void row_arm_overrun(void)", 1)
s = s.replace(reg, reg +
              T + "row_srst_aborts_ata_only();" + NL +
              T + "row_srst_aborts_pkt_only();" + NL +
              T + "row_srst_aborts_empty_ring();" + NL +
              T + "row_hob_is_not_a_reset();" + NL, 1)
for a, b in [("if (rows != 96) {", "if (rows != 100) {"),
             ("rows = %i, want 96", "rows = %i, want 100")]:
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
print("  #482 candidate written; REPO NOT TOUCHED")
