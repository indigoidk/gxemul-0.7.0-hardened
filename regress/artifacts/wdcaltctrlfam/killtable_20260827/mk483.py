"""#483: the two UNCONTESTED rows from #482's panel.

The seats disagreed about how to rank the abort-gating and state-qualifier families
(likelihood vs blast radius). These two are outside that dispute -- both were proposed by
the opus seat, neither was challenged, and neither needs a new fixture.

  ROW A -- THE ORPHAN RING.  Kills `disj2` / `M1_disj`, which BOTH flagship seats built
  independently and which is "precisely the repair a maintainer writes after reading the
  four #482 rows": `if (write_in_progress || atapi_cmd_in_progress)`.

      It defeats all four of #482's rows because each arms one of those flags. The state
      that kills it -- RING NON-EMPTY, BOTH FLAGS CLEAR -- had no row, and is guest
      reachable: the #464 tenant test gates only the one-shot diagnostic, while the
      wdc_addtoinbuf() calls sit OUTSIDE it and push unconditionally.

      A LIVENESS CONTROL SHIPS WITH IT: the same traffic with no reset must LEAVE the
      bytes. Without it the row is satisfied by a ring that was empty all along, which is
      the vacuity this file has been bitten by before.

  ROW D -- THE MASK SWEEP.  All 256 control values, asserting the reset latches IF AND ONLY
  IF bit 2 is set.

      *** IT REMOVES AN APPEAL TO KNOWLEDGE THIS TREE DOES NOT HOLD. ***  #482's 0x88 row
      pins ONE arbitrary high bit and its comment has to disclose that the HOB reading comes
      from general ATA knowledge, with no ATA document anywhere in the tree. The sweep needs
      no such appeal: it pins the model's own decode across the whole input space, and bit 6
      (`hob6`, measured escaping by the fable seat) falls out for free.

      An IFF assertion is also strictly stronger than a set of point pins: it fails on a mask
      that is too WIDE and on one that is too NARROW, where each point pin sees only one
      direction.

The 0x88 row is KEPT. The sweep subsumes it, but it is named in gate_offline.sh and removing
a row needs its own warrant -- the ADDITION LICENCE has a mirror. Its comment gains a line
pointing at the sweep as the stronger form.
"""
import io, os, shutil

NL, T, BS = chr(10), chr(9), chr(92)
N = BS + "n"
ROOT = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC"
OUT = (r"C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-CC-GXEMUL"
       r"\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\r483")

s = io.open(os.path.join(ROOT, "regress", "diff_wdc_identify.c"),
            encoding="utf-8", newline="").read()

