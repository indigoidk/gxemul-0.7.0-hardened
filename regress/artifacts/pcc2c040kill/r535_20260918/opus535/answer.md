OPUS_SEAT_ALIVE_20260918_535
VERDICT: DO NOT RATIFY (as-is) -- one L2 in the same class the round repairs (latch x MIEN, 17/17 escape), fix is one free row; wiring (Q2) correct.

Q1 MEASURED. Scratch clone /tmp/gxopus535 (cp -a build/, dev_pcc2.c = git show HEAD, rm src/cpus/*.o, FRESH=OK each build, .MUTANT cleared after cmp vs HEAD + fresh rebuild). Probe = frozen copy of the working-tree pcc2_c040_probe.py (md5 6b8cd318...). Every .raw ends PCC2C040_DONE.

 BASE                      17/17   DIAG announce count td(0x06x1)=1  x2(0x06x2)=1
 A latch bypassed if MIEN  17/17   DIAG td=7  x2=8        <- ESCAPE, L2
   if ((GENCTL & MIEN) || !(warned & C040bit))
 F latch SET only if !MIEN 17/17   DIAG td=7  x2=8        <- ESCAPE, same cell
 C fatal( -> debug(        17/17                          <- ESCAPE (channel)
 D latch bit C040 -> MASK_LEN (both lines) 17/17          <- ESCAPE (collision)
 E && pending_timer2==0    17/17                          <- ESCAPE, clause (e)

A/F: the round opened the MIEN axis for announce PRESENCE (`c040 says mien`) and left the latch cell (MIEN set, warned=1) empty: the announce fires 7-8 times per session and no row counts it. Same class twice running (agy late seat: presence x MIEN; here: count x MIEN) -> repair-chain class closure owed: {MIEN} x {warned} for the announce. Free repair, no new session:
   row("c040 once mien", "%d" % td.count(SAYS), "1", ...)
Caution: `t2`/`t3` are REBOUND to the x2/rec assert_row transcripts later in the file; use `td` (7 vs 1 alone discriminates) or rename.
C: every C040 write in the probe is STEPPED, and debug() prints under single-step, so a verbosity downgrade of the announce is invisible. Real effect: silent under free-running/-q. Needs a free-running C040 write; disclose in the contract and FILE.
D: `c040 predirty` pins only PCC2_W_GENCTL_LEN; its note says "a DIFFERENT warned bit" -- generic claim, one bit rowed. Tighten the note (L4) and disclose; enum makes duplicate IDs impossible, a name swap is not.
E: body never tests pending counts -> clause (e) disclosure.

Q2: correct. Keyed on $C040LOG, 17 names, pins 17/17/0, sentinel checked; "c040 says" vs "c040 says mien" and "c040 noassert" vs "noassert2" cannot cross-match under the two-space pattern; longest name 15.
Q3: acceptable because the correction immediately follows and holds the closing position; the "14/16" should name its log (ctlq_20260909/repaired_M_d1_noassert.raw exists).
Q4: add the count row; disclose C/D/E in the header contract.

## r2 (coordinator follow-up): the 18-row probe with `c040 once mien`, frozen copy probe.r2.py md5 80d49ce2...
 r2_BASE.raw  PCC2C040_RESULT=18/18  PASS  ends PCC2C040_DONE
 r2_A.raw     PCC2C040_RESULT=17/18  red: c040 once mien got 7 want 1  ends PCC2C040_DONE
 r2_F.raw     PCC2C040_RESULT=17/18  red: c040 once mien got 7 want 1  ends PCC2C040_DONE
Clone restored to HEAD dev_pcc2.c, rebuilt fresh, sentinel CLEARED. The L2 (A/F) is closed; C, D and E are unchanged (disclose them).
