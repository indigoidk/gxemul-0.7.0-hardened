"""#485 L2: three legs that close eleven measured escapes.

*** ROOT CAUSE, IN ONE SENTENCE FROM THE MEASURING SEAT: `altctl_fresh()` memsets the device
and every leg writes ONLY the command register, so THE ENTIRE TASK FILE IS ZERO ON EVERY LEG.
I learned that for `precomp` and did not generalise it. ***

  Row F  ONE TASK-FILE-LOADED LEG.  Kills all NINE field-guard variants -- D1..D5 (the
         `default:` arm guarded on seccnt/head/cyl/sector/drive) and O2/O6/O9/O12 (both arms
         guarded on drive/seccnt/precomp/lba).  These are INSIDE clause (d)'s bound and not
         invented: the guarded body reads exactly those fields -- they are literally the
         fatal() arguments -- so the GUARD-FIELD-vs-BODY-FIELD check enumerates them
         mechanically.
  Row D  THE LEVEL IS HELD.  Kills O1 (assert the macro directly instead of the field) and
         O8 (the tick clears int_assert after asserting).  Leg 3 pins RETRACTION only -- that
         a STATUS read lowers the line.  NOTHING PINNED THAT THE REQUEST SURVIVES UNTIL THAT
         READ, so an edge assert satisfies leg 3 exactly.  The precise dual of M7_noclear:
         one direction of the level property was covered and the other was not.
  Row E  THE ABRT BIT, both arms, on the FIRST command.  Leg 1 counts ABRT only among opcodes
         that stayed SILENT -- so the moment the fix makes them assert, the ABRT half of the
         very same two-statement pair goes unpinned.  O4/O5 (delete the WDCE_ABRT from either
         arm) escaped for exactly that reason.
"""
import io

NL, T = chr(10), chr(9)
P = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\diff_wdc_identify.c"
s = io.open(P, encoding="utf-8", newline="")
s = s.read()

OLD = (T + "int sf_irq = -1, sf_abrt = -1;" + NL)
assert s.count(OLD) == 1, "decl anchor occurs %d times" % s.count(OLD)
s = s.replace(OLD, OLD +
 T + "int tf_sec = -1, tf_def = -1, held = -1, abrt_sec = -1, abrt_def = -1;" + NL, 1)

ANCHOR = (T + "stub_disk_exists = 0;" + NL + NL + T + "rows ++;" + NL)
assert s.count(ANCHOR) == 1, "tail anchor occurs %d times" % s.count(ANCHOR)

