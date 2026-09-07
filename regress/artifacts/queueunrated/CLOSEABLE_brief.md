# CLOSURE PASS — 11 open ledger rows that already carry a COMMIT

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** Today a seat refuted a premise I had stated as
*settled* after three other seats confirmed it; the refutation was right. Separately, **four of my
own censuses each keyed on one spelling and missed a variant** (`severity` vs `sev`, `<< 24` vs
`<< 16`, `(int)idata` vs `(int) idata`, `witness != 'none'` vs `none -- <why>`). **Assume the framing
below has at least one such error and find it.**

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** Three pristine-2021-upstream copies of GXemul sit
under the project root and are NOT this fork; a seat reading one reports line numbers off by hundreds.

**SCOPE:** `GXEMUL-SEC/src/`, `GXEMUL-SEC/regress/`, `GXEMUL-SEC/tools/pipeline/ledger.json`, and
`git log` / `git show` on this repo.

**VERDICT LINE FIRST.**

---

## §C — SETTLED PREMISES

**S1 — the class is real and today produced five instances.** `lunaabsentcpu` (fixed by `#503`,
never closed); `wdcflood`, `pitclobber` and `asiceventaddr` (all three found still-open by a codex
rating pass and verified fixed by reading); and a `dev_pvr.c` site a grok census found already
de-fatalised by `#166`. **Five is a class, not an accident.**

**S2 — the signal, and why it is not a correlate.** A ledger row that carries a `commits` value is a
row where **work landed**. If it is still `open`/`in work`, either residual work genuinely remains,
or nobody closed it. Derived:

```
open + in work                          190
  carrying commits                       14      <- this list
  note/witness merely CITES a #NNN round  40      <- a different, weaker key
  both                                     4
```

The two keys overlap in only 4 rows, which is the point of running both: *carries a commit* and
*mentions a round* are different claims.

**S3 — three of the fourteen are already known-fixed** (`wdcflood`, `pitclobber`, `asiceventaddr`)
and are **excluded below**. That the signal caught 3 of the 4 known instances is what licenses using
it on the rest.

**S4 — what a closure needs here.** Not "the code looks fixed". This project requires: the defect no
longer reachable, **named carrying rows** (which probe, which row label) that would redden if it
returned, and — where a row is closed because *another* round's fix removed the defect — a
discriminating control. **A row with no carrier is not closeable; it is uncovered.**

---

## The rows

**Product code:**
```
pcc2widthkills       high  open     b78bb0f   dev_pcc2.c: TEN live width kills of twelve guards
wdcaddtoinbufbound   med   in work  ae68e29   the ATAPI data-port WRITE arm bound
gdromdmawidth        -     open     029a137   the DMA tail store ignores `len`
gdromwarnbits        -     in work  84f6682 84765ec   six of eight warn bits, hand-assigned
landiskdisk          -     in work  b744299   the landisk rig attaches NO DISK
ovsync               -     in work  4d0981d   SYNCHRONIZE CACHE does not flush overlay/bitmap files
```

**Harness / tooling:**
```
wiringcliff          med   open     8404520   eight probe-wiring exemptions expire 2026-09-20
diskimagesign        -     in work  18893de   #472's clamp introduced two -Wsign-compare warnings
probetimebased       -     open     abf665c   pty probes with NO prompt detection
seatthinkburn        -     open     a4d054d   the fifth seat-failure class
wdcfloodstale        -     in work  3cdb58a   `overrun x2` cannot reach its target
```

## The questions

**Q1 — FOR EACH: is the defect still present at HEAD?** Read the source (and `git show` the named
commit to see what it did). **Answer CLOSEABLE / RESIDUAL-REMAINS / STILL-OPEN, and say which part
remains** where it does. A partial fix left open is the correct state and is not a finding.

**Q2 — FOR EVERY ROW YOU CALL CLOSEABLE, NAME ITS CARRIER.** Which probe, which row label, would
redden if the defect returned? **If you cannot name one, say so plainly** — that converts the row
from "closeable" into "fixed but uncovered", which is a different disposition and a more useful
finding.

**Q3 — WHICH ARE MIS-STATED RATHER THAN FIXED?** A row whose title describes something the code never
did is not closeable, it is *wrong*, and it should be withdrawn rather than closed. This project
withdrew one such finding this week (`sgilinearnegidx` — an `unsigned` declaration three lines above
the quoted code voided the whole analysis).

**Q4 — `pcc2widthkills` IS THE ONE I EXPECT TO BE LEGITIMATELY OPEN** (ten live host kills, a probe
witness, an unresolved design question). **Check that expectation rather than accepting it** — if its
commit already removed some of the ten, the row's own count is stale and that matters, because this
project has had three separate rows carry a wrong kill-count.

**Q5 — WHAT DOES THIS SIGNAL MISS?** A row fixed by a round that never attached its commit carries
no `commits` value and is invisible here. **Can you name a better key?** `lunaabsentcpu` was found by
accident, not by this signal.

## What I am not asking

Do not write patches, do not edit the ledger, and do not run builds, gates or probes. **Nothing ships
until the flagship adjudication on 2026-09-09.**

**If, while verifying a claim, you found something ELSE — say so.**
