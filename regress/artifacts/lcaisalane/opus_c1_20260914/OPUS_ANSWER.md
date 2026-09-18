# #530 CLOSING PASS 1 (on the pass-2 repair) -- the Opus 5 seat (Agent tool, measuring)

*** TRANSCRIBED BY THE MAIN LOOP (Agent seats leave no file).  Verdict and table VERBATIM in substance; the main loop
re-read logs/probe_{c1_w2,c1_w1w,c1_r4,p_port10}.raw (each `LCAISALANE_RESULT=51/51') and logs/disc_c1_*.out before
recording. ***

Liveness `OPUS_SEAT_ALIVE_20260914_LCA530_C1`; CHECKPOINT line 1 quoted verbatim.

## VERDICT: GAP -- `byte = data[ofs];` -> `byte = data[ofs == 2? 0 : ofs];` (write arm) scores 51/51 and changes a
## guest-visible outcome (an `stl` to a port 2 mod 4 forwards data[0] instead of data[2]).  MEASURED.
The seat's severity qualifier, recorded as given: clause-(e) COVERAGE DEBT, not a floor breach -- the write body never
tests `ofs' against a constant; every clause-(d) mutant of the position rule is killed.  But the 51-row set does not
cover the invariant its top line states ("(P & 3) % len on BOTH arms"): three one-cell edits escape.

| mutant | edit to the FIXED dev_lca.c | 51-row | discriminator base -> mutant | disposition |
|---|---|---|---|---|
| c1_w2 | write `byte = data[ofs == 2? 0 : ofs];` | 51/51 | d_msr 0xb2 -> 0xf4 (stl -> MSR forwards data[0]) | write lane 2 (len >= 3) unrowed |
| c1_w1w | write `byte = data[(ofs == 1 && len > 2)? 0 : ofs];` | 51/51 | d_ier 0x33 -> 0x44 (stl -> IER forwards data[0]) | write lane 1 at len >= 4 unrowed |
| c1_r4 | read `data[i] = (i == ofs \|\| (len == 4 && ofs >= 2 && i == 0))? byte : 0x00;` | 51/51 | d_scr 0x5a000000 -> 0x5a00005a (ldl SCR full reg) | no full-register len-4 read at ofs >= 2 (`ofs2/ofs3 wide' are single-lane masks) |
| p_port10 | `relative_addr &= 0x3ff;` (disclosed) | 51/51 | -- | correctly disclosed; escapes |

Cheapest closure: a write at (4,2), one at (4,1), a full-register read at (4,3) -- three rows, no new session.

## Q2
Every enumerated catch-list item has a killing mutant with a varying channel; no vacuous kill-claiming row.  But the
catch-list is narrower than the invariant the header states (write lanes 1-2 at len 4/8; the full len-4 read at ofs >= 2).

## Q3 -- wrong statements
1. POSTTABLE 2 "SOLE CARRIERS ... ld4 full for p_rep4 (with ld4 lane0)" -- self-contradictory; two carriers.
2. The p_port10 disclosure's premise "every probed port is below 0x400" -- the split TAILS are at 0x400 (the conclusion
   holds; measured 51/51).
3. The header's "a lane decode ... on the read arm or the write arm" is true only for the bit-1/`& 3' forms rowed.
4. (minor) POSTTABLE's "(c) the pre-fix file as the stale medium" mislabels clause (c).
5. (aside) the pass-2 prose "Nine of eleven ... eight change" disagrees with its own table; "ten ... nine" is right.

## Clone
/tmp/gxopus530c1 restored (cmp-clean, no .MUTANT, fresh, restored == base); GXEMUL-SEC dev_lca.c unchanged.
