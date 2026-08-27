"""*** THE ENTIRE DETECTOR HAS ONLY EVER TESTED ONE ENDIANNESS ARM. ***

Found by the Fable seat on #478's pass 2, and it is the largest coverage finding of the
session:

    det_mle.out and det_new.out are BYTE-IDENTICAL (md5 0d7abf97...)

`M_le_nobad` -- deleting `badlen_this = 1;` from the LITTLE-ENDIAN default only -- is
invisible to all 60 rows.  `fake_cpu()` memsets `stub_cpu` and never sets `byte_order`,
so it is 0, and the device tests `cpu->byte_order == EMUL_LITTLE_ENDIAN`.  Every row, and
therefore EVERY KILL TABLE THIS SESSION, exercised only the big-endian switch.

And the rung-3 witness machine, `evbmips -e malta`, is LITTLE-ENDIAN.  The detector tests
the opposite arm from the machine the defect was witnessed on.

THE FIX IS DELIBERATELY CONSERVATIVE.  `stub_byte_order` defaults to the value the harness
has always had, so no existing row changes behaviour -- a default flip would silently
re-point 78 rows at the other arm and any row that then failed would be indistinguishable
from a real defect.  New rows opt IN.
"""
import io

NL, T = chr(10), chr(9)
P = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\diff_wdc_identify.c"
s = io.open(P, encoding="utf-8", newline="").read()

OLD = ("static struct cpu *fake_cpu(void)" + NL +
       "{" + NL +
       T + "static int done = 0;" + NL +
       T + "if (!done) {" + NL +
       T*2 + "memset(&stub_machine, 0, sizeof(stub_machine));" + NL +
       T*2 + "memset(&stub_cpu, 0, sizeof(stub_cpu));" + NL +
       T*2 + "stub_cpu.machine = &stub_machine;" + NL +
       T*2 + "done = 1;" + NL +
       T + "}" + NL +
       T + "return &stub_cpu;" + NL +
       "}" + NL)
assert s.count(OLD) == 1, "fake_cpu anchor %d" % s.count(OLD)

NEW = ("/*  *** EVERY ROW IN THIS FILE TESTED ONE ENDIANNESS ARM UNTIL 2026-08-27." + NL +
       " *" + NL +
       " *  `stub_cpu` is memset to zero and nothing ever set `byte_order`, while the" + NL +
       " *  device branches on `cpu->byte_order == EMUL_LITTLE_ENDIAN`.  So the BIG-endian" + NL +
       " *  arm ran for every row -- and for every kill table measured against them." + NL +
       " *" + NL +
       " *  A seat proved it the only way that settles it: deleting `badlen_this = 1;`" + NL +
       " *  from the LITTLE-endian default alone produced a detector run BYTE-IDENTICAL" + NL +
       " *  to the unmutated one, same md5.  Not one row could tell them apart." + NL +
       " *" + NL +
       " *  The sting is that the rung-3 witness machine for this defect family," + NL +
       " *  `evbmips -e malta`, is LITTLE-endian.  The detector was testing the opposite" + NL +
       " *  arm from the machine the defect was witnessed on." + NL +
       " *" + NL +
       " *  THE DEFAULT IS DELIBERATELY UNCHANGED.  Flipping it would silently re-point" + NL +
       " *  every existing row at the other arm, and any row that then failed would be" + NL +
       " *  indistinguishable from a real defect.  New rows opt IN by setting this." + NL +
       " */" + NL +
       "static int stub_byte_order = 0;" + T + "/*  0 = the arm this file always ran  */" + NL + NL +
       "static struct cpu *fake_cpu(void)" + NL +
       "{" + NL +
       T + "static int done = 0;" + NL +
       T + "if (!done) {" + NL +
       T*2 + "memset(&stub_machine, 0, sizeof(stub_machine));" + NL +
       T*2 + "memset(&stub_cpu, 0, sizeof(stub_cpu));" + NL +
       T*2 + "stub_cpu.machine = &stub_machine;" + NL +
       T*2 + "done = 1;" + NL +
       T + "}" + NL +
       T + "stub_cpu.byte_order = stub_byte_order;" + NL +
       T + "return &stub_cpu;" + NL +
       "}" + NL)
