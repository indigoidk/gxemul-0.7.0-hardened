# #499 WIRING — the obligations `GATE_SNIPPET.sh` does not carry

Written by the coordinator, 2026-08-31, **not** by the measuring seat. Its snippet covers
`gate_arm.sh` correctly and completely; these are the *other* files a new probe touches, and
`grep -ciE 'EXPECT_PTY_PROBES|GRANDFATHERED|hygiene'` over `GATE_SNIPPET.sh` and
`REPIN_REQUIRED.md` returns **0** for both. That is not a criticism of the handoff — the seat
was asked for the detector and the gate block, and delivered both — it is the gap being closed
where the wiring happens rather than in someone's memory.

## 1. `regress/gate_hygiene.sh` — BOTH pins, IN THE SAME COMMIT

`regress/sgi_re_unmapped_probe.py` calls `pty.fork()` and has **no** `endswith(` prompt
predicate. Measured just now: `grep -c 'pty.fork'` = 1, `grep -c 'endswith('` = 0.

    EXPECT_PTY_PROBES            42 -> 43
    GRANDFATHERED_PROMPTLESS     add sgi_re_unmapped_probe.py   (16 -> 17 members)

**Re-derive, never transcribe** — the numbers above are true as of this file's writing and the
population moves whenever anyone adds a probe:

    find regress -name '*.py' ! -path '*/artifacts/*' | xargs grep -l pty.fork | wc -l

> ### *** WHY THIS IS IN A FILE AND NOT A NOTE TO SELF ***
>
> **This exact omission has already happened twice in one session**, both times mine. `#498`
> shipped `sgi_de_width_probe.py` — the 42nd pty-forking probe — *hours after* the same session
> raised this pin 37 -> 41 for precisely this reason, and did not add it to the grandfathered
> set either. Both halves were caught only because the **weekly battery of 2026-08-30 18:00 had
> already failed on the earlier instance** and its verdict sat unread for ten hours.
>
> **The feedback loop is the problem, not the care.** This check cannot fire until the weekly
> battery runs, so a mistake here surfaces up to SEVEN DAYS later — by which time the round that
> made it is closed and the person who made it is elsewhere. The denominator is the half that
> keeps going stale specifically because it is *the half no round has to touch to make its own
> probe pass*.

## 2. `check_probe_wiring.py` — the probe must be classified

A committed detector that no gate runs is a hard failure. Once the `gate_arm.sh` block from
`GATE_SNIPPET.sh` is in place the probe is gate-run and needs no MANIFEST entry as research —
but **verify it rather than assume it**:

    python tools/pipeline/check_probe_wiring.py     # expect PROBEWIRING_PASS

## 3. The `port/` artifacts themselves

The three python files here (`mkvariant499.py`, `patch_mk.py`, `patch_mk2.py`, `repin.py`) are
CLASS_RESEARCH evidence, not detectors, and each needs a MANIFEST line with the reason it is
kept — the same treatment the `killtable_20260831/` set already has.

## 4. Ordering, which is not optional

The oracle re-pin in `REPIN_REQUIRED.md` lands **before** the code edit, and the committed build
is measured RED under the new expectation first. `table3.out` already contains that proof
(`base` -> `got=exit1-txt want=exit0+txt FAIL`, `fix` -> `ok`), so the round inherits it rather
than re-deriving it — but the *edits* must still go in that order, or the record is false about
how it was done.

## 5. What this round must NOT do

Re-pin `tail_acc_x` in `sgi_de_width_probe.py` onto `"exit0"`. That belongs to `#500`, not this
round, and it is a trap: under a reinstated `exit(0)` the session announces once, dies, and the
row reads GREEN — total escape. See that probe's own comment block in `gate_arm.sh`.
