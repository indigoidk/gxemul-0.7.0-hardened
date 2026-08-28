"""#485's detector.  FOUR legs, and every one of them exists because a measured mutant
escaped the two-observable sweep I first designed.

  M9_notailtick   delete dev_wdc_access's tail call to dev_wdc_tick.  My repro called
                  wdc_command() and then ran the tick BY HAND, so it could not see this
                  at all.  Leg 1 drives the REAL REGISTER PATH instead.
  M4_hoist        one `int_assert = 1` after the switch.  "Fixes" all 242 and silently
                  starts asserting at dispatch for the three DEFERRED opcodes.  My
                  two-bucket oracle read ABRT+NO-irq = 0 and passed it.  Leg 1 now pins
                  the silent set as an IDENTITY, not a count.
  M5_inlatch      move the assert inside `if (!d->warned_unimpl_cmd)`.  Only the FIRST
                  unimplemented command per device interrupts.  A sweep with one fresh
                  device per opcode CANNOT SEE IT -- the latch is 0 on every leg.  Leg 2.
  M7_noclear      the STATUS read stops clearing the request.  int_assert is a LEVEL and
                  the tick re-raises it every ~16k instructions forever.  Leg 3.
  M8_sfabortonly  SET_FEATURES asserts only on its abort sub-case.  My sweep varies the
                  command byte and never `precomp`, so the SUCCESS path never ran.
                  Input coverage in ONE dimension is not input coverage.  Leg 4.
"""
import io
import os
import shutil

NL, T, BS = chr(10), chr(9), chr(92)
N = BS + "n"
ROOT = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC"
OUT = (r"C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-CC-GXEMUL"
       r"\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\r485c")

src = io.open(os.path.join(ROOT, "regress", "diff_wdc_identify.c"),
              encoding="utf-8", newline="").read()

