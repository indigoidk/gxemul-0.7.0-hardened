#!/usr/bin/env python3
"""lanes46.py NLANES -- split the 92 replay specs into NLANES balanced lane scripts (lane_<i>.sh) and one driver
(replay_all46.sh) that runs them concurrently and waits.  FULL entries re-run every matching session, including
S38 (`rearm *') and S52 (`latch *'); the others serve S38/S52 from the capture BY DECLARATION (REPLAY_FROMCACHE),
on the derivation that those two sessions' rows -- two announce counts, a RAM trip and the CONTROL-text count --
cannot move under a silent decline of an access that prints no CONTROL text.  The FULL set is every entry whose
disposition rests on S38/S52: the EQUIVALENT candidates, the host-only candidate and the text-printing CONTROL
writes.  Sentinel: LANES46_DONE."""
import os, re, sys

N = int(sys.argv[1])
HERE = os.path.dirname(os.path.abspath(__file__))
SPW = "/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46"
FULL = {1, 3, 4, 8, 10, 11, 12, 13, 14, 15, 16, 17, 40, 43, 44}
COST = {38: 667, 52: 387}

specs = [l.split() for l in open(os.path.join(HERE, "specs46.out")) if not l.startswith("SPECS46")]
plans = [l.split() for l in open(os.path.join(HERE, "plan46.out")) if l.startswith("PLAN ")]
assert len(specs) == len(plans) == 92
jobs = []
for (k, lt, spec, _lbl), p in zip(specs, plans):
    assert p[1] == spec, (spec, p)
    sess = [int(s.split(":")[0][1:]) for s in p[2].split("=", 1)[1].split(",")]
    cmds = int(p[3].split("=")[1])
    full = int(k) in FULL
    if not full:
        cmds -= sum(COST[s] for s in sess if s in COST)
    jobs.append((cmds, int(k), lt, spec, full))
jobs.sort(reverse=True)
lanes = [[] for _ in range(N)]
load = [0] * N
for j in jobs:
    i = load.index(min(load))
    lanes[i].append(j)
    load[i] += j[0]
for i, L in enumerate(lanes):
    with open(os.path.join(HERE, "lane_%d.sh" % i), "w", newline="\n") as f:
        f.write("#!/bin/bash\ncd /tmp\nP=%s/r17.2fe7123b.py\nR=%s/replay46.frozen.py\n" % (SPW, SPW))
        f.write("B=/tmp/gxopus_acc46_bins/envmut\nK=/tmp/gxopus_acc46_cache.pkl\n")
        for cmds, k, lt, spec, full in L:
            fc = "" if full else "REPLAY_FROMCACHE=38,52 "
            f.write("%spython3 -u $R replay $P $B $K k%02d%s '%s' > %s/runs/k%02d%s.raw 2>&1\n"
                    % (fc, k, lt, spec, SPW, k, lt))
            f.write("echo \"k%02d%s rc=$? $(date '+%%T') $(grep -h '^CRIMEP_RESULT' %s/runs/k%02d%s.raw)\"\n"
                    % (k, lt, SPW, k, lt))
        f.write("echo LANE_%d_DONE\n" % i)
    print("lane %d: %d specs, ~%d cmds (~%.0f min)" % (i, len(L), load[i], load[i] * 0.25 / 60))
with open(os.path.join(HERE, "replay_all46.sh"), "w", newline="\n") as f:
    f.write("#!/bin/bash\n#  the four replay lanes, concurrently; waits for all.  Frozen copies of the driver.\n")
    f.write("cp %s/replay46.py %s/replay46.frozen.py\n" % (SPW, SPW))
    f.write("md5sum %s/replay46.frozen.py %s/r17.2fe7123b.py /tmp/gxopus_acc46_bins/envmut "
            "/tmp/gxopus_acc46_cache.pkl > %s/runs/replay.md5\n" % (SPW, SPW, SPW))
    f.write("echo \"REPLAY_ALL_START $(date '+%F %T')\"\n")
    for i in range(N):
        f.write("cp %s/lane_%d.sh %s/lane_%d.run.sh\n" % (SPW, i, SPW, i))
        f.write("bash %s/lane_%d.run.sh > %s/runs/lane_%d.log 2>&1 &\n" % (SPW, i, SPW, i))
    f.write("wait\necho \"REPLAY_ALL_DONE $(date '+%F %T')\"\n")
    f.write("cat %s/runs/lane_*.log\n" % SPW)
print("LANES46_DONE")
