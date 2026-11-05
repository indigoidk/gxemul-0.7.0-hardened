#!/bin/bash
# asan_measure.sh <asan-clonedir> <variant-label>
# Runs guest ld.bu r2,r3,+off at +0x7c and +0xff against the (already built) ASAN binary.
# Probe session shape: -E mvme88k -e mvme187 -M 64, r3 = 0xfff43000.  ASAN_OPTIONS=detect_leaks=0.
set -u
CLONE="$1"; V="$2"
B=/mnt/c/DocumentNoSnc/cc/GXEMUL
SCR="$B/_scratchpad/opus_20261104/m_memc"
OUT="$SCR/out_asan"; mkdir -p "$OUT"
BIN="$CLONE/gxemul"
DUM="$OUT/dummy.bin"; printf '\0\0\0\0' > "$DUM"
export ASAN_OPTIONS=detect_leaks=0

run() {   # <offset-name> <instr-word-hex>
    local name="$1" word="$2" f="$OUT/${V}_${1}.txt"
    {
      echo "r3=0xfff43000"
      echo "r2=0x55555555"
      echo "put w 0x10000, 0x${word}"
      echo "pc=0x10000"
      echo "step 1"
      echo "reg"
      echo "quit"
    } | "$BIN" -V -x -E mvme88k -e mvme187 -M 64 "0x10000:$DUM" > "$f" 2>&1
    local rc=$?
    echo "=== $V $name  rc=$rc ==="
    if grep -q "ERROR: AddressSanitizer" "$f"; then
        echo "  ASAN: REPORTED"
        grep -m1 "ERROR: AddressSanitizer" "$f" | sed 's/^/  /'
        grep -m1 -E "^ *#0 " "$f" | sed 's/^/  /'
        grep -m1 -E "READ of size|WRITE of size" "$f" | sed 's/^/  /'
    else
        echo "  ASAN: none"
    fi
    if grep -q "GXemul> reg" "$f" && grep -q "cpu0:" "$f"; then echo "  prompt-returned: yes"; else echo "  prompt-returned: no"; fi
    grep -qE "mvme187_memc" "$f" && echo "  handler-text: $(grep -m1 -oE 'mvme187_memc[^]]*' "$f")"
}

run "off_7c" "0c43007c"
run "off_ff" "0c4300ff"
echo "ASAN_MEASURE_DONE_${V}"
