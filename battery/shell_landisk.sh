#!/bin/sh
# --- configurable paths (override via env, or edit these defaults) ----------
GXEMUL="${GXEMUL:-../gxemul}"                 # built gxemul binary (./configure && make at the repo root)
DRIVE="${DRIVE:-$(dirname "$0")/drive.py}"    # expect driver (shipped in this folder)
KERNELS="${KERNELS:-./kernels}"               # guest test kernels / images -- PROVIDE YOUR OWN (see TEST_BATTERY.md)
RIGDIR="${RIGDIR:-./rig}"                      # OpenBSD/pmax installed-disk rig: bsd + disk.img -- PROVIDE YOUR OWN
WORK="${WORK:-./out}"; mkdir -p "$WORK"
# ---------------------------------------------------------------------------
GX="$GXEMUL"; DR="$DRIVE"; O="$KERNELS"
S="$WORK"
pkill -9 -x gxemul 2>/dev/null
python3 "$DR" "$S/sh4_shell.log" 110 "$GX" -E landisk "$O/inst_landisk.gz" <<'EOF' >/dev/null 2>&1
E:Terminal type
S:vt100\n
W:7
S:a\n
W:5
S:e\n
W:4
S:a\n
W:4
S:echo SH4_SHELL_START\n
W:3
S:sysctl hw.model hw.physmem 2>/dev/null; uname -m -r 2>/dev/null; echo SH4_MID\n
W:5
S:dmesg | grep -iE 'cpu0|wdc0|real mem' 2>/dev/null; echo SH4_SHELL_END\n
W:5
EOF
d=$(tr '\200-\377' '\000-\177' < "$S/sh4_shell.log" 2>/dev/null | sed 's/\x1b\[[0-9;?]*[A-Za-z]//g')
echo "=== landisk SH4 shell drive ==="
printf '%s' "$d" | grep -avE 'memory (READ|WRITE):|non-existant|^\[(SENT|WAIT|MATCHED)' | grep -aiE 'SH4_SHELL_START|SH4_MID|SH4_SHELL_END|hw.model|hw.physmem|SH7751|landisk|cpu0|wdc0|real mem|# ' | tail -18
echo "reached-shell=$(printf '%s' "$d" | grep -ac 'SH4_SHELL_START')  sysctl-ran=$(printf '%s' "$d" | grep -aci 'hw.model.*Landisk\|SH7751\|hw.physmem')"
