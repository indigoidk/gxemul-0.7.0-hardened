
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
