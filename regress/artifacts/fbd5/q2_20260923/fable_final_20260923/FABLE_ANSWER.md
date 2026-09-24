FABLE_FINAL_20260923
# CHECKPOINT -- 2026-09-23 21:50 (087a90 sections rewritten; the peer's sections below are untouched)

VERDICT #545: SHIP
VERDICT census: SHIP

Both SHIP verdicts carry records-only conditions for the commit (no code, no row, no re-table): four for #545 (Q2/Q5), one
sentence plus the owed gate-6 run and a `git add` for the census (Q7/Q8).  If any of those cannot be made before the
commit, the corresponding verdict is HOLD on L4 (wrong record), not on the code.

Seat: Fable 5.1 (claude-fable-5-1), the ninth seat of both passes.  Read-only throughout: nothing under GXEMUL-SEC, est,
build or build-asan was edited, built or run.  Every claim below says what it was checked against.

---------------------------------------------------------------------------------------------------------------------
## ROUND 1 -- #545 (fbdeclinefive): does the chain close on 3e's pass, with 3f?
---------------------------------------------------------------------------------------------------------------------

Premises re-derived rather than ratified: `GXEMUL-SEC/regress/diff_footbridge.c` md5 08329803 == `_scratchpad/fbd5/q2h/
diff_footbridge.r3f.c` (cmp clean); `src/devices/dev_footbridge.c` md5 783c0c7f == the frozen device; `verify_r3f.out`
reads `STRIPPED: identical (41423 bytes)`, both binaries `864 rows, 0 failures DIFF_FOOTBRIDGE_PASS`, `OUTPUT: identical`,
`VERIFY_R3F_DONE`.  `r3f.diff` is 6 hunks and every `+` line is inside a comment (read line by line).  So "3f is records
only" is TRUE, and the instrument under review is exactly the tabled 3e.

### Q1 -- is any of 3e's-pass dissents a FLOOR BREACH?  No.  Checked one by one against the source.

The floor (brief §C.2, the carrier's DEPENDS-ON bound): the predicates DOMINATING the five edited declines, walked to the
function boundary -- the direction test and the site's own latch test under `switch (relative_addr)` -- crossed with the
body-read lvalues of the guarded bodies (the five latches).  The two head statements (`if (writeflag == MEM_WRITE) idata =
memory_readmax64(...)` and the timer fold) do NOT dominate any edited line: both branches of each reach the switch.  So a
variant at the head fetch's LENGTH is not a floor cell; a variant at the head TEST (`&& len == 4`, `!=`) is red on X12's
narrow Clear rows (idata stays 0, `ne` wrong), which I derived from lines 1356-1366.

* grok, `d->irq_asserted = 1` on the IRQ_STATUS read.  Traced every row that reads `irq_asserted`: the line-4 IRQ_STATUS
  row (1529-1539) enters with it 1 and checks `== 1`; the re-arm row (1557-1573) snapshots inside the first `ZDECLINE`,
  after the producer set it 1; the DEVINIT declines rows snapshot AFTER the reads on the same instance (1491-1515) and their
  end check (1513-1514) names the four fields, never `irq_asserted`; X6/X9/X10/X11-X13 and the P-rows never read it.
  Green by reading; the Opus seat's comma form QIASRD2 was measured green on both instruments (addendum.sh, output not
  preserved).  NOT a floor cell -- `irq_asserted` is neither a dominating predicate's operand nor a body-read lvalue of any
  decline -- and NOT a claimed cell: the only row that claims `irq_asserted` at that read enters with it already 1, so the
  store cannot vary the channel.  It is the STORE class 3e already disclosed, and 3f names it.  UPHOLD (disclosed).
