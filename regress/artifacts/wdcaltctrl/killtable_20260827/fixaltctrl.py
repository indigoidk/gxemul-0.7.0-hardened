"""The ALT-CTRL fix: A1 (the bit) + B4 (level, no edge) + C1 (#479's helper).

Every choice below was settled by a MEASUREMENT a panel seat made, not by argument.

  A1  WDCTL_4BIT (0x08) -> WDCTL_RST (0x04).
      A2 (leave it) is refuted by five red reproduction rows.
      A3 (trigger on either bit) is MEASURED DEAD: it is identical to today on the
      only two scenarios that are wrong, so the "compatibility hedge" hedges nothing.

  B4  LEVEL-TRIGGERED on the corrected bit -- NO prev_ctl, and this is the choice the
      two flagship seats split on.  The opus seat argued B1 (assert edge); the fable
      seat MEASURED that dropping the edge escapes every row AND produces a
      byte-identical scenario differential.  A measured delta of ZERO means prev_ctl
      has no warrant under the ADDITION LICENCE -- and the `mec` prev_asserted idiom
      the design was going to borrow from exists to suppress spurious INTERRUPT
      re-assertion, which has no analogue here.
      *** AND ADDING IT WOULD COST SOMETHING: the same seat built `m7`, a prev_ctl
      update mis-scoped inside the if, which escapes every row and makes EVERY
      SUBSEQUENT SRST be ignored.  B4 makes that failure impossible by construction. ***

  C1  call wdc_new_command_reset() rather than a second helper.  The forward
      declaration a seat's control mutant tripped over was MEASURED to be one line
      that builds clean, so it is not a design constraint.  A second reset helper
      would diverge from the one wdc_command() uses, and #479 already reasoned out
      what belongs in it -- including which latches must NOT be cleared.

NOT DONE, and filed with its measurement rather than folded in:
  * the POWER-ON signature (`wdcponsig`).  Fable's scenario matrix shows power-on is
    dark BOTH pre- and post-fix, so this fix does not regress it -- it is a
    pre-existing gap in a different semantic class, and the offline differential
    cannot even witness it because its rows memset a struct and never run DEVINIT.
    Folding it in would need a new oracle, which the round-scope rule forbids.
  * clearing `error` and releasing the interrupt on reset.  A transferred warrant
    exists (dev_asc_reset's #266 clause) but nothing in this round measures it, and
    the fable seat measured a fixture trap behind it: interrupt.h calls through the
    deassert pointer unconditionally, so every row that writes ctl would have to wire
    it or the harness segfaults in a way that reads as a detector defect.
"""
import io

NL, T = chr(10), chr(9)
P = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\src\devices\dev_wdc.c"
s = io.open(P, encoding="utf-8", newline="").read()

#  ---- the forward declaration, immediately above the ALT-CTRL handler ----------
DECL_AT = "DEVICE_ACCESS(wdc_altstatus)" + NL
assert s.count(DECL_AT) == 1, "handler anchor %d" % s.count(DECL_AT)
FWD = ("/*  #481: forward-declared so the ALT-CTRL arm below can call it.  A panel seat's" + NL +
       "    control mutant failed to compile for want of exactly this line and the failure" + NL +
       "    was briefly read as a design constraint against calling the shared helper; it" + NL +
       "    is one line and it builds clean.  */" + NL +
       "static void wdc_new_command_reset(struct wdc_data *d);" + NL + NL +
       DECL_AT)
s = s.replace(DECL_AT, FWD, 1)

#  ---- the handler itself -------------------------------------------------------
OLD = (T*2 + "if (idata & WDCTL_4BIT)" + NL +
       T*3 + "d->cur_command = COMMAND_RESET;" + NL)
assert s.count(OLD) == 1, "arm anchor %d" % s.count(OLD)

NEW = (T*2 + "/*  #481: THE RESET BIT IS WDCTL_RST (0x04), NOT WDCTL_4BIT (0x08)." + NL +
 T*2 + "" + NL +
 T*2 + "    WDCTL_4BIT is \"use four head bits (wd1003)\", a head-addressing" + NL +
 T*2 + "    mode selector that Linux libata holds as its STEADY-STATE ap->ctl." + NL +
 T*2 + "    Testing it here meant three measured defects at once:" + NL +
 T*2 + "" + NL +
 T*2 + "      * a real soft reset was MISSED.  Older OpenBSD asserts with 0x06," + NL +
 T*2 + "        which has bit 3 CLEAR -- measured `cur_command 0x0`." + NL +
 T*2 + "      * a ROUTINE control write DESTROYED THE RECORD OF WHICH COMMAND IS" + NL +
 T*2 + "        EXECUTING -- measured `0xec -> 0x100`.  cur_command is also the" + NL +
 T*2 + "        value assigned into write_in_progress, so this is only harmless" + NL +
 T*2 + "        because wdc__write() has exactly ONE caller, immediately after" + NL +
 T*2 + "        the assignment.  An accident, not an invariant." + NL +
 T*2 + "      * an nIEN write latched a reset.  0x0a is libata's polled-mode" + NL +
 T*2 + "        staple -- measured `0x0a->0x100`." + NL +
 T*2 + "" + NL +
 T*2 + "    COMMAND_RESET IS NOT A RESET ACTION.  It is read at exactly two" + NL +
 T*2 + "    sites, both making the cylinder registers return the ATAPI signature" + NL +
 T*2 + "    0xEB14 for a CD-ROM.  It is the SIGNATURE LATCH -- which is why the" + NL +
 T*2 + "    wrong bit went unnoticed: triggering on libata's steady state kept" + NL +
 T*2 + "    the signature on almost always." + NL +
 T*2 + "" + NL +
 T*2 + "    LEVEL-TRIGGERED, DELIBERATELY, AND THE EDGE WAS DECLINED ON A" + NL +
 T*2 + "    MEASUREMENT.  A seat built the edge-dropped mutant and it escaped" + NL +
 T*2 + "    every row with a BYTE-IDENTICAL scenario differential: edge and" + NL +
 T*2 + "    level are indistinguishable here, because the abort is idempotent" + NL +
 T*2 + "    and no protocol-following driver issues commands while holding" + NL +
 T*2 + "    SRST.  A measured delta of zero is not a licence to add state --" + NL +
 T*2 + "    and a prev_ctl update mis-scoped by one brace makes every LATER" + NL +
 T*2 + "    reset be ignored, a failure this form cannot have." + NL +
 T*2 + "" + NL +
 T*2 + "    THE ABORT IS #479's HELPER, not a second one: a channel reset and a" + NL +
 T*2 + "    new command must not disagree about what gets cleared, and #479" + NL +
 T*2 + "    already reasoned out which latches must SURVIVE (see its comment --" + NL +
 T*2 + "    clearing warned_* would undo #337 and #464).  */" + NL +
 T*2 + "if (idata & WDCTL_RST) {" + NL +
 T*3 + "d->cur_command = COMMAND_RESET;" + NL +
 T*3 + "wdc_new_command_reset(d);" + NL +
 T*2 + "}" + NL)

io.open(P, "w", encoding="utf-8", newline="").write(s.replace(OLD, NEW, 1))
print("  dev_wdc.c: A1 + B4 + C1 applied")
