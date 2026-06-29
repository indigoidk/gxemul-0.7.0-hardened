#!/bin/sh
# --- configurable paths (override via env, or edit these defaults) ----------
GXEMUL="${GXEMUL:-../gxemul}"                 # built gxemul binary (./configure && make at the repo root)
DRIVE="${DRIVE:-$(dirname "$0")/drive.py}"    # expect driver (shipped in this folder)
KERNELS="${KERNELS:-./kernels}"               # guest test kernels / images -- PROVIDE YOUR OWN (see TEST_BATTERY.md)
RIGDIR="${RIGDIR:-./rig}"                      # OpenBSD/pmax installed-disk rig: bsd + disk.img -- PROVIDE YOUR OWN
WORK="${WORK:-./out}"; mkdir -p "$WORK"
# ---------------------------------------------------------------------------
GX="$GXEMUL"; DR="$DRIVE"; O="$KERNELS"
W="$KERNELS"
S="$WORK"
cp "$W/3.4/macppc/bsd.rd" "$O/obsd34_macppc.rd" 2>/dev/null
pkill -9 -x gxemul 2>/dev/null
python3 "$DR" "$S/ppc_shell.log" 175 "$GX" -q -E macppc -e g4 "$O/obsd34_macppc.rd" <<'EOF' >/dev/null 2>&1
E:hell
W:3
S:s\n
W:5
S:echo PPC_SHELL_START\n
W:3
S:sysctl hw.model hw.machine 2>/dev/null; echo PPC_MID\n
W:5
S:dmesg | grep -iE 'cpu0|OpenBSD|real mem|mesh|bm0|PowerPC|601|604|750|7400' 2>/dev/null; echo PPC_SHELL_END\n
W:5
EOF
d=$(tr '\200-\377' '\000-\177' < "$S/ppc_shell.log" 2>/dev/null | sed 's/\x1b\[[0-9;?]*[A-Za-z]//g')
echo "=== macppc (PPC) shell drive ==="
printf '%s' "$d" | grep -avE 'memory (READ|WRITE):|non-existant|^\[(SENT|WAIT|MATCHED)' | grep -aiE 'PPC_SHELL_START|PPC_MID|PPC_SHELL_END|hw.model|hw.machine|OpenBSD|cpu0|real mem|PowerPC|Shell|# ' | tail -16
echo "reached-shell=$(printf '%s' "$d" | grep -ac 'PPC_SHELL_START')"
echo "--- last 12 non-warning lines (where it actually got) ---"
printf '%s' "$d" | grep -avE 'memory (READ|WRITE):|non-existant|^\[(SENT|WAIT|MATCHED)' | tail -12
