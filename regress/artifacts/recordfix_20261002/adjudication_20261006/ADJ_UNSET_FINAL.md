# Previously-unsettled record places -- final rulings on 36 places (2026-10-06)

Adjudicator: the main loop (Claude Opus 5.5).  Evidence: two read-only Opus helpers settled every place against the
files (ADJ_UNSET_A.md: places 2-26; ADJ_UNSET_B.md: places 28-44); GPT-6 Astra at `ultra` checked all 36
(`aconf_unset/codex_aconf_unset.txt`: 6 of 36 wrong, DENOMINATOR 36 of 36).

## Rulings

* **30 places: as the helpers' tables state** (Astra RIGHT).
* **Astra adopted on all six disputes.**  Each is the helper OVER-correcting, and Astra's reading is the minimal edit
  the evidence supports; every objection cites its lines:
  * **A/11, A/12** -- the ORIGINAL ruled replacement fits: it names two examples and never says "only two"; its
    "most" is right (26 sessions, 33 rows, 19 single-row, 7 two-row; `ip30_abort_probe.py`).  The helper's exhaustive
    seven-pair wording is optional and is NOT applied.
  * **A/26** -- the ORIGINAL fits: "that run" sits inside the pmax parenthesis and claims nothing about the full
    sweep (`machine_pmax.c:135,309`; `machine_mvme88k.c:109`).
  * **B/33** -- the ORIGINAL fits: it says the quotient CAN invert the region and already cites `pvrdirtyregion`; the
    zero-width addition is true but optional (`dev_pvr.c:2325`).
  * **B/39** -- the ORIGINAL fits and is supported (`DISPOSITIONS.md:751`; `cpu_alpha_palcode.c:430`).
  * **B/42** -- CURRENT is NOT false: two observed cells do not refute three causal consequences; A+40 observes the
    chain jointly and CURRENT never promised independent observation (`CHANGELOG.md:7304,7308,7330`;
    `alpha_harness_probe.py:318,320,358`).  NO edit.

## Counts

36 places: CURRENT false 35, not false 1 (B/42).  Replacement as ruled 31 (26 + the five restored originals);
helper's corrected wording 4 (A: none of 11/12/26; B: 28, 31, 32, 43).  Already fixed at HEAD 0.

## Also found (outside these places)

`regress/sh_iprbcd_probe.py:293` repeats place 29's IPRB/IPRC mistake; `CHANGELOG.md:19574` ("every mutant is
reddened by exactly the row built for it") is contradicted by `:19558`.  Both are owed in the next records commit.

## Addendum -- `regress/sh_iprbcd_probe.py:301-302` (found by the #561 drafter; ruled by the main loop 2026-10-06)

CURRENT: "These two rows are the reason that exposure exists; without them it is an unused convenience, and with them
the escape class is closed."  **FALSE**, the same false half as place 31: EIGHT shipped rows read `iprio_<slot>` through
`write_ipr_then_read` (HEAD `regress/sh_iprbcd_probe.py`): `iprb wdt` (:328), `ipra rtc` (:334), `iprd hold` (:358),
`iprd ctl` (:360), and `scif eri/rxi/bri/txi` (:393-395); `git grep iprio` finds no other shipped reader.
REPLACEMENT: "These two rows read that exposure for the IPRB and IPRA sources; six more read it too (`iprd hold`,
`iprd ctl`, `scif eri/rxi/bri/txi`), and together they close the escape class."  (Worded without any claim about which
rows came first: that history was not verified.)