s = s.replace(OLD, NEW, 1)

ROW = r'''

/*  THE LITTLE-ENDIAN ARM, which had ZERO coverage until now.
 *
 *  The width switch is duplicated once per endianness branch, and only the
 *  big-endian copy was ever reached.  A one-line deletion in the little-endian
 *  copy swept all 60 rows -- byte-identical output, same md5.
 *
 *  This runs the decline path through the OTHER arm.  It is not a duplicate of
 *  the big-endian rows: it is the same assertion against a second copy of the
 *  code, which is exactly what a duplicated switch requires.
 *
 *  `#337`'s comment records that `warned_badlen` is shared across the two arms
 *  BECAUSE they are mutually exclusive at runtime -- true, and it is also why a
 *  latch-based reading of the flag cannot distinguish them.  The rows must.
 */
static void row_little_endian_arm(void)
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
		printf("  SETUP le_arm inbuf failed\n");
		return;
	}

	stub_byte_order = EMUL_LITTLE_ENDIAN;

	/*  an unread payload, so a failed decline writes something identifiable  */
	for (i = 0; i < 512; i++)
		wdc_addtoinbuf(&d, 0xbe);

	d.write_in_progress = WDCC_WRITE;
	d.write_count  = 1;
	d.write_offset = 0x12000;

	stub_disk_writes = 0;
	stub_disk_first = -1;
	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 8, MEM_WRITE, &d);

	rows ++;
	if (stub_disk_writes != 0) {
		printf("  FAIL %-38s %i w, first=0x%02x\n",
		    "LE arm: leftover is not drained",
		    stub_disk_writes, stub_disk_first);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "LE arm: leftover is not drained", stub_disk_writes);
	}

	/*  and a LIVENESS control -- prove the LE arm was actually taken, or the
	    row above passes for the same reason it always did.  A 2-byte store
	    on this arm pushes low byte first; on the other, high byte first.  */
	d.inbuf_head = d.inbuf_tail = 0;
	buf[0] = 0x34; buf[1] = 0x12;
	buf[2] = 0; buf[3] = 0;
	dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_WRITE, &d);

	rows ++;
	if (d.inbuf[0] != 0x34) {
		printf("  FAIL %-38s first pushed 0x%02x, want 0x34\n",
		    "LIVENESS: the LE arm really ran", d.inbuf[0]);
		failures ++;
	} else {
		printf("  ok   %-38s 0x%02x\n",
		    "LIVENESS: the LE arm really ran", d.inbuf[0]);
	}

	stub_byte_order = 0;
	free(d.inbuf);
}

'''

anchor = NL + NL + "static void row_arm_overrun(void)"
assert s.count(anchor) == 1, "anchor %d" % s.count(anchor)
reg = T + "row_leftover_second_badlen();" + NL
assert s.count(reg) == 1, "reg %d" % s.count(reg)

for lbl in ("LE arm: leftover is not drained", "LIVENESS: the LE arm really ran"):
    assert len(lbl) < 38, "label %d chars: %s" % (len(lbl), lbl)
    print("  label ok (%2d < 38): %s" % (len(lbl), lbl))

s = s.replace(anchor, ROW + NL + "static void row_arm_overrun(void)", 1)
s = s.replace(reg, reg + T + "row_little_endian_arm();" + NL, 1)
for a, b in [("if (rows != 78) {", "if (rows != 80) {"),
             ("rows = %i, want 78", "rows = %i, want 80")]:
    assert s.count(a) == 1, "%r %d" % (a, s.count(a))
    s = s.replace(a, b, 1)

io.open(P, "w", encoding="utf-8", newline="").write(s)
print("  stub_byte_order added (default unchanged) + LE rows, pin -> 80")
