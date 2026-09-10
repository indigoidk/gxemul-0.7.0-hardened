# `#516` measurement artifacts — WHICH INSTRUMENT PRODUCED WHICH NUMBER

**Read this before citing any figure here.** Two different instruments ran during this round, and
their scores are not comparable.

## The CITED pair — one instrument, both directions

    prefix_lca_irqstub_probe.raw            3/6      the 6-row instrument, PRE-FIX
    fix_lca_irqstub_probe.raw               6/6      the 6-row instrument, POST-FIX

    prefix_lca_irqstub_uart_probe.raw       2/5      the 5-row instrument, PRE-FIX
    fix_lca_irqstub_uart_probe.raw          5/5      the 5-row instrument, POST-FIX

## The SUPERSEDED pair — the 4-row instrument, kept only as history

    SUPERSEDED_4row_instrument_lca_irqstub_probe.raw        4/4
    SUPERSEDED_4row_instrument_lca_irqstub_uart_probe.raw   4/4

These ran **before the round added its three discriminating rows**, so their `4/4` says only that
the original witness rows went green. They are NOT the post-fix score and must not be quoted as it.
Renamed from `w1.raw`/`w2.raw`, which said nothing about which instrument produced them.

## A defect that affected the numbers, and is repaired

The three added rows were first inserted BELOW each probe's score computation, which split both
scorers — numerator over the old row set, denominator evaluated at print time. The 8042 probe
printed **six rows all `ok` under a summary of 4/6**, and the UART probe reported **3/5 pre-fix where
the honest score was 2/5**. Repaired by moving the computation adjacent to the print in both files.
**Every figure above is from the repaired scorers.**

A position census over HEAD found **0 of 73** candidate probes were ever split: both instances were
created by this round's own edits, not inherited. Filed as `splitscorer` (low).
