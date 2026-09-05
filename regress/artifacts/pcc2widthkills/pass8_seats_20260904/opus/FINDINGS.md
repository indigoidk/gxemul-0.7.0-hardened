# pcc2widthkills PASS 8 -- Opus seat findings (working notes; final answer goes in the report)

Tree: GXEMUL-SEC uncommitted on b78bb0f.  dev_pcc2.c md5 f9168636; probe md5 82c6a7c5.
Clone /tmp/gxopus_p8 (cp -a of build/), cmp-CLEAN vs SEC before mutants, BASE FRESH_OK.
Predictions: PRETABLE_pass8_opus.out, mtime 06:41:22, written before any mutant build.

## F1 (L2 instrument + L4 x3) -- THE PASS-7 `until' REPAIR IS INERT.
pcc2_width_probe.py:382-384.  Line 383 rebinds c to c[0] (the STRING); line 384 then indexes
the STRING and len(c) is the STRING's length.  For ("continue", 20.0, "BREAKPOINT") at :718:
    c = "continue"; w = 20.0; len("continue")==8>2; until = "continue"[2] == "n"
rd() tests `until in buf' BEFORE its first select() (:363-365) and buf already holds the echo
of "breakpoint add 0x...", so the wait returns TRUE IMMEDIATELY.
* the claimed 20 s ceiling is ZERO;
* the pre-repair form was rd(8.0), an unconditional 8 s drain -- the repair CUT the time the
  guest gets to reach its breakpoint from 8 s to ~0 s, making the load-sensitivity WORSE;
* falsifies three records: contract :236-238, PRETABLE_pass7 Section 14, pass-7 CHANGELOG.
Confirmed under the gate's own interpreter: until = 'n', w = 20.0.

## F2 (L4 + laundered failure) -- A SIGKILLED GUEST REPORTS how = "exit0".
:406-427.  WNOHANG returns (0,0) while the child lives, so stat is 0, NOT None.  for/else sets
how="killed", then WIFEXITED(0)=True overwrites it with "exit0".  Verified in WSL python3.
`how' is the survival oracle of ~20 rows; a HANGING mutant reads as "survived, exit 0".  The
paired `lv' rows still catch it, so the pair discipline holds -- but the `killed' branch is
unreachable-as-observed and nothing reaps after kill(9) (zombie per killed session).

## F3 (answers Q3) -- 8 OF THE 12 FREE-RUNNING ROWS STILL FAIL SILENTLY.
armval() (:722-726) was applied to FOUR rows only: pend2 arm :732, pend1 arm :740,
ovf2 arm :756, ovf1 arm :763.  The other eight rows of the SAME four sessions keep the old
idiom: the four *rb* rows (:734,:742,:758,:765) print "died" -- the same token a real host
death gives -- when the second `print r4' has merely not been drained; the four *decl* rows
(:733,:741,:757,:764) count DECL against 1 and red as if the GUARD failed when the session was
cut short.  Neither says FAILED FOR SOME OTHER REASON.

## F4 (Q1) -- THE ENUMERATION SAYS SEVEN ARMS "read nothing"; ALL SEVEN READ `idata'.
:219-223.  idata is a function-scope lvalue (dev_pcc2.c:410) and every one of those bodies
reads it -- the sentence's own "= idata & m" says so.  Five read it twice (VECBASE :461-462,
SCCICR :562-563, SCCTX :576-577, SCCRX :590-591, SCSIICR :610-611).  Ten of twelve bodies read
idata; only SCCERR (:553) and IPL (:628-631) do not.  idata is the operand of the row THIS
PASS shipped (latch all one, F-K, ruled L2 IN CLOSURE), so the docstring contradicts itself.
Also omitted: relative_addr at TxCTL (read at :496,:497,:500; TxCTL is a two-label block like
TxICR, for which the enumeration DOES name it).  Coverage exists; the list does not.

