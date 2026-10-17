#!/usr/bin/env python3
"""m88kexcdeliver -- rung-3 witness AND detector: does the m88k exception core DELIVER a trap-like
exception (vector entry reached, shadow registers right, machine still running), or stop the machine?

`cpu_m88k.c`'s exception switch marks only RESET / INTERRUPT / INSTRUCTION_ACCESS / DATA_ACCESS
`implemented`; every other vector below M88K_EXCEPTION_USER_TRAPS_START falls to a fallback that
prints `unimplemented vector=0x%03x` and sets `running = false` on EVERY guest CPU.  The vector-
specific tail switch then has a `default:` that stops THIS cpu with `internal error` -- so a fix
needs BOTH `implemented = true` AND a tail arm (the naive one-site fix was MEASURED to halt, pass 1).
Real hardware delivers VBR + 8*vector (MC88100 UM Table 6-1, mc88100.txt:8524-8538) and the guest OS
turns it into a signal; rte resumes at SNIP (:8983-8985), the destination register is unchanged
(6.6 :9305-9308; 6.8.3 :10300-10305).

Cold-debugger probe on the COMMITTED `testm88k` machine (no machine or device edits).  Per row: a
guest program at 0x10000 planted with `put w` (liveness marker `addu r9,r0,r10` first), registers
seeded with `rN=`, a `br .` (c0000000) planted at every vector entry so a delivered exception spins
rather than executing zeros, `breakpoint add <8*vector>`, `continue`, then `reg` and `reg 0,0`.

  row        program (after the marker at 0x10000)                 raise                     entry
  div0       divu r2,r3,r0            f4436800                    ILLEGAL_INTEGER_DIVIDE 8  0x40
  ovf        add  r2,r3,r4 (7fffffff+1) f4437004                  INTEGER_OVERFLOW 9        0x48
  misalign   ld   r2,r3,0 (r3 odd)    14430000 (major opcode 5)   MISALIGNED_ACCESS 4       0x20
  bounds     tb1  0,r3,7 (r3=1)       f003d807  supervisor trap   BOUNDS_CHECK 7            0x38
  priv       stcr r3,cr1 (r3=0x2: MODE clear) 80038023; ldcr r2,cr1 80404020   PRIVILEGE 6  0x30
  privtb     stcr r3,cr1; tb1 0,r4,8 (f004d808) in user mode      PRIVILEGE 6               0x30
  unimpl     stcr r3,cr1; prom_call f400fc92 in user mode         UNIMPLEMENTED_OPCODE 5    0x28
  error      div0 whose handler at 0x40 is a misaligned ld: the 2nd fault with SFRZ set re-routes
             to ERROR 10                                                                    0x50
  dslot      br.n +16 (c4000004) with divu r2,r3,r0 in its delay slot -> the else-arm of the
             delay-slot branch (SNIP = pc+4 = 0x1000c, SFIP = delay_target = 0x10014 -- two
             DIFFERENT numbers; with br.n +8 both were 0x1000e and the SFIP channel was vacuous)  ILLEGAL_INTEGER_DIVIDE 0x40
             *** THIS ROW PINS THE ELSE-ARM AS IMPLEMENTED, NOT AS THE MANUAL'S CONTRACT.  Table 6-3 (the shadows copy
             XIP/NIP/FIP) with the pointer definitions at UM 6.2 (mc88100.txt:2093-2104: FIP is the taken branch's
             target while the branch executes, so for a fault in its delay slot NIP = target, FIP = target+4) and X(rte)'s
             `fip != nip + 4' arm say the else-arm returns WRONG (codex, grok, pass 2: the fallthrough executes
             before the target).  Pre-existing, out of this diff's scope, filed as m88kdslotshadow; when that round
             lands this row is RE-PINNED FIRST (oracle-correction rule: re-pin, measure HEAD red, then fix). ***
  dslotmisalign/dslotunimpl/dslotpriv/dslotovf   v20 (repair 13, 2026-10-16): the same br.n +16 with the fault IN ITS
             DELAY SLOT at the four other arms a guest INSTRUCTION can raise -- ld r2,r3,0 (r3 odd), prom_call and
             ldcr r2,cr1 after stcr r3,cr1 (user mode), add 7fffffff+1.  `implemented = !cpu->delay_slot' at each of those
             arms swept v19 59/59 (artifacts/m88kexcdeliver/delayslot_20261016/, predicted by Fable 5.1); each row
             kills its own arm's form.  Scored like dslot (the else-arm, AS IMPLEMENTED): SNIP = fault+4,
             SFIP = fault+12 = the branch's delay_target                                       0x20/0x28/0x30/0x48
  errortb    tb1  0,r3,10 (r3=1)      f003d80a  supervisor trap naming ERROR (10) directly -- the
             only route to switch 1's ERROR arm (the double-fault route enters at the re-route AFTER
             switch 1, so it cannot see that arm: M_ERRORDROP escaped the error row 9/9, table 1)  0x50
  misaligntb/unimpltb/div0tb/ovftb   tb1 0,r3,{4,5,8,9} (f003d804/05/08/09), supervisor: the TRAP
             ROUTE into switch 1 for the four classes whose other rows arrive by instruction --
             `if (!is_trap) implemented = true' escapes those rows (grok, deepseek, pass 2)  0x20/0x28/0x40/0x48
  vbrtb      stcr r5,cr7 (800580e5, r5=0x2000) then tb1 0,r3,7: the vector table RELOCATED -> entry
             0x2038, not 0x38.  Every other row runs with VBR == 0, so `pc = 8*vector' (VBR dropped)
             was a 10/10 escape (Opus, pass 2).  The one ANCHORED row: it alone reds if the table moves.  0x2038
  trapfrozen div0 whose handler at 0x40 is tb1 0,r3,7 (r3=0x11): a TRAP with SFRZ already set is NOT
             re-routed to ERROR (UM :8633-8636, 6.10 :10613-10614) -- it delivers to 0x38 with the
             shadows still frozen.  `if (!is_trap)' -> `if (true)' was a 10/10 escape (Opus, pass 2)  0x38
  trapfrozen4/5/6/9   the same shape naming 4, 5, 6, 9: the {SFRZ set, is_trap} x {class} closure -- with only class 7 rowed,
             `if (!is_trap || vector == <class>)' re-routed that one frozen trap to ERROR unseen (codex, pass 5)  0x20/0x28/0x30/0x48
  trapfrozen8 first fault add 7fffffff+1 (handler planted at 0x48), handler tb1 0,r3,8: the frozen trap naming DIV0
             delivers to 0x40 -- observable only because the handler is NOT at 0x40 for this row.                     0x40
  trapfrozen10 the same shape naming 10: for the RE-ROUTE mutant it is equivalent (0x50 either way), but switch 1's ERROR
             arm is a separate predicate -- a frozen trap naming 10 enters switch 1 AS ERROR, which no other row does
             (the err* rows enter under their own classes and become ERROR after the fallback); `implemented =
             !(PSR & SFRZ)' there sends it to the fallback -- M_ERRORFRZOFF (codex, pass 6).  Expect 0x50, shadows frozen 0x50
  privsuptb  tb1 0,r3,6 (f003d806) in SUPERVISOR mode: the trap route into PRIVILEGE_VIOLATION.  privtb is
             NOT that route -- the user-mode filter in X(tb0) raises PRIVILEGE with is_trap == 0, so
             `implemented = !is_trap' on the PRIVILEGE arm left priv AND privtb green (codex, glm: pass 2)  0x30
  usertb     tb1 0,r3,128 (f003d880): the first USER trap vector, delivered by the pre-existing code to
             0x400.  Pins the tail switch's `< USER_TRAPS_START' guard: `<=' sends 128 into the tail
             default and stops the cpu (codex's one-character escape, pass 2)                       0x400
  resid50    tb1 0,r3,50 (f003d832): a residual vector.  EXPECTED RESULT = HALT (the fallback, by design).
  resid127   tb1 0,r3,127 (f003d87f): the LAST residual vector -- pins the fallback window's FAR bound (`vector < 128').
             The interior pins were resid50 (50) and sfu1h (114: its nested SFU1 halts at the fallback), so a shrink of the
             bound to any N in (114, 128) escaped BY CONSTRUCTION (measured: `< 127' 29/29 on v5, `< 51' 28/29 -- sfu1h saw
             that one), and usertb (128, just outside) pins only that 128 is not halted: the accept-row-at-the-LAST-slot
             rule (deepseek and glm, pass 5, from the packet alone; glm's [115,128] named it -- the shrink VALUES are
             115..127, 128 being the bound itself: deepseek, pass 6).  EXPECTED RESULT = HALT
             naming 0x07f; a shrunk bound delivers 127 to 0x3f8
             and the tail default stops the cpu instead (TAILHALT) -- mutants M_FALLBACK127, M_FALLBACK51.
  resid11    tb1 0,r3,11 (f003d80b): the FIRST residual vector (M88K_EXCEPTION_NMI in cpu_m88k.h, unimplemented in switch 1 --
             grok, pass 7) -- the fallback window's NEAR bound.  `vector >= 12 &&' on the
             fallback swept 36/36 because no row named 11..49 (kimi, pass 6).  EXPECTED RESULT = HALT naming 0x00b        (0x58)
  resid50ind stcr r5,cr1 (r5=0x80000000: IND CLEAR) then tb1 0,r3,50: the fallback with IND clear -- `&& (PSR & IND)' on the
             fallback swept 36/36 because every fallback row had IND set.  EXPECTED RESULT = HALT naming 0x032          (0x190)
  resid50c   stcr r5,cr1 (r5=0x90000002: C SET) then tb1 0,r3,50: the fallback with C set -- `&& !(PSR & C)' swept likewise.
             With usfu1 (MODE clear, SFD1 set), sfu1h (SFRZ set) and resid50ser (SER set) these give every settable PSR
             bit both sides at the fallback -- SIX bits, not five.  *** THIS SENTENCE WAS FALSE FROM v16 UNTIL v17 and
             said `every settable bit' the whole time: it was written when SER was believed 88110-only, and when the
             MC88100 manual settled that it is software-settable the claim silently became an overclaim with no row
             behind it.  minimax asked on pass 10 whether the blurb matched its rows; it did not, and resid50ser is what
             makes it true.  A claim that enumerates its evidence stays checkable when the world changes underneath it;
             one that says `every' does not. ***  MXM and BO cannot be set by stcr without stopping the cpu -- disclosed.
             EXPECTED RESULT = HALT    (0x190)
  trapfrozen450 / trapfrozen496  the same shape naming 0x1c2 (the OpenBSD >= 5.3 syscall vector) and MVMEPROM_VECTOR: the LAST
             two switch-1 labels.  Switch 1 has TEN deliverable labels -- 4..10, 128, 450, 496 -- and the frozen-trap rows now
             cover all ten; `!is_trap || vector == 0x1c2' swept 41/41 before these (codex, pass 7)                  0xe10 / 0xf80
  trapfrozen511 the same shape naming 511, the LAST nameable trap vector (tb1's field is 9 bits): trapfrozen128 pinned only the
             near edge of the user range -- `!is_trap || vector >= 129' swept (kimi, pass 7; the last-slot rule again)          0xff8
  trapfrozen128 div0 whose handler is tb1 0,r3,128: a frozen USER trap is exempted from the re-route like any trap and
             delivered to 0x400 with frozen shadows -- `!is_trap || vector >= 128' swept 36/36 (kimi, pass 6)              0x400
  usfu1      stcr r5,cr1 (r5=0x0000000a: USER mode, SFD1 set) then a LEGAL divu r6,r5,r4: SFU1 (114) raised from USER
             mode reaches the fallback -- the only user-mode route to it (a user tb1 naming < 128 raises PRIVILEGE).
             Every other fallback row is supervisor, so `&& (PSR & MODE)' on the fallback predicate swept 29/29 (kimi,
             pass 5, MEASURED).  EXPECTED RESULT = HALT naming 0x072; the mutant delivers to 0x390 and the #if 0'd SFU1
             tail arm makes that TAILHALT -- mutant M_FBSUPONLY                                                (0x390)
             Negative control: the shipped form must NOT deliver it (rejected D4 would)             (0x190)
  sfu1h      div0 whose handler at 0x40 is a LEGAL divu r6,r5,r4: with SFD1 set the divide raises
             SFU1_PRECISE (114), which halts at the FALLBACK (it runs before the SFRZ re-route).  EXPECTED
             RESULT = HALT naming vector 0x072, with pc == 0x40 (the first delivery happened -- on HEAD the
             first divu halts on vector 0x008, not this row's 0x072, and it reads STOP).  With the fallback off (M_DELIVERALL) the
             nested SFU1 is RE-ROUTED TO ERROR (0x50), not delivered to 0x390: the row reds as STOP.  So it
             pins 'SFU1 inside a handler still halts', NOT 'SFU1 is not delivered to its vector' -- the
             first-exception SFU1 route is row m88kexcsfu1's (grok, kimi, pass 3)                    (0x390)
  udiv0      stcr r3,cr1 (r3=0x2: user mode) then divu r2,r3,r0: the fallback comment's own sentence,
             'one user-mode divu by zero ended the emulation', measured literally; also pins that user mode
             with SFD1 CLEAR yields vector 8, not SFU1 (the m88kexcsfu1 boundary)              ILLEGAL_INTEGER_DIVIDE 0x40
  indclr     stcr r5,cr1 (r5=0x80000000: MODE only, IND CLEAR) then add 7fffffff+1: the exception path must
             SET IND (PSR 0x8000000b from 0x80000000; EPSR 0x80000000).  Every other row's pre-fault PSR already
             has IND, so `| M88K_PSR_IND' was unobservable -- the carry shape again (grok, codex, pass 3)     0x48
  umisalign  stcr r5,cr1 (r5=0x2: user mode) then ld r2,r3,0 with r3 odd: MISALIGNED from USER mode
             (a MODE-conditioned `implemented' on that arm swept 23/23 -- Opus, pass 4)                    0x20
  uovf       stcr r5,cr1 (user mode) then add 7fffffff+1: OVERFLOW from USER mode -- the measured
             M_OVFSUPONLY escape (a user-mode overflow ended the emulation again, 23/23)               0x48
  errovf     div0 whose handler at 0x40 is add 7fffffff+1: a NON-TRAP fault of a SECOND class with
             SFRZ set -> re-routed to ERROR with frozen shadows (M_SFRZMIS -- `!is_trap && vector ==
             MISALIGNED' on the re-route -- swept 23/23 because `error' was that cell's only row)      0x50
  errind     div0 whose handler is stcr r4,cr1 (r4=0x80000009: SFRZ kept, IND CLEAR) then the odd ld: the re-route with
             interrupts enabled -- every SFRZ-set row had reached it with IND set, so `(PSR & SFRZ) && (PSR & IND)'
             swept (grok, pass 7).  Expect ERROR at 0x50, frozen shadows, the diagnostic present                     0x50
  errc       the same with r4=0x9000000b (C SET): `&& !(PSR & C)' on the re-route swept likewise; expects PSR 0x9000000b after
             delivery (C survives exception entry -- the row first shipped wanting 0x8000000b and BASE caught it).  MODE (errpriv) and SFD1
             (errdiv0) already vary at the re-route; MXM/BO cannot be set by stcr without stopping the cpu; SER is varied by trapfrozenser 0x50
  errdiv0    div0 whose handler is stcr r5,cr1 (r5=0x80000003: SFD1 CLEAR, SFRZ kept) then divu by zero:
             a frozen non-trap DIV0 -> ERROR (with SFD1 set the same divu raises SFU1 instead: sfu1h)     0x50
  errpriv    div0 whose handler is stcr r5,cr1 (r5=0x00000003: USER mode, SFRZ kept) then ldcr: a frozen
             non-trap PRIVILEGE -> ERROR (Fable, pass 4: the {SFRZ, !is_trap} x {class} closure)        0x50
  errunimpl  div0 whose handler is stcr r5,cr1 (user mode, SFRZ kept) then prom_call: a frozen non-trap
             UNIMPLEMENTED -> ERROR.  BOUNDS and ERROR have no non-trap route (trapfrozen covers the trap)  0x50
  ovfc       stcr r5,cr1 (80058025, r5=0x90000002: C set) then add 7fffffff+1: the carry bit must
             SURVIVE the exception path (UM 6.6) -> PSR 0x9000000b, EPSR 0x90000002.  Every other
             row's pre-fault C is 0, so PSR == 0x8000000b pinned 'C not set', never 'C unchanged'  0x48
  live       divu r2,r3,r4  (r3=0x60, r4=0x10) -> r2 = 6           none      LIVENESS control
  attrib     divu r2,r3,r4  (r3=0x10, r4=0x10) -> r2 = 1           none      ATTRIBUTION control
  selftest   no program: `reg 0,0` at reset must parse PSR == 0x80000002 (the CR parse works)

RESULT per fault row (the classifier tests the STOP channel before pc, deliberately: the naive fix
sets pc = entry and THEN stops, so pc alone cannot tell it from delivery):
  HALT       `unimplemented vector=` printed AND the machine stopped (both observed, pass 3); an
             expected-HALT row (resid50, resid127, sfu1h, usfu1) must also see ITS vector named in the diagnostic
  TAILHALT   `internal error` printed and the machine stopped (the naive fix's shape)
  STOP       the machine stopped for another reason (e.g. a wrong vector base landed in zeros)
  BADREGS    the entry breakpoint fired but a shadow-register/PSR/destination assert failed, or (bad=refatal) the re-route's
             `[ SFRZ already set in PSR => ERROR ]' line was present on a frozen-TRAP row or absent on a re-routed err* row --
             the channel that separates the exemption arm from the re-route arm when both deliver to 0x50 (kimi, pass 6), or
             (bad=level) the transcript carried an `exception <CLASS>' line: the class printed at ERROR
             level, which the fork's default WARNING verbosity shows and INFO does not (kills M_LEVEL)
  (rows resid50, resid127, sfu1h and usfu1 EXPECT HALT: the fallback stopping the machine is the correct answer there)
  DELIVER    entry breakpoint fired, machine running, and every assert holds:
             pc == entry, SXIP == fault_pc|V, SNIP, SFIP, PSR == 0x8000000b (SFRZ|IND|SFD1|MODE),
             EPSR == the pre-fault PSR (0x80000002 supervisor rows; 0x00000002 user-mode rows),
             r2 unchanged (0xdeadbeef)
  NOSTART    the liveness marker never ran
Controls print DONE (r2 == the expected quotient, machine running) or a failure word.

Output: one `M88KEXC_ROW=<name> RESULT=<word> ...` line per row, `M88KEXC_RESULT=<delivered>/<fault rows>`,
`M88KEXC_SELFTEST=OK|FAIL`, `M88KEXC_DONE`.  Set M88KEXC_VERBOSE=1 for transcripts.

CONTRACT (clause e): catches a class returned to the fallback (HALT) by either route (instruction rows
and the *tb trap rows); a SHRUNK fallback window (resid127 pins the far bound: `< 128' -> `< 127' or `< 51' both deliver 127 to the
tail default, TAILHALT; usertb pins that 128 is outside it, resid50 the interior); a class reaching the tail default (TAILHALT); a wrong vector SCALING (M_VEC4,
M_VEC7: STOP) and a DROPPED vector base (vbrtb: STOP); a stale SXIP/SNIP/SFIP; a wrong PSR, including a
cleared carry (ovfc); a dropped IND (indclr); the debugmsg LEVEL regression to ERROR/WARNING (bad=level on any
delivered row: those print at the post-startup WARNING floor, INFO and DEBUG do not -- so exact INFO is NOT pinned,
only 'not ERROR/WARNING' -- M_LEVEL; codex, pass 3); a skipped EPSR save; a skipped supervisor switch (the user-mode rows: EPSR MODE
clear vs PSR MODE set); a MODE-conditioned `implemented' on any class that user mode can raise ({class} x
{MODE} closure: DIV0 udiv0, PRIVILEGE priv/privtb, UNIMPLEMENTED unimpl, MISALIGNED umisalign, OVERFLOW uovf;
BOUNDS and ERROR have no user-mode route -- a user tb1 naming them raises PRIVILEGE, and every handler runs
supervisor; the FALLBACK predicate itself is pinned in user mode by usfu1, the one user-mode route to it); a class-conditioned SFRZ re-route, its diagnostic pinned both ways by the refatal channel, and a PSR-bit conjunct on the re-route (the
predicate reads PSR: every stcr-settable 88100 bit now varies there -- MODE errpriv, SFD1 errdiv0, IND errind, C errc; MXM/BO cannot be
set by stcr without stopping the cpu, and SER is NOT an 88110-only bit -- mc88100.txt, anchor `SER - Serial Mode', documents it
for the MC88100 as software-settable and m88k_stcr stores it verbatim, so trapfrozenser rows it.  *** AND THE CONFIGURATION CLAIM
THIS DOCSTRING USED TO MAKE WAS FALSE TWICE OVER: it said the 88110-only bits `are 88100 here', and this probe launches
`-E testm88k' with NO `-C', while machine_test.c's MACHINE_DEFAULT_CPU(testm88k) sets cpu_name to "88110".  Every table this
round has run measured an 88110.  The SCORES stand -- nothing in the m88k model reads cpu_type to change behaviour outside the
name and the PID register, so the exception path is shared -- but the CLAIM did not, and pinning `-C 88100' with a PID control
row is owed as its own revision with its own BASE run (codex, pass 8). ***) ({SFRZ set, !is_trap} x {class}: MISALIGNED error, OVERFLOW errovf,
DIV0 errdiv0 -- the handler clears SFD1 first, with it set the divu raises SFU1 instead (sfu1h) --, PRIVILEGE errpriv
and UNIMPLEMENTED errunimpl -- the handler drops to user mode keeping SFRZ; BOUNDS and ERROR have no non-trap route,
the frozen TRAP is trapfrozen); a wrong return address; the delay-slot else-arm's SFIP source (dslot, +16
geometry); a delay-slot-conditioned `implemented' on any class a guest INSTRUCTION can raise from a delay slot ({class} x
{delay slot} closure, v20: DIV0 dslot, MISALIGNED dslotmisalign, UNIMPLEMENTED dslotunimpl, PRIVILEGE dslotpriv, OVERFLOW
dslotovf -- `implemented = !cpu->delay_slot' at the four latter arms swept v19 59/59, delayslot_20261016/, and the body's own
`if (cpu->delay_slot)' is what makes delay_slot a floor axis; BOUNDS and ERROR x {delay slot} need a TRAP INSTRUCTION IN A
DELAY SLOT, which the MC88100 manual does not settle -- mc88100.txt:9433-9440 covers the slot OF a trap-taken instruction, not a
trap in one -- so they are DISCLOSED with their measured escapes, M_DSNOT_BOUNDS and M_DSNOT_ERROR, table 16, and so is
every trap instruction in a slot at the other five arms; multi-axis joints of delay slot with SFRZ, is_trap or a PSR bit stay
clause (e)); a trap re-routed to ERROR while frozen, per class ({SFRZ set, is_trap} x {every switch-1 label a trap can NAME -- 0..3 are deliverable too and are unrowed, disclosed as
m88kexchwtraps; the word EVERY overclaimed until v16}: trapfrozen (7),
trapfrozen4/5/6/8/9/10/128/450/496/511 -- the ten labels 4..10, 128, 0x1c2, MVMEPROM_VECTOR, enumerated from switch 1's `case' list, plus
the far edge of the user range (511) --
class 10's re-route exemption is told from the re-route by the refatal channel (the pass-6 packet called it equivalent; kimi refuted
that: the re-route prints a diagnostic the exemption does not) and switch 1's ERROR eligibility under SFRZ by trapfrozen10's
HALT/DELIVER; 0..3 are the hardware-event tails, m88kexchwtraps); the fallback window's NEAR bound (resid11) and the fallback predicate
conditioned on any settable PSR bit (resid50ind, resid50c, resid50ser, usfu1, sfu1h -- SIX bits, and resid50ser is
what made that claim true when SER turned out to be settable); a written destination.  Does NOT catch:
fcr2/fcr4/fcr5; scoreboard (SSBR) bits; DMT contents; the post-delivery
`cpu->delay_slot' write on the NON-delay path (M_DELAYALWAYS: needs a second UNFROZEN exception -- filed);
vectors 0..3's tail arms (no row: M_TAILOFF -- filed); vectors 11..113 and 116..127 (fallback halts by
design); SFU1 (114/115, row m88kexcsfu1); `implemented = is_trap' on BOUNDS/ERROR (EQUIVALENT today: no
instruction raises 7 or 10 -- becomes live when tbnd lands, row m88ktbnd); a PSR-bit conjunct on a switch-1 `implemented' arm
OTHER than MODE (closed for every class) and SFRZ at ERROR (both polarities: errortb unfrozen, trapfrozen10 frozen) -- the arms read no PSR
bit, so {arm} x {C, IND, SFD1} is clause-(e) debt, not floor; the representative (MISALIGNED with `!(PSR & C)', M_MISNOC) MEASURED
41/41 on v10 (the escape, as disclosed) and 45/46 on v14 -- KILLED by errc, whose second fault is MISALIGNED with C set (table 11).  So the
{MISALIGNED} x {C} and {MISALIGNED} x {IND} cells are rowed by errc / errind as a side effect of the re-route rows; the disclosure stands
for the remaining arms -- and that sentence was WRONG THREE WAYS until v16, all three measured (opus5, pass 8): it named
OVERFLOW, which ovfc and indclr already close, since both fault at that arm with C set and IND clear respectively; it
claimed {any arm} x {SFD1}, closed at all seven (at DIV0 architecturally -- X(divu) tests SFD1 BEFORE the divisor, so only
the tb1 route reaches that arm with SFD1 set); and it OMITTED BOUNDS and ERROR, which were open.  v16 closes
{UNIMPL, PRIV, BOUNDS, DIV0, ERROR} x {C, IND} with five rows and the re-route's trap side with three.  The DENOMINATOR is 7 arms x SIX settable bits (8 architectural
minus BO and MXM, which the store path refuses) = 42 cells, minus the 2 MODE-unreachable at BOUNDS/ERROR = 40 -- v16 said 35
and five bits, and grok corrected both on pass 9.  Those two ARE unreachable rather than merely unrowed: neither constant is
raised by any instruction, a user tb1 naming a vector below 128 raises PRIVILEGE with is_trap == 0, and the re-route writes
ERROR after switch 1 so it never enters that arm -- a warrant that EXPIRES when X(tbnd) lands (row m88ktbnd).  The re-route's TRAP side is closed on all five bits that can vary there
(MODE trapfrozenuser -- uniquely, per CTL_RRTRAPINV; SFD1 trapfrozensfd1 AND trapfrozenuser, which clears both bits;
IND trapfrozenind, C trapfrozenc, SER trapfrozenser; SFRZ is invariant BY CONSTRUCTION, since it is the guard) -- v17 closed three of those five and left MODE and SFD1, and pass 11 graded that
L2 rather than debt on two precedents from this round's own records.  What remains
disclosed: MULTI-AXIS joints of two or more PSR bits at one arm (clause (e) by the carrier's own bound), and vectors 0..3
(m88kexchwtraps).
"""
import os, pty, re, select, struct, sys, time

