# `#567` gate 16 run IN SITU -- F2's G4 (2026-10-19 07:30:37-07:31:35)

**What was owed.**  F2's three seats (GPT-6 Astra, Grok 4.7, GLM 5.3) all named it: the offline replay sourced the
block's lines with a stub `check()` and an injected `fcrc`, so the launch line, `lib.sh`'s real `check()`, the exit
status and `#549`'s probe running beside this one had never executed together.

**What ran.**  The real `regress/gate_mips_folds.sh` from the working tree (md5 `80462d1f85cdd5a6fcdf8b63fd265f67`), with
the 123-row probe (`regress/fbctrl_cmd_probe.py`, md5 `d1a69bb13488797b7c5103cc50b6d54d` -- table 4's frozen v4 with
its final header; its code AST-identical to `killtable4_20261019/probe.v4.frozen.py.txt`), `LOGDIR` in scratch, once
per binary, by `insitu_20261019/insitu567.sh`.  Clearance before the runs: `build/` part 1 and part 2 ok; `/tmp/gx566`
holds HEAD's `dev_fbctrl.c` and a binary newer than it.

| binary | how | gate rc | gate 16 | the `#567` block |
|---|---|---|---|---|
| `build/gxemul` (the fix) | the gate's DEFAULT `PMAX` | 0 | **PASS, 159 checks** | 133 checks, 0 red |
| `/tmp/gx566/gxemul` (HEAD) | `PMAX=` | 1 | **FAIL, 75 of 159** | 133 checks, **75 red** -- every red check in the gate is this block's |

On HEAD's binary `#549`'s block stays green (HEAD carries `#549`) and the fold rows read 14/14, so the gate's failure
is attributable to this block alone; its reds are the probe's exit status, the score, the failed-row count and 72
named rows (`ref 3 alive  got=DIED/1` first).  Both gate logs, both probe logs and `#549`'s probe logs are in
`insitu_20261019/` (completion lines present: `INSITU_DONE`; each probe log ends `FBCMD_DONE`).

**So G4 is discharged**: the launch line runs the shipped probe on the default binary, `check()` grades it, the exit
status propagates (rc 0 / rc 1), and the two device probes coexist in one run of gate 16.

**Re-run after pass 3 (08:07:21-08:08:18, `insitu41_20261019/`), with the block that ships** -- 125 names and pins,
after the owner's ruling added `edge x1` and `edge y1` -- and the probe as committed (md5 `7c34e8809f11f5d889542be73fb712f6`,
code AST-identical to `killtable4_20261019/legs41/probe.v41.frozen.py.txt`; gate md5 `6cef649b9b0452e56ed8b647c370ecd4`):

| binary | gate rc | gate 16 | the `#567` block |
|---|---|---|---|
| `build/gxemul` (the fix, default `PMAX`) | 0 | **PASS, 161 checks** | 135 checks, 0 red |
| `/tmp/gx566/gxemul` (HEAD) | 1 | **FAIL, 77 of 161** | 135 checks, 77 red -- again every red check in the gate |

Every probe log ends `FBCMD_DONE` (`#549`'s `FBCTRLP_DONE`) and the run log `INSITU_DONE`.

*After this run, and before the commit, only COMMENT text changed in both files, per pass 3's record findings (Grok
4.7): the `#567` block's header comment in `gate_mips_folds.sh` and the probe's docstring.  The probe's code was
re-checked AST-identical to `legs41/probe.v41.frozen.py.txt`; no check, pin or name in the block changed.  The
committed copies' md5s therefore differ from the ones above.*

The offline replay of the v4 block (123 names) on all 48 table-4 logs and five hand-made broken logs is
`GATE16_REPLAY_v4.out`: 133 checks green only on the fix; every mutant, both null media and all five broken logs red;
the block's own FCROW counts 123 rows in each of the 48 logs.
