# EVIDENCE PASS — 11 open ledger rows that carry a TITLE and NO NOTE

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** Earlier today I stated a premise as *settled*;
three of six seats confirmed it and **one seat opened the file and refuted it** — correctly, and it
reversed the round's blocking question. **Every title below is a claim written by someone who has
since forgotten the evidence. Treat each as a HYPOTHESIS, not a finding.** I expect at least one to
be wrong.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** Three pristine-2021-upstream copies of GXemul sit
under the project root and are NOT this fork; a seat reading one reports line numbers off by hundreds
and different arms exist.

**SCOPE:** `GXEMUL-SEC/src/devices/`, `GXEMUL-SEC/regress/*.py`.

**VERDICT LINE FIRST.**

---

## §C — SETTLED PREMISES

**S1 — the gap, derived.** Of 189 open/in-work ledger rows, **12 carry a title and no `state_note` at
all**. A row with no note cannot be worked, ranked, or closed without re-deriving everything from its
title — which is exactly what happened this afternoon to `lcaconfwidth` (also bare) and cost a full
census. **All 12 are also unrated.**

**S2 — these are not junk rows.** Five of the eleven below carry a **witness**, meaning someone
measured something and wrote none of it down.

**S3 — what a usable note contains here**, from the rows that have good ones: the defect in one
sentence; the **source anchor** (file plus a grep-able string, *not* a bare line number — same-file
line numbers go stale from a round's own edits); whether a **guest can reach it**; and what would have
to be true for the row to be wrong.

---

## The rows

**`dev_dreamcast_gdrom.c` family:**
```
gdromcondavail   COND_DATA_AVAIL permanently lies after an overread          [has witness]
gdromdmaclear    a decline path CLEARS an already-pending DMA completion     [has witness]
gdromdmaguard    `count == 1` -> `count <= 1` accepts a (0,1) arming         [has witness]
gdromkeyindex    five mutants score a full 32/32 against #461's detector     [has witness]
```

**`dev_sh4.c` family:**
```
sh4cpudevscope    the SH-4 on-chip block is added PER-CPU but ...
sh4iprunpinned    #458's detector reads only four of the ~20 priority fields
sh4irlm           ICR IRLM=1 is refused outright, and that refusal is ...
sh4pclockquiet    five measured mutants of #459's pclock guard ...
sh4standinglower  no row asserts at a high priority and then ...
sh4testclock      baresh and testsh have no pclock, so the harness ...
```

**Harness:**
```
gatebuildallow   gate_build.sh PINS its own twin-tree allowlist while ...     [has witness]
```

## The task

For **each** row: **read the source and write the note S3 describes.** Three to eight lines each. Then
answer:

**Q1 — WHICH OF THESE ARE STILL TRUE?** Several titles are weeks old and the code has moved. **Name
every one whose claim no longer holds**, with the evidence. A row that has been fixed by another round
and never closed is the single most valuable thing you can find here — this queue closed one such row
today (`lunaabsentcpu`, fixed by `#503` and left open).

**Q2 — `sev` FOR EACH: high / med / low.** Say which axis drives it — **guest reachability** or
**consequence**. A defect a guest cannot reach is not high whatever it would do. For calibration, four
current `high` rows: a device with twelve live `exit()` calls reachable from guest writes; a legal
one-byte guest write that ends the process; a page-table walk returning a wrong PFN; an exception path
that stops every guest CPU.

**Q3 — WHICH ARE THE SAME DEFECT?** The four `gdrom*` rows were filed separately over several rounds.
**If any two are one defect, say so** — a duplicate closed on one of its faces buries the other, which
this project has recorded happening.

**Q4 — WHICH ARE PRODUCT DEFECTS AND WHICH ARE DETECTOR/COVERAGE DEBT?** `gdromkeyindex`,
`sh4iprunpinned`, `sh4pclockquiet` and `sh4standinglower` all read as claims about *detectors* rather
than about emulator code. **That distinction changes the disposition entirely** — product defects get
rounds; coverage debt gets filed and ranked below live defects in the same file.

## What I am not asking

Do not write patches, do not edit the ledger, and do not run builds, gates or probes. **Nothing ships
until the flagship adjudication on 2026-09-09.**

**If, while verifying a claim, you found something ELSE — say so.**