BIN = sys.argv[1] if len(sys.argv) > 1 else "/tmp/gxsec-build/gxemul"
CODE = 0x10000
DATA = 0x20000
XIP_V = 0x2
PSR_RESET = 0x80000002          # MODE | IND (cpu_m88k.c: cr[PSR] = M88K_PSR_MODE | M88K_PSR_IND)
PSR_EXC = 0x8000000b            # MODE | SFD1 | IND | SFRZ after the common path
PSR_USER = 0x00000002           # IND only: what the user-mode rows write via stcr
PSR_FRZSUP = 0x80000003         # MODE | IND | SFRZ, SFD1 CLEAR: a frozen handler that wants its divu to raise DIV0, not SFU1
PSR_FRZUSER = 0x00000003        # IND | SFRZ: a frozen handler dropping to user mode (PRIVILEGE / UNIMPLEMENTED routes).
                                # *** MODE **AND SFD1** ARE BOTH CLEAR HERE, and this comment said only MODE until v20.
                                # That omission cost a prediction: PRETABLE15 expected M_RRTRAPSFD1 to red trapfrozensfd1
                                # alone (58/59) and it measured 57/59, because trapfrozenuser -- which uses this value --
                                # presents SFD1 clear as well.  A constant's comment that lists SOME of the bits it clears
                                # reads like a complete decode and is not one.
