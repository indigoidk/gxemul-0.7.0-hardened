> 4. `ppcdsformxo` (HIGH, FIXED by `#571` on 2026-10-24, held for Fable) -- DS-form XO bits: ldu/lwa/stdu run as ld/std at EA+1/+2.  T2;
>    ~~design owed~~ -- shipped: opcodes 58 and 62 decode their five forms by XO with the displacement DS||00, the reserved encodings and the RA = 0 update forms stop the cpu, with a 39-row rung-3 detector in gate 13; see the second 2026-10-24 section at the end.

### 2026-10-24 -- `ppcdsformxo` fixed by `#571` (held for Fable); `ppcdisasmxo`, `ppcdisasmfpupd`, `ppcldxabsent`, `ppc64on32gate` and `wiringwitnessclass` filed

`#571` makes `src/cpus/cpu_ppc_instr.c`'s D/DS-form arm decode primary opcodes 58 and 62 as DS forms: the two case
bodies re-assign the shared `imm` to `(int16_t)(iword & ~3)` -- EXTS(DS || 0b00), the XO bits no longer part of the
displacement -- and dispatch on `iword & 3`: `ld` / `ldu` (RA <- EA) / `lwa` (the sign-extended word, the existing
`ppc_instr_lwa` handler) and `std` / `stdu`, the reserved encodings (58 with XO 3, 62 with XO 2 or 3) taking the arm's
bare `goto bad` (the common tail's `UNIMPLEMENTED instruction` stop) and `ldu`/`stdu` with RA = 0 reaching the arm's
existing `ra == 0 && update` guard.  Before it every `ldu` loaded from EA+1 and performed no base update, every `lwa` loaded a DOUBLEWORD
from EA+2, and every `stdu` -- the instruction every PowerPC64 stack frame is pushed with -- stored at EA+1 and left the
stack pointer.  No handler changed (every form selects a slot the generated table already holds); the shared
assignment and the other 22 opcodes of the arm are untouched; 32-bit CPUs are disclosed (illegal opcodes, decoded
through the same arm, so their MODE32 decode and refusal behaviour change with this fix too; no width test -- filed as
`ppc64on32gate`).  It ships `regress/ppc_dsform_probe.py`,
a 39-row rung-3 detector on the unmodified `bareppc -M 64` (seven debugger-stepped guest sessions -- the loads, the stores
with every destination read back by the debugger's dump, five stop sessions -- and the bogus-machine control; every word from the
probe's own encoder; a census of all 108 placed words against the tree's current disassembler text), gated in gate 13
with every row identity, the four protocol keys and the census pinned.  Measured in
`regress/artifacts/ppcdsformxo/table1_20261024/` (pre-fix 22/39 with the 17 symptom rows red for the reason under test
-- the store half's clause-(a) artifact; fixed 39/39; the frozen 8-row witness 8/8; 16 of 16 kill-table legs red, 14 at
their written prediction, the identity body measured 17/39; clearance clean and fresh on every build tree; gate 13
PASS with 193 checks, the `#571` block 53 of 53).  Panel: Astra, Grok, Argon (through agy), GLM 5.3 and DeepSeek on
pass 1 (five READY WITH CHANGES, DeepSeek NOT READY twice on the 32-bit test and the store rows), adjudicated by Astra
(AMEND) and by Grok (AMEND; the one adjudicator disagreement -- the DS = 0 x RA = 0 refusal cells -- ruled for Grok on
the carrier's floor bound); pass 2 on the diff by the same five seats (seven answers, all LAND WITH CHANGES: records-only changes and three
docstring/comment-only detector revisions, each re-measured; Argon's Q2 confabulated and discounted), F2 adjudicated by Astra and
Grok (both AMEND, LANDING GO WITH THE CHANGES NAMED -- applied: the second and third docstring/comment-only detector revisions (each re-measured), the design row's severity left unset, two more PRETABLE claims in the erratum, the drafts' base-update wording; Astra's exact-text readings of the landed texts (`adj/final/codex_t2final*.txt`): reading 1 named twelve record corrections -- ten completed, one left incomplete and one wrongly rejected (the frozen witness copy's MANIFEST class: the checker's WITNESS/DETECTOR line governs, the copy asserts the repaired property, so it is CLASS_RESEARCH, and the mis-classed precedents are filed as wiringwitnessclass); reading 2 named ten -- nine applied, one (the stale count sentences) left incomplete; reading 3 named seven, applied; each later reading is recorded in PASS2_RULINGS.md, and the reading that says GO is the clearance this commit rests on); Fable HELD with its question.  The row's witness is the frozen
rung-3 probe (`witness_20261024/ppc_dsform_probe.py`, RED on HEAD 5/8, the loads); the store half's pre-fix red is the
detector's own `prefix_BASE.out`.  Not claimed: `ldu` with RA = RT, 32-bit CPUs, the DS = 0 x RA = 0 joints, a
positive-word `lwa`, translation on, the indexed forms, the disassembler's text.

* **`ppcdisasmxo` (LOW, open)** -- new.  cpus/cpu_ppc.c:1495-1517: the disassembler folds the XO bits into the
  displacement and prints `ld`/`std` for every opcode-58/62 word (`ldu r5,-96(r21)` appears as `ld r5,-95(r21)`);
  guest-invisible.  Witnessed by the frozen witness's census lines.  Its fix owes the oracle-correction order: re-pin
  the detector's `unasm census` expectations first, measure HEAD red, then edit.
* **`ppcdisasmfpupd` (LOW, open)** -- new.  cpus/cpu_ppc.c:1468-1489: no case for LFDU/LFSU/STFDU/STFSU, which execute
  since `#310` and disassemble as an unimplemented primary opcode.  Found by three seats independently; unfiled before
  this row.  Source-derived.
* **`ppcldxabsent` (MED, open)** -- new.  include/opcodes_ppc.h + opcode 31's dispatch: `ldx`/`ldux`/`lwax`/`lwaux` have
  no `PPC_31_*` define and reach `default: goto bad` on every cpu while `stdx`/`stdux` are implemented -- a legal 64-bit
  guest's indexed doubleword load stops the cpu.  Unfiled before this row (the main loop's grep of the bug file and
  all 1,079 ledger rows).  Source-derived; the rung-3 witness shape is one stepped `ldx` word on HEAD PPC970.
* **`ppc64on32gate` (design, open; no severity assigned)** -- new.  At least fourteen 64-bit-only instructions decode with no width test
  on a 32-bit cpu (only `rld*` is gated; `extsw` counted although its MODE32 handler diagnoses and returns) and eleven more are absent on every width; PEM :6253 makes opcodes 2, 30, 58
  and 62 illegal on 32-bit implementations.  `#571` discloses it; the licensed fix is the `rld*` width idiom applied to the
  ungated implemented set, in its own round with a 32-bit session row per gated label -- the filing does not
  pre-authorise a uniform sweep (`PASS1_RULINGS.md` F1).
* **`wiringwitnessclass` (LOW, open; records)** -- new, from `#571`'s final exact-text clearance.  tools/pipeline/
  check_probe_wiring.py's MANIFEST classes frozen rung-3 witness copies that are red on HEAD and GREEN once the defect is
  gone (`m88kbuserrregs/witness_20261023/`, #539's post-fix entries -- not `vmedefaultkill`'s, whose sites probe reports
  outcomes without grading the defect and whose free-run companion asserts the pre-fix symptom) as CLASS_WITNESS,
  against the checker's own line (`:55-57`: a WITNESS asserts the pre-fix symptom and is RED once the defect is gone).  `#571`
  classes its frozen copy CLASS_RESEARCH; the earlier entries owe a re-classification in a records round.  No gate obligation
  rides on either class.
