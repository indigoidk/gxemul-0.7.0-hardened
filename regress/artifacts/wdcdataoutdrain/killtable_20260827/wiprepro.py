"""wdcwipclear -- REPRODUCTION for the ALIAS ROOT, built against the current tree.

`wdc_command()` clears `atapi_cmd_in_progress` and `error`, and does NOT clear
`write_in_progress`.  So a packet command arriving mid-WRITE leaves BOTH live and the
one shared ring serves two masters -- which is the root the Opus seat measured, and the
reason #478 is a point-guard rather than a closure.

NOT part of #478.  The stopping rule keeps a new finding out of a round that is already
built, so this is evidence for its own round.  Built in the scratchpad; the repo is not
touched.

TWO harness needs, both following the file's own inert-by-default idiom:
  * `diskimage_exist` returns 0 hardcoded, so wdc_command aborts before the switch and
    write_in_progress is never set.  A control makes it answerable; default 0 keeps
    every existing row byte-identical.
  * the row carries a LIVENESS control -- it asserts the flag IS set after the WRITE
    command, so a vacuous pass (nothing ever happened) cannot be mistaken for a fix.
"""
import io, os, shutil

NL, T = chr(10), chr(9)
ROOT = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC"
OUT = (r"C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-CC-GXEMUL"
       r"\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\wip")

s = io.open(os.path.join(ROOT, "regress", "diff_wdc_identify.c"),
            encoding="utf-8", newline="").read()

#  ---- 1. make diskimage_exist answerable, inert by default -------------------
OLDEX = ('int diskimage_exist(struct machine *machine, int id, int type)' + NL +
         '{' + NL +
         T + '(void)machine; (void)id; (void)type;' + NL +
         T + 'return 0;' + NL +
         '}' + NL)
assert s.count(OLDEX) == 1, "exist stub anchor %d" % s.count(OLDEX)
NEWEX = ('static int stub_disk_exists = 0;' + T + '/*  inert by default  */' + NL + NL +
         'int diskimage_exist(struct machine *machine, int id, int type)' + NL +
         '{' + NL +
         T + '(void)machine; (void)id; (void)type;' + NL +
         T + 'return stub_disk_exists;' + NL +
         '}' + NL)
s = s.replace(OLDEX, NEWEX, 1)

#  ---- 2. the row ------------------------------------------------------------
ROW = r'''

/*  wdcwipclear -- REPRODUCTION.  `wdc_command()` clears `atapi_cmd_in_progress`
 *  and `error`, and does NOT clear `write_in_progress`.
 *
 *  So a guest can issue WRITE SECTORS and then a packet command, and the device
 *  holds BOTH flags live at once: the one shared input ring is then serving the
 *  disk-write path and the CDB path simultaneously.  That is the root of the
 *  alias -- #478 guards the sink, this is the source.
 *
 *  LIVENESS CONTROL FIRST.  The row asserts the flag IS set after the WRITE
 *  command before asserting it is cleared by the next one, because otherwise a
 *  fixture where nothing happened at all would pass and read as a fix.
 */
static void row_wip_not_cleared(void)
{
	struct wdc_data d;

	memset(&d, 0, sizeof(d));
	d.addr_mult  = 1;
	d.io_enabled = 1;
	d.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
	d.irq.interrupt_assert = arm_sink;
	if (d.inbuf == NULL) {
		printf("  SETUP wip inbuf failed\n");
		return;
	}

	/*  the command path aborts on a missing image, so the write would never be
	    set up at all and the row would pass for the wrong reason.  */
	stub_disk_exists = 1;
	d.seccnt = 1;
	d.sector = 1;

	wdc_command(fake_cpu(), &d, WDCC_WRITE);

	rows ++;
	if (d.write_in_progress == 0) {
		printf("  FAIL %-38s flag never set -- row is vacuous\n",
		    "LIVENESS: a WRITE arms write_in_prog");
		failures ++;
	} else {
		printf("  ok   %-38s 0x%x\n",
		    "LIVENESS: a WRITE arms write_in_prog", d.write_in_progress);
	}

	/*  now a packet command supersedes it.  wdc_command clears the ATAPI flag
	    here; it must clear this one too, or both are live at once.  */
	wdc_command(fake_cpu(), &d, ATAPI_PKT_CMD);

	rows ++;
	if (d.write_in_progress != 0) {
		printf("  FAIL %-38s still 0x%x with ATAPI live\n",
		    "a new command clears write_in_prog",
		    d.write_in_progress);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "a new command clears write_in_prog", d.write_in_progress);
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

anchor = NL + NL + "static void row_arm_overrun(void)"
assert s.count(anchor) == 1, "anchor %d" % s.count(anchor)
s = s.replace(anchor, ROW + NL + "static void row_arm_overrun(void)", 1)

reg = T + "row_partial_sector();" + NL
assert s.count(reg) == 1, "reg %d" % s.count(reg)
s = s.replace(reg, reg + T + "row_wip_not_cleared();" + NL, 1)

for a, b in [("if (rows != 52) {", "if (rows != 54) {"),
             ("rows = %i, want 52", "rows = %i, want 54")]:
    assert s.count(a) == 1, "%r %d" % (a, s.count(a))
    s = s.replace(a, b, 1)

for lbl in ("LIVENESS: a WRITE arms write_in_prog",
            "a new command clears write_in_prog"):
    assert len(lbl) < 38, "label %d chars: %s" % (len(lbl), lbl)
    print("  label ok (%2d < 38): %s" % (len(lbl), lbl))

if os.path.isdir(OUT):
    shutil.rmtree(OUT)
os.makedirs(os.path.join(OUT, "regress"))
os.makedirs(os.path.join(OUT, "src", "devices"))
io.open(os.path.join(OUT, "regress", "diff_wdc_identify.c"),
        "w", encoding="utf-8", newline="").write(s)
shutil.copy(os.path.join(ROOT, "src", "devices", "dev_wdc.c"),
            os.path.join(OUT, "src", "devices", "dev_wdc.c"))
print("  wip repro tree written; REPO NOT TOUCHED")
