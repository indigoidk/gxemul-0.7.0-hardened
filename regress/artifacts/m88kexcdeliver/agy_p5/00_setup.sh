#!/bin/bash
set -e

SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
B=/mnt/c/DocumentNoSnc/CC/GXEMUL/build
C=/tmp/gxagy502
OUT=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/m88kexc/agy_p5

echo "=== 1. Checking source identity vs SEC ==="
cmp "$B/src/cpus/cpu_m88k.c" "$SEC/src/cpus/cpu_m88k.c" && echo "CMP_CLEAN_BUILD_VS_SEC"

echo "=== 2. Creating scratch clone /tmp/gxagy502 ==="
rm -rf "$C"
cp -a "$B" "$C"
cmp "$C/src/cpus/cpu_m88k.c" "$SEC/src/cpus/cpu_m88k.c" && echo "CMP_CLEAN_CLONE_VS_SEC"

echo "=== 3. Freezing probe ==="
cp "$SEC/regress/m88k_exc_probe.py" "$C/probe.frozen.py"
PROBE_MD5=$(md5sum "$C/probe.frozen.py" | cut -d' ' -f1)
echo "PROBE_MD5=$PROBE_MD5"
case "$PROBE_MD5" in
  96ab47a0*) echo "PROBE_MD5_MATCHES_96ab47a0" ;;
  *) echo "PROBE_MD5_MISMATCH!"; exit 1 ;;
esac

echo "=== 4. Rebuilding baseline in clone ==="
cd "$C/src/cpus"
rm -f cpu_m88k.o
make -s -j4
cd "$C"
make -s -j4

if [ "$C/gxemul" -nt "$C/src/cpus/cpu_m88k.c" ]; then
    echo "BINARY_NEWER_OK"
else
    echo "BINARY_STALE_ERROR"
    exit 1
fi

echo "=== 5. Running BASE probe ==="
python3 -u "$C/probe.frozen.py" "$C/gxemul" > "$OUT/BASE.out"
echo "BASE_PROBE_EXIT=$?"

grep -E 'M88KEXC_RESULT|M88KEXC_DONE|M88KEXC_SELFTEST' "$OUT/BASE.out"
echo "SETUP_DONE"
