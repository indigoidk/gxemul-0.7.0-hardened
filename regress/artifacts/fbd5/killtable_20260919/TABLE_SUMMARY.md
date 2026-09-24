# #545 fbdeclinefive -- kill table 2 (the round's table), 2026-09-19 08:58-09:03

Scratch clone /tmp/gxfbd5 = `cp -a build/`; baseline dev_footbridge.c cmp == SEC HEAD f685d75; every build FRESH
(`[ gxemul -nt dev_footbridge.c ]`); instruments FROZEN in the clone before the first run; clone-local .MUTANT dropped
first and cleared only after the restore verified (source == SEC HEAD, binary fresh, md5 e5d18154 == the HEAD build).
Table 1 (08:51) found two defects in the INSTRUMENT (a quit-leg arm named `Q` shadowed arm E's constant; the witness
rollup still named the retired `K`) -- recorded in PRETABLE.out, fixed, and table 1 kept as table1_instrumentdefect/.
The patched probes in GXEMUL-SEC are byte-identical to the copies table 2 measured.

| build | sites probe (36 rows) | offline differential (111 rows) | pending probes |
|---|---|---|---|
| HEAD (pre-fix) | **FAIL: 21 of 36 rows green, 15 red** -- SC1 SA1 S1-S5 SF1 SF2 N0-N5 red (arm S dies at its first decline, exit 1) | **dies at P1** (rc 1) | witness H1/H2 ok (legs are product-independent) |
| FIX | **36/36 PASS**, controls OK | **111/111 PASS** | witness PASS, drain H1/H2/R0 ok |
| M1 keep exit(1) at FIQ_RAW_STATUS write | 21/36 (arm S dies) | dies (rc 1) | |
| M2 unlatched announce, IRQ_STATUS | 34/36: N1 N0 | 4 red: P1 latch, P6, P8 | |
| M3 IRQ_STATUS/IRQ_RAW_STATUS share a latch | 34/36: N2 N0 | 3 red: P2 once, P6, P8 | |
| M4 FIQ_RAW_STATUS tests the FIQ_STATUS latch | 34/36: N5 N0 | 3 red: P5 once, P6, P8 | |
| M5 the +0x18c read keeps leaking irq_enable | 35/36: N3 | 1 red: P3 read returns 0 | |
| M6 IRQ_STATUS decline stores into irq_status | 33/36: S1 S2 SF1 | 12 red: preservation | |
| M7 legal IRQ_STATUS read -> constant 0 (Q2 f) | **36/36 -- guest-blind, as DISCLOSED** | 2 red: P0, P7 | |
| M8 FIQ_STATUS read drops the `&` | **36/36 -- guest-blind, as DISCLOSED** | 1 red: P0 FIQ_STATUS | |
| M9 IRQ_RAW_STATUS text misnames the register | 33/36: N1 N2 N0 | **0 red -- offline-blind, as PREDICTED** (fatal() is a counter there) | |
| M10 the +0x18c read clears its own latch | 34/36: N3 N0 | 4 red: P3 latch, P6, P8 | |
| M11 IRQ_STATUS decline only for len == 4 | **36/36 -- guest-blind** | 1 red: P9 byte-first | |
| M12 (harness) H2 without the quit | 35/36: H2 | | |
| M14 (harness) H1 on any nonzero exit, `-M notanumber` launch | weakened H1 **ok** (the vacuity is real) | | |
| M14ctl the SHIPPED H1 predicate, same launch | shipped H1 **FAIL** (named=False) -- the text clause discriminates | | |

**Every product mutant M1-M11 is killed by the COMPOSITE detector** (sites guest rows + offline P-rows).  Three are
killed only offline (M7, M8, M11) and one only by the guest rows (M9) -- each exactly as PRETABLE.out predicted, and the
split is the contract the probe header states: guest rows = reachability, survival, latch count, TEXT; differential
rows = preservation, expression, width.  M13 (teardown moved before the observation) was NOT built: the sites
implementation observes `dead` inside run_arm before the teardown code by construction; recorded as a harness-reorder
mutant owed to pass 2's review, not measured.

Logs: `regress/artifacts/fbd5/killtable_20260919/` (sites_*.log, diff_*.log, witness/drain logs, build logs, the
frozen instruments, TABLE2.log, PRETABLE.out); table 1 under `table1_instrumentdefect/`.  Propagation:
`propagate545.out` -- build/ d19184ee (== the FIX binary above), build-asan/ 0c1fd857, /tmp/gxsec-build c9b4340a, all
part 1 CLEAN + part 2 FRESH; est/ source CLEAN, part 2 N/A.
