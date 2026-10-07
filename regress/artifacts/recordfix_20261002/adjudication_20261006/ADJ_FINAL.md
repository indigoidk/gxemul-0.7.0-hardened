# Record corrections -- final rulings on the 36 flagged places (2026-10-06)

Adjudicator: the main loop (Claude Opus 5.5), owner's instruction 2026-10-06 ("if there is anything that opus (5.5) can
adjudicate ... proceed").  Evidence: three read-only Opus helpers (ADJ_01_03.md, ADJ_04_06.md, ADJ_07_09.md), each place
settled against the files at 1329d894 and HEAD; GPT-6 Astra at `ultra` checked all 36 rows against the files
(`aconf_rrec/codex_aconf_rrec.txt`: 1 of 36 wrong, DENOMINATOR 36 of 36).

## Rulings

* **35 rows: as the helpers' tables state** (Astra RIGHT on each).
* **ADJ_01_03 place 27 (devle:F5): the helper's corrected replacement is WRONG** -- Astra, verified here by reading
  `src/devices/dev_le.c` at HEAD: the copy into SRAM runs at `:572-580`, the #262 lookahead at `:619-636`, the
  writeback of the CURRENT descriptor at `:648-652`.  DMA precedes the lookahead, so it cannot invalidate an
  already-accepted next descriptor in the same call.  The CURRENT sentence is still FALSE as an absolute; the
  replacement keeps only the later-call qualification (partial-frame retention plus an intervening descriptor change)
  and drops the same-call explanation.

## Counts

36 places: current false 33; current true 3 (59 -- the false claim is the `memory_rw.c` source comment, retarget there;
69 and 70 -- true as history, append a dated note instead of overwriting).  Ruled replacement fits 25; needs new
wording 11 (helpers' corrections, place 27 as amended above).  Already fixed at HEAD: 0.

## Not ruled here

Places all of whose readings were FITS or UNSETTLED only -- they are being re-read with the rebuilt packets (citations
inlined) and are ruled when those return.  The corrections land as ONE records commit by family after that, staged from
HEAD plus these edits only (several files carry another session's uncommitted work), with Astra's confirmation first.