ROW = '''

static int cmpl_de = 0;
static void cmpl_desink(struct interrupt *a) { (void)a; cmpl_de++; }

/*  #485: a command that TERMINATES must raise its completion interrupt.
 *
 *  THE INVARIANT, derived over all 256 opcodes: every command wdc_command()
 *  FINISHES asserts.  The only silent opcodes are the THREE that hand control
 *  back for a data phase -- WDCC_WRITE, WDCC_WRITEMULTI, ATAPI_PKT_CMD -- each
 *  of which asserts when its data phase drains.
 *
 *  *** EVERY LEG BELOW EXISTS BECAUSE A MEASURED MUTANT ESCAPED THE
 *  TWO-OBSERVABLE SWEEP THIS ROUND FIRST DESIGNED. ***  The reproduction called
 *  wdc_command() directly and ran the tick by hand; that cannot see a fix whose
 *  repair depends on dev_wdc_access()'s tail calling the tick.  So leg 1 drives
 *  the REAL REGISTER PATH.
 */
static void row_completion_irq(void)
{
	struct wdc_data d;
	unsigned char buf[8];
	int v, ran = 0, abrt_noirq = 0, first_bad = -1;
	int silent[8], nsilent = 0, i;
	int second = -1, retract_de = -1, retract_field = -1, retract_re = -1;
	int sf_irq = -1, sf_abrt = -1;

	/*  LEG 1 -- THE SWEEP, THROUGH THE REGISTER PATH.  A command STORE, not a
	    direct call, so dev_wdc_access's tail tick is inside the measurement.  */
	for (v = 0; v < 256; v++) {
		altctl_fresh(&d);
		if (d.inbuf == NULL)
			continue;
		ran ++;
		stub_disk_exists = 1;
		d.irq.interrupt_assert = arm_sink;
		d.irq.interrupt_deassert = cmpl_desink;
		arm_asserts = 0;
		buf[0] = v;
		dev_wdc_access(fake_cpu(), NULL, wd_command, buf, 1,
		    MEM_WRITE, &d);
		if (arm_asserts == 0) {
			if (nsilent < 8)
				silent[nsilent] = v;
			nsilent ++;
			if ((d.error & WDCE_ABRT) && abrt_noirq ++ == 0)
				first_bad = v;
		}
		altctl_free(&d);
	}

	/*  LEG 2 -- A SECOND UNIMPLEMENTED COMMAND ON *ONE* DEVICE.  Kills the
	    edit that moves the assert inside the warned_unimpl_cmd latch, which a
	    fresh-device-per-opcode sweep cannot see at any oracle width.  */
	altctl_fresh(&d);
	if (d.inbuf != NULL) {
		stub_disk_exists = 1;
		d.irq.interrupt_assert = arm_sink;
		d.irq.interrupt_deassert = cmpl_desink;
		buf[0] = 0xaa;
		dev_wdc_access(fake_cpu(), NULL, wd_command, buf, 1, MEM_WRITE, &d);
		buf[0] = wd_command;
		dev_wdc_access(fake_cpu(), NULL, wd_command, buf, 1, MEM_READ, &d);
		arm_asserts = 0;
		buf[0] = 0xab;			/*  a DIFFERENT unknown opcode  */
		dev_wdc_access(fake_cpu(), NULL, wd_command, buf, 1, MEM_WRITE, &d);
		second = arm_asserts;
		altctl_free(&d);
	}

	/*  LEG 3 -- RETRACTION.  int_assert is a LEVEL: dev_wdc_tick re-raises it
	    every tick until a STATUS read clears it, so a set-and-never-cleared
	    request is asserted forever.  Only this leg sees that.  */
	altctl_fresh(&d);
	if (d.inbuf != NULL) {
		stub_disk_exists = 1;
		d.irq.interrupt_assert = arm_sink;
		d.irq.interrupt_deassert = cmpl_desink;
		buf[0] = 0xaa;
		dev_wdc_access(fake_cpu(), NULL, wd_command, buf, 1, MEM_WRITE, &d);
		cmpl_de = 0;
		dev_wdc_access(fake_cpu(), NULL, wd_command, buf, 1, MEM_READ, &d);
		retract_de = cmpl_de;
		retract_field = d.int_assert;
		arm_asserts = 0;
		dev_wdc_tick(fake_cpu(), &d);
		retract_re = arm_asserts;
		altctl_free(&d);
	}

	/*  LEG 4 -- SET_FEATURES' *SUCCESS* SUB-CASE.  The sweep varies the command
	    byte and never `precomp`, so this path never ran: input coverage in one
	    dimension is not input coverage.  It must assert AND not abort.  */
	altctl_fresh(&d);
	if (d.inbuf != NULL) {
		stub_disk_exists = 1;
		d.irq.interrupt_assert = arm_sink;
		d.irq.interrupt_deassert = cmpl_desink;
		d.precomp = WDSF_SET_MODE;
		arm_asserts = 0;
		buf[0] = SET_FEATURES;
		dev_wdc_access(fake_cpu(), NULL, wd_command, buf, 1, MEM_WRITE, &d);
		sf_irq = arm_asserts;
		sf_abrt = (d.error & WDCE_ABRT) ? 1 : 0;
		altctl_free(&d);
	}
	stub_disk_exists = 0;

	rows ++;
	printf("  IRQ swept %i | ABRT+NO-irq %i first 0x%02x | silent %i:",
	    ran, abrt_noirq, first_bad, nsilent);
	for (i = 0; i < nsilent && i < 8; i++)
		printf(" 0x%02x", silent[i]);
	printf(" | 2nd %i | retract de=%i f=%i re=%i | sf irq=%i abrt=%i@N@",
	    second, retract_de, retract_field, retract_re, sf_irq, sf_abrt);

	/*  THE SILENT SET IS PINNED AS AN IDENTITY, NOT A COUNT.  A single
	    `int_assert = 1` hoisted after the switch reads ABRT+NO-irq == 0 and
	    passes a count-only oracle, while starting to assert at DISPATCH for
	    the three deferred opcodes -- a spurious completion interrupt on every
	    disk write a real guest issues.  */
	if (ran != 256 || abrt_noirq != 0 || nsilent != 3 ||
	    silent[0] != WDCC_WRITE || silent[1] != ATAPI_PKT_CMD ||
	    silent[2] != WDCC_WRITEMULTI ||
	    second != 1 || retract_de != 1 || retract_field != 0 ||
	    retract_re != 0 || sf_irq != 1 || sf_abrt != 0) {
		printf("  FAIL %-38s see the IRQ line above@N@",
		    "a terminated command raises its irq");
		failures ++;
	} else {
		printf("  ok   %-38s 256 swept, 3 deferred@N@",
		    "a terminated command raises its irq");
	}
}

'''.replace("@N@", N)

anchor = NL + NL + "static void row_arm_overrun(void)"
assert src.count(anchor) == 1, "anchor %d" % src.count(anchor)
reg = T + "row_ring_occupancy_sound();" + NL
assert src.count(reg) == 1, "reg %d" % src.count(reg)

s = src.replace(anchor, ROW + NL + "static void row_arm_overrun(void)", 1)
s = s.replace(reg, reg + T + "row_completion_irq();" + NL, 1)
for a, b in [("if (rows != 127) {", "if (rows != 128) {"),
             ("rows = %i, want 127", "rows = %i, want 128")]:
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
print("  #485 detector written to r485c/ -- 4 legs.  REPO NOT TOUCHED YET.")
