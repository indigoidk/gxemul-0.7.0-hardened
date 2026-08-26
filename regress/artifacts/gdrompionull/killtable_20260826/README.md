# `gdrompionull` kill table — opus5, 2026-08-26

Preserved from WSL `/tmp` **at the seat's own request**: *"These are session-temp paths. Per
your own durable-path rule, copy them beside the round record before citing any number."*

## What these logs are, and what they are NOT

`gxo465_det_*.txt` are the **INTENT-ONLY 16-row** table — the detector built from the fix's
own stated intent. The seat's report also quotes a **FULL 26-row** table; those scores are not
in this directory, and the distinction matters because the two denominators tell opposite
stories about the same mutant.

    build           intent /16      what it means
    base            10/16           the committed defect: six rows red
    fix             16/16           the tail form, clean on intent
    m_helper        16/16           the free_data() form, clean on intent
    m_helper_ret    16/16           helper + break->return: STILL CLEAN
    m_ret415        16/16           *** tail form + break->return: CLEAN SWEEP ***
    m_free          13/16           clear at :446 only — caught by the STAGED route
    m_top           13/16           clear at :326 only — caught by the CHEAP route
    m_swapcnt       10/16           clause-(d) operand swap: reads like base

## The two results this table carries

**1. `m_ret415` sweeps the intent detector CLEAN at 16/16.** One word — `break;` → `return;`
at `:415` — and a detector built only from the fix's intent sees nothing. That is why the
round owes rows for the `:406`/`:415` arms as **L1 pre-ship construction**: they are the only
rows that catch the tail-bypass class.

**2. `m_free` and `m_top` escape COMPLEMENTARY halves** — 13/16 each, and not the same 13.
`m_free` is caught only by the staged route; `m_top` only by the cheap route. **So the two
witnessed routes are not redundant; each is the sole killer of one relocation mutant.** Any
future round tempted to drop one as duplicative is measured wrong.

## Excluded deliberately

The eight mutant binaries (6,155,864 bytes each, ~49 MB) are **not** here. They are
rebuildable from the recorded mutant edits, and bulk in a records directory is not evidence.
The build logs and score logs are.

## Caveat on the load

The seat disclosed unprompted that its runs overlapped a concurrent kill table in the same
session. These particular measurements are load-insensitive — offline differentials and
opcode censuses with no wall-clock oracle — but that disclosure belongs beside the numbers
rather than in a transcript nobody re-reads.
