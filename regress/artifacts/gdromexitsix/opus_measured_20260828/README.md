# Measurements the round CITES and neither kill table CONTAINS

These nine logs were produced by `#489`'s pass-2 measuring seat in its own scratch tree
(`/tmp/gxopus489`, a relocatable `cp -a` of `build/`). **It wrote into no project tree** and
left its scratch `cmp`-clean; the `build/.MUTANT` live at the time was the main loop's table 4.

## *** WHY THEY ARE HERE: `095aa96` CITES TWO OF THEM AND THEY LIVED ONLY IN `/tmp`. ***

The commit message states *"the measuring seat built that mutant: 12/19, and `zero surv` reads
exit0"*, and `OUTSTANDING_BUGS.md`'s `gdromlatchreuse` row states 19/19. **Neither number
appears in any of the five kill tables** — they are facts the tables do not cover, measured by
a different seat on a different tree.

So a COMMITTED record cited evidence in a rotating directory. That is the volatile-path class
this project has now paid for three times, and twice already today: `gdromexitsix`'s own
`probe:` field once cited two scratchpad scripts a `find` cannot locate, and `landiskaux`'s
census sat untracked while a round leaned on it.

**The seat caught it by OFFERING the logs rather than assuming they had been kept.** Nothing in
the harness would have flagged it: `check_cited_artifacts.py` enforces citations in a specific
form, and a number quoted in prose is not in that form.

## What each log establishes

| log | score | what it settles |
|---|---|---|
| `base_shipped.raw` | 15/15 | the 15-row detector, clean, reproducing the main loop's own base |
| `M8_breakinside_shipped.raw` | **15/15** | *** THE ESCAPE: `break;` moved one brace inward, into the announce block. First bad TOC declines; every one after it reaches `alloc_data()`. Fifteen rows, no reds. *** |
| `M8_breakinside_ext.raw` | 15/16 | the SAME mutant against a 16th row of the seat's own construction — `latch cond` = `0xa8` vs `0xa0`. **This pair is the measured warrant for the row the round shipped.** |
| `base_ext.raw` | 16/16 | that row is green on correct code, i.e. not a false-positive row |
| `M9_latchreuse.raw`, `c_M9_latchreuse.raw` | **19/19** | reusing `GDROM_W_LEN` instead of the new bit: **no row reds.** Filed as `gdromlatchreuse` |
| `M10_lt408.raw` | 15/15 | `< 408` against the 15-row set — closed mid-review by `over cond` |
| `c_base.raw` | 19/19 | the shipped 19-row detector, independently reproduced |
| `c_M0_delete.raw` | **12/19** | *** THE BARE DELETION, which NO kill table ran: `zero surv` reads `exit0`. The host SURVIVES writing 408 bytes past a `malloc(0)`. *** |

## The two that matter most, and why

**`c_M0_delete.raw` is the strongest evidence the round's central thesis has.** The maximal-
damage mutant — delete the guard outright — leaves the host alive, and **not one of the four
survival rows (`bad surv`, `zero surv`, `over surv`, `latch surv`) reds under it.** That is
"a survive-only row is vacuous at this site", measured at the extreme rather than argued.

**Its honest limit, stated by the seat that measured it:** it confirms the write does not
FAULT, not that the write is absent. **One ASan run would convert the claim from derived to
measured** — and `build-asan/` currently has no binary, which is the filed `asanunbuildable`
row. That is now a concrete reason to fix that tree rather than a tidiness argument.

**`M8_breakinside_shipped.raw` + `M8_breakinside_ext.raw` are a matched pair**, and the pair is
the point: 15/15 without the row, 15/16 with it, same mutant, same binary lineage. A single
log would show only that a row can go red; the pair shows the row is *why*.