PSR_USERSFD1 = 0x0000000a       # IND | SFD1, MODE CLEAR: user mode with the FPU disabled -- a legal divu raises SFU1 (kimi, pass 5)
PSR_FRZNOIND = 0x80000009       # MODE | SFD1 | SFRZ, IND CLEAR: a frozen handler that re-enables interrupts (grok, pass 7)
PSR_FRZC = 0x9000000b           # C | MODE | SFD1 | IND | SFRZ: a frozen handler with the carry bit set (grok, pass 7)
PSR_SUPCNOIND = 0xb0000000      # SER | MODE | C, IND CLEAR: supervisor, carry set, interrupts enabled, SERIAL MODE set.  ONE value
                                # closes the C, IND and SER cells at an arm together (grok, pass 9: v16 set only MODE|C here and closed
                                # SER at ONE arm, which is the cell-not-class error inside the repair for that error).  ONE value closes BOTH
                                # open cells at a switch-1 arm, because the open cells are always (C never set) and (IND never clear)
                                # -- opus5's census, pass 8.  The same trick ovfc and indclr already play at the OVERFLOW arm.
PSR_FRZSER = 0xa000000b         # SER | MODE | SFD1 | IND | SFRZ: a frozen handler with SERIAL MODE set.  SER is NOT an 88110-only bit:
PSR_SERSUP = 0xa0000002         # SER | MODE | IND: supervisor with serial mode set and nothing else unusual -- the pre-fault value for
                                # the fallback and non-trap rows that close SER at those two sites (grok, pass 9)
                                # mc88100.txt, anchor `SER - Serial Mode', says "This bit is set by software as appropriate", and
                                # m88k_stcr stores PSR verbatim after its BO / MXM / MODE checks.  The fork's vendored header comments
                                # it `/* 88110 serial mode */', which is upstream's error and which this probe's contract had copied
                                # (codex, pass 8; checked against the manual on disk rather than against the header).

