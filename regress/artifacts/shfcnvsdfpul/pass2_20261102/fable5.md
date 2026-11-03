FABLE_SEAT_ALIVE_20261102_P2
# PANEL PASS 2 -- `shfcnvsdfpul` (#576): the real diff, the detector, the pre-table check and the measured kill table

VERDICT: SHIP WITH CHANGES (3)

Seat: Fable 5.1, file-reading, pass 2, read-only. Disclosed self-review: F4, F5, F6, F7 and the filed F9 are my pass-1 findings. Tree:
`GXEMUL-SEC` at HEAD `987cb596` (confirmed by `git log`); every source line through `git show HEAD:<path>`; the two scratch files diffed
against their HEAD copies; every file under `regress/artifacts/shfcnvsdfpul/` opened, and the eleven raw logs compared byte for byte
with the scratch run dir (`_scratchpad/w576/killtable_20261102/`, all identical); manuals by absolute path. Nothing built or run; the
one thing I executed was a parse-only check (`ast.parse`) on two copies of a script, which runs no code.

The product diff is right and complete; ship it as it stands. The eight rows, their encodings, wants and the gate pin are right; every
score in section 5 reconciles with its raw log. The three changes are to artifacts and records, none to code:

1. ARTIFACT INTEGRITY, before the commit. The mutator preserved in the artifacts dir cannot run.
   `killtable_20261102/mutate576.py` (2409 bytes, 17:24:47) has a real newline inside the M_gm string at line 25 (the carrier's
   backslash-consumed-on-the-heredoc-path trap); `ast.parse` rejects it with "unterminated string literal (detected at line 25)". A
   file that does not parse cannot apply ANY leg, not only M_gm, so the preserved table is not reproducible from the preserved script.
   The scratch copy `_scratchpad/w576/mutate576.py` (2411 bytes, 17:25:30) parses and is the one that applied M_gm at 17:25:53.
   `KILLTABLE.log` carries the honest trace (`M_gm APPLY-FAILED`, the traceback, then `applied M_gm`); the packet's section 5 and the
   CHANGELOG draft say nothing about it. Copy the fixed mutator over the preserved one (`cmp` against the w576 copy) and add one clause
   to the round block naming the failed first apply.

2. THE CONTRACT OVERCLAIMS THE DESTINATION AXIS, and the ask-again lands exactly there. The probe comment says "a destination-keyed
   re-introduction of the store is seen from both sides". That is true of the two-cell split {DR0, not DR0} that M_g and M_gm measured
   and false of the register: the rows use DR0 and DR2 only, so
   `if (ic->arg[0] == (size_t)&cpu->cd.sh.fr[4]) cpu->cd.sh.fpul = (int32_t) op1.f;`
   keeps all 52 rows green and corrupts FPUL on the first FCNVSD FPUL,DR4 the guest runs (FPUL 0x3fc00000 becomes 0x00000001). The same
   holds for a store keyed to FPSCR.SZ, FPSCR.FR, any FPSCR cause/enable/flag bit, or `cpu->delay_slot`: no row varies any of them.
   Every one of these is clause (e) by the rule's letter (the body tests none of them, so no row is owed), but the disclosure list names
   VALUE classes only; it must name these STATE axes too, and the "both sides" sentence must say "DR0 and DR2". One sentence in the
   probe comment, zero sessions, and it does not change the instrument the table measured. Optional, L1 pre-ship, if the adjudicator
   wants coverage rather than disclosure: re-target `inf` to DR14 (0xfead, fr14/fr15 seeded) and `snan` to DR8 (0xf8ad, fr8/fr9), zero
   added sessions, and re-run the ten legs (about six minutes by the log); that also gives `inf` a second job, which answers F8 from
   the other side. I own this gap: F4 and F7 were mine, and F7 enumerated values and forgot state.

