#!/bin/bash
B=/mnt/c/DocumentNoSnc/cc/GXEMUL/build/gxemul
O=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/mipsprimundec/killtable_20261104
printf "put w 0xffffffff80020000, 0x78000000\npc=0xffffffff80020000\nstep 1\nreg\nreg ,0\nquit\n" | timeout 60 $B -V -x -E testmips -C R5900 0xffffffff80020000:$O/cpu_mips_instr.c.base > /tmp/r5900_probe.out 2>&1; echo "R5900 rc=$? prompts=$(grep -c "GXemul>" /tmp/r5900_probe.out) unimpl=$(grep -c "UNIMPLEMENTED" /tmp/r5900_probe.out)"; tail -4 /tmp/r5900_probe.out | cut -c1-150
