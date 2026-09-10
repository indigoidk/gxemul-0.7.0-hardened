#!/bin/bash
# launch.sh -- wrapper so the kill table runs from a SCRIPT FILE rather than
# through `wsl -- bash -c '<string>'`, which does not deliver shell variables
# to the inner shell even inside single quotes.
#
# TABLE 2: the 13-row closed detector.  Output goes to t2/ so table 1's logs
# in t1/ are never overwritten -- a citation into a reused log name decays
# silently, and t1's numbers are cited in this round's record.
KT=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/alphatbinegsel/killtable_20260910
exec bash /tmp/gx520run/killtable.run.sh \
    "$KT/t2" \
    "$KT/t2/alpha_tbi_probe.frozen.py" \
    "$KT/head_cpu_alpha_palcode.c" \
    "$KT/t2/mutate.asrun.py"
