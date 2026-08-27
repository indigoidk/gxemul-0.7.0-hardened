"""MEASURE `wdcfloodstale` myself, instead of carrying a seat's number.

The ledger has it at BELIEVED: two independent READINGS plus one seat's offline measurement.
This builds my own, and it measures BOTH halves -- the death AND the remedy -- because a
death measurement without a working replacement is only half a finding.

  LEG 1  THE DEATH.  1026 IDENTIFY commands through `wdc_command()`, exactly what
         `wdc_flood_probe.py`'s `overrun x2` row drives.  The row wants the latched overrun
         message ONCE.  `wdc_command()` calls `wdc_new_command_reset()` unconditionally, which
         zeroes both pointers, and IDENTIFY then stages 512 bytes -- so occupancy after any
         command is at most 512 and 1026 commands cannot lap a 262656-byte ring.
         EXPECT: 0 overrun messages.  The row is dead.

  LEG 2  THE CONTROL, and it is what makes leg 1 a finding rather than a broken harness.
         Neuter the reset (the pre-#479 shape) and drive the SAME 1026 commands.
         EXPECT: 1.  If leg 2 also reads 0, my harness cannot see the message at all and
         leg 1 proves nothing.

  LEG 3  THE REMEDY.  The same overrun driven through the guest data-port WRITE arm, which
         takes no `wdc_command()` and therefore no reset -- the only surviving wrap route.
         EXPECT: 1.  This is the stimulus the row must be re-aimed at.

Built against the COMMITTED source; the repo is not touched.
"""
import io
import os
import shutil

NL, T = chr(10), chr(9)
SEC = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC"
OUT = (r"C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-CC-GXEMUL"
       r"\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\fs")

ROW = '''

/*  wdcfloodstale: measure the death AND the remedy.  */
static void row_floodstale(void)
{
	struct wdc_data d;
	unsigned char buf[8];
	int i, msgs_live, msgs_ctl, msgs_port;

	/*  LEG 1 -- THE DEATH.  1026 IDENTIFY commands, the probe's own stimulus.  */
	altctl_fresh(&d);
	if (d.inbuf == NULL) { printf("  SETUP fs1@N@"); return; }
	stub_disk_exists = 1; stub_size = 512L*1024*1024;
	stub_fatals = 0;
	for (i = 0; i < 1026; i++)
		wdc_command(fake_cpu(), &d, WDCC_IDENTIFY);
	msgs_live = stub_fatals;
	altctl_free(&d);

	/*  LEG 2 -- THE CONTROL.  The same 1026 commands with the ring NOT reset
	    between them: the pre-#479 shape, reproduced by pushing IDENTIFY's
	    payload directly instead of going through wdc_command().  If this
	    reads 0 too, the harness cannot see the message and leg 1 is void.  */
	altctl_fresh(&d);
	if (d.inbuf == NULL) { printf("  SETUP fs2@N@"); return; }
	stub_fatals = 0;
	for (i = 0; i < 1026 * 512; i++)
		wdc_addtoinbuf(&d, 0x11);
	msgs_ctl = stub_fatals;
	altctl_free(&d);

	/*  LEG 3 -- THE REMEDY.  The same overrun through the guest DATA PORT with
	    no tenant armed.  No wdc_command(), so no reset.  */
	altctl_fresh(&d);
	if (d.inbuf == NULL) { printf("  SETUP fs3@N@"); return; }
	stub_fatals = 0;
	for (i = 0; i < WDC_INBUF_SIZE / 2 + 8; i++) {
		buf[0] = 0x22; buf[1] = 0x22;
		dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_WRITE, &d);
	}
	msgs_port = stub_fatals;
	stub_disk_exists = 0;
	altctl_free(&d);

	rows ++;
	printf("  FLOODSTALE  leg1(1026 IDENTIFY)=%i  leg2(control, no reset)=%i"
	    "  leg3(data port)=%i@N@", msgs_live, msgs_ctl, msgs_port);
	printf("  FLOODSTALE  want  leg1=0 (the row is DEAD)  leg2>0 (harness works)"
	    "  leg3>0 (the remedy)@N@");
	if (msgs_live != 0 || msgs_ctl == 0 || msgs_port == 0) {
		printf("  FAIL %-38s see FLOODSTALE lines@N@", "wdcfloodstale measured");
		failures ++;
	} else {
		printf("  ok   %-38s dead=%i ctl=%i remedy=%i@N@",
		    "wdcfloodstale measured", msgs_live, msgs_ctl, msgs_port);
	}
}

'''.replace("@N@", chr(92) + "n")

src = io.open(os.path.join(SEC, "regress", "diff_wdc_identify.c"),
              encoding="utf-8", newline="").read()
anchor = NL + NL + "static void row_arm_overrun(void)"
assert src.count(anchor) == 1, "anchor %d" % src.count(anchor)
reg = T + "row_ring_occupancy_sound();" + NL
assert src.count(reg) == 1, "reg %d" % src.count(reg)
s = src.replace(anchor, ROW + NL + "static void row_arm_overrun(void)", 1)
s = s.replace(reg, reg + T + "row_floodstale();" + NL, 1)
for a, b in [("if (rows != 127) {", "if (rows != 128) {"),
             ("rows = %i, want 127", "rows = %i, want 128")]:
    assert s.count(a) == 1, "%r %d" % (a, s.count(a))
    s = s.replace(a, b, 1)

shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(os.path.join(OUT, "regress"))
os.makedirs(os.path.join(OUT, "src", "devices"))
io.open(os.path.join(OUT, "regress", "diff_wdc_identify.c"),
        "w", encoding="utf-8", newline="").write(s)
shutil.copy(os.path.join(SEC, "src", "devices", "dev_wdc.c"),
            os.path.join(OUT, "src", "devices", "dev_wdc.c"))
print("  floodstale measurement harness written; REPO NOT TOUCHED")