def tri(sub, d, s1, s2):
    return 0xf4000000 | (d << 21) | (s1 << 16) | (sub << 8) | s2

MARK = tri(0x60, 9, 0, 10)                       # addu r9,r0,r10  -> r9 = 0x12345678 (liveness)
SELF = 0xc0000000                                # br . (disp 0)
DIVU_R2_R3_R0 = tri(0x68, 2, 3, 0)               # f4436800
DIVU_R2_R3_R4 = tri(0x68, 2, 3, 4)               # f4436804
DIVU_R6_R5_R4 = tri(0x68, 6, 5, 4)               # f4c56804 -- a LEGAL divide inside a handler: SFD1 is set there, so X(divu) raises
                                                 #   SFU1_PRECISE (114) before it looks at the divisor -> the fallback must still HALT
ADD_R2_R3_R4 = tri(0x70, 2, 3, 4)                # f4437004
LD_R2_R3_0 = 0x14000000 | (2 << 21) | (3 << 16)  # 14430000 (major opcode 5, ld)
TB1_0_R3_7 = 0xf003d807                          # tb1 0,r3,7   (computed vector 7, supervisor)
TB1_0_R4_8 = 0xf004d808                          # tb1 0,r4,8
TB1_0_R3_10 = 0xf003d80a
TB1_0_R3_4 = 0xf003d804                          # tb1 0,r3,4   -- a supervisor trap naming MISALIGNED_ACCESS (4) directly
TB1_0_R3_5 = 0xf003d805                          # tb1 0,r3,5   -- naming UNIMPLEMENTED_OPCODE (5)
TB1_0_R3_8 = 0xf003d808                          # tb1 0,r3,8   -- naming ILLEGAL_INTEGER_DIVIDE (8)
TB1_0_R3_9 = 0xf003d809                          # tb1 0,r3,9   -- naming INTEGER_OVERFLOW (9)
TB1_0_R3_6 = 0xf003d806                          # tb1 0,r3,6   -- naming PRIVILEGE_VIOLATION (6): the user-mode tb1 filter raises
                                                 #   PRIVILEGE with is_trap == 0 (cpu_m88k_instr.c X(tb0)), so privtb is NOT the trap route
TB1_0_R3_450 = 0xf003d9c2                        # tb1 0,r3,450 -- the 0x1c2 syscall vector (OpenBSD >= 5.3): a switch-1 label of its own
TB1_0_R3_496 = 0xf003d9f0                        # tb1 0,r3,496 -- MVMEPROM_VECTOR: likewise
TB1_0_R3_511 = 0xf003d9ff                        # tb1 0,r3,511 -- the LAST nameable trap vector (9-bit field): the far edge of the user-trap range
TB1_0_R3_128 = 0xf003d880                        # tb1 0,r3,128 -- the first USER trap vector: delivered by the pre-existing code (entry 0x400)
TB1_0_R3_50 = 0xf003d832                         # tb1 0,r3,50  -- a RESIDUAL vector (11..113): must still HALT (negative control vs D4)
TB1_0_R3_11 = 0xf003d80b                         # tb1 0,r3,11  -- the FIRST residual vector: the fallback window's NEAR bound (kimi, pass 6)
TB1_0_R3_127 = 0xf003d87f                        # tb1 0,r3,127 -- the LAST residual vector: pins the fallback window's FAR bound (< 128),
                                                 #   which resid50 (interior) and usertb (128, outside) cannot see (deepseek, glm, pass 5)
#  The four *tb rows are the TRAP ROUTE into switch 1 for the classes whose other rows arrive by INSTRUCTION
#  (is_trap == 0).  Pass-2 seats (grok, deepseek, independently) predicted `if (!is_trap) implemented = true;'
#  escapes the instruction rows for MISALIGNED/UNIMPL/DIV0/OVF; these rows are the ones that redden it (M_ISTRAP).
                         # tb1 0,r3,10  (a supervisor trap naming vector 10 = ERROR directly)
STCR_R3_CR1 = 0x80038023                         # stcr r3,cr1 (PSR)
STCR_R4_CR1 = 0x80048024                         # stcr r4,cr1 (PSR) -- for handlers whose r5 is the odd load address
STCR_R5_CR1 = 0x80058025                         # stcr r5,cr1 (PSR)  -- same format: 0x80000000 | S1<<16 | 0x8000 | CR<<5 | S1
STCR_R5_CR7 = 0x800580e5                         # stcr r5,cr7 (VBR)
PSR_CARRY = 0x90000002                           # MODE | C | IND: the ovfc row's pre-fault PSR (C = bit 28, UM 6.6 'carry bit unchanged')
PSR_INDCLR = 0x80000000                          # MODE only, IND CLEAR: the indclr row's pre-fault PSR -- every other row starts with IND
                                                 #   already set, so `| M88K_PSR_IND' in the exception-path PSR write was unobservable (grok, codex, pass 3)
VBR_TEST = 0x2000                                # the vbrtb row relocates the vector table here (OpenBSD relocates its own)
LDCR_R2_CR1 = 0x80404020                         # ldcr r2,cr1
PROM_CALL = 0xf400fc92                           # M88K_PROM_INSTR
BR_N_PLUS8 = 0xc4000002
BR_N_PLUS16 = 0xc4000004                         # br.n +16: delay_target (slot+8) != slot_pc+4, so SNIP and SFIP are DIFFERENT numbers                          # br.n +2 words

V_MISALIGN, V_UNIMPL, V_PRIV, V_BOUNDS, V_DIV0, V_OVF, V_ERROR = 4, 5, 6, 7, 8, 9, 10
V_SFU1 = 114
V_USER0 = 128
V_RESID = 50
V_RESID2 = 127
V_RESID0 = 11
V_SYSCALL = 450
V_MVMEPROM = 496
V_USERLAST = 511
VECTORS = (V_MISALIGN, V_UNIMPL, V_PRIV, V_BOUNDS, V_DIV0, V_OVF, V_ERROR, V_SFU1, V_USER0, V_RESID, V_RESID2, V_RESID0, V_SYSCALL, V_MVMEPROM, V_USERLAST)

