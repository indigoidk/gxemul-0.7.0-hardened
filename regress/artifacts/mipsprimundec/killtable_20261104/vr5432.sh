#!/bin/bash
B=/mnt/c/DocumentNoSnc/cc/GXEMUL/build/gxemul
O=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/mipsprimundec/killtable_20261104
printf "pc=0xffffffff80020000\nstep 1\nreg\nquit\n" | timeout 60 $B -V -x -E testmips -C VR5432 0xffffffff80020000:$O/cpu_mips_instr.c.base > $O/vr5432_construct.out 2>&1; echo "VR5432 rc=$? prompts=$(grep -c "GXemul>" $O/vr5432_construct.out)"; grep -m2 -i "error\|config0\|cpu rev" $O/vr5432_construct.out
