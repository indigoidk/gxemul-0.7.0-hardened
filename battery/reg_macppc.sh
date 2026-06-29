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
W="$KERNELS"
pkill -9 -x gxemul 2>/dev/null
chk() {
	tag="$1"; sub="$2"; kern="$3"; secs="$4"
	log="$S/fin_${tag}_${sub}.log"
	python3 "$DR" "$log" $((secs+8)) "$EST" -q -E macppc -e "$sub" "$kern" <<EOF >/dev/null 2>&1
W:$secs
EOF
	deg=$(tr '\200-\377' '\000-\177' < "$log")
	banner=$(printf '%s' "$deg" | grep -aoiE 'NetBSD [0-9][0-9.]*|OpenBSD [0-9][0-9.]*' | head -1)
	printf "%-10s -e %-7s banner=[%s]\n" "$tag" "$sub" "$banner"
}
echo "=== OB-35 macppc regression (OpenBSD 3.4 must boot on BOTH; NetBSD = research) ==="
chk obsd34  g4     "$W/3.4/macppc/bsd" 42
chk obsd34  g4plus "$W/3.4/macppc/bsd" 42
chk netbsd82 g4plus "$O/k_macppc"      45
echo "=== done $(date +%H:%M:%S) ==="
