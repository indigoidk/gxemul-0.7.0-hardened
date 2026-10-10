# REGRESS review of #562 (`4f908ad5`, armmsrmodekill) -- the flagship-only stage

**Liveness, first two lines of your answer:** (1) `FABLE_SEAT_ALIVE_20261009_R562`; (2) the FIRST LINE of
`C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\CHECKPOINT.md`, verbatim.  Then
`VERDICT: REGRESS CLEAN / REGRESS WITH FINDINGS (<n>) / REGRESSION FOUND -- <one line>`.

You adjudicated #562's nine rulings this afternoon (`regress/artifacts/armmsrmodekill/fable_adjudication_20261009/`).
It is now COMMITTED, locally, as `4f908ad5` (parent `04f3e7c0`, whose four ARM sources are identical to `ef577140`'s).
This project reserves the REGRESS stage of a closed row to the flagship seat.  The question is the standard one, asked
of what actually landed rather than of the working tree you reviewed:

1. **Does the committed detector still discriminate?**  Build the PARENT (`04f3e7c0`) and the COMMIT (`4f908ad5`) in
   your OWN WSL scratch clone (`git -C C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC archive <sha>` into `/tmp/...`; WSL Gentoo,
   `./configure`, `make`; check the binary is newer than `src/cpus/cpu_arm.c`), and run the COMMITTED
   `regress/arm_msrmode_probe.py` against each.  The records say the parent scores 18/47 with 29 named reds and the
   commit 47/47 (`regress/artifacts/armmsrmodekill/killtable5_20261008/run_head.out`, `run_fixed.out`).  Does that hold
   for the committed files, and is every red on the parent red for the reason its row names?
2. **Did anything land that the review did not see?**  `git show --stat 4f908ad5` against the package you adjudicated
   (`fable_adjudication_20261009/`): any file, hunk or record that differs from what you ruled on.  In particular the
   three corrections you asked for, the 59 seat-by-seat ledger entries added for #562's seven panels, and gate 14's
   section in `regress/gate_arm.sh`.
3. **Anything the gate would not catch** -- e.g. a row whose expected value no longer matches the committed probe's
   own docstring, or the `rows failed` grep you flagged.

READ-ONLY on every project tree (`GXEMUL-SEC`, `est`, `build`, `build-asan`, WSL `/tmp/gxsec-build`): no edits, no
`git add/commit/stash/checkout/reset`, no plain `git status` (use `git --no-optional-locks status`), no gates -- a
commit precheck may be running.  Separate what you READ from what you RAN.  **If you found something ELSE -- say so.**

Write your FULL answer to `C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-cc-GXEMUL\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\c562\fable\fable5_regress562.md`
and return it as your final message.