* codex dedicated, `data[len] = 0` in the Clear write.  X12/X13 (1358-1370, 1378-1392) poison `b`, write, then check the
  enable, status, FIQ fields and the drive -- no `pad_kept`; X9's and X10's Clear writes (1212-1219, 1312-1317) use an
  unpoisoned `b` and check no pad.  NOBODY BUILT IT: `grep -rl 'data\[len\]'` over `regress/artifacts/fbd5` and
  `_scratchpad/fbd5` finds only codex's answer, the r3f patch and the two record drafts.  An insertion, not a predicate
  weakening or an operand swap -- outside DEPENDS-ON; and COVERED claims the poisoned INPUT ("the buffer's bytes above the
  width poisoned"), never that they stay.  Above the floor.  UPHOLD (filed) -- with the "measured" wording corrected (Q3).
* glm / deepseek, a fetch past `len` at the declined writes.  The four decline arms never read `idata` (the handler as
  inlined; the SEC device is the frozen one), and the harness's `memory_readmax64` stub (lines 72-81) records nothing, so
  no buffer check can ever see it.  3e's COVERED word was "untouched", which a fetch does not violate; 3f now says "no
  write-back past len", which is exact.  Disclosed.  UPHOLD.
* codex, FW03's `EQ` classification.  `irq_enable &= ~idata` truncates bytes 4-7 of an 8-byte fetch, so the guest sees the
  same register; a real word store's `data[4]` is read past.  3f says both halves.  UPHOLD (disclosed); nit under Q2.
* the Opus seat (VENDOR_ID, TIMER_1_VALUE) and the main loop (+0x288, +0x28c).  The tail is code AFTER every arm, not a
  predicate dominating any edited line; measured green on the 864 (`qwb_20260923/QWBVEND.log`, `QWBTMRV.log`, `QWB288.log`,
  `QWB28C.log` each end `864 rows, 0 failures / DIFF_FOOTBRIDGE_PASS`; controls `QIRQST.log` 24 failures, `WB8.log` 144).
  Above the floor.  UPHOLD (filed) -- the instance list is incomplete (Q2).
* codex, grok, agy, kimi-k3:cloud, the Opus seat: the over-broad sentences ("X14's multi-access rows", "checks every field
  ... after EACH access of the multi-access rows", "in X6, X9 and X10 the bytes above the width untouched").  All three are
  rewritten in 3f and each rewrite is true of the rows (Q2).  Wrong records, corrected in place -- L4, not L2.

So every dissent is a wrong record (fixed) or above-floor coverage debt (filed).  My own sweep of the floor, so the zero
carries a denominator: five arms x {direction test, latch test, latch operand} x four states, the Clear body's `&= ~idata`
and drive test, the head test and the timer fold, the common tail's width -- against the 864 rows as read, the 748-variant
r3e table (`r3e_20260923/`, PRETABLE 20:53:58 before the table), the Opus seat's 52 file-backed edits (`q2h_opus/
results_all.jsonl`; QIASRD's build failure correctly excluded) and the codex dedicated job's 37-cell matrix.  Zero floor
breaches surviving adjudication.

### Q2 -- is every sentence 3f changed now TRUE of the 864 rows?  All but two, and two more are imprecise.

Checked against the rows (line numbers of the SEC file today):
* COVERED (912-913) "after X6's declined accesses and X9/X10's legal reads, the bytes above the width untouched: no
  write-back past len (3e)" -- TRUE: `pad_kept` at 1083 (X6, every access, both directions), 1203 (X9 reads), 1299 (X10
  reads); the declines that follow X9's reads and precede X10's are not "legal reads", so the scope is exact.
* (935-936) re-arm "irq_asserted kept -- checked after EACH of its accesses (3e)" -- TRUE: `ZKEPT` after each of the 16
  (ZDECLINE 1460-1464, the reads 1566, the Clear 1569, ZDECLINE again).
* (989-996) the CALLER line, "any condition on caller state that holds for that one fixed caller (and not for a real one)
  passes every row", "ten more shapes over seven fields, two of them grok's" -- TRUE (CX01-CX10 = ten shapes; running x4,
  byte_order, is_32bit, ninstrs, ncpus, pc, cpsr = seven fields; CX02/CX09 are grok's BO1/PC1).
* (997-999) FMT01 "whose declaration carries no format attribute, so no compiler warns" -- TRUE: `src/include/misc.h:262`
  is `void fatal(const char *fmt, ...);`, no `__attribute__` anywhere in misc.h.
* (1004-1005) "Since 3e the three X14 rows that CLAIM kept fields (the DEVINIT declines rows, the re-arm row) check the
  five fields after each access" -- TRUE.
* (1005-1007) "the DEVINIT reads and Set/Clear rows claim values and the drive, so a store there to a field they do not
  name passes (grok, 3e's pass: `d->irq_asserted = 1` on the IRQ_STATUS read)" -- NOT TRUE AS A UNIVERSAL.  Those two rows
  run on the SAME instance as the DEVINIT declines row, whose end check pins `irq_status == 0x18, irq_enable == 0x60,
  fiq_status == 0x60, fiq_enable == 0xc0` absolutely (1513-1514), and X9 checks the four fields after every one of the same
  reads and writes on fresh instances.  A store to any of the FOUR fields at those accesses is red; only `irq_asserted`
  (and the STORE-class state) passes.  Replace with: "so a store there to irq_asserted -- the one field of the five that
  those rows, X9 and X10 never name -- passes (grok, ...)".  Safe direction (it under-claims coverage), but the question
  asked for any untrue sentence and this is one.
* (1008-1016) the `fbbufbounds` line.  "a FETCH past len ... at every declined write" TRUE by construction; "FW03 ...
  equivalent for the guest and a read past a real word store's data[4]" TRUE; "a STORE past len inside a legal write
  (codex ...: X12/X13 poison the buffer and do not re-check it after the write)" TRUE of the source (a reading, and the
  sentence claims no measurement); "and the common tail's write-back past len at a legal read outside X9/X10's five
  registers -- VENDOR_ID (+0x00), the timer value (+0x304; +0x324/+0x344/+0x364 fold onto it), FIQEnable (+0x288) and the
  FIQEnableClear read (+0x28c), which X3 and X7 read with no check above the width" -- the four named are right (X7's LR
  list at 1057-1060 reads all four; X3 at 830-832 reads three of them and WRITES +0x288 at 828, so "X3 and X7 read" is true
  only collectively), the fold arithmetic is right (0x324/0x344/0x364 & ~0x60 = 0x304, and the tail runs after the fold),
  and "an 8-byte write-back keyed on any one passes" is measured.  BUT THE LIST READS AS EXHAUSTIVE AND IS NOT: the timer
  rows at the top of the file read TIMER_1_LOAD (H1/H2, 453-467), TIMER_1_CLEAR and TIMER_2_CLEAR (503-632, "a READ still
  runs the common tail") through the same tail into `unsigned char buf[4]`, read back 4 bytes and check nothing above them
  -- so a write-back keyed on any of those passes too, and overflows the harness's own 4-byte buffer silently, which is
  exactly the WB8-on-3d shape the round already recorded.  Not a #545 arm; a records fix: "among them" plus the timer reads
  named in `fbbufbounds`.
* (1022-1024) FS02 "of the Clears entered with irq_asserted 1, only the Clear 0x10 row reaches that state, and it leaves
  irq_asserted unread on purpose" -- TRUE: the Clears entered with it 1 are line-4 k=0 (0x10: enable 0, nothing pending
  and enabled), k=1 (0x400: keeps 0x10) and the re-arm Clear (0x400); only k=0 reaches the state and its check (1553-1554)
  never reads `irq_asserted`.
* X14 header (1427-1430) "checks every field and irq_asserted after EACH access of the three rows that claim them kept" --
  TRUE.
* macro comment (1450-1451) "a field a row claims KEPT is checked after EACH of that row's accesses, never only at its end"
  -- TRUE of every X14 row; as a universal over the file it is loose: P1-P5's "after #2, byte, halfword -- preserved" is a
  kept claim over three accesses checked once at the end (717-728; carried by X6's per-width rows, so no cell is open).
  Prefix "an X14 row" and it is exact.
* IDENTITY comment (1588-1590) -- TRUE (864, no row added; 3f records only).

### Q3 -- filing `fbbufbounds` rather than rowing it: RIGHT.  Nothing is owed in-round as rows; two records items are.

Row demand is per enumerated floor mutant; all three residual shapes are above the floor (Q1), none is a claimed cell, and
the cheap fix shapes (pad_kept after X12/X13's narrow writes; a length-recording stub for the fetch) are new CHANNELS on
existing rows, which the draft itself says owes a table -- the #462 cost, correctly declined.  Owed instead:
1. `_scratchpad/fbd5/records/bugs_draft545_r3e_additions.md` says "Three shapes stay unobserved, each measured green on the
   864 rows".  Shape (2) was never built (Q1), and shape (1)'s "every declined write" was never built either (FW01/FW02 were
   RED controls at the Clear; FW03 is the one green fetch).  That is the frozen-number class: a prediction in a measured
   column.  Either build `data[len] = 0` in the qwb scratch clone (one gcc and one run, prediction GREEN written first, log
   preserved under `qwb_20260923/`) -- the carrier's under-two-minutes rule says check it -- or reword to "(1) unobservable
   by construction; (2) predicted green by codex, not built; (3) measured green".
2. Add the timer LOAD/CLEAR reads (buf[4] rows) to shape (3)'s list, and "among them" in the 3f sentence (Q2).

### Q4 -- does the chain close on 3e's pass?  YES, and it is a valid closing pass.

* Diff delivered: the brief inlined all 14 hunks; codex reproduced the frozen 15a1c2a2 from them in memory and the Opus
  seat found them == `diff -u` of the two frozen harnesses; I checked the SEC file against the frozen 3e and the r3f copy.
* Roster: eight scriptable transports answered (SEATS.txt: 7/8 plus kimi-k3:cloud covering the weekly-walled kimi CLI --
  `kimi.txt` is the 403 text, not an answer), the dedicated codex job, the Opus measuring seat (first turn fell back to
  claude-opus-4-8 after a refusal; resumed, its verdict and corrections are claude-opus-5-5's; the one measurement the
  records rest on was re-run by the main loop -- `MANIFEST_NOTE.txt` says all of this and the fill repeats it), and this
  seat.  Nine.
* The zero carries its denominator: the Opus seat's 52 file-backed edits over the named arms, tests and tail (corrected in
  place from 53), the main loop's 748 variants with every prediction held, codex's 37 primary cells, and my Q1 sweep.
* Class-closure verification: (A)'s enumeration -- exactly the two DEVINIT declines rows and the re-arm row claim kept
  fields; the reads row claims values, the Set/Clear row the enable and the drive -- verified from lines 1491-1573 by me,
  codex, grok, agy and the Opus seat, and corroborated by CXT1 RED3, IAS01 RED2, QIASRAW RED2 (`results_all.jsonl`).  (B)'s
  contract now names what `pad_kept` covers and what it does not.
No further measurement is a closure condition.  The one I would still run is the `data[len] = 0` build above, for the
records' honesty, not for the floor.

### Q5 -- which of the accepted dispositions is wrong?

1. `cl545_r3pass_fill.md` says 3d's pass "met the CLASS-CLOSURE trigger twice: (A) ... and (B)" AND that "(B) was an
   ABOVE-FLOOR addition".  Both cannot stand.  The trigger is two consecutive passes finding BREACHES of one class.  (A)
   met it (3c's pass: the Clear 0x20 row named the pending status and read it nowhere; 3d's pass: a toggle cancelled across
   a row that claims the fields kept -- two claimed-cell escapes).  (B) had ONE claimed-cell instance (3c's pass, deepseek:
   X12's claimed narrow-Clear cell was indistinguishable with zeros above the width -- repaired by 3d's poison) and one
   coverage-debt instance (3d's pass, kimi-k3:cloud: bytes above the width were never claimed).  Say: (A) met the trigger;
   (B) was closed alongside it by choice, its first instance a contract breach already repaired in 3d, its 3e half and its
   remainder above the floor.
2. "each measured green" in the `fbbufbounds` draft (Q3).
3. "a store there to a field they do not name passes" (Q2).
4. The tail instance list presented as complete (Q2).
5. `qwb_20260923/PREDICTIONS.txt` no longer proves the order for run 1: its mtime is 21:40:21 (the qwb2 section was appended
   after run 1's logs at 21:38:31-35), so "predictions first" for WB8/QIRQST/QWBVEND/QWBTMRV rests on the file's text.  The
   Opus seat's own `q2h_opus/PREDICTIONS.txt` (21:20:26, before any 3e build) predicted QWBVEND/QWBTMRV GREEN-REAL, so cite
   that for the two that matter; run 2 (QWB288/QWB28C, 21:40:31-33) is proven by the same mtime.  Next time a second run's
   predictions go in a second file.  (`attempt1/NOTE.txt` records the first apparatus failure honestly.)
Minor, not wrong: the QIASRD2 measurement behind grok's example is unpreserved -- the 3f sentence claims only a reading,
which is correct; the fill's flat "passes" would be better as "passes by reading; measured green, output unpreserved".

---------------------------------------------------------------------------------------------------------------------
## ROUND 2 -- hygienecensus: F6e under the owner's "one more pass, then file"
---------------------------------------------------------------------------------------------------------------------

Premises re-derived: the SEC files equal `c6e_frozen/` (derive 2c37a208, gate cdd91ba3, census_tokens ea579526);
`f6e.diff` is 8 + 1 + 1 = 10 hunks; `controls_c6e/PREDICTIONS.txt` mtime 21:48:47 precedes every result (first
`t_dfwrite_F6e.out` 21:52:39, RESULT.txt 21:56:09) and RESULT.txt says every part held -- I read the two `t_dfwrite`
outputs: F6d prints `Exception ignored ... OSError: [Errno 27] File too large` then `WRITTEN ... DERIVE_DONE`; F6e prints the
traceback then `DERIVE_FAIL: the writer failed (rc=1); nothing to trust in <gate>`.  The BOM witness really begins
`ef bb bf` (od on `regress/artifacts/wdcaltdigin/agy_altdigin_witness_20260911.py`).  `_ptylist` (gate 454-455) is relative
to regress/ and greps `pty.fork` only, while `pty_driving()` (712-714) greps `pty\.fork|forkpty|pty\.spawn|import drive_guest`
-- which is why FIX-A' refusing `forkpty|pty\.spawn` on a name that left `_ptylist` mirrors the gate's own population term,
and why `t_k14release` still refuses on F6e (the name is in `_ptylist`, the parser runs).

### Q6 -- is each classification right under the ruling?  Yes, all of them.

REAL, fixed: codex's swallowed close-time flush (measured both ways, above); the Opus seat's F1 (a committed real file
with a BOM; `utf-8-sig` reads a BOM-less file identically, so nothing else moves -- RESULT part A/B); F2 (a real refactor
onto drive_guest; S8b/S8c now RELEASED with a green gate, S8a and `t_ptyspawn` refused with a true message); F3 (messages
by rc, both modes).  FILED as exotic, each checked against the ruling's four classes: the crafted split name (`:` is not
an NTFS filename byte, so git-bash and WSL-on-/mnt/c cannot even hold it); PYTHONOPTIMIZE (an env var nobody sets, and
harm needs a hand-edited duplicate line too); a classifier that dies part-way (a broken tool); hand-edited layouts; the
`eval` of the gate's own list (43 names, 0 bytes outside the allow-list, `t_gpbytes`).  The three F6d-pass residues: "any
`.endswith(` is readiness" is the census's DEFINITION (§C.2), symmetric in gate and deriver, pre-existing -- filed rightly;
the match-pattern wedge needs a spelling no probe uses and fails CLOSED -- filed rightly; grok's unquoted `$whole_files` in
the gate's awk line -- 0 of today's two tokens carry a glob byte, NTFS forbids `*`/`?` (not `[`, but a bracketed name only
expands if a file of the expanded spelling exists), and the deriver refuses any token outside `name:count` before a write --
LOW is right.

The truncated-gate residue: FILED CORRECTLY, and for the right reason.  It is not exotic -- a full disk is ordinary use --
and the drafts do not call it exotic: `bugs_census_holes_addition.md` appends it to `hygienecensusholes` and says "filed by
owner ruling: one more pass, then file".  The finding the pass made (codex) was success printed over a truncated gate; that
is fixed and measured.  The non-atomic write was found by the main loop's own post-pass control, so it is a post-pass
finding, which the ruling files; and by the brief's own harm definition (a wrong pin, a wrong name listed or released, a
failure reported as success) a loud rc 6 naming the gate, with the gate recoverable from git, is not harm.  If the owner
wants it anyway it is about four lines (write `g + ".tmp"`, `os.replace`) plus a re-run of `t_dfwrite`/`t_dfgrand`; under
the ruling as given, filed.

### Q7 -- does F6e itself do anything wrong?  One F6e comment is false; two are imprecise; the code is right.

* FALSE (deriver lines 35-37): "the ruling and change note (printable ASCII without `"`, `\`, `$` or a backtick)".  The
  sink (319) checks the ruling with `[ !#%&-\[\]-_a-~]*` -- printable ASCII minus exactly those four bytes -- but the
  change note with `[ -~]*`, ALL printable ASCII.  The parenthetical is true of the ruling and false of the note.  Replace
  with "the ruling (printable ASCII without `"`, `\`, `$` or a backtick) and the change note (printable ASCII)".  This was
  the sentence rewritten to answer deepseek, and deepseek's own claim was also wrong: the shell refuses those four bytes
  in a ruling at line 98 before the sink ever sees them.
* Imprecise (21-22): "a glob character expands wherever a list is printed unquoted (this tool's and the gate's printed
  lists run under `set -f` since F6b ...)".  The gate's `whole_full=$(printf '%s\n' $whole_files | awk ...)` (721) is an
  unquoted list not under `set -f` (grok's residue, disclosed in the draft), and the UNTRACKED list got `set -f` in F6c.
  "the four lists a reader sees ... since F6b/F6c" would be exact.
* Nit, refusal direction only: FIX-A' tests `grep -qE 'forkpty|pty\.spawn'` as text, so a refactored probe whose COMMENT
  mentions either word is refused with a message that is then false.  Needs that comment; exotic; no action.
Everything else checked TRUE against the code: the `--grandfather` rc-0/rc-2 messages (231-232), the `--release` branch and
its comment (235-247), the `utf-8-sig` note (187-189, and "as Python itself reads a script" is right), the S14 sentence
(132-134), the clean-0 sentence (148-151: every checked value ends in a counter), the two `with` comments, the gate's
"never by hand" message, and the census_tokens docstring's "Since F6b the deriver re-checks ... and refuses it".

### Q8 -- anything that must still be fixed before this round commits?

1. The one-line header fix in Q7 (records).
2. The owed gate-6 run on the final SEC files -- the F6d brief listed it as owed; c6e ran the gate on copies (the Opus
   matrix under WSL; `t_gbwrite`'s tree 0 FAIL of 12) but not on the tree being committed after F6e's gate edit.  A run,
   not a review pass; the carrier's per-commit targeted gate.
3. `git status` shows `?? regress/census_tokens.py` and `?? tools/derive_hygiene_pins.sh` -- UNTRACKED, so the commit must
   `git add` them or the gate ships calling a classifier that is not in the repo.
4. The round record must say F6e had NO panel pass by owner ruling and was reviewed by this seat only, by name.

### Q9 -- which of the dispositions is wrong?

The one that accepted "the sink grammar ... named truly": the rewritten sentence is true for the ruling and false for the
note (Q7).  Every other classification stands; the truncated-gate filing is right and correctly NOT labelled exotic.

---------------------------------------------------------------------------------------------------------------------
## Files read, and what I ran
---------------------------------------------------------------------------------------------------------------------

Read: the brief; `_scratchpad/CHECKPOINT.md` (first line); `fable_final_20260923/r3f.diff`, `f6e.diff`;
`panel_20260923_210234/` -- SEATS.txt, brief_sent.md, codex.txt (last 12 KB), grok.txt, ollama_glm.txt,
ollama_deepseek.txt, ollama_kimi.txt, ollama_minimax.txt, agy.txt, kimi.txt; `_scratchpad/fbd5/q2h/codex_ded/codex_r3e.txt`;
`GXEMUL-SEC/regress/artifacts/fbd5/q2_20260923/q2h_opus/` -- MANIFEST_NOTE.txt, PREDICTIONS.txt, SUMMARY.txt,
brief_shapes.out, analysis.txt (head), results_all.jsonl (the FW/QWB/QIAS/QTAIL0/IAS entries), addendum.sh;
`qwb_20260923/` -- PREDICTIONS.txt, RUN.out, RUN2.out, run.run-2.sh, run2.run-214021.sh, attempt1/NOTE.txt and RUN.out,
the tails of all eight logs; `r3f_20260923/verify_r3f.out`, verify_r3f.sh; `_scratchpad/fbd5/records/
bugs_draft545_r3e_additions.md`, cl545_r3pass_fill.md; `GXEMUL-SEC/regress/diff_footbridge.c` in full (1601 lines);
`GXEMUL-SEC/src/include/misc.h` (the `fatal` declaration); `regress/gate_offline.sh` (the footbridge pin block);
`panel_20260923_202350/` -- SEATS.txt, brief_sent.md, codex.txt (last 10 KB), grok.txt, ollama_glm.txt,
ollama_deepseek.txt, ollama_kimi.txt, ollama_minimax.txt, agy.txt, kimi.txt; `_scratchpad/census0923/codex_ded/codex_c6.txt`;
`_scratchpad/census0923/opus_c6/SUMMARY.txt`, PREDICTIONS.txt (head); `GXEMUL-SEC/regress/artifacts/hygienecensus_20260923/
controls_c6e/` -- PREDICTIONS.txt, RESULT.txt, SUMMARY_new.txt, TABLE.txt, TABLE_new.txt, run_gb.log, t_gitbash_c6e.txt,
t_dfwrite_F6d.out, t_dfwrite_F6e.out; `_scratchpad/census0923/bugs_census_residue_draft.md`,
bugs_census_holes_addition.md; `GXEMUL-SEC/tools/derive_hygiene_pins.sh` in full; `GXEMUL-SEC/regress/census_tokens.py` in
full; `GXEMUL-SEC/regress/gate_hygiene.sh` lines 440-500 and 700-730 plus greps for its census lines.

Ran (read-only): `ls -la` of every directory named above; `head -1` of CHECKPOINT.md; `md5sum`/`cmp` of the SEC
diff_footbridge.c against the r3f copy and the frozen 3e, of dev_footbridge.c against the frozen device, and of the three
census files against `c6e_frozen/`; `od -An -tx1` of the BOM witness's first four bytes; `stat` mtimes in `qwb_20260923/`
and `controls_c6e/`; `grep -rl 'data\[len\]'` over the fbd5 artifacts and scratch; `grep` for `fatal`/`__attribute__` in
misc.h and debugmsg.c; a python one-liner listing the FW/QWB/QIAS entries of results_all.jsonl; `wc -l` of the six source
files; `git status --porcelain`, `git ls-files`, `git cat-file -e HEAD:...`, `git log --oneline -3`, `git diff --stat HEAD`
on the round's files.  No build, no gate, no probe, no edit anywhere but this answer file.
