# Round 2's measured mutant table — and WHICH OF THESE LOGS IS COMPLETE

Produced by the opus (measuring) seat in `/tmp/gxopus_r2`: a `cp -a` clone of `build/`,
`cmp`-clean against SEC before mutant 1, baseline rebuilt in-clone with
`[ binary -nt source ]` checked, and a `.MUTANT` sentinel in every mutant tree. It wrote
nothing into `GXEMUL-SEC/`, `est/`, `build/` or `build-asan/`, and `build/` still passed the
two-part clearance afterwards.

## *** SENTINEL AUDIT — RUN BEFORE CITING ANY NUMBER BELOW ***

A preserved log is verified by its COMPLETION SENTINEL, not by its existence.

| log | bytes | last line | complete? |
|---|---|---|---|
| `t_base.txt` | 432 | `TPROBE_DONE` | **YES** |
| `t_fixed.txt` | 432 | `TPROBE_DONE` | **YES** |
| `t2_fixed.txt` | 813 | `TPROBE2_DONE` | **YES** |
| `table2_targeted.txt` | 1529 | `TARGETED_DONE` | **YES** |
| `t2_M1ret.txt` | 600 | mid-row, `S2 fmt x2 …` | **NO — TRUNCATED** |
| `table1_full_M1ret.txt` | 740 | `===== M2nolatch =====` | **NO — TRUNCATED** |

**The two truncated logs are truncated AT SOURCE, not by the copy.** Verified by comparing
byte counts against the seat's own scratchpad: 600 and 740 in both places. The seat stopped
measuring deliberately when the main loop began its own probe run, because its sessions carry
wall-clock budgets and a contended run is a discarded run.

### What that does and does not cost — stated precisely, because this is the round's headline

`M1ret` (`break;` → `return;` at Site B) is the round's central finding, and it is
**MEASURED AND INTACT** for the claim that matters. The rows that carry it are present in
`t2_M1ret.txt`:

    S1 unkcmd    alive=True  death=exit0  COND=0xa0  CNT=0x98  EVT32=0x1  unk=1
    S2 unk x2    alive=True  death=exit0  COND=0xa0  CNT=0x98  EVT32=0x1  unk=1

against the same sessions on the fixed tree, where `CNT=0x0`. **So "only CNT moves, and it
moves" is measured.**

**What is NOT measured is the COMPLETENESS half.** `S3 both` and `S4 acceptA` were never run
under `M1ret`, so the statement "it escapes all 58 rows" rests on a partial run for two of
eight sessions. Nothing observed contradicts it, and the two missing sessions exercise the
*other* site — but the honest form is:

> `M1ret` moves `CNT` and nothing else **in the six sessions that ran**. The two unrun
> sessions are Site A's, and re-running them costs about one minute.

That distinction is exactly the one this project keeps having to make between a measurement
and a summary of one, so it is written here rather than left to a reader who sees six rows
and a missing sentinel.

## The completed table

| mutant | killed by | escapes |
|---|---|---|
| **M1ret** `break;`→`return;` (Site B) | **nothing planned** — only `CNT` 0x0→0x98 | death-mode (`exit0`), latch (`unk=1`), the 0x70 row, all 58 |
| **M2nolatch** latch tested, never set | same bad command **twice** (`unk=2`) | both-sites session; any one-decline row |
| **M3shared** both sites share one warn bit | **both sites in one session** (`fmt` 1→0) | same-command-twice session |
| **M4nobreakA** Site A announces, no `break` | bad format + **valid** sector count (`rej` 0→1) | everything planned, all 58 |
| **M5outerA** Site A `break` hoisted out of the `else if` | **the accept row only** (`huh` 1→0) | the format-decline row entirely |
| **M6cond** tail guard `data`→`data_len` | **nobody — EQUIVALENT** | everything |

**M2nolatch and M3shared are ORTHOGONAL, measured**: neither session substitutes for the
other, so a single "the latch fires once" row catches exactly one of them.

**M5outerA is the sharpest de-escalation case on record here**: the mutant that breaks the
whole `case 0x30` accept path is invisible to a row aimed at the format decline, and visible
only to a row that *completes* a `0x30` — which **no session in the 58-row probe does**.

**M6cond measuring EQUIVALENT** is a result, not a gap: it corroborates X1 (post-`#465`,
`data` and `data_len` agree in every guest-reachable state) from a second direction. It is the
TAIL site, not `M11`'s DMA-arm site, so it does not settle the `M11` kill claim by itself.

## Still owed

**X1 remains DERIVED, not MEASURED.** The claim is that `#465`'s `free_data(d)` prologue —
which sets both `d->data = NULL` and `d->data_len = 0` — makes the "data NULL, data_len stale"
state unconstructible, so the probe comment asserting it is a wrong record and the contract's
`M11` operand-swap kill claim has EXPIRED. Three source facts are verified by reading
(`free_data` clears both; it is the prologue; the comment claims otherwise). The seat built the
real `M11` mutant and a replicating session and **deliberately did not run it** to avoid
contending. Its runner is preserved beside these logs; it takes about four minutes alone.

*An absence record is time-indexed, and this is that rule applied to a KILL record: the warrant
was edited by `#465`, so the death measurement must be re-run rather than inherited.*