# name, program words after MARK, regs, vector, fault_pc, epsr, handler words at the div0 entry (None = br .)
# [, handler_at: the vector whose entry the handler is planted at -- only trapfrozen8 sets it, to OVF (0x48), because its frozen
#  trap names DIV0 and a handler AT 0x40 would make the first fault's breakpoint mask the second event]
ROWS = [
    ("div0",     [DIVU_R2_R3_R0],               {"r3": 0x10},                    V_DIV0,     0x10004, PSR_RESET, None),
    ("ovf",      [ADD_R2_R3_R4],                {"r3": 0x7fffffff, "r4": 1},     V_OVF,      0x10004, PSR_RESET, None),
    ("misalign", [LD_R2_R3_0],                  {"r3": DATA + 1},                V_MISALIGN, 0x10004, PSR_RESET, None),
    ("bounds",   [TB1_0_R3_7],                  {"r3": 1},                       V_BOUNDS,   0x10004, PSR_RESET, None),
    ("priv",     [STCR_R3_CR1, LDCR_R2_CR1],    {"r3": PSR_USER},                V_PRIV,     0x10008, PSR_USER,  None),
    ("privtb",   [STCR_R3_CR1, TB1_0_R4_8],     {"r3": PSR_USER, "r4": 1},       V_PRIV,     0x10008, PSR_USER,  None),
    ("unimpl",   [STCR_R3_CR1, PROM_CALL],      {"r3": PSR_USER},                V_UNIMPL,   0x10008, PSR_USER,  None),
    ("error",    [DIVU_R2_R3_R0],               {"r3": 0x10, "r5": DATA + 1},    V_ERROR,    0x10004, PSR_RESET,
                 [0x14000000 | (6 << 21) | (5 << 16)]),       # handler at 0x40: ld r6,r5,0 with r5 odd -> 2nd fault
    ("dslot",    [BR_N_PLUS16, DIVU_R2_R3_R0],  {"r3": 0x10},                    V_DIV0,     0x10008, PSR_RESET, None),
    #  ---- v20, repair 13 (2026-10-16): {class} x {delay slot} at the four other arms an INSTRUCTION reaches from a slot.
    #  `implemented = !cpu->delay_slot' at MISALIGNED/UNIMPL/PRIV/OVF swept v19 59/59 (delayslot_20261016/); dslot held
    #  only DIV0.  BOUNDS and ERROR need a trap instruction IN a slot -- disclosed in the contract with measured escapes.
    ("dslotmisalign", [BR_N_PLUS16, LD_R2_R3_0], {"r3": DATA + 1},               V_MISALIGN, 0x10008, PSR_RESET, None),
    ("dslotunimpl", [STCR_R3_CR1, BR_N_PLUS16, PROM_CALL], {"r3": PSR_USER},      V_UNIMPL,   0x1000c, PSR_USER,  None),
    ("dslotpriv", [STCR_R3_CR1, BR_N_PLUS16, LDCR_R2_CR1], {"r3": PSR_USER},      V_PRIV,     0x1000c, PSR_USER,  None),
    ("dslotovf", [BR_N_PLUS16, ADD_R2_R3_R4],   {"r3": 0x7fffffff, "r4": 1},     V_OVF,      0x10008, PSR_RESET, None),
    ("errortb",  [TB1_0_R3_10],                 {"r3": 1},                       V_ERROR,    0x10004, PSR_RESET, None),
    ("misaligntb", [TB1_0_R3_4],                {"r3": 1},                       V_MISALIGN, 0x10004, PSR_RESET, None),
    ("unimpltb", [TB1_0_R3_5],                  {"r3": 1},                       V_UNIMPL,   0x10004, PSR_RESET, None),
    ("div0tb",   [TB1_0_R3_8],                  {"r3": 1},                       V_DIV0,     0x10004, PSR_RESET, None),
    ("ovftb",    [TB1_0_R3_9],                  {"r3": 1},                       V_OVF,      0x10004, PSR_RESET, None),
    ("vbrtb",    [STCR_R5_CR7, TB1_0_R3_7],     {"r3": 1, "r5": VBR_TEST},       V_BOUNDS,   0x10008, PSR_RESET, None),
    ("trapfrozen", [DIVU_R2_R3_R0],             {"r3": 0x11},                    V_BOUNDS,   0x10004, PSR_RESET,
                 [TB1_0_R3_7]),                               # handler at 0x40: tb1 0,r3,7 with SFRZ set -> a TRAP is not re-routed to ERROR
    ("trapfrozen4", [DIVU_R2_R3_R0],            {"r3": 0x11},                    V_MISALIGN, 0x10004, PSR_RESET,
                 [TB1_0_R3_4]),                               # frozen tb1 naming 4 -> its own vector 0x20, shadows frozen (codex, pass 5)
    ("trapfrozen5", [DIVU_R2_R3_R0],            {"r3": 0x11},                    V_UNIMPL,   0x10004, PSR_RESET,
                 [TB1_0_R3_5]),                               # frozen tb1 naming 5 -> 0x28
    ("trapfrozen6", [DIVU_R2_R3_R0],            {"r3": 0x11},                    V_PRIV,     0x10004, PSR_RESET,
                 [TB1_0_R3_6]),                               # frozen tb1 naming 6 -> 0x30
    ("trapfrozen8", [ADD_R2_R3_R4],             {"r3": 0x7fffffff, "r4": 1},     V_DIV0,     0x10004, PSR_RESET,
                 [TB1_0_R3_8], V_OVF),                        # first fault OVF (handler at 0x48); frozen tb1 naming 8 -> 0x40, observable
    ("trapfrozen9", [DIVU_R2_R3_R0],            {"r3": 0x11},                    V_OVF,      0x10004, PSR_RESET,
                 [TB1_0_R3_9]),                               # frozen tb1 naming 9 -> 0x48
    ("trapfrozen450", [DIVU_R2_R3_R0],          {"r3": 0x11},                    V_SYSCALL,  0x10004, PSR_RESET,
                 [TB1_0_R3_450]),                             # a frozen trap naming the 0x1c2 syscall label -> its own entry 0xe10 (codex, pass 7)
    ("trapfrozen496", [DIVU_R2_R3_R0],          {"r3": 0x11},                    V_MVMEPROM, 0x10004, PSR_RESET,
                 [TB1_0_R3_496]),                             # a frozen trap naming MVMEPROM_VECTOR -> its own entry 0xf80
    ("trapfrozen511", [DIVU_R2_R3_R0],          {"r3": 0x11},                    V_USERLAST, 0x10004, PSR_RESET,
                 [TB1_0_R3_511]),                             # the LAST user trap vector, frozen: exempted like 128 (kimi, pass 7: 128 pinned only the near edge)
    ("trapfrozen128", [DIVU_R2_R3_R0],          {"r3": 0x11},                    V_USER0,    0x10004, PSR_RESET,
                 [TB1_0_R3_128]),                             # a frozen USER trap: exempted from the re-route, delivered to 0x400 with frozen shadows
    ("trapfrozen10", [DIVU_R2_R3_R0],           {"r3": 0x11},                    V_ERROR,    0x10004, PSR_RESET,
                 [TB1_0_R3_10]),                              # frozen tb1 naming 10 -> 0x50: the re-route cannot see it (same target) but
                                                              # switch 1's ERROR arm can (M_ERRORFRZOFF: eligibility conditioned on SFRZ -- codex, pass 6)
    ("ovfc",     [STCR_R5_CR1, ADD_R2_R3_R4],   {"r3": 0x7fffffff, "r4": 1, "r5": PSR_CARRY}, V_OVF, 0x10008, PSR_CARRY, None),
    ("indclr",   [STCR_R5_CR1, ADD_R2_R3_R4],   {"r3": 0x7fffffff, "r4": 1, "r5": PSR_INDCLR}, V_OVF, 0x10008, PSR_INDCLR, None),
    ("umisalign", [STCR_R5_CR1, LD_R2_R3_0],    {"r3": DATA + 1, "r5": PSR_USER}, V_MISALIGN, 0x10008, PSR_USER,  None),
    ("uovf",     [STCR_R5_CR1, ADD_R2_R3_R4],   {"r3": 0x7fffffff, "r4": 1, "r5": PSR_USER}, V_OVF, 0x10008, PSR_USER,  None),
    ("errovf",   [DIVU_R2_R3_R0],               {"r3": 0x7fffffff, "r4": 1},     V_ERROR,    0x10004, PSR_RESET,
                 [ADD_R2_R3_R4]),                             # handler at 0x40: an OVERFLOW (non-trap) with SFRZ set -> re-routed to ERROR
    ("errind",   [DIVU_R2_R3_R0],               {"r3": 0x10, "r4": PSR_FRZNOIND, "r5": DATA + 1}, V_ERROR, 0x10004, PSR_RESET,
                 [STCR_R4_CR1, 0x14000000 | (6 << 21) | (5 << 16)]),   # handler: keep SFRZ, clear IND, then the odd ld -> re-route with IND clear
    ("errc",     [DIVU_R2_R3_R0],               {"r3": 0x10, "r4": PSR_FRZC, "r5": DATA + 1},     V_ERROR, 0x10004, PSR_RESET,
                 [STCR_R4_CR1, 0x14000000 | (6 << 21) | (5 << 16)]),   # handler: keep SFRZ, set C, then the odd ld -> re-route with C set
    ("errdiv0",  [DIVU_R2_R3_R0],               {"r3": 0x10, "r5": PSR_FRZSUP},  V_ERROR,    0x10004, PSR_RESET,
                 [STCR_R5_CR1, DIVU_R2_R3_R0]),               # handler: clear SFD1 (SFRZ kept), divu by zero -> DIV0 frozen -> ERROR
    ("errpriv",  [DIVU_R2_R3_R0],               {"r3": 0x10, "r5": PSR_FRZUSER}, V_ERROR,    0x10004, PSR_RESET,
                 [STCR_R5_CR1, LDCR_R2_CR1]),                 # handler: drop to USER mode (SFRZ kept), ldcr -> PRIVILEGE frozen -> ERROR
    ("errunimpl", [DIVU_R2_R3_R0],              {"r3": 0x10, "r5": PSR_FRZUSER}, V_ERROR,    0x10004, PSR_RESET,
                 [STCR_R5_CR1, PROM_CALL]),                   # handler: drop to USER mode (SFRZ kept), prom_call -> UNIMPLEMENTED frozen -> ERROR
    ("privsuptb", [TB1_0_R3_6],                 {"r3": 1},                       V_PRIV,     0x10004, PSR_RESET, None),
    ("udiv0",    [STCR_R3_CR1, DIVU_R2_R3_R0],  {"r3": PSR_USER},                V_DIV0,     0x10008, PSR_USER,  None),
    ("usertb",   [TB1_0_R3_128],                {"r3": 1},                       V_USER0,    0x10004, PSR_RESET, None),
    ("resid50",  [TB1_0_R3_50],                 {"r3": 1},                       V_RESID,    0x10004, PSR_RESET, None),
    ("resid127", [TB1_0_R3_127],                {"r3": 1},                       V_RESID2,   0x10004, PSR_RESET, None),
    ("resid11",  [TB1_0_R3_11],                 {"r3": 1},                       V_RESID0,   0x10004, PSR_RESET, None),
    ("resid50ind", [STCR_R5_CR1, TB1_0_R3_50],  {"r3": 1, "r5": PSR_INDCLR},     V_RESID,    0x10008, PSR_INDCLR, None),
    ("resid50c", [STCR_R5_CR1, TB1_0_R3_50],    {"r3": 1, "r5": PSR_CARRY},      V_RESID,    0x10008, PSR_CARRY, None),
    #  ---- v16, THE CLASS CLOSURE.  {switch-1 arm} x {C, IND}: five arms, one PSR value, because the open cells are
    #  always (C never set) and (IND never clear).  MEASURED OPEN by opus5 at DIV0, ERROR and BOUNDS (46/46 sweeps with
    #  their polarity twins red); UNIMPL and PRIV are the same cells at the two remaining arms its census names open.
    ("unimpltbc", [STCR_R5_CR1, TB1_0_R3_5],    {"r3": 1, "r5": PSR_SUPCNOIND},  V_UNIMPL,   0x10008, PSR_SUPCNOIND, None),
    ("privtbc",   [STCR_R5_CR1, TB1_0_R3_6],    {"r3": 1, "r5": PSR_SUPCNOIND},  V_PRIV,     0x10008, PSR_SUPCNOIND, None),
    ("boundstbc", [STCR_R5_CR1, TB1_0_R3_7],    {"r3": 1, "r5": PSR_SUPCNOIND},  V_BOUNDS,   0x10008, PSR_SUPCNOIND, None),
    ("div0tbc",   [STCR_R5_CR1, TB1_0_R3_8],    {"r3": 1, "r5": PSR_SUPCNOIND},  V_DIV0,     0x10008, PSR_SUPCNOIND, None),
    ("errortbc",  [STCR_R5_CR1, TB1_0_R3_10],   {"r3": 1, "r5": PSR_SUPCNOIND},  V_ERROR,    0x10008, PSR_SUPCNOIND, None),
    #  ---- v17 (grok, pass 9): the SER axis, which v16 closed at ONE arm.  PSR_SUPCNOIND now carries SER, so the five
    #  rows above close {UNIMPL, PRIV, BOUNDS, DIV0, ERROR} x {SER} as well; these three close the rest -- the OVERFLOW
    #  arm (no other row faults there with the bit set), the FALLBACK (whose blurb already claimed every settable bit),
    #  and the NON-TRAP re-route (which closes MISALIGNED x SER at the same time, since its second fault is misaligned).
    ("ovftbser",  [STCR_R5_CR1, TB1_0_R3_9],    {"r3": 1, "r5": PSR_SUPCNOIND},  V_OVF,      0x10008, PSR_SUPCNOIND, None),
    #  ovftbser completes the OVERFLOW arm rather than closing it alone: `ovfc' already holds {OVF x C} and `indclr'
    #  holds {OVF x IND}, both faulting at this arm through `add 0x7fffffff + 1'.  Stated because a pass-10 seat read
    #  the packet's description of this row -- `the overflow arm, where no other row sets the bit' -- as a ONE-ARM
    #  closure of the kind pass 9 had just found, and was right to, since the packet never mentioned the other two.
    ("resid50ser", [STCR_R5_CR1, TB1_0_R3_50],  {"r3": 1, "r5": PSR_SERSUP},     V_RESID,    0x10008, PSR_SERSUP, None),
    ("errser",    [DIVU_R2_R3_R0],              {"r3": 0x10, "r4": PSR_FRZSER, "r5": DATA + 1}, V_ERROR, 0x10004, PSR_RESET,
                 [STCR_R4_CR1, 0x14000000 | (6 << 21) | (5 << 16)]),   # handler keeps SFRZ and sets SER, then the odd ld -> re-route with SER set
    #  ---- {SFRZ set, is_trap} x {IND, C}: the re-route's TRAP side.  MEASURED OPEN by table 12 -- M_RRTRAPIND and
    #  M_RRTRAPC each swept 46/46 while the polarity twin reddened all eleven trapfrozen rows, so the eleven cover
    #  eleven LABELS in ONE status state and nothing varied the trap side's PSR.  A frozen handler writes the bit and
    #  THEN traps, so the re-route sees it (grok, pass 8, with the row shapes).
    ("trapfrozenind", [DIVU_R2_R3_R0],          {"r3": 0x11, "r5": PSR_FRZNOIND}, V_BOUNDS,  0x10004, PSR_RESET,
                 [STCR_R5_CR1, TB1_0_R3_7]),                  # frozen, IND CLEAR, then tb1 naming 7 -> exempted to 0x38, no refatal
    ("trapfrozenc",   [DIVU_R2_R3_R0],          {"r3": 0x11, "r5": PSR_FRZC},     V_BOUNDS,  0x10004, PSR_RESET,
                 [STCR_R5_CR1, TB1_0_R3_7]),                  # frozen, C SET, same trap -- PSR_WANT keeps C (the errc lesson)
    #  ---- {SFRZ set, is_trap} x {SER}.  NOT YET MEASURED, and said so: SER is an 88100 software-settable bit that no
    #  row has ever varied, so the cell is open by the same argument as IND and C.  Its mutant is owed.
    ("trapfrozenser", [DIVU_R2_R3_R0],          {"r3": 0x11, "r5": PSR_FRZSER},   V_BOUNDS,  0x10004, PSR_RESET,
                 [STCR_R5_CR1, TB1_0_R3_7]),                  # frozen, SER SET, same trap
    #  ---- v19, THE L2 REPAIR: {SFRZ set, is_trap} x {MODE, SFD1}.  v16-v17 closed IND, C and SER at this site
    #  and left these two, which is the cell-not-class error this chain has now made four times -- here inside the
    #  census written to end it.  All fourteen trap rows above carry MODE=1 and SFD1=1, so `if (!is_trap ||
    #  !(PSR & MODE))' and its SFD1 twin were invisible to the 57-row instrument.  FLOOR, not debt, on two
    #  independent precedents: PRETABLE12 graded this same inner `if' L2 for IND/C (grok, pass 11), and the pass-5
    #  and pass-7 `!is_trap || vector == <class>' mutants condition on a field the body does not test either and
    #  were repaired in-round (kimi, pass 11, in its body -- its verdict line said debt).
    #  MEASURED, table 15: trapfrozenuser is a JOINT row -- PSR_FRZUSER clears MODE **and SFD1** -- so it reds
    #  under an SFD1-conditioned mutant too.  It is still the UNIQUE carrier of the MODE cell, and the polarity
    #  control proves that rather than asserting it: CTL_RRTRAPINV reddened all fifteen MODE-set trap rows and
    #  left this one alone.  trapfrozensfd1 below is the SINGLE-AXIS discriminator (MODE set, SFD1 clear): its
    #  measured delta against its own mutant is ZERO -- trapfrozenuser alone catches M_RRTRAPSFD1 at 58/58.
    #
    #  *** THE ATTRIBUTION WARRANT WAS RULED NOT TO TRANSFER, AND THE RULING IS RECORDED HERE RATHER THAN
    #  ARGUED WITH (codex/GPT-6 Astra at max, pass 12, the closing adjudication). ***  This round claimed the
    #  anchor rule's principle one level down -- a row varying two bits cannot say which fired.  The ruling:
    #  the anchor rule repairs an oracle that compares a path with ITSELF, which is not the situation here,
    #  since the joint row already checks concrete vector and register expectations; and the carrier bounds row
    #  demand "per enumerated mutant, never per attribution need".  Removing this row loses NONE of the 56
    #  closed cells and none of table 15's kills.
    #
    #  IT IS KEPT PENDING THE 2026-09-09 ADJUDICATION, and the reason is the same seat's own next paragraph:
    #  after removal, SFD1 coverage rests entirely on trapfrozenuser, whose PSR_FRZUSER (0x03) is SHARED with
    #  errpriv and errunimpl -- so changing it to 0x0b would preserve THEIR routes while silently removing the
    #  only SFD1-clear stimulus, and BASE alone would not notice.  Remove-or-keep is a RULE QUESTION about what
    #  the addition licence authorises when redundancy buys a failure signature, and the carrier sends rule
    #  questions to the flagship seat at the next round boundary.  Row m88ksfd1row carries it.
    #
    #  WHATEVER IS DECIDED: any edit to PSR_FRZUSER owes a re-check of the pre-trap bit values and a repeat of
    #  BOTH named mutant measurements.  That obligation is independent of the row's fate.
    ("trapfrozenuser", [DIVU_R2_R3_R0],         {"r3": 0x11, "r5": PSR_FRZUSER},  V_USER0,   0x10004, PSR_RESET,
                 [STCR_R5_CR1, TB1_0_R3_128]),                # frozen handler drops to USER mode, then a user trap at
                                                              # 128: >= USER_TRAPS_START so the fallback does not claim
                                                              # it, and X(tb1) checks privilege only for vector < 128 --
                                                              # so the re-route sees is_trap with MODE CLEAR.  r3 = 0x11:
                                                              # bit 0 must be SET or tb1 does not trap at all
    ("trapfrozensfd1", [DIVU_R2_R3_R0],         {"r3": 0x11, "r5": PSR_FRZSUP},   V_BOUNDS,  0x10004, PSR_RESET,
                 [STCR_R5_CR1, TB1_0_R3_7]),                  # frozen, SFD1 CLEAR, same trap as trapfrozenind
    ("usfu1",    [STCR_R5_CR1, DIVU_R6_R5_R4],  {"r5": PSR_USERSFD1, "r4": 0x10}, V_SFU1,    0x10008, PSR_USERSFD1, None),
    ("sfu1h",    [DIVU_R2_R3_R0],               {"r3": 0x10, "r5": 0x60, "r4": 0x10}, V_SFU1, 0x10004, PSR_RESET,
                 [DIVU_R6_R5_R4]),                             # handler at 0x40: a legal divu with SFD1 set -> SFU1 (114) -> fallback HALT
    ("live",     [DIVU_R2_R3_R4],               {"r3": 0x60, "r4": 0x10},        None,       None,    None,      None),
    ("attrib",   [DIVU_R2_R3_R4],               {"r3": 0x10, "r4": 0x10},        None,       None,    None,      None),
]
EXPECT_R2 = {"live": 6, "attrib": 1}
VBR_OF = {"vbrtb": VBR_TEST}                     # rows that relocate the vector table; every other row runs with VBR == 0
#  NEGATIVE CONTROLS: rows whose CORRECT result is the fallback HALT.  They pin the boundary the diff keeps on purpose --
#  vectors 11..113/116..127 and SFU1 (114/115) still stop the machine -- and separate the shipped D1 form from the rejected
#  D4 (tail-default-delivers) and from delivering SFU1 (row m88kexcsfu1).  A mutant that delivers them turns these rows RED.
EXPECT_RESULT = {"resid50": "HALT", "resid127": "HALT", "resid11": "HALT", "resid50ind": "HALT", "resid50c": "HALT", "resid50ser": "HALT", "sfu1h": "HALT", "usfu1": "HALT"}
PSR_WANT = {"errc": 0x9000000b,   # v14: exception entry ORs MODE|SFRZ|IND|SFD1 and leaves C alone (mc88100 manual: "the shadow freeze,
                                  #      SFD1, and IND bits of the PSR are set"), so the C-set handler row keeps C -- table 11 BASE read
                                  #      45/46 bad=psr on this row before any mutant: a MIS-CUT ROW, not the fix (case 3)
            "ovfc": 0x9000000b,                  # MODE | C | SFD1 | IND | SFRZ: carry PRESERVED through the exception path
            "unimpltbc": 0xb000000b, "privtbc": 0xb000000b, "boundstbc": 0xb000000b,
            "div0tbc": 0xb000000b, "errortbc": 0xb000000b, "ovftbser": 0xb000000b,   # v17: entry ORs MODE|SFRZ|IND|SFD1 onto
                                                 # 0xb0000000 and leaves BOTH C and SER alone -- the same fact ovfc pinned for C
            "trapfrozenc": 0x9000000b,           # a frozen trap keeps the carry it was given
            "trapfrozenser": 0xa000000b,         # ... and keeps SER, which the common path also leaves alone
            "errser": 0xa000000b}                # v17: the non-trap re-route with SER set -- also the MISALIGNED x SER cell
