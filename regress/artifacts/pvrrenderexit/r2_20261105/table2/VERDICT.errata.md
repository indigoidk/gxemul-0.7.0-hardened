# ERRATA / ADDENDA to table2/VERDICT.md -- dated 2026-11-05 (repair 3)

VERDICT.md is a measurement record and is NOT rewritten.  Its scores stand.  Two things it says or implies need a correction and an
addendum, both found while measuring codex's pass-3 cells (`../../r3_20261105/PVR3_NOTE.md`, "THE STDIN CAP").

## 1. The cause of the "16-command mask session" timeout

> "the first base run timed out a 16-command mask session, split in two: base68/SPLIT_NOTE.md"

True as a description; the implied cause -- a session too long for the probe's 90 s limit -- is wrong, and it travelled: the probe
docstring said such a session "outran the 90 s session limit", and repair 3's brief said "keep each session to about 8 [TA commands]".
**The cause is a 4100-byte cap on a session's debugger input.**  Sessions run in tens of milliseconds; the first `step 1` of each
session (at byte 100 of its input) runs the Dreamcast maple keyboard's tick for the first time, and that tick reads whatever stdin
the debugger's 4096-byte console FIFO has not yet taken -- everything past byte 4100 -- as key presses.  The 16-command mask session
sent 6088 bytes; its transcript stops after ~4100 bytes of input, mid-`step`, and the session waited for the timeout.  Measured:
`../../r3_20261105/stdin_cap_test.out` (`reg`-only input of any length is safe) and `stdin_cap_test2.out` (with `step`, 4100 bytes exit
0 and 4150 bytes TIMEOUT at exactly 349 prompts; moving the first step 1500 bytes later moves the cut by the same amount).

## 2. Addendum: every table-2 leg on a gxemul binary waited out one 90 s timeout

`texyedges` sent 4104 bytes, four past the cap, so its `quit` arrived as `q` and the session ended by TIMEOUT on every leg run against
a gxemul binary -- base, HEAD, 61 of the 62 variants, restored (`sessions_*/texyedges.txt`: `--- transcript (TIMEOUT) ---`) -- the one
exception being Y2t, whose texyedges session died by SIGSEGV first (`--- transcript (sig11) ---`: its undefined behaviour, NOT
PREDICTED; `probe_Y2t_tex_ltm1.out` elapsed 1.4 s).  Every other gxemul leg therefore took ~90.5 s (`probe_*.out`; table 1's 51-row
probe took 0.4 s).  **The scores are unaffected**: all six
texyedges pixel reads come before the cut, so each texyedges row read a real pixel, and no table-2 red set depends on the hang.  The
repair-3 probe stores only the red texel texyedges samples (4060 bytes) and refuses any session past 4096 bytes before running it.

## Not in this file

Codex's pass-3 records a-e are corrected in the probe docstring, in `../PRETABLE_2.errata.md` (c, e) and in the gate text
(`../../r3_20261105/gate_pvr_block.new`, b).  VERDICT.md's own wording of the PRETABLE order ("the only older file here is the frozen
probe, copied first") is the CORRECT form of record c.
