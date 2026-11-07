# `ghostround` -- census, prototype checker, controls, and the owner's question

> **DURABLE COPY, banked 2026-11-06 by a records commit.**  The original is `_scratchpad/wghost/DECISION.md` (scratch, not durable; md5 55f16f74).  This banner and one marked change to the heading of the Files section are the only edits.  Copied beside it, byte-identical: `check_ghost_rounds.py`, `census.out`, `replay.out`, `replay_class.tsv`, `replay_class.out` and `controls/run_controls.out`.  Every other file this record names (`census.py`, `census_hits.tsv`, `triage_*.txt`, `replay.py`, `replay_hits.tsv`, `replay_class.py`, `writeback_delay.*`, the rest of `controls/`, the HEAD snapshots, `survey_*`, `ref_*`) stays in the scratch original only.  `PROVENANCE.md` here lists every file of that directory with its md5.

Scratch work for ledger row `ghostround` (filed 2026-08-29).  Everything here was read from
GXEMUL-SEC **at HEAD `2632277f`** (`git show HEAD:` / `git blame HEAD`), or read-only from older
commits for the replay.  The working tree was not read for any number.  Nothing under
`GXEMUL-SEC/`, `est/` or `build*/` was written; no gate, build, probe, panel seat or codex ran.

## Bottom line

1. **The row's own wording cannot see its own motivating case.**  At `d9efd339`, the commit
   before the `#479` rows were written back, each of the three carried nine research entries
   dated 2026-08-27, the ship day.  Entries carry a date and no time, so "an entry dated on or
   after the round" is satisfied by work done *before* the ship.  Replayed on every landing
   commit, that rule catches **2 of the 11** documented ghosts and would have failed **84 of 141**
   landings, including **10 of 10** in November, because a row a round files has no entry yet.
2. **The rule that works is "the row names the round".**  A pre-ship stage cannot know which
   round shipped it.  A write-back says `#479` (or `Round 479`).  Applied to the rows a round
   names **in its header** plus any named row still **`in work`**, it catches **11 of 11**
   documented ghosts and would have failed **20 of 141** landings: **13** with a real gap and **7**
   on references or filings only.  Since 2026-10-01 it would have failed **2 of 32**, both of
   them references.
3. **At HEAD the population is all false positives.**  Under the proposed default, **13** hits,
   and every one is an `in work` row that a later round only *references*.  Under the literal
   reading (every named row), **268** (date rule) or **184** (mention rule) hits, with **0**
   genuine ghosts and **0** parse noise.  Ghosts at HEAD read zero because each one was
   eventually repaired by hand (after 1 to 36 days).  The class is real; the replay measures it,
   and the HEAD census cannot.

## How the CHANGELOG is shaped (and how it was parsed)

* A **block** starts at every H1 outside a code fence, or at an H2 of a block shape.  H2 is the
  block level in the older stretch: `## Round 479 (#479) -- ...`, `## R11 (#438)`,
  `## Twentieth round (#224-#226)`, `## #561 -- records: ...`.  Other H2s (`## Gate`,
  `## Records corrections made in-round`, `## Not changed (assessed, ...)`) are subsections.
  An early, looser pattern split three blocks on those subsections; fixed.
* **Kinds**: ROUND (the header states its own round, e.g. `` # `#584` (2026-11-05) -- `fmtattr`: ``,
  `# Round #504 sgirandompixel --`, `## Round 495 (#495)`), RECORDS (`Records, ...`,
  `` `#584` Records (follow-up, ...) ``, `RECORDS/ADJUDICATION/SEAT AUDIT <date>`, `Probe wiring`,
  `Retrospective`), SECTION (the est-era file headers).  Only ROUND blocks are checked.  RECORDS
  blocks mostly *file* rows, and a filing is legitimately open.