#  indclr wants the default PSR_EXC (0x8000000b): IND was CLEAR before the fault and must be SET by the exception path;
#  EPSR keeps the pre-fault 0x80000000.  A write that drops `| M88K_PSR_IND' leaves 0x80000009 -> bad=psr.
EXPECT_VECTOR = {"resid50": 0x032, "resid127": 0x07f, "resid11": 0x00b, "resid50ind": 0x032, "resid50c": 0x032, "resid50ser": 0x032, "sfu1h": 0x072, "usfu1": 0x072}
#  (the vector the fallback diagnostic must NAME for an expected-HALT row -- the comment that used to trail the dict above)
#  refatal: the re-route prints `[ SFRZ already set in PSR => ERROR ]' (fatal() is a plain print in this fork); a re-routed non-trap row
#  must SEE it, a frozen-trap row must NOT -- the channel that tells the exemption arm from the re-route arm when both land on 0x50
#  (kimi, pass 6: the class-10 "equivalent" disclosure was false for the composite).
REFATAL = "SFRZ already set in PSR"
REFATAL_EXPECT = {"error": True, "errovf": True, "errdiv0": True, "errpriv": True, "errunimpl": True, "errind": True, "errc": True, "errser": True,
                  "trapfrozen": False, "trapfrozen4": False, "trapfrozen5": False, "trapfrozen6": False, "trapfrozen8": False,
                  "trapfrozen9": False, "trapfrozen10": False, "trapfrozen128": False, "trapfrozen450": False, "trapfrozen496": False, "trapfrozen511": False,
                  "trapfrozenind": False, "trapfrozenc": False, "trapfrozenser": False,
                  "trapfrozenuser": False, "trapfrozensfd1": False}   # v19: the exemption must hold with MODE and
                  #      SFD1 clear too -- and this is the CHANNEL that makes the two rows non-vacuous, because the
                  #      mutant re-routes the trap and the diagnostic then APPEARS where these expect none
