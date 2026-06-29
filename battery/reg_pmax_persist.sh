#!/bin/sh
# --- configurable paths (override via env, or edit these defaults) ----------
GXEMUL="${GXEMUL:-../gxemul}"                 # built gxemul binary (./configure && make at the repo root)
DRIVE="${DRIVE:-$(dirname "$0")/drive.py}"    # expect driver (shipped in this folder)
KERNELS="${KERNELS:-./kernels}"               # guest test kernels / images -- PROVIDE YOUR OWN (see TEST_BATTERY.md)
RIGDIR="${RIGDIR:-./rig}"                      # OpenBSD/pmax installed-disk rig: bsd + disk.img -- PROVIDE YOUR OWN
WORK="${WORK:-./out}"; mkdir -p "$WORK"
# ---------------------------------------------------------------------------
# Disk-INTEGRITY regression: write a known file on the root FS, clean halt, then RE-BOOT the SAME
# image and prove (a) the file survived (cksum match => disk flush persisted) and (b) FFS is clean
# (no fsck repair). Boots the same /tmp image TWICE (no re-copy between boots).
GX="$GXEMUL"
RIG="$RIGDIR"
S="$WORK"
IMG=/tmp/rz1.persist.img
L1="$S/persist_boot1.log"; L2="$S/persist_boot2.log"
cp -f "$RIG/bsd" /tmp/bsd.pmax
cp -f "$RIG/disk.img" "$IMG"
boot() { python3 "$DRIVE" "$1" 220 "$GX" -q -e 3max -d 1:"$IMG" /tmp/bsd.pmax; }

echo "=== BOOT 1: write /root/gxpersist.dat, cksum, sync, clean halt ==="
: > "$L1"; n=0
while [ $n -lt 2 ]; do n=$((n+1)); pkill -9 -x gxemul 2>/dev/null; sleep 1
  boot "$L1" <<'EOF'
E:root device
S:rz1\n
E:login:
S:root\n
W:5
S:vt100\n
W:3
S:\n
W:2
S:echo W1_START; rm -f /root/gxpersist.dat; echo GXPERSIST_DATA_123456 > /root/gxpersist.dat; cksum /root/gxpersist.dat; sync; sync; echo W1_DONE\n
W:6
S:sync; sync; halt\n
E:halted
EOF
  tr '\200-\377' '\000-\177' < "$L1" | grep -aq W1_DONE && break
done
CK1=$(tr '\200-\377' '\000-\177' < "$L1" | grep -a 'gxpersist.dat' | grep -aoE '^[0-9]+ [0-9]+' | head -1)

echo "=== BOOT 2: SAME image -> fsck on boot + re-read the file ==="
: > "$L2"; pkill -9 -x gxemul 2>/dev/null; sleep 1
boot "$L2" <<'EOF'
E:root device
S:rz1\n
E:login:
S:root\n
W:5
S:vt100\n
W:3
S:\n
W:2
S:echo R2_START; cat /root/gxpersist.dat; cksum /root/gxpersist.dat; echo R2_DONE\n
W:6
S:sync; halt\n
E:halted
EOF
D2=$(tr '\200-\377' '\000-\177' < "$L2")
CK2=$(printf '%s' "$D2" | grep -a 'gxpersist.dat' | grep -aoE '^[0-9]+ [0-9]+' | head -1)
CONTENT=$(printf '%s' "$D2" | grep -ac 'GXPERSIST_DATA_123456')
# fsck markers: the golden disk.img has PRE-EXISTING salvage markers (UNREF inode from 1996). Compare
# boot2 vs the fresh-image baseline (boot1) -- only NEW markers indicate a real disk-write regression.
DMGRE='WAS MODIFIED|UNREF|UNALLOCATED|SALVAG|BAD SUPER|PARTIALLY|INCORRECT|CANNOT READ'
FSCKBAD1=$(tr '\200-\377' '\000-\177' < "$L1" | grep -aciE "$DMGRE")
FSCKBAD2=$(printf '%s' "$D2" | grep -aciE "$DMGRE")
NEWDMG=$((FSCKBAD2 - FSCKBAD1)); [ $NEWDMG -lt 0 ] && NEWDMG=0
echo "######## DISK-INTEGRITY (PERSISTENCE) RESULT ########"
echo "boot1 cksum: [$CK1]   (fresh-image fsck baseline markers=$FSCKBAD1 -- pre-existing in golden img)"
echo "boot2 cksum: [$CK2]   content-survived=$CONTENT   boot2 fsck markers=$FSCKBAD2   NEW-vs-baseline=$NEWDMG"
if [ -n "$CK1" ] && [ "$CK1" = "$CK2" ] && [ "$CONTENT" -ge 1 ] && [ "$NEWDMG" -eq 0 ]; then
  echo "RESULT: PASS  (file persisted across reboot: cksum match + content survived + NO new FFS damage vs baseline => disk flush works)"
else
  echo "RESULT: CHECK (ck-match=$([ "$CK1" = "$CK2" ] && echo yes || echo NO) content=$CONTENT new-fsck-damage=$NEWDMG)"
fi
