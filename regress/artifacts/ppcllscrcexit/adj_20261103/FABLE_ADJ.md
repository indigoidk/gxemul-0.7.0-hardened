# `ppcllscrcexit` -- final adjudication of the pass-1 design (Fable 5.1, main loop, 2026-11-03 ~23:0x)

HEAD `ebe5af82`.  Written by GXEMUL [087a90] with the session model Fable 5.1 (the owner switched to it ~22:4x; the
09:1x hold on Fable adjudication existed only because the main loop was Opus 5.5).  Owner roster of 12:0x: GLM 5.3, Grok,
Astra and Argon review; Fable rules.  Nothing is implemented, built or measured by this record: it decides the DESIGN the
round implements and what the round owes.

## Evidence basis (name it, so the ruling's provisionality is on its face)

| stage brief (one Gemini-web packet = one panel brief) | GLM 5.3 | Grok 4.7 | Astra | Argon | Argon's adjudication draft |
|---|---|---|---|---|---|
| bug review `ppcllscrcexit` (`_scratchpad/panel_20261103_103044_next5_ppcllscrcexit/`, `gweb/jobs_20261102_next5/ppcllscrcexit/`) | GO | GO (no verdict line; read whole) | GO-WITH-CHANGES (`codex_ppcllscrcexit_r2.txt`) | 5/0/4/1 | `gweb/jobs_20261103_adj/ppcllscrcexit_adj/` |
| fix draft `ppcllscrcexit_draft` (`..._103045_next5_ppcllscrcexit_draft/`) | GO-WITH-CHANGES | GO-WITH-CHANGES | GO-WITH-CHANGES | 6/1/3/2 | `.../ppcllscrcexit_draft_adj/` |
| manual (Book I/II/III text) `_manual` (`..._111221_...`) | GO-WITH-CHANGES | GO-WITH-CHANGES | **not yet** (Astra walled 11:14-00:08) | 10/2/6/2 | not built (waits for Astra) |
| siblings `_siblings` (`..._111222_...`) | GO-WITH-CHANGES | GO | **not yet** | 8/0/4/4 | not built |
| witness design `_witness` (`..._111224_...`) | GO-WITH-CHANGES | GO-WITH-CHANGES | not asked (by design) | 4/1/0/3 | `.../ppcllscrcexit_witness_adj/` 7/2/1/4 |
| port comparison `_port` (`..._111225_...`) | NO-GO (nothing to port) | NO-GO (nothing to port) | **not yet** | 5/3/0/2 | not built |
| revised draft (Argon, `.../ppcllscrcexit_v2/`, 15/8/1/6) and its review (Argon, `.../ppcllscrcexit_v2r/`, 12/3/7/2) | -- | -- | -- | both read | -- |

**Stage briefs: 4 of 4 roster seats.  Extras: 3 of 4 (Astra owed on manual, siblings, port).**  So this ruling is FINAL on
the stage briefs and PROVISIONAL on the extras' questions; Astra's three answers, when they land (the codex resume waits for
00:08), are read against this record and anything they refute is corrected here in place.  Seats outside the 12:0x roster
(agy, deepseek, minimax, kimi-k3; the Opus seat was stopped) answered too and stay on disk, marked OUTSIDE the roster in each
dir's JOB.txt; they were not read for this ruling and are not counted.

Every fact below marked CHECKED was settled by me by opening the file named, not taken from a seat.

## 1. The defect as filed -- CONFIRMED, two record corrections

* CHECKED `src/cpus/cpu_ppc_instr.c` at HEAD: the two guards are at :2305-2308 (`if (rc) { fatal("ll: rc-bit set?\n");
  exit(1); }`) and :2331-2334 (`if (!rc) { fatal("sc: rc-bit not set?\n"); exit(1); }`); the decoder arm :4895-4900 sends all
  four extended opcodes with the raw word (`xo = (iword >> 1) & 1023` at :4643 drops bit 31); `X(llsc)` recomputes
  `rc = iw & 1` (:2279).  No MSR[PR] test anywhere on the path, so user-mode reach holds.  The eight (XO, bit-31) classes that
  reach the function and the four that end the process are exactly as filed; every seat that enumerated them agrees.
