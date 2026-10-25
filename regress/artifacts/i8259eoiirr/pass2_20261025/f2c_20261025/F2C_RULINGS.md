# i8259eoiirr (#574) -- F2c (the instrument repair's own pass) rulings of the main loop, 2026-10-25 13:3x

Six answers: `codex_t19f2c.txt` (GPT-6 Astra, ADJUDICATING: RATIFY WITH CHANGES -- three DERIVED holes), `grok_t19f2c.txt` (RATIFY WITH
CHANGES -- one breach cell of the recompute, three shapes), `ollama_glm_t19f2c_A.txt` (RATIFY WITH CHANGES -- the recompute's no-op
shape; records counts), `ollama_glm_t19f2c_B.txt` (RATIFY WITH CHANGES -- the recompute's mask-term cell; disclosure gaps; records),
`ollama_deepseek_t19f2c_A.txt` (NOT RATIFY -- counts the three disclosed escapes as breaches), `ollama_deepseek_t19f2c_B.txt` (RATIFY --
zero breaches).  No wall, no echo, no burn (every answer read in full).  Argon OWED (queued); Fable HELD; kimi/minimax/Opus seat
not fired by roster; agy walled.

## The ruling: THE CHAIN DOES NOT CLOSE ON THIS PASS -- the SAME CLASS a second time, so the next repair owes the CLASS CLOSURE
Every new row is valid by construction and none is vacuous (Astra, Grok, GLM A, GLM B, DeepSeek B agree; each checked the mutant's
measured value against its row).  But three seats independently name a cell of the fix's recompute predicate `d->irr & ~d->ier`
that no row observes -- its OTHER partition cells: a MASKED request remaining (the mask term dropped: Grok, GLM B, Astra), NOTHING
remaining (the recompute deleted or made constant-true: Grok, GLM A) -- and Astra names two more cells of the fix's predicates: the
EOI's `d->isr & bit` weakened to "any ISR bit" (an EOI of a line NOT in service while another IS), and the GT cascade conjunct
`n == 2` dropped (a non-cascade master acknowledge with slave work pending).  F2b found cells of this class; F2c finds more of it.
Per the repair-chain amendment the next repair ENUMERATES the full space of the fix's predicates from the functions' own inputs,
rows every cell in ONE diff, measures every named shape as a mutant, and writes into the CONTRACT which cells are rowed and which are
deliberately not; the closing pass (F2d) VERIFIES THE ENUMERATION rather than hunting cells.

## Dispositions on the F2c answers
C1  DeepSeek A (NOT RATIFY: "three escaped mutants remain"): REJECTED by argument -- the three escapes are the DISCLOSED cells
    (`D_fold`: the two-slave stall, owed as `i8259cascline`; the two retire-guard conjuncts: filed `pit8253retireguard` with the
    band-row construction), named in PRETABLE.out before the table ran and in the contract; Astra, Grok, GLM A, GLM B and DeepSeek B
    all read them as disclosed.  "Zero breaches with the denominator" counts undisclosed escapes; a disclosed cell is clause (e).
C2  The recompute's partition (Grok BREACH; GLM B BREACH; Astra hole 2; GLM A's `pit ip2`): ACCEPTED as clause-(d) floor cells --
    the predicate the fix ADDS, with its body-tested partition {unmasked request remains -> ASSERT; nothing remains -> DEASSERT;
    only masked remains -> DEASSERT}; v2f rows only the first.  v2g rows all three: `maskrem ip2` (both UARTs pending, line 4
    masked, the poll acknowledges 3; Cause bit 10: FIX 0 / HEAD 1 -- symptom), `ack ip2` (the poll acknowledges the only pending
    line; FIX 0 / HEAD 1 -- symptom) and `pit ip2` (the poll retires the only 8253 event; FIX 0 / HEAD 1 -- symptom).  Mutants
    MEASURED first against v2f: `D_recompute_raw`, `D_recompute_true`, `D_recompute_none`.
C3  Astra hole 1 (`d->isr & bit` -> `d->isr != 0`): ACCEPTED as a clause-(d) cell (the added predicate weakened to a coarser test
    of the same lvalue).  v2g session `isrother`: line 3 acknowledged, line 4 pending and NOT acknowledged, EOI 0x64 -- the legacy
    branch must consume IRR bit 4 (`isrother irr4` 0 both; the mutant leaves 1) and ISR must keep bit 3 (`isrother isr` FIX 0x08 /
    HEAD 0x00).  Mutant `D_eoi_anyisr`, measured first.
C4  Astra hole 3 (GT `n == 2` dropped): ACCEPTED as a clause-(d) cell of the GT guard's partition {n == 2 with slave work; n != 2
    with slave work; n != 2 without}.  v2g session `gtmask`: UART 4 and RTC 8 pending, master line 2 MASKED (OCW1 0x04), the GT
    read: the master acknowledges 4, the slave is left alone -- `gtmask iack` 4 both, `gtmask isr8` 0 both (the mutant returns 8
    and sets slave ISR bit 0), `gtmask isr` FIX 0x10 / HEAD 0x00.  Mutant `D_gt_nocasc2`, measured first.
