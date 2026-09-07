# TABLE P8 (Opus 5 measuring seat, #502 pass 8) -- MEASURED
Clone `/tmp/gxopus502p8` (a `cp -a` of the idle table-11 clone, baseline `cmp`-verified against the GXEMUL-SEC
working copy = HEAD 83df95c + the uncommitted #502 fix, md5 3593a8a5).  Instrument: the SHIPPED
`regress/m88k_exc_probe.py` v15, md5 eb11ab7c, frozen as `m88k_exc_probe.frozenP8.py` before mutant 1 and
UNMODIFIED.  Driver frozen as `driver_p8.run-151805.sh`.  Every score below is in a named log in
`killtable_opus_p8/`.  Predictions were written in `PRETABLE_OPUS_P8_m88kexc.out` at **15:13:15**, before the
first build (the file's mtime is the order proof).  **8 predictions, 8 hits.**

| step | exact edit | predicted | MEASURED | red rows | log |
|---|---|---|---|---|---|
| BASE | (none) | 46/46 | **46/46** | -- | `BASE.out` |
| CENSUS | `fatal("[ M88KCENSUS ...]")` at function entry | 46/46 (non-perturbing) | **46/46** | -- | `CENSUS.out`, `CENSUS_cells.txt` |
| **M_DIV0IND** | `case ILLEGAL_INTEGER_DIVIDE: implemented = (PSR & M88K_PSR_IND) != 0` | **46/46 SWEEP** | **46/46 SWEEP** | **NONE -- row-for-row identical to BASE** | `M_DIV0IND.out` |
| **M_ERRNOC** | `case ERROR: implemented = !(PSR & M88K_PSR_C)` | **46/46 SWEEP** | **46/46 SWEEP** | **NONE** | `M_ERRNOC.out` |
| **M_BNDIND** | `case BOUNDS_CHECK_VIOLATION: implemented = (PSR & M88K_PSR_IND) != 0` | **46/46 SWEEP** | **46/46 SWEEP** | **NONE** | `M_BNDIND.out` |
| CTL_DIV0INDINV | `case ILLEGAL_INTEGER_DIVIDE: implemented = !(PSR & M88K_PSR_IND)` | KILLED | **23/46** | 23 (div0, dslot, div0tb, udiv0, error, all 11 trapfrozen*, all 6 err*, sfu1h) | `CTL_DIV0INDINV.out` |
| CTL_OVFNOC | `case INTEGER_OVERFLOW: implemented = !(PSR & M88K_PSR_C)` | KILLED, red `ovfc` | **45/46** | `ovfc` HALT | `CTL_OVFNOC.out` |
| CTL_DIV0SFD1 | `case ILLEGAL_INTEGER_DIVIDE: implemented = !(PSR & M88K_PSR_SFD1)` | KILLED, red `trapfrozen8` | **45/46** | `trapfrozen8` HALT | `CTL_DIV0SFD1.out` |
| BASE_final | restored | 46/46 | **46/46** | -- | `BASE_final.out` |

`clone cmp CLEAN vs baseline; clone clean: no sentinel; KILLTABLE_P8_DONE 15:44:18`.

## WHY THE THREE SWEEPS ARE BLINDNESS AND NOT AN INERT EDIT
`CTL_DIV0INDINV` is the **polarity twin of M_DIV0IND at the same arm, the same bit, one token apart** -- and it
reds 23 of 46 rows.  So the DIV0 arm is emphatically on the instrument's path and the mutator's edit reaches the
binary; the 46/46 of M_DIV0IND is a property of the ROW SET, not of the apparatus.  The mutator additionally
treats MUTANT-TEXT-NOT-FOUND as a hard FAIL (anchored on the case label plus its own `debugmsg_cpu` line, exactly
one match required), and each build was gated on `[ binary -nt source ]`.

## WHAT EACH SWEEP COSTS IN THE PRODUCT
* **M_DIV0IND** -- a guest divide-by-zero taken with **interrupts ENABLED** stops every emulated CPU.  IND clear
  is the normal state of running kernel and user code; the probe never exercises it at this arm because every
  DIV0 row starts from reset (PSR 0x80000002 = MODE|IND) or from inside a frozen handler.  **This is exactly the
  defect #502 exists to remove, restored for the majority of real guest states, behind one token, scoring 46/46.**
* **M_ERRNOC** -- a supervisor `tb1 0,rX,10` with the carry bit set stops every CPU.
* **M_BNDIND** -- a supervisor `tb1 0,rX,7` with interrupts enabled stops every CPU.

## THE TWO CONTROLS REFUTE TWO SENTENCES OF THE SHIPPED CONTRACT
The probe v15 docstring says the disclosed debt "stands for the other arms (OVERFLOW, DIV0, PRIVILEGE,
UNIMPLEMENTED) x {C, IND} and for {any arm} x {SFD1}".
* `CTL_OVFNOC` **45/46, red `ovfc`**: OVERFLOW x {C} is CLOSED.  (`indclr` closes OVERFLOW x {IND} the same way.)
* `CTL_DIV0SFD1` **45/46, red `trapfrozen8`**: {arm} x {SFD1} is CLOSED -- at every one of the seven arms, per the
  census.
* and the sentence names four arms, omitting **BOUNDS and ERROR**, which `M_BNDIND` and `M_ERRNOC` measure OPEN.

## CONTENTION
The #503 luna88k table (`/tmp/gxlunaabs_kill`, killtable5) ran concurrently throughout; builds were capped at
`-j2` for that reason.  No row in this table produced an unexpected STOP or NOBOOT, so nothing here needed a
solo re-run.  The one failure that did occur (table run 1, aborted at the census build) was a quoting bug in my
own mutator, reproducible off-line -- recorded in `PRETABLE_OPUS_P8_ADDENDUM1.out`, and explicitly NOT the
contention.
