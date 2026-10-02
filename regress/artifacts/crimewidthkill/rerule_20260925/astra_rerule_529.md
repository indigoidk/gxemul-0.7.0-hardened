You are the second ADJUDICATOR (with the flagship seat) for round #529 of a C hardware emulator (GXemul fork): the
SGI O2 CRIME register block (`src/devices/dev_sgi_ip32.c`, `DEVICE_ACCESS(crime)`) used to end the emulator process on
a guest access of an unsupported width; the uncommitted fix declines those accesses with a once-per-device message,
and a 204-row regression probe (`regress/crime_width_probe.py`, untracked) defends it.  Read-only; no file may be
changed.  Nothing is committed until you confirm.

**Why you are asked.**  Three rulings on record under the flagship seat's name were written by a fallback model, and one
of them overturned a ruling the flagship seat genuinely wrote.  Tonight the flagship seat (verified claude-fable-5-1)
re-ruled all four questions first-hand: **C3 STANDS, D7 FLOOR (its own earlier RA3 overturned), Q3 ADOPT (amended),
STOP RATIFY**, and set out what the round owes.  Confirm or overturn each, on the evidence.

Read ONLY these, under `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\` (do not read other `regress/artifacts/` folders or
`tools/pipeline/ledger.json`):
1. The ruling to check: `regress/artifacts/crimewidthkill/rerule_20260925/fable5_rerule_529_20260925.md`, and the brief
   it answered, `fable_rerule_brief.md` beside it.  The survey both rely on: `resume_dossier_20260925.md` beside it
   (sections 0, 2, 3; each claim tagged READ / COMPUTED / INFERRED).
2. The four earlier rulings: `regress/artifacts/lcaisalane/FABLE_C3_RULING_20260914.md`, `FABLE_C4_RULING_20260915.md`
   (genuine; its RA3), `FABLE_C5_RULING_20260915.md`, and
   `regress/artifacts/crimewidthkill/repair14_20260916/FABLE_RULING_20260917.md`.
3. The measurements they cite: `regress/artifacts/crimewidthkill/repair14_20260916/POSTTABLE.out` and `check_pred.out`,
   and `regress/artifacts/crimewidthkill/killtable11_20260916/POSTTABLE.out`.
4. The code: `src/devices/dev_sgi_ip32.c` (the CRIME access function) and `regress/crime_width_probe.py` (its header is
   the probe's contract).
5. The rule text the ruling applies: `C:\DocumentNoSnc\cc\GXEMUL\CLAUDE.md`, the block headed "JOINT CELLS" and the
   paragraphs after it through "TESTS MEANS MASKS OR COMPARES AS A CASE".

FIRST LINE: `VERDICT: <CONFIRM | CONFIRM WITH CHANGES | DO NOT CONFIRM>`.  Then, one short paragraph each: (1) C3;
(2) D7 -- in particular whether the latch read at the decline path makes the latch-conditioned accept shrink a floor
cell, and whether that is consistent with the #549 ruling cited in the ruling; (3) Q3 and its three amendments; (4) the
stop condition, including whether the INTMASK and CONTROL-write label swaps must be measured rather than derived, and
whether repair 14's single-seat pass can close the chain; (5) the "what #529 owes" list -- anything missing, misgraded
or out of order.  Check every line number the ruling cites against the file.  Say what is a reading and what is a
measurement.
