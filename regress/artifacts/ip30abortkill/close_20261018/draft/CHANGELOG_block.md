# Records, 2026-10-18: `ip30abortkill` closes -- clause (b) measured on the shipped 33-row instrument, 14/33 as named before the run; its residuals move to `ip30abortresidual`; REGRESS held

`#531` (`686d179c`, committed 2026-09-18) took the four guest-reachable `abort()` calls out of
`src/devices/dev_sgi_ip30.c`: the `0x10020` and `0x10028` loads decline silently, their stores keep their effect with
one latched announce (`IP30_W_ISR`), the `0x10030` store is dropped with that same announce, and DEVICE_TICK's bit-50
arm announces once on its own bit.  Its detector, `regress/artifacts/ip30abortkill/ip30_abort_probe.py` (33 rows),
runs in gate 14 since `#566` (`8faf4a16`).  `#566` named three things still owed before the row could close; this
commit discharges them and closes it:

* **CLAUSE (b), MEASURED** (`regress/artifacts/ip30abortkill/close_20261018/`).  HEAD's `dev_sgi_ip30.c` with the
  removed `fatal("IP30 legacy interrupt rewrite: TODO\n"); abort();` pair re-inserted verbatim at all four fixed sites
  -- after DEVICE_TICK's latched bit-50 announce, after the `0x10020` and `0x10028` arms' if/else, after the `0x10030`
  write announce -- built in `#566`'s scratch clone: **14/33**, the six kill rows DEAD and thirteen state rows `died`;
  gate 14's block text on that log, 41 checks and 22 red.  `PREDICT_clause_b.txt`, written before the build, named
  the same 19 red rows and the same 14 green ones; `CLAUSE_B.txt` records the file times, which git does not carry.
  The clone was restored to HEAD and cleared both parts.  `build/` was not touched.
* **THE WITNESS** now leads with the shipped instrument's pair -- PRE-FIX 10/33, POST-FIX 33/33 (`#566`'s legs) --
  and the clause (b) leg; the 21-row pair and the 18-row oracle-correction order proof stay, as history.
* **THE RESIDUALS** move to a new row, `ip30abortresidual` (LOW, open), rather than close with `ip30abortkill`, as
  `#527`'s closure did with `ppc527residual`: `V7_nocounter` (delete `d->reg_0x20000 += 1000`; 32/32 in kill table 4,
  on the 32-row instrument) and the width axis `V8_len4` (`&& len == 4` on the `0x10020` write guard; 33/33 in kill
  table 5), both disclosed in the probe's CONTRACT; and places 7-10 of `#561`'s HELD list, ruled replacements for
  `dev_sgi_ip30.c`'s latch comment -- which still counts SIX announce paths with `IP30_W_ISR` covering FIVE, both
  read arms among them, where the shipped code has four and three -- and for three sentences that still count five ISR
  sites.  `#561` held them because a `src/` comment owes `est/` byte-identity and build-tree propagation; the row puts
  that `dev_sgi_ip30.c` obligation on the ledger.  None is a floor breach.
* **REGRESS and the closure review held for the flagship**: the row's `hold_question` asks for 33/33, 10/33 and 14/33
  on the three builds, and whether the closure stands.
* `wiringcliff`'s commits field gains `#566`'s `8faf4a16`.

{CLOSURE_CHECK}  Ledger, bug file, matrix, queue and this block only; no `src/` touched.
