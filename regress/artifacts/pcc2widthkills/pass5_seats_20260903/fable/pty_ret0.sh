#!/bin/bash
set -u
G=/mnt/c/DocumentNoSnc/CC/GXEMUL; SEC=$G/GXEMUL-SEC; T=/tmp/gxfable_p5; F=src/devices/dev_pcc2.c
OUT=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/pcc2p5_fable
say() { echo "[$(date +%H:%M:%S)] $*"; }; die() { echo "*** ABORT: $*"; exit 9; }
[ -e "$T/.MUTANT" ] && die "sentinel present"; cmp -s "$T/$F" "$SEC/$F" || die "clone not clean"
build() { cd "$T" || die cd; rm -f src/devices/dev_pcc2.o; make -j4 > "$OUT/build_$1.log" 2>&1; [ "$T/gxemul" -nt "$T/$F" ] || die "$1: binary not newer"; }
say "BASE pty session (fix)"; python3 "$OUT/pty_ret0_probe.py" "$T/gxemul" fix
echo "$F  mutant M_RET0_VECBASE (pty)" > "$T/.MUTANT"
python3 - "$T/$F" <<'PYEOF'
import io, sys
p = sys.argv[1]; s = io.open(p, encoding='utf-8').read()
a = '\t\tif (len != 1 && writeflag == MEM_WRITE) {\n\t\t\tpcc2_width_decline(d, PCC2_W_VECBASE_LEN, "PCCTWO_VECBASE", len);\n\t\t\tbreak;\n\t\t}\n'
assert s.count(a) == 1; s = s.replace(a, a.replace('\t\t\tbreak;\n', '\t\t\treturn 0;\n'))
io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
PYEOF
cmp -s "$T/$F" "$SEC/$F" && die "UNCHANGED"; build M_RET0_pty
say "    mutant text: $(grep -c 'return 0;' "$T/$F") ret0; binary $(date -r "$T/gxemul" +%H:%M:%S) source $(date -r "$T/$F" +%H:%M:%S)"
say "MUTANT pty session"; python3 "$OUT/pty_ret0_probe.py" "$T/gxemul" ret0
cp "$SEC/$F" "$T/$F"; cmp -s "$T/$F" "$SEC/$F" || die "restore cmp FAILED -- sentinel KEPT"
build restore3; rm -f "$T/.MUTANT"; say "restored + REBUILT + verified, sentinel cleared"; say "PTY_RET0_DONE"
