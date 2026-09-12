#!/bin/bash
set -e
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
SD=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_p2
CL=/tmp/gxopus_p2
OX="$SEC/regress/artifacts/xscaleinten/opus_pass2_20260912"
STUB="$SEC/regress/artifacts/xscaleinten/base_20260912/xscale_stub.bin"
F=src/cpus/cpu_arm_coproc.c
T=$'\t'
printf 'cpu->cd.arm.r[rd] = cpu->cd.arm.i80321_inten;' > "$SD/x_old.txt"

build () { # $1 label $2 body
  cp "$SEC/src/cpus/cpu_arm_coproc.c" "$CL/$F"
  printf 'cpu->cd.arm.r[rd] = cpu->cd.arm.i80321_inten;\n%s%s%s%s%s\n' "$T" "$T" "$T" "$T" "$2" > "$SD/x_new.txt"
  python3 "$SD/patch.py" "$CL/$F" "$SD/x_old.txt" "$SD/x_new.txt" >/dev/null
  echo "$1" > "$CL/.MUTANT"
  cd "$CL"; rm -f src/cpus/*.o; make -j4 >/tmp/ob.log 2>&1
  [ gxemul -nt "$CL/$F" ] || { echo "$1 STALE"; exit 1; }
}

# read inten into r0:  mrc 6,0,r0,cr0,cr0,0 = 0xee100610
livecheck () { # label word setup_cmds...
  local L="$1"; shift; local W="$1"; shift
  { for c in "$@"; do echo "$c"; done
    echo "put w 0x00008000, $W"
    echo "pc=0x00008000"
    echo "step 1"
    echo "reg"
    echo "quit"; } | "$CL/gxemul" -V -T -E iq80321 -M 32 "0x8000:$STUB" > "$OX/live_${L}.log" 2>&1 || true
  echo -n "$L exit=$?  "; grep -c "TODO: XScale read from inten" "$OX/live_${L}.log" | sed 's/^/TODOcount=/'
}

echo "=== XM_RD0 liveness: read inten into r0 must DIE ==="
build XM_RD0 'if (rd == 0) { fatal("TODO: XScale read from inten?\n"); exit(1); }'
livecheck XM_RD0_r0 0xee100610
echo "   control on same build: read inten into r9 must SURVIVE"
livecheck XM_RD0_r9 0xee109610

echo "=== XM_MAGICBIT liveness: inten<-0x400000 then read must DIE ==="
build XM_MAGICBIT 'if (cpu->cd.arm.i80321_inten & 0x00400000) { fatal("TODO: XScale read from inten?\n"); exit(1); }'
# r1=0x400000; mcr inten<-r1 (0xee001610); mrc r9<-inten (0xee109610)
{ echo "r1=0x00400000"
  echo "put w 0x00008000, 0xee001610"
  echo "put w 0x00008004, 0xee109610"
  echo "pc=0x00008000"; echo "step 2"; echo "reg"; echo "quit"; } | "$CL/gxemul" -V -T -E iq80321 -M 32 "0x8000:$STUB" > "$OX/live_XM_MAGICBIT.log" 2>&1 || true
echo -n "XM_MAGICBIT(bit22 read) : "; grep -c "TODO: XScale read from inten" "$OX/live_XM_MAGICBIT.log" | sed 's/^/TODOcount=/'

echo "=== restore ==="
cp "$SEC/src/cpus/cpu_arm_coproc.c" "$CL/$F"
cd "$CL"; rm -f src/cpus/*.o; make -j4 >/tmp/ob.log 2>&1
cmp -s "$CL/$F" "$SEC/src/cpus/cpu_arm_coproc.c" && [ gxemul -nt "$CL/$F" ] && { rm -f "$CL/.MUTANT"; echo "RESTORE CLEAN"; } || echo "RESTORE PROBLEM"
echo VERIFY_X_DONE