C5  GLM B disclosure gaps: `pic1 != NULL` false and `pic2 == NULL` are UNOBSERVABLE on a one-machine instrument (no session can
    remove a PIC) -- DISCLOSED in the contract's OUTSIDE list; `n2 >= 0` false (the spurious cascade) is unreachable while the fold
    invariant holds (PRETABLE G4) -- named explicitly in the contract and in the `i8259cascline` filing's note.  GLM B's open
    question (a bare command read after an OCW3 ISR selection): the fix's one-shot touches only the 0x0c poll; the 0x0a/0x0b
    selections are HEAD's unchanged lines -- not a cell of the fix's predicates; recorded, not rowed.
C6  The scan direction (main loop, from the enumeration): the two-line rows pin lowest-first by construction (`poll first` 0x83,
    `gtboth iack` 8); mutant `D_scan_high` added so the pin is MEASURED, not inferred.
C7  Records (GLM A, GLM B, Astra A12/A7): the F2c packet's "two sessions and six rows" undercounted -- v2f added THIRTEEN explicit
    rows (seven answering cells, six companions) plus four liveness rows (two sessions x ram/stable) = 17, 84 -> 101; the packet's
    diff caption said v2d -> v2e for a v2d -> v2f diff; the 20/3 table is of v2f (its SCORES header names the fixlegs_114055 copy);
    the rate artifact lives at `pass1_20261025/rate_explore_20261025/` (the drafts cited it without the pass-1 prefix: corrected);
    the A7 gloss "a run of about a second" is UNMEASURED -- the rate session's wall time is not recorded; the FIX count 3 is a band
    guard, the cadence is filed with `pit8253retireguard`.  All L4, corrected in the drafts and here.
C8  Astra A1 (the Linux ICW2 extract is relayed, not version-pinned): ACCEPTED as the honest state -- the warrant is Grok's
    re-fetch, recorded as such; a version-pinned extract is owed to `i8259isrnever`'s neighbourhood, not to this landing.
C9  Astra on `D_eoi_n3`/`D_eoi_n4` also red on `spec eoi one`/`spec eoi both` (coherent over-catch) and on `spec isr both` being the
    precondition witness, not a second kill: ACCEPTED as wording for the contract.

## What v2g adds (the class closure, one diff), measured first as mutants against v2f
Sessions `maskrem`, `isrother`, `gtmask`; rows `ack ip2`, `pit ip2`, `maskrem ip2`, `isrother irr4`, `isrother isr`, `gtmask iack`,
`gtmask isr8`, `gtmask isr` (+ the sessions' liveness and precondition rows).  Mutants `D_recompute_raw`, `D_recompute_true`,
`D_recompute_none`, `D_eoi_anyisr`, `D_gt_nocasc2`, `D_scan_high` -- measured against the UNCHANGED v2f first (table_v2f_extra/),
then the full table of record on v2g (29 mutants).  PRETABLE.out's v2g block carries the ENUMERATION: every predicate the fix adds,
its body-tested partition, the row per cell or the disclosure per cell.

MEASURED 13:23-13:42 against the UNCHANGED v2f instrument (`run_extra2_19.sh` -> `/tmp/gxt19/killtable_v2f_extra_132336`, banked as
`killtable_20261025/table_v2f_extra/`): **D_recompute_raw ESCAPED 101/101** (the mask-term cell: a real breach, as Grok, GLM B and
Astra said), **D_eoi_anyisr ESCAPED 101/101** and **D_gt_nocasc2 ESCAPED 101/101** (Astra's two other holes: real); D_recompute_true
and D_recompute_none KILLED 99/101 -- by the RATE session (`rate poll byte` 0x00 and a storm count of ~15,000: a line that never
drops makes the handler re-enter; GLM B predicted this consequence-kill), so Grok's "three shapes stay green" held for one of the
three; D_scan_high KILLED 94/101 (the two-line rows pin the order, as the enumeration said by construction).  v2g rows the three
escapes directly (`maskrem ip2`; `isrother irr4`; `gtmask iack` / `gtmask isr8`) and gives the two consequence-kills a direct row
each (`ack ip2`, `pit ip2`).  v2g cycle: witness_20261025f 123/123 on HEAD; fixlegs_132736 123/123 both legs; legs_133457 L0
91/123 with exactly the 32 symptom rows red, L3 0/123.  PRETABLE.out's v2g block (the enumeration) appended 13:42:29, before the
29-mutant table of record.

## Corrections from F2d (2026-10-25 16:0x; pass2_20261025/f2d_20261025/F2D_RULINGS.md D5, D12)
* C2 said "v2f rows only the first".  Read: v2f DIRECTLY SAMPLES only the first cell; D_recompute_true / D_recompute_none already
  failed two rate rows on v2f (99/101, table_v2f_extra/SCORES.txt) -- consequence kills, rowed directly by v2g (Astra, F2d).
* C9 attributed the coherent over-catch observation (D_eoi_n3 / D_eoi_n4 also red on spec eoi one / spec eoi both) to Astra.  It is
  GLM A's; Astra supplied the prerequisite-versus-kill distinction (spec isr both the precondition witness) (Astra, F2d).
* "Mutants MEASURED first against v2f" (C2) and the section head "measured first as mutants against v2f": the v2f-extra sweep
  (13:23:36 - 13:42:08) ran CONCURRENTLY with the v2g re-pin (13:23:56) and both legs (13:27:36), on separate scratch clones; it
  completed before the enumeration block (13:42:29) and the table of record (13:43:16).  Values unaffected (F2d D5).
