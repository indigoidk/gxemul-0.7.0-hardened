# Predicted kill table — written BEFORE the measure phase ran

**Written 2026-08-29 ~05:0x, before `measure.sh` was launched. Its mtime is the order
proof.** These are derived by reading the fix and the probe, not by running anything. They
are recorded so that a measurement which *disagrees* is visible as a surprise to be
investigated, rather than being quietly absorbed as "what I expected".

Baseline: `dev_dreamcast_gdrom.c` md5 `85846dc966d00efe511d2b5755364490` — the round's
post-fix working set, verified against live SEC, `build/`, `est/`, the scratch clone and
the (since-popped) stash blob.

Probe: `pinned/gdrom_decline_probe.py.FROZEN` md5 `188e92ebd8f9593664c294c63fed0d98`,
443 lines, 20 rows.

| mutant | what it edits | predicted rows to REDDEN | predicted score |
|---|---|---|---|
| `Ma_toclen` | Site A latch bit -> `GDROM_W_TOCLEN` | `crossbit` | 19/20 |
| `Mb_toclen` | Site B latch bit -> `GDROM_W_TOCLEN` | `crossbit` | 19/20 |
| `M_braceA` | Site A `break` moved INSIDE the latch `if` | `latch cond` | 19/20 |
| `M0_exitA` | floor (b): Site A `exit(1)` reinstated verbatim | `fmt surv`, `fmt says`, `fmt x2`, `fmt cnt`, `fmt event`, `both sites`, `crossbit` | 13/20 |
| `M1_exitB` | floor (b): Site B `exit(1)` reinstated verbatim | `unk surv`, `unk says`, `unk x2`, `unk cnt`, `unk event`, `both sites`, `crossbit` | 13/20 |
| `Md_nolatchA` | clause (d): Site A latch tested, never set | `fmt x2` | 19/20 |
| `Md_nolatchB` | clause (d): Site B latch tested, never set | `unk x2` | 19/20 |
| `M_growA` | `!= 0x20` -> `!= 0x21` (accept-set growth) | `fmt says`, `fmt x2`, `latch cond`, `both sites`, `crossbit`, `acceptA`, `accept sil` | 13/20 |
| `Md_hoistannounce` | the announce hoisted to the head of `case 0x30` | `fmt 0x24`, `accept sil` — and **`acceptA` GREEN** | 18/20 |
| `M_retA` | Site A `break;` -> `return;` | `fmt cnt`, `fmt event` | 18/20 |
| `M_retB` | Site B `break;` -> `return;` | `unk cnt`, `unk event` | 18/20 |

## The two predictions that are actually load-bearing

1. **`latch cond` must redden under `M_braceA`, and nothing else in the probe reads `REJ`.**
   `REJ` is the one channel in this probe that is never asserted with a NON-ZERO wanted
   value anywhere. `latch cond` wants `0`, which is also what a regex that matches nothing
   returns. So until `M_braceA` reddens it, the row is *indistinguishable from a dead
   regex*. This mutant is the row's entire liveness proof.

2. **`accept sil` must redden under `Md_hoistannounce` while `acceptA` stays GREEN.**
   `M_growA` reddens both, which shows only that `accept sil` is failable — not that it
   discriminates anything its neighbour does not. The hoist is the case where the legal
   command still reaches the `Huh?` guard (so `acceptA` is satisfied) while the decline
   text nevertheless appears on the accepted path (so `accept sil` must fail). If
   `acceptA` also reddens here, `accept sil` has no measured independent value.
