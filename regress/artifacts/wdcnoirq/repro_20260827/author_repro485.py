"""#485 REPRODUCTION, test-first, against the COMMITTED build.  REPO IS NOT TOUCHED.

`wdcnoirq`: `wdc_command()` has FOUR arms that terminate a command with `WDCE_ABRT`.  Two of
them also set `d->int_assert = 1`; two do not.

    :686-687   no disk image                      ABRT + int_assert   <- asserts
    :694-695   IDENTIFY on an ATAPI drive         ABRT + int_assert   <- asserts
    :799-800   the five WDCC_SEC_* commands       ABRT, NO assert     <- DEFECT
    :818       `default:` (unimplemented opcode)  ABRT, NO assert     <- DEFECT

*** THE WARRANT IS TRANSFERRED FROM INSIDE THE SAME FUNCTION, which is the strongest range
this project recognises: same function, same semantic (abort a command), opposite behaviour.
No specification needs to be cited, and none is available -- there is no ATA document in this
tree. ***

THE ORACLE IS THE WIRE, NOT THE FIELD.  `d->int_assert` is only a request; `DEVICE_TICK(wdc)`
is what turns it into `INTERRUPT_ASSERT(d->irq)`.  A row asserting the FIELD would pass a
mutant that sets the field and breaks the tick.  So every leg below runs the real tick and
counts real sink calls, and reports the field alongside it for diagnosis only.

SHAPE: a 256-OPCODE SWEEP over the invariant **ABRT implies ASSERT**, with a fresh device per
opcode.  Two observables, not one -- #483 measured that a sweep with a narrow oracle can be
strictly WEAKER than a point pin, so this varies the input AND reads both effects.

  CONTROL A (liveness, and it uses an arm the fix does not touch): with NO disk image every
  opcode takes the `:686` arm, which asserts today.  If this leg does not show asserts, the
  harness cannot observe an assert at all and the defect legs mean nothing.

  CONTROL B (denominator): the count of opcodes actually exercised is COUNTED, never written.
  A literal denominator is a denominator that cannot fail -- shipped once in #483 and caught
  by a seat.
"""
import io
import os
import shutil

NL, T, BS = chr(10), chr(9), chr(92)
N = BS + "n"
ROOT = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC"
OUT = (r"C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-CC-GXEMUL"
       r"\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\r485")

src = io.open(os.path.join(ROOT, "regress", "diff_wdc_identify.c"),
              encoding="utf-8", newline="").read()

ROW = '''

/*  #485 REPRO `wdcnoirq`: an aborted command must still raise the completion
 *  interrupt, and two of the four abort arms do not.
 *
 *  THE ORACLE IS THE WIRE.  `d->int_assert` is a request; DEVICE_TICK(wdc) is
 *  what calls INTERRUPT_ASSERT.  Reading the field alone would pass a mutant
 *  that sets the field and breaks the tick, so each leg runs the real tick and
 *  counts real sink calls.  The field is printed for diagnosis only.
 */
static void repro_abort_asserts(void)
{
	int v, ran = 0;
	int ctl_abrt = 0, ctl_irq = 0;		/*  no disk: the asserting arm  */
	int bad_first = -1, bad_n = 0;		/*  ABRT with no interrupt      */
	int ok_n = 0;				/*  ABRT with an interrupt      */
	int quiet_n = 0;			/*  no ABRT (implemented)       */

	/*  CONTROL A -- LIVENESS, on an arm this fix does not touch.  With no
	    disk image every opcode takes the no-disk arm, which sets ABRT and
	    asserts today.  If this leg reads 0 the harness cannot see an
	    assert at all and every leg below is meaningless.  */
	{
		struct wdc_data d;
		altctl_fresh(&d);
		if (d.inbuf == NULL) { printf("  SETUP noirq ctl@N@"); return; }
		stub_disk_exists = 0;
		arm_asserts = 0;
		wdc_command(fake_cpu(), &d, 0x5a);
		dev_wdc_tick(fake_cpu(), &d);
		ctl_abrt = (d.error & WDCE_ABRT) ? 1 : 0;
		ctl_irq  = arm_asserts;
		altctl_free(&d);
	}

	/*  THE SWEEP.  A fresh device per opcode; disk present, so the no-disk
	    arm is out of the way and each opcode reaches its real handler.  */
	for (v = 0; v < 256; v++) {
		struct wdc_data d;
		int abrt, irq;

		altctl_fresh(&d);
		if (d.inbuf == NULL)
			continue;
		ran ++;
		stub_disk_exists = 1;
		arm_asserts = 0;
		wdc_command(fake_cpu(), &d, v);
		dev_wdc_tick(fake_cpu(), &d);
		abrt = (d.error & WDCE_ABRT) ? 1 : 0;
		irq  = arm_asserts;

		if (abrt && irq == 0) {
			bad_n ++;
			if (bad_first < 0)
				bad_first = v;
		} else if (abrt) {
			ok_n ++;
		} else {
			quiet_n ++;
		}
		altctl_free(&d);
	}
	stub_disk_exists = 0;

	rows ++;
	printf("  REPRO ctl(no disk) abrt=%i irq=%i | swept %i | ABRT+irq %i |"
	    " ABRT+NO-irq %i first=0x%02x | no-ABRT %i@N@",
	    ctl_abrt, ctl_irq, ran, ok_n, bad_n, bad_first, quiet_n);
	printf("  REPRO want  ctl abrt=1 irq=1 | swept 256 | ABRT+NO-irq 0@N@");
	if (ctl_abrt != 1 || ctl_irq != 1 || ran != 256 || bad_n != 0) {
		printf("  FAIL %-38s see REPRO lines above@N@",
		    "an aborted command raises its irq");
		failures ++;
	} else {
		printf("  ok   %-38s %i swept, %i abort+irq@N@",
		    "an aborted command raises its irq", ran, ok_n);
	}
}

'''.replace("@N@", N)

anchor = NL + NL + "static void row_arm_overrun(void)"
assert src.count(anchor) == 1, "anchor %d" % src.count(anchor)
reg = T + "row_reset_bit_iff();" + NL
assert src.count(reg) == 1, "reg %d" % src.count(reg)

s = src.replace(anchor, ROW + NL + "static void row_arm_overrun(void)", 1)
s = s.replace(reg, reg + T + "repro_abort_asserts();" + NL, 1)
for a, b in [("if (rows != 103) {", "if (rows != 104) {"),
             ("rows = %i, want 103", "rows = %i, want 104")]:
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
print("  #485 reproduction written to r485/; REPO NOT TOUCHED")
