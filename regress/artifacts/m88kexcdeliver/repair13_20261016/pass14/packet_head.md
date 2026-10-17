# PASS 14 -- `m88kexcdeliver` (#502): review of REPAIR 13 (probe v20), with the close adjudication's findings shared

Four seats, by the owner's roster of 2026-10-16: Fable 5.1, GPT-6 Astra, Grok 4.7, GLM 5.3.  The other five (Opus, agy,
kimi, deepseek, minimax) are DELIBERATELY NOT FIRED under that roster.  This is an ordinary regression-detector coverage
review.  READ-ONLY: write nothing to any project tree.  The tree under review is `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC`
(HEAD 7b23b785 plus the uncommitted repair inlined below); ignore any other `src/` you find under the project root -- the
one at `C:/DocumentNoSnc/cc/GXEMUL/src/` is pristine 2021 upstream.  Everything a packet-fed seat needs is inlined; file-
reading seats may verify against `git show HEAD:<path>` and the working tree.

**Please do not simply ratify.**  Earlier today three of four seats ratified a 56-cell denominator, and the fourth showed it
omitted an axis the function TESTS; a measurement then confirmed it (section 1).  Check the premises, not just the arithmetic.

Open with your seat token -- `FABLE_M88KP14_20261016` / `ASTRA_M88KP14_20261016` / `GROK_M88KP14_20261016` /
`GLM_M88KP14_20261016` -- then ONE line: `VERDICT: CLOSE / DO NOT CLOSE (<one line>)`.

## 1. What happened since the close packet (each with its artifact under regress/artifacts/m88kexcdeliver/)

1. The close adjudication (`../adj_20261016/m88kexcdeliver/`): GPT-6 Astra, Grok 4.7 and GLM 5.3 ruled CLOSE on the 56-cell
   denominator; Fable 5.1 ruled DO NOT CLOSE -- the denominator omits `cpu->delay_slot`, which the delivery body tests, so
   {MISALIGN, UNIMPL, PRIV, OVF} x {delay slot set} were unrowed (only `dslot`, at DIV0, faulted in a slot).
2. MEASURED (`delayslot_20261016/`, scratch clone of HEAD 7b23b785): `implemented = !cpu->delay_slot;` at each of those four
   arms scored **59/59** on the shipped 59-row probe, every log byte-identical to BASE (md5 898eb0a7) -- a clean sweep at all
   four.  The polarity twins `implemented = cpu->delay_slot ? true : false;` scored OVF 50/59, MISALIGN 51/59, PRIV 53/59,
   UNIMPL 54/59 -- the per-arm row counts Fable had predicted from the row table.  Graded L2 (floor breach), repaired in-round.
3. REPAIR 13 = probe v20 (diff in section 3): four rows faulting IN A DELAY SLOT -- `dslotmisalign`, `dslotunimpl`, `dslotpriv`,
   `dslotovf`, each a `br.n +16` immediately before the faulting word, scored like `dslot` (the else-arm AS IMPLEMENTED); the
   gate pin 59/59 -> 63/63 plus a check that all five delay-slot rows deliver at their entries; the contract names the closure
   and discloses BOUNDS/ERROR x {delay slot}.  `repair13_20261016/PRETABLE.out` was written before table 16 ran (mtime order).
4. Records riding with it: two import-time asserts on `PSR_FRZUSER` / `PSR_FRZSUP` (negative-controlled: `assert_controls.out`);
   the probe comment's "58/58" corrected in place to 57/58; the m88ksfd1row ruling text; `derive_cells.py` taught the v19/v20
   rows and a delay-slot axis, `CELLCENSUS.out` regenerated (its v16 and v17/v18 grids are byte-identical to the old output).

## 2. Settled premises (warrants inline; challenge any of them)

* `m88k_exception(cpu, vector, is_trap)` (section 5, HEAD, untouched by this repair) TESTS, in its delivery path: `vector` (both
  switches), `!implemented` (the fallback, line 799), `PSR & SFRZ` (811), `is_trap` (816), and `cpu->delay_slot` (840 inside
  `if (update_shadow_regs)`, and 865 on every path that passes the fallback).  Every other PSR bit is copied to EPSR or ORed.
* In a delay slot every one of the seven trap-like arms takes the shadow branch's ELSE-arm (SNIP = pc+4, SFIP =
  delay_target): only DATA_ACCESS and INSTRUCTION_ACCESS have their own arms there.  `m88kdslotshadow` (filed) records that
  this else-arm returns wrong per the manual; the five `dslot*` rows pin it AS IMPLEMENTED and share ONE scoring branch, so
  that round re-pins all five in one place, before the code moves.
* MODE at BOUNDS/ERROR is unreachable (no instruction raises 7 or 10; a user `tb1` naming a vector below 128 raises
  PRIVILEGE with is_trap == 0; the re-route writes ERROR after switch 1) -- the warrant expires when `X(tbnd)` lands
  (row `m88ktbnd`).  SFRZ is invariant BY CONSTRUCTION inside both frozen sites (it is their guard).
* `trapfrozensfd1` runs its handler with `PSR_FRZSUP` = 0x80000003 (MODE set, SFD1 clear); `trapfrozenuser` with
  `PSR_FRZUSER` = 0x00000003 (MODE clear AND SFD1 clear), the constant `errpriv` / `errunimpl` also use.
* The probe launches `-E testm88k` with no `-C`, so every table measures an 88110 configuration; nothing in the exception path
  reads `cpu_type` (recorded since pass 8; pinning `-C 88100` is filed, not part of this repair).
* `mc88100.txt:3712-3728` (3.3.2 Delayed Branching) and `:9433-9440` (6.7.2 note 6, "instructions residing in the delay slot
  of a branch, jump, or a trap-taken instruction are never executed") are what the manual on disk says about delay slots;
  neither says whether a TRAP instruction may sit IN a delay slot.  `X(tb1)` carries no delay-slot guard, so the emulator
  reaches that case.