* The block's **own number** is read only where a header states it (`` `#584` ``, `Round #504`,
  `Round 477 pass 2`, `R11 (#438)`).  `## Round wdcatapistswap -- the accept side of #495's guard`
  is unnumbered, and the `#495` there is a reference.
* **Row citations**: in the body, a code span that is exactly a row id, or a list whose every
  member is one (`` `ppcrlwimiwidth, ppcrldimimask, ppcgateimageskip` ``).  In the header, the
  same, plus a parenthesised list element (`(lecsrmask)`, `(sgirekills, the MTE half)`) or the
  word after the round marker.  **Not** a bare word elsewhere in a header: row `census` is also
  an English word, and `#546`'s header says "gate 6's readiness census was 24 probes stale".
  That was the only parse-noise pair found (the row is closed, so it never produced a hit), and
  the subject-position rule removes it.  Fenced code is skipped.
* **Dates**: the header's own date, read only where headers state one (first in a parenthesised
  group, or after `Records,`/`RECORDS`).  Otherwise the git blame date of the header line.
  `#550`'s header says "exemptions that all fell due on 2026-09-27" and the round landed
  2026-09-26.  The cutoff compares the blame (landing) date.

| parsing denominator (HEAD `2632277f`) | count |
|---|---|
| CHANGELOG lines | 38,513 |
| blocks parsed | **378** (ROUND 312, RECORDS 63, SECTION 3) |
| ROUND blocks dated by header / git blame / undated | 15 / 297 / 0 |
| ROUND blocks with no number of their own (date-rule fallback) | 16 |
| code spans scanned (fences skipped) | 24,067 (39,529 tokens) |
| id-shaped code spans (one bare word) / of which a ledger row id | 7,417 / **1,132** |
| ledger rows / non-terminal (`open`, `in work`, `held`) | 1,261 / 1,074 |
| (ROUND block, row) pairs / distinct rows | **649** / 458 (header 99, body only 550) |
| ROUND blocks naming at least one row | 146 of 312 (the est-era blocks predate the ledger) |
| pairs whose row is non-terminal | **493** (open 395, held 60, in work 38) |
| pairs in RECORDS blocks (not checked) | 222 |
| rows named only inside an artifact path (not counted) | 31 pairs |

## Census at HEAD

Each pair is a non-terminal row named in a ROUND block with no write-back.  All of them are
ARCHIVED under the proposed cutoff (none landed after 2026-11-05).  Every context was read
(`triage_read.txt`, `triage_filed.txt`, `triage_recorded.txt`; 315 pairs).

| rule | scope | in-scope pairs | hits | (i) genuine ghost | (ii-a) filed by this round | (ii-b) round already named on the row | (ii-c) referenced only | (iii) parse noise |
|---|---|---|---|---|---|---|---|---|
| date (the row's wording) | all | 493 | **268** | 0 | 84 | 55 | 129 | 0 |
| mention | all | 493 | **184** | 0 | 23 | -- | 161 | 0 |
| date | subject | 78 | 7 | 0 | 0 | 2 | 5 | 0 |
| **mention (DEFAULT)** | **subject** | **78** | **13** | **0** | 0 | 0 | **13** | 0 |

**How each class was told:**
* (ii-a) the row was opened on or after the round's date.  The text says "filed `x`",
  "**Filed** (... all LOW)", or "filed from this round".
* (ii-b) the row's record names the round ("Filed by #583 ...", "[#584, 2026-11-05: ... LANDED
  ...]") but has no entry dated after it.  Only the date rule flags these.