* CHECKED `opcodes_ppc.h`: LWARX 20, LDARX 84, STWCX_DOT 150, STDCX_DOT 214 are the 10-bit fields (the `_DOT` names do not
  filter bit 31).
* CHECKED `tmp_ppc_tail.c`: the same source builds the 64-bit and the MODE32 decoders, so one edit covers every CPU in the table.
* Record correction L4 (the filing's wording): "stwcx./stdcx. with Rc=0" names the dotted mnemonic, which MEANS bit 31 = 1; the
  killing store words are the UNDOTTED encodings (bit 31 clear).  Say "stwcx./stdcx. encodings with bit 31 clear".
* Record correction L4 (the ledger note): the decoder citations ":4614, :4866-4871" are stale; at HEAD they are :4643 and
  :4895-4900.  The guard citations :2305-2308 / :2331-2334 have NOT drifted -- the bug-review packet's "say where they drift"
  presumed a drift that does not exist (packet defect, recorded, no action).
* Rejected: GLM's point that "HOST-STOP" is "neither defined class" -- it is TRIAGE.md's vocabulary for `exit(1)`; the
  packet's own gloss ("host kill") is the same thing.  No change.

## 2. The architecture -- CHECKED in the local extracts, and it decides the pair-by-pair disposition

* `_scratchpad/ppc_uisa_book1_v201.txt:432-433` (Book I v2.01 S1.5.2): "Reserved fields in instructions are ignored by the
  processor."  `:438-439`: "/" denotes a reserved field.  `:445-450` is only a Programming Note telling SOFTWARE to code them zero.
* `_scratchpad/ppc_vea_book2_v201.txt:1264`: the lwarx and ldarx layouts show bit 31 as "/".  **So lwarx/ldarx with bit 31 set
  are VALID forms whose reserved bit must be ignored.**  Book I `:1109-1114` defines an invalid form as a wrongly coded field
  "excluding the opcode fields and reserved fields" -- the load pair is not an invalid form at all, and a Program interrupt on it
  would be acting on a field the architecture says to ignore.  (The tentative draft's load comment, "INVALID FORM ...
  boundedly undefined", is therefore WRONG for the loads and is corrected below.)
* `ppc_vea_book2_v201.txt:1305, :1307`: the stwcx. and stdcx. layouts show bit 31 as "1".  Book I `:1122-1128` names the Store
  Conditional instructions among those whose non-opcode field "other than that specified in the layout diagram" makes the
  form invalid, and `:1116-1120` gives the permitted outcomes: "either cause the system illegal instruction error handler to be
  invoked or yield boundedly undefined results".  `:451-452` (completed by `ppc_pem_32and64_2005.txt:6213`): boundedly
  undefined = achievable by executing an arbitrary instruction sequence from the prior state.  Executing the defined stwcx.
  (store if reserved, CR0 written per `ppc_vea_book2_v201.txt:1323/:1337`) is achievable by executing stwcx. itself, so it is
  inside the bound.  **For the store pair both outcomes are permitted and neither is required.**
* EH (Astra's caution): CHECKED `cpu_ppc.h:75-88` -- the eleven modelled CPUs (405GP, 601, 603, 603e, 604, 620, 7400, 7455,
  750, G4e, 970) all predate the ISA revision that assigned the load-reserve low bit as a hint, and on such a CPU "ignore
  the bit" is also the right behaviour for a hint.  One behaviour serves both readings; no model-specific predicate is needed.
* ldarx/stdcx. on the 32-bit members are an illegal-OPCODE question for both values of bit 31; this row does not touch it.
  CHECKED `cpu_ppc_instr.c:4315-4317`: #571 made the same choice for opcodes 58/62 ("illegal on 32-bit implementations ... no
  width test is added here (disclosed)").  Same disposition here: disclosed, not fixed.

## 3. Ruling on the disposition

**Draft A, applied to both pairs: remove both guards and let the body the extended opcode already selected run.**  Named per
pair, because the manual's reason differs: **DELETE (member 1) for the load pair** -- the encoding is a valid form and the
value was always acceptable; **ACCEPT (member 4) for the store pair** -- an invalid form whose defined-operation result is a
permitted (boundedly undefined) outcome that the body already computes.  No announce, latched or otherwise: there is no event
a guest needs told about (the architecture permits exactly this result), and a `(once)` message would be a wrong record for
the load pair.

**Draft B (an illegal-instruction Program interrupt) is REJECTED**, on three grounds, any one sufficient:
1. For the load pair it is architecturally prohibited (S2).  A B-only design would trap valid instructions.
2. For the store pair it buys no conformance A lacks, and it is IMPLEMENT, not a disposition: CHECKED `cpu_ppc.c:318-345` --
   `ppc_exception()` has no Program vector constant (CHECKED `cpu_ppc.h:252-257`: DSI 3, ISI 4, EI 5, FPU 8, DEC 9, SC 0xc),
   writes SRR1 as `msr & 0x87c0ffff` (or the 0x10-0x13 form), which carries no illegal-instruction cause bit, and takes SRR0 from
   `cpu->pc`, which `X(llsc)` never synchronises (CHECKED: no `cpu->pc` write in :2276-2374; the sync idiom is at :216-225 and
   :3414-3418).  Three new correctness surfaces for a result the no-machinery alternative already satisfies.
3. A mixed design (A for loads, B for stores) splits one defect across a reserved-vs-required bit for no guest benefit and
   doubles the detector.

Argon's bug-review adjudication framed the disposition as an open Argon+GLM-vs-Grok dispute; the manual seats (Grok, GLM on the
`_manual` brief; Argon's own `_manual` answer) settle it the way this ruling does, and its UNSETTLED F4-F7 are settled above by
the files it named.  Count the arguments, not the seats: the deciding argument was the Book I/II text, which no bug-review
seat had.

## 4. The fix the round implements (the implementer writes the diff from HEAD; this is the specification)

In `src/cpus/cpu_ppc_instr.c`, `X(llsc)` only:
1. Delete the four lines :2305-2308 and the four lines :2331-2334.  Nothing else in the function moves: CHECKED, every exit
   path (`return` at :2314, :2347, :2362) is already inside the valid-form body, the function has no common tail after the
   if/else, and `old_so` (:2330) is read before the removed store guard in both versions.
2. Drop `rc` from the declaration at :2279 (`int i, rt, ra, rb;`) -- it is otherwise set and never read.
3. One `/* #NNN: */` comment per site, in the file's style, recording for the LOAD site: bit 31 is a reserved field ("/") in the
   lwarx/ldarx layout and the processor ignores it (Book I v2.01 S1.5.2), so the Rc=1 words run the one body the instruction
   has and CR is not written; it used to end the emulator.  For the STORE site: bit 31 is "1" in the stwcx./stdcx. layout, the
   bit-clear words are an invalid form whose permitted outcomes are the illegal-instruction handler or boundedly undefined results
   (Book I S1.9.2), and this core takes the latter -- the defined store-conditional, CR0 `0b00 || EQ || XER[SO]` included -- because
   `ppc_exception()` has no Program vector and no illegal-instruction cause bit and none is required; it used to end the emulator.
   Both comments: the #216 returns below stay (they follow a DSI `memory_rw` already raised); ldarx/stdcx. on the 32-bit CPUs
   are an illegal-opcode question left exactly as #571 left opcodes 58/62.
4. Do NOT touch: the decoder arm :4895-4900 -- and, made explicit at the pass-2 panel's request (GLM): routing the bit-31 forms to `goto bad`, the core's illegal-opcode idiom, is REJECTED, a CPU-STOP on a valid form (the loads) and on a permitted-outcome form (the stores), neither of which is a permitted outcome -- the #216 returns, the
   CR0/XER-SO logic, the all-CPU `ll_bit` clear, `X(invalid)` :241-245, the fetch exit :4117-4119 (`qhslowifetch`, the next
   row), the disassembler `cpu_ppc.c:1002-1021` (bit-31-blind mnemonics; disclosed), the pre-existing :2338-2341 comment (its
   "to to bit 4" is upstream text about CR0; the code is right; assessed, not changed).
5. The revised draft Argon wrote (`ppcllscrcexit_v2`) is the right DIFF (it drops `rc`, deletes both guards, adds no third hunk)
   but its COMMENTS are wrong for the load pair ("INVALID FORM ... boundedly undefined") -- use the wording in item 3.  Its
   second rendering carries real line numbers (@@ -2276,8 ...); the v2r reviewer's "BROKEN" on excerpt-relative hunk headers
   applies only to the first rendering.  The tentative draft's third hunk (`+ ll_bit = 0`) was a FALSE ADDITION -- CHECKED,
   the line exists at :2346 -- so Grok and Astra were right and GLM/Argon wrong on that point; the draft adjudication's
   F3 is SETTLED YES.
6. Propagate the edited file to build/, build-asan/ and /tmp/gxsec-build (part 1 cmp, part 2 rebuild) and est/ (source tree);
   the kill table runs in a scratch clone by default.

## 5. Witness (rung 3, owed BEFORE the edit) and detector -- the shape, for the implementer

* Machine: unmodified `-E bareppc` (PPC970, 64-bit) driven cold exactly as `regress/ppc_crlogic_probe.py:115-135` does (`-V -x
  -E bareppc -M 64`, a four-byte dummy file at CODE, commands on stdin, `put w` / `pc=` / `step` / `reg` / `dump`).  A second
  leg on a 32-bit CPU (`-C PPC750`, or `-E pmppc`) for the lwarx/stwcx. words only.  CHECKED: `cpu_ppc.c:95` big-endian;
  `ll_bit`/`ll_addr` are not debugger registers, so the reservation is observed through CR0 and the stored bytes.
* Words (RT=r3, RA=0, RB=r4): lwarx `0x7C602028`/`0x7C602029`, ldarx `0x7C6020A8`/`0x7C6020A9`, stwcx. `0x7C60212D`/`0x7C60212C`,
  stdcx. `0x7C6021AD`/`0x7C6021AC` (the second of each pair is the bit-31 form that ends the pre-fix process).  Grok's
  `_witness` answer walks the field arithmetic and the expected observables build by build; the implementer re-derives it.
* Pre-fix symptom: the session ends at the step with the fatal text on the pty (`ll: rc-bit set?` / `sc: rc-bit not set?`) --
  the TEXT is the signature; EOF alone is an instrument failure.  Post-fix: the same word executes as the valid form.
* Controls: liveness = the valid lwarx loads a non-palindromic pattern into r3 and the valid stwcx. after it stores and sets CR
  `0x2fffffff` from seed `0xffffffff`; architecture signature = the pattern (4 vs 8 bytes distinguishes `len`), the stored bytes,
  the CR value (the no-reservation path gives `0x0fffffff`, so the control demands the success value).  Null medium: no emulator
  -> no prompt -> every row fails, with no fatal text to mistake for the defect.
* Detector rows (names <= 13 chars; one session per row; pin by COUNT in `regress/gate_ppc.sh` beside the #571 block):
  controls `ll-lw-ok`, `ll-ld-ok`, `sc-stw-ok`, `sc-std-ok`; fixed rows `ll-lw-rc1`, `ll-ld-rc1`, `sc-stw-rc0`, `sc-std-rc0`
  (each demands the valid form's SIGNATURE, not survival: a bare-`return` mutant lives and does nothing); plus `sc-noresv`
  (stwcx. with no prior lwarx: CR0 EQ clear, memory unchanged) and `sc-so` (XER[SO] seeded: CR0 bit 3 set on both outcomes).
* Floor: (a) the four rc rows fail pre-fix; (b) each guard reinstated verbatim fails its two rows; (c) null medium above;
  (d) DEPENDS ON -- the predicates dominating the deleted lines up to the function boundary are `if (load)` and the `switch (xo)`
  arms that set `load`/`len`: mutants = `load` inverted or forced (lwarx takes the store path), `len = 8` dropped on ldarx/stdcx.,
  `len = 8` added on the word forms, a case label re-keyed -- each is seen by a control row's value/width/CR signature;
  (e) contract: catches the above plus a `return` (no-op) or any re-added kill at either site; DISCLOSES bit-31 forms on the
  32-bit CPUs for ldarx/stdcx., EH-style XOs 532/596 (`goto bad` today), the #216 DSI paths and `ppcllscsrr0`, alignment,
  little-endian, ncpus > 1, the disassembler's mnemonic.  PRETABLE.out before table 1.
* The reservation chain row (lwarx A; stwcx. B fails; stwcx. A must fail) is clause-(e) coverage of the existing :2346 clear,
  not owed by this diff; take it if cheap.

## 6. Dispositions of the extra briefs' findings (provisional until Astra answers manual/siblings/port)

* Witness brief: ACCEPT Argon F1 (the jazz driver's MIPS registers -- use the PPC probe pattern instead); ACCEPT F6 (the
  packet's "CR0 per the valid form" was vacuous for the loads; the comment says "CR not written"); REJECT F7 (Grok reading the
  tree is its ROLE; Argon's ground rules bind packet-fed seats only); its UNSETTLED F2-F5 are settled by `opcodes_ppc.h`,
  `machine_test.c:448-457` (bareppc = PPC970) and the crlogic probe's launch recipe.
* Siblings brief: S1 `X(invalid)` -- Grok's reading that no translated call reaches it on PPC (the generator's filler slots; no
  producer emits the sign-extending-double index) is ACCEPTED as "assessed, no row"; `armldrexbhdspin` is the ARM instance and
  is already filed.  S7 (the fetch exit) IS `qhslowifetch`, next in the queue -- a different member (return into the raised
  ISI).  The bit-31 CPU-STOPs Grok listed are already filed: `ppccntlzwrc` (11-02), `ppcoeundec`, `ppcfpreservedrc`.  Nothing new
  to file from this sweep.
* Port brief: NO-GO on porting is UPHELD -- rs6000's d13a974/3c00042 are #216's shape (already here) and 3dafe765 is
  `ppcllscsrr0`'s; keep the rows separate.  The round block records this so the research note's "nothing safe to copy" has its
  reason.
* Manual brief: the pair-by-pair result in S2 is adopted verbatim as the design's warrant.

## 7. Open, and who closes it

1. Astra on `_manual`, `_siblings`, `_port` (owed; the resume runs after 00:08).  Read against this record; correct in place.
2. The witness run itself (rung 3) -- the round's first step after this ruling; nothing here is measured.
3. `ppcllscsrr0` (stale SRR0 on a DSI inside `X(llsc)`) is adjacent and NOT folded in (reopening rule: a different fix,
   a different oracle).
4. The commit message's own pass-2 and F2 receipts follow the standing method; this record is the pass-1 adjudication.

---

## Corrections (2026-11-04), ordered by the F2 ruling of record (`MYTHOS_F2R.md`); the text above is kept as it was written

* **F15** -- section 5's "Null medium: no emulator -> no prompt -> every row fails, with no fatal text to mistake for the defect" is
  wrong.  Replacement: "Null medium: no emulator, no prompt -- every value, bytes, CR, pc and seed row fails; the exit-status `session`
  rows and (until the census repair) the 0/0 census pass: /bin/true 15/83, a missing binary 1/83 (14/83 and 0/83 after repair B).
  RESULT, pinned by equality, and CONTROL=FAIL reject both."
* **F16** -- ground 3's "and doubles the detector" is withdrawn as unsupported (the same eight classes either way); grounds 1 and 2 stand.
