#!/usr/bin/env python3
"""mk_driver_t2.py <kt568.sh> <out kt568t2.sh> -- table 2's driver = table 1's kt568.sh with its locations, md5 pins
and the 38/38 clearance changed; every replacement must match exactly the stated number of times."""
import io, sys
src = io.open(sys.argv[1], encoding="latin-1", newline="").read()
V = "/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/vme"
REPL = [
    ("# kt568.sh -- kill table 1 for #568 (vmedefaultkill).  Run under WSL Gentoo:",
     "# kt568t2.sh -- KILL TABLE 2 for #568 (vmedefaultkill): table 1's kt568.sh with its locations, md5 pins and the\n"
     "# 38-row clearance changed (fix568b, the frozen rev-3 probe, clone /tmp/gxkt568t2).  Run under WSL Gentoo:", 1),
    ("/killtable1/kt568.sh <subcommand> [args]", "/rev3/table2/kt568t2.sh <subcommand> [args]", 1),
    ("/tmp/gxkt568;", "/tmp/gxkt568t2;", 1),
    ("-> /tmp/gxkt568 (refuses", "-> /tmp/gxkt568t2 (refuses", 1),
    ("install dev_vme.fix568.c (md5 4e3e7fc2) -> BASE", "install dev_vme.fix568b.c (md5 beb120ea) -> BASE", 1),
    ("fix568 + the pristine machine_mvme88k.c back", "fix568b + the pristine machine_mvme88k.c back", 1),
    ("legs/BASE_FINAL.raw is 34/34 CONTROL=OK", "legs/BASE_FINAL.raw is 38/38 CONTROL=OK", 1),
    ("removes /tmp/gxkt568 ONLY", "removes /tmp/gxkt568t2 ONLY", 1),
    ("OUT=" + V + "/killtable1\n", "OUT=" + V + "/rev3/table2\n", 1),
    ("FIX=" + V + "/fix/dev_vme.fix568.c\nFIXMD5=4e3e7fc220062b429f7d9d6e140fec9e",
     "FIX=" + V + "/rev3/dev_vme.fix568b.c\nFIXMD5=beb120eae1be112b682bd528f103191c", 1),
    ("MACHREF=$OUT/ref/machine_mvme88k.head.c", "MACHREF=" + V + "/killtable1/ref/machine_mvme88k.head.c", 1),
    ("PROBE=$OUT/vme_default_probe.frozen.py\nPROBEMD5=19de15b3ea69af28e437cdf92e22c97e",
     "PROBE=" + V + "/rev3/vme_default_probe.rev3.frozen.py\nPROBEMD5=ddcebfe3257d3370f3c16b0bee79a4be", 1),
    ("W=/tmp/gxkt568\n", "W=/tmp/gxkt568t2\n", 1),
    ("= dev_vme.fix568.c (md5 $FIXMD5) over HEAD", "= dev_vme.fix568b.c (md5 $FIXMD5) over HEAD", 1),
    ("a one-edit variant of fix568 -- restore with kt568.sh restore", "a one-edit variant of fix568b -- restore with rev3/table2/kt568t2.sh restore", 1),
    ("$VME = fix568 -- restore with kt568.sh restore", "$VME = fix568b -- restore with rev3/table2/kt568t2.sh restore", 1),
    ("$VME <- dev_vme.fix568.c, $MACH", "$VME <- dev_vme.fix568b.c, $MACH", 1),
    ("dev_vme.c cmp vs fix568=$c1", "dev_vme.c cmp vs fix568b=$c1", 1),
    ("grep -qx 'VME_DEFAULT_RESULT=34/34' \"$O\"", "grep -qx 'VME_DEFAULT_RESULT=38/38' \"$O\"", 1),
    ("SENTINEL CLEARED: RESTORE_OK, BASE_FINAL 34/34 CONTROL=OK", "SENTINEL CLEARED: RESTORE_OK, BASE_FINAL 38/38 CONTROL=OK", 1),
    ("        /tmp/gxkt568) rm -rf -- \"$W\" ;;", "        /tmp/gxkt568t2) rm -rf -- \"$W\" ;;", 1),
    ("echo \"usage: kt568.sh setup", "echo \"usage: kt568t2.sh setup", 1),
]
for old, new, n in REPL:
    c = src.count(old)
    assert c == n, "count %d for %r" % (c, old[:70])
    src = src.replace(old, new)
assert "\r" not in src
io.open(sys.argv[2], "w", encoding="latin-1", newline="").write(src)
print("DRIVER_T2_WRITTEN %d replacements" % len(REPL))
