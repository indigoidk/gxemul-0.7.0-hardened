# J7 -- three small filed rows on shipped probes and one device: check each premise and choose a disposition

## READING SCOPE AND FORM

The tree under review is `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\` (git HEAD cdbe7d7).  Pristine 2021 copies of GXemul
under the project root (`./src/`, `_archive/`) are NOT this fork.  Do not read `regress/artifacts/`, the ledger, the
CHANGELOG or OUTSTANDING_BUGS.  Read-only: no edits, builds or runs.  VERDICT LINE FIRST.  Mark claims READ
(file:line), REASONED or NOT CHECKED; counts carry denominators.  Each row below states its premise; check it.

## ROW 1 -- `pcc2c040debugchan` (LOW), `regress/pcc2_c040_probe.py`, `src/devices/dev_pcc2.c`

Premise: every C040 write in the probe runs under the debugger's `step`, and under `step` the fork's `debug()`
prints as well as `fatal()` (see `src/core/debugmsg.c`: `debug()` returns early when `(quiet_mode && !ss) || v < 0`,
where `ss` is single-stepping; `fatal()` has no early-out).  So a model edit that downgrades the C040 announce from
`fatal()` to `debug()` is invisible to all 18 rows (measured 17/17 on a mutant), although under free-running or `-q`
the announce would vanish.  Proposed: ONE free-running C040 write (breakpoint + `continue`, the shape
`regress/sh_intprio_probe.py` uses) whose transcript must carry the announce.
  Q: cite the debugmsg.c lines and the probe's session shape (step vs continue).  Is the premise right?  Would a
  free-running arm on this machine (`-E mvme88k -e mvme187`) reach the C040 write without a host-timer dependency
  (this probe's writes are synchronous guest stores -- confirm)?  What is the smallest addition (one arm, its
  breakpoint, its expected transcript line), and does the existing announce-count oracle then need an `-q`
  variant too?  Disposition.

## ROW 2 -- `pcc2c040latchswap` (MED), same files

Premise: the C040 announce is latched on a per-device bit `PCC2_W_GENCTL_LEN` in `d->warned`; the row `c040
predirty` pre-sets ONLY that bit before the write.  A model edit that keys the latch on a DIFFERENT warned bit
(e.g. `MASK_LEN`) passes all rows (measured 17/17); and since ordinary guest MASK traffic sets `MASK_LEN`, a halfword
store to MASK would then silence the C040 announce for the rest of the run -- a reachable hazard.  Proposed: pre-set
EVERY other warned bit (or `MASK_LEN` specifically) before the C040 write, so a swapped bit is caught.
  Q: enumerate `d->warned` bits and every site that sets each (grep `warned |=`), with lines; which are set by
  ordinary guest traffic vs only by error paths.  Does pre-setting ALL other bits before the C040 write change any
  existing row's result?  Is "pre-set MASK_LEN only" sufficient, or does the hazard exist for every bit set by
  benign traffic (count them)?  Disposition and the row's exact expected observation.

## ROW 3 -- `landiskauxorder` (LOW), `src/devices/dev_wdc.c`

Premise: #533 added a `case MACHINE_LANDISK:` to the aux-register address selection in `dev_wdc.c` and it landed
LAST, after `MACHINE_IQ80321`, so IQ80321's `break` is now load-bearing: deleting it would send IQ80321's aux
register to landisk's offset (+0x2c).  No row covers IQ80321.  Two options: move the landisk case ABOVE IQ80321
(then a dropped break falls onto landisk's own break, which an existing mutant already kills), or add an IQ80321
construction row.  Constraint: #533 is shipped and closed; this ships under its own number.
  Q: cite the switch and every case with its break; confirm the ordering claim.  Does any gate or probe construct
  an IQ80321 machine today (grep `iq80321` in regress/ and src/machines/)?  Which option is cheaper and which is
  sounder, and is there a third (a `default:` that fails loudly)?  Disposition.

**Standing licence:** anything else found in these files.