#  (v12 COPIED this dict's trailing comment up to EXPECT_VECTOR, where it belongs, and claimed to have REMOVED it here.
#   It had not: the file carried it twice.  v16 then tried to delete it with a find-text that was only a PREFIX of the
#   old sentence, so `.replace()` left the tail behind and produced the nonsense `claimed tognostic must NAME for an
#   expected-HALT row'.  Found by grok on pass 9, reading the shipped file rather than the diff.  THE LESSON IS THE
#   SECOND FAILURE, not the first: a correction is not safer than the thing it corrects, and this one shipped a worse
#   sentence than the duplicate it was removing.  A deletion whose find-text is a PREFIX must match to end-of-line.)

class Sess:
    def __init__(self):
        stub = "/tmp/gx_m88k_exc_%d.bin" % os.getpid()
        with open(stub, "wb") as f:
            f.write(struct.pack(">I", 0xf4005800))          # or r0,r0,r0 so the machine constructs
        self.pid, self.fd = pty.fork()
        if self.pid == 0:
            os.execvp(BIN, [BIN, "-V", "-E", "testm88k", "-M", "64", "0x10000:%s" % stub])
            os._exit(127)
        self.buf = ""
    def rd(self, t=0.4):
        r, _, _ = select.select([self.fd], [], [], t)
        if self.fd not in r:
            return True
        try:
            d = os.read(self.fd, 65536)
        except OSError:
            return False
        if not d:
            return False
        self.buf += d.decode("latin1", "replace")
        return True
    def wait_prompt(self, mark, timeout=30):
        t = time.time()
        while time.time() - t < timeout:
            if not self.rd():
                return False
            if len(self.buf) > mark and self.buf[mark:].rstrip().endswith("GXemul>"):
                return True
        return False
    def send(self, sx, timeout=30):
        mark = len(self.buf)
        b = (sx + "\n").encode("latin1"); n = 0
        while n < len(b):
            n += os.write(self.fd, b[n:])
        self.wait_prompt(mark, timeout)
        return mark
    def cr(self, name):
        m = self.send("reg 0,0")
        mm = re.search(r"(?<![A-Z])%s=0x([0-9a-f]{8})" % name, self.buf[m:])
        return int(mm.group(1), 16) if mm else None
    def gpr(self, n):
        m = self.send("reg")
        mm = re.search(r"r%-2d\s*=\s*0x([0-9a-f]{8})" % n, self.buf[m:])
        return int(mm.group(1), 16) if mm else None
    def pc(self):
        m = self.send("reg")
        mm = re.search(r"pc\s*=\s*0x([0-9a-f]{8})", self.buf[m:])
        return int(mm.group(1), 16) if mm else None
    def close(self):
        try:
            os.write(self.fd, b"quit\n"); time.sleep(0.3); os.kill(self.pid, 9); os.waitpid(self.pid, 0)
        except Exception:
            pass

def fmt(v):
    return ("0x%08x" % v) if isinstance(v, int) else str(v)