NEW = NL.join([
 "",
 T + "/*  ROW F -- A TASK FILE THAT IS NOT ALL ZERO.  *** THE ROOT CAUSE OF",
 T + "    ELEVEN MEASURED ESCAPES: altctl_fresh() memsets the device and every",
 T + "    leg above writes ONLY the command register, so the whole task file is",
 T + "    ZERO on every leg. ***  A guard added on ANY of those fields is then",
 T + "    true by default and the fix looks intact.",
 "",
 T + "    These are INSIDE clause (d)'s bound and are not invented predicates:",
 T + "    the `default:` arm's guarded body reads drive, head, cyl_hi, cyl_lo,",
 T + "    sector and seccnt -- they are literally the fatal() arguments -- so",
 T + "    the GUARD-FIELD-vs-BODY-FIELD check enumerates them mechanically.",
 "",
 T + "    Measured escapes closed here: the `default:` arm guarded on seccnt,",
 T + "    head, cyl, sector or drive, and BOTH arms guarded on drive, seccnt,",
 T + "    precomp or lba.  Nine variants, one leg.",
 "",
 T + "    The round had already learned this for `precomp` -- 'input coverage",
 T + "    in one dimension is not input coverage' -- and applied it only to",
 T + "    SET_FEATURES, not to the two arms the diff edits.  */",
 T + "altctl_fresh(&d);",
 T + "if (d.inbuf != NULL) {",
 T*2 + "stub_disk_exists = 1;",
 T*2 + "d.irq.interrupt_assert = arm_sink;",
 T*2 + "d.irq.interrupt_deassert = cmpl_desink;",
 T*2 + "d.precomp = 0x5a; d.seccnt = 0x11; d.sector = 0x22;",
 T*2 + "d.cyl_lo = 0x33; d.cyl_hi = 0x44;",
 T*2 + "d.drive = 0; d.head = 0x0e; d.lba = 1;",
 T*2 + "arm_asserts = 0;",
 T*2 + "buf[0] = WDCC_SEC_FREEZE_LOCK;",
 T*2 + "dev_wdc_access(fake_cpu(), NULL, wd_command, buf, 1, MEM_WRITE, &d);",
 T*2 + "tf_sec = arm_asserts;",
 T*2 + "buf[0] = wd_command;",
 T*2 + "dev_wdc_access(fake_cpu(), NULL, wd_command, buf, 1, MEM_READ, &d);",
 T*2 + "arm_asserts = 0;",
 T*2 + "buf[0] = 0xaa;",
 T*2 + "dev_wdc_access(fake_cpu(), NULL, wd_command, buf, 1, MEM_WRITE, &d);",
 T*2 + "tf_def = arm_asserts;",
 T*2 + "altctl_free(&d);",
 T + "}",
 "",
 T + "/*  ROW D -- THE LEVEL IS HELD, WHICH IS THE DUAL OF LEG 3.  Leg 3 pins",
 T + "    RETRACTION: a STATUS read lowers the line.  *** NOTHING PINNED THAT",
 T + "    THE REQUEST SURVIVES UNTIL THAT READ, so an EDGE assert satisfies leg",
 T + "    3 exactly. ***  Two measured escapes lived in that gap: asserting the",
 T + "    macro directly instead of setting the field, and a tick that clears",
 T + "    int_assert after asserting.  Both make the interrupt an edge.",
 "",
 T + "    int_assert is a LEVEL: the tick re-raises it every tick until the",
 T + "    STATUS read.  So: one command, then TWO ticks with NO read between,",
 T + "    and the sink must count both.  */",
 T + "altctl_fresh(&d);",
 T + "if (d.inbuf != NULL) {",
 T*2 + "stub_disk_exists = 1;",
 T*2 + "d.irq.interrupt_assert = arm_sink;",
 T*2 + "d.irq.interrupt_deassert = cmpl_desink;",
 T*2 + "arm_asserts = 0;",
 T*2 + "buf[0] = 0xaa;",
 T*2 + "dev_wdc_access(fake_cpu(), NULL, wd_command, buf, 1, MEM_WRITE, &d);",
 T*2 + "dev_wdc_tick(fake_cpu(), &d);",
 T*2 + "held = arm_asserts;\t\t/*  the store's own tick, plus one more  */",
 T*2 + "altctl_free(&d);",
 T + "}",
 "",
 T + "/*  ROW E -- THE ABRT BIT, ON THE FIRST COMMAND, AT BOTH ARMS.  *** LEG 1",
 T + "    COUNTS ABRT ONLY AMONG OPCODES THAT STAYED SILENT, so the moment the",
 T + "    fix makes them assert, the ABRT half of the very same two-statement",
 T + "    pair goes UNPINNED. ***  Deleting `d->error |= WDCE_ABRT;` from",
 T + "    either arm escaped every leg, measured.  The fix added a statement",
 T + "    beside an existing one and the detector stopped watching the one it",
 T + "    did not add.  */",
 T + "altctl_fresh(&d);",
 T + "if (d.inbuf != NULL) {",
 T*2 + "stub_disk_exists = 1;",
 T*2 + "d.irq.interrupt_assert = arm_sink;",
 T*2 + "d.irq.interrupt_deassert = cmpl_desink;",
 T*2 + "buf[0] = WDCC_SEC_FREEZE_LOCK;",
 T*2 + "dev_wdc_access(fake_cpu(), NULL, wd_command, buf, 1, MEM_WRITE, &d);",
 T*2 + "abrt_sec = (d.error & WDCE_ABRT) ? 1 : 0;",
 T*2 + "altctl_free(&d);",
 T + "}",
 T + "altctl_fresh(&d);",
 T + "if (d.inbuf != NULL) {",
 T*2 + "stub_disk_exists = 1;",
 T*2 + "d.irq.interrupt_assert = arm_sink;",
 T*2 + "d.irq.interrupt_deassert = cmpl_desink;",
 T*2 + "buf[0] = 0xaa;",
 T*2 + "dev_wdc_access(fake_cpu(), NULL, wd_command, buf, 1, MEM_WRITE, &d);",
 T*2 + "abrt_def = (d.error & WDCE_ABRT) ? 1 : 0;",
 T*2 + "altctl_free(&d);",
 T + "}",
 T + "stub_disk_exists = 0;",
 "",
 T + "rows ++;",
])
s = s.replace(ANCHOR, NEW + NL, 1)

s = s.replace('" | 2nd %i secarm %i | retract de=%i f=%i re=%i | sf irq=%i abrt=%i' + chr(92) + 'n",',
              '" | 2nd %i secarm %i | retract de=%i f=%i re=%i | sf irq=%i abrt=%i"' + NL +
              T + '    " | taskfile %i/%i held %i abrt %i/%i' + chr(92) + 'n",', 1)
s = s.replace("	    second, second_sec, retract_de, retract_field, retract_re,\n	    sf_irq, sf_abrt);",
              "	    second, second_sec, retract_de, retract_field, retract_re,\n"
              "	    sf_irq, sf_abrt, tf_sec, tf_def, held, abrt_sec, abrt_def);", 1)
s = s.replace("	    retract_re != 0 || sf_irq != 1 || sf_abrt != 0) {",
              "	    retract_re != 0 || sf_irq != 1 || sf_abrt != 0 ||\n"
              "	    tf_sec != 1 || tf_def != 1 || held != 2 ||\n"
              "	    abrt_sec != 1 || abrt_def != 1) {", 1)

io.open(P, "w", encoding="utf-8", newline="").write(s)
print("  three legs added: task-file (F), level-held (D), ABRT-both-arms (E)")