* (ii-c) the sentence names the row as a sibling, a carrier, or an earlier filing ("stays its
  own row", "Filed, not fixed: ...", "Tracked as `arcbiosubsan`, not fixed here", "is adjacent
  and not folded in").
* (i) none: no context reads as "this round shipped the row's fix".  This was cross-checked
  independently: of the 41 non-terminal rows that a landing commit names in its subject
  (`#NNN <row>: ...`), 40 name their round in their record.  The 41st, `arcbiosubsan`, has
  post-ship entries and a re-open note.
* (iii) none among hits.  6,285 of 7,417 id-shaped spans match no row, and so cannot be hits.

Hits by landing date: date/all 253 after 2026-08-29, 132 after 09-30, 42 after 10-31.
Mention/all: 153, 36, 7.  Default: 10, 1, 0.

## Forward replay: what the checker would have said on each landing commit

`replay.py` takes every ROUND block since the ledger entered git (2026-08-17).  For each one it
finds the commit that added the block (git blame) and reads that commit's own CHANGELOG and
ledger.  That is what a pre-commit run on the landing would have seen.  141 landing commits,
161 blocks, 588 pairs, **0 skipped**.

| variant | landings failed (of 141) | Aug (54) | Sep (55) | Oct (22) | Nov (10) | hits | documented ghosts caught (of 11) |
|---|---|---|---|---|---|---|---|
| date, every named row (the row's wording) | 84 | 22 | 31 | 21 | **10** | 328 | **2** |
| mention, every named row | 76 | 25 | 34 | 14 | 3 | 213 | 11 |
| mention, rows opened on/after the round exempt | 71 | 21 | 33 | 14 | 3 | 199 | 10 |
| mention, `in work` rows only | 14 | 6 | 6 | 2 | 0 | 25 | 10 |
| mention, header-named rows only | 11 | 1 | 10 | 0 | 0 | 12 | 6 |
| **mention, header-named or `in work` (DEFAULT)** | **20** | 6 | 12 | **2** | **0** | 31 | **11** |

**The 11 documented ghosts**: rows where a later record states the gap in words.  They come
from 7 rounds; `writeback_delay.tsv` gives the delays and `replay_class.tsv` the evidence.

| round | rows | days unrecorded | the record that found it |
|---|---|---|---|
| `#479` | `wdcwipclear`, `wdcringnoflush`, `wdcstalephase` | 2 | this row: a nine-seat panel re-briefed shipped work |
| `#484` | `wdcringambig`, `wdcaddtoinbufbound` | 3 | `f42d747d` "#484 closed ONE of the two rows it claims" |
| `#496` | `gdromcondlies` | 1 | `66c5855e` "a HIGH row was advertising a critical bug that had already been fixed" |
| `#505` | `sgirergbroundtrip` | 1 | its note: "FIXED BY `#505` AND THE ROW WAS LEFT OPEN" |
| `#526`, `#527`, `#528` | `xscaleinten`, `ppcrlwimiwidth`, `ppcrldimimask`, `mapledmaaddr` | **36** | three Records blocks of 2026-10-18: "finished on 2026-09-12 and was never moved out of `in work`" |

The default also flags 6 more rows at landing whose write-back came later: 5 the same day
(`stagetokens`, `sgimtelabelcells`, `pcc2c040ctlq`, `pcc2genctlc040alias`, `sgirandompixel`),
and `sgirekills` after 40 days with only a sha.

**Why a sha in `commits` is not accepted** (opt-in `--accept-commits`): `#526`-`#528`'s same-day
follow-up wrote only the landing sha into `commits`, and the rows then sat `in work` for 36
days.  At `2951694f` (2026-10-17) the default names all four.  With the flag they go silent
(control 7).  The flag rescues no pair at HEAD under the default scope, and inside a landing
commit it can never apply.

## The prototype: `check_ghost_rounds.py`

* **Existence-only.**  A named row in scope must be `closed`/`dropped`, or its record must name
  the round.  "Its record" means state_note, hold, hold_question, closure, witness, commits,
  note, or an entry dated on/after the round.  It checks that the write-back exists, never what
  it says.
* **Forward-only.**  `CUTOFF = 2026-11-05`.  Blocks that landed on or before it are reported as
  ARCHIVED (`--list`); later ones FAIL.  A block not yet committed lands today.  Dating follows
  `check_bugfile_sync.py` / `HOLDQ_CUTOFF`; ledger reading follows `check_stage_panels.py`
  (`GXLEDGER`/`GXCHANGELOG` overrides, so controls run on copies, and the run prints what it read).
* **VOID, never PASS, on a null medium.**  No ROUND block, no ledger row, or no (block, row)
  pair: exit 2, `GHOST_ROUNDS_VOID`.
* `--at=REV` replays any commit read-only from git.  `--rule=date` and `--scope=all` reproduce
  the literal reading.  Runtime is about 1.3 s, most of it `git blame CHANGELOG.md`.
* **Usable inside the landing commit.**  The landing commit knows its round number, never its
  own sha.  Current practice already writes back there (`#583`/`#584`: subjects closed, filings
  carry "#583").

**What it does not catch**, stated so a green run is not over-read:
1. An `open`/`held` row a round shipped on and named only in the body.  There, a filing and a
   reference look alike.  This is the price of 2 failures in 32 instead of 17 in 32.
2. An incidental mention.  Any `#NNN` on the row counts.  `pitclobber` carried "#440 pass 2"
   while its note says `#439` fixed it.
3. Rounds with no CHANGELOG block.  The 2026-09-17 RECORDS block lists seven (`#436`,
   `#439`, `#441`, `#443`, `#466`, `#487`, `#493`); `#470` and `#471` (`180afaa3`,
   `0a7c4687`) have none either.  `probewiringscope` says "FIXED AS #471" and is still
   `in work`; that is a stale *state*, which an existence check does not judge.
4. RECORDS blocks, and the 16 unnumbered round blocks.  The unnumbered ones fall back to the
   date rule, which is blind at day granularity.
5. It reads the working tree, like its siblings.  In a shared tree, a peer session's
   uncommitted round block is checked too.  Editing an old block's *header* line moves its
   blame date past the cutoff; body edits do not.

## Controls: 35 of 35 ok (`controls/run_controls.sh`, `controls/run_controls.out`, `controls/out/`)

| # | control | expected | got |
|---|---|---|---|
| 1 | synthetic round naming an open row with no write-back (`c1a`) | FAIL | FAIL (both rules) |
| 1b/1c | same-day pre-ship entry; `#479` shape (body-named, `in work`) | FAIL | FAIL under mention, **PASS under date: the blindness, reproduced** |
| 2 | the same block naming a properly closed row (`c2a`) | PASS | PASS (both rules) |
| 2b/2c | row left open that names the round; body-only reference | PASS | PASS (date rule FAILs 2b; `--scope=all` FAILs 2c) |
| 3 | null: empty CHANGELOG | VOID, "0 blocks parsed" | VOID, exit 2, no PASS line |
| 3b/3c | empty ledger; RECORDS-only CHANGELOG | VOID | VOID |
| 4 | `--at=d9efd339` (before the write-back) | the three `#479` rows | named under mention, **absent under date**; gone at `4cc3952a` |
| 5 | `--at=2632277f`, cutoff 2026-11-05 | PASS | PASS, 13 archived (184 / 268 under the literal readings) |
| 6 | scratch git repo, an uncommitted round block | lands today | FAIL; PASS once the row names `#903` |
| 7 | `--at=2951694f`, the 36-day window | the four `#526`-`#528` rows | named; silent with `--accept-commits` |

## False positives the default would raise

* **At HEAD: 13, all archived.**  Each is an `in work` row named in a later round's body:
  * `gdromacceptdmanum` (#557)
  * `wiringcliff` (#530, #535, #550)
  * `alphavmkill`, `lcabadval`, `lcairqstubkill`, `lcaisaphys` (#538)
  * `lcairqstubkill` (#515)
  * `pcc2genctlc040alias` (#532)
  * `gdromwarnbits` (#462, #489)
  * `probewiringscope` (#467)
* **In the replay: 14 hits at 7 landing commits, all references or one filing:**
  * #558: `mapledmaaddr`, `ppcrldimimask`, `xscaleinten`
  * #557: `gdromacceptdmanum`
  * #550: `wiringcliff`
  * #538: `lcabadval`, `lcairqstubkill`
  * #532: `ip30abortkill`, `lcaisalane`, `pcc2genctlc040alias`
  * #527: `ppcwitnessmaskoracle`
  * #489: `gdromwarnbits`
  * #440: `pitclobber`
  * #467: `loadfragile` (a filing)
* **Remedy, the same each time:** one bracketed line naming the round on the referenced row
  (e.g. `[#558, <date>: audited, nothing owed]`), or closing the row.
* **The literal readings' false positives:** the 268 / 184 pairs in `census_hits.tsv`.  These
  are filings (84 / 23), rows that already name the round (55 / --), and references (129 / 161).

## Proposed cutoff

**2026-11-05** (the census date at `2632277f`), compared as *landed after the cutoff fails*.
None of the 13 archived hits fails, and the first round to land from 2026-11-06 on is checked.
If the owner wires it later, use the wiring date.

| cutoff | default hits that would FAIL at HEAD |
|---|---|
| 2026-08-29 (the date this row was filed) | 10, all references |
| 2026-09-30 | 1 |
| 2026-11-05 (proposed) | 0 |

## Proposed wiring, if the answer is not "not at all"

Section **`P2`**, beside P's ledger/bugfile sync.  Every letter A-Z is taken.  `soft` for a soft
section, `bad` for a hard one:

```sh
say ""; say "P2. a round block's subject and in-work rows record the round (ghostround)"
GHOSTCHK=$_HERE/pipeline/check_ghost_rounds.py
if [ ! -f "$GHOSTCHK" ]; then
	warn "check_ghost_rounds.py MISSING -- ghost rounds NOT verified"
elif out=$(python "$GHOSTCHK" 2>&1); then
	good "$(printf '%s' "$out" | grep -E 'GHOST_ROUNDS_PASS' | tr '\n' ' ')"
else
	soft "A ROUND SHIPPED WITHOUT RECORDING ITSELF ON ITS ROWS:"   # or: bad
	printf '%s\n' "$out" | grep -E 'GHOST_ROUNDS_(FAIL|VOID)|^  GHOST' | sed 's/^/          /'
fi
```

Exit 2 (VOID) takes the else branch, so a null run never prints `ok`.  Wiring a hard section
owes the same two negative controls in place (an unrecorded round reds; a closed row does not);
controls 1 and 2 are those, run here on copies.

## The owner's question

**Wire `check_ghost_rounds.py` (default: a round block's header-named and `in work` rows must
be closed or name the round; cutoff 2026-11-05) into precommit_check.sh as a soft section, a
hard section, or not at all?**

## Files (all in `_scratchpad/wghost/`, the scratch original -- this durable copy holds only this file and the six the banner names; see `PROVENANCE.md`)

* `check_ghost_rounds.py`: the prototype.
* `census.py` / `census.out` / `census_hits.tsv`, and `triage.py` with its three `triage_*.txt`
  reading files.
* `replay.py` / `replay.out` / `replay_hits.tsv`, `replay_class.py` / `replay_class.out` /
  `replay_class.tsv`, and `writeback_delay.py` / `writeback_delay.out` / `writeback_delay.tsv`.
* `controls/`.
* HEAD snapshots: `CHANGELOG_HEAD.md`, `ledger_HEAD.json`, `blame_HEAD.porcelain`,
  `gitlog_HEAD.tsv`, `HEAD_SHA.txt`.
* Parsing surveys: `survey_*.py`, `survey_blocks.out`.
* Reference copies of the two sibling checkers and the precommit script: `ref_*`.

One slip, repaired: a mistyped path wrote three copies of historical `ledger.json` blobs to
`C:\Program Files\Git\` (`/tmp_ledger_*.json`).  They were deleted at once, and an `ls`
confirmed they were gone.