3. RECORDS: four sentences in the CHANGELOG draft (`_scratchpad/w576/records_576/CHANGELOG_576.md`) and the packet.
   (i) "`PRETABLE.out` written 17:18 before the base leg" is supported by no surviving timestamp and is in tension with one.
   `base_head.raw` was complete at 17:18:13 (scratch run dir mtime, the `LEG_DONE` write); a 52-session leg takes about 30 s (M_b:
   binary 17:19:19, log complete 17:19:49; M_c: 17:19:52 to 17:20:22), so the base leg started about 17:17:43; and `PRETABLE.out`'s
   own mtime is 17:29:21, because the correction was written into it in place, which destroyed the order proof the mandate relies on.
   A file first written in minute 17:18 cannot have preceded a leg that started at 17:17:4x, so at least one of "17:18" and "before the
   base leg ran" is wrong. What CAN be shown: `IMPLEMENTATION_PLAN.md` (17:15:08) carries the base, fixed and mutant predictions
   before any leg ran, and the wrong M_g prediction shows the mutant block predates the M_g leg (17:21:32 to 17:22:01). Write that.
   (ii) "0x3dcccccd ... the one input with a nonzero low word" is false: `snan` widens to the shared encoder's all-ones NaN, whose low
   word is 0xffffffff, and `M_h.raw:50-51` measured exactly that word landing in FPUL. Say "the one numeric input".
   (iii) "the FTRC store mis-copied" is stated as fact in the product comment and the round block; it is an inference from an
   identical line (`git log -L` shows only the import). "the same store FTRC makes, apparently copied here" is the honest form.
   (iv) "the host's indefinite 0x80000000 for ... finite values of 2^31 or more" is by reading (the ftrc comment, the x86-64
   indefinite), not by measurement: no row has such an input. Mark it so.
   Nits, not counted: keep "UB" attached to FCNVSD's side in the F1 correction (FTRC's cast is no longer UB; FCNVSD's was, for Inf,
   NaN and |v| >= 2^31 other than -2^31); the gate's :66 comment "EXACTLY 9 of the 17 vectors" becomes 9 of 25 with this commit.

## Q1, the diff

The edit is right and complete. HEAD :3056-3057 are `ieee_interpret_float_value(cpu->cd.sh.fpul, &op1, IEEE_FMT_S);` and
`cpu->cd.sh.fpul = (int32_t) op1.f;`; the diff removes :3057 and puts a five-line comment in its place (+5 -1, hunk `-3054,7 +3054,11`,
both consistent). After the edit the handler is :3049-3067 as section 2 shows, and I re-read it against HEAD line by line.

Other observables: none change.
* DRn: `ieee_store_float_value(op1.f, IEEE_FMT_D)` consumes `op1.f`, which the deleted cast read and never wrote; the result is
  byte-identical for every input. Note this call IS on `sh_dn()`'s path: `ieee_store_float_value` is a macro at `cpu_sh_instr.c:195-196`
  wrapping `sh_dn(cpu, ...)`, so the PRETABLE's "sh_dn()'s DN test and fpclassify live in callees" is correct (I checked this because I
  was about to call it wrong; the macro is what makes it right). `sh_dn` cannot touch a widened single (biased D exponent 874..1151, or
  zero/Inf/NaN), so DN does not enter, on either build.
* FPSCR: the handler never writes it, before or after. (The architecture's `clear_cause()`, `set_E()` and `invalid()` write FPSCR
  cause/flag bits in the DENORM and sNaN arms; this model implements none of them, on either build. The comment's "writes DRn only" is
  exact about the code and slightly stronger than the manual about the architecture; the round block's "not changed" paragraph is the
  place for that, and it already names the exception model.)
* Exceptions: `FLOATING_POINT_AVAILABLE_CHECK` (:57-66) is the only exit before the body and is untouched; FD is clear at reset.
* The only route by which the fix could change DRn at all is a compiler having exploited the removed UB on HEAD (Inf, NaN, |v| >= 2^31
  inputs). Unmeasured, since no DRn row has such an input; any such change would be in the defined direction, and HEAD's measured DRn
  halves for 0.1 agree with the fixed build's.

