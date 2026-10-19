
## 6. Questions -- answer each

1. **The premise audit.**  Each of these is load-bearing; tell me which is false, with evidence.
   * Every DATA value a guest can write at COMMAND reaches the compare as the FULL access value, ZERO-extended
     (`memory_readmax64(cpu, data, len)` for sb/sh/sw/sd), so `idata > 2` on `uint64_t` refuses everything except
     0, 1 and 2 at every width.  Is any access width or path able to present a value the compare misreads?
   * After the fix COMMAND can only ever hold 0, 1 or 2 (power-on 0 from `memset`; nothing else writes
     `port[DEV_FBCTRL_PORT_COMMAND]`; GET_RESOLUTION writes X1/Y1 only), so `fbctrl_command()`'s `default:` is
     unreachable and kept only as a tripwire.  Is there a writer I missed?
   * The read path is unchanged: a read of COMMAND returns the stored int, and a refused write never changes it.
   * `B_gateoff` (the gate removed) is HEAD's DATA arm byte for byte, so it is floor clause (b) -- and its 95 rows are
     row-for-row identical to the pre-fix leg.  Is the mutant really the removed defect, at every fixed site?
2. **The smallest edit that breaks this and still passes** -- name it, and the row you expect to stay green.
3. **Option-set completeness**: pass 1 settled member 3.  Is there evidence in THIS diff that changes that?
4. **The floor's clause (d), DEPENDS-ON.**  My enumeration of the predicates the fix depends on, each with its measured
   mutant: the port test (D9); the compare's width (D1), sign (E5), bound moved down (D2, D3, D4) and up (E1); the latch
   (D6 shared, D10 never set); the announce level (D7); the store order (D8); the dispatch's placement (E4); a width
   qualifier (D5).  Joint cells are disclosed, not rowed -- the latch SET crossed with a wide alias is the contract's
   NOT CLAIMED (0).  **Which predicate, or which cell of one, has no measured mutant?**
5. **CHANNEL.**  Two rows were found unable to vary under a named mutant: D4's NOP rows (masked, because D4 also refuses
   the GET that seeds those sessions -- E2 measures the NOP cell alone) and `ref w2 cmd` under D8 (w2 truncates to the
   previous COMMAND value, 2).  Is there a third?
6. **The gate block.**  Can any of its nine checks pass on a run that should fail?  It counts rows with one anchored
   pattern because this probe prints a row's status AFTER got/want.  (The replay above is my evidence; find its hole.)
7. **The census repair inside `#567`.**  Folding `#564`'s stranded pins into this round's diff, because the deriver will
   not write `#567`'s pins while they stand -- right, or should it be its own commit, landed first?
8. **WHICH OF MY ACCEPTED DISPOSITIONS IS WRONG?**  I accepted FIVE: (a) D4's two non-varying NOP rows are not a floor
   breach, because E2 measures that cell alone; (b) `ref w2 cmd` under D8 is not a breach, because ten classes and
   `two cmd` pin the store; (c) the 15 rows green on a dead binary are acceptable because the gate requires CONTROL=OK
   and pins the score by equality -- clause (c) MEASURED at `killtable1_20261018/C_absent.raw` and `C_bintrue.raw`;
   (d) grandfathering `sgi_mte_decline_probe.py` rather than converting it; (e) adding a second device probe to gate 16,
   a CPU gate, compounding the recorded `gatedevicesplit` debt.  Be harder on any of these that you would have argued for.

If, while verifying a claim, you found something ELSE -- say so.

**Answer format:** open with your token, then ONE line `VERDICT: SHIP | SHIP WITH CHANGES | DO NOT SHIP -- <one line>`,
then `FLAG:` lines for any false premise (with evidence: a grep anchor or a construct name), then answers to 1-8.
