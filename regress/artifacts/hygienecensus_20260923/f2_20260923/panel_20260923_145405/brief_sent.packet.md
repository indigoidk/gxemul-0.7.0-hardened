# hygienecensus §F2 -- the ADJUDICATION pass (the panel shares its findings) + the REPAIR's own pass 2

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated
wrongly.  **Check the premises, not just the derivations.**  Where I state something as
fact, ask whether it is true.  A seat that re-derives a premise from something this brief
did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/`** -- `regress/gate_hygiene.sh`, `tools/derive_hygiene_pins.sh`,
`regress/crime_width_probe.py` (one comment) and `regress/luna_absentcpu_probe.py`.  There are THREE
pristine-2021-upstream copies of GXemul under the project root (`./src/` and two under
`_archive/audit-results-*/builds/`).  They are NOT this fork.

**If you cannot read files that is expected** — every fact you need is inlined.  Name any
premise you cannot settle from this packet rather than guessing at it.

**Where this brief states an ARITHMETIC claim — a count, a set, a membership — ENUMERATE it
rather than reasoning about it.**  And ENUMERATE THE RIGHT DOMAIN.

**VERDICT LINE FIRST**: `VERDICT: SHIP` or `VERDICT: DO NOT SHIP -- <reason>`.

## What this pass is

Pass 2 of the census round (gate 6's readiness census re-derived by owner ruling) drew eight answers: codex, grok, agy,
deepseek and the kimi seat (via its kimi-k3 transport; the kimi CLI is walled on its weekly limit) said DO NOT SHIP;
glm and minimax said SHIP; the Opus seat MEASURED fourteen edits that leave every readiness row green.  This packet
gives every seat the others' findings, my disposition on each, and the REPAIR I made in response -- which owes its own
pass 2 under the repair-chain rule.  **Seats reviewing their own finding: be harder on it, and on whether the FIX is
right, not only on whether the finding was.  Seats whose position a disposition ADOPTS: scrutinise that one most.**

## §C — SETTLED PREMISES (owner rulings 2026-09-23 -- the design; do not re-open them, but DO say if the repair fails to implement them)

1. **Count every probe lying in the tree**, including the three untracked ones (`crime_width_probe.py`
   (#529), `arm_msrmode_probe.py`, `lca_isaphys_probe.py`) -- the census counts files, not commits.
2. **Grandfather** the two promptless ones (`arm_msrmode_probe.py`, `lca_isaphys_probe.py`) BY NAME.
3. **`arm_bdt_probe.py:76`**, a whole-buffer site committed 2026-09-12 (`if self.buf.rstrip().endswith("GXemul>"):`),
   is ALLOWLISTED BY NAME at pin 3 -- against the gate block's own default ("a new hit is never answered by
   raising the pin"), recorded as an exception; converting it is filed (`armbdtreadiness`).
4. **`crime_width_probe.py:956`**'s `op.endswith("P")` is re-spelled so the closed-world spelling census
   does not count it as an unrecognised readiness predicate.
5. **ONE bulk re-derivation of the pins** by `tools/derive_hygiene_pins.sh --write`, never by hand.

6. **D1 is settled by measurement** (opus): a single-quoted whole-buffer site leaves `unknown` at 0.

## THE FINDINGS, AND MY DISPOSITION ON EACH (every seat's, consolidated)

Stopping rule applied: in-round only a MEASURED FALSE PASS or a WRONG RECORD in THIS round's material (the deriver
and the name row are new material still being built, so defects in them are pre-ship construction); everything else
FILED.

**IN-ROUND -- seven, all applied (the diff is inlined below):**

* **C1 -- a third promptless probe, hidden by MY comment.**  `crime_width_probe.py` (#529, untracked) reads its guest
  by timed drains and has no prompt predicate; the only `endswith(` in it was the comment this round added at its
  re-spelled line, and the promptless classifier was a raw `grep -L "endswith("` that keeps comments.  Found by codex,
  grok, agy; MEASURED by opus (reword the comment -> promptless got=43 want=42).  FIX: (a) the classifier reads CODE
  (full-line comments stripped, as every other census here does; a basename that is not a file in `regress/` --
  a subdirectory probe, none today -- is listed promptless, fail-closed); (b) the comment reworded; (c)
  `crime_width_probe.py` grandfathered BY NAME under the owner's ruling-2 principle, reported to the owner as a third
  name rather than asked first.
* **C2 -- single quotes walked past both whole-buffer rows.**  Both matched only `endswith("GXemul>")` while the
  closed-world spelling census accepts either quote, so `unknown` stayed 0 and every row stayed green (opus, measured;
  codex, grok, agy).  FIX: one `WHOLE_RE` taking either quote, used by both rows.
* **C3 -- the name row pinned a SET, so a site could move between the two files** (opus e6: count 3, names
  unchanged).  FIX: each file WITH ITS COUNT -- `WHOLE_FULL_FILES="arm_bdt_probe.py:1 arm_flags_probe.py:2"`; taken as
  a refinement inside ruling 3 (allowlist BY NAME), not a new option.
* **C4 -- the promptless row compared COUNTS**, so swapping one grandfathered probe for a new promptless one read
  42 == 42 (opus e14; kimi-k3, grok).  Ruling 2 says "by NAME".  FIX: a row grading the names -- new and gone both
  empty.
* **C5 -- the deriver (NEW in this round).**  Its `--write` RAISED `EXPECT_UNKNOWN` (opus dL1; codex, kimi-k3) and
  `EXPECT_WHOLE_FULL` (opus dL2; grok) -- pins the gate says are never answered by raising; it never derived, reported
  or wrote `WHOLE_FULL_FILES`, so ruling 5 ("never by hand") was unachievable for the pin this round added (agy,
  deepseek, kimi-k3, glm); it printed success after its own writer failed (codex); it would re-pin to ZERO on an empty
  population (glm).  FIX: refuse a rise of `EXPECT_UNKNOWN`; refuse a rise of `EXPECT_WHOLE_FULL` or any change of the
  per-file set other than SHRINKING, unless an owner ruling is named in `WHOLE_FULL_RULING`; derive, report and write
  `WHOLE_FULL_FILES`; a `--release` mode for grandfathered names that are no longer promptless (so the names row never
  forces a hand edit); refuse a zero denominator; propagate the writer's exit status.
* **C6 -- wrong records, fixed where they stand.**  The deriver's usage line said `--write` rewrites `EXPECT_BARE`
  (it never did); the grandfather note said each of the 20 "uses a fixed-wait or drain-to-EOF session rather than a
  prompt predicate" -- false for `alpha_tbi_probe.py`, whose `wait_prompt` is a real readiness wait spelled
  `"gxemul>" in buf[...].lower()` (grok); "moved no census" -- they moved the promptless census and the denominator,
  just no PIN (glm); "the LAST TWO LINES" -- positional, and the next `--grandfather` makes it false (agy, glm,
  kimi-k3; now anchored by each block's first NAME -- and this round's own `--grandfather` has since made it THREE
  blocks, which the rewritten note says); the fresh-clone sentence (a clone reds the names row too, and reads 70 only
  while NONE of the three is committed -- codex, grok); "FILED (`armbdtreadiness`)" when no such row existed (codex --
  it is filed with this round's records); "THE PRESENT VALUE OF 2" near the whole-buffer rows (codex).
* **C7 -- `LC_ALL=C` on the sorts** (agy, glm).  A flake guard only: opus measured four locales with no change and
  found the battery's `en_US.UTF-8` is not installed on the WSL image (it falls back to C); a reorder fails CLOSED.

**FILED as a new row `hygienecensusholes` (MED, harness) -- pre-existing, measured by opus, none introduced here:**
another buffer name (`out.rstrip()...`); a predicate split across lines; `strip()` for `rstrip()`; `endswith (` with a
space; **`buf.endswith (">")` -- the #37 bare defect itself -- walks past the #37 row with one space**; a slice compare
(`buf.rstrip()[-7:] == "GXemul>"`); a filename with a space (a bare `xargs` in the denominator); a probe in a
subdirectory; `_mark = -len(self.buf)` (the fresh-mark row checks the call's spelling, not the value -- codex); a second
session with no predicate inside an already-counted file (kimi-k3); narrowing an enumerator and then `--write` (glm).
The census is a SPELLING census: it guarantees spellings, not readiness (glm).  Filed to #529: `crime_width_probe.py`'s
"six KINDS" comment does not describe its literal domain (eight op strings, 46 entries -- codex).

**DISAGREEMENTS -- settled by measurement, not by vote:**

* **D1** "a single-quoted site reds the `unknown` row" (minimax, deepseek, glm, kimi-k3 -- all packet-fed) vs "it
  passes every row" (codex, grok, agy, opus).  SETTLED BY OPUS'S RUN: the recogniser `full` is
  `endswith([\"']GXemul>[\"'])`, so `allends` and `full` both rose 49 -> 50 and `unknown` stayed 0.  The pass-2
  packet did not inline `full`; glm and kimi-k3 named exactly that premise as unsettleable -- a conditioned answer,
  and scored as one.
* **D2** SHIP (glm, minimax) vs DO NOT SHIP (five seats, opus's measurements).  Not a tally: C1, C2 and C5 are measured
  false passes in this round's material; glm itself listed C5's halves and C7 as defects, calling them non-blocking.
* **D3** the locale question -- all agree the row fails CLOSED; C7 taken as a flake guard only.
* **D4** "every grandfathered name really is promptless" -- TRUE under the census's lexical proxy (codex enumerated
  all 42), FALSE as a property for `crime_width_probe.py` (C1) and misleading for `alpha_tbi_probe.py` /
  `drive_guest.py` (real readiness waits the proxy cannot see -- C6).

**OWNER QUESTIONS this pass raised:** (O1) the third untracked promptless probe, grandfathered under ruling 2's principle
-- reversible if the owner prefers converting it; (O2) an EXPIRY on the arm_bdt allowlist entry (codex, grok, agy, glm,
kimi-k3) -- the house idiom exists (`gate_offline.sh`'s `exempt_expired`); needs an owner-chosen date; not added.

## THE REPAIR, MEASURED -- and the controls found a defect in it before this packet was written

`regress/artifacts/hygienecensus_20260923/controls_p2/SUMMARY.txt` -- ten cases on /tmp COPIES of `regress/` + `tools/`,
each with its expected outcome written into the script BEFORE it ran.  **RUN 1 FAILED TWO PREDICTIONS**, and they
shared one cause, in MY repair: the new classifier loop was fed by `printf '%s'` -- `$(...)` strips the list's last
newline and `while read` then DROPS THE LAST FILE.  A new promptless probe named `zz_*` sorted last and vanished from
both promptless rows; the deriver then re-pinned the denominator to 74 without refusing.  (The real tree was unaffected
only because its last pty probe happens to be prompt-detecting.)  Fixed (`printf '%s\n'`); run 1 kept as evidence
(`controls_p2_run1_lastline_bug/`).  **RUN 2, on the fixed gate:**

    real      0 FAIL of 12 readiness rows                  (expected 0)
    move      1 FAIL: per-file row                          (a site moved arm_bdt -> luna; count still 3)
    add       2 FAIL: count 4/3, per-file row
    squote    2 FAIL: count 4/3, per-file row               (the single-quoted site of C2)
    redist    1 FAIL: per-file row                          (arm_bdt:2 arm_flags:1; count still 3 -- C3)
    swap      1 FAIL: names row new=zz_swapped gone=gdrom_cond   (counts equal -- C4)
    cmt       3 FAIL: denominator 74/73, promptless 44/43, names row (a new probe whose only endswith( is a comment)
    deriver:  cmt --write REFUSED (new promptless); unk --write REFUSED (unrecognised spelling); grow --write REFUSED,
              then WRITTEN only with WHOLE_FULL_RULING set (EXPECT_WHOLE_FULL=4, arm_bdt_probe.py:2); empty -> DERIVE_FAIL,
              gate file unchanged; rel (a grandfathered probe gains a predicate) --write REFUSED -> --release -> --write
              WRITTEN -> gate 0 FAIL.

*(One expectation TEXT was stale: `cmt` was written expecting "promptless 43/42"; it read 44/43 because
`crime_width_probe.py`'s grandfathering had moved the baseline by one between writing and running.  The predicted row
count, 3 FAIL, held.)*  The real tree, after `--grandfather crime_width_probe.py` and `--write`: every census got ==
pinned (`derive_p2repair.txt`); the only pin that moved is the grandfathered list (42 -> 43 names).

## THE REPAIR DIFF -- regress/gate_hygiene.sh (vs the file pass 2 reviewed; -U1)

```diff
--- a/regress/gate_hygiene.sh
+++ b/regress/gate_hygiene.sh
@@ -354,4 +354,5 @@
 #  and lca_isaphys_probe.py (#540).  The owner chose to count all three.  Consequence, stated so nobody
-#  meets it cold: until those three are committed, a FRESH CLONE counts 70 and reds this row.  Written by
-#  `tools/derive_hygiene_pins.sh --write`, never by hand. ***
+#  meets it cold: until all three are committed, a FRESH CLONE counts FEWER than 73 (70 with none of them)
+#  and reds this row -- and the promptless-names row too, because all three are grandfathered names that
+#  exist only in the working tree.  Written by `tools/derive_hygiene_pins.sh --write`, never by hand. ***
 EXPECT_PTY_PROBES=73
@@ -389,11 +390,18 @@
 alpha_harness_probe.py alpha_pfnoffset_probe.py alpha_swpctx_v0_probe.py alpha_tbi_probe.py arm_bfx_width_probe.py landisk_aux_probe.py lca_badval_probe.py lca_confbus_probe.py lca_confwidth_probe.py lca_irqstub_probe.py lca_irqstub_uart_probe.py lca_isalane_probe.py lca_widewrite_probe.py maple_dmaaddr_probe.py pcc2_c040_probe.py sgi_mte_fill_probe.py sgi_re_colourdefault_probe.py sgi_re_randompixel_probe.py sgi_re_rgb_probe.py wdc_altdigin_probe.py
-arm_msrmode_probe.py lca_isaphys_probe.py"
-#  hygienecensus: the LAST TWO LINES of the list above were appended by tools/derive_hygiene_pins.sh
-#  --grandfather.  The first of them (2026-09-19): 20 promptless pty probes committed between 2026-09-05
-#  and 2026-09-18 that moved no census (b78bb0f pinned 46 probes; HEAD had 70).  Each uses a fixed-wait or
-#  drain-to-EOF session rather than a prompt predicate -- GRANDFATHERED, not converted: converting a
-#  probe's readiness is its own round.  The last (2026-09-23, OWNER RULING): arm_msrmode_probe.py
-#  (armmsrmodekill) and lca_isaphys_probe.py (#540), both UNTRACKED and lying in the tree, named here so
-#  the census can pass on the tree the weekly battery runs.  Re-derive, never hand-edit: run
-#  `bash tools/derive_hygiene_pins.sh` (report), `--grandfather NAME...`, then `--write`.
+arm_msrmode_probe.py lca_isaphys_probe.py
+crime_width_probe.py"
+#  hygienecensus: tools/derive_hygiene_pins.sh --grandfather appended THREE blocks to the list above; they are
+#  named here by their FIRST NAME, never by position, because the next --grandfather appends another.
+#  The block beginning `alpha_harness_probe.py` (derived 2026-09-19): 20 pty probes committed between
+#  2026-09-05 and 2026-09-18 that moved NO PIN -- they moved the promptless census (20 -> 40) and the
+#  denominator (46 -> 70) while EXPECT_PTY_PROBES sat at b78bb0f's 46.  None contains the literal
+#  `endswith(` this census keys on: most use fixed waits or drain-to-EOF, and alpha_tbi_probe.py has a real
+#  readiness wait the census cannot see (`"gxemul>" in buf[...].lower()`).  GRANDFATHERED, not converted:
+#  converting a probe's readiness is its own round.  The block beginning `arm_msrmode_probe.py`
+#  (2026-09-23, OWNER RULING): arm_msrmode_probe.py (armmsrmodekill) and lca_isaphys_probe.py (#540).  The
+#  block beginning `crime_width_probe.py` (2026-09-23, pass 2 of this round, under the same ruling's
+#  principle): crime_width_probe.py (#529), hidden from this census by a comment until the classifier below
+#  learned to skip comments.  All three are UNTRACKED and lying in the tree, named so the census passes on
+#  the tree the weekly battery runs.  Re-derive, never hand-edit: `bash tools/derive_hygiene_pins.sh` (report),
+#  `--grandfather NAME...` / `--release NAME...`, then `--write`.
 
@@ -412,4 +420,12 @@
 _ptyn=$(printf '%s' "$_ptylist" | grep -c . )
-_promptless=$(cd "$HERE" && printf '%s' "$_ptylist" | tr ' ' '
-' | xargs grep -L "endswith(" 2>/dev/null | sort)
+#  hygienecensus pass 2 (2026-09-23): THE CLASSIFIER READS CODE, NOT COMMENTS.  It was a raw `grep -L "endswith("`,
+#  so a comment naming the method hid a promptless probe -- measured: crime_width_probe.py's only `endswith(` was a
+#  comment this very round added, and it kept the file out of this set (reworded, the count read 43 against 42).  Every
+#  other census here strips full-line comments; this one now does too.  A basename that is not a file in $HERE (a
+#  probe in a subdirectory -- none today) is listed as promptless: FAIL-CLOSED, it cannot be read, so it is not trusted.
+code_has() { grep -v '^[[:space:]]*#' "$1" 2>/dev/null | grep -q -- "$2"; }
+#  `printf '%s\n'`, NOT `printf '%s'`: $(...) strips the list's final newline, and `while read` then DROPS THE LAST
+#  FILE -- measured by this round's own controls, where a new promptless probe named zz_* sorted last and vanished
+#  from both promptless rows (the `xargs grep -L` this replaced did not care).
+_promptless=$(cd "$HERE" && printf '%s\n' "$_ptylist" | tr ' ' '\n' | while IFS= read -r f; do [ -z "$f" ] || code_has "$f" 'endswith(' || echo "$f"; done | LC_ALL=C sort)
 _want=$(printf '%s' "$GRANDFATHERED_PROMPTLESS" | tr ' ' '
@@ -423,4 +439,9 @@
 #  WHICH file, and the whole point of the denominator is attribution.
-_new=$(comm -13 <(printf '%s' "$GRANDFATHERED_PROMPTLESS" | tr ' ' '
-' | grep . | sort)                 <(printf '%s' "$_promptless" | grep . | sort) 2>/dev/null)
+#  hygienecensus pass 2: AND GRADE THE NAMES, not only the count.  The count row alone read 42 == 42 after one
+#  grandfathered probe was swapped for a new promptless one (measured); the owner's ruling is "grandfather BY NAME",
+#  so the set is what is graded.  LC_ALL=C on both sides: comm needs one collation.
+_gfs=$(printf '%s' "$GRANDFATHERED_PROMPTLESS" | tr ' ' '\n' | grep . | LC_ALL=C sort)
+_new=$(LC_ALL=C comm -13 <(printf '%s\n' "$_gfs") <(printf '%s\n' "$_promptless" | grep .) 2>/dev/null | tr '\n' ' ' | sed 's/ $//')
+_gone=$(LC_ALL=C comm -23 <(printf '%s\n' "$_gfs") <(printf '%s\n' "$_promptless" | grep .) 2>/dev/null | tr '\n' ' ' | sed 's/ $//')
+check "readiness: promptless names == grandfathered names" "new=${_new:-none} gone=${_gone:-none}" "new=none gone=none"
 if [ -n "$_new" ]; then
@@ -597,5 +618,10 @@
 #  readiness to #392's anchored form is FILED (`armbdtreadiness`).  A count alone would let a site MOVE
-#  between files unseen, so a second row pins the SET of files too (WHOLE_FULL_FILES, sorted). ***
-WHOLE_FULL_FILES="arm_bdt_probe.py arm_flags_probe.py"
+#  between files unseen, so a second row pins each FILE WITH ITS OWN COUNT (WHOLE_FULL_FILES, `name:count`,
+#  sorted under LC_ALL=C).  Pass 2 of this round MEASURED two holes in the first form of these rows, both
+#  closed here: a set of names alone let a site move between the two files (count 3, set unchanged), and
+#  both patterns matched only the double-quoted spelling while the closed-world spelling census accepts
+#  both quotes -- so a single-quoted whole-buffer site passed every row.  WHOLE_RE takes either quote. ***
+WHOLE_FULL_FILES="arm_bdt_probe.py:1 arm_flags_probe.py:2"
 EXPECT_WHOLE_FULL=3
+WHOLE_RE="buf.rstrip().endswith([\"']GXemul>[\"'])"
 #  *** ROW 3: SCOPED TO FILES THAT CAN DRIVE A REAL GUEST, rather than exempting a
@@ -634,3 +660,3 @@
 #  what pty.fork wraps); `import regress.drive_guest`.  Censused at 0 apiece.  THE
-#  PRESENT VALUE OF 2 IS CORRECT; THAT DOES NOT ESTABLISH POPULATION COMPLETENESS.
+#  PRESENT VALUE (3, pinned above) IS CORRECT; THAT DOES NOT ESTABLISH POPULATION COMPLETENESS.
 #
@@ -649,10 +675,9 @@
              | xargs -0 grep -h "$1" 2>/dev/null | grep -v '^[[:space:]]*#'; }
-whole_full=$(pty_code 'buf.rstrip().endswith("GXemul>")' | grep -c .)
+whole_full=$(pty_code "$WHOLE_RE" | grep -c .)
 check "readiness: whole-buffer full-prompt sites (allowlist)" "$whole_full" "$EXPECT_WHOLE_FULL"
-#  hygienecensus 2026-09-23: the allowlist BY NAME -- the files holding a CODE (non-comment) whole-buffer
-#  site, over the same pty-driving population as the count above, sorted and space-joined.
-whole_files=$(pty_driving | while IFS= read -r f; do
-                  n=$(grep -h 'buf.rstrip().endswith("GXemul>")' "$f" 2>/dev/null | grep -v '^[[:space:]]*#' | grep -c .)
-                  [ "$n" -gt 0 ] && basename "$f"; done | sort | tr '\n' ' ' | sed 's/ $//')
-check "readiness: whole-buffer sites, allowlisted files" "$whole_files" "$WHOLE_FULL_FILES"
+#  hygienecensus 2026-09-23: the allowlist BY NAME, WITH EACH FILE'S OWN COUNT -- `name:count` for every file
+#  holding a code-line whole-buffer site (full-line comments stripped; a trailing comment or a string still
+#  counts), over the same pty-driving population as the count above, sorted under LC_ALL=C and space-joined.
+whole_files=$(pty_driving | while IFS= read -r f; do n=$(grep -h "$WHOLE_RE" "$f" 2>/dev/null | grep -v '^[[:space:]]*#' | grep -c .); [ "$n" -gt 0 ] && printf '%s:%s\n' "$(basename "$f")" "$n"; done | LC_ALL=C sort | tr '\n' ' ' | sed 's/ $//')
+check "readiness: whole-buffer sites, per allowlisted file" "$whole_files" "$WHOLE_FULL_FILES"
 check "readiness: anchored full-prompt sites (#392)" "$conv_anchor" "$EXPECT_CONVERTED"
```

## THE REPAIR -- regress/crime_width_probe.py, the comment above the re-spelled test (whole new text)

```python
    #  hygienecensus (2026-09-23, owner ruling): spelled `op[-1:] == "P"', not with the str method -- identical over the
    #  eight op strings ACCEPTS produces (and on ""), but gate_hygiene's spelling census is CLOSED-WORLD over that method
    #  and counted this operation-name test as a readiness predicate it could not classify (got=1 want=0 at the
    #  2026-09-20 battery).  This probe has NO prompt predicate -- session() reads by timed drains -- so it is
    #  grandfathered by name as promptless; pass 2 found that an earlier wording of THIS comment had hidden that.
    if op[-1:] == "P":
```

## THE REPAIR -- tools/derive_hygiene_pins.sh, THE WHOLE NEW FILE (pass 2 reviewed a 106-line version; this replaces it)

```bash
#!/bin/bash
#  derive_hygiene_pins.sh -- re-derive gate_hygiene.sh's census pins FROM THE GATE'S OWN ENUMERATORS, instead of
#  hand-editing numbers.  (hygienecensus, 2026-09-19: EXPECT_PTY_PROBES sat at 46 while 24 pty probes were committed
#  over two weeks, and nothing said so until a pre-flight read of the weekly battery.)
#
#  It does NOT re-implement the counting.  It extracts the gate's own enumerator functions (py_code, probe_code,
#  pty_driving, pty_code, code_has) and assignment lines (bare/allends/full, _ptylist/_ptyn/_promptless, conv_*,
#  WHOLE_RE/whole_full/whole_files) out of gate_hygiene.sh by name and evaluates them -- so an edit to how the gate
#  counts flows into the deriver.  An enumerator it cannot find is a hard error, never a zero.
#
#    derive_hygiene_pins.sh                 report: got vs pinned, per census, the promptless NAMES that differ, and
#                                           the untracked files the censuses count
#    derive_hygiene_pins.sh --write         rewrite EXPECT_UNKNOWN, EXPECT_PTY_PROBES, EXPECT_CONVERTED,
#                                           EXPECT_WHOLE_FULL and WHOLE_FULL_FILES in place (EXPECT_BARE is never
#                                           written; see the refusals)
#    derive_hygiene_pins.sh --grandfather F [F...]
#                                           append the NAMED files to GRANDFATHERED_PROMPTLESS (deliberate, never bulk)
#    derive_hygiene_pins.sh --release F [F...]
#                                           remove NAMED files from GRANDFATHERED_PROMPTLESS -- only files that are
#                                           grandfathered and no longer promptless (converted, or gone)
#
#  --write REFUSES, each with its reason printed, and the refusals are the point of the tool:
#    * the pty denominator is 0 -- the enumerators saw nothing (wrong tree, moved file); it never re-pins to zero;
#    * the three #392 counts (anchor, echo, fresh mark) disagree -- they share ONE pin, and a disagreement IS a
#      defect (a guard present but uncounted): fix the probe, not the pin;
#    * a promptless probe is neither grandfathered nor given prompt detection, or a grandfathered name is no longer
#      promptless -- the gate grades the NAMES, so --grandfather / --release first;
#    * EXPECT_BARE or EXPECT_UNKNOWN would RISE -- a bare `endswith(">")` and an unrecognised spelling are defects the
#      gate freezes at its pin (both may fall);
#    * EXPECT_WHOLE_FULL would rise, or WHOLE_FULL_FILES would change other than by SHRINKING (a file's count falling
#      or a file leaving) -- #392 measured the whole-buffer form at 0/80, so a new site is never answered by raising
#      the pin.  The ONE way past it is an owner ruling, named in the environment: WHOLE_FULL_RULING="<ruling>".
#  (hygienecensus pass 2, 2026-09-23: the first version raised EXPECT_UNKNOWN and EXPECT_WHOLE_FULL on --write --
#  measured -- never derived WHOLE_FULL_FILES, re-pinned to zero on an empty population, and reported success after
#  its own writer failed.)
#
#  Run it from anywhere; HERE is the regress directory beside this script's tools/ directory ($GXROOT overrides).
set -u
PY=""; for c in python3 python; do "$c" -c "import sys" >/dev/null 2>&1 && { PY=$c; break; }; done   # RUN it: a Windows Store stub exists and fails
[ -n "$PY" ] || { echo "DERIVE_FAIL: no working python"; exit 2; }
ROOT=${GXROOT:-$(cd "$(dirname "$0")/../.." && pwd)}
HERE="$ROOT/GXEMUL-SEC/regress"
[ -d "$HERE" ] || HERE="$(cd "$(dirname "$0")/../regress" 2>/dev/null && pwd)"
G="$HERE/gate_hygiene.sh"
[ -f "$G" ] || { echo "DERIVE_FAIL: no gate_hygiene.sh at $G"; exit 2; }
MODE=report; GF=()
case "${1:-}" in
    --write) MODE=write ;;
    --grandfather) MODE=grandfather; shift; GF=("$@") ;;
    --release) MODE=release; shift; GF=("$@") ;;
    "") ;;
    *) echo "usage: $0 [--write | --grandfather FILE... | --release FILE...]"; exit 2 ;;
esac

fn() {  # extract a shell function definition by name: from `name() {` through the first line ending in `}`
    awk -v n="$1" 'index($0, n "() {")==1 {p=1} p {print} p && /}[[:space:]]*$/ {exit}' "$G"
}
asg() { # extract an assignment by variable name: continue while the line ends in a backslash OR a single quote is
        # still open (the gate writes `tr ' ' '<newline>'` with a LITERAL newline inside the quotes)
    awk -v n="$1" 'index($0, n "=")==1 {p=1}
        p {print; q += gsub(/\047/, "\047"); if ($0 !~ /\\$/ && q % 2 == 0) exit}' "$G"
}
CODE=""
for f in py_code probe_code pty_driving pty_code code_has; do
    d=$(fn $f); [ -n "$d" ] || { echo "DERIVE_FAIL: enumerator $f() not found in gate_hygiene.sh"; exit 3; }
    CODE="$CODE$d"$'\n'
done
for v in bare allends full unknown _ptylist _ptyn _promptless conv_anchor conv_echo conv_mark WHOLE_RE whole_full whole_files; do
    a=$(asg $v); [ -n "$a" ] || { echo "DERIVE_FAIL: assignment $v= not found in gate_hygiene.sh"; exit 3; }
    CODE="$CODE$a"$'\n'
done
GP=$(awk 'index($0,"GRANDFATHERED_PROMPTLESS=")==1 {p=1} p {print} p && /"[[:space:]]*$/ && NR>1 && !/^GRANDFATHERED_PROMPTLESS="[^"]*$/ {exit}' "$G")
eval "$GP"
eval "$CODE"

pin() { sed -n "s/^$1=\([0-9]*\).*/\1/p" "$G" | head -1; }
spin() { sed -n "s/^$1=\"\(.*\)\"$/\1/p" "$G" | head -1; }
[ "${_ptyn:-0}" -gt 0 ] 2>/dev/null || { echo "DERIVE_FAIL: the pty denominator is ${_ptyn:-empty} -- the enumerators saw nothing; refusing to report or write zeros"; exit 3; }
_want=$(printf '%s' "$GRANDFATHERED_PROMPTLESS" | tr ' ' '\n' | grep -c .)
_got=$(printf '%s' "$_promptless" | grep -c .)
GFS=$(printf '%s' "$GRANDFATHERED_PROMPTLESS" | tr ' ' '\n' | grep . | LC_ALL=C sort)
NEWP=$(LC_ALL=C comm -13 <(printf '%s\n' "$GFS") <(printf '%s\n' "$_promptless" | grep .))
GONE=$(LC_ALL=C comm -23 <(printf '%s\n' "$GFS") <(printf '%s\n' "$_promptless" | grep .))
#  -prune, not `! -path`: the old form still DESCENDED into artifacts/ (thousands of files) once per probe, which made
#  one report take minutes over /mnt/c.  The untracked list it prints must not change (checked by the controls).
UNTR=$(cd "$HERE" && printf '%s\n' $_ptylist | while read -r f; do p=$(find . -path ./artifacts -prune -o -name "$f" -print | head -1); git -C "$HERE" ls-files --error-unmatch "$p" >/dev/null 2>&1 || echo "$f"; done)
WFP=$(spin WHOLE_FULL_FILES)

printf '%-34s %6s %6s\n' census got pinned
printf '%-34s %6s %6s\n' EXPECT_BARE "$bare" "$(pin EXPECT_BARE)"
printf '%-34s %6s %6s\n' EXPECT_UNKNOWN "$unknown" "$(pin EXPECT_UNKNOWN)"
printf '%-34s %6s %6s\n' EXPECT_PTY_PROBES "$_ptyn" "$(pin EXPECT_PTY_PROBES)"
printf '%-34s %6s %6s\n' "promptless vs GRANDFATHERED" "$_got" "$_want"
printf '%-34s %6s %6s\n' "EXPECT_CONVERTED (anchor)" "$conv_anchor" "$(pin EXPECT_CONVERTED)"
printf '%-34s %6s %6s\n' "EXPECT_CONVERTED (echo)" "$conv_echo" "$(pin EXPECT_CONVERTED)"
printf '%-34s %6s %6s\n' "EXPECT_CONVERTED (fresh mark)" "$conv_mark" "$(pin EXPECT_CONVERTED)"
printf '%-34s %6s %6s\n' EXPECT_WHOLE_FULL "$whole_full" "$(pin EXPECT_WHOLE_FULL)"
printf '%-34s got    [%s]\n%-34s pinned [%s]\n' WHOLE_FULL_FILES "$whole_files" "" "$WFP"
[ -n "$NEWP" ] && { echo "NEW PROMPTLESS (neither grandfathered nor prompt-detecting):"; printf '  %s\n' $NEWP; }
[ -n "$GONE" ] && { echo "GRANDFATHERED BUT NO LONGER PROMPTLESS (--release them):"; printf '  %s\n' $GONE; }
[ -n "$UNTR" ] && { echo "UNTRACKED files counted by these censuses (the battery counts what is lying in the tree):"; printf '  %s\n' $UNTR; }

#  run the python writer and FAIL LOUDLY if it fails -- the first version printed DERIVE_DONE after a failed write
pywrite() { "$PY" - "$@"; local rc=$?; [ $rc -eq 0 ] || { echo "DERIVE_FAIL: the writer failed (rc=$rc); nothing to trust in $G"; exit 6; }; }

if [ "$MODE" = grandfather ] || [ "$MODE" = release ]; then
    [ ${#GF[@]} -gt 0 ] || { echo "REFUSED: --$MODE needs the file names, one by one"; exit 4; }
    for f in "${GF[@]}"; do
        if [ "$MODE" = grandfather ]; then
            printf '%s\n' $NEWP | grep -qxF -- "$f" || { echo "REFUSED: $f is not a NEW promptless probe"; exit 4; }
        else
            printf '%s\n' $GONE | grep -qxF -- "$f" || { echo "REFUSED: $f is not a grandfathered name that is no longer promptless"; exit 4; }
        fi
    done
    pywrite "$G" "$MODE" "${GF[@]}" <<'PY'
import io, re, sys
g, mode, names = sys.argv[1], sys.argv[2], sys.argv[3:]
s = io.open(g, encoding="utf-8", newline="").read()
i = s.index('GRANDFATHERED_PROMPTLESS="') + len('GRANDFATHERED_PROMPTLESS="'); j = s.index('"', i)
body = s[i:j]
if mode == "grandfather":
    body = body + "\n" + " ".join(names)
else:
    for n in names:
        body, k = re.subn(r"(?<![\w.])%s(?![\w.])" % re.escape(n), "", body)
        assert k == 1, (n, k)
    body = "\n".join(" ".join(l.split()) for l in body.split("\n"))
    body = "\n".join(l for l in body.split("\n") if l.strip())
io.open(g, "w", encoding="utf-8", newline="").write(s[:i] + body + s[j:])
print("%s: %s" % ("GRANDFATHERED" if mode == "grandfather" else "RELEASED", " ".join(names)))
PY
    echo "DERIVE_DONE"
    exit 0
fi
if [ "$MODE" = write ]; then
    [ "$conv_anchor" = "$conv_echo" ] && [ "$conv_echo" = "$conv_mark" ] || {
        echo "REFUSED: the three #392 counts disagree ($conv_anchor/$conv_echo/$conv_mark) -- a guard present but uncounted; fix the probe, not the pin"; exit 5; }
    [ -z "$NEWP" ] || { echo "REFUSED: new promptless probes must be grandfathered by NAME (--grandfather) or given prompt detection first"; exit 5; }
    [ -z "$GONE" ] || { echo "REFUSED: grandfathered names are no longer promptless -- --release them first"; exit 5; }
    [ "$bare" -le "$(pin EXPECT_BARE)" ] || { echo "REFUSED: bare endswith(\">\") grew -- a defect, never re-pinned"; exit 5; }
    [ "$unknown" -le "$(pin EXPECT_UNKNOWN)" ] || { echo "REFUSED: an unrecognised endswith( spelling appeared -- a defect, never re-pinned"; exit 5; }
    shrink=$("$PY" -c '
import sys
def parse(t): return dict((p.rsplit(":", 1)[0], int(p.rsplit(":", 1)[1])) for p in t.split())
got, pinned = parse(sys.argv[1]), parse(sys.argv[2])
print("yes" if all(n in pinned and c <= pinned[n] for n, c in got.items()) else "no")' "$whole_files" "$WFP") || { echo "DERIVE_FAIL: WHOLE_FULL_FILES does not parse (got [$whole_files] pinned [$WFP])"; exit 6; }
    if [ "$whole_full" -gt "$(pin EXPECT_WHOLE_FULL)" ] || [ "$shrink" != yes ]; then
        [ -n "${WHOLE_FULL_RULING:-}" ] || { echo "REFUSED: the whole-buffer sites grew or moved (got [$whole_files], pinned [$WFP]) -- #392 measured that form at 0/80; convert the site, or name an owner ruling in WHOLE_FULL_RULING"; exit 5; }
        echo "WHOLE_FULL_RULING: $WHOLE_FULL_RULING"
    fi
    pywrite "$G" "$unknown" "$_ptyn" "$conv_anchor" "$whole_full" "$whole_files" <<'PY'
import io, re, sys
g, unk, pty, conv, whole, files = sys.argv[1:]
s = io.open(g, encoding="utf-8", newline="").read()
for k, v in (("EXPECT_UNKNOWN", unk), ("EXPECT_PTY_PROBES", pty), ("EXPECT_CONVERTED", conv), ("EXPECT_WHOLE_FULL", whole)):
    s, n = re.subn(r"(?m)^%s=\d+" % k, "%s=%s" % (k, v), s, count=1)
    assert n == 1, k
s, n = re.subn(r'(?m)^WHOLE_FULL_FILES="[^"\n]*"', 'WHOLE_FULL_FILES="%s"' % files, s, count=1)
assert n == 1, "WHOLE_FULL_FILES"
io.open(g, "w", encoding="utf-8", newline="").write(s)
print("WRITTEN: EXPECT_UNKNOWN=%s EXPECT_PTY_PROBES=%s EXPECT_CONVERTED=%s EXPECT_WHOLE_FULL=%s WHOLE_FULL_FILES=\"%s\"" % (unk, pty, conv, whole, files))
PY
fi
echo "DERIVE_DONE"
```

## §E -- QUESTIONS (answer each, numbered)

**Q1 -- which of my SEVEN in-round dispositions (C1-C7) is wrong?**  Name the count you checked.  Include whether each
FIX is right, not only whether its finding was -- in particular: (a) the code-only promptless classifier lists a
basename that is not a file in `regress/` as PROMPTLESS (fail-closed) -- right, or a false red waiting to happen?
(b) grandfathering `crime_width_probe.py` by name under the owner's ruling-2 principle, reported to the owner rather
than asked first; (c) per-file counts as a refinement INSIDE ruling 3 rather than a new option; (d) the deriver's one
escape hatch is an environment variable, `WHOLE_FULL_RULING`, naming an owner ruling -- is that the right shape, and
can it be set by accident?
**Q2 -- which FILED item should have been fixed in-round?**  Especially e9: `buf.endswith (">")` -- the #37 bare defect
itself, with one space -- walks past the #37 row.  The round's claim is "gate 6's census, re-derived"; does leaving e9
open make any sentence this round writes false?
**Q3 -- the disagreements.**  D1 was settled by the Opus seat's run (a single-quoted site leaves `unknown` at 0 because
the closed-world recogniser accepts both quotes).  If you were on the other side of D1, D2 or D4: is the settlement
right, and is anything in your original answer still standing?
**Q4 -- the repair's own pass 2.**  Name the smallest change to a probe, to `gate_hygiene.sh` or to the deriver that
re-opens what the REPAIRED rows guard while every readiness row stays green -- and the row you expect to stay green.
**Q5 -- records.**  Is any sentence added by the repair (the rewritten grandfather note, the classifier comment, the
WHOLE_FULL comment, the deriver header, the crime_width comment) false today, or stale the moment it lands?

If, while verifying a claim, you found something ELSE -- say so.

End with a seat record: model, what you read, what you ran.


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
