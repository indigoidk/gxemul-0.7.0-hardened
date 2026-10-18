#!/bin/bash
# build_pre522.sh -- negative control 2 for the rldicl gate wiring: build e777ff06's parent 02af7f3e (the pre-fix rldicl)
# in a SCRATCH clone under WSL /tmp -- no project tree is touched -- and run HEAD's probe (a frozen copy) against it.
set -u
P=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/ppcw
W=/tmp/gxpre522
rm -rf "$W"; mkdir -p "$W" && tar -xf "$P/pre522.tar" -C "$W" || { echo "UNPACK FAILED"; exit 9; }
cd "$W" && ./configure > "$P/pre522_configure.log" 2>&1 || { echo "CONFIGURE FAILED"; tail -5 "$P/pre522_configure.log"; exit 9; }
make -j4 > "$P/pre522_make.log" 2>&1; echo "MAKE_RC=$?"
[ -x "$W/gxemul" ] && [ "$W/gxemul" -nt "$W/src/cpus/cpu_ppc_instr.c" ] || { echo "NO FRESH BINARY"; tail -5 "$P/pre522_make.log"; exit 9; }
grep -n 'tmp & tmp2\|tmp2' "$W/src/cpus/cpu_ppc_instr.c" | grep -i -m3 'rldicl\|tmp & tmp2' > "$P/pre522_rldicl_lines.txt"
cd /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress || exit 9
timeout 120 python3 -u "$P/ppc_rldicl_probe.FROZEN.py" "$W/gxemul" prefix > "$P/rldicl_prefix_02af7f3e.log" 2>&1; echo "PROBE_RC=$?"
grep -E '^SCORE|^FAILING|PROBE_DONE' "$P/rldicl_prefix_02af7f3e.log"
echo PRE522_DONE
