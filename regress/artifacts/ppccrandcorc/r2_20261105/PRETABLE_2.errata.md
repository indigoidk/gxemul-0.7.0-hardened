# PRETABLE_2.out -- errata (2026-11-05, round 3; pass 3 = ../p3_20261105/codex_codex_r575_p3.txt)

PRETABLE_2.out is the prediction record written before table 2 and is not rewritten.  The item quotes what it corrects.

## R6 -- the control session's seed in the manifest is a simulator placeholder, not the probe's seed

PRETABLE_2.out, ROW MANIFEST:

>   ctl              seed=0x00000000  (apparatus)

The executed probe seeds its control session with CTL_CR = 0x12345678 (regress/ppc_crlogic_probe.py, `CTL_CR = 0x12345678`, the
`ctl cr seed' and `ctl mfcr' rows want 0x12345678).  The simulator v575b.py yielded the ctl session with a placeholder seed of 0
because no prediction reads it: the six ctl rows are apparatus rows, predicted green unconditionally.  No prediction in PRETABLE_2
depends on the value.  r3_20261105/v575c.py carries the real CTL_CR and r3_20261105/PRETABLE_3.out prints it.
