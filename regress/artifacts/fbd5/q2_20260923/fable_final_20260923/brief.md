# Final adjudication, two rounds -- GXemul hardened fork, 2026-09-23 (you are the last seat; every other seat has answered)

Start your answer with the token FABLE_FINAL_20260923 and then quote, verbatim, the FIRST LINE of
`C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\CHECKPOINT.md`.  Then one verdict line per round:
`VERDICT #545: SHIP` or `VERDICT #545: HOLD -- <reason>`, and `VERDICT census: SHIP` or `VERDICT census: HOLD -- <reason>`.

READ-ONLY.  Do not edit, build or run anything under `GXEMUL-SEC/`, `est/`, `build/` or `build-asan/`.  The tree under
review is `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\`; the `src/` at the project root is 2021 upstream -- ignore it.
**Please do not simply ratify.**  Check premises against the files; when you agree, say what you checked.  Be hardest on
the dispositions I made in my own favour.  Plain engineering terms throughout: "variant" for a one-line code change
used to test a regression table, "undetected" when every row still passes.

## ROUND 1 -- #545 (fbdeclinefive): does the review chain close on repair 3e's pass, with repair 3f (records only)?

**Context.**  #545 made five register accesses of the DC21285 footbridge model (`src/devices/dev_footbridge.c`) decline
and announce once instead of ending the process.  Its regression table is `regress/diff_footbridge.c` (864 rows; it
#includes the device and calls the access function directly; `regress/gate_offline.sh` pins the counts).  Repairs 3,
3c, 3d, 3e each followed a review pass; the carrier's repair-chain rule closes the chain on the first VALID pass (diff
delivered, roster named, a zero carried with its denominator) that finds no floor breach.  3e closed two classes in one
diff with NO new row: (A) the three X14 rows that claim fields KEPT now check them after each access (`ZSNAP`/`ZKEPT`);
(B) `pad_kept()` requires the buffer bytes above the access width untouched after X6's declined accesses and X9/X10's
legal reads.

**3e's pass.**  Panel `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\panel_20260923_210234\` -- codex, grok, glm, deepseek
DO NOT SHIP; agy, minimax, kimi-k3:cloud SHIP; the kimi CLI walled on its weekly limit (covered by kimi-k3:cloud).  A
dedicated codex job: `_scratchpad\fbd5\q2h\codex_ded\` (FAIL).  The Opus measuring seat:
`GXEMUL-SEC\regress\artifacts\fbd5\q2_20260923\q2h_opus\` -- SHIP; **its first turn fell back to claude-opus-4-8 after a
refusal; resumed, its verdict and corrections are claude-opus-5-5's** (see `MANIFEST_NOTE.txt` there).

**My dispositions.**  Every dissent, as I read it, found both closures correctly implemented and the CONTRACT (the
comment above X6) overstating them: per-access checks exist on the three rows that CLAIM kept fields, not on every
multi-access row (grok: `d->irq_asserted = 1` on the IRQ_STATUS read passes -- the DEVINIT reads row claims values);
`pad_kept` runs only after X6's declines and X9/X10's reads, so a fetch past `len` no channel uses, a store past `len`
inside a legal write (codex: `data[len] = 0` in the Clear write) and the common tail's write-back at other reads pass.
The Opus seat found that last gap at VENDOR_ID/TIMER_1_VALUE; I re-measured it (predictions first) and found it also at
+0x288 and +0x28c: `GXEMUL-SEC\regress\artifacts\fbd5\q2_20260923\qwb_20260923\` (all four keyed 8-byte write-backs pass
864/864; an IRQ_STATUS-keyed control fails 24 rows; len 8 fails 144).  (B) was an above-floor addition -- the floor's
DEPENDS-ON enumeration ends at the predicates dominating the five edited arms, and the tail and the fetch are not among
them -- so its remainder is FILED as `fbbufbounds` (draft: `_scratchpad\fbd5\records\bugs_draft545_r3e_additions.md`),
not rowed.  **Repair 3f** is records only: `_scratchpad\fable_final_20260923\r3f.diff` (6 hunks); comment-stripped
source identical to 3e, output identical, 864/0 (`...\q2_20260923\r3f_20260923\verify_r3f.out`).  CHANGELOG text for
these passes: `_scratchpad\fbd5\records\cl545_r3pass_fill.md`.

**Questions.**
* **Q1.**  Is ANY of 3e's-pass dissents actually a FLOOR BREACH -- an undetected variant at one of the five edited arms,
  the two head tests, or a cell the contract's COVERED list claims -- rather than an overstated sentence?  Read at least
  the final blocks of `codex.txt`, `grok.txt`, `ollama_glm.txt`, `ollama_deepseek.txt` and the codex_ded answer.
* **Q2.**  Is every sentence 3f changed now TRUE of the 864 rows?  Quote any that is not.
* **Q3.**  Filing `fbbufbounds` (above the floor) rather than rowing it: right?  If not, what is owed in-round?
* **Q4.**  Does the chain close on 3e's pass -- valid by the rule's three conditions?  If not, name the one measurement
  that would close it.
* **Q5.**  Which of my accepted dispositions is wrong?

## ROUND 2 -- hygienecensus: the owner's "one more pass, then file" -- is F6e right, and is the filing right?

**Context.**  `tools/derive_hygiene_pins.sh` derives and writes the pins of `regress/gate_hygiene.sh`'s readiness census
(which pty probes lack prompt detection; the grandfather list; the whole-buffer allowlist); `regress/census_tokens.py`
is its token classifier.  **Owner ruling (2026-09-23, verbatim intent): run ONE more review pass (the F6d pass); fix only
findings a REAL probe name or REAL git-bash/WSL use could trigger; FILE exotic-input findings (crafted names,
deliberately broken interpreters, hand-edited gate layouts, unusual environment variables) as one LOW item.**

**The F6d pass.**  Panel `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\panel_20260923_202350\` -- codex and deepseek DO NOT
SHIP; agy, grok, glm, minimax, kimi-k3:cloud SHIP; the kimi CLI walled (covered).  Dedicated codex:
`_scratchpad\census0923\codex_ded\codex_c6.txt` (no functional defect; one false comment).  The Opus seat:
`_scratchpad\census0923\opus_c6\SUMMARY.txt` (DO NOT SHIP; measured fixes).

**What I fixed as REAL (F6e = `_scratchpad\fable_final_20260923\f6e.diff`, 10 hunks over the three files):**
* codex (panel): both writers wrote through an unclosed temporary, so a flush failing at close (a full disk) was
  swallowed and the tool printed success over a truncated gate -> `with io.open(...)`.
* the Opus seat F1: the parser check read files with "utf-8", keeping a byte-order mark, so a real BOM probe (agy's
  committed witness `regress\artifacts\wdcaltdigin\agy_altdigin_witness_20260911.py`) could be neither grandfathered
  nor released -> "utf-8-sig".
* the Opus seat F2: a grandfathered probe that stops forking its own pty (moved onto drive_guest) could not be released
  and blocked `--write` -> the parser check now applies to names still in the pty census; a name that left it is
  released unless its file still makes a pty another way (forkpty, pty.spawn), which is refused with a true message.
* the Opus seat F3 and deepseek/codex-ded records: messages chosen by the parser's return code; the sink grammar, the
  count-check limits and the header named truly.

**Controls, predictions first:** `GXEMUL-SEC\regress\artifacts\hygienecensus_20260923\controls_c6e\` -- read
`PREDICTIONS.txt` (mtime before any run) and `RESULT.txt`.  The Opus seat's own case matrix re-run on the shipped F6e
differs from its measured fix only in the three reworded messages; the full-disk failure reproduces on F6d (success
printed, gate truncated) and fails loudly on F6e (rc 6) -- but BOTH leave the gate truncated.

**What I FILE (LOW), not fix:** `_scratchpad\census0923\bugs_census_residue_draft.md` (crafted names split into real
entries; PYTHONOPTIMIZE dropping asserts; a classifier that dies part-way passing the canary; hand-edited gate layouts;
the gate's eval of its own list) plus three residues of the F6d pass: ANY `.endswith(...)` call is credited as
readiness, by the census and the parser alike (glm); a census/parser disagreement (a `match` class pattern) has no tool
exit -- the probe must be edited (kimi-k3:cloud); the gate's `whole_full=$(printf '%s\n' $whole_files | awk ...)` expands
unquoted (grok; no real token has a glob character).  And, from c6e: a failed write leaves the gate truncated (F6e says
so loudly; an atomic replace would keep the old gate).  `armbdtreadiness` (LOW) carries no expiry, by owner ruling.

**Questions.**
* **Q6.**  Under the owner's ruling, is each classification right -- fixed as REAL vs filed as exotic?  In particular:
  is the truncated-gate-after-a-failed-write residue correctly FILED, given a full disk is ordinary use?
* **Q7.**  Does F6e itself do anything wrong?  Quote any F6e comment that is false.
* **Q8.**  Anything that must still be fixed before this round commits (the ruling forbids another review pass)?
* **Q9.**  Which of my dispositions is wrong?

End with: files you read, and anything you ran.
