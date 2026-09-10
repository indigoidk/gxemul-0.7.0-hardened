#!/bin/bash
# launch.asrun.sh -- TABLE 3 launcher, PRESERVED IN ITS OWN TABLE DIRECTORY.
#
# Table 1's launcher was overwritten in place by table 2's, which destroyed the
# only copy of the sentence explaining why each table needs its own output dir.
# So every table now keeps its own launcher, probe and mutator beside its logs,
# and the top-level copies are working files rather than the record.
#
# WHY EACH TABLE GETS ITS OWN OUTPUT DIR: the driver writes probe_<leg>.raw and
# reuses those names on every run.  A record citing them stays true only until
# the next table runs, and then the named log says something ELSE -- the claim
# does not become unverifiable, it becomes contradicted by its own evidence.
#
# The wrapper exists because `wsl -- bash -c '<string>'` does not deliver shell
# variables to the inner shell, even inside single quotes; a script file does.
KT=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/alphatbinegsel/killtable_20260910
exec bash /tmp/gx520run/killtable.run.sh \
    "$KT/t3" \
    "$KT/t3/alpha_tbi_probe.frozen.py" \
    "$KT/head_cpu_alpha_palcode.c" \
    "$KT/t3/mutate.asrun.py"
