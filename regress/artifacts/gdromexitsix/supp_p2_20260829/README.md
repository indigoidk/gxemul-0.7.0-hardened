# #490 SUPPLEMENTARY pass 2 -- the measuring seat's artifacts

*** THE TREE MOVED DURING THIS REVIEW.  EVERY FILE HERE IS LABELLED WITH THE CODE
STATE IT MEASURED, because an artifact whose caption describes one state and whose
numbers describe another is this project's frozen-number defect at its worst. ***

    PRE  md5 6366988a5156c59a9b6bc8cc7aab9ec2   the OR-based assert, as at 13:35
    POST md5 53dd0e22fcc46a5f9e2ba921d62ea9d9   the SUM-based assert, landed ~14:4x

`bothstates_20260829.out` is the authoritative record: eight states x both forms.

| file | code state measured | what it says |
|---|---|---|
| `bothstates_20260829.out` | **BOTH** | PRE has 3 escapes; POST has 0.  Read this one. |
| `enumattack_20260829.out` | PRE (standalone TU, `\|` hardcoded) | the enum-side escape, isolated |
| `repair_20260829.out` | PRE vs a `sum==or` candidate | superseded -- see note below |
| `realfile2_20260829_POSTFIX_TREE.out` | **POST** | all green.  Its own caption asks "which aliases escape" and the answer on the POST tree is NONE.  It does NOT show the pre-fix escape; `bothstates` does. |
| `nbits32_20260829.out` | either | the seam between the two asserts at NBITS==32 |
| `probe_{base,E2_assignA,E3_widenA}.log` | round's pinned post-fix binary | the two candidate rows, 22 rows |
| `def_{base,H1_exit1}.log` | clone-rebuilt base + main.c mutant | `stale how`'s measured red |

## The `sum==or` candidate is SUPERSEDED and this says so rather than deleting it

I proposed `SUM(masks) == OR(masks)` and measured it catching all three enum-side
aliases.  It is strictly WEAKER than what landed: it proves disjointness only, so
it misses A6/A7 (a bit added without extending the list), and I had therefore
recommended keeping BOTH declarations.  The landed
`SUM(masks) == ((1u << NBITS) - 1u)` proves disjointness AND coverage in one
expression -- measured at A2/A3/A5 REFUSED and A6/A7 still REFUSED.  One
declaration, no pair.  Recorded because a superseded proposal that is silently
dropped reads later as if it had never been tested.

## Apparatus

No project tree was written.  Compiles ran on copies in /tmp; the probe runs used
already-built binaries from the ask-again (`/tmp/gxopus490p2_bins`, md5s verified
against `p2askagain_20260829/RESULTS.md` before use) plus one clone for `stale how`
(`/tmp/gxsupp490_h1`, sentinel dropped before the mutant and cleared only after
`cmp` against SEC AND a rebuild reproducing base md5 `8d473baa488b2aef3eabd3be569f2c9d`).
Every probe log carries its completion sentinel.

## MANIFEST LINES THIS COMMIT OWES (check_probe_wiring.py)

Every python artefact under `regress/` needs a MANIFEST line with a CLASS.  Four
pending files have none, and **two of them predate this seat**:

    artifacts/gdromexitsix/p2askagain_20260829/mut490p2.py        <- the ask-again's mutator
    artifacts/gdromexitsix/rot_20260829/probe.frozen.py           <- the rot run's instrument
    artifacts/gdromexitsix/supp_p2_20260829/extend.py             <- mine
    artifacts/gdromexitsix/supp_p2_20260829/instrument_22row.frozen.py   <- mine

All four are CLASS_TOOL / CLASS_RESEARCH, not detectors: none is gated and none
should be.  My instrument copy was originally named `gxsupp490_probe.py` and was
RENAMED, because a `_probe.py` suffix trips the checker's MISFILED rule when the
file is classed as a tool -- the exact "file with no honest class" the checker's
own header at :138-143 warns about.

`instrument_22row.frozen.py` is reproducible rather than magic:
`python3 extend.py <pinned 20-row probe> out.py`, from
`/tmp/r2m_pinned/gdrom_decline_probe.py.FROZEN` md5 `188e92ebd8f9593664c294c63fed0d98`,
yields md5 `17115bba7c5022b26eebd9dfe5cd15cb` -- the instrument all three
`probe_*.log` runs used, as each log's `PROBE_INSTRUMENT_MD5` records.
