# PREDICT2 -- #529 closing pass 7, Opus FINISHING seat (the first seat walled before its report).
# Written BEFORE building or running anything of mine.  This file's mtime is the order proof.
# Liveness: CRIME_CLOSE7_OPUS_20260916.

Instrument: scripts2/post7.py -- a PROTOTYPE of the proposed repair-13 rows ONLY, run standalone.  It is NOT
the shipped probe and the shipped probe is NOT edited.  Binaries: the predecessor's /tmp/gxopuscrimec7_bins.

## What post7.py rows (all POST = after ONE refused `lb +0x07', so d->warned & CRIME_W_LEN is SET)

P1 REV window    p revP sw/sd/ld/lw pc   want 0x80004000 (ra)          + p revP once = 1
P2 12-cell       p acc ctl ld 0x100, p acc istat ld BIT, p acc imask sw 0x1000000000000000,
                 p acc time sd odd, p acc 40 lw 0xa0b0c0d, p acc 40 sw 0xa0b0c0d00000000,
                 p acc ctl sd 1                                        + p acc once = 1
P3 istw          p istw pre clear, p istw sd set, p istw mid clear, p istw sw set
P4/P5 TIME 4B    p time 4w upd large, p time 4r upd large
P6 residue       p rev ld 0x11, p rev lw4 0x11, p dog ld <seed>, p dog rhi, p dog rlo,
                 p imask ld <seed>                                     + p resid once = 1
Total 23 rows.

## PREDICTIONS (score out of 23, and the failing row names)

| binary | predicted | reasoning |
|---|---|---|
| base           | **23/23** | every want is the shipped behaviour, read out of the handler; the POST prefix changes nothing on a correct build because the decline arm is reached only by width |
| K1_w_imask4w   | **22/23** {p acc imask sw} | INTMASK 4W silently declined once the latch is set: the sw never lands, the accepted ld +0x18 reads 0 |
| K2_w_rev4      | **21/23** {p revP sw pc, p revP lw pc} | REV 4-byte declined post-latch: the two 4-byte window accesses lose the redirect (pc = 0xbfc05184); sdP/ldP are 8-byte and unaffected |
| K3_w_ctl8r     | **22/23** {p acc ctl ld} | CONTROL 8R declined post-latch answers 0, not 0x100 |
| E2_byp_time4   | **21/23** {p time 4w upd, p time 4r upd} | the TIME 4-byte bypass skips crime_update_crime_time, and a read takes odata BEFORE its own update, so the following ld reads the stale small value.  Everything else untouched |
| E1_byp_ctl4r   | **23/23** | CONTROL 4R is not rowed here and is EQUIVALENT anyway (high half 0) |
| E3b_byp_revout_acc | **23/23** | it bypasses REV only OUTSIDE the window; `p rev ld' is an 8R from CODE, which E3b DOES bypass -> *** I predict `p rev ld' RED, 22/23.  Corrected before the run: E3b's condition is `len == 4 \|\| (len == 8 && MEM_WRITE)', so an 8R from code is NOT bypassed.  23/23. *** |
| F1_byp_ctl8w_0201 | **23/23** | `p acc ctl sd' writes 0x01, not 0x0201 |
| F3_byp_sw04    | **23/23** | it bypasses a 4W at +0x04; no row here writes there (`p rev lw4' is a READ) |

## The two claims the prototype is built to settle

1. **A POST prefix is sufficient.**  If base is 23/23 and K1/K2/K3/E2 each red exactly their own cell, then the
   whole K class closes by ONE structural change -- repeating the existing value checks once with the latch set --
   and no new channel has to be invented.
2. **The negative control matters as much.**  E1/E3b/F1/F3 must stay 23/23.  A prototype that reds them too would
   be measuring the POST prefix rather than the mutant.

## Row-count prediction for repair 13 (before measuring)

14 rows if only the three value sessions gain a POST twin (P1+P2+P3 = 4+7+4, minus the `once' controls folded into
existing ones), +2 for the TIME 4-byte update pair, +6 for the P6 residue = **~20-22 rows, 6 new sessions**.
I expect the measurement to let P6 shrink, because several of its cells are already pinned post-latch by
`imask keeps', `sb keeps', `lo keeps', `top*' and `mid keeps'.

