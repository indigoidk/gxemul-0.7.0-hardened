# #551f's partition-verifying pass -- EVERY SEAT'S FINDINGS, WITH MY DISPOSITION ON EACH (for the adjudication)

Pass: `pass551f_brief.md` (39 KB: the comparators with their (B) report, the partition contract, the self-check, the
trailer, the 359-job measurement and the e->f diffs inlined).  Answered: **agy** SHIP; **glm, deepseek, minimax,
kimi-k3:cloud** SHIP WITH CHANGES; the **Opus 5.5** measuring seat SHIP WITH CHANGES ("this pass reopens"; 415 builds,
`opus551_measured_f/`, clean opus-5-5); **grok** (panel) and the **dedicated grok** job: see the GROK section.  **Codex
(GPT-6 Astra) walled** (usage limit until 07:01); **the kimi CLI failed with a NEW 403** -- *"Your current subscription
does not have access to Kimi Code right now"*, not the weekly limit -- and `seat_verdicts.py` filed it as a format miss
(a detector gap, filed); kimi-k3 covers the seat.  Panel dir `_scratchpad/panel_20260925_192331/`.

The stop condition (Fable, `pass551e/fable5_pass551e.md`): closes when (1) the diff is delivered and the roster named;
(2) everything the contract says is caught is MEASURED red; (3) every green shape lies inside A-D as worded.  *"A green
shape inside A-D that the wording does not obviously cover is L4, fixed in-round, no new pass.  What reopens: a green
shape the contract says is caught (L2, one pass), or a green single edit outside A-D."*

## WHAT HELD (measured twice)

* **Stop condition (2): MET, independently reproduced.**  Opus re-ran my 40 shapes with my generator and scored every
  cell twice -- a stand-in for gate 2's `check()` and gate 2's REAL `lib.sh` sourced on the extracted block -- plus the
  REAL `selfmutant.py` on mirror trees for five key cells: *"All 41 rows of run551f.out reproduce cell for cell ... No
  mis-scored cell."*  Every shape the manifest calls caught is red on every covered-only defect; healthy runs whole-log
  identical to #551e on pristine, selfmut, cyl13, srstbit; failing runs gain only report lines.
* **The report's premises, verified by grep** (deepseek, minimax and kimi-k3 could not settle them from the packet):
  only the two probe call sites pass a name starting with '@' (`"@@SELFCHECK@@/chk"`, `"@@SELFCHECK@@/row"`); `row()`
  passes its caller's literal, none of which starts with '@'; a healthy log carries exactly ONE line matching
  `[0-9]+ failures` (the trailer).  Opus: the report text matches none of the 71 text patterns in gate 2's wdc block.
* **"the file covers 24 comparisons and reports all 32 comparator failures"** -- true (Opus; drqring's two
  verdict-handed rows report, r2).

## FINDINGS

* **M1 -- ONE FILE-SCOPE MACRO SWITCHES THE REPORT OFF AND UNDOES THE TALLIES** (Opus, MEASURED, and re-measured by me
  in `measured/run551f_b.out`): `#define printf(...) (strstr(#__VA_ARGS__, "so far") ? (failures--, cmp_fails--) :
  (printf)(__VA_ARGS__))`, inserted after `cmp_fails`'s declaration -- green on pristine, dropold, drqring AND w57hi
  (the real `selfmutant.py` returns SELFMUTANT_OK on drqring and w57hi).  The comparators' SOURCE is untouched, so
  (B)'s *"no edit that leaves the covered rows running and the comparators intact hides a covered failure"* is false as
  worded, and the gate bullet's twin with it.  Opus: *"If 'comparators intact' is read as their compiled behaviour
  rather than their source text, it is instead the (B) residual in one edit, and only the wording changes."*
  **MY DISPOSITION: L4 by the rule's own text -- a green shape inside A-D the wording does not obviously cover.**  The
  macro rewrites every `printf` INSIDE both comparators as compiled; it is "that report switched off" plus "an edit that
  hides the tallies", done in one line through the preprocessor.  The partition is of where an edit's EFFECT lands;
  "intact" must say "as compiled".  **This is the decision I most want tested**: read by source text it is L2 and owes
  one more pass.
