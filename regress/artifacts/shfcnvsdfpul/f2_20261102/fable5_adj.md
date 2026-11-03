FABLE_ADJ_20261102_576
# ADJUDICATION PASS (F2) -- `shfcnvsdfpul` (#576): the panel shares its pass-2 findings; adjudicate them
F2 VERDICT: RATIFY WITH CHANGES (5)

(The launcher asked for the liveness token and the packet's first line ahead of everything; the verdict line follows them and
closes the file, as the packet asks.)

Seat: Fable 5.1, adjudicator of record for this pass pending GPT-6 Astra's confirmation (Astra on its weekly wall; the owner holds
the commit for it).  Read-only: every source line through `git -C GXEMUL-SEC show HEAD:<path>` at `987cb596`; the staged copies
diffed against their HEAD versions; every file under `regress/artifacts/shfcnvsdfpul/` and the scratch run dir opened; all eleven
`.raw` logs re-read; the manuals by absolute path; the pass-1 and pass-2 answers of all seats read.  The one thing executed was a
parse-only check (`python -I -c "import ast; ast.parse(...)"`) on two copies of the mutator, which runs none of their code.  Nothing
built, run or modified.  Disclosed self-review: P1, P2, P3, P6, P7, P8, P9, P11, P13 and the pass-1 changes F4-F7/F9 are mine; where I
found my own earlier wording weak I say so below rather than defending it.

The product diff is right and complete and stands as it is.  Re-read against HEAD: the handler is `cpu_sh_instr.c:3049-3063`, the
removed store is `:3057`, the only early exit is `FLOATING_POINT_AVAILABLE_CHECK` (`:57-66`), the double store goes through the
`sh_dn` wrapper macro at `:195-196`, and the decoder arm is `:5061-5064` with bit 8 required clear.  Nothing in this ruling touches
the code.  The changes are to records, one preserved artifact and one filing.

## 0. The three verifications the launcher asked for

* **Mutator.**  `killtable_20261102/mutate576.py` is byte-identical to `_scratchpad/w576/mutate576.py` (`cmp` clean, md5
  `1b559e37e53d...`, 2411 bytes each) and both parse.  The driver scripts `run_killtable.sh`, `run_mgm.sh`, `run_probe_leg.sh`,
  `build_fixed_clone.sh` and the preserved `IMPLEMENTATION_PLAN_20261102_1715.md` are each `cmp`-clean against their scratch copies;
  the two witness scripts are identical.
* **Probe row list.**  The staged `sh_rounding_probe.NEW.py` differs from HEAD by exactly two hunks: the `ftrcS-nan` relabel (comment
  plus the name `qNaN+` -> `sNaN+`, oracle untouched) and the `#576` block.  The eight row tuples are byte-identical to the eight
  tuples in the hunk the pass-2 packet inlined from the 17:16:50 instrument (the one the table ran), so the VECTORS row list is
  unchanged apart from the relabel; only the comment text grew.  Note HOW this was established: by comparing against the packet's
  inlined hunk, because the as-run file itself is preserved nowhere (section 3, item a).
