#!/bin/sh
# --- configurable paths (override via env, or edit these defaults) ----------
GXEMUL="${GXEMUL:-../gxemul}"                 # built gxemul binary (./configure && make at the repo root)
DRIVE="${DRIVE:-$(dirname "$0")/drive.py}"    # expect driver (shipped in this folder)
KERNELS="${KERNELS:-./kernels}"               # guest test kernels / images -- PROVIDE YOUR OWN (see TEST_BATTERY.md)
RIGDIR="${RIGDIR:-./rig}"                      # OpenBSD/pmax installed-disk rig: bsd + disk.img -- PROVIDE YOUR OWN
WORK="${WORK:-./out}"; mkdir -p "$WORK"
# ---------------------------------------------------------------------------
EST="$GXEMUL"
DR="$DRIVE"
O="$KERNELS"
S="$WORK"
pkill -9 -x gxemul 2>/dev/null
log=$S/luna_shell.log
python3 "$DR" "$log" 90 "$EST" -e luna-88k "$O/luna_bsd.rd" <<'EOF' >/dev/null 2>&1
E:hell
W:2
S:s\n
W:4
S:echo LUNA_SH_START; uname -a; sysctl hw.model hw.ncpu hw.physmem; echo LUNA_SH_END\n
W:6
S:ls /dev | tr '\n' ' '; echo; echo DEV_DONE\n
W:5
S:dmesg | grep -iE 'cmmu|M881|le0|real mem' ; echo DMESG_DONE\n
W:5
S:halt\n
W:3
EOF
deg=$(tr '\200-\377' '\000-\177' < "$log")
echo "=== luna88k SHELL exercise ==="
printf '%s' "$deg" | grep -aiE 'LUNA_SH_START|OpenBSD [0-9]|uname|hw.model|hw.ncpu|hw.physmem|M881|CMMU|le0|real mem|DEV_DONE|DMESG_DONE|reboot|halt' | grep -avE '^\[(SENT|WAIT|MATCHED)' | head -25
echo "reached-shell=$(printf '%s' "$deg" | grep -ac 'LUNA_SH_START')  uname-ran=$(printf '%s' "$deg" | grep -aci 'OpenBSD.*luna88k\|OpenBSD .* GENERIC\|OpenBSD .* RAMDISK')"
