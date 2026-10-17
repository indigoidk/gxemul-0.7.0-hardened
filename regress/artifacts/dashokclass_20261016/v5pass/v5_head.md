# V5 PASS -- `dashokclass`: the dashboard's legacy class and the entry-domain check, v5 = EACH PIN'S DUAL EDGE

Four seats, by the owner's roster of 2026-10-16: Fable 5.1, GPT-6 Astra, Grok 4.7, GLM 5.3.  Opus, agy, kimi, deepseek and
minimax are DELIBERATELY NOT FIRED under that roster.  An ordinary review of a records tool (the dashboard generator), a
pre-commit check over its JSON ledger, and the controls that pin both.  READ-ONLY: write nothing to any project tree.  The
tree is `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC`; the v5 files are STAGED under
`regress/artifacts/dashokclass_20261016/staged_v5/` (mirroring `tools/`; v5 changes only two title lines of v4's); the
controls are `run_controls_v5.py` and `run_mutants_v5.py` beside it, run with CTL_CHECKER / CTL_RENDER / CTL_PRECOMMIT naming
the staged files; the v4-pass answers are in `v4pass/` (Fable's mirror measurements in `v4pass/fable5_meas/`).  Everything a
packet-fed seat needs is inlined below.

**Why v5.**  The v4 pass found 21 one-edit mutants passing all 72 v4 controls, 15 of them at decisions v4 listed as pinned,
and Fable 5.1 named their one shape: **each pin tested ONE edge of its decision** -- the trailing end of a key field but not
the leading one, the first literal line but not the binding that takes effect, a number but not its label, a substring but
not the whole tooltip, two branches of Q2's three.  So v5 rows the DUAL edge of every pin: for each decision, the edit its v4
pin would not see.  The staged CODE is unchanged (the seats found no defect in it); the controls grew from 72 to 96 and the
kill table from 66 to 105 mutants.  **This pass's job is to VERIFY that every pin now holds at both edges**, and that no
decision of the checker, the renderer change or the Q2 block is missing.  The chain closes on the first pass whose zero floor
breaches survive adjudication; if you find none, NAME THE DECISIONS YOU CHECKED.  Check the premises in 2b; do not ratify them.

<TOKEN_LINE>

## 1. The v4-pass verdicts

* **Fable 5.1 -- SHIP WITH CHANGES (18)** (`v4pass/fable5_dashokv4.md`; claude-fable-5-1 throughout).  Measured in a mirror:
  72/72 and the 66-mutant table reproduce byte for byte; 29 mutants of its own through the 72.
* **GPT-6 Astra -- SHIP WITH CHANGES (4)** (`v4pass/codex_dashokv4.txt`).  Ten survivors run in memory.
* **Grok 4.7 -- SHIP WITH CHANGES (6)** (`v4pass/grok_dashokv4.txt`).  Six survivors traced.
* **GLM 5.3 -- SHIP WITH CHANGES (4)** (`v4pass/glm_dashokv4.txt`).

## 2. Every finding, numbered, with my disposition

| # | seats | finding | disposition |
|---|---|---|---|
| K1 | Fable, Grok, Astra | the checker-side padded glyph: `str(x["d"]).strip() in DOMAIN` passes all 72 (only the renderer's R1h held a padded ✓), so Q2 would admit an answer the dashboard shows as legacy | **PINNED**: C28 (a new answer before the cutoff with d " ✓" -> rc 1).  Mutant `d_dompad` |
| K2 | Fable | C27 read the FIRST `DOMAIN = ` / `D_CLASS = ` line; a second assignment further down is the one that takes effect, and passes | **PINNED**: C27 walks each file's ast -- exactly ONE binding of the name anywhere (every store, any `global` refused), at module level, its literal the four.  Mutants `d_domredef`, `r_dclassredef` |
| K3 | Fable, Grok | `summary()` counting by a stripped d passes: R2 recomputes on the shipped ledger, which holds no padded glyph | **PINNED**: R2b (the FIXTURE page's strip, exactly, against the fixture's own counts -- its padded ✓ and its null count legacy).  Mutant `r_sumstrip` |
| K4 | Fable, Grok, Astra | the key's LEADING end: `.lstrip()` on the date, d, seat, phase or note, and a row-id strip, pass (C25 edited only the trailing end; the CONTRACT's "C25 edits the ends" was false) | **PINNED**: C25l (a row id with a trailing space), C25m-q (date, d, note, seat, phase each with a LEADING space), C25r (a row id with a leading space).  Mutants `d_rowstrip`, `d_rowrstrip`, `d_rowlstrip`, `d_datelstrip`, `d_dlstrip`, `d_notelstrip`, `d_seatlstrip`, `d_phaselstrip` |
| K5 | Fable, Astra | each refusal line's content: the cutoff reason replaced, the ceiling reason emptied, row and phase swapped -- C11 counted lines, W2 checked a prefix | **PINNED**: the WHOLE refusal line at C3 (the cutoff reason), C6 (an undated entry: `date (none)`, no ISO clause), C9 (a frozen copy: the ceiling reason, every identifier in order) and C19a (the ISO clause).  Mutants `d_cutreason`, `d_ceilreason`, `d_rowphaseswap`, `d_hintundated`, `d_datenone` |
| K6 | Fable | the summary's baseline number equals the within-count wherever a row reads it (1356/1356, 0/0), so printing the within-count passes | **PINNED**: every C12 row's summary EXACTLY -- the fixture baseline holds N+1 and a refused entry leaves N within, so the two differ; C1 and C11 exact too (which also pins "inclusive").  Mutants `d_basewithin`, `d_cutoffmsg` |
| K7 | Fable, Grok, Astra | the ISO shape anchored at its end (`^...$`) refuses a matched `2026-10-17T12:00:00` by nothing | **PINNED**: C12s (a FROZEN identity dated `2026-10-17T12:00:00` -> rc 1).  Mutant `d_isodollar` |
| K8 | Fable, Grok, Astra | the baseline row test at its clauses: `len(k) >= 7`, `isinstance(k[6], int)` (a bool is an int), `k[6] != 0`, the string test narrowed -- each passes; the CONTRACT's `> 0` -> `>= 0` "equivalent" holds for the ceiling's arithmetic, not for the promised malformed-baseline exit | **PINNED**: C17c-i, the shipped baseline plus ONE misshapen row each (eight fields; a count of true; -1; 0; 1.0; a numeric first field; a numeric note sha) -> rc 2.  Mutants `d_len7ge`, `d_boolcount`, `d_negcount`, `d_zerocount`, `d_floatcount`, `d_str1`, `d_str5`.  The "equivalent" disclosure is dropped |
| K9 | Fable, Astra | R1e asserted the record line as a SUBSTRING, so dropping the class line from every cell with a record beside it passes | **PINNED**: R1e asserts the WHOLE tooltip (class line, date, note, record line).  Mutant `r_tipnorecord` |
| K10 | Fable, Grok, Astra | an explicit `"d": null` on the RENDERER is unrowed (C26 pins only the checker): rendering it pend, or skipping its class line, passes | **PINNED**: a fixture null entry -- R1n (legacy, the glyph `None`) and R1g (its whole tooltip).  Mutants `r_nullpend`, `r_tipnotnull` |
| K11 | Fable, Astra | the strip's LABELS: "1397 approved" passes (R2 read the numbers) | **PINNED**: R2 asserts the whole strip string.  Mutant `r_striplabel` |
| K12 | Astra, Fable | Q2's `else` narrowed to `elif [ $_cedrc -eq 2 ]` passes, leaving rc 7 or 127 silently green; dropping `2>&1` is unread | **PINNED**: W7 (a stub checker exiting 7 with its message on STDERR -> BAD "could not run (rc 7): <that message>"), W8 (python ABSENT from the PATH -- a real launch failure, rc 127 -> BAD).  Mutants `w_elif2`, `w_no2to1` |
| K13 | Astra, Fable | C24 is confounded: the shipped ledger carries five off-domain NOTSEAT records, so `d_isheld` reddened C24 for the LEDGER's reason | **FIXED**: C24 runs in a ledger holding only its own entry |
| K14 | Grok, Fable | the whitespace glyph's character set: `.strip(" \t")` passes (R1d held a space and a tab; R3's presence pin was the only thing that saw it) | **PINNED**: R1d adds a newline-only and an NBSP-only d.  Mutant `r_wsset` |
| K15 | Astra, Fable | the two CSS rules the class adds are read by nothing: `font-size:0` makes every legacy glyph invisible and passes | **PINNED**: R5 (both rules, exactly, on the page).  Mutants `r_css0`, `r_cssoutline` |
| K16 | Grok, GLM | a ledger with NO `rows` key is unrowed (`.get("rows", [])` would walk it as empty) | **PINNED**: C21i (`{}` and `{"seats": []}` -> rc 2).  Mutant `d_rowsabsent` |
| K17 | Fable | `str()` of d in the key: dropping it is equivalent on the baseline, but a list d raises in the Counter -- rc 1 WITH a traceback | **PINNED**: C26b (a new answer whose d is a LIST -> rc 1, no traceback).  Mutant `d_nostr` |
| K18 | Fable | equivalent or out-of-scope edits | **DISCLOSED / recorded**: `ISO.match` -> `ISO.search` (the pattern is `^`-anchored: tabled UNPINNED, measured to escape); `r_recheld` is HEAD's own record loop, outside this landing's diff; the Q2 section header is display only (`say` is stubbed in the W block) |
| K19 | GLM | a mis-typed note (list, None, dict) might be SKIPPED as a non-answer, rc 0 | **NO CHANGE, measured** (Fable 5.1, v4 pass): a list, None or dict note is refused rc 1, a bool rc 2; nothing is skipped.  C21h keeps the except-arm a measured rc 2 |
| K20 | GLM | a hold or record cell carrying an explicit off-domain d is unrowed | **NO CHANGE**: R1's fixture already holds both -- grok's HELD marker with d "HELD" (renders hold) and kimi's NOTSEAT record with d "OK" (renders a record, ∅) |
| K21 | GLM | the 72-row enumeration was not checkable from the packet | **FIXED in the packet**: section 4a inlines the controls whole |
| K22 | Fable, Astra | two TITLE lines kept the retired identity wording: the checker's docstring ("OR IS ONE OF THE ENTRIES FROZEN WHEN THIS CHECK LANDED") and the Q2 banner ("OR IS A FROZEN LEGACY ENTRY") | **FIXED** in `staged_v5` (section 3): "within the (frozen) legacy ceiling" |
| K23 | GLM, Fable, Astra | records: 5d's "killed by exactly C15/C16" (v4 kills `d_nonote2` by C15 C16 C25e C25f); "miss the baseline everywhere" (on HEAD's ledger the d fold changes 1,100 of 1,356 frozen keys, the note strip 2, the note fold 1,352); "68/72 on v3 (the four structure rows)" folds in C21g, a baseline object | **CORRECTED** in the CONTRACT, the CHANGELOG draft and `run_mutants_v5.py`'s comment on the one-sided folds -- that comment was corrected AFTER the kill table ran (the diff is comment lines only; the table's behaviour is unchanged) |
| K24 | Fable | RULINGS_C's "5,150 at the ruling's HEAD": 5,150 is the count at e483d931; at c64445fa, which committed the file, 5,167 | **CORRECTED** (section 5c) |
| K25 | Fable, Astra, Grok | `dashmissingd`'s "158 / 127 / 71" came from a screen whose regex was never written down; nobody could reproduce it | **REPLACED by a deriver**: `dashmissingd_census.py` now carries the screen, `/not[ -]fired|roster/i`, and prints 222 entries / 200 untokened / 87 with no d at HEAD 8bf8b5a1 -- the record cites that output |
| K26 | Astra | the sha1-16 disclosure gave one figure for two searches | **CORRECTED**: a note passing as a FROZEN entry's is a fixed-target second preimage (~2^64); an arbitrary collision between two new notes (~2^32, birthday) passes nothing |
| K27 | GLM | J3's red MECHANISM ("the v3 rows reddened for the ledger's reason") was asserted, not derivable from the packet | **KEPT, with its measurement named**: Fable 5.1 measured the shipped ledger's 21 ⏸ and 35 … answers (v4 pass, census) -- the reason the un-isolated rows went red |
| K28 | all four | NOTSEAT on the five not-fired entries | **UPHELD unanimously** (Astra withdrew its advice after measuring H: 9/9 untokened, 4/9 tokened): they stay untokened on this landing; `dashmissingd` carries the RULE question and Fable's mechanism (an entry-scoped "not fired by owner roster" token that `is_answer` treats as a non-answer, the renderer as a record, section H as roster-excused -- an owner decision).  Nine recorded seats are not nine reviews, and the prose says so |

## 2b. Premises to CHECK (stated as questions)

* **Every pin at both edges.**  For each decision in the CONTRACT (section 4a's docstring), does the row named on the OTHER
  edge actually go red under the edit its v4 pin missed?  The kill table (section 4c) claims so for 103 of 105 mutants.
* **Is "the dual edge of each pin" the whole class**, or does some decision have a THIRD edge -- an edit neither the v4 pin nor
  the v5 row sees (a middle-of-field strip is disclosed; what else)?
* **The ast walk (K2).**  Does counting every `Name` store of DOMAIN / D_CLASS, plus `global`s, catch every way a second
  binding can take effect -- or is there one it misses (`globals()[...]`, an import, a function attribute)?
* **W8's PATH.**  Is "python absent from the PATH" a faithful launch failure, and does the git-bash wrapper add any directory
  holding a python?  (The receipt shows `env: 'python': No such file or directory`, rc 127.)