The comment: "reads FPUL and writes DRn only" matches the code; "(sh4_programming.txt 9.29, :10866-10871)" is the right section and
the right lines (`:10854` is the 9.29 heading, `:10866` the code row, `:10870-10871` the description); "a guest reading FPUL after an
FCNVSD saw a truncated integer" is true for finite in-range inputs and loosely true for the specials (the host's indefinite);
"Removed; nothing else in this handler changes" is true of the diff. The one word I would change is "mis-copied" (change 3 iii).

## Q2, the floor

No floor cell is open. The floor is the cross-product of the dominating predicates with the body-tested partitions: the one dominating
predicate is `sr.FD`, whose only reachable cell at the body is FD = 0 (FD = 1 returns from the macro before the body on both builds, so
a store re-introduced under FD = 1 is dead code, not an escape); the body tests nothing on any lvalue (`fpul`, `ic->arg[0]`, `fpscr`
are read in callees or not at all). So the floor is one cell and every one of the 52 rows sits in it.

Verified against the raw logs (not the packet), every leg 52 row lines, a fresh binary (`binary newer than cpu_sh_instr.c: yes`), a
distinct md5 and its own sentinel, no `FAIL(no-readback)` anywhere, `SH_ROUND_DISCRIMINATING=9` in all eleven:

* (a) `base_head.raw` 40/52: the six FPUL rows red in both modes with exactly the predicted HEAD values (0x00000001, 0xffffffff,
  0x00000000, 0x00000000, 0x80000000, 0x80000000). This also settles my pass-1 unsettled premise: the `inf` and `snan` pre-fix values
  ARE the host's indefinite.
* (b) `M_b.raw` 40/52, the same six rows with the same values. And a stronger fact than the score: M_b's binary md5 is `b76a7799a3ea`,
  IDENTICAL to the HEAD binary's (`base_head.raw` header). The reinstatement is verbatim at the binary level, not only at the source
  level (a comment is the only source difference, and the build is reproducible enough to show it).
* (c) `M_c.raw` 48/52: `dr hi`/`dr lo` red with 0xdeadbeef in both modes, every FPUL row green. The identity body is the right null
  medium for an instruction-handler round, it came back RED, and the contract names the two DRn rows as its only carriers. Measured,
  not by construction.
* (d) the fix is a pure deletion, so (d) is the removed store under a different predicate: `M_f.raw` 50/52 (`-0` alone, both modes),
  `M_g.raw` 42/52 (the five DR2 rows: 1.5, -1.5, -0, inf, snan), `M_gm.raw` 50/52 (`0.1` alone), `M_z.raw` 50/52 (`-0` alone),
  `M_d.raw` 48/52 (`inf`, `snan`). All red. Note M_f's mirror (store only with DN SET) was not built; it is caught by construction,
  since the five DN=1 rows red under the unconditional store (M_b) and would red the same way under a DN=1-conditioned one.
