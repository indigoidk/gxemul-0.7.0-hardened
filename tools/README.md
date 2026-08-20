# `tools/` — the harness that gates this repository

Moved here 2026-08-17 by owner decision. Until then it lived at the project root, **outside
version control**, and on the day of the move it had gained two hard gates, a corrected causal
record and the derived-brief mechanism in a single session. An outage would have lost all of it.

## What is here

| file | what it does |
|---|---|
| `precommit_check.sh` | the pre-commit gate. Sections A–L. The later ones are not redundant with each other and each was built after a specific failure: **G** verifies a seat that ANSWERED was recorded; **H** verifies the seat was FIRED at all; **I** verifies that work which is OWED is written down (H reads a HELD marker as "waiting", and waiting is indistinguishable from forgotten); **I2** verifies the queue's own SUMMARY of those markers is current (it said "nineteen held stages" when the ledger held **thirty-four**); **J** hard-fails on carrier-copy divergence; **K** enforces the witness ladder; **L** asks whether the ledger noticed the code that shipped. |
| `install_hooks.sh` | installs `precommit_check.sh` as a REAL git pre-commit hook. **Built after the gate was bypassed twice in one day, by two mechanisms that both looked careful:** `precommit_check.sh \| tail -3 && git commit` (a pipeline's exit status is the LAST command's) and `... \| grep -E "FAIL" && git commit` (grep SUCCEEDS when it FINDS failures, so the `&&` fired precisely because the gate was red). An advisory check is a check that eventually is not respected. `git commit --no-verify` remains the escape hatch, deliberately loud. |
| `nightly_battery.sh` | runs the full 16-gate battery unattended and writes a stamped verdict. Invoked by the Windows scheduled task `GXemul-weekly-battery`, Sundays 18:00. |
| `nightly_check.sh` | the dead-man switch. Every threshold in the battery lives *inside* the run, so none of them can observe the run not happening. This asks the one question the battery cannot ask about itself. |
| `panel.sh` | convenes the seven scriptable review seats concurrently, verifies each produced a real answer, and persists that verdict to `$OUT/SEATS.txt` with a `PANEL_COMPLETE` sentinel. |
| `adjudicate.sh` | fires the three packet-fed seats at ONE seat's finding and asks them to refute it. |
| `panel_ollama.py` | the packet-fed seat helper. |
| `pipeline/ledger.json` | **the source of truth** for the review record. 74 rows × 9 seats × 4 phases. |
| `pipeline/gen_dashboard.py` | renders the ledger. Refuses to run if an entry names a seat no column declares — 59 entries once rendered nowhere because they were keyed `opus` against a column called `opus5`. |
| `pipeline/check_seat_coverage.py` | **reports** per-seat coverage: for each seat, how many of its on-disk answers are recorded, how many sit in dirs that predate the ledger, and how many are a real GAP. Not a second gate -- section G already fails on a gap. It exists because "is deepseek missing?" was asked FIVE times, and the first bespoke audit answered it WRONG: it reported "82 answers, 17 recorded, 65 unrecorded" when the 65 sat in dirs no entry cites at all, where no seat of any kind is recorded. Confusing "the ledger did not exist yet" with "this seat's review was lost" is the failure this tool prevents. Run `check_seat_coverage.py deepseek` for the per-file listing. |
| `pipeline/check_seats_read.py` | fails if a seat answered in a cited panel and was never recorded. Keyed on the **file**, not the seat: one seat with two answers in a directory was fully vouched for by citing either. |
| `pipeline/check_stage_panels.py` | fails if a post-cutoff stage moved on without all nine seats. Distinguishes complete / grandfathered / filed / **HELD** — and a HELD stage on a *closed* row is a hard violation, so the marker cannot be used to walk away from a gap. |
| `pipeline/fable_queue.md` | work that requires the flagship seat, held when its quota is short. A queued job is not a done job. |
| `pipeline/check_commit_attribution.py` | asks whether the LEDGER noticed the work that SHIPPED. On its first run, 33 of the 40 most recent commits were named by no row -- most legitimately, two sharply: a commit whose subject read "selfmutant6 CLOSED" against a row still marked held, and a row whose `commits` field named an unrelated device round. **Reports BOTH its own blindnesses on every run** -- row ids too short to match safely, and rows carrying commits that no subject ever names -- because a check that silently skips a third of its subjects while printing a green line is this project's newest named vacuity class. |
| `pipeline/census_floods.py` | inventories `fatal()` calls and latch idioms across `src/devices/`. Built after TWO rows -- `rtcflood` and `wdcflood` -- were filed separately and turned out to be one class: **84 files, 776 calls, 72 files with no latch idiom at all.** Ships as an INSTRUMENT, not a number, for the same reason `census_exits.py` did. It prints its own limits every run: the latch column is per FILE, not per PATH, and it does NO reachability analysis, so its numbers are bounds and never defect counts. |
| `pipeline/gen_codex_wall.py` | DERIVES the queue's held-stage section from the ledger's `[HELD AWAITING SEAT: ...]` markers. Built after that list was maintained by hand through six panels in one evening and drifted -- "nineteen" against a real thirty-four. The prose stays human because it is judgement; only the row list and the count are generated. `--check` is wired as precommit **I2**. |

`pipeline/dashboard.html` is **generated** and gitignored. Write the ledger, regenerate,
republish; never hand-edit the rendering.

## Paths

Every script derives the project root from its own location (`tools` → `GXEMUL-SEC` → project),
with `$GXROOT` overriding for tests. They used to hardcode one machine's absolute path, which is
only half-tracked — a fresh clone anywhere else would run against whatever happened to be at the
old address, or nothing.

**The migration got this wrong once, and the dead-man switch caught itself.** The old two-line
form was `ROOT=${ROOT:-/abs}` followed by `[ -d "$ROOT" ] || ROOT=/mnt/abs`; rewriting only the
second path left `[ -d "$ROOT" ] ||` dangling, which swallowed the new assignment as its
right-hand side. `ROOT` resolved **empty**, `nightly_check.sh` looked for verdicts in
`/_scratchpad/nightly`, and it reported `NIGHTLY_CHECK_FAIL` rather than passing quietly. It now
carries an explicit guard that refuses to run on an unresolvable root.

## The scheduled task

`GXemul-weekly-battery` was repointed at `tools/nightly_battery.sh` in the same change and then
**triggered to prove it fires from the new path** — a scheduled task you cannot prove runs is the
exact failure this harness exists to catch. Its `LastRunTime` was `11/30/1999` for the whole of
its first week: it had never run, and nothing said so.

## Working rules these encode

- A non-answering seat is a **seat failure**, never agreement — and never silently.
- A blank cell, a seat failure, and an answer nobody read must never render the same.
- A crash is a **FAULT**, never a detection. `attempted = killed + survived + faults`.
- A green row that cannot fail is worth nothing; controls get controlled too.
- Settle disagreements by **measurement**, never by vote.