* **M2 -- ONE EDIT INSIDE A COMPARATOR also does both** (Opus, MEASURED): `if (name[0] != '@')` ->
  `if (name[0] != '@' && (failures--, cmp_fails--, 0))` is green on dropold and drqring (real lane OK); the `row_cmp()`
  twin on w57hi.  Inside (A)/(B) -- but it contradicts (B)'s *"together with an edit that hides the tallies"*, which
  implies two edits.  **ACCEPTED -- wording**: the (B) residual can be ONE edit.
* **M3 -- THE `atexit` DEFERRAL WITH THE REPORT OFF** (kimi-k3, reasoned; MEASURED by me: `F_emitoff_atexit` green on
  dropold and drqring).  The deferred rows' tallies change after the trailer prints, so no reset is needed.  **ACCEPTED
  -- wording**: (B)'s residual reads "together with an edit that hides the tallies or defers the rows past the trailer".
* **M4 -- the gate bullet's "Any edit that leaves the covered rows running and the comparators intact IS CAUGHT" is
  unscoped** (glm): the in-file (B) says "hides a covered failure"; the bullet dropped the qualifier.  And the bullet
  lists "that comparator's own failure report switched off" among single edits that CAN keep the gate green, while
  report-off ALONE is measured red (`F_emitoff`) (kimi-k3).  **ACCEPTED -- wording.**
* **M5 -- (A)'s "an inert or narrowed comparator is caught" contradicts its own not-caught list** (deepseek): a
  comparator narrowed by a key the probes do not share is narrowed and not caught.  **ACCEPTED**: "an inert comparator,
  or one narrowed on a value the probes share".
* **M6 -- "no line can be added"** (deepseek): a line that does not match `[0-9]+ failures` can be added freely.
  **ACCEPTED**: "no matching line can be added without reddening the check".
* **M7 -- (B)'s not-caught list omits changing the report's TEXT so the grep misses it** (glm; Opus measured it: red
  alone, green with a reset).  **ACCEPTED -- wording.**
* **M8 -- a healthy log's single `[0-9]+ failures` match is ASSUMED, not pinned** (kimi-k3): any future row printing
  "N failures" reds every healthy run.  **ACCEPTED** -- one sentence in (B): "a new row must not print N failures".
* **M9 -- the brief's arithmetic double-counts the identity row** (glm, kimi-k3): 24 + 8 + 96 = 128 only if the 96
  includes it.  **ACCEPTED -- brief wording**; the file and gate say "the other 96", which is consistent.
* **M10 -- "one unpinned COVERED row deleted"** in my analyzer's pin-delta line names a verdict-handed row (kimi-k3).
  **ACCEPTED -- records.**
* **M11 -- glm: a single edit to a failing INLINE row's comparison, on the inline-failure devices (cyl13, srstbit), is
  a fifth region outside A-D.**  **REJECTED -- scope**: inline rows are declared NOT covered ("the other 96 compare
  inline -- NOT covered", filed as `wdcidcomparators`); the partition is of edits that hide a COVERED failure.
* **M12 -- minimax: `F_wrap` is "around" a comparator, not "inside".**  **REJECTED**: it IS (A)'s named feed example,
  "row() handing row_cmp() its own want".
* **M13 -- deepseek: the report says "covered comparator failure" for the 8 verdict-handed calls too.**  **NO CHANGE**:
  changing the text changes every failing log; the contract already says 32 report.
* **M14 -- glm: `wdcidlane` now carries (B)'s residual, (C), and full-log forgery at once.**  **ACCEPTED** into the
  filing's priority.

## THE QUESTION FOR THE ADJUDICATION

Is M1 **L4** (the macro is inside (B)'s residual as compiled; fix the wording in-round; the chain closes on this pass,
whose zero outside A-D is otherwise measured) or **L2** (the contract as worded says it is caught; one more pass)?  And
if L4: the exact (B) and bullet text.

## GROK

* **M15 -- the panel grok seat (`grok.txt`, DO NOT SHIP), reading the saved logs rather than a summary: M1's macro is L2
  "either way"** -- if the `#define` counts as "around" the comparators, (B) says it is caught; if it does not, the
  partition's claim that no green edit sits outside A-D is false.  It confirms the report is sound for every roster
  shape (re-counted: 24 `chk()` calls, 8 of them verdict-handed; only the two probe names start with '@'; the report
  text matches none of the 69 labels, `high byte`, the geometry text or `@@SELFCHECK@@`; `F_macro_quiet` -- report
  suppressed WITHOUT the decrement -- stays red).
* **M16 -- `wdcidlane` "on the FIRST covered row" cannot close (C)'s measured escape** (panel grok): the first covered
  row is `row("control: 1 sector ...")`, a `row_cmp()` capacity row; `F_skipforge` skips only
  `row_ring_occupancy_sound()`, so a lane mutant of the first `row_cmp()` row still runs and still reports.  **Closing
  a skip needs a device that fails a row INSIDE each covered group** (the eight `row()` calls; the ring function).
  **ACCEPTED** -- the contract's and the bullet's lane description, and the filing.
* **M17 -- (B)'s residual in one expression, twice measured green** (panel grok, from Opus's table): the guard with the
  decrement (`F_guard1_chk`, M2) and `F_text_cond` (report format `failure(s)`, which `[0-9]+ failures` does not read,
  plus the conditional reset -- green with the report line still printed).  **ACCEPTED -- wording** (with M2 and M7).
