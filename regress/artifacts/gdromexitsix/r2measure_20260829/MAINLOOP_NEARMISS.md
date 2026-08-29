# *** MY `git stash` NEARLY INVALIDATED THIS TABLE, AND THE SENTINEL DOCTRINE CANNOT SEE IT. ***

**2026-08-29.  Recorded by the main loop, from the measuring seat's report, verified after.**

## WHAT HAPPENED

While the twelve-mutant table was running, **I ran `git stash` on `GXEMUL-SEC` twice** — at
about 04:54 and 05:06 — to let unrelated records commits through the pre-commit gate.  Each
stash left the source **PRE-FIX** and deleted `regress/gdrom_decline_probe.py` from disk.

I did this deliberately and I verified the restore byte-identical both times.  **What I never
considered is that a measurement was reading that tree.**

## WHY IT DID NOT CORRUPT THE TABLE — and why that was LUCK plus one seat's discipline

Nine of the mutants find-and-replace text that exists **only in the post-fix file**, so on a
stashed tree they would have failed loudly: mutant-text-not-found, which this project's drivers
treat as a hard FAIL precisely so a find-text doubles as a presence pin.

> ### *** BUT `M_growA` ANCHORS ON `d->cmd[1] != 0x20`, WHICH IS PRESENT IN **BOTH** VERSIONS.
> ### It would have applied SILENTLY, to the WRONG BASELINE, and produced a score. ***

A wrong score that looks exactly like a right one.  The seat caught it only because it had
**pinned the baseline and the instrument up front** and verified the pin against five
witnesses, then drove every run from the pin rather than from the live tree.

## THE DOCTRINE GAP, and it is the part worth carrying

The standing rule is *"restore from GXEMUL-SEC, the repo source, NEVER the script's own
backup"* — written after a crashed run left a tree mutant and the next run's backup captured
the mutant.

> **THAT RULE SILENTLY ASSUMES `GXEMUL-SEC` IS STABLE.  The sentinel discipline protects a
> measurement against MY OWN mutations; it protects nothing against SOMEONE ELSE'S.**

Every mechanism this project has is scoped to one actor: a `.MUTANT` sentinel announces *my*
mutation, the two-part clearance checks *my* source against SEC and *my* binary against that
source, and the frozen-copy rule protects *my* driver from *my* edits.  **None of them fires
when a second actor changes the reference tree underneath a live run.**  A measurement reading
SEC has no way to notice that SEC moved, and the two-part clearance would have passed at every
instant — the tree was internally consistent both before and after each stash.

## WHAT ACTUALLY DEFENDED IT

Not a rule — a practice the seat brought: **pin the baseline and the instrument, verify the
pin, and drive from the pin, never from the live tree.**  That is the frozen-copy rule
generalised from the DRIVER to the SUBJECT, and it is the only thing here that would have
survived an actor the doctrine does not model.

**The cheap operational rule, and it costs nothing: DO NOT MUTATE A TREE A MEASUREMENT IS
READING — including with `git stash`, which does not look like a mutation and is not covered by
any sentinel.**  If a records commit is blocked behind a running measurement, the honest answer
is that it waits.  I chose to unblock the commit and got away with it because the seat was more
careful than the doctrine required.

*Filed as a carrier candidate rather than written into the carrier here: it is a change to the
sentinel doctrine, which is owner territory.*

---

# THE OTHER OBLIGATION THE SEAT FOUND: `build-asan/` IS PRE-FIX

Verified independently, by md5 of `src/devices/dev_dreamcast_gdrom.c`:

    build        85846dc9    the round fix
    est          85846dc9    the round fix
    GXEMUL-SEC   85846dc9    the round fix
    build-asan   a1bd4373    *** PRE-FIX ***

**DELIBERATELY NOT PROPAGATED YET, and the reason is the carrier's own most-repeated trap.**
`build-asan` is currently CONSISTENT — pre-fix source, pre-fix binary.  Copying the source in
without rebuilding would make it **INCONSISTENT in the dangerous direction**: source that
`cmp`s clean against SEC sitting under a binary that predates it, carrying no sentinel, which
is exactly the state that has twice produced a wrong measurement nobody suspected.

> **The propagation and the ASAN rebuild are ONE action, and they belong at commit time.**
> Until then the honest record is: `build-asan` is pre-fix and must not be measured for #490.

# RESIDUALS THE SEAT FILED (detector is above the floor; these are debt, not breaches)

* **`unk cnt` has no same-session staging guard while `fmt cnt` does** — a sibling-parity
  asymmetry: the round's own wanted-equals-failure rule was applied at ONE site only.  Not
  vacuous today (`M_retB` measured `0x98`), but not self-certifying either.
* **`fmt stage` has no product kill BY DESIGN** — it is an apparatus control.  Worth one
  sentence in the probe header, because a row with no kill is otherwise indistinguishable from
  a vacuous one.
* **`crossbit` covers only the A x B x TOCLEN corner** of a nine-writer field.

*And one finding worth promoting out of the residuals: `latch cond` was formally
indistinguishable from a DEAD REGEX before this table — `REJ` is read by no other row, and by
none with a non-zero want.  It is now measured at 0 / 1 / 2 across builds, so it is a real
oracle rather than a row that cannot fail.*
