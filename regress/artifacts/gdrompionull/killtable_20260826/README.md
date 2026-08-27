# `gdrompionull` kill table — opus5, 2026-08-26

Preserved from WSL `/tmp` **at the seat's own request**: *"These are session-temp paths. Per
your own durable-path rule, copy them beside the round record before citing any number."*

## What these logs are, and what they are NOT

*** THIS README WAS WRONG ON BOTH ITS CLAIMS AND THE PASS-2 CODEX SEAT CAUGHT IT. ***
It said the full 26-row scores were "not in this directory". **They are** — every
`gxo465_det_*.txt` carries its own `FULL=n/26 INTENTONLY=n/16` line. And it let the
round claim `m_ret415` "swept a clean detector", which is true only of the
intent-only subset.

`gxo465_det_*.txt` carry BOTH denominators, and they tell opposite stories about the
same mutant — which is exactly why quoting one without naming it is a wrong record.

    build           intent/16   FULL/26   what it means
    base            10/16       16/26     the committed defect
    fix             16/16       26/26     the shipped helper form
    m_helper        16/16       26/26     helper, equivalent
    m_helper_ret    16/16       25/26     *** helper + break->return: KILLED, fails `cnt post`
    m_ret415        16/16       23/26     tail form + break->return: THREE rows kill it
    m_free          13/16       19/26     clear at :446 only -- caught by the STAGED route
    m_top           13/16       23/26     clear at :326 only -- caught by the CHEAP route
    m_swapcnt       10/16       14/26     *** the real clause-(d) mutant: STRONGLY KILLED

## The two results this table carries — RESTATED after the pass-2 correction

**1. `m_ret415` is NOT a clause-(d) breach, and the round's framing of it was wrong.** It
scores 16/16 on the intent-only subset but **23/26 on the full table**, and — decisively — it
attacks the **rejected tail-assignment design**, not the shipped helper. The mutant against the
shipped design is `m_helper_ret`, killed at 25/26. **The actual clause-(d) repair-null mutant
is `m_swapcnt`, strongly killed at 14/26.** So the shipped fix's own repair IS defended, and
the missing tail rows are above-floor coverage debt rather than an L1 obligation the round
failed to discharge. *The round called them "L1 pre-ship construction" while omitting them,
which is internally inconsistent: L1 means finish in-round.*

**2. `m_free` and `m_top` escape COMPLEMENTARY halves.** Each witnessed route is the sole
killer of one relocation mutant, so the two are not redundant, and a future round tempted to
drop one as duplicative is measured wrong. *(This one survives the correction unchanged.)*

## Excluded deliberately

The eight mutant binaries (6,155,864 bytes each, ~49 MB) are **not** here. They are
rebuildable from the recorded mutant edits, and bulk in a records directory is not evidence.
The build logs and score logs are.

## Caveat on the load

The seat disclosed unprompted that its runs overlapped a concurrent kill table in the same
session. These particular measurements are load-insensitive — offline differentials and
opcode censuses with no wall-clock oracle — but that disclosure belongs beside the numbers
rather than in a transcript nobody re-reads.
