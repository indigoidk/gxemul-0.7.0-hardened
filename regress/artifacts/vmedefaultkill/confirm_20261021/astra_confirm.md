ASTRA seat -- a RECORDS CONFIRMATION before a commit (ordinary documentation-accuracy review; nothing to build, nothing
to run but read-only file and git-read commands).  READ-ONLY: write nothing to any project tree.

A commit unit lands round #568 (an emulator's VME bus-controller model: a fix, its 38-row regression probe, gate wiring,
records).  Your job is to confirm the unit says what the measurements and the adjudication established -- no more, no
less -- before it is committed.  Open your answer with the token ASTRA_VME_CONFIRM_20261021, then ONE line:
VERDICT: CONFIRM | CONFIRM WITH CHANGES (n) | DO NOT COMMIT -- <one line>

Read, in this order:
1. The repair-diff pass's adjudication: C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/vmedefaultkill/r1_20261021/ADJUDICATION_R1.md
2. The commit message: C:/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/vme/commit/commit_msg.txt
3. The unit's changes against committed HEAD 86114a90: C:/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/vme/commit/confirm/unit_diff_text.patch (every unit file; the ledger as a JSON
   diff; matrix.html generated, not rendered) and C:/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/vme/commit/confirm/unit_new_files.txt (598 new artifact files).  The unit is
   C:/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/vme/commit/spec568.json; files marked `from: file' commit the staged copies under C:/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/vme/commit/staged/.
4. The evidence the records cite, all under C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/vmedefaultkill/: killtable2_20261021/ (KILLTABLE2_VS_PRETABLE2.out and the table2b,
   table2c, table2d addenda, each with its PRETABLE written first), gate_20261021/ (the clean-clone block runs
   mini3_PREFIX.out / mini3_FIX.out and the full run GATE14_FULL3.out), r1_20261021/ (every seat's answer and Argon's).

Deliberate decisions to RULE ON (ACCEPT / REVERT, with the reason):
  D1. Argon was re-sent with extended thinking OFF, against the owner's 2026-10-14 "thinking level High", after both #568
      jobs with it died at ~25 minutes ("connection lost while generating"); every extended-off job since 10-15 returned.
  D2. The frozen probe copies and table scripts are classed CLASS_RESEARCH in check_probe_wiring.py; three seats read the
      #471 comment as defining WITNESS -- `git blame' puts that comment with CLASS_RESEARCH (0a7c4687) and CLASS_WITNESS in
      85bc6ab4.
  D3. gate_hygiene.sh's EXPECT_PTY_PROBES 76 -> 77 counts another session's UNTRACKED lca_isaphys_probe.py, by the
      2026-09-23 owner ruling that the census counts what lies in the tree the weekly battery runs (75 committed + this
      probe + that one); the new probe is grandfathered as "promptless" although it does wait for the prompt (`in'/`find').
  D4. m88kpsrmxm is filed MED where pass 1 adjudicated LOW: reading cpu_m88k.c's PSR store shows a halt (cpu->running =
      false), not a silent divergence.
  D5. vmedefaultkill lands HELD for Fable 5.1's REGRESS review (FABLE-ONLY by standing directive), with its question in
      hold_question, rather than closed.
  D6. The rev-2 full gate (PASS 1264, on build/gxemul, which carried another session's uncommitted PCC2/LCA/SH4/Alpha edits)
      is recorded as superseded; the rev-3 gate ran on a clean clone of HEAD (PASS 1270).
  D7. PRETABLE2.out:72's incomplete prose ("the 20 population rows") is NOT edited -- its mtime is the order proof; the
      correction is appended to KILLTABLE2_VS_PRETABLE2.out and stated in the CHANGELOG.

Questions:
Q1. Does the unit implement ADJUDICATION_R1.md exactly -- every ACCEPTED records item applied, every FILED item filed, nothing
    the adjudication did not decide?  Cite the file and the diff line of any miss or excess.
Q2. Does any added or changed sentence (commit message, CHANGELOG block, OUTSTANDING_BUGS section, ledger notes and
    hold_question, MANIFEST descriptions, the probe's docstring changes, gate_hygiene.sh's note, precommit_check.sh's line)
    assert something its cited artifact does not support -- a score, a count, a timestamp, a "measured", a seat's verdict?
    Spot-check at least EIGHT citations against their files.
Q3. Rule on D1-D7.
Q4. Is any file this round changed MISSING from the unit, or does any unit file carry an edit that is NOT this round's?  The
    working tree also holds other sessions' uncommitted edits (src/devices/dev_pcc2.c, dev_lca.c, dev_sh4.c,
    src/cpus/cpu_alpha_palcode.c, mvme_pcctworeg.h, several regress/ probes and gate scripts, tools/*.md) -- they must NOT
    be in the unit.
Q5. Anything else.
