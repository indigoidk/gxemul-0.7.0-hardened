VERDICT: 29 of 30 dispositions kept as written, 1 changed.

First-hand engineering re-review of fable_batch1a.md (HEAD 8ea26abb), read as a plain correctness review of the emulator source. Severity scale as instructed: HIGH = the emulator process terminates or memory use leaves a buffer's bounds; MED = guest-visible behaviour differs from the hardware manual; LOW = records, diagnostics, test coverage.

CHANGED
devsh4:F1 | was CONFIRMED-NEW LOW sh4tmupending | now CONFIRMED-NEW MED sh4tmupending | src/devices/dev_sh4.c:527 (`timer_interrupts_pending[i]++`, unsaturated), :604-607 (DEVICE_TICK re-asserts and re-sets TCR_UNF while pending > 0, with no test of tstr), :2148-2151 (one TCR ack decrements by one). Two underflows before one acknowledgment yield two delivered interrupts, and a stopped timer with residual pending keeps re-asserting; the manual (sh7750_hardware.txt:20741-20755, :21037) defines UNF as a single status bit cleared by writing 0. That is guest-visible behaviour differing from the manual, so MED on the scale regardless of the in-comment note at :518-525 that the queue-vs-coalesce choice was "recorded rather than decided." The signed-overflow half (~226 days) stays latent and does not change the grade.

KEPT (29)
devwdc: F1 wdcpktstatus, F2 wdcbeoddtail, F3 wdcresetirq, F4 wdcsrstnoedge, F5 wdcaltdecode, F6 CONFIRMED-NEW MED wdcnien, F7 wdccylwrap, F8 RECORD-L4, F9 RECORD-L4, F10 RECORD-L4, F11 UNSETTLED, F12 RECORD-L4.
devdreamcastgdrom: F1 CONFIRMED-NEW HIGH gdromdmareentr, F2 RECORD-L4 (minor), F3 RECORD-L4, F4 RECORD-L4 (minor), F5 RECORD-L4, F6 RECORD-L4, F7 RECORD-L4, F8 RECORD-L4, F9 CONFIRMED-FILED.
devsh4: F2 RECORD-L4, F3 RECORD-L4, F4 RECORD-L4, F5 RECORD-L4, F6 UNSETTLED, F7 TEST-GAP-FILE sh4chcrdualdiag, F8 CONFIRMED-FILED M1_sh4latchleak, F9 CONFIRMED-FILED pcicmergeA.

Severity spot-checks on the kept new rows, first-hand:
- gdrom:F1 HIGH holds. dev_dreamcast_gdrom.c:1502-1503 writes d->data to a guest-chosen dst via memory_rw(PHYSICAL); with dst inside the device's own DMA window at +0x18, memory_rw.c:480/587 dispatches back into the same handler, the arming words (+0x0c, +0x14) and d->data are unchanged, and the call repeats without bound. Unbounded recursion terminates the process. No in-flight guard exists.
- wdc:F6 MED holds. nIEN is never read; INTRQ is asserted with nIEN set, contrary to ATA-2 :1311-1314. Guest-visible, not a bounds or termination issue.
- gdrom:F2 and F4 are kept as L4 but are the two weakest rulings in the file (precision of comment wording, not behaviour); I would not object to either being dropped by the confirming seat.

THE TWO L2 OBLIGATIONS -- are their rows absent from the committed probes at HEAD?
- M2_gdromnodatawidth: YES, absent.
  grep: `git grep -n -E 'row\("(nodata byte|accept byte)"' HEAD -- 'regress/*.py' 'regress/*.sh'` -> no match (rc=1). The only hits in all of regress/ are
  `HEAD:regress/artifacts/stateaudit_20260923/diffs/regress_gdrom_default_probe.py.diff:210` and `:294` -- a diff artifact of uncommitted work, not the live probe. The committed gdrom_default_probe.py has only `arm bytetrig` (:1096), which drives the arming arm, not the no-data completion arm.
- M1_sh4latchleak: YES, absent.
  Committed sh4_chcr_probe.py:572-574 drives X4a (channel 1) and X4b (channel 7) with `wr(addr, x, ...)` -- a single store each -- and `grep -n -E 'two_stores\(.*(SH4_CHCR1|SH4_CHCR7)'` returns nothing (rc=1). Only X3 (:550) repeats a request, on channel 0. The (1,set) and (7,set) cells named at CHANGELOG:2903 have no row.
Both were graded L2 in the CHANGELOG (#496 pass, :2896-2909), i.e. repair-in-round, and neither repair is in committed HEAD. That is an undischarged obligation, not a test-gap, and should be surfaced as such.
