# r2measure — method, apparatus, and the two things that nearly went wrong

Written before the table's results, so the apparatus is described independently of what
it went on to measure.

## What is being measured

`dev_dreamcast_gdrom.c`'s `handle_command()` had two `fatal()` + `exit(1)` sites reachable
by an ordinary guest store:

* **Site A** — `case 0x30`, an unimplemented data format (now latched on `GDROM_W_FMT`)
* **Site B** — `default:`, an unimplemented command byte (now latched on `GDROM_W_CMD`)

Both now decline, announce once per device instance, and `break` to the common tail. The
detector under test is `regress/gdrom_decline_probe.py`, **20 rows**.

**The claim being tested is not that the probe passes. It is that the probe DETECTS.** A
row is discharged by a measured kill, never by existing.

## The baseline, named rather than assumed

`dev_dreamcast_gdrom.c` md5 **`85846dc966d00efe511d2b5755364490`** — the round's post-fix
working set, which is UNCOMMITTED. It was verified against **five** independent witnesses
before a single mutant was applied:

| witness | md5 |
|---|---|
| live `GXEMUL-SEC/src/devices/dev_dreamcast_gdrom.c` | `85846dc9…` |
| `build/src/devices/dev_dreamcast_gdrom.c` | `85846dc9…` |
| `est/src/devices/dev_dreamcast_gdrom.c` | `85846dc9…` |
| the scratch clone `/tmp/gxr2m/…` (taken 04:45) | `85846dc9…` |
| `git show 'stash@{0}:src/devices/dev_dreamcast_gdrom.c'` (04:54 window) | `85846dc9…` |

Instrument: `pinned/gdrom_decline_probe.py.FROZEN`, md5
`188e92ebd8f9593664c294c63fed0d98`, 443 lines, 20 rows.

## *** THE THING THAT NEARLY INVALIDATED THE WHOLE TABLE ***

**At 04:54:01 a CONCURRENT session ran `git stash` on `GXEMUL-SEC`.** For ~85 seconds the
working tree's copy of `dev_dreamcast_gdrom.c` was the **PRE-FIX** file (58553 bytes, byte-
identical to `HEAD`), and `regress/gdrom_decline_probe.py` **did not exist on disk at all**.
The stash was popped at 04:55:25, after an unrelated roster commit (`55ef9db`) landed.

The standing rule is *restore from SEC, never from your own backup* — and its stated reason
is that a crashed run's backup can capture a mutant. **That rule silently assumes SEC is
stable.** Here it was not.

The concrete hazard, and it is specific rather than theoretical: `mut.py` asserts a unique
anchor and refuses on a miss, so nine of the eleven mutants would have died loudly against a
pre-fix file. **`M_growA` anchors on `d->cmd[1] != 0x20`, which exists in BOTH the pre- and
post-fix file** — it would have applied *silently* to the wrong baseline, and its row would
have been scored against a binary with no fix in it.

**Remedy: the baseline and the instrument were PINNED** into `pinned/`, read-only, verified
against the five witnesses above, and every restore in the table is from the pin. The pin's
purpose is the same as the rule's — never restore from something that might hold a mutant —
achieved by verification rather than by trusting a tree another process is editing.

*This is a genuinely new failure mode for this harness: the sentinel discipline protects
against **my** mutations of a build tree. It says nothing about **someone else's** mutations
of the reference tree the restore reads from.*

## Apparatus discipline

* **Build and measure are decoupled.** All mutant binaries are built first and copied out;
  the clone is then restored, rebuilt and its sentinel cleared. The probe runs never race a
  compiler — the probe's oracles are fixed wall-clock windows (`settle=8.0`, `spin=2.0`,
  0.35 s per debugger command), so a concurrent build is a load-sensitive oracle.
* **Runs are strictly serial**, for the same reason.
* **One instrument for the whole comparison.** Python reads its script at startup, so a
  running invocation is immune to an edit but the *next* one loads whatever the file says
  then. Every run in the table uses the pinned copy, and `base` is **re-run** with it so the
  baseline and the mutants share one instrument rather than two. (`probe_base_run1_prestash_instrument.log`
  is the earlier 04:46 baseline run, taken with the on-disk instrument before the stash
  window; it is kept as corroboration, not as a table row.)
