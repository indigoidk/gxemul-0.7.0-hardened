#!/bin/bash
# hygienecensus controls: run gate_hygiene.sh's CENSUS rows on the real tree and on two mutated COPIES.
# Never touches the tree: every run is on a copy of regress/ (top level only, as the census scopes it).
# The pty-log half of the gate needs gate 4's logs and SKIPS here by design (empty LOGDIR); only the
# readiness/census rows are graded.
set -u
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
W=/tmp/gxcensus0923
OUT=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/census_controls
mkdir -p "$OUT"
mk() {  # fresh copy of regress/ top-level files (not artifacts/)
    rm -rf "$W/$1"; mkdir -p "$W/$1/regress"
    (cd "$SEC/regress" && find . -maxdepth 1 -type f -exec cp -p {} "$W/$1/regress/" \;)
}
run() {  # grade the census rows of the gate in copy $1
    mkdir -p "$W/$1/logs"
    ( cd "$W/$1/regress" && LOGDIR="$W/$1/logs" bash ./gate_hygiene.sh ) > "$OUT/$1.out" 2>&1
    echo "== $1: $(grep -cE '^\s*(ok|FAIL)\b' "$OUT/$1.out" | tr -d ' ') rows graded"
    grep -E 'readiness|whole-buffer' "$OUT/$1.out" | sed 's/\x1b\[[0-9;]*m//g' | sed 's/^/   /'
}
# (a) the tree as it is
mk real; run real
# (b) MOVE: take arm_bdt_probe.py's site out, put one in another pty-driving probe -> count stays 3
mk move
python3 - "$W/move/regress" <<'PY'
import io, sys, os
d = sys.argv[1]
p = os.path.join(d, 'arm_bdt_probe.py')
s = io.open(p, encoding='utf-8', newline='').read()
old = 'self.buf.rstrip().endswith("GXemul>")'
assert s.count(old) == 1, s.count(old)
io.open(p, 'w', encoding='utf-8', newline='').write(s.replace(old, 'self.buf.rstrip()[-7:] == "GXemul>"'))
q = os.path.join(d, 'luna_absentcpu_probe.py')
t = io.open(q, encoding='utf-8', newline='').read()
io.open(q, 'w', encoding='utf-8', newline='').write(t + '\n_control_site = lambda buf: buf.rstrip().endswith("GXemul>")\n')
print('move applied')
PY
run move
# (c) ADD: a fourth site, nothing removed
mk add
printf '\n_control_site = lambda buf: buf.rstrip().endswith("GXemul>")\n' >> "$W/add/regress/luna_absentcpu_probe.py"
run add
rm -rf "$W"
echo "CONTROLS_DONE"
