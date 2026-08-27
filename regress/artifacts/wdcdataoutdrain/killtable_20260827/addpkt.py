"""Append the WRITE+PKT door to the GENERATED detector as plain C.

Written this way on purpose: generating C through a Python list of escaped string
fragments cost three separate quoting failures in a row (a cooked \\n, a mismatched
paren, an unterminated literal).  Here the C is C.
"""
import io, os

NL = chr(10)
SCR = (r"C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-CC-GXEMUL"
       r"\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad")
DET = os.path.join(SCR, "drain", "regress", "diff_wdc_identify.c")

ROW = r'''

/*  THE WRITE+PKT DOOR, measured independently by the Fable seat.
 *
 *  No bad-len access is involved at all.  A WRITE is in progress AND a packet
 *  command is being assembled; the 12-byte CDB dispatches, and the dispatch loop
 *  consumes the LOCAL `inbuf_len` down to 0 while pushing fresh DATA-IN bytes into
 *  the ring.  The drain below therefore reads a STALE ZERO and fires, putting the
 *  guest's own returned DATA-IN payload on the disk image.
 *
 *  This door is closed by `inbuf_len > 0` (the stale local is 0) and is NOT closed
 *  by declining the bad-len width, because no bad-len access occurs.  The leftover
 *  door is the exact mirror.  That is why neither edit alone is sufficient.
 */
static void row_pkt_drain(void)
{
	struct wdc_data g;
	unsigned char buf[8];
	int i;

	memset(&g, 0, sizeof(g));
	g.addr_mult  = 1;
	g.io_enabled = 1;
	g.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
	g.irq.interrupt_assert = arm_sink;
	if (g.inbuf == NULL) {
		printf("  SETUP pkt_drain inbuf failed\n");
		return;
	}

	/*  the real device sets all three together  */
	g.cur_command = ATAPI_PKT_CMD;
	g.atapi_cmd_in_progress = 1;
	g.atapi_phase = PHASE_CMDOUT;

	/*  ...and a disk WRITE is live at the same time  */
	g.write_in_progress = WDCC_WRITE;
	g.write_count  = 1;
	g.write_offset = 0xa000;

	for (i = 0; i < 10; i++)
		wdc_addtoinbuf(&g, 0x5a);

	stub_datain_len = 512;
	stub_disk_writes = 0;
	stub_disk_first = -1;
	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_WRITE, &g);
	stub_datain_len = 0;

	rows ++;
	if (stub_disk_writes != 0) {
		printf("  FAIL %-38s %i write(s), first=0x%02x\n",
		    "a CDB dispatch does not drain to disk",
		    stub_disk_writes, stub_disk_first);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "a CDB dispatch does not drain to disk", stub_disk_writes);
	}

	if (g.atapi_st != NULL) {
		free(g.atapi_st->data_in);
		free(g.atapi_st->cmd);
		free(g.atapi_st);
	}
	free(g.inbuf);
}

'''

s = io.open(DET, encoding="utf-8", newline="").read()

anchor = NL + NL + "static void row_arm_overrun(void)"
assert s.count(anchor) == 1, "anchor %d" % s.count(anchor)
s = s.replace(anchor, ROW + NL + "static void row_arm_overrun(void)", 1)

reg = chr(9) + "row_dataout_drain();" + NL
assert s.count(reg) == 1, "reg %d" % s.count(reg)
s = s.replace(reg, reg + chr(9) + "row_pkt_drain();" + NL, 1)

for a, b in [("if (rows != 48) {", "if (rows != 49) {"),
             ("rows = %i, want 48", "rows = %i, want 49")]:
    assert s.count(a) == 1, "%r %d" % (a, s.count(a))
    s = s.replace(a, b, 1)

io.open(DET, "w", encoding="utf-8", newline="").write(s)
lbl = "a CDB dispatch does not drain to disk"
assert len(lbl) < 38, "label %d chars" % len(lbl)
print("  WRITE+PKT door appended as plain C (label %d chars, pin -> 49)" % len(lbl))
