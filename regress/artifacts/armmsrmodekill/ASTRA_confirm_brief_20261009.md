# #562 armmsrmodekill -- GPT-6 Astra CONFIRMATION of the final package before the local commit

Open with `VERDICT: CONFIRM / CONFIRM WITH CHANGES (<n>) / DO NOT CONFIRM` (verdict line first).  READ-ONLY: write
nothing, build nothing, run nothing.  Tree under review: `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\` working tree (HEAD
`ef577140`); ignore any other `src/` under the project root, and ignore the other session's unrelated uncommitted
files (cpu_alpha_palcode.c, dev_lca.c, dev_pcc2.c, dev_sh4.c, mvme_pcctworeg.h, gate_sh_rounding.sh,
gdrom_default_probe.py, sh4_chcr_probe.py, and their ledger/wiring lines).

This is a RECORDS CHECK of a round whose code review is finished: please check every claim below against the evidence
it cites, and say which sentences are false or unsupported.  **Do not simply ratify** -- a correction is more useful
than agreement.  The owner ruled on 2026-10-09: commit the fix with the 47-row detector, narrow the contract
comment-only, file the measured residue.  Fable 5.1 is deliberately not fired; you are the confirming seat.

## What to check (files)

1. The draft CHANGELOG round block:
   `C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-cc-GXEMUL\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\c562\changelog_block.md`
2. The draft OUTSTANDING_BUGS section (armusrstop, armspsrthumb, armmmuvehicle, armmsrmodedebt, headerstaleobj):
   `...\scratchpad\c562\bugs_section.md` (same directory)
3. The draft commit message: `...\scratchpad\c562\msg562.txt`
4. The probe as it will be committed, `GXEMUL-SEC\regress\arm_msrmode_probe.py` -- its module docstring (CONTRACT, NOT
   CLAIMED, tally).  The code is claimed AST-identical to the measured frozen probe
   `regress\artifacts\armmsrmodekill\killtable5_20261008\probe_frozen.py` (`SHIPPED_vs_FROZEN.txt` says how it was
   checked); please check that claim too (diff the two files: only the module docstring should differ).
5. The gate section appended to `GXEMUL-SEC\regress\gate_arm.sh` (search `#562 armmsrmodekill`), and
   `tools\precommit_check.sh`'s `SCORE_CLAIMS_MANIFEST=33`.
6. The ledger rows `armmsrmodekill`, `armusrstop`, `armspsrthumb`, `armmmuvehicle`, `armmsrmodedebt`,
   `headerstaleobj`, `armthumbabortkill` in `GXEMUL-SEC\tools\pipeline\ledger.json`.

## The evidence (all under `GXEMUL-SEC\regress\artifacts\armmsrmodekill\`)

witness_20261007/, killtable_20261007/, killtable2_20261007/, killtable3_20261008/, killtable4_20261008/,
killtable5_20261008/ (KILLTABLE5_lanes*.out, kt1..kt4b/, run_fixed.out, run_head.out, PRETABLE5.out with its appended
CORRECTIONS, SHIPPED_vs_FROZEN.txt), panel_pass1_20261007 .. panel_pass2r5_20261009/, opus_pass2*_2026100*/
(opus_pass2r5_20261009/opus_pass2r5.md and KTR5*.out are the final pass's measurements), gate14_20261009/
(gate14_run1.out, xscale_ab.out, cleanbuild.out, xscale_clean.out; gate14_run2.out lands when the second run finishes).

## The one finding of this round's gate that the records must state exactly

Gate 14's first run went red on the xscale section (28/30).  The records say the cause was a STALE `dev_i80321.o`:
#562 inserted `mode_warned` into `struct arm_cpu` ahead of the i80321 fields, the build tracks no header
dependencies, and every #562 build rebuilt only `src/cpus/*.o`.  Please check that account against
`src/include/cpu_arm.h` (field order), `src/devices/dev_i80321.c` (the only non-CPU object touching those fields --
check that "only" by grep), `src/include/cpu.h` (`cd` as the LAST member of `struct cpu`), and the A/B and clean-build
outputs.  Is any part of "the kill tables are unaffected" (the msrmode probe drives `-E testarm`, which attaches no
i80321) false?

## Questions -- `<n> | <answer>`
1. Which sentences in files 1-3 are false or unsupported by the cited evidence?  Quote each and give the fix.
2. Is the probe AST-identical to the measured frozen probe, docstring aside?
3. Is the stale-object account (and its scope) correct and complete?
4. Anything the records omit that a reader of the commit would need?
**If you found something ELSE -- say so.**
