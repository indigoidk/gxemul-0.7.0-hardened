"""The row `#477` owed and did not have, prescribed by the codex seat on pass 2 and
MEASURED necessary: M_phaseonly (the `atapi_cmd_in_progress` conjunct DELETED from the
dispatch guard) sweeps all 52 rows clean.

Mechanism, from the seat: `wdc_command(ATAPI_PKT_CMD)` sets PHASE_CMDOUT.  A following
`wdc_command(WDCC_WRITE)` clears the flag but LEAVES THE PHASE STALE and arms the write.
Six 16-bit payload writes then reach occupancy 12, and a phase-only guard dispatches the
guest's own disk payload as a SCSI CDB, removing those bytes from the pending sector.

So both conjuncts are load-bearing and `#477`'s comment headline is unsafe.

Appended to the repo detector directly -- this discharges a debt against SHIPPED code,
which the late-dissent rule puts in a follow-up commit rather than in `#477` itself.
"""
import io

NL = chr(10)
DET = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\diff_wdc_identify.c"

ROW = r'''

/*  THE ROW `#477` OWED.  Prescribed by the codex seat on `#477`'s pass 2, after it
 *  reasoned that deleting the `atapi_cmd_in_progress` conjunct from the dispatch
 *  guard would sweep the table.  MEASURED: it swept all 52 rows clean.
 *
 *  THE STALE PHASE IS THE POINT.  `wdc_command(ATAPI_PKT_CMD)` sets PHASE_CMDOUT.
 *  A following `wdc_command(WDCC_WRITE)` clears the flag at the top of the function
 *  and arms the write -- but NOTHING RESETS THE PHASE.  So the device sits with
 *  `phase == PHASE_CMDOUT`, `atapi_cmd_in_progress == 0`, and a disk write armed:
 *  exactly the state a phase-only guard cannot tell from a real CDB collection.
 *
 *  Under that mutant, the guest's own sector payload reaches occupancy 12 and the
 *  first twelve bytes are issued as a SCSI command AND removed from the pending
 *  sector.  Both conjuncts are load-bearing; `#477`'s "key on the phase, not on
 *  the flag" was the wrong headline and is corrected in place.
 *
 *  (The stale phase is itself a defect and is filed as part of `wdcwipclear` /
 *  `wdcringnoflush` -- a new command does not reset what the old one left.)
 */
static void row_stale_phase_write(void)
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
		printf("  SETUP stale_phase inbuf failed\n");
		return;
	}

	stub_disk_exists = 1;
	d.seccnt = 1;
	d.sector = 1;

	/*  a packet command, which is what leaves PHASE_CMDOUT behind  */
	wdc_command(fake_cpu(), &d, ATAPI_PKT_CMD);

	/*  then an ordinary ATA write.  This clears the flag and arms the write; the
	    phase is NOT reset, which is the state under test.  */
	wdc_command(fake_cpu(), &d, WDCC_WRITE);

	rows ++;
	if (d.atapi_phase != PHASE_CMDOUT || d.atapi_cmd_in_progress != 0 ||
	    d.write_in_progress == 0) {
		printf("  FAIL %-38s phase %i flag %i wip %i\n",
		    "LIVENESS: stale CMDOUT with a write",
		    d.atapi_phase, d.atapi_cmd_in_progress,
		    d.write_in_progress);
		failures ++;
	} else {
		printf("  ok   %-38s phase 0x%x\n",
		    "LIVENESS: stale CMDOUT with a write", d.atapi_phase);
	}

	/*  the guest streams one legal sector, 256 sixteen-bit stores  */
	stub_scsi_cmds = 0;
	stub_disk_writes = 0;
	stub_disk_bytes = 0;
	for (i = 0; i < 256; i++) {
		buf[0] = 0x6b; buf[1] = 0x6b;
		buf[2] = 0; buf[3] = 0;
		dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_WRITE, &d);
	}

	/*  NO byte of a disk payload may be issued as a SCSI command...  */
	rows ++;
	if (stub_scsi_cmds != 0) {
		printf("  FAIL %-38s %i SCSI dispatch(es)\n",
		    "disk payload is not issued as a CDB", stub_scsi_cmds);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "disk payload is not issued as a CDB", stub_scsi_cmds);
	}

	/*  ...and the sector must arrive INTACT, which is the half that catches a
	    mutant that merely eats the bytes without dispatching.  */
	rows ++;
	if (stub_disk_writes != 1 || stub_disk_bytes != 512) {
		printf("  FAIL %-38s %i w, %i b\n",
		    "the sector survives a stale phase",
		    stub_disk_writes, stub_disk_bytes);
		failures ++;
	} else {
		printf("  ok   %-38s %i w, %i b\n",
		    "the sector survives a stale phase",
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

#  the harness needs diskimage_exist answerable; inert by default, exactly as the
#  file's own stub_datain_len / stub_cdrom_poison controls are.
OLDEX = ('int diskimage_exist(struct machine *machine, int id, int type)' + NL +
         '{' + NL + chr(9) + '(void)machine; (void)id; (void)type;' + NL +
         chr(9) + 'return 0;' + NL + '}' + NL)
if s.count(OLDEX) == 1:
    s = s.replace(OLDEX,
        'static int stub_disk_exists = 0;' + chr(9) + '/*  inert by default  */' + NL + NL +
        'int diskimage_exist(struct machine *machine, int id, int type)' + NL + '{' + NL +
        chr(9) + '(void)machine; (void)id; (void)type;' + NL +
        chr(9) + 'return stub_disk_exists;' + NL + '}' + NL, 1)
    print("  stub_disk_exists control added (inert by default)")

anchor = NL + NL + "static void row_arm_overrun(void)"
assert s.count(anchor) == 1, "anchor %d" % s.count(anchor)
s = s.replace(anchor, ROW + NL + "static void row_arm_overrun(void)", 1)

reg = chr(9) + "row_partial_sector();" + NL
assert s.count(reg) == 1, "reg %d" % s.count(reg)
s = s.replace(reg, reg + chr(9) + "row_stale_phase_write();" + NL, 1)

for a, b in [("if (rows != 52) {", "if (rows != 55) {"),
             ("rows = %i, want 52", "rows = %i, want 55")]:
    assert s.count(a) == 1, "%r %d" % (a, s.count(a))
    s = s.replace(a, b, 1)

for lbl in ("LIVENESS: stale CMDOUT with a write",
            "disk payload is not issued as a CDB",
            "the sector survives a stale phase"):
    assert len(lbl) < 38, "label %d chars: %s" % (len(lbl), lbl)
    print("  label ok (%2d < 38): %s" % (len(lbl), lbl))

io.open(DET, "w", encoding="utf-8", newline="").write(s)
print("  row_stale_phase_write appended to the REPO detector, pin -> 55")
