# #490 pass 2 ask-again — method and apparatus

Written before the results, so the apparatus is described independently of what it measured.
Predictions are in `PREDICTIONS.md`, whose mtime precedes every mutant log in this directory.

## Baseline, NAMED rather than assumed

The round's post-fix working set as pinned by the r2measure table:
`dev_dreamcast_gdrom.c` md5 **`85846dc966d00efe511d2b5755364490`**, taken from
`/tmp/r2m_pinned/dev_dreamcast_gdrom.c.BASELINE` and verified by md5 before mutant 1.

**The clone's source was FORCED to the pin rather than trusted.** A `cp -a` of `/tmp/gxr2m`
inherits whatever that tree held; the pin is the authority.

*** THE LIVE TREE MOVED DURING THIS REVIEW, WHICH IS WHY THE PIN MATTERS. ***
`GXEMUL-SEC/src/devices/dev_dreamcast_gdrom.c` was `85846dc9…` when this seat started and
`d3db9a02…` an hour later — a **comment-only** L4 correction landed by a concurrent pass-2
seat (an expired "MEASURED: this build dies there" claim at the `DEVICE_ACCESS` byte-store
site, which #490 made false). Verified comment-only by `diff`: one hunk, every line a `*`
continuation. **So the code these numbers describe is the code in the diff under review**,
and the delta is prose. This is the third concurrent-mutation event on this tree today; the
first two are recorded in `../r2measure_20260829/MAINLOOP_NEARMISS.md`.

## Build

Clone `/tmp/gxopus490p2`, binaries copied out to `/tmp/gxopus490p2_bins`. Build log
`/tmp/gxopus490p2_build_*.log`. Driver: `build490p2.sh` in this directory.

* **The clone rebuilt the baseline to binary md5 `8d473baa488b2aef3eabd3be569f2c9d` —
  byte for byte the r2measure table's own baseline binary.** That is the apparatus control
  that matters: an independent clone of the same pinned source compiles to the same binary,
  so any difference below is the mutant and not the tree.
* `[ binary -nt source ]` checked per build; all four reported `YES`.
* All three mutant binaries md5-DISTINCT from base — a mutant whose binary matches base did
  not take effect.
* `.MUTANT` sentinel dropped **before** mutant 1 and cleared only after `cmp` against the pin
  AND a rebuild that produced a fresh binary. The restore rebuild reproduced
  `8d473baa…` exactly.
* Mutator `mut490p2.py` asserts a UNIQUE anchor and exits non-zero on a miss or an ambiguity,
  so MUTANT-TEXT-NOT-FOUND is a hard failure rather than a silent no-op. Each mutant's `diff`
  against the pin is printed in the build log — one line each.

## Measure

* **Instrument frozen into my own copy**, `/tmp/gxopus490p2_probe.py`, md5
  `188e92ebd8f9593664c294c63fed0d98` — the same instrument the twelve-run table used, copied
  out of a directory another session writes to. A comparison run owes ONE instrument.
* Runs strictly **serial**; no compiler ran during any probe. The probe's oracles are fixed
  wall-clock windows (`settle=8.0`, `spin=2.0`), so a concurrent build is a load-sensitive
  oracle.
* Each log carries `PROBE_BIN_MD5`, `PROBE_INSTRUMENT_MD5`, start/end stamps and the
  completion sentinel **`P2ASK_DONE`**. A log is cited only if it carries the sentinel —
  a copy taken from a still-running job preserves a truncation that looks complete.
* Per-run apparatus control is `GDROM_DECL_CONTROL`, computed over the three identity rows
  alone.

## Scope of the escape claim

An escape is claimed against **`gdrom_decline_probe.py`'s 20 rows**. Whether the round is
blind overall additionally depends on the other gated GD-ROM probes, so that was checked by
reading rather than assumed:

| gated probe | rows | drives Site A (`cmd[1]=0x21`)? | drives Site B (`cmd[0]=0x31`)? |
|---|---|---|---|
| `gdrom_data_probe.py` | 23 | no | no |
| `gdrom_default_probe.py` | 60 | **no** — its two `0x21`/`0x31` hits are an opcode constant (`0x2122`) and a comment | no |
| `gdrom_toclen_probe.py` | 19 | no | no |
| `artifacts/gdrompionull/gdrom_pio_null_probe.py` | 13 | no | no |
| `gdrom_decline_probe.py` | **20** | yes | yes |

**So the 20 rows are the whole of the round's coverage of these two sites**, and an escape
there is an escape everywhere in the gated set.
