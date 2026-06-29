#!/bin/sh
# --- configurable paths (override via env, or edit these defaults) ----------
GXEMUL="${GXEMUL:-../gxemul}"                 # built gxemul binary (./configure && make at the repo root)
DRIVE="${DRIVE:-$(dirname "$0")/drive.py}"    # expect driver (shipped in this folder)
KERNELS="${KERNELS:-./kernels}"               # guest test kernels / images -- PROVIDE YOUR OWN (see TEST_BATTERY.md)
RIGDIR="${RIGDIR:-./rig}"                      # OpenBSD/pmax installed-disk rig: bsd + disk.img -- PROVIDE YOUR OWN
WORK="${WORK:-./out}"; mkdir -p "$WORK"
# ---------------------------------------------------------------------------
# Multi-arch boot regression on the rebuilt est build/gxemul, WITH per-machine device-attach
# assertions + negative-marker (panic/fatal/ASan) detection (post-boot check #1, Codex+agy consensus).
B="$GXEMUL"
DR="$DRIVE"
O="$KERNELS"
S="$WORK"
pkill -9 -x gxemul 2>/dev/null; pkill -9 -x python3 2>/dev/null
echo "==================== MULTI-ROM BOOT REGRESSION (+device-attach asserts) ===================="
# args: name  expect-device-regex  kernel  gxemul-args...
run() {
	name="$1"; exp="$2"; kern="$3"; shift 3
	log="$S/sweep_$name.log"
	if [ ! -f "$kern" ]; then printf "%-10s SKIP (no kernel)\n" "$name"; return; fi
	python3 "$DR" "$log" 52 "$B" -q "$@" "$kern" <<'EOF' >/dev/null 2>&1
W:42
EOF
	deg=$(tr '\200-\377' '\000-\177' < "$log" 2>/dev/null)
	banner=$(printf '%s' "$deg" | grep -aoiE 'NetBSD [0-9][0-9.]*|Linux version [0-9][^ ]*|OpenBSD [0-9][0-9.]*' | head -1)
	dev=$(printf '%s' "$deg" | grep -acE "$exp")
	# NEGATIVE markers: real-regression signals the banner-only check used to miss (panic/fatal added)
	bad=$(printf '%s' "$deg" | grep -acaiE 'panic|fatal error|AddressSanitizer|Segmentation fault|runtime error:|internal error|abort \(core|cannot (mount|open)')
	if   [ "$bad" != 0 ];                              then v="FAIL!! "
	elif [ -n "$banner" ] && [ "$dev" -gt 0 ];        then v="BOOTED "
	elif [ "$dev" -gt 0 ];                            then v="early  "
	else                                              v="REVIEW "; fi
	printf "%-10s %s banner=[%s] dev-attach=%s(%s) bad=%s\n" "$name" "$v" "$banner" "$dev" "$exp" "$bad"
}
#   name      expected machine-specific device line(s)               kernel            machine args
run cats     'cpu[0-9]|mainbus0|footbridge|fcom'                     "$O/k_cats"        -E cats
run arc_nb   'cpu0|mainbus0|com0|pica|jazzio'                        "$O/k_arc"         -E arc -e pica
run hpcmips  'cpu0|mainbus0|vrip|vrgiu'                              "$O/k_hpcmips"     -E hpcmips -e mobilepro770
run sgimips  'cpu0|mainbus0|crime|mace|zsc'                          "$O/k_sgimips"     -E sgi -e o2
run macppc   'of:|bandit|mac-io|mainbus|cpu'                         "$O/k_macppc"      -E macppc -e g4
run prep     'cpu0|mainbus0|pci|com0|NetBSD'                         "$O/nb82_prep.gz"  -E prep -e ibm6050
run landisk  'cpu0|mainbus0|shb|superio|wdc'                         "$O/rk_landisk"    -E landisk
run luna88k  'M88100|CMMU|le0 at|mainbus0|sio0'                      "$O/luna_bsd.rd"   -e luna-88k
run malta_lx 'CPU revision|Linux|console |Memory:'                   "$O/vmlinux-malta-el" -E evbmips -e malta -o "console=ttyS0"
echo "=================== sweep done $(date +%H:%M:%S) ==================="
echo "(BOOTED=banner+expected device; early=device-probe milestone, no banner [macppc]; FAIL=panic/fatal/ASan)"