* **Gate.**  The staged `gate_sh_rounding.NEW.sh` differs from HEAD by exactly two hunks (`@@ -56,14` and `@@ -77,7`): the pin
  36 -> 52 with its two-line comment and the eight names in the per-row loop, and both prose corrections ("52 vector-mode pairs since
  #576 (36 before it)", "9 of the 25 vectors (17 until #576 ...)") sit inside those hunks.  The working copy's three unrelated hunks
  are at `@@ -527`, `@@ -587`, `@@ -819`, as the packet says; the staged copy carries none of them.

Raw logs: eleven legs, 52 row lines each, no `FAIL(no-readback)`, every header a fresh binary with its own sentinel; every score and
every red set in the packet's section 5 table matches its log.  `base_head.raw` and `M_b.raw` both name md5 `b76a7799a3ea`.
`M_g.raw` reds the five DR2 rows and leaves `0.1` green; `M_gm.raw` reds `0.1` alone; `M_h.raw:50-51` reads `0xffffffff` for `snan`.

## 1. P1..P13, D1..D2

* **P1 UPHOLD.**  Verified as above.  The round-block clause is still OWED: the draft `records_576/CHANGELOG_576.md` (17:32:51)
  does not carry it.  Harder on my own finding: the failed first apply cost the measurement nothing (`M_gm.raw`'s header names a
  fresh binary from the repaired script), so this was artifact integrity only, which is how it was graded.
* **P2 UPHOLD, as disclosure.**  The contract now says what the logs support (M_g 42/52 on the five DR2 rows, M_gm 50/52 on the
  DR0 row alone) and names the unrowed destinations.  The body tests nothing on the destination, so this is clause (e); a filter may
  repair or reject a row and may demand a new row only for a floor cell.  Row additions and re-targeting are D1.
* **P3 UPHOLD.**  The state axes are in the contract.  One precision for the record: FPSCR.FR is modelled by a bank swap inside
  `sh_update_fpscr` (FRCHG at `:3618`), which the cold debugger's `fpscr=` write bypasses, so an FR=1 row would need the guest to
  execute FRCHG; disclosure is the right form for it.
* **P4 UPHOLD.**  Relabel verified; the oracle is unchanged; the gate's loop entry is `ftrcS-nan` and its grep `^ftrcS-nan.*ok$`
  matches both labels.  I grepped for other consumers of the exact old label: only as-run logs (an artifact under `wdclbaaddr`) and
  unrelated m88k/ppc rows that happen to end in `qNaN+`.  Safe.  But see section 3, item a: the preserved raw logs carry the OLD
  label and the preserved probe prints the NEW one.
* **P5 UPHOLD.**  Verified in the gate diff.  Nit, no change ordered: the first corrected comment's breakdown after the colon still
  sums to 36; the parenthetical and the `#576` comment beneath it make that readable.
* **P6 REFINE.**  Withdrawing "17:18" is right: `run_probe_leg.sh` was written 17:17:41 and `base_head.raw` was complete at
  17:18:13 in the scratch run dir, so the base leg ran 17:17:4x-17:18:13 and a file first written in minute 17:18 could not have
  preceded it.  But the disposition's "What is established: PRETABLE.out was written by the tool call immediately preceding the
  base-leg launch" is established by no artifact; it is the author's account, the mtime that would prove it was lost to the in-place
  correction at 17:29:21, and the record must say "by the author's account".  The plan (17:15:08, `cmp`-clean with its preserved
  copy) IS evidenced and is the right citation; say also that it predicted M_f conditionally ("green unless the NODN row exists")
  and predicted neither M_d nor the mirror.  The process note (sibling file, or copy the original before correcting it) is right and
  belongs beside the carrier's PRETABLE rule, whose "its mtime proves the order" collides with "correct in place" exactly here.
* **P7 UPHOLD.**  Verified in `M_h.raw`.  "the one numeric input" is right; "the one finite input" would be equally right.
* **P8 REFINE.**  The product comment's new wording is right, and I could not verify it in any artifact on this side: the scratch
  `product.diff` (17:24:47) and the preserved `build_fixed_clone.sh` both carry the old text; the new text exists in the F2 packet
  and, presumably, in the WSL clone.  The correction also missed its siblings: `sh_rounding_probe.NEW.py:214` still reads "upstream
  residue, the FTRC store mis-copied" and the CHANGELOG draft `:9-10` reads "The line was the FTRC store mis-copied".  The carrier's
  mechanical rule 2 (grep for the siblings before calling it fixed).  Change 1.
* **P9 UPHOLD.**  No row has a finite input of 2^31 or more; "by reading, not rowed" is the honest mark.  Owed in the record.
* **P10 REFINE** (and the most likely wrong accepted disposition, section 2).  Grok's fact holds: no `shfpprreserved` or `shnanquiet`
  row exists anywhere (grep counts 0 in `ledger.json`, `OUTSTANDING_BUGS.md`, `CHANGELOG.md`); my pass 1 wrote "FILE once as a
  class", Astra's wrote "whether it is already recorded is unsettled", nobody filed it.  The filing is owed.  But the row as worded
  asserts an architecture the manual does not state; see section 2.  Change 3.
* **P11 UPHOLD.**  Both headers name `b76a7799a3ea`.  A free consequence for landing: HEAD and M_b differ by a five-line comment and
  share an md5, so the build is insensitive to comment text, and the fixed binary's `303275e8bdbf` is a cross-check for the rebuilt
  trees.  "M_e not built" is right; write "caught by the same channel M_b's toward-zero lines measured", not "by construction",
  which in this project means a gate pin.
* **P12 UPHOLD the rejection.**  `pass1_20261102/codex3/codex_shfcnvsdp1c.txt` exists (12,359 bytes, 17:40:08), opens `VERDICT:
  PROCEED WITH CHANGES (3)`, and its lines 78, 98 and 129 carry the FD/PR disclosure the probe comment attributes to it.  Grok read
  the directory before that file landed: a timing artifact, not a seat error.
* **P13 UPHOLD.**  `inf` stays; the M_d leg (48/52: `inf`, `snan`) is where it earns its sessions.
* **D1 UPHOLD: DISCLOSE.  The re-target is NOT ordered.  Added rows are NOT ordered.**  Explicitly, the three forms: (i) disclosure
  ships, and the sentence in section 3 of the packet is the terminal form; (ii) the zero-session re-target (`inf` to DR14, `snan` to
  DR8, the table re-run) is not ordered; (iii) a `dr0 hi`/`dr0 lo` pair is not ordered.  Reasons.  The body tests nothing on the
  destination, so every destination cell is clause (e), and the rule forbids a filter demanding a row outside the floor, which
  settles (iii).  On (ii), being harder on my own proposal: the re-target closes two of the six open FPUL-channel destination cells
  and none of the DRn-value cells (the FPUL rows never read DRn), so the disclosure sentence stays and only its enumeration moves;
  and a row change made after pass 2 is a detector repair that owes its own pass on the repaired diff plus a re-stamped table of
  record with the prior logs preserved first.  A reopened review chain is the wrong price for two clause-(e) cells.  If Astra asks for
  coverage on Nov 8, the re-target is the cheap form and comes with those three obligations, and its PRETABLE predictions count as
  predictions only for the two re-targeted rows.
* **D2 UPHOLD: withdraw the literal, cite the plan, no re-run**, with P6's wording refinement.  Re-running the table to manufacture
  an order proof would be the laundering shape the oracle-correction rule names; the plan's mtime is real evidence and is enough.

## 2. Which accepted disposition is most likely wrong

**P10, in its content.**  The acceptance is right (the row is owed); what is filed under it is wrong in two ways, and a row filed on a
wrong premise is worked under that premise later.

First, the architecture.  The row says FCNVSD/FCNVDS at PR=0 "convert instead of raising the reserved-instruction exception".  The
manual's pseudocode calls `undefined_operation()` (`sh4_programming.txt:10883`, `:10770`) and never defines it; the hardware manual's one
sentence on a reserved FPU mode combination reads "Reserved (FPU operation instruction is undefined.)" (`sh7750_hardware.txt:8394`,
`:13525`).  No manual line says an exception is raised.  The exception reading is an inference from the fork's own `#316`, which chose
`EXPEVT_RES_INST` for FSRRA at PR=1 (`cpu_sh_instr.c:3279-3295`), an instruction this manual does not document at all.  That is an
inference stated as architecture, the same shape P8 corrects one row up.  "WRONG-RESULT" does not fit an operation the architecture
leaves undefined; the honest class is "undefined by the manual, the model performs the operation, a policy is owed", severity LOW.

Second, the census.  `grep -n undefined_operation _scratchpad/sh4_programming.txt` returns SEVEN sites, not four: FCNVDS 9.28
(`:10770`, PR=0), FCNVSD 9.29 (`:10883`, PR=0), FIPR 9.31 (`:11251`, PR=1), FMAC 9.36 (`:11429`, PR=1), FRCHG 9.41 (`:12234`, PR=1),
FSCHG 9.42 (`:12270`, PR=1), FTRV 9.47 (`:12852`, PR=1).  The row should carry the deriver and let its own round census the handlers
(FRCHG and FSCHG at `:3618`/`:3623` toggle their bit with no PR test; I did not read FMAC's handler and do not claim it).

Runner-up: P6's "What is established", which replaces a wrong number with an unverifiable sequence claim.  Section 1 has the fix.

## 3. What the whole panel missed

* **(a) The instrument the table ran is preserved nowhere.**  Only one probe copy exists in each place (`_scratchpad/w576/` and the
  artifacts dir), both the 17:48 revision; the packet's "both copies preserved beside the table" (section 5) is false as of the
  listing.  `run_probe_leg.sh` ran `$W/sh_rounding_probe.NEW.py` from the volatile scratch dir, so the as-run instrument's identity
  rests on the hunk the pass-2 packet inlined at 17:29.  And the difference shows: the raw logs print `ftrcS-nan qNaN+`
  (`fixed.raw:30-31`, `base_head.raw:30-31`, every leg) while the preserved probe prints `ftrcS-nan sNaN+`, so the preserved probe
  cannot reproduce the preserved logs line for line.  That is P1's class one file over, milder: a label, not a parse failure, and
  the row tuples are byte-identical.  Change 2.
* **(b) P8's siblings** (section 1, change 1).
* **(c) A dropped pass-2 finding.**  Grok wrote that exactly -2^31 (`0xcf000000`) belongs in the disclosed-not-rowed sentence: its
  cast is defined and yields `0x80000000`, it is not a fixed point, and no row has it, yet the contract's "other than -2^31" drops it
  out of the enumeration.  It appears nowhere in P1..P13.  Change 5.
* **(d) The accepted record edits are not applied.**  The CHANGELOG draft (17:32:51) predates every pass-2 answer (17:41-17:46) and
  still says "PRETABLE.out written 17:18 before the base leg", "the one input with a nonzero low word", "the FTRC store mis-copied",
  "filed once as a class", with no "by reading", no M_b/HEAD md5 clause, no "M_e not built", no failed-first-apply clause.  The F2
  packet's section 2 reads as if these were in the record ("the record cites", "marked in the record").  They are owed at landing.
* **(e) The base leg's run is unlogged.**  `KILLTABLE.log`'s "base leg done; fixed leg next 17:18:40" is in the same second as
  "killtable start"; the base leg ran under a separate `run_probe_leg.sh` invocation (17:17:4x-17:18:13) that no log records, which
  is why D2's timing had to be inferred from mtimes.  One sentence in the record.
* **(f) glm's unsettled encoding premise is settled by reading:** the manual's code row `:10866` is `1111nnn010101101` and the
  decoder's `(iword & 0x01ff) == 0x00ad` both require bit 8 clear, so `0xf2ad` is DR2 and `0xf0ad` is DR0; the recalled set-D-bit form
  is wrong.
* **(g)** The witness `RECEIPT.txt` (16:54:50) still ends "The same script must give 6/6 on the fixed build" and was not updated when
  `witness_fixed.out` landed at 17:26:20.  The round block cites both outs, so this is a tidy-up.
* **(h)** Landing premises hold today: `est/src/cpus/cpu_sh_instr.c` is `cmp`-clean against `GXEMUL-SEC`'s, and the SEC working copy
  equals HEAD for that file.

## 4. The five changes

1. **P8's siblings.**  Replace "the FTRC store mis-copied" in `sh_rounding_probe.NEW.py:214` and in the CHANGELOG draft with the
   product comment's form ("the same store FTRC makes, apparently copied").  Leave the as-run `build_fixed_clone.sh` as-run, and say in
   the record that the measured clones carried the pre-P8 comment (comment-only; the HEAD/M_b md5 equality shows the build does not
   see it).  Regenerate `product.diff` from the final clone or drop it from the citations.
2. **Preserve the as-run instrument** beside the table: copy it from `/tmp/gxfix576/regress/` if that clone still exists, otherwise
   reconstruct it as HEAD plus the pass-2 packet's section-3 hunk (whose tuples I verified byte-identical to the shipped rows) and
   name it `sh_rounding_probe.ASRUN_1716.py` with a one-line note; copy `brief_shfcnvsdfpul_p2.md` beside it.  One record sentence:
   the raw logs carry `ftrcS-nan qNaN+`, the as-run label; the shipped probe prints `sNaN+`.  Correct "both copies preserved".
3. **P10 re-worded and re-classed**: undefined by the manual (seven sites, by the deriver), the model performs the operation, `#316`'s
   FSRRA is the fork's precedent for a reserved precision combination, a policy is owed; LOW; not WRONG-RESULT; not "instead of
   raising the reserved-instruction exception".
4. **P6 wording**: "by the author's account" for the PRETABLE order; the mtime loss named; the plan as the evidenced pre-leg record,
   with its conditional M_f and its silence on M_d and the mirror.
5. **The -2^31 clause** in the contract: "finite |v| >= 2^31 (an undefined cast on HEAD, except exactly -2^31, whose cast is defined and
   also gave 0x80000000)".

Landing obligations, not counted as changes: the accepted record edits of section 3 (d); `GXEMUL-SEC` and `est/` byte-identical;
`build/`, `build-asan/`, `/tmp/gxsec-build` propagated and rebuilt with the two-part clearance per tree (`est/`: source tree, part 2
N/A); the SH gate run end to end on the applied tree; the gate staged from the HEAD-based copy; Astra's pass 2 and its confirmation of
this ruling, for which the commit holds by owner ruling.  This adjudication is on four of five mandated seats and is provisional on its
face until Astra answers.

F2 VERDICT: RATIFY WITH CHANGES (5)