ROW = '''

/*  #483: THE ORPHAN RING -- the state no row reached, and the one that kills the
 *  edit a maintainer is most likely to make.
 *
 *  `if (d->write_in_progress || d->atapi_cmd_in_progress)` in front of the helper
 *  call reads as an obvious tidy-up: only abort if something is actually in
 *  flight.  BOTH flagship seats built it independently against #482, and it
 *  defeats all four of that round's rows, because every one of them arms one of
 *  those two flags.
 *
 *  *** THE STATE IS GUEST-REACHABLE, and that is what makes this a row rather
 *  than a curiosity.  The #464 unexpected-write test gates ONLY the one-shot
 *  diagnostic; the wdc_addtoinbuf() calls sit OUTSIDE it and push
 *  unconditionally.  So a guest can stage bytes with NEITHER tenant armed and
 *  then assert SRST, and a disjunctively-guarded abort would leave them. ***
 */
static void row_srst_purges_orphan_ring(void)
{
	struct wdc_data d;
	unsigned char buf[8];
	int i, live, occ;

	/*  LIVENESS FIRST: the same traffic with NO reset must LEAVE the bytes.
	    Without this the row is satisfied by a ring that was empty all along --
	    the vacuity shape this file has been bitten by before.  */
	altctl_fresh(&d);
	if (d.inbuf == NULL) {
		printf("  SETUP orphan live@N@");
		return;
	}
	for (i = 0; i < 8; i++) {
		buf[0] = 0x5a; buf[1] = 0x5a;
		dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_WRITE, &d);
	}
	live = d.inbuf_head - d.inbuf_tail;
	while (live < 0)
		live += WDC_INBUF_SIZE;
	altctl_free(&d);

	/*  Now the same stores, with NEITHER tenant armed, followed by SRST.  */
	altctl_fresh(&d);
	if (d.inbuf == NULL) {
		printf("  SETUP orphan@N@");
		return;
	}
	for (i = 0; i < 8; i++) {
		buf[0] = 0x5a; buf[1] = 0x5a;
		dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_WRITE, &d);
	}
	memset(buf, 0, sizeof(buf));
	buf[0] = WDCTL_RST | WDCTL_4BIT;
	dev_wdc_altstatus_access(fake_cpu(), NULL, 0, buf, 1, MEM_WRITE, &d);

	occ = d.inbuf_head - d.inbuf_tail;
	while (occ < 0)
		occ += WDC_INBUF_SIZE;

	rows ++;
	if (live != 16 || occ != 0) {
		printf("  FAIL %-38s live %i occ %i@N@",
		    "an SRST purges an orphan ring", live, occ);
		failures ++;
	} else {
		printf("  ok   %-38s live %i occ %i@N@",
		    "an SRST purges an orphan ring", live, occ);
	}
	altctl_free(&d);
}


/*  #483: THE PACKET WITH AN EMPTY RING -- the SIBLING of #482's empty-ring row,
 *  and its absence was a parity miss the fable seat named before I measured it.
 *
 *  #482 built "an armed ATA writer with nothing staged" and did NOT build its
 *  mirror.  So a guard reading `write_in_progress || ring-occupancy` survives
 *  everything: the ATA rows arm the writer, and every other row stages bytes.
 *
 *  *** MEASURED: with only the orphan-ring and sweep rows added, `wipocc` STILL
 *  ESCAPED all 102.  This row is what kills it, and it exists because the table
 *  said so -- the same way #482's empty-ring row did.  The parity question ("I
 *  built this shape for tenant A; did I build it for tenant B?") is cheaper to
 *  ask than to measure, and I have now failed to ask it twice. ***
 */
static void row_srst_aborts_pkt_empty_ring(void)
{
	struct wdc_data d;
	unsigned char buf[8];

	altctl_fresh(&d);
	if (d.inbuf == NULL) {
		printf("  SETUP pkt_empty@N@");
		return;
	}

	/*  A packet is armed and NOTHING is staged -- a guest that issues PACKET
	    and resets before sending a single CDB byte.  */
	d.atapi_cmd_in_progress = 1;
	d.atapi_phase = PHASE_CMDOUT;

	memset(buf, 0, sizeof(buf));
	buf[0] = WDCTL_RST | WDCTL_4BIT;
	dev_wdc_altstatus_access(fake_cpu(), NULL, 0, buf, 1, MEM_WRITE, &d);

	rows ++;
	if (d.atapi_cmd_in_progress != 0 || d.atapi_phase != 0) {
		printf("  FAIL %-38s flag %i phase %i@N@",
		    "an SRST clears a packet with no bytes",
		    d.atapi_cmd_in_progress, d.atapi_phase);
		failures ++;
	} else {
		printf("  ok   %-38s flag %i phase %i@N@",
		    "an SRST clears a packet with no bytes",
		    d.atapi_cmd_in_progress, d.atapi_phase);
	}
	altctl_free(&d);
}


/*  #483: THE WHOLE INPUT SPACE, and it retires an appeal this tree cannot support.
 *
 *  #482 pinned ONE high bit (0x88) and its comment had to disclose that reading
 *  0x80 as an HOB-style control bit comes from general ATA knowledge -- there is
 *  no ATA document anywhere in this tree.  A seat then measured bit 6 escaping,
 *  which is exactly what a single-point pin cannot see.
 *
 *  This asserts the model's own decode across all 256 values: THE RESET LATCHES
 *  IF AND ONLY IF BIT 2 IS SET.  No specification is cited or needed.
 *
 *  *** AND AN IFF IS STRICTLY STRONGER THAN A SET OF POINT PINS.  It fails on a
 *  mask that is too WIDE (a value without bit 2 latches) and on one that is too
 *  NARROW (a value with bit 2 does not), where each point pin sees one direction
 *  only. ***
 */
static void row_reset_bit_iff(void)
{
	int v, wide = -1, narrow = -1;

	for (v = 0; v < 256; v++) {
		struct wdc_data d;
		unsigned char buf[8];
		int want, got;

		altctl_fresh(&d);
		if (d.inbuf == NULL)
			continue;
		d.cur_command = WDCC_IDENTIFY;

		memset(buf, 0, sizeof(buf));
		buf[0] = v;
		dev_wdc_altstatus_access(fake_cpu(), NULL, 0, buf, 1,
		    MEM_WRITE, &d);

		want = (v & WDCTL_RST) ? 1 : 0;
		got  = (d.cur_command == COMMAND_RESET) ? 1 : 0;
		if (got && !want && wide < 0)
			wide = v;
		if (!got && want && narrow < 0)
			narrow = v;
		altctl_free(&d);
	}

	rows ++;
	if (wide >= 0 || narrow >= 0) {
		printf("  FAIL %-38s wide 0x%02x narrow 0x%02x@N@",
		    "reset latches IFF bit 2 is set", wide, narrow);
		failures ++;
	} else {
		printf("  ok   %-38s 256 of 256@N@",
		    "reset latches IFF bit 2 is set");
	}
}

'''.replace("@N@", N)

anchor = NL + NL + "static void row_arm_overrun(void)"
assert s.count(anchor) == 1, "anchor %d" % s.count(anchor)
reg = T + "row_hob_is_not_a_reset();" + NL
assert s.count(reg) == 1, "reg %d" % s.count(reg)

for lbl in ("an SRST purges an orphan ring", "reset latches IFF bit 2 is set",
            "an SRST clears a packet with no bytes"):
    assert len(lbl) < 38, "label %d: %s" % (len(lbl), lbl)
    print("  label ok (%2d < 38): %s" % (len(lbl), lbl))

s = s.replace(anchor, ROW + NL + "static void row_arm_overrun(void)", 1)
s = s.replace(reg, reg + T + "row_srst_purges_orphan_ring();" + NL +
                        T + "row_srst_aborts_pkt_empty_ring();" + NL +
                        T + "row_reset_bit_iff();" + NL, 1)
for a, b in [("if (rows != 100) {", "if (rows != 103) {"),
             ("rows = %i, want 100", "rows = %i, want 103")]:
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
print("  #483 candidate written; REPO NOT TOUCHED")
