# `#566` (wiringcliff): `regress/artifacts/ip30abortkill/ip30_abort_probe.py` is wired into gate 14 thirteen days before its exemption would refuse every commit -- 41 checks score all 33 rows by name; floor clauses (a) and (c) measured through the block; the probe's stale CONTRACT and the bug file's stale `ip30abortkill` entry corrected; two rows filed

**The cliff.**  Section R (`tools/pipeline/check_probe_wiring.py`) held `#531`'s detector for four guest-reachable
`abort()` calls in `src/devices/dev_sgi_ip30.c` (`686d179c`) in its EXEMPT table: dated 2026-09-20 with `#531`, then
re-dated three times -- `eec0f4a3` to 2026-09-27, `04500deb` (`#550`) to 2026-10-15, `7b23b785` (2026-10-16, a four-seat
ruling, GPT-6 Astra dissenting "wire now") to 2026-10-30.  HEAD's checker run with `--today 2026-10-31` names it
EXPIRED.  Witness `harness:` -- the round's subject is the test apparatus.

**What ships.**
* `regress/gate_arm.sh` -- a block at depth 0 after the `#564` `sgi_mte_decline` block, running the probe from its
  artifacts path (as `gate_sh_rounding.sh` runs `gdrom_pio_null_probe.py`).  PARSE BEFORE SCORE: exactly one well-formed
  `IP30ABORT_RESULT=`, `IP30ABORT_CONTROL=` and `IP30ABORT_DONE` line, so a crash or kill before the report, or a missing
  probe file, is a FAIL, never a SKIP; then CONTROL `OK`, the probe's exit status 0 (a death after the report), EVERY row
  by name exactly once (`^  NAME  *got=[^ ]*  *want=[^ ]*  *ok  ` -- the status token sits mid-line, before the note, so
  gate 14's usual ` ok$` would match nothing; six names overflow their 12-column field), and five counts pinned to
  literals: rows run (the RESULT denominator) 33, rows correct 33, rows emitted 33, green 33, red 0.  41 checks when
  green.  Its comment discloses the cost -- about 9.5 minutes, every surviving session waiting out the probe's 12 s
  death poll -- that nothing times the probe out (the reap after the poll's SIGKILL blocks), and that a load stall is NOT
  always a red: a session the poll kills reads like a run whose remaining accesses never happened -- a stall before its
  access leaves its `alive` and `no` rows green (the kill rows, `acc 30 rd`, `tick 49`, the read arms' `txt` rows) and
  its `yes` row red, and a count row that wants ONE announce reads green whenever exactly one was captured, so on
  `V2_assigntick` the `xbit rev2` session stalling with one announce captured, every other session passing, leaves all
  41 checks green (filed, `ip30stallgreen`).
* `tools/pipeline/check_probe_wiring.py` -- the EXEMPT tuple and its 24-line comment deleted; a dated DISCHARGED note
  beside `#565`'s; the MANIFEST entry's own `*** RUNS IN NO GATE: see EXEMPT. ***` corrected, and the
  `ip30_tick_probe.py` comment's `dated-exempt in the open` qualified.
* `tools/precommit_check.sh` -- `SCORE_CLAIMS_MANIFEST` 34 -> 35, for the new `ip30_abort rows run ... 33` pin.  Section U
  checks no prose for this pin: it reads only comment lines (`#`, `*`, `//`) naming the stem, of which there are none,
  and docstrings at `regress/<stem>_probe.py` or `regress/<stem>.py`.
* `regress/artifacts/ip30abortkill/ip30_abort_probe.py` -- records only: a dated note above its CONTRACT, whose CATCHES
  list, fourteen-cell paragraph and "THE CLOSURE IS OWED" were the 27-row instrument's while the file's own later
  sections record the 33-row closure -- six statements corrected (four announce sites and three ISR sites, not six and
  five; `latch 1x` on the write arms; the ten enumerated latch cells and the `xbit rev2` a measured escape added after
  them; the pre-fix red now 23 of 33 rows; the first CATCH resting on the pre-fix build, not a kill table; THE CLAIM
  UNDER TEST quoting the pre-fix file).  Its AST, docstring excluded, is identical to HEAD's.
* `OUTSTANDING_BUGS.md` -- the `ip30abortkill` entry's "28 ROWS ... PRE-FIX owed ... pass 2 owed" corrected in place
  (pass 2 `panel_20260917_215210`, 2026-09-17; F2 and kill tables 3-5, 2026-09-18), and a `#566` section.
* `tools/pipeline/ledger.json` -- `wiringcliff`'s state note and this round's seat entries, Fable's two stages as HELD
  markers with the row's `hold_question`; `ip30abortkill`'s state note, and the 33-row pair beside its 21-row witness;
  two rows FILED, `ip30stallgreen` (LOW) and `fableheldform` (MED).  `fable_queue.md` regenerated; `matrix.html` rendered.

**Measured** (all under `regress/artifacts/ip30abortkill/gatewire_20261018/`).
* Gate 14, alone, on the scratch clone's HEAD binary (md5 `25ac428c`, unchanged after): PASS, 1225 checks, rc 0,
  12:37:40 -> 14:49:35 -- the block's 41 among them, all green (`gate14/RUN.txt`, `gate14/gate_arm.out`,
  `gate14/ip30_abort.log`).  The other live session on this machine paused its CPU-heavy work for the run.
* The probe through the block's scoring text, in a scratch clone of `build/` (`legs/legs566.sh`: `cp -a build`, the other
  session's five uncommitted sources set back to HEAD; `build/` untouched): HEAD rebuilt 33/33, 41 of 41 green, 567 s;
  HEAD with `dev_sgi_ip30.c` set to `686d179c^`'s -- clause (a), all four `abort()` calls back -- 10/33, 23 rows and 26
  checks red, every abort site among them (`kill 20 rd`, `kill 28 rd`, `kill 30 wr`, `tick 50`, `kill 20 wr`, `kill 28 wr`
  read DEAD); `/nonexistent/gxemul` and `/bin/true` -- clause (c), the null media for a runtime probe -- CONTROL=DEAD and
  38 checks red (`legs/LEGS.out`).  Re-scored by the final scoring text, the same (`legs/RESCORE.out`: gate_arm.sh md5
  `bf7b6af6`, the scoring text `21d7b874`; the legs ran the probe as `5bf04f2d`, before its docstring note, and it ships
  as `7fbf52ab` with an identical AST).  In the full gate an absent binary stops at `need_exec` first, a SKIP;
  `/bin/true` reaches the block.  The clone was restored to HEAD and cleared both parts (`legs/RESTORE.out`).
* The scoring text against doctored copies of the 33/33 log (`selftest/SELFTEST.out`): 15 cases, each red where it
  should be -- a row turned FAIL, lost, duplicated or renamed; a DEAD vehicle; an empty log; DONE removed or doubled;
  RESULT doubled, contradicted or shrunk; CONTROL doubled or malformed; the good log under a non-zero exit status; and a
  REAL invocation of a probe file that does not exist (python3 exits 2).
* Section R (`controls/R_CONTROLS.out`, on the final gate): the commit checker with the wired gate passes (77/85
  detectors run by a gate, 8 dated-exempt, 44 witnesses correctly ungated) and at `--today 2026-10-31` fails only on the
  other session's four expiries; HEAD's checker reports STALE EXEMPTION at the exec line; the exec line commented out
  reports UNWIRED DETECTOR; HEAD's checker with the gate unwired passes today and at `--today 2026-10-31` reports the
  probe EXPIRED.  Section U: `SCORE_CLAIMS_PINNED=35`, PASS, 13 of 35 stems with a docstring checked.

**Panel.**  Pass 1 (`brief_p1_body.md`): GPT-6 Astra 4 flags and a list of controls, Grok 4.7 7, GLM 5.3 11 (packet-fed;
most "not settleable from the packet", settled here by reading `lib.sh`, `git log` and the checker).  Pass 2
(`brief_p2_body.md`): GPT-6 Astra 9, Grok 4.7 12, GLM 5.3 5 -- every wording error above was theirs to find, among them
three in this round's own repairs; GLM's "hunks one line short" was rejected (both diffs were inlined byte-for-byte), and
so was Grok's "not a clone of `build/`" (the legs script copies it).  F2 (`brief_f2_body.md`): GPT-6 Astra 3 flags, GLM 5.3 4, Grok 4.7 6 -- the stall sentences once more (a count row reads green
only with exactly one announce captured), the ten-cell colon, the leg script's clause (b), `the read sessions`, and
`fableheldform`'s count (16 entries on ten rows once keyed on the property, eight when keyed on the spelling `NOT FIRED`) --
all taken; GLM's misread hunk header and its L5 objection rejected; D3 upheld by all three.  Fable 5.1 was
NOT TRIED on pass 1 or pass 2, an omission against the owner's 2026-10-17 directive (one try per pass); TRIED on F2 and
WALLED (`You've reached your Fable limit`, HTTP 429, `fable5_f2_WALL.txt`) -- a seat failure, recorded as HELD with its
question.

**Not done here, and why.**  `ip30abortkill` stays `in work` (all three seats): before it closes, its witness must lead
with the 33-row pair, and `#531`'s clause (b) -- `abort()` re-inserted at each fixed site of the FIXED file -- is held by
no kill table; whether its two disclosed escapes (`V7_nocounter`, 32/32 in kill table 4; the width axis `V8_len4`, 33/33
in kill table 5) need a carrier is that commit's question.  Target: before the 2026-10-25 battery.  The stall false-green
is disclosed and filed, not repaired: shortening the poll is what reads a slow abort as alive, and the repair is a probe
change owing a kill table.  The 16 fable5 entries on ten rows since the owner's 2026-10-17 hold that record a non-answer
without a stage token -- each counted as an ANSWER by `stage_tokens.is_answer()` -- are filed as `fableheldform`, for their
own records commit.
