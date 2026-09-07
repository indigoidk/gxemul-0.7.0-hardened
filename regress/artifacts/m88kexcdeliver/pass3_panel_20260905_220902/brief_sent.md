# ADJUDICATION PASS (§F2) -- `m88kexcdeliver` (#502, HIGH): the panel SHARES its pass-2 findings.  Tree `GXEMUL-SEC/src/`, HEAD `83df95c` + the UNCOMMITTED round (diff to cpu_m88k.c 63+/12-: the seven-class delivery fix, comments corrected per pass 2; new `regress/m88k_exc_probe.py` v3 (22 fault rows + 2 controls); gate 11 wiring).  2026-09-05, ~23:05.

## CONTEXT AND VOCABULARY
An ordinary correctness review of an open-source machine emulator's CPU model (GXemul 0.7.0, hardened fork): the MC88100
exception-delivery path in `cpu_m88k.c`.  The "guest" is the operating system inside the emulator.  Plain engineering vocabulary
("the emulation stops", "the exception is delivered").  Read the project's own records NARROWLY (grep anchors, a few lines of
context; never whole CHANGELOG blocks or the ledger) and paraphrase in neutral terms.

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY
A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.  **Check the premises, not just the
derivations.**  THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`; three pristine-2021-upstream copies sit under the project root and are
NOT this fork.  **If you cannot read files that is expected** -- every fact you need is inlined; name any premise you cannot settle
rather than guessing.  ENUMERATE arithmetic rather than reasoning about it.  **VERDICT LINE FIRST.**  Cite by grep anchor.

**THIS IS A THIRD PASS, not another review.**  Until 2026-08-30 every seat answered blind to the other eight and the main loop
arbitrated alone.  Below is every seat's pass-2 finding, numbered, WITH THE MAIN LOOP'S DISPOSITION and what changed as a result;
the disagreements separately; and what is still owed.  **Three questions**: (1) adjudicate F1..F24 and D1..D3 -- UPHOLD / OVERTURN
/ REFINE / CANNOT SETTLE, one line each with a reason; (2) WHICH OF MY ACCEPTED DISPOSITIONS IS WRONG?  I accepted 21 of 24
findings and repaired the detector on 13 of them in one evening -- that is a suspicious number and agreement is not evidence;
(3) WHAT DID ALL NINE OF US MISS?  A seat re-reading its OWN finding is doing self-review: be HARDER on it, and check that the
REPAIR is right, not only that the finding was.  This pass is also the REPAIR's pass 2 (the v3 probe is new floor-bound material):
the chain closes on the first VALID pass finding zero floor breaches -- so state your denominator: which cells / mutant shapes you
swept and found closed.

## 1. SETTLED PREMISES (re-inlined; each a QUESTION if you can check it)
* The fix: seven trap-like classes (MISALIGNED 4, UNIMPLEMENTED 5, PRIVILEGE 6, BOUNDS 7, ILLEGAL_DIVIDE 8, OVERFLOW 9, ERROR 10)
  gain `implemented = true` at VERBOSITY_INFO in switch 1 of `m88k_exception()` AND bare `case` labels in the tail switch; the
  fallback (`vector < 128 && !implemented` -> stop every CPU) and the tail `default:` are untouched.  Product lines unchanged
  since 16:16; ONLY the two comments changed at 23:00 (F19-F22 below).
* Two routes into switch 1: INSTRUCTION faults (is_trap 0) and supervisor `tb0/tb1/tcnd` naming any vector (is_trap 1; the
  user-mode filter in X(tb0) raises PRIVILEGE with is_trap 0).  The SFRZ re-route (`if (SFRZ) { if (!is_trap) vector = ERROR; ...
  update_shadow_regs = false; }`) runs AFTER switch 1.  BOUNDS (7) has no instruction raise site (`tbnd` undecoded, row m88ktbnd);
  ERROR's switch-1 arm is reached only by a trap naming 10.
* MEASURED, all logs in `regress/artifacts/m88kexcdeliver/` (untracked until the commit): HEAD 0/9 (probe2_head.out), 0/10
  (probe10_head.out); the fix 9/9 -> 10/10 -> 22/22 (probe_v3_fix.out, 21:52).  TABLE 1 (13 mutants, 9 rows): 12 killed, M_LEVEL
  survived (then thought unobservable), M_ERRORDROP ESCAPED 9/9.  TABLE 2 (errortb added): M_ERRORDROP 9/10, M_ERRORTAIL 8/10,
  M_REVERT1 9/10.  OPUS SEAT (pass 2, 15 mutants, 10 rows): M_NOVBR, M_SFRZTRAP, M_SFIPNOTGT, M_DSLOTSWAP, M_DELAYALWAYS, M_TAILOFF
  all 10/10 ESCAPED; M_ISTRAPBOUNDS 10/10 EQUIVALENT; M_MODECOND 3/10, M_VEC7 5/10, M_EPSRAFTER 0/10, M_IMPLOVF 9/10 killed.
  TABLE 3 (v3 probe, 22 rows, frozen md5 28302f55, 21:54-22:04, clone clean before and after, BASE 22/22 both ends):

      M_ISTRAP      17/22  killed: misaligntb unimpltb div0tb ovftb privsuptb (HALT)
      M_NOVBR       21/22  killed: vbrtb (STOP -- pc 0x38, entry 0x2038)
      M_SFRZTRAP    21/22  killed: trapfrozen (STOP -- re-routed to 0x50)
      M_SFIPNOTGT   21/22  killed: dslot bad=sfip          M_DSLOTSWAP  21/22  killed: dslot bad=snip,sfip
      M_CARRYCLR    21/22  killed: ovfc bad=psr            M_LEVEL       3/22  killed: 19 rows bad=level
      M_DELIVERALL  20/22  killed: resid50 TAILHALT, sfu1h STOP (the negative controls)
      M_TAILLE      21/22  killed: usertb TAILHALT         M_TRAPONLY   22/22  EQUIVALENT (disclosed: no instruction raises 7)
      M_REVERT       3/22  M_ERRORDROP 21/22 (errortb)     M_DSLOT 21/22 (dslot)     M_NAIVE 3/22
  (3/22 = the two HALT-expected controls + usertb, which the fallback never touched.)
* The v3 rows: div0 ovf misalign bounds priv privtb unimpl error dslot errortb | misaligntb unimpltb div0tb ovftb privsuptb (trap
  routes) | vbrtb (VBR=0x2000, entry 0x2038) | trapfrozen (div0 handler = tb1 naming 7 with SFRZ set -> 0x38, shadows frozen) |
  ovfc (PSR C set before the overflowing add -> 0x9000000b) | udiv0 (user-mode divu by zero -> vector 8) | usertb (tb1 naming 128
  -> 0x400) | resid50, sfu1h (EXPECT HALT) | live, attrib.  dslot now uses br.n +16 (SNIP 0x1000e, SFIP 0x10016 -- two DIFFERENT
  numbers).  Every DELIVER row also asserts no `exception <CLASS>` line in the free-running transcript (the LEVEL channel).  The
  probe exits non-zero on any failure.  Gate 11 pins `M88KEXC_RESULT=22/22`, the two controls, resid50/sfu1h HALT, vbrtb at 0x2038,
  trapfrozen at 0x38, ovfc PSR 0x9000000b, and no bad=level.

## 2. THE FINDINGS, NUMBERED, WITH DISPOSITIONS
F1 (grok, deepseek, glm-mini -- independent) `if (!is_trap) implemented = true;` for classes 4/5/8/9 escapes the 10-row probe.
   ACCEPTED -> four trap-route rows misaligntb/unimpltb/div0tb/ovftb; M_ISTRAP killed 17/22.
F2 (codex, glm-mini) the same for PRIVILEGE: privtb arrives with is_trap 0 (the user-mode filter), so `implemented = !is_trap` on
   the PRIVILEGE arm leaves priv AND privtb green.  ACCEPTED -> row privsuptb (supervisor tb1 naming 6); M_ISTRAP extended to 5
   classes, killed.
F3 (Opus, MEASURED 10/10; kimi, Fable independently) `cpu->pc = 8 * vector` (VBR dropped) invisible: no row sets VBR.  L2 + L4
   (comment and contract claimed VBR).  ACCEPTED -> row vbrtb (stcr r5,cr7 = 0x2000 then tb1 naming 7; entry 0x2038); M_NOVBR
   killed 21/22; contract split into "wrong scaling (M_VEC4/M_VEC7)" and "dropped base (vbrtb)".
F4 (Opus, MEASURED 10/10; Fable, kimi) `if (!is_trap)` -> `if (true)` in the SFRZ re-route: the (SFRZ set, is_trap 1) cell empty;
   manual :8633-8636 / 6.10 :10613 / :9290-9294 make it load-bearing (a syscall from a frozen handler would become ERROR).  L2.
   ACCEPTED -> row trapfrozen; M_SFRZTRAP killed 21/22.
F5 (Opus, MEASURED 10/10 twice; codex, kimi) dslot's SNIP and SFIP expectations were ONE number (0x1000e): the SFIP channel
   vacuous by construction (L3).  ACCEPTED -> br.n +16 (SFIP 0x10016 != SNIP 0x1000e; an assert in the probe refuses a
   collapsed geometry); M_SFIPNOTGT and M_DSLOTSWAP killed.
F6 (Opus, codex, kimi, Fable -- four seats) F14 of pass 1 was WRONG: the exact PSR compare pinned carry only at its pre-fault
   value 0, never "unchanged".  ACCEPTED -> row ovfc (stcr r5,cr1 = 0x90000002 before the overflowing add; expect 0x9000000b);
   M_CARRYCLR (`(PSR & ~M88K_PSR_C) | ...`) killed 21/22.
F7 (Fable) "no row can observe the level" is FALSE: main.c lowers every subsystem to WARNING after startup, so an ERROR-level
   `[ exception <CLASS>: ]` line prints in the free-running transcript and INFO does not.  ACCEPTED -> the LEVEL channel on every
   DELIVER row; M_LEVEL killed 3/22 (19 rows bad=level).  The pass-1/2 "disclosed as unobservable" record is CORRECTED, not kept.
F8 (codex) tail guard `<` -> `<=`: vector 128 enters the tail default and stops; no row used an already-delivered vector.
   ACCEPTED -> row usertb (tb1 naming 128 -> 0x400); M_TAILLE killed 21/22.
F9 (kimi) NO NEGATIVE-CONTROL rows: the probe could not tell the shipped D1 form from the rejected D4 (tail default delivers) or
   from delivering SFU1.  ACCEPTED -> rows resid50 (tb1 naming 50: EXPECT HALT) and sfu1h (div0 handler = a legal divu with SFD1
   set -> SFU1 -> EXPECT HALT); M_DELIVERALL (fallback disabled) killed 20/22 on exactly those two.
F10 (Fable 9b, codex) "one user-mode divu by zero ended the emulation" was DERIVED, not measured (div0 is supervisor).
   ACCEPTED -> row udiv0 (stcr user mode, divu by zero -> vector 8 not SFU1); comment now cites div0/udiv0.
F11 (Opus) M_DELAYALWAYS (post-delivery `cpu->delay_slot` else-branch unpinned) 10/10 -- clause-(e) debt, needs a second
   UNFROZEN exception (a real new session).  ACCEPTED as DISCLOSED in the contract; FILED (m88kexcdebt).
F12 (Opus) M_TAILOFF (tail switch gated `< MISALIGNED`) 10/10 -- no rows for vectors 0..3 whose tail arms do real work.  Fable:
   equivalent BY CONSTRUCTION for the seven (bare breaks); Opus: escape because vectors 0..3 unrowed.  ACCEPTED as disclosed +
   FILED (m88kexcdebt: rows for vectors 0..3 = a different round: the hardware-event arms).
F13 (Opus, Fable, kimi) M_ISTRAPBOUNDS / M_TRAPONLY (`implemented = is_trap` at BOUNDS) EQUIVALENT today: no instruction raises 7.
   ACCEPTED -> measured 22/22 in table 3 and DISCLOSED with its warrant (m88ktbnd re-runs it).
F14 (Fable finding 1; codex; grok) THE DELAY-SLOT ELSE-ARM IS ARCHITECTURALLY WRONG: manual pointer definitions :2097-2104,
   :4207-4208, :8898-8902, Table 6-3 -- for a fault in the slot of a taken br.n, NIP = target, FIP = target+4; the fork sets
   SNIP = pc+4, SFIP = delay_target ("Perhaps something like this could work" -- upstream's guess).  X(rte) then executes slot+4
   (skipped by the branch) before the target, or the target twice when target == slot+4.  Pre-existing; made reachable by
   ordinary faults by this fix; the diff's comment CERTIFIED it as the contract; table 1's M_DSLOT "kill" produced the MANUAL's
   value (0x10012).  DISPOSITION: do NOT hold the fix (a wrong SFIP in one sub-case beats stopping every CPU; different semantic
   class, untouched code -> its own round by the reopening rule); L4 in-round: comment reworded ("OUTSIDE A DELAY SLOT ... INSIDE
   a delay slot the else-arm is upstream's guess and the manual disagrees, row m88kdslotshadow"); the dslot row LABELLED as
   pinning the arm AS IMPLEMENTED, held for re-pin under the oracle-correction rule when m88kdslotshadow lands; PRETABLE's "M_DSLOT
   (else-arm SFIP wrong)" corrected to "a change detector, not a correctness oracle".  FILED m88kdslotshadow MEDIUM (fix = the
   DATA_ACCESS arm's shape; rows dslot16 + dslotnt; re-pin first).  kimi DISSENTS in part (D1 below).
F15 (grok, Opus, kimi, glm-mini, codex, Fable -- six seats) the tail comment's "ERROR arrives here from the SFRZ re-route with the
   shadows frozen" is false as a universal (errortb: a trap naming 10, shadows updated).  ACCEPTED -> comment names both routes;
   also codex's point that SXIP then names the FIRST fault.
F16 (Opus, Fable) "6.8.3 and 6.6 say the destination register (and carry bit) are unchanged": 6.8.3 says nothing about carry.
   ACCEPTED -> "6.5.x/6.8.3 ... (6.6: and the carry bit, for the overflow case)".
F17 (Opus) the tail `default:` is now DEAD CODE for vectors < 128 (implemented = {0..10} = the tail labels).  ACCEPTED -> one
   sentence in the comment ("unreachable code kept as the tripwire for an eighth class").  M_NAIVE/M_ERRORTAIL re-arm it.
F18 (codex, kimi) "SSBR stays 0" too absolute: the zero is written only under update_shadow_regs; a frozen SSBR keeps its value.
   kimi: "the FP exception registers the fork does not write" slightly overbroad (the SFU1 raise sites DO write FPECR).
   ACCEPTED both -> comment reworded.
F19 (codex, deepseek) F6-of-pass-1's "residual 119 vectors" is the five-class count; seven classes -> 117 (11..113 = 103, 116..127
   = 12, + 114/115).  ACCEPTED -> comment says "117 vectors with the two SFU1 ones"; the CHANGELOG carries the deriver.
F20 (codex, kimi) the "8-of-128" census is wrong (11 of 128 low vectors delivered = 4 pre-existing + 7; 117 halt).  ACCEPTED for
   the records; Fable and kimi could not FIND "8 of 128" in any file (it was the main loop's pass-1 disposition text) -> record the
   corrected census, not a correction of a phantom.
F21 (codex) F15-of-pass-1 cited Figure 6-4 (the rte flow); the recognition diagram is Figure 6-3 and §6.10 prose is the better
   warrant.  ACCEPTED (records).
F22 (Fable 8) the house-idiom sentence ("MIPS/PPC/ARM cores deliver everything they recognise") is wrong for ARM: `arm_exception`
   exits on RESET and on an unrecognised number.  ACCEPTED -> records: "MIPS and PPC deliver unconditionally; SH and ARM exit only
   on RESET-class or unrecognised numbers".
F23 (codex, kimi) a trap while frozen: the common path zeroes DMT0-2/DMD/DMA OUTSIDE the update_shadow_regs guard, while 6.5.5
   says a trap taken while frozen modifies none of the exception-time registers.  Pre-existing, unasserted.  FILED
   m88kexcfrozendmt LOW (the trapfrozen row observes pc and the shadows, not DMT).
F24 (Fable 9d) supervisor tb1 naming 1/2/3 reaches the INTERRUPT/INSTRUCTION_ACCESS/DATA_ACCESS tail arms built for the hardware
   event (SNIP -= 4 -> rte re-executes the trap forever; SNIP = SFIP = 0; DMT from stale dmt[]).  Pre-existing, F4-of-pass-1's
   family (vector 0 named by a trap dies in the RESET tail arm: filed m88kexcresetkill in pass 1 -- CHECK that row exists; the
   ledger grep for `m88kexc` finds only m88kexcdeliver and m88kexcsfu1, so it was NOT filed and the pass-1 record is wrong about
   that).  DISPOSITION: file ONE row m88kexchwtraps LOW covering vectors 0..3 named by a supervisor trap.

## 3. DISAGREEMENTS
D1 THE DELAY-SLOT CONTRACT.  Fable/codex/grok: the else-arm is wrong per Table 6-3 and the pointer definitions (:2097-2104: while
   the SLOT executes, NIP = target, FIP = target+4).  kimi: "The manual's SNIP/SFIP pipeline-shadow semantics at 6.4.3.1.2/.3 do
   support the code's else-arm: SNIP = shadow of NIP, SFIP = 'the target of a jump or branch instruction.'  The pre-existing
   DATA_ACCESS-in-delay-slot arm, SNIP = delay_target, is the odd one out against that reading."  RULING: FILED as m88kdslotshadow
   MEDIUM with kimi's dissent VERBATIM as provenance; the re-pin-first discipline settles it by measurement (the manual's rte flow
   :9023-9050 executes the SNIP instruction then the SFIP one, so the two readings predict DIFFERENT post-rte execution sequences
   -- that is the row).  Parties: kimi vs Fable/codex/grok -- adjudicate your own dispute; the question is WHICH pipeline stage the
   shadows snapshot for a precise fault IN the slot.
D2 M_TAILOFF: Opus "escape -- vectors 0..3 unrowed" vs Fable "equivalent by construction for the seven".  Both true of different
   things: for the seven arms (bare break) the guard is equivalent; for vectors 0..3 it is not, and they are unrowed.  RULING: filed
   in m88kexcdebt as "vectors 0..3 unrowed", disclosed in the contract.
D3 THE INFO LEVEL: Fable 8 says #261's break-on-ERROR is why INFO matters; grok/Opus say the level is sibling-consistent and no
   hygiene row keys on it; codex says "unobservable must mean unobserved by this detector -- verbosity filtering and configured
   subsystem/error breakpoints observe it."  RULING: all compatible; the level IS observable (F7) and INFO is right.  No dispute
   survives -- confirm or refute.

## 4. WHAT IS STILL OWED / WHERE I MIGHT BE FOOLING MYSELF
* The repair (v3 probe, 12 new rows) is NEW floor-bound material and this pass is its pass 2.  Denominator I claim for the chain
  to close: the (d) DEPENDS-ON closure of m88k_exception() over the diff -- `implemented` per class x route {instruction, trap}
  (F1/F2: 5 classes x 2 routes, BOUNDS/ERROR trap-only by construction); the fallback predicate (M_REVERT/M_DELIVERALL); the tail
  labels (M_NAIVE/M_ERRORTAIL); the tail guard bound (M_TAILLE); {SFRZ} x {is_trap} four cells (error, errortb, trapfrozen, and the
  ordinary rows); VBR (vbrtb); the PSR write's four bits + carry (ovfc; MODE via the user rows; SFRZ/SFD1 via the exact compare;
  IND idem); EPSR (M_NOEPSR/M_EPSRAFTER); shadow update (M_NOSHADOW/M_SNIPX/M_DSLOT/M_SFIPNOTGT/M_DSLOTSWAP); the level.  NOT
  closed and DISCLOSED: M_DELAYALWAYS, vectors 0..3, M_TRAPONLY (equivalent), DMT under a frozen trap, SSBR, fcr2/4/5.  Is there a
  cell in that enumeration with no row, or a body-tested lvalue I left out of the enumeration?
* The dslot row now PINS a behaviour three seats call wrong.  I have labelled it rather than re-pinned it.  Is that the honest
  form, or is a labelled wrong pin still laundering?
* The comment edits (F15-F19) were made at 23:00 without a table: comment-only, product lines byte-identical (verified by a
  non-comment diff), and build/ is being rebuilt with the probe re-run (probe_v3_fix_final.out).  Say if a comment-only edit
  owes anything more.
* Records owed at commit: the CHANGELOG #502 block; ledger rows m88kexcdeliver (close, with the corrected note: "BOUNDS and ERROR
  have NO raise site" -> "no LITERAL-CONSTANT raise site; a supervisor trap reaches them"), m88kdslotshadow, m88kexcfrozendmt,
  m88kexchwtraps, m88kexcdebt; OUTSTANDING_BUGS; pass2_ledger.tsv receipt.  Seat record: pass 1 -- Opus, kimi, grok, deepseek,
  minimax answered; codex REFUSED twice, glm BURNED (mini re-fire answered), Fable WALLED (re-fired at pass 2); pass 2 -- codex,
  kimi, grok, deepseek, minimax, Opus, Fable answered; glm BURNED then answered the mini packet; agy DELIBERATELY NOT FIRED both
  passes (reserved for measurement).

VERDICT LINE FIRST (CLOSE THE CHAIN / ONE MORE REPAIR NEEDED: <which> / DO NOT SHIP), then F1..F24 and D1..D3 one line each,
then Q2 (which accepted disposition is wrong), then Q3 (what all nine missed), then what you could not settle.


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