## ADDENDUM -- written after lanes A and B, BEFORE post7b.  My `p time 4w/4r upd' rows were VACUOUS and this is the repair.

MEASURED: E2 scored 29/29 -- my two TIME rows did NOT fire.  Raw: base 0x10d49672 / 0x10d30928, E2 0x86c913c /
0x86a6a08.  The channel IS there (a factor of exactly 2) and my ORACLE could not see it: `mag()' thresholds at
66 x 100000 and both are far above it.

CAUSE (derived, then to be checked by the run below): the POST prefix's own `step' RUNS THE CPU, so `dev_crime_tick'
fires and calls crime_update_crime_time, which sets `d->last_microseconds'.  The "TIME is still 0" property that
disc7b's STEP rows relied on is destroyed by the refusal that makes the session POST.  After that every accepted TIME
access only ever "catches up", so skipping one halves the total instead of zeroing it.

THE CORRECTED SHAPE: put the refusal AND the three TIME accesses in ONE run, as the session's FIRST CPU execution, so
`last_microseconds' starts at 0 and the 4-byte access is the only thing that can move TIME before the final read.
Rows want a NONZERO MULTIPLE OF 66 (disc7 measured base 0xc6 = 3x66 and 0x108 = 4x66; E2 exactly 0x0, 12/12 over two
scripts).

post7b.py rows, both a FREE-RUNNING and a STEPPED variant of each:
  p t4w free, p t4r free, p t4w step, p t4r step   want `mult66'      + p t post once (notice count 1)

PREDICTIONS
| binary | predicted |
|---|---|
| base | **5/5** -- all four TIME reads a nonzero multiple of 66 |
| E2_byp_time4 | **1/5** {p t4w free, p t4r free, p t4w step, p t4r step} -- TIME never moves, every read 0x0 |
| K1_w_imask4w | **5/5** -- control: a mutant at another cell must not disturb these |

NAMED RISK: the STEPPED variant may read 0x0 ON BASE TOO (all four instructions inside one `step 4' can fall in one
microsecond, so `to_add' is 0 and no update happens).  If base reads 0 there, the stepped form is UNUSABLE and only the
free-running form survives; I am measuring both precisely because I cannot tell from reading.

## ADDENDUM 2 -- written after post7b, BEFORE post7c.  Both post7b shapes FAILED, in opposite ways.

MEASURED (logs2/post7b_*.out):
  FREE  one run [lb, ld, 4-byte, ld]   base 0x84 / 0x42   E2 0x0 / 0x0   K1 0xc6 / **0x0**
  STEP  one `step 4' of the same       base 0xfba / 0x1188  E2 0x8c4 / 0xa92   K1 0xce4 / 0xca2
* The STEPPED form is NON-DISCRIMINATING: E2 reads a nonzero multiple of 66 too, because the four instructions inside
  one `step 4' span tens of microseconds, so the FIRST ld's own update already moves TIME off 0.
* The FREE form DOES discriminate E2 (exactly 0x0, twice) but is FLAKY: `p t4r free' went RED on K1, a binary that
  does not touch TIME at all.  The four instructions can complete inside ONE microsecond, `to_add' is 0, TIME never
  moves, and a control binary reads 0 exactly as a bypass does.  A FALSE RED on a control, 1 of 4 free samples.

post7c: THE THIRD SHAPE.  Fuse the refusal and the first TIME read into the session's FIRST `step 2' (so TIME is still
~0 after it), then take the 4-byte access and the final read as SEPARATE `step 1' commands, so the debugger's own
~0.25 s gap guarantees a large `to_add' at the 4-byte access and at nothing else.
  p t4w gap, p t4r gap    want `large' (> 66 x 100000)

PREDICTIONS
| binary | p t4w gap | p t4r gap |
|---|---|---|
| base | large (~66 x 250000 = 1.6e7) | large |
| E2_byp_time4 | **small** (only the two steps' own tick contributions, hundreds) | **small** |
| K1_w_imask4w | large | large |
| K3_w_ctl8r | large | large |
Separation predicted ~10^5, against the free form's flaky 1-3 microseconds.  If base comes back SMALL, or a control
comes back SMALL, this shape is dead too and the honest answer is that TIME 4W/4R has no reliable post-latch row.
