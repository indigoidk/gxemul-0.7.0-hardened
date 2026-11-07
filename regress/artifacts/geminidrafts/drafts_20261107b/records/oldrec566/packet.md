# Reading task: oldrec566 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBOLDREC566-5689` on a line of its own.

# GXemul hardened fork -- RECORDS CHECK of one landed round's CHANGELOG block: #566 wiringcliff (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator and this fork records each
fix in a CHANGELOG round block.  The block below has landed; a flagship review of it is still owed.  You cannot read files, so
judge the block AS WRITTEN.  Do not simply ratify it.  A bracketed dated note inside the block is this project's in-place
correction form (it quotes the text it corrects); it is not by itself a contradiction.

## The round block (CHANGELOG.md lines 3124-3213 of CHANGELOG_8d9df658.md; each line carries its own number -- cite those numbers)

```text
 3124| # `#566` (wiringcliff): `regress/artifacts/ip30abortkill/ip30_abort_probe.py` is wired into gate 14 thirteen days before its exemption would refuse every commit -- 41 checks score all 33 rows by name; floor clauses (a) and (c) measured through the block; the probe's stale CONTRACT and the bug file's stale `ip30abortkill` entry corrected; two rows filed
 3125| 
 3126| **The cliff.**  Section R (`tools/pipeline/check_probe_wiring.py`) held `#531`'s detector for four guest-reachable
 3127| `abort()` calls in `src/devices/dev_sgi_ip30.c` (`686d179c`) in its EXEMPT table: dated 2026-09-20 with `#531`, then
 3128| re-dated three times -- `eec0f4a3` to 2026-09-27, `04500deb` (`#550`) to 2026-10-15, `7b23b785` (2026-10-16, a four-seat
 3129| ruling, GPT-6 Astra dissenting "wire now") to 2026-10-30.  HEAD's checker run with `--today 2026-10-31` names it
 3130| EXPIRED.  Witness `harness:` -- the round's subject is the test apparatus.
 3131| 
 3132| **What ships.**
 3133| * `regress/gate_arm.sh` -- a block at depth 0 after the `#564` `sgi_mte_decline` block, running the probe from its
 3134|   artifacts path (as `gate_sh_rounding.sh` runs `gdrom_pio_null_probe.py`).  PARSE BEFORE SCORE: exactly one well-formed
 3135|   `IP30ABORT_RESULT=`, `IP30ABORT_CONTROL=` and `IP30ABORT_DONE` line, so a crash or kill before the report, or a missing
 3136|   probe file, is a FAIL, never a SKIP; then CONTROL `OK`, the probe's exit status 0 (a death after the report), EVERY row
 3137|   by name exactly once (`^  NAME  *got=[^ ]*  *want=[^ ]*  *ok  ` -- the status token sits mid-line, before the note, so
 3138|   gate 14's usual ` ok$` would match nothing; six names overflow their 12-column field), and five counts pinned to
 3139|   literals: rows run (the RESULT denominator) 33, rows correct 33, rows emitted 33, green 33, red 0.  41 checks when
 3140|   green.  Its comment discloses the cost -- about 9.5 minutes, every surviving session waiting out the probe's 12 s
 3141|   death poll -- that nothing times the probe out (the reap after the poll's SIGKILL blocks), and that a load stall is NOT
 3142|   always a red: a session the poll kills reads like a run whose remaining accesses never happened -- a stall before its
 3143|   access leaves its `alive` and `no` rows green (the kill rows, `acc 30 rd`, `tick 49`, the read arms' `txt` rows) and
 3144|   its `yes` row red, and a count row that wants ONE announce reads green whenever exactly one was captured, so on
 3145|   `V2_assigntick` the `xbit rev2` session stalling with one announce captured, every other session passing, leaves all
 3146|   41 checks green (filed, `ip30stallgreen`).
 3147| * `tools/pipeline/check_probe_wiring.py` -- the EXEMPT tuple and its 24-line comment deleted; a dated DISCHARGED note
 3148|   beside `#565`'s; the MANIFEST entry's own `*** RUNS IN NO GATE: see EXEMPT. ***` corrected, and the
 3149|   `ip30_tick_probe.py` comment's `dated-exempt in the open` qualified.
 3150| * `tools/precommit_check.sh` -- `SCORE_CLAIMS_MANIFEST` 34 -> 35, for the new `ip30_abort rows run ... 33` pin.  Section U
 3151|   checks no prose for this pin: it reads only comment lines (`#`, `*`, `//`) naming the stem, of which there are none,
 3152|   and docstrings at `regress/<stem>_probe.py` or `regress/<stem>.py`.
 3153| * `regress/artifacts/ip30abortkill/ip30_abort_probe.py` -- records only: a dated note above its CONTRACT, whose CATCHES
 3154|   list, fourteen-cell paragraph and "THE CLOSURE IS OWED" were the 27-row instrument's while the file's own later
 3155|   sections record the 33-row closure -- six statements corrected (four announce sites and three ISR sites, not six and
 3156|   five; `latch 1x` on the write arms; the ten enumerated latch cells and the `xbit rev2` a measured escape added after
 3157|   them; the pre-fix red now 23 of 33 rows; the first CATCH resting on the pre-fix build, not a kill table; THE CLAIM
 3158|   UNDER TEST quoting the pre-fix file).  Its AST, docstring excluded, is identical to HEAD's.
 3159|   *[2026-10-20, records (the late-review adjudication): the CATCHES list was not only the 27-row instrument's -- its M11
 3160|   line names `isr 28 rd val`, row 28, and the qualifiers on its last three entries came with the same F2 adjudication;
 3161|   the probe's dated block of 2026-10-20 lists this and the file's other stale sentences.]*
 3162| * `OUTSTANDING_BUGS.md` -- the `ip30abortkill` entry's "28 ROWS ... PRE-FIX owed ... pass 2 owed" corrected in place
 3163|   (pass 2 `panel_20260917_215210`, 2026-09-17; F2 and kill tables 3-5, 2026-09-18), and a `#566` section.
 3164| * `tools/pipeline/ledger.json` -- `wiringcliff`'s state note and this round's seat entries, Fable's two stages as HELD
 3165|   markers with the row's `hold_question`; `ip30abortkill`'s state note, and the 33-row pair beside its 21-row witness;
 3166|   two rows FILED, `ip30stallgreen` (LOW) and `fableheldform` (MED).  `fable_queue.md` regenerated; `matrix.html` rendered.
 3167| 
 3168| **Measured** (all under `regress/artifacts/ip30abortkill/gatewire_20261018/`).
 3169| * Gate 14, alone, on the scratch clone's HEAD binary (md5 `25ac428c`, unchanged after): PASS, 1225 checks, rc 0,
 3170|   12:37:40 -> 14:49:35 -- the block's 41 among them, all green (`gate14/RUN.txt`, `gate14/gate_arm.out`,
 3171|   `gate14/ip30_abort.log`).  The other live session on this machine paused its CPU-heavy work for the run.
 3172| * The probe through the block's scoring text, in a scratch clone of `build/` (`legs/legs566.sh`: `cp -a build`, the other
 3173|   session's five uncommitted sources set back to HEAD; `build/` untouched): HEAD rebuilt 33/33, 41 of 41 green, 567 s;
 3174|   HEAD with `dev_sgi_ip30.c` set to `686d179c^`'s -- clause (a), all four `abort()` calls back -- 10/33, 23 rows and 26
 3175|   checks red, every abort site among them (`kill 20 rd`, `kill 28 rd`, `kill 30 wr`, `tick 50`, `kill 20 wr`, `kill 28 wr`
 3176|   read DEAD); `/nonexistent/gxemul` and `/bin/true` -- clause (c), the null media for a runtime probe -- CONTROL=DEAD and
 3177|   38 checks red (`legs/LEGS.out`).  Re-scored by the final scoring text, the same (`legs/RESCORE.out`: gate_arm.sh md5
 3178|   `bf7b6af6`, the scoring text `21d7b874`; the legs ran the probe as `5bf04f2d`, before its docstring note, and it ships
 3179|   as `7fbf52ab` with an identical AST).  In the full gate an absent binary stops at `need_exec` first, a SKIP;
 3180|   `/bin/true` reaches the block.  The clone was restored to HEAD and cleared both parts (`legs/RESTORE.out`).
 3181| * The scoring text against 15 negative cases (`selftest/SELFTEST.out`), each red where it should be: thirteen doctored
 3182|   copies of the 33/33 log -- a row turned FAIL, lost, duplicated or renamed; a DEAD vehicle; an empty log; DONE removed
 3183|   or doubled; RESULT doubled, contradicted or shrunk; CONTROL doubled or malformed -- the unchanged good log under a
 3184|   non-zero exit status, and a REAL invocation of a probe file that does not exist (python3 exits 2).
 3185| * Section R (`controls/R_CONTROLS.out`, on the final gate): the commit checker with the wired gate passes (77/85
 3186|   detectors run by a gate, 8 dated-exempt, 44 witnesses correctly ungated) and at `--today 2026-10-31` fails only on the
 3187|   other session's four expiries; HEAD's checker reports STALE EXEMPTION at the exec line; the exec line commented out
 3188|   reports UNWIRED DETECTOR; HEAD's checker with the gate unwired passes today and at `--today 2026-10-31` reports the
 3189|   probe EXPIRED.  Section U: `SCORE_CLAIMS_PINNED=35`, PASS, 13 of 35 stems with a docstring checked.  [2026-10-20: no section-U
 3190|   receipt was archived with #566; these figures were re-derived against 8faf4a16 by the records check, receipt
 3191|   `regress/artifacts/ip30abortkill/argonlate_20261020/rederive_U_8faf4a16.out`.]
 3192| 
 3193| **Panel.**  Pass 1 (`brief_p1_body.md`): GPT-6 Astra 4 flags and a list of controls, Grok 4.7 7, GLM 5.3 11 (packet-fed;
 3194| most "not settleable from the packet", settled here by reading `lib.sh`, `git log` and the checker).  Pass 2
 3195| (`brief_p2_body.md`): GPT-6 Astra 9, Grok 4.7 12, GLM 5.3 5 -- every wording error above was theirs to find, among them
 3196| three in this round's own repairs; GLM's "hunks one line short" was rejected (both diffs were inlined byte-for-byte), and
 3197| so was Grok's "not a clone of `build/`" (the legs script copies it).  F2 (`brief_f2_body.md`): GPT-6 Astra 3 flags, GLM 5.3 4, Grok 4.7 6 -- the stall sentences once more (a count row reads green
 3198| only with exactly one announce captured), the ten-cell colon, the leg script's clause (b), `the read sessions`, and
 3199| `fableheldform`'s count (16 entries on ten rows once keyed on the property, eight when keyed on the spelling `NOT FIRED`) --
 3200| all taken; GLM's misread hunk header and its L5 objection rejected; D3 upheld by all three.  Fable 5.1 was
 3201| NOT TRIED on pass 1 or pass 2, an omission against the owner's 2026-10-17 directive (one try per pass); TRIED on F2 and
 3202| WALLED (`You've reached your Fable limit`, HTTP 429, `fable5_f2_WALL.txt`) -- a seat failure, recorded as HELD with its
 3203| question.
 3204| 
 3205| **Not done here, and why.**  `ip30abortkill` stays `in work` (all three seats): before it closes, its witness must lead
 3206| with the 33-row pair, and `#531`'s clause (b) -- `abort()` re-inserted at each fixed site of the FIXED file -- is held by
 3207| no kill table; whether its two disclosed escapes (`V7_nocounter`, 32/32 in kill table 4; the width axis `V8_len4`, 33/33
 3208| in kill table 5) need a carrier is that commit's question.  Target: before the 2026-10-25 battery.  The stall false-green
 3209| is disclosed and filed, not repaired: shortening the poll is what reads a slow abort as alive, and the repair is a probe
 3210| change owing a kill table.  The 16 fable5 entries on ten rows since the owner's 2026-10-17 hold that record a non-answer
 3211| without a stage token -- each counted as an ANSWER by `stage_tokens.is_answer()` -- are filed as `fableheldform`, for their
 3212| own records commit.
 3213| 
```

## Questions -- verdict line first

1. Does the block contradict itself anywhere -- two different numbers for one quantity, a total that its own parts do not sum
   to, a claim in one paragraph that another paragraph undoes?  Quote both places, with their line numbers.
2. Which claims are stated as MEASURED but cite no artifact, or cite one only by a bare file name that could be ambiguous?
3. Which sentences overclaim -- 'every', 'all', 'never', 'exactly' -- where the block's own evidence covers less?
4. What would a reviewer checking this block against its artifacts most likely find wrong?
When you count items the block enumerates, list them by name before giving the count.

End with one line: `RECBLOCK_566: <c> CONTRADICTIONS, <u> UNCITED, <o> OVERCLAIMS`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBOLDREC566: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