* The other two: `M_h.raw` 40/52 (all six FPUL rows; snan reads 0xffffffff, the all-ones NaN's low word) and `M_i.raw` 48/52
  (`dr hi` 0xa0000000, `dr lo` 0x3fb99999, the halves exchanged). `fixed.raw` 52/52.

Nulled-repair forms that escape all 52 rows: the DR4-keyed store in change 2 (first differs at FCNVSD FPUL,DR4 with FPUL != +0); a
store keyed to FPSCR.SZ (first differs at SZ = 1, bit 20); to FPSCR.FR (bank 1); to `cpu->delay_slot` (FCNVSD in a delay slot); and the
value-class forms already disclosed, e.g. `if (op1.f >= 2147483648.0)` (first differs at 0x4f000000) or `isinf(op1.f) && op1.f < 0`
(0xff800000). None is inside the floor; the first four are not yet disclosed, which is change 2.

## Q3, the ask-again (one, capped)

The smallest edit to the FIXED handler that keeps all 52 rows green and changes guest-visible behaviour is one line:
`if (ic->arg[0] == (size_t)&cpu->cd.sh.fr[4]) cpu->cd.sh.fpul = (int32_t) op1.f;` (any of DR4..DR14 in place of `fr[4]`). First
differing input: the first FCNVSD FPUL,DR4 with FPUL other than +0, e.g. FPUL = 0x3fc00000 leaves FPUL = 0x00000001 where the fixed
handler leaves 0x3fc00000. No row catches it. It is clause (e) material, but it is NOT written in the contract: the contract's sentence
claims the destination axis is "seen from both sides", and the disclosure list is value classes only. So the third answer the packet
did not offer applies: disclose it (change 2), and if a row is wanted, re-target two existing rows at zero added sessions rather than
add any. The destination family has eight values and six FPUL rows cannot close it; disclosure is the honest terminal form whatever
the owner decides about re-targeting.

## Q4, the records

Section 6 and the draft `CHANGELOG_576.md`, sentence by sentence against the artifacts and the code:

* Defect paragraph: `:3049-3063`, `9.29 :10866-10871`, the pseudocode assigning only `DR[n>>1]` (`:10903`), the measured values for
  1.5 / -1.5 / 0.1 and the specials, `#297` GUARDED (the casts remain at `:3016` and `:3038`, verified at HEAD; the ladder is
  `:2996-3014` and `:3020-3036`): all true. "finite values of 2^31 or more" gave 0x80000000 is by reading (change 3 iv); "the FTRC store
  mis-copied" is an inference (3 iii). Incidentally -2^31 exactly (0xcf000000) is a DEFINED cast to INT32_MIN and also reads back
  0x80000000, so the sentence is true of the pattern on both sides of the definedness line.
* Witness paragraph: `witness_head.out` RESULT=3/6 with the three FPUL rows FAILED-FOR-THE-REASON-UNDER-TEST, `dr hi`/`dr lo` and
  `fcnvds ctl` ok; `witness_fixed.out` RESULT=6/6; same script (the two copies of `sh_fcnvsd_witness.py` are identical), binaries fresh,
  unmodified `-E landisk`. Clause (i) met; clause (ii)'s liveness control is the DRn pair and the attribution control is the FCNVDS row
  (0x3fc00000 could only come from the sibling's conversion). True.
* Fix paragraph: "+5 -1", "nothing else in the handler, its sibling or the decoder (:5061-5068) changes", the option-set sentence:
  true. "byte-identical in GXEMUL-SEC and est/" is a commit-time obligation, not yet an artifact.
* Detector paragraph: eight rows, PR on all, both modes, NODN on `-0`, DR0 on `0.1`, both halves seeded, `snan`: all true of
  `sh_rounding_probe.NEW.py` (the diff against HEAD is exactly the one block). Gate: pin 36 -> 52 by EQUALITY, eight names in the
  per-row loop, disc 9: true of `gate_sh_rounding.NEW.sh` (exactly two hunks against HEAD; the working copy's three unrelated hunks are
  at `@@ -527`, `@@ -587`, `@@ -819`, consistent with the packet's "old :530/:590/:822"). "the one input with a nonzero low word" is
  false (change 3 ii).
* Pre-table and table paragraph: the eleven scores and red-row lists are true of the logs (above). "written 17:18 before the base leg"
  is not supported (change 3 i). "`PRETABLE.out` predicted every score but M_g's direction" is true: base 40, fixed 52, M_b 40, M_c 48,
  M_d 48, M_f 50, M_h 40, M_i 48, M_z 50 all matched, M_g 42 against a predicted 50, and the correction is in place quoting what it
  refutes. "M_gm was built after the table" is true (17:25:53 against `KILLTABLE_DONE 17:23:41`). The missing sentence is the failed
  first apply (change 1). One PRETABLE detail worth a word: its CHANNEL line names `M_e` (an RZ-only store) as a mutant `1.5` kills;
  M_e was never built. It is caught by construction (every row runs both modes), but the record should say "not built".
* Records paragraph: the `:24069` id entry exists; the `:8240` prose row carries the "removed from FTRC" wording and the correction
  must quote it (the packet says it will); `SCOPING.md:47` carries the same wording; the ledger has the `shfcnvsdfpul` row; the
  `#548` gate-staging recipe is the right one. True.

F1's wording is right: "the same `(int32_t)` cast that `#297` GUARDED in FTRC behind a range ladder (the casts remain at :3016 and
:3038)" is exactly what HEAD shows. Keep "UB" on FCNVSD's side (nit above), and when the row is corrected, date its `:3057` citation
("at HEAD 987cb596; removed by #576"), since :3057 is the comment's first line after the fix.

F8, keeping `inf`: the rejection is right, and the reason is measured, which my pass-1 argument was not. I argued from cost; a leg of
52 sessions plus a rebuild took about 30 s in this table, so the two `inf` sessions cost about a second. On value: `inf` is the only
+Inf representative, the only non-NaN row whose HEAD value is the host's indefinite, and the only row that would red an Inf-only
re-introduction (`if (isinf(op1.f))`), which `snan` would not. Keep it; and if change 2's optional re-targeting is taken, `inf` is the
natural row to carry a third destination.

Harder on my own adopted findings, as asked. F4 (the DR0 row): it did exactly what it was added for (M_gm 50/52, the DR0 row alone)
and M_g is caught by the DR2 rows; but the contract generalised "both forms" to "both sides", which overclaims, and that is downstream
of my wording. F5 (NODN on `-0`): M_f 50/52 caught by that row alone; its DN-set mirror is by construction, not built; fine. F6
(`snan`): the manual at `:4980-4981` is unambiguous; the label is right. F7 (disclosed classes): incomplete; it listed values and
not states, which is change 2. F9 (filed): `M_h.raw` is a measured confirmation of its premise, the D NaN result's low word is
0xffffffff, the all-ones pattern.

## Q5, the roster

Nothing here needs Astra specifically. The standing rule holds the commit until the roster completes or the owner exempts, and that
is the only hold I see. Change 1 must land before the commit regardless of Astra, because the commit would otherwise preserve a
script that cannot reproduce the table it documents. Changes 2 and 3 are comment and record edits that do not invalidate any
measurement. If Astra's window runs long, the four-seat pass 2 plus Astra's later answer under the late-dissent rule suffices; the
owner's exemption is the mechanism, not a judgement I can make.

## Found while checking

1. The M_b binary is byte-identical to the HEAD binary (md5 `b76a7799a3ea` in both headers). That is the strongest possible form of
   clause (b): the mutant IS the pre-fix build. Worth one clause in the round block.
2. `IMPLEMENTATION_PLAN.md` (17:15:08) predicted M_g correctly ("FPUL rows red (DR2 is used)"); `PRETABLE.out` three minutes later
   inverted it. The plan is therefore the better provenance artifact for the predictions and should be the one the record cites.
3. The in-place correction of `PRETABLE.out` is the right records form (quote what you refute) and the wrong artifact form: it
   overwrote the one mtime the mandate says proves the order. Future rounds: write the correction to a sibling file
   (`PRETABLE_CORRECTION.out`) and leave the original's mtime alone. Process note, not a change to this round.
4. `KILLTABLE.log` is honest about the failed apply and the packet is silent about it; the log is the record that saved this.
5. The gate names are used as regexes in `grep -c "^$v.*ok$"`; the `.` in `1.5` and `0.1` is a metacharacter. Harmless today (no other
   row begins `fcnvsd fpul 1`), noted so nobody adds one later.

## Premises I could not settle

* Whether any guest depends on FPUL holding the truncated integer after FCNVSD: the tree cannot say; no guest source read.
* The DRn value on HEAD for Inf and NaN inputs: no DRn row has one, so whether the removed UB had any effect on DRn there is unmeasured
  (irrelevant to the fix's correctness, relevant only to the sentence "DRn is unchanged", which is proven for 0.1 and argued for the
  rest).
* Astra's state: `codex2`/`codex3` launch logs exist in the pass-1 dir; I did not read them and take the packet's account as given.

VERDICT: SHIP WITH CHANGES (3)
