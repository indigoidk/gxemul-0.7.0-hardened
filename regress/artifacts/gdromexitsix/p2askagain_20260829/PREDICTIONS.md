# #490 pass 2 — the ASK-AGAIN, predictions written BEFORE the runs

**Written 2026-08-29 ~07:41 by the opus measuring seat, while `probe_base.log` was still
being written and NO mutant run had started.** The directory listing at the time of writing
showed exactly one log (`probe_base.log`, in progress) and no `probe_E*` files. This file's
mtime is the order proof: a prediction written after its own measurement cannot be told from
a number fitted to the answer, which is this project's own rule for score claims and for
oracle re-pins.

## Apparatus

* Clone `/tmp/gxopus490p2`, `cp -a` of `/tmp/gxr2m`, source FORCED to the pin
  `/tmp/r2m_pinned/dev_dreamcast_gdrom.c.BASELINE` (md5 `85846dc966d00efe511d2b5755364490`)
  rather than trusting what the clone inherited.
* **The clone rebuilt the baseline binary to md5 `8d473baa488b2aef3eabd3be569f2c9d` — byte
  for byte the r2measure table's own baseline.** That is the apparatus control: my tree and
  the round's tree compile to the same binary.
* `.MUTANT` sentinel dropped before mutant 1, cleared only after `cmp` against the pin AND
  `[ binary -nt source ]`. All four builds reported `binary-newer-than-source=YES`; all
  three mutant binaries are md5-distinct from base.
* Instrument: my own frozen copy of `gdrom_decline_probe.py.FROZEN`, md5
  `188e92ebd8f9593664c294c63fed0d98` — the same instrument the twelve-run table used.
* Runs strictly serial; no build runs during a probe.

## The three mutants, and why each is a clause-(d) form rather than a new class

### E1_aliasover — `(1u << GDROM_W_FMT_B)` -> `(1u << GDROM_W_OVERREAD_B)`

Site A's latch aliased onto a pre-existing bit that is **not** the one `crossbit` builds.
`crossbit` establishes exactly one prior state — `GDROM_W_TOCLEN`, via a short TOC — so it
covers 1 of the 7 pre-existing bits. The other six (`LEN`, `NODATA`, `NOTWAIT`, `OVERREAD`,
`DMANODATA`, `DMAARM`) are set from inside `DEVICE_ACCESS` and **no probe session sets any of
them**: no session reads `GDROM_DATA` (so `NODATA`/`OVERREAD` never fire), every session
writes `COND` before the packet (so `NOTWAIT` never fires), every access is 16-bit (so `LEN`
never fires), and no session arms DMA.

**PREDICTION: 20/20, ESCAPES.**

### E2_assignA — `d->warned |= GDROM_W_FMT;` -> `d->warned = GDROM_W_FMT;`

One character. Site A's latch set **clears every other latch bit in the device**. The defect
is not at Site A at all — Site A still announces exactly once — it is that the other eight
once-only diagnostics become re-announceable, so a guest alternating a bad data format with
any latched condition floods the log without bound. That is the guest-drivable-`fatal()`
flood class the latch idiom exists to close, re-opened by deleting one character.

No row observes a latch bit across a FMT decline except `crossbit`, and `crossbit` reads only
whether the two NEW sites still speak — which they do.

**PREDICTION: 20/20, ESCAPES.**

### E3_widenA — `if (!(d->warned & GDROM_W_FMT))` -> `if (!(d->warned & (GDROM_W_FMT | GDROM_W_CMD)))`

Site A's guard widened to test both bits. **Order-asymmetric**: on the probe's fixed
FMT-then-CMD order nothing changes, because `warned` is 0 when Site A is reached. Reverse the
order — an unknown COMMAND before an unknown FORMAT, which is the order a probing guest
naturally walks — and Site A is permanently silent. `both sites` and `crossbit` both fix the
FMT-then-CMD order, so neither can see it.

**PREDICTION: 20/20, ESCAPES.**

## A fourth, REASONED ONLY — not built, and said so plainly

### E4 — delete `case 0x70:` (the MOUNT arm)

`handle_command`'s switch has exactly three case labels (`0x14`, `0x30`, `0x70`) plus
`default:`. Deleting `case 0x70:` routes MOUNT — a command NetBSD's `gdrom_mount_disk()`
actually issues — into the now-declining `default:` arm. **Before this round that edit killed
the host on the first mount; after it, the mount is silently declined once.** That is the
de-escalation clause verbatim: the fix deleted the accidental tripwire that made this
self-announcing.

It is provable without building: `grep -c 0x70` is **0** in `gdrom_default_probe.py` and
**1** in `gdrom_decline_probe.py`, and that one occurrence is the definition of `MOUNT`,
which is **never used in any session**. No row can observe a command no session sends.

**PREDICTION: 20/20, ESCAPES — by inspection, not by measurement.**

`MOUNT = cmd(0x70)` is the fossil of the PRE-TABLE block's prescribed row 8, `0x70 negative
diag -- the sibling row, re-aimed`, which was specified before the product edit and never
written.