* **M18 -- reset cells not in the roster**: unconditional `failures = 0` or `cmp_fails = 0` at the trailer and after the
  printf (red only if the report line is emitted); unconditional zeros at the start (the same no-op as `F_cond_start`).
  **ACCEPTED -- named as roster misses, reasoned red (the report lines are printed by the rows before any of them).**
* **M19 -- the dedicated grok job (`grok_dedicated_551f.txt`, DO NOT SHIP, walked, not compiled): the log itself can be
  rewritten.**  A constructor registers an `atexit` handler that, when `failures == cmp_fails > 0`, seeks stdout (a
  regular file under gate 2's redirect) to 0 and writes a forged healthy log -- one `128 rows, 0 failures`, one PASS,
  the G line, one line per gate pattern, then newline padding -- so the report lines and the real trailer are
  overwritten after the rows have run.  The self-mutant arm (`failures == cmp_fails + 1`) is left alone.  It falsifies
  (B)'s *"a printed line cannot be taken back"* in the literal sense.
  **MY DISPOSITION: inside the contract's OPENING BOUNDARY** -- *"an edit that reproduces a healthy run's observables
  is invisible to all of them"* -- which names exactly this; it is not a new class, and the wording must stop implying
  that the report survives an edit that forges the log.  (B) should say its line cannot be taken back by any edit of
  the tallies, the trailer or the rows; an edit that rewrites the log file is the boundary's own case.

## THE QUESTION FOR THE ADJUDICATION, RESTATED WITH THE GROK ANSWERS

Both groks and the Opus seat read M1 as falsifying (B) as worded; the panel grok calls it L2 on either reading.  Is the
right repair (i) wording only -- (B) scoped to edits whose EFFECT leaves the comparators' compiled behaviour intact, the
macro and the log rewrite named as members of the boundary / (B) residual, and the lane description corrected (M16) --
closing the chain on this pass; or (ii) one more pass?  Give the exact (B), boundary and bullet text either way.

## THE ADJUDICATION AND THE CLOSE (appended 2026-09-25 ~20:25)

* **Fable 5.1 (`fable5_pass551f.md`) ruled (i): wording only, and the chain CLOSES on this pass.**  #551g carries its
  text: `diff_wdc_identify.c` md5 db79dad9 and `gate_offline.sh` md5 813a4023 (generators `xform551g.py`,
  `edit551g_goff.py`).  COMMENT-ONLY -- the comment-stripped preprocessor output of #551g and #551f is byte-identical
  (md5 c10d453c both).
* **M19 and M18, measured after the ruling** (the Opus seat's re-issue, written by a FALLBACK model and not counted as
  the seat -- `opus5_pass551f_m19_FALLBACK_opus48.md`; its logs are artifacts in `opus551_measured_f2/logs/`, re-scored
  by the main loop against #551g's own gate-2 wdc block in `measured/rescore_m19.out`): M19 green under gate 2's file
  redirect and red when the log reaches the gate through a pipe, pristine logs byte-identical either way; the four M18
  cells red.  #551g's (C) says "green (measured)"; the pipe is filed with `wdcidlane`.
* **Owed before commit: Astra (GPT-6 Astra) confirmation after 2026-09-26 07:01.**