def run_row(name, prog, regs, vector, fault_pc, epsr_exp, handler, grace=6.0, handler_at=None):
    if handler_at is None:
        handler_at = V_DIV0                              # the first fault of every two-fault row is DIV0 unless the row says otherwise
    s = Sess()
    if not s.wait_prompt(0, 60):
        s.close(); return dict(result="NOBOOT")
    vbr = VBR_OF.get(name, 0)
    entry = (vbr + 8 * vector) if vector is not None else None
    words = [MARK] + prog + [SELF]
    for i, w in enumerate(words):
        s.send("put w 0x%x, 0x%08x" % (CODE + 4 * i, w))
    for base in sorted({0, vbr}):                       # every entry spins unless a handler is planted (both tables if relocated)
        for v in VECTORS:
            s.send("put w 0x%x, 0x%08x" % (base + 8 * v, SELF))
    if entry is not None:
        s.send("put w 0x%x, 0x%08x" % (entry, SELF))
    if handler:
        for i, w in enumerate(handler):
            s.send("put w 0x%x, 0x%08x" % (8 * handler_at + 4 * i, w))
        s.send("put w 0x%x, 0x%08x" % (8 * handler_at + 4 * len(handler), SELF))
    s.send("put w 0x%x, 0x%08x" % (DATA, 0x0badf00d))
    for r, v in regs.items():
        s.send("%s=0x%x" % (r, v))
    s.send("r10=0x12345678"); s.send("r2=0xdeadbeef")
    if vector is not None:
        s.send("breakpoint add 0x%x" % entry)
    s.send("pc=0x%x" % CODE)
    mark = len(s.buf)
    os.write(s.fd, b"continue\n")
    t = time.time()
    while time.time() - t < grace:
        s.rd(0.3)
        if s.buf[mark:].rstrip().endswith("GXemul>"):
            break
    if not s.buf[mark:].rstrip().endswith("GXemul>"):
        os.write(s.fd, b"\x03"); s.wait_prompt(len(s.buf), 15)
    tr = s.buf[mark:]
    #  HALT is the fallback's diagnostic AND the machine-stopped observation (codex, pass 3: a mutant that keeps the
    #  message and drops the stop would otherwise classify as HALT); an expected-HALT row must also see ITS vector named.
    diag = re.search(r"unimplemented[^\r\n]*vector=0x([0-9a-f]+)", tr)
    stopped = "machines stopped" in tr           # emul.c's `All machines stopped.' -- the ONE stop observation (pass 4:
    halted = diag is not None and stopped        # an `or "stopped" in tr' disjunct had made the exact term dead code)
    if halted and name in EXPECT_VECTOR and int(diag.group(1), 16) != EXPECT_VECTOR[name]:
        halted = False                              # halted on some OTHER vector: not the row's answer
    #  LEVEL channel (Fable review seat, pass 2): main.c lowers every subsystem to WARNING after startup, so a
    #  free-running `continue' prints an ERROR-level `[ exception <CLASS>: ]' line and stays silent at INFO.  A
    #  delivered row that carries the line has the pre-fix level (M_LEVEL) -- #261's opt-in break-on-ERROR would
    #  then stop the emulator into the debugger on a user process's divide by zero.
    levelmsg = re.search(r"exception (MISALIGNED_ACCESS|UNIMPLEMENTED_OPCODE|PRIVILEGE_VIOLATION|"
                         r"BOUNDS_CHECK_VIOLATION|ILLEGAL_INTEGER_DIVIDE|INTEGER_OVERFLOW|ERROR)", tr) is not None
    tailhalt = "internal error" in tr
    pc = s.pc(); r2 = s.gpr(2); r9 = s.gpr(9)
    sxip, snip, sfip, psr, epsr = s.cr("SXIP"), s.cr("SNIP"), s.cr("SFIP"), s.cr("PSR"), s.cr("EPSR")
    s.close()
    started = (r9 == 0x12345678)
    res = dict(pc=pc, sxip=sxip, snip=snip, sfip=sfip, psr=psr, epsr=epsr, r2=r2, transcript=tr)
    if not started:
        res["result"] = "NOSTART"; return res
    if vector is None:
        ok = (not stopped) and r2 == EXPECT_R2[name]
        res["result"] = "DONE" if ok else ("STOP" if stopped else "BADREGS"); return res
    if halted:
        res["result"] = "HALT"
        if name == "sfu1h" and pc != 8 * V_DIV0:
            res["result"] = "BADREGS"; res["bad"] = ["stage1"]   # halted before the handler ran (the pre-fix shape)
    elif tailhalt:
        res["result"] = "TAILHALT"
    elif stopped:
        res["result"] = "STOP"
    elif pc != entry:
        res["result"] = "STOP"          # ran past its grace without the entry breakpoint firing
    else:
        want = dict(sxip=(fault_pc | XIP_V), psr=PSR_WANT.get(name, PSR_EXC), epsr=epsr_exp, r2=0xdeadbeef)
        if name in ("error", "trapfrozen", "errovf", "errdiv0", "errpriv", "errunimpl", "errind", "errc", "errser",
                    "trapfrozen4", "trapfrozen5", "trapfrozen6", "trapfrozen8", "trapfrozen9", "trapfrozen10", "trapfrozen128",
                    "trapfrozen450", "trapfrozen496", "trapfrozen511",
                    "trapfrozenind", "trapfrozenc", "trapfrozenser", "trapfrozenuser", "trapfrozensfd1"):
            # the second fault runs with SFRZ set: the shadows stay FROZEN at the first fault's values.  For
            # `trapfrozen' the second fault is a TRAP, which the manual (:8633-8636, 6.10 :10613-10614) exempts from
            # the ERROR re-route: it must deliver to ITS OWN vector (0x38), shadows still frozen.  M_SFRZTRAP sends it to 0x50.
            want.update(sxip=(0x10004 | XIP_V), snip=(0x10008 | XIP_V), sfip=(0x1000c | XIP_V), epsr=PSR_RESET)
        elif name.startswith("dslot"):
            # the else-arm of the delay-slot branch: SNIP = (pc + 4) | V, SFIP = delay_target | V.  br.n +16 puts
            # delay_target at 0x10014 while slot_pc+4 is 0x1000c, so the two channels are DIFFERENT numbers (with
            # br.n +8 they were both 0x1000e and M_SFIPNOTGT / M_DSLOTSWAP escaped 10/10 -- Opus, pass 2).
            # v20: every dslot* row puts the br.n +16 IMMEDIATELY before its faulting word, so delay_target is
            # (fault_pc - 4) + 16 -- for dslot itself that is 0x10014, the CODE + 4 + 16 this line used to spell.
            want.update(snip=((fault_pc + 4) | XIP_V), sfip=((fault_pc - 4 + 16) | XIP_V))
            assert want["snip"] != want["sfip"], "dslot geometry collapsed: SNIP and SFIP would be one number"
        else:
            want.update(snip=((fault_pc + 4) | XIP_V), sfip=((fault_pc + 8) | XIP_V))
        bad = [k for k, v in want.items() if res.get(k) != v]
        if name in REFATAL_EXPECT and ((REFATAL in tr) != REFATAL_EXPECT[name]):
            bad.append("refatal")                      # the re-route's diagnostic present where the exemption should hold, or absent where the re-route fired
        if levelmsg:
            bad.append("level")
        res["result"] = "DELIVER" if not bad else "BADREGS"
        res["bad"] = bad
    return res

def selftest():
    s = Sess()
    ok = s.wait_prompt(0, 60)
    psr = s.cr("PSR") if ok else None
    s.close()
    return psr == PSR_RESET, psr

def main():
    ok, psr = selftest()
    print("M88KEXC_SELFTEST=%s psr_at_reset=%s (want 0x80000002)" % ("OK" if ok else "FAIL", fmt(psr)), flush=True)
    delivered = 0; total = 0; controls_bad = []
    for row in ROWS:
        name, prog, regs, vector, fault_pc, epsr_exp, handler = row[:7]
        handler_at = row[7] if len(row) > 7 else V_DIV0
        res = run_row(name, prog, regs, vector, fault_pc, epsr_exp, handler, handler_at=handler_at)
        print("M88KEXC_ROW=%-9s RESULT=%-8s pc=%s sxip=%s snip=%s sfip=%s psr=%s epsr=%s r2=%s%s" % (
            name, res.get("result"), fmt(res.get("pc")), fmt(res.get("sxip")), fmt(res.get("snip")),
            fmt(res.get("sfip")), fmt(res.get("psr")), fmt(res.get("epsr")), fmt(res.get("r2")),
            (" bad=" + ",".join(res["bad"])) if res.get("bad") else ""), flush=True)
        if vector is not None:
            total += 1
            if res.get("result") == EXPECT_RESULT.get(name, "DELIVER"):
                delivered += 1
        elif res.get("result") != "DONE":
            controls_bad.append(name)
        if os.environ.get("M88KEXC_VERBOSE"):
            print("---- transcript ----"); print(res.get("transcript", "")[-1200:]); print("--------------------")
    print("M88KEXC_RESULT=%d/%d" % (delivered, total), flush=True)
    if controls_bad:
        print("M88KEXC_CONTROLS=BAD %s" % ",".join(controls_bad), flush=True)
    print("M88KEXC_DONE", flush=True)
    #  exit status: the gate can rely on it (a row printing a failure word while the process exits 0 was a pass-2 finding)
    sys.exit(0 if (ok and delivered == total and not controls_bad) else 1)

if __name__ == "__main__":
    main()
