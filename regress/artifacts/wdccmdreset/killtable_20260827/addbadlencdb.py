"""codex's #478 pass-2 finding, under test: does a BAD-LEN access still dispatch a CDB?

Its claim: `badlen_this` guards only the SECTOR DRAIN.  The CDB dispatch is guarded by
`atapi_cmd_in_progress && phase == PHASE_CMDOUT && inbuf_len == 12` and NOT by
`badlen_this` -- so an access of an unimplemented width, which pushes nothing and reports
"(ignored)", can still issue a 12-byte SCSI command if occupancy was already 12.

If that holds, two things follow:
  * a LIVE defect -- a rejected access has a side effect;
  * an L4 -- #478's record claims #337's "(ignored)" finally becomes TRUE, and it does not.

The existing `no-push write does not dispatch` row does NOT cover this: it sets the phase
to DATAIN, so #477's PHASE guard blocks the dispatch for a different reason.  This row
puts the phase where a real CDB collection is, which is the state that makes the question
live.
"""
import io

NL = chr(10)
DET = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\diff_wdc_identify.c"

ROW = r'''

/*  A REJECTED ACCESS MUST HAVE NO SIDE EFFECT -- including the CDB dispatch.
 *
 *  Named by the codex seat on `#478`'s pass 2: `badlen_this` guards the sector
 *  drain and NOT the CDB dispatch, so an access of an unimplemented width -- which
 *  pushes nothing and is reported "(ignored)" -- can still issue a 12-byte SCSI
 *  command when occupancy was already 12.
 *
 *  The existing `no-push write does not dispatch` row does not cover this: it sits
 *  in PHASE_DATAIN, so `#477`'s phase guard blocks the dispatch for an unrelated
 *  reason.  Here the phase is CMDOUT -- where a real CDB is collected -- which is
 *  the state that makes the question live.
 *
 *  If this row is RED, `#478`'s claim that `#337`'s "(ignored)" became TRUE is a
 *  wrong record in product code, and a rejected access still has a side effect.
 */
static void row_badlen_no_dispatch(void)
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
		printf("  SETUP badlen_cdb inbuf failed\n");
		return;
	}

	/*  the real device sets all three together  */
	d.cur_command = ATAPI_PKT_CMD;
	d.atapi_cmd_in_progress = 1;
	d.atapi_phase = PHASE_CMDOUT;

	/*  a CDB's worth already queued -- occupancy is exactly 12 BEFORE the
	    rejected access, so the access itself pushes nothing and changes it
	    not at all.  */
	for (i = 0; i < 12; i++)
		wdc_addtoinbuf(&d, 0x12);

	stub_scsi_cmds = 0;
	stub_fatals = 0;

	/*  an 8-byte store: the width switch rejects it and says so.  */
	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 8, MEM_WRITE, &d);

	rows ++;
	if (stub_scsi_cmds != 0) {
		printf("  FAIL %-38s dispatched %i\n",
		    "a rejected width issues no command", stub_scsi_cmds);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "a rejected width issues no command", stub_scsi_cmds);
	}

	/*  and it must SAY something -- a silently rejected access with a side
	    effect is the worst of both.  */
	rows ++;
	if (stub_fatals < 1) {
		printf("  FAIL %-38s emitted %i\n",
		    "a rejected width is announced", stub_fatals);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "a rejected width is announced", stub_fatals);
	}

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
reg = chr(9) + "row_residue_recovery();" + NL
assert s.count(reg) == 1, "reg %d" % s.count(reg)

for lbl in ("a rejected width issues no command", "a rejected width is announced"):
    assert len(lbl) < 38, "label %d chars: %s" % (len(lbl), lbl)
    print("  label ok (%2d < 38): %s" % (len(lbl), lbl))

s = s.replace(anchor, ROW + NL + "static void row_arm_overrun(void)", 1)
s = s.replace(reg, reg + chr(9) + "row_badlen_no_dispatch();" + NL, 1)
for a, b in [("if (rows != 73) {", "if (rows != 75) {"),
             ("rows = %i, want 73", "rows = %i, want 75")]:
    assert s.count(a) == 1, "%r %d" % (a, s.count(a))
    s = s.replace(a, b, 1)
io.open(DET, "w", encoding="utf-8", newline="").write(s)
print("  row_badlen_no_dispatch appended, pin -> 75")
