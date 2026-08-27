"""The ACCEPT row for the bad-len decline, and it exists because my own candidate
was about to ship a regression.

The `D`/`AD` variants set `badlen_seen` as a STRUCT FIELD, which latches for the life
of the device: after one 3- or 8-byte store, every later legal write is silently
dropped.  The 45-row baseline did not catch it because no row performs a legal write
AFTER a bad-len one -- so "all green" was measuring the wrong thing.

This is the de-escalation clause's accept side: a fix that removes a write must prove
the LEGAL write still lands.  The row is written to red on the persistent form and
pass on a per-access local.
"""
import io, os

NL = chr(10)
SCR = (r"C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-CC-GXEMUL"
       r"\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad")
DET = os.path.join(SCR, "drain", "regress", "diff_wdc_identify.c")

ROW = r'''

/*  THE ACCEPT ROW FOR THE BAD-LEN DECLINE.
 *
 *  A fix that declines the drain after an unimplemented width MUST NOT latch that
 *  decision for the life of the device.  If the flag is a struct field, one 8-byte
 *  store silences every subsequent legal write -- turning a corruption defect into
 *  a silent data-loss defect, which is worse.
 *
 *  Sequence: one bad-len (8-byte) store, then a full LEGAL 512-byte write via
 *  256 two-byte stores.  The legal write MUST reach the disk image.
 *
 *  Expected: RED under a persistent struct-field flag; GREEN under a per-access
 *  local.  That is the whole point of the row -- it distinguishes two fixes that
 *  the four corruption rows score identically.
 */
static void row_badlen_then_legal(void)
{
	struct wdc_data h;
	unsigned char buf[8];
	int i;

	memset(&h, 0, sizeof(h));
	h.addr_mult  = 1;
	h.io_enabled = 1;
	h.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
	h.irq.interrupt_assert = arm_sink;
	if (h.inbuf == NULL) {
		printf("  SETUP badlen_then_legal inbuf failed\n");
		return;
	}

	h.write_in_progress = WDCC_WRITE;
	h.write_count  = 1;
	h.write_offset = 0xb000;

	/*  (1) the bad-len store -- pushes nothing, must drain nothing  */
	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 8, MEM_WRITE, &h);

	/*  (2) a full legal sector, 256 two-byte stores carrying 0x77  */
	stub_disk_writes = 0;
	stub_disk_bytes = 0;
	stub_disk_first = -1;
	for (i = 0; i < 256; i++) {
		buf[0] = 0x77; buf[1] = 0x77;
		buf[2] = 0; buf[3] = 0;
		dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_WRITE, &h);
	}

	rows ++;
	if (stub_disk_writes != 1 || stub_disk_bytes != 512) {
		printf("  FAIL %-38s %i write(s), %i bytes\n",
		    "a legal write after a bad-len lands",
		    stub_disk_writes, stub_disk_bytes);
		failures ++;
	} else {
		printf("  ok   %-38s %i write(s), %i bytes\n",
		    "a legal write after a bad-len lands",
		    stub_disk_writes, stub_disk_bytes);
	}

	free(h.inbuf);
}

'''

s = io.open(DET, encoding="utf-8", newline="").read()

anchor = NL + NL + "static void row_arm_overrun(void)"
assert s.count(anchor) == 1, "anchor %d" % s.count(anchor)
s = s.replace(anchor, ROW + NL + "static void row_arm_overrun(void)", 1)

reg = chr(9) + "row_pkt_drain();" + NL
assert s.count(reg) == 1, "reg %d" % s.count(reg)
s = s.replace(reg, reg + chr(9) + "row_badlen_then_legal();" + NL, 1)

for a, b in [("if (rows != 49) {", "if (rows != 50) {"),
             ("rows = %i, want 49", "rows = %i, want 50")]:
    assert s.count(a) == 1, "%r %d" % (a, s.count(a))
    s = s.replace(a, b, 1)

io.open(DET, "w", encoding="utf-8", newline="").write(s)
lbl = "a legal write after a bad-len lands"
assert len(lbl) < 38, "label %d chars" % len(lbl)
print("  accept row appended (label %d chars, pin -> 50)" % len(lbl))
