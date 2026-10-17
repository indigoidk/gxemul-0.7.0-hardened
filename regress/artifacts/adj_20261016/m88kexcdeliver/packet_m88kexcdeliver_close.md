# ADJUDICATION -- `m88kexcdeliver` (#502): close the chain?  Plus the queued `m88ksfd1row` question

Four independent adjudicators (owner roster 2026-10-16: Fable 5.1, GPT-6 Astra, Grok 4.7, GLM 5.3).  An ordinary
regression-detector coverage review.  READ-ONLY: write nothing to any project tree.  The facts you need are inlined;
seats that can read files may verify them under `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC` (HEAD 7b23b785; committed text
via `git show HEAD:<path>`).

Open with your seat token (`FABLE_M88KCLOSE_20261016` / `ASTRA_M88KCLOSE_20261016` / `GROK_M88KCLOSE_20261016` /
`GLM_M88KCLOSE_20261016`), then ONE line: `VERDICT: CLOSE / DO NOT CLOSE (<one line>); m88ksfd1row: KEEP / REMOVE`.

## Facts

1. The row (HIGH, "in work" since 2026-09-05): the m88k CPU model stopped the guest CPU for five trap-like exception
   classes (privilege violation, integer divide error, integer overflow, misaligned access, unimplemented opcode) instead
   of delivering them through the vector base.  The fix shipped and is committed; a rung-3 witness
   (`regress/m88k_exc_probe.py`, real guest instructions on the committed `testm88k` machine) measured HEAD 0/9 before and
   the fix 22/22.  The detector then went through a repair chain of twelve panel passes; it is now 59 rows
   (commit 79cd12e8, 2026-09-06).
2. Pass 9 (grok) found the previous "class closure" had closed one status-register bit at one of seven dispatch arms and
   corrected the denominator to six settable bits: 7 arms x 6 = 42, less 2 unreachable = 40 cells.  Version 17 of the probe
   closed all seven arms; table 14 measured three predicted sweeps at 54/54 on the old instrument, each killed on v17.
3. Pass 11 (grok) overturned the coordinator's own filing: the trap side x {MODE, SFD1} cells were FLOOR, not disclosed
   debt.  Repaired in-round (rows `trapfrozenuser`, `trapfrozensfd1`, 57 -> 59); table 15 measured both mutants sweeping
   the pre-repair instrument clean (57/57 each).
4. Pass 12 (codex, 2026-09-06; `regress/artifacts/m88kexcdeliver/pass12_codex/codex.txt`): **CLOSE THE CHAIN -- zero
   floor breaches**, denominator re-derived independently: dispatch arms 4-10 x six bits less MODE at BOUNDS/ERROR 40/40;
   fallback x six bits 6/6; frozen non-trap re-route x five varying bits 5/5; frozen trap exemption x five varying bits
   5/5; total 56/56.  The other seats were not available that day: agy deliberately unfired, Opus and Fable held for a
   three-day allowance wall, GLM out of budget twice.  So the closing pass is ONE seat.
5. The flagship seat's deferred question from 2026-09-06 (`tools/pipeline/fable_queue.md` "### 1. m88kexcdeliver"): the
   DEPENDS-ON enumeration treated an arm that reads no status-register bit as out of scope for bit-conjunct mutants, which
   made {arm} x {C, IND, SFD1} disclosed debt rather than floor -- "is 'the arm reads no PSR bit' the right test at all,
   given that the fault reaching the arm carries PSR state the arm could trivially be made to read?"  And: "of the pass-7
   dispositions, which is wrong?"  Since then, passes 9-11 closed the bit axis at ALL seven arms (fact 2) and the trap
   side (fact 3).
6. `m88ksfd1row` (LOW, open; `fable_queue.md` "### `m88ksfd1row`"): row `trapfrozensfd1` has ZERO measured delta against
   its own mutant -- deleting it, the mutant is still caught 58/58 by `trapfrozenuser`.  Codex (pass 12) ruled the
   attribution warrant does not transfer ("row demand is bounded per enumerated mutant, never per attribution need") and
   that removing it loses none of the 56 cells.  But codex's own next paragraph: after removal, SFD1 coverage rests
   entirely on `trapfrozenuser`, whose constant `PSR_FRZUSER` is SHARED with rows `errpriv` and `errunimpl`; changing that
   constant 0x03 -> 0x0b keeps their routes while silently deleting the only SFD1-clear stimulus, and the baseline would
   not notice.  The queue asks: (a) the licence is right, the row goes, the shared-constant hazard is handled another way;
   or (b) a distinguishing failure signature is a licensed benefit when the alternative concentrates an axis on a shared
   constant -- then the licence's wording should say so.

## The coordinator's dispositions (attack them)

- **CLOSE the chain.**  Pass 12 is a valid closing pass in substance -- the diff delivered, the denominator re-derived and
  stated (56/56), zero floor breaches -- and its one weakness is the roster (one seat).  This four-seat adjudication is the
  missing roster: if no seat finds a floor breach in the 56-cell enumeration, the row closes (witness unchanged:
  `probe:regress/m88k_exc_probe.py`).
- **The deferred cut question is MOOT, not answered.**  Passes 9-11 closed every bit x arm cell the question was about, so
  no row depends on the cut any more.  Whether "reads no PSR bit" is the right DEPENDS-ON test in general stays a rule
  question for the owner if a future round needs it; this round does not.
- **`m88ksfd1row`: KEEP the row, no licence change.**  The addition licence governs additions to PRODUCT code ("licensed by
  measured deltas or a transferred warrant, never by it cannot hurt"), and row DEMAND ("per enumerated mutant") governs
  whether a NEW row is owed.  Neither rule requires deleting an existing, passing, inexpensive row, and codex's own
  shared-constant paragraph names a concrete edit under which this row is the only SFD1-clear stimulus.  Record it as
  "kept, not owed", close `m88ksfd1row`.

## Questions (VERDICT LINE FIRST)

1. CLOSE or DO NOT CLOSE -- if not, name the floor cell and the edit that sweeps the 59-row detector.
2. Is the deferred cut question moot as stated, or does something still rest on it?
3. `m88ksfd1row`: KEEP or REMOVE, and does the addition licence (or row-demand rule) need new wording?
4. Which of the coordinator's dispositions is wrong?

Seat notes: Grok -- passes 9 and 11 were yours; be harder on them.  Astra -- pass 12 was yours (as codex); self-review.