## F5 (Q1) -- THE IPL ARM HAS TWO FUNCTION-STATICS; THE ENUMERATION NAMES ONE.
dev_pcc2.c:629 (write branch) and :634 (READ branch).  Contract :217 says "the function-static
`w'", singular.  The OUT-OF-CLOSURE sentence :224-227 excludes reg[IPL] because it is read by
"the IPL arm's READ branch"; the second static lives in that same branch and is named nowhere.
MEASURED as M_IPLR below.

## F6 (Q1) -- ONE BIT-DOMAIN STATED TOO WIDE.
:212 "TxICR ... bits 0-4 by presets".  The mask is 0x17 = bits 0,1,2,4; bit 3 (ICLR) is not in
it and is never set by anything, so it is permanently zero (safe direction, wrong statement).
TxCTL's bits 2-3 are likewise unreachable, which is WHY "bits 0-1 / 4-7" is complete there --
the warrant is absent in both places.

## Q2 -- WIDTH CLOSURE BY LABEL: VERIFIED, THE CLAIM HOLDS.
(uint8_t)idata is the composed value's LOWEST byte = HIGHEST-address lane.
w4 = 0xaab8ccd9 at GENCTL else 0xaab8ccdd -> lane 0xd9 / 0xdd.
w8 = ...00112240 at GENCTL else ...00112244 -> lane 0x40 / 0x44.
    GENCTL  0x82  = idata          -> 0xd9 / 0x40   != preset, C040 CLEAR in both
    VECBASE 0x50  & 0xf0           -> 0xd0 / 0x40   != preset
    T2CTL   0x03  RMW &3           -> 0x01 / 0x00   != preset
    T2ICR   0x13  RMW &0x17        -> 0x15 / 0x04   != preset
    SCCICR  0x1f  & 0x1f           -> 0x1d / 0x04   != preset
    SCCTX   0x1f  & 0x1f           -> 0x1d / 0x04   != preset
    SCCRX   0x1f  & 0xdf           -> 0xdd / 0x44   != preset
    SCSIICR 0x1f  & 0xdf           -> 0xdd / 0x44   != preset
    MASK    0x12  = idata          -> 0xdd / 0x44   != preset
    T1CTL   0x03  RMW &3           -> 0x01 / 0x00   != preset
    T1ICR   0x13  RMW &0x17        -> 0x15 / 0x04   != preset
Second death path checked (the one the C040 finding came from): reassert_interrupts()'s only
exit(1) is on reg[GENCTL] & PCC2_C040 (:263-269); each rb4/rb8 session writes ONE register, so
GENCTL is 0 except in its own session where the lane is 0xd9.  The ASSERT path is inert too:
MIEN (GENCTL 0x02) is clear so assert is forced to 0 at :333-334.

## PREMISES RE-DERIVED FROM SOURCE
* Premise 3 CONFIRMED independently: memory_rw.c:584-585 dispatches only if
  !no_exceptions || (flags & DM_READS_HAVE_NO_SIDE_EFFECTS); pcc2 registers DM_DEFAULT
  (dev_pcc2.c:736); put b and debugger reads use NO_EXCEPTIONS (debugger_cmds.c:1506-1507,
  :716-717); put h/w/d go through store_16/32/64bit_word (:1523/:1543/:1558) -> memory_rw with
  CACHE_DATA (core/memory.c:827-828).
* Offsets CONFIRMED from mvme_pcctworeg.h: six EVEN guarded (0x02,0x16,0x1a,0x1c,0x1e,0x3e),
  eight ODD (0x03,0x15,0x17,0x1b,0x1d,0x1f,0x2f,0x3f); only SCCERR 0x1c is 4-aligned.
* Product-comment counts CONFIRMED: eight masking/RMW/clearing arms; seven blocks reassert;
  five of those eight.
* ovf arithmetic CONFIRMED: tick adds 1000000/PCC_TIMER_TICK_HZ (:185), so ONE tick crosses
  2^31 from 0x7fffff00 and oc = 1 + (reg>>4) = 1 -> T2CTL 0x11 (:216-220,:240-244).
* row() carries a DUPLICATE-NAME assert (:340) and assert len(name) <= 15 (:341) -- the guard
  that keeps this project's padded-column trap out of the gate pattern.  Longest live name is
  "brd pscale noig" (15): a ONE-character margin, held by an assert.  gate_arm.sh:1295 lists
  exactly 171 names (counted).

## F7 (Q5) -- NO GATE HAS RUN AGAINST THE SHIPPED PROBE.
CHANGELOG.md:121 calls the pass-8 gate's instrument "the shipped 171-row instrument
(md5 e43bde87)".  Measured mtimes to the second:
    06:03:03.626  killtable2_20260903/gate14_p8.log     (gate finished)
    06:03:04.015  regress/pcc2_width_probe.py           (probe EDITED 0.39 s later)
    06:29:30.976  part7b/frozen_probe.py  md5 82c6a7c5
md5sum of the live probe is 82c6a7c5, not e43bde87.  Part 7b's BASE does cover the shipped
bytes, so the ROWS are measured; what is unmeasured is the GATE (its 171 name-string checks)
against the file that ships.

## F1 MEASURED (f1_err.txt, f1_out.txt in this directory; instrumented copy of the frozen
## probe, 11 added lines, run against the clone's BASE binary)
    F1 tuple: c='continue' until='n' w=20.0
    F1 wait: 0.000 s  until='n'  BREAKPOINT_in_buf=False
    F1 EARLY EXIT after pend2
The wait after `continue' returned in **0.000 s** with the BREAKPOINT text NOT YET IN THE
BUFFER -- i.e. the driver sent the next command to a guest that had not reached its
breakpoint, which is verbatim the failure pass 7 says it repaired.  The rows were still green
in that run (pend2 arm 0x31, pend2 decl 1, pend2 rb 0x31), so the defect is LATENT, not
currently red: the ~8 following commands' 0.25 s drains happen to exceed the ~10 ms one
SIGALRM tick needs.  112 rows emitted before the early exit.