* **`[ binary -nt source ]` is checked per build**, because `MAKE_RC` has been observed
  reporting 0 on a failed build.
* **Every binary's md5 is recorded and checked for distinctness** — a mutant whose binary
  matches the baseline did not take effect.
* **A log is preserved only if it carries `R2MEASURE_DONE`.** A copy taken from a still-
  running job preserves a truncation that looks complete.
* **Every mutant was dry-run against a throwaway copy first** and shown to change the file;
  `mut.py` refuses on a missing or ambiguous anchor, so MUTANT-TEXT-NOT-FOUND is a hard
  failure rather than a silent no-op.

## Floor clause (b): "VERBATIM" was checked, not asserted

The reinstated text was diffed against `git show HEAD:src/devices/dev_dreamcast_gdrom.c`:

* **`M0_exitA` — byte-identical**, including the `\n` in the format string and the tab
  indentation.
* **`M1_exitB` — statements byte-identical**, with one recorded difference: upstream writes
  `default:fatal("GDROM handle_command: …"` on ONE line, and the mutant keeps `default:`
  attached to the `#490` comment block with the `fatal(` on the following line. Behaviour
  is identical; the label's line placement is not.

## Two apparatus errors of my own, recorded because they are the class this file is about

1. A `bash -c 'ART=…; cp … $ART/…'` chain expanded `$ART` **empty**, and the first preserved
   log landed in the WSL filesystem root instead of the artifacts dir. Caught by reading the
   `echo` output (`preserved -> /probe_base_…`) rather than by any check. Everything that
   matters now goes through script files.
2. A gate-vs-probe row-list checker used `for v in ((?:.|\n)*?); do`, which spanned from an
   **earlier section's** `for v in` to this section's `count "$DECLLOG"` and reported **146
   names for a 20-name list**. The absurd count was the tell — a denominator caught it. The
   scoped rewrite reports the real answer: 20 names, exact ordered match with the probe,
   correct `$DECLLOG` variable, denominator literal 20 agrees, longest name 10 chars
   (limit 13), no prefix collisions.

## The stash recurred — this was not a one-off race

At **05:06**, minutes after the build phase finished and while the measure phase was
starting, `git stash list` showed a **second** hold:

```
stash@{0}: On main: #490 in flight (2nd hold)
```

`GXEMUL-SEC/src/devices/dev_dreamcast_gdrom.c` was `a1bd4373…` (pre-fix) again. The build
phase's own cross-check had already printed it:

```
=== RESTORE from the pinned baseline, verified by cmp ===
RESTORE cmp vs pin: CLEAN
cross-check vs LIVE SEC: DIFFERS RIGHT NOW (concurrent session mid-edit)
```

So the fix under measurement is stashed and unstashed repeatedly by a concurrent session
throughout this table's run. **Every number in this directory was produced against the
pinned baseline and the pinned instrument, never against the live tree**, which is the only
reason the table is coherent at all.

Two further guards were added once the recurrence was seen:

* the pinned baseline and instrument were copied **outside `GXEMUL-SEC`** — to
  `_scratchpad/r2m/pinned_backup/` and to `/tmp/r2m_pinned/` — because this artifacts
  directory is UNTRACKED (`?? regress/artifacts/gdromexitsix/r2measure_20260829/`) and a
  `git stash -u` or `git clean` would take it. md5s verified identical in all three places.
* the restore at the end of the build phase was verified at the **binary** level as well as
  the source level: rebuilding from the pin reproduced the baseline binary md5
  `8d473baa488b2aef3eabd3be569f2c9d` exactly.

## Build-tree state at 05:07 (observation, not a finding of this measurement)

| tree | md5 | |
|---|---|---|
| `GXEMUL-SEC` | `a1bd4373` | pre-fix — mid-stash |
| `build/` | `85846dc9` | carries the fix |
| `est/` | `85846dc9` | carries the fix |
| `build-asan/` | `a1bd4373` | **pre-fix — the fix has not been propagated here** |

No `.MUTANT` sentinel in `build/`, `est/`, `build-asan/`, or the scratch clone. The
`build-asan/` gap is the round's propagation obligation at commit time (the owner ruled on
2026-08-27 that `build-asan/` joins the propagation set for the files a commit changes); it
is recorded here because it was observed, not because this table depends on it.