## F8 (Q5) -- BOTH PASS-7 AS-RUN DRIVERS CARRY A PASS-2 HEADER.
`killtable2_20260903/part7/killpcc2b_part7.asrun.sh` and `.../part7b/killpcc2b_part7b.asrun.sh`
both open with 22 lines headed "PART 2, reduced ... pcc2widthkills pass-2 repair table -- the
IPL/MASK rows" and list M_DELETE_MASK / M_KILL_IPL / M_KILL_MASK / M_DELETE -- none of which
either script runs.  The executable bodies are correct (the `mut' lines build M_IPL_W,
M_TXCTL_OVF, M_T1_W4FALL_CTL/ICR, M_IDATA_NE1_ALL and M_IDATA_NE1_QUAL, each with a count
assertion).  Pass 7's own finding F-I was that part6/6b had NO preserved driver; the repair
shipped one whose documentation describes a different table -- the same copy-paste class the
round corrected in the MASK product comment this pass.

## F9 (Q5) -- THE BRIEF'S PREMISE 8 REPEATS THE MISCOUNT PASS 7 CORRECTED.
Premise 8: "nine of nine answered (codex, grok, fable5, opus5, deepseek, the kimi-k3:cloud
substitute ..., glm and minimax ...); agy DELIBERATELY NOT FIRED" -- eight names, "nine of
nine", and then the ninth declared not fired.  The CHANGELOG gets it right ("eight answering
seats of nine").  Pass 7's correction list contains, verbatim: *codex: "nine of nine answered"
for pass 6 -- eight answering seats of nine, agy deliberately not fired.*
Counted from `_scratchpad/panel_20260904_033322/`: codex 440336 B, grok 12110, kimi.txt 350 B
(the weekly WALL, correctly detected), ollama_kimi 8961 (the substitute), ollama_glm 137538
(BURNED) + refire 3553, ollama_minimax 54746 (BURNED) + refire 2718, ollama_deepseek 2167.
Six transports on disk + the two Agent seats (which leave no file) = EIGHT answering.

## RECORD CLAIMS RE-DERIVED AND CONFIRMED (so the zero has a denominator)
* init values, DEVINIT :705-709: CHIPID 0x20, CHIPREV 0, GENCTL 0x00, VECBASE 0x0f,
  PSCALEADJ 256-33 = 0xdf.  Of the TWELVE GUARDED registers only VECBASE and PSCALEADJ are
  non-zero; CHIPID is non-zero and is not one of them.  Opus F-E's pass-7 correction is right.
* GENCTL == 0 at init, so PCC2_MIEN (0x02) is CLEAR -- the free-running loops' stated
  dependency holds.
* DEV_PCC2_TICK_SHIFT is 14 (:62) -- "every 2^14 instructions" is right.
* `latch all fail's` oracle string "failed ]" has exactly ONE source in the tree,
  memory_rw.c:605, guarded by `res <= 0 && !no_exceptions` (:603) -- reachable from `put h`,
  which does not pass NO_EXCEPTIONS.  The row's mechanism is sound.
* the DECL suffix "-- declined.  (once) ]" is emitted by pcc2 and exactly THREE other devices
  (dev_dreamcast_gdrom.c, dev_sgi_re.c, dev_sh4.c), none on mvme187 -- the disclosure is exact.
* d->warned is uint32_t (:134) with twelve enum members ending in PCC2_W_NBITS (:116-128), and
  the negative-array-size typedef (:151-152) tests the FIELD, not a literal.

## F10 (Q1, the sharpest enumeration finding) -- THE BIT-DOMAINS ARE CLAIMED AT LVALUE
## GRANULARITY AND SATISFIED AT ONE BIT.
The restated enumeration promises "each lvalue with its FULL bit-domain and the row holding it
non-initial at a wide write".  For the two IN-CLOSURE registers the rows hold a proper subset:

* **TxCTL, "bits 4-7, the overflow count ... by `ovf1 *` / `ovf2 *`".**  The ovf rows drive
  the count to exactly ONE (`oc = 1 + (reg >> 4)`, dev_pcc2.c:217/:241), so the register is
  0x11: **bit 4 held, bits 5, 6, 7 at their initial zero.**  A guard `&& !(reg & 0x20)` (or
  0x40 / 0x80) at TxCTL is in closure, is a sub-mask of the very mutant the round DID build
  (M_TXCTL_OVF used `PCC2_TCTL_OVF` = 0xf0), and escapes every row.
  Cost of closing it is real, and that is the point: a SECOND overflow needs the counter to
  climb 2^31 again at 10000/tick, 100 Hz -- about **2147 s of host time** -- unless the row
  re-stores T2COUNT and free-runs again per increment (8 cycles for bit 7).  So the honest
  repair is a DISCLOSURE ("bit 4 held; bits 5-7 cost one extra free-run each and are not
  rowed"), not more rows.  As written the sentence claims coverage no row carries.
* **TxICR, "bits 0-4 by presets".**  Every TxICR preset in the file is 0x13 (16 occurrences),
  0x11 (`PEND_REGS`) or 0x10 (`acc all`) -> bits 0, 1, 4 only.  **Bit 2 (IL bit 2, 0x04) is in
  the arm's own `idata & 0x17` domain and is held by no row**; bit 3 is not in the mask at all
  (F6).  A guard `&& !(reg & 0x04)` at TxICR escapes.
  This one closes for FREE: change the TxICR preset from 0x13 to **0x17** and bits 0,1,2,4 are
  all held.  Checked for side effects -- the arm stores `(reg & ~0x17) | (idata & 0x17)` so the
  readback want becomes 0x17, and the fall-through lanes stay distinct from it (len 2 -> 0xb8 &
  0x17 = 0x10; len 4 -> 0x15; len 8 -> 0x04; all != 0x17).

Not a floor breach in my reading -- neither sub-mask is a named constant, so the "plausible
future edit" test is weaker than for the forms the round built -- but it IS a coverage claim
the rows do not carry, which is exactly what Q5 asks to be named.

## F11 (Q3, second half) -- CAN THE GATE STILL HANG?  The waitpid half of the repair WORKS.
Walked every exit of session():  `rd()` is time-bounded on every call; the WNOHANG loop is
bounded (30 x 0.1 s) and then SIGKILLs; the follow-up `waitpid(pid, 0)` is REACHED ONLY when
`stat is None`, which happens only on an OSError path where the blocking call raises ECHILD
immediately and is caught.  So no hang there -- the repair's stated purpose is achieved (with
F2's cosmetic defect on `how`).
One residual, and F1 makes it MORE likely rather than less: `os.write(fd, ...)` to the pty
master has no timeout, and with the wait broken the driver now writes ~8 further commands while
the guest is still free-running instead of draining for 8 s first.  A full pty input buffer
would block that write forever, and a blocking write is not an OSError so the `except OSError`
does not cover it.  The queued commands are ~400 bytes against a ~4 KB buffer, so it does not
bite today.

## F12 (Q3, third half) -- THE TOKEN IS RIGHT.
`cpu_dyntrans.c:1833/:1837` print `BREAKPOINT: pc = 0x...` via **fatal()**, which this fork has
measured to have NO early-out (unlike debug()), so the token survives -q and every verbosity
setting.  Good choice; only its DELIVERY is broken (F1).
Related and also correct: `latch all fail's` oracle is memory_rw.c:604 **debug()**, and the
contract's stated reason -- "prints because this probe single-steps" -- is right, since debug()
returns early on `(quiet_mode && !ss) || v < 0` and `-V` puts the session in single_step.

## F13 (Q5) -- THE VALUE-COVERAGE DISCLOSURE UNDERSTATES ITS OWN ROWS.
The C-warrant sentence says a value-test qualifier is caught "only for the VALUES rows drive --
3, 0 and 1".  Counted from the probe, the wide-written values are at least: 0x0001, 0x0003,
0x0022, 0x0000, 0x0303, 0x1234, 0xaab8, 0xaabb, 0x00000003, 0xaab8ccd9, 0xaab8ccdd,
0x0000000000000003, 0xaab8ccdd00112240, 0xaab8ccdd00112244 -- fourteen, not three.  Safe
direction (it disclaims coverage it has), but a future round reading that sentence would think
`&& idata != 0x0303` escapes when `op vecbase dcl` and six siblings kill it.

## VALIDITY OF THIS PASS (the closing-zero conditions, checked rather than asserted)
* **Diff delivered: YES, in full.**  Product diff `git diff -U3 src/devices/dev_pcc2.c` = **5
  hunks** (@@ -64,8 / -80,22 / -135,6 / -603,7 / -624,7); the brief inlines all five.  Probe
  diff `diff -u part6b/frozen_probe.py regress/pcc2_width_probe.py` = **9 hunks** (@@ -82,8 /
  -185,34 / -316,10 / -335,14 / -355,8 / -605,11 / -625,10 / -640,14 / -655,12), 146 added and
  27 removed lines; the brief inlines all nine.  This is NOT one of the three briefs the
  carrier records as blinded by a `git show | head -N`.
* **Roster**: I am the opus5 seat.  `_scratchpad/panel_20260904_063019/` holds codex 721114 B,
  grok 10653, kimi.txt 350 (the weekly wall), ollama_kimi 4729 (the substitute), ollama_glm
  5686 (no burn this time -- the packet is 8885 B), ollama_minimax 4468, ollama_deepseek 1643.
  The two Agent seats leave no file, so a file count under-counts by exactly two.

## F14 (OUTSIDE THE QUESTIONS) -- EIGHT UNFILED SIBLINGS OF `pcc2pscaleflood`, SEVEN OF THEM
## IN THE ARMS THIS ROUND EDITED.
Census of every `fatal(` in dev_pcc2.c (16 call sites; :68 is a comment):
  LATCHED   :403 (the width helper, per-instance d->warned), :425 (beyond-reg-space read),
            :630 and :635 (IPL's two #119 statics)
  UNLATCHED, GUEST-DRIVABLE BY AN ORDINARY BYTE WRITE, and fatal() so -q cannot silence:
            :439 CHIPID/CHIPREV  "IGNORING write to read-only ..."   -- every write
            :463 VECBASE  HUH?   -- every byte write with idata & ~0xf0
            :483 PSCALEADJ       -- every byte write   *** the only one FILED ***
            :504 TxCTL    HUH?   -- idata & ~7
            :540 TxICR    HUH?   -- idata & 0xe0
            :564 SCCICR   HUH?   -- idata & ~0x1f
            :578 SCCTX    HUH?   -- idata & ~0x1f
            :592 SCCRX    HUH?   -- idata & ~0xdf
            :612 SCSIICR  HUH?   -- idata & ~0xdf
  UNLATCHED but not guest-drivable in a normal path: :267 (C040, filed pcc2c040kill),
            :370 (interrupt_common default), :678 (iack write)
`pcc2pscaleflood` is filed for ONE of the nine and names the class ("floodclass family").
**Eight siblings are unfiled**, seven of them inside the twelve arms this round rewrote.  The
carrier's own rule -- "when correcting a claim, grep for its siblings before calling it fixed"
-- applies to a FILING as much as to a correction.  The probe's `devsig` oracle is :439's
message, and it counts it at 1 after ONE byte write, so latching that site per the house idiom
(`(once)`) would NOT break the detector.
Note the probe already trips two of these itself: `acc all` stores 0x10 at every block, which
is `& ~7` at TxCTL and `& ~0x1f` at SCCICR/SCCTX.

## F15 (census completeness, checked) -- THE THIRTEENTH ARM CLAIM IS RIGHT, AND THE CENSUS CLOSES.
Every `case` in DEVICE_ACCESS(pcc2): CHIPID/CHIPREV (write prints, no idata read);
GENCTL, VECBASE, PSCALEADJ, TxCTL, TxICR, SCCERR, SCCICR, SCCTX, SCCRX, SCSIICR, IPL, MASK =
the TWELVE guarded; T1CMP/T2CMP/T1COUNT/T2COUNT = the raw `memcpy` (disclosed pcc2counter8);
SCCRXIACK :598-602 = the thirteenth, which reads neither idata nor len (it clears SCCRX's INT
bit and reasserts) -- width-invariant, correctly excluded.  `default:` :658-665 still exits
(disclosed pcc2defaultkill).  Note SCCRXIACK also runs on READS -- there is no writeflag test
-- so a debugger-visible read at 0x27 clears the bit; true of upstream, not a width matter.
`PCCTWO_SCCTXIACK` (0x25) has NO case at all and therefore reaches `default:` and exit(1) --
inside pcc2defaultkill's disclosed family.

## F16 (Q2 follow-up, and a structural recommendation) -- THE NOROW LINE IS TRUE AGAIN AND
## NOTHING ENFORCES IT.
`pcc2_width_probe.py:927-928` still prints "pcc2c040kill -- ... every GENCTL lane here keeps
that bit clear".  I re-derived every value the probe puts on GENCTL's byte:
  BYTE writes 0x82, 0x11, 0x10;
  WIDE lanes  0xbb, 0xb8, 0x03, 0x22, 0x01, 0xd9, 0x40 (and 0x03 at len 4 and 8).
All eleven have bit 0x04 clear, so the sentence is TRUE at this revision.  It was FALSE at the
previous one, for exactly two rows, and nothing in the file would have said so -- it is prose,
checked by a human, in a file that already carries two structural asserts (`assert len(name)
<= 15` and the duplicate-name assert) doing precisely this job for other invariants.
**Cheap structural fix, in the file's own idiom:** a helper that asserts `(lane & PCC2_C040)
== 0` for every value written to GENCTL, so a future lane change that reintroduces the bit
fails at probe-authoring time instead of killing two rows by host death and being read as a
value kill.  This is the round's own pass-7 finding turned into a check.

## Q1's THREE SUB-QUESTIONS, ANSWERED WITH A DENOMINATOR
* **"a static elsewhere?" YES.**  `DEVICE_ACCESS(pcc2)` contains exactly THREE function-statics
  -- :423 (`warned`, the beyond-reg-space read latch, ABOVE the switch, dominated by no width
  guard), :629 (IPL write branch -- the one the enumeration names), :634 (IPL READ branch).
  The enumeration names one of three and excludes neither of the other two by name.
* **"a bit no preset reaches?" YES, two.**  TxCTL OVF bits 5-7 (the ovf rows reach count 1
  only) and TxICR bit 2 (every preset is 0x13 / 0x11 / 0x10).  See F10.
  A THIRD of the same shape that the question's wording does not cover: `d->warned` is
  enumerated as the helper's lvalue with `rb2 *` as its channel, but `rb2 *` holds each arm's
  OWN bit and no row holds ANOTHER block's bit set at this arm's decision point.  That is the
  M_WARNX cell.
* **"an lvalue read through a macro?" NO -- checked, and the check is empty rather than
  unrun.**  The twelve bodies use only object-like CONSTANT macros (PCC2_TCTL_COVF,
  PCC2_TTIRQ_IEN/ICLR/INT, PCC2_C040 ...), which are not lvalue reads.  Every function-like
  macro in the file (CHECK_ALLOCATION, INTERRUPT_CONNECT, INTERRUPT_ASSERT/DEASSERT) is in
  DEVINIT or in the callee `reassert_interrupts()`, never in a guarded body.  Worth stating
  explicitly, because a body using `INTERRUPT_ASSERT(d->cpu_irq)` inline would hide
  `d->cpu_irq` from exactly the field-name walk that missed the IPL static in pass 6.
* Fully-held in-closure operands, for the denominator: `len` (all four widths: acc all=1,
  latch all=2, latch all w=4, latch all d=8), `writeflag` (both values; MEM_READ 0 /
  MEM_WRITE 1 per memory.h:117-118, closed by `hrd * nod` / `wrd sccerr nod`),
  `relative_addr` at BOTH two-label arms, `pending_timer1/2` (pend rows), TxCTL bits 0-1 and
  4, TxICR bits 0, 1, 4 and 5, IPL's write-branch static.

## WHAT CHECKS OUT (so the negatives are read as signal, not as a tone)
Every cited measurement I could open matches its claim:
  part3/driver.log   BASE 95/96 with `rb t1ctl` red -- the string-mismatch the contract
                     discloses -- and M_RDDECL_ALL 88/96 red on the seven `nod` rows + `hrd
                     ipl nod`, exactly the RDDECL closure the contract describes;
  part3b/driver.log  BASE 96/96 and M_GROW_PSCALEADJ **96/96** -- the `put b' vacuity,
                     measured, as claimed;
  part3c/driver.log  M_GROW_PSCALEADJ 95/96 with `acc all` ALONE red -- the guest-byte
                     rewrite, measured, as claimed;
  part7/driver.log   the five mutants with their diff counts (8 / 2 / 2 / 2 / 24 lines) and a
                     `assert len(a.findall(s))==12` denominator on the twelve-guard regex;
  gate14_p8.log      171 named row checks + 3 summary rows, PASS 737 checks, zero FAIL lines.
The driver is a proper scratch-clone driver (clone, cmp vs SEC, freeze the probe, per-mutant
diff proof, sentinel-checked probe output, restore-and-rebuild).  It never writes to build/.
The probe carries real structural guards (duplicate-name assert, `len(name) <= 15`).

## MEASURED: BASE = 171/171 (probe_BASE.txt, PCC2W_PROBE_DONE present)
    BASE|PCC2W_RESULT=171/171||sentinel=1
The control reproduces on the clone, so the mutants below mean something.

## F7 BOUNDED BY MEASUREMENT
The shipped probe (82c6a7c5) emits **171 row names**, and `gate_arm.sh:1295` lists **171**;
the symmetric difference is **ZERO**.  So the gate's 171 name checks would still pass against
the file that ships; what remains unmeasured is only the whole gate (737 checks) against
82c6a7c5, and the CHANGELOG sentence attributing that run to "the shipped ... instrument".

*** AND I HIT THE CARRIER'S OWN WRONG-SECTION TRAP DOING IT, WHICH IS WORTH RECORDING. ***
My first namecheck anchored on the list's own first names (`for v in "live"`) and matched a
DIFFERENT probe's row list in the same gate -- it reported 30 gate names and a 197-line
difference.  `gate_arm.sh` has several such loops, and the discriminator is the LOG VARIABLE on
the next line (`count "$PCC2LOG" ...`), exactly as this project's own rule says.  Re-anchored
on `$PCC2LOG` it resolves to line 1295 and the answer is 171/171/0.  A count check could not
have told the two apart.

## M_IPLR built and proven (diff_M_IPLR.txt, 8 changed lines against SEC)
    410a411  > static int w_r = 0;                     part 1, INERT (a declaration move)
    624c625  < if (len != 1 && writeflag == MEM_WRITE) {
             > if (len != 1 && writeflag == MEM_WRITE && !w_r) {     part 3, THE LIVE EDIT
    634,636c635,636  the READ branch's block static deleted, its two uses renamed w_r
                                                       part 2, INERT (a rename)
Build FRESH_OK.  Probe running.

## THE CLOSURE ASYMMETRY, which stands whatever M_IPLR measures
The enumeration counts **TxCTL's OVF nibble as IN closure** although the only thing that ever
writes it is `pcc_timer_tick()`, a different function entirely -- a WIDE reading of "the lvalue
the guarded body reads".  At IPL it takes a NARROW reading, excluding `reg[IPL]` because it is
read by "the IPL arm's READ branch" rather than by its write body.  **Those two readings cannot
both be the rule**, and the second one is what makes the arm's second function-static
invisible.  This is independent of the measurement: either the read branch is inside the
guarded body (and the second static is an unrowed in-closure cell) or it is not (and the second
static owes a disclosure beside `reg[IPL]`'s).  The round has done neither.

## CHEAP CLOSURES I CAN NAME PRECISELY (each zero or one extra session)
* **The second IPL static: ZERO new sessions.**  Prepend one instruction to `ipl wset`:
  `program([LD_BU(4, IPL), ST_B(5, IPL), ST_H(6, IPL)])`.  A BYTE read of IPL at init has
  `reg[IPL] == 0`, so it fires the read latch; the byte write fires the write latch; the wide
  write is then declined with BOTH statics set.  `ipl wset` still wants DECL == 1 (the read
  branch's message is not a DECL), so the row's oracle is unchanged and it now kills M_IPL_W
  and M_IPLR together.
* **The cross-bit latch cell: ONE new session, and it closes ALL 132 ordered pairs.**  Add
  `latch all rev` -- the twelve wide writes in REVERSE BLOCKS12 order, DECL 12.  A qualifier at
  arm A naming arm B's bit is killed by the forward `latch all` when B precedes A and by the
  reverse one when B follows A; together they cover every (A, B) pair.  The forward row alone
  leaves the FIRST block (GENCTL) covered by nothing, which is why M_WARNX picks GENCTL.
* **TxICR bit 2: ZERO new sessions.**  Change the TxICR preset from 0x13 to 0x17 (see F10).

## F17 -- THE FOREIGN-LATCH-BIT CELL WAS FOUND, MEASURED AND CLOSED IN THE **SIBLING ROUND**
## IN THIS SAME WORKING SET, AND NOT CARRIED ACROSS.
`regress/sgi_de_primop_probe.py` (round `#500`, uncommitted in the same tree, 20 insertions in
today's working set) says, at :621-630, verbatim:

    *** SECOND DRAW ADDED: the LATCH-FIELD axis had the same empty 2x2 cell as the
    operand axis, and a seat flagged it as a softer claim while being right. ***
        NO session both PRE-SET a foreign d->warned bit AND drew twice.
        xlatch all pre-set bits 0-8 and drew ONCE;  dec flood drew twice and
        pre-set NOTHING.  So || (d->warned & SGIRE_W_DE_LEN) -- a predicate on the
        guard's OWN field, squarely inside (d) -- bypassed the latch and flooded,
        and every row stayed green.
    One extra draw closes it: ...

and at :149-156 it downgrades its own latch-field closure in the contract:

    latch-field bits  0-8 by `xlatch all'; 9 is the latch itself.  (DERIVED,
                      not mutant-measured: no `|| (d->warned & bit)' cell was
                      ever built.  Pass 16 named it; filed.  An unmeasured
                      closure must not render like a measured one.)

**pcc2's contract states the same closure flatly** -- "helper reads d->warned: `rb2 *` (latch
SET)" -- with no foreign-bit qualifier, no foreign-bit row, and no disclosure.  The two
detectors are in one working set, edited on one day, by one campaign; the sibling calls the
predicate "squarely inside (d)" and pcc2's says nothing.
That is this project's own finding about itself: knowledge present in the tree, unconsulted at
row-writing time.  It also settles M_WARNX's PLAUSIBILITY question by precedent rather than by
my judgement -- the foreign-bit predicate on the guard's own latch field is an adjudicated
clause-(d) cell in this repo as of today.
(The two shapes are duals: sgi's `|| (warned & foreign)` bypasses the LATCH and floods; mine,
`&& !(warned & foreign)` at the GENCTL guard, bypasses the GUARD and lands the write.)

## F17 (cont.) -- THE CLASS IS FILED BUT HAS NEVER BEEN MEASURED ANYWHERE IN THIS REPO.
`OUTSTANDING_BUGS.md:14644-14647`, item 1 of `sgideprimopstrengthen`:

    1. **The latch-field closure is derived, not measured.**  The contract says bits 0-8 are
       closed by `xlatch all`, and in twenty-eight mutants across every table no
       `|| (d->warned & SGIRE_W_UNMAP_WR)` cell was ever built.  One cell.

So across `#500`'s twenty-eight mutants and `pcc2widthkills`'s seven tables, the foreign-latch-
bit cell has **never been built**.  `#500` filed it (correctly -- its chain had CLOSED, and
shipping a row would have made new floor-bound material) AND corrected its contract to say the
closure is derived.  `pcc2widthkills` has done neither, and its chain is OPEN.

DISPOSITION I would argue for, whatever M_WARNX measures:
* **L4, mandatory**: pcc2's contract must carry the sibling's qualifier -- `rb2 *` closes each
  arm's OWN bit, and the foreign-bit form is derived, not measured.  "An unmeasured closure
  must not render like a measured one" is the sibling probe's own sentence, in this tree.
* **If M_WARNX sweeps clean**: it is a clause-(d) mutant on an operand the contract ENUMERATES
  and claims closed, on a chain that has NOT closed -> L2 by the floor, fix in-round.  The
  sibling escaped that conclusion by having already closed, not by the cell being out of
  closure -- it calls the predicate "squarely inside (d)".
* The fix is ONE session (`latch all rev`) and it closes all 132 ordered (arm, bit) pairs
  together with the existing forward `latch all`.  The sibling round should get the same row.

## F18 (THIS PASS'S OWN ROSTER) -- THE KIMI SUBSTITUTE ANSWERED AND THE SEAT CHECK RECORDS
## THE SEAT AS LOST.
`_scratchpad/panel_20260904_063019/SEATS.txt` says:
    kimi(sub)  WITHDRAWN -- the CLI is the kimi seat (owner directive 2026-08-29).
    SEATS: 5/6 scriptable produced output -- no answer from: kimi
    NOTE: ... so this seat is LOST rather than covered.
**`ollama_kimi.txt` in that same directory is 4,729 bytes, written 06:36, and is a
substantive, verdict-first review.**  So the substitute WAS fired and DID answer; the seat is
COVERED, not lost, and the panel is EIGHT answering of nine with agy deliberately not fired --
not 5/6 with kimi lost.  This is the sixth seat-failure class inverted: not a live seat
recorded as down, but a live ANSWER recorded as absent -- an UNREAD REVIEW, which this project
has twice found real defects sitting in.
**It matters for THIS pass specifically**, because roster completeness is one of the closing
zero's validity conditions, and the seat check would have had a closing pass believe a seat
was lost while its answer sat unread beside it.

## F19 -- AND THE UNREAD ANSWER INDEPENDENTLY REACHES F10 AND F6, FROM THE PACKET ALONE.
Its verdict: *"TxCTL bits 5-7 are held non-initial by NO listed row -- the 'bits 4-7' claim is
false of its own cited rows"* (= my F10, reached from the packet's own numbers while I reached
it from `pcc_timer_tick`), and *"the 'bits 0-4 by presets' claim for TxICR is contradicted by
the packet's own write mask (bit 3 not writable)"* (= my F6).  Two seats, two routes, same two
defects.
**And it found a THIRD instance of the same shape that I had not: `pending_timer1/2`.**  The
`pend*` rows arm compare=1, count=0, CEN without COC, so exactly ONE interrupt is pending when
the wide write happens; a guard `&& d->pending_timer1_interrupts < 2` is in closure and escapes.
So the pattern generalises: **every in-closure operand's coverage is CLAIMED at lvalue
granularity and HELD at one bit or one value** -- TxCTL (bit 4 of 4-7), TxICR (bits 0,1,4 of
0,1,2,4 + bit 5), pending (the value 1), d->warned (the arm's own bit of twelve).

### I adjudicate two of its five points AGAINST it, having the source it did not:
* Its point 2 (TxCTL/TxICR **bit 1** undriven) is **REFUTED**: it reasoned from the LANE values
  0xdd/0x44 and the presets are 0x03 (TxCTL: bits 0 AND 1) and 0x13 (TxICR: bits 0, 1, 4).
  Bit 1 is driven at both arms.  The seat flagged its own uncertainty honestly ("if some preset
  writes 2/3/0xff ... the claim stands").
* Its point 4 (no `rb2` row at t1ctl, t1icr, ipl, sccerr, pscaleadj) is **answered by the
  block-vs-label distinction the contract already makes**: `d->warned`'s bit is per BLOCK
  (`PCC2_W_TXCTL_LEN` / `PCC2_W_TXICR_LEN`), so `rb2 t2ctl` / `rb2 t2icr` pin the T1 labels'
  guard too; `pscale noig2` and `ipl noig2` are the print-only arms' equivalents; SCCERR is E.
  Coverage there is complete.

## F20 -- THE TxCTL BYTE HAS A **THIRD WRITER**, INSIDE THIS DEVICE, EIGHT LINES ABOVE THE
## TxCTL ARM, AND THE ENUMERATION NAMES TWO.  (This supersedes half of F10 -- see below.)
`dev_pcc2.c:468-475`, the counter arm:

    case PCCTWO_T1CMP: case PCCTWO_T2CMP: case PCCTWO_T1COUNT: case PCCTWO_T2COUNT:
        if (writeflag == MEM_WRITE && relative_addr + len <= PCC2_SIZE)
            memcpy(d->pcctwo_reg + relative_addr, data, len);

`PCCTWO_T2COUNT` is **0x10**.  An 8-byte write there memcpy's `0x10..0x17` -- **which includes
T2CTL (0x16) and T1CTL (0x17)** -- with no width guard, no mask and no bit filtering.  And
`0xfff42010` is 8-ALIGNED, so this is reachable by a GUEST `st.d`, not only by `put d`.
(Derived, not assumed: the four counter offsets are 0x04/0x08/0x0c/0x10 and their len-8 spans
are 0x04-0x0b, 0x08-0x0f, 0x0c-0x13, 0x10-0x17.  Only the last reaches a guarded register, and
it reaches BOTH TxCTL labels.  T2ICR 0x1a / T1ICR 0x1b are beyond every span.)

**Three consequences, and the third corrects me:**
1. **The enumeration's TxCTL bit-domain is wrong in a SECOND way.**  It lists bits 0-1 (byte
   presets) and 4-7 (the tick).  **Bits 2-3 are omitted and are reachable**, so
   `&& !(reg & 0x0c)` at TxCTL is in closure and escapes all 171 rows.
2. **It settles the packet-fed seats' open question, which none of them could.**  glm,
   deepseek and minimax all flagged TxCTL bits 2-3 / TxICR bits 6-7 and each said explicitly
   that reachability was "not checkable from the packet".  From the source: **TxCTL 2-3 are
   REACHABLE (this memcpy) -> real escape; TxICR bits 3, 6 and 7 are UNREACHABLE (mask 0x17,
   reassert ORs only 0x20, and no memcpy span reaches 0x1a) -> equivalent by construction,
   their claims REFUTED.**  Three of the four "missing bit" families are equivalent; one is
   real.
3. *** THIS SUPERSEDES MY OWN F10 REMEDY.  Do not use the earlier sentence. ***  F10 said
   TxCTL bits 5-7 cost "~2147 s of host time" per extra overflow.  That is true only of the
   TICK path.  Through the counter memcpy the WHOLE BYTE is settable instantly:
   `put d 0xfff42010, 0x000000000000fcfc` leaves T2CTL = T1CTL = 0xfc -- bits 2-7 set, CEN and
   COC CLEAR so no timer runs and no free-running is needed -- and then a wide write of 0xaabb
   to T2CTL is declined (readback 0xfc) on the fix and lands 0xfc | (0xbb & 3) = 0xff under
   `&& !(reg & 0x0c)` or `&& !(reg & 0xe0)`.  **ONE stepping session closes TxCTL bits 2-7 at
   both labels**, replacing the two expensive free-running rows I proposed.
   (Choose the lane for its `& 3`: 0xaab8 gives 0xb8 & 3 = 0 and would read back 0xfc either
   way -- the same preset-collision trap part 6 already hit with 0x33.)

## F20 (cont.) -- AND THE ROUND FOUND THIS ON **PASS 1** AND FILED IT.
`OUTSTANDING_BUGS.md:14576-14585`, `pcc2counter8`, filed by the codex seat on the pass-1 panel:

    An 8-byte write at `T2COUNT (0x10)` raw-copies through `PSCALE (0x14)`, `PSCALEADJ (0x15)`,
    `T1CTL (0x16)` and `T2CTL (0x17)` -- bypassing the per-register write semantics those arms
    implement (masks, read-modify-write, COVF clear, `reassert_interrupts`).
    **A guest can set timer control bits through a path that skips their arm.**

So the third writer of the TxCTL byte was **identified on pass 1 and written down**, and the
pass-6/7 bit-domain enumeration -- whose whole job is to ask *what can put this lvalue in a
non-initial state* -- was written six passes later naming only the presets and the tick.  This
is not an obscure miss; it is this project's own documented failure mode: knowledge present in
the tree, unconsulted at the moment the enumeration was written.  It is the third instance I
found today (with F17's sibling-probe latch note and the pass-1 kimi answer the pass-7 record
already cites).
*(One correction to that filed item, derived from `mvme_pcctworeg.h:26-27`: it names 0x16 as
T1CTL and 0x17 as T2CTL.  They are the other way round -- `PCCTWO_T2CTL 0x0016`,
`PCCTWO_T1CTL 0x0017`.  The substance is unaffected; both are reached.)*

## Q4 -- THE SMALLEST EDIT.  The best answer is ONE TOKEN inside a mutant THIS ROUND ALREADY
## BUILT AND KILLED.  *** DERIVED, NOT MEASURED -- I say so rather than let it read like the
## two I did build. ***
Pass 7 built `M_TXCTL_OVF`: `&& !(d->pcctwo_reg[relative_addr] & PCC2_TCTL_OVF)` at the TxCTL
guard.  It scored **167/171** (ovf1/ovf2 decl+rb red).  Change the identifier to its neighbour
in the same header --

    PCC2_TCTL_OVF  (0xf0)   ->   PCC2_TCTL_COVF  (0x04)
    mvme_pcctworeg.h:101-102, adjacent lines

-- and I predict **171/171, a clean sweep**, because TxCTL register bit 2 is written by nothing
any row does: the arm sets only bits 0-1 (`|= idata & 3`), the tick sets only 4-7 (`|= oc << 4`),
and the third writer (F20's counter memcpy) is used by no row.  The arm's `if (idata & COVF)`
branch READS bit 2 of *idata*, never of the register, and the register's bit 2 is only ever
CLEARED (`&= ~(OVF|COVF)`).
It is the round's own ALIAS cell ("one enum member for two blocks") wearing the qualified-guard
hat, and it is the most plausible edit I found: a one-identifier slip between two adjacent
constants, inside a predicate the round has already demonstrated is a live (d) shape.
**Rows I expect to stay green: all 171, and specifically the four the parent mutant killed** --
`ovf1 decl`, `ovf1 rb`, `ovf2 decl`, `ovf2 rb` -- because those rows hold bit 4, not bit 2.
Closure: the same single session F20 names (`put d 0xfff42010, 0x000000000000fcfc`, then a wide
write of 0xaabb to T2CTL, then read back) kills COVF, OVF-subset and bits-2-3 forms together.

## DISPOSITION SUMMARY (my recommendation as a seat; the adjudicator decides)
  F1   until='n', the free-running repair is INERT      MEASURED   L2/L4  FIX IN-ROUND (1 line)
  F2   SIGKILL reported as how="exit0"                  MEASURED   L4     fix in-round (2 lines)
  F3   8 of 12 free-running rows fail silently          READ       L3     fix in-round (1 helper)
  F4   "seven arms read nothing" -- all read idata      READ       L4     correct in place
  F5   IPL's SECOND function-static unnamed             MEASURED*  L2/L4  see M_IPLR
  F6   TxICR "bits 0-4" (mask is 0x17)                  READ       L4     correct in place
  F7   gate cited md5 != shipped md5                    MEASURED   L4     correct; names bounded
  F8   part7/7b as-run scripts carry PASS-2 headers     READ       L4     correct in place
  F9   brief premise 8 repeats pass 7's own miscount    READ       L4     correct in place
  F10  bit-domains claimed at lvalue, held at one bit   READ       L4+debt correct; 1 session closes
  F11  no hang in waitpid; one unbounded os.write left  READ       note
  F12  BREAKPOINT token correct (fatal(), no early-out) READ       -- confirms the round
  F13  value-coverage list understates its own rows     READ       L4     safe direction
  F14  8 unfiled floodclass siblings in this file       READ       FILE
  F16  the NOROW C040 sentence is unenforced prose      READ       structural suggestion
  F17  foreign-latch-bit cell closed in SIBLING probe   READ       L4     carry the qualifier
  F18  kimi substitute ANSWERED; seat check says LOST   READ       roster defect, this pass
  F19  that unread answer independently found F10, F6   READ       corroboration + 1 new (pending)
  F20  TxCTL's THIRD writer, filed on pass 1, omitted   READ       L4 + floor question
  Q4   PCC2_TCTL_OVF -> PCC2_TCTL_COVF, one token       DERIVED    predicted 171/171, NOT measured

## THE THREE INSTRUMENT FIXES, WRITTEN OUT (all small, all in pcc2_width_probe.py)
F1, at :381-384 -- compute `until` BEFORE rebinding `c`:
        until = None
        if isinstance(c, tuple):        # (cmd, wait[, until])
            until = c[2] if len(c) > 2 else None
            c, w = c[0], c[1]
    (or the one-liner `c, w, until = c[0], c[1], (c[2] if len(c) > 2 else None)` -- the RHS
    tuple is fully evaluated before any name is rebound, so it is safe.)
    NEGATIVE CONTROL, and it is cheap because the "before" is already measured: the same
    instrumented copy must print `until='BREAKPOINT'` and a NON-ZERO wait after the fix, where
    today it prints `until='n'` and `0.000 s`.
    Say in the record that the fix RESTORES the ceiling: four free-running rows may now each
    wait up to 20 s on a starved host, where today they wait ~0.  That is the intended
    behaviour and it is a real change to gate 14's worst-case time.

F2, at :406-427 -- the `for/else` must not leave `stat` holding the WNOHANG sentinel:
    in the else branch set `stat = None` before `how = "killed"`, REAP after the kill
    (`os.waitpid(pid, 0)` in a try) so no zombie is left, and guard the
    WIFSIGNALED/WIFEXITED block so it cannot overwrite `how` with "exit0".

F3, at :722-765 -- one helper for ALL TWELVE free-running rows, not four:
        def freeval(t, alive, f):
            if not alive: return "died"
            if "BREAKPOINT" not in t: return "no-breakpoint (FAILED FOR SOME OTHER REASON)"
            return f()
    and wrap the four `* decl` counts and the four `* rb` readbacks in it, exactly as the four
    `* arm` rows already are.  A string token against an int `want` still fails, so the row
    oracles are unchanged.

## *** MEASURED: M_IPLR = 171/171.  A TOTAL CLEAN SWEEP, AS PREDICTED. ***
    BASE  |PCC2W_RESULT=171/171||sentinel=1
    M_IPLR|PCC2W_RESULT=171/171||sentinel=1      (no PCC2W_RED line at all)
Logs preserved here: probe_BASE.txt, probe_M_IPLR.txt, diff_M_IPLR.txt, TABLE.txt, driver.log.
Prediction written 06:41:22 in PRETABLE_pass8_opus.out; first mutant build 07:04:13.

**So the IPL arm's SECOND function-static, read by a width guard, is invisible to the entire
171-row detector.**  It is the SAME class pass 7 ruled **L2, in closure** -- "state no row holds
non-initial at a wide write" -- at the SAME arm, found on the very next pass, inside the
sentence the round rewrote to close that class.  Pass 7's own M_IPL_W (the WRITE-branch static)
scored 170/171 and was killed by `ipl wset`; its twin nine lines below scores 171/171.
The round's stated closure boundary decides the LABEL, not the fact: if the guarded body
includes the branch its `break` skips, this is an unrowed in-closure cell (L2, fix in-round);
if it does not, it is an UNDISCLOSED out-of-closure cell that owes a sentence beside
`reg[IPL]`'s.  Either way the enumeration named one of the arm's two statics and the detector
cannot see the other.  Closure cost: ZERO new sessions (prepend `LD_BU(4, IPL)` to `ipl wset`).

## M_WARNX built and proven (diff_M_WARNX.txt, 3 changed lines against SEC)
    445c445,446
    < 		if (len != 1 && writeflag == MEM_WRITE) {
    ---
    > 		if (len != 1 && writeflag == MEM_WRITE &&
    > 		    !(d->warned & (1u << PCC2_W_MASK_LEN))) {
The GENCTL width guard qualified by MASK's latch bit -- the pass-5 canonical
`&& !(d->warned & (1u << bit))` with ONE token changed.  Build FRESH_OK.

## RESTORE DISCIPLINE, as run (driver.log, verbatim)
    [07:16:51] M_IPLR: PCC2W_RESULT=171/171   sentinel=1
    [07:16:51] restore CMP CLEAN against SEC
    [07:16:52] restore build FRESH_OK
    [07:16:52] sentinel cleared (source cmp-clean AND binary rebuilt newer)
Each mutant is restored FROM SEC (never from a backup), cmp'd, REBUILT, and only then is the
sentinel cleared -- the two-part clearance, run rather than asserted.

## *** FINAL TABLE -- BOTH MUTANTS SWEPT CLEAN, BOTH PREDICTED ***
    BASE   |PCC2W_RESULT=171/171||sentinel=1        control reproduces
    M_IPLR |PCC2W_RESULT=171/171||sentinel=1        TOTAL ESCAPE, predicted 171/171
    M_WARNX|PCC2W_RESULT=171/171||sentinel=1        TOTAL ESCAPE, predicted 171/171
Neither run emitted a PCC2W_RED line.  All three carry PCC2W_PROBE_DONE.
Predictions PRETABLE_pass8_opus.out mtime 06:41:22; first mutant build 07:04:13; last
mutant build 07:16:53.  Two of two predictions held exactly.
Clone finished CLEAN: no `.MUTANT`, `dev_pcc2.c` cmp-clean against SEC, binary FRESH.
GXEMUL-SEC, build/, est/ and build-asan/ were never written.
Logs in this directory: probe_BASE.txt, probe_M_IPLR.txt, probe_M_WARNX.txt,
diff_M_IPLR.txt, diff_M_WARNX.txt, TABLE.txt, driver.log, f1_err.txt, f1_out.txt,
PRETABLE_pass8_opus.out, driver.sh, mutate.py, namecheck.sh.

## POST-RUN CHECK (added after the report; nothing in the findings changes)
`ps -ef | grep -c "[g]xemul"` returned 3, then 2.  **None of them is mine.**  The two real ones
are the MAIN LOOP's own part-8 table -- `/tmp/killpcc2b8/frozen_probe.py /tmp/gxpcc2b8/gxemul
BASE`, started ~08:03 and still on BASE at 08:16:56.  My clone is `/tmp/gxopus_p8`; nothing
references it.  So my run leaked no emulator, and F2's zombie point stays a code-reading
observation, not an observed leak.

TIMING: my table ran 06:51:34 -> 07:29:29 (probe_M_WARNX.txt mtime 07:29:27); the main loop's
started ~08:03 (killpcc2b8/BASE.out 08:16:56).  **No overlap**, so neither measurement was
taken under the other's load -- which matters here, because F1 means the four free-running rows
have essentially no wait budget and are exactly the rows a loaded host would red.

*** AND MY OWN PROCESS CHECK MATCHED ITSELF, which is the trap this project documents. ***
`ps -eo pid,ppid,stat,etime,args | grep "[g]xopus_p8"` returned ONE hit: the `bash -c` running
that very grep, because the pattern is in the checking command's own argv.  The bracket trick
protects against matching the *grep*, not against the pattern appearing in the wrapper.  The
answer that actually settled it was reading the ARGS column of the surviving processes and
seeing `/tmp/gxpcc2b8`, a different clone.
