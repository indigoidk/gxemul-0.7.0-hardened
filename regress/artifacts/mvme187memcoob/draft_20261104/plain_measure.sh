#!/bin/bash
# plain_measure.sh  --  part (b): the draft (A3) in the plain clone /tmp/gxopus_memc.
set -u
B=/mnt/c/DocumentNoSnc/cc/GXEMUL
SCR="$B/_scratchpad/opus_20261104/m_memc"
OUT="$SCR/out_plain"; mkdir -p "$OUT"
BIN=/tmp/gxopus_memc/gxemul
PROBE="$B/GXEMUL-SEC/regress/mvme187_memc_probe.py"
DUM="$OUT/dummy.bin"; printf '\0\0\0\0' > "$DUM"

echo "===== 1. repo probe (READ-ONLY, absolute path) ====="
python3 -u "$PROBE" "$BIN" draft_plain "$OUT/probe_work" > "$OUT/probe.out" 2>&1
tail -1 "$OUT/probe.out" | grep -q MVME187_MEMC_PROBE_DONE && echo "(sentinel present)" || echo "(SENTINEL MISSING)"
cat "$OUT/probe.out"

# one declined-read session: r2 preset to SENT, ld.bu r2,r3,<off>, step, read r2
rd() {  # <name> <word>
    local f="$OUT/rd_$1.txt"
    { echo "r3=0xfff43000"; echo "r2=0x55555555"; echo "put w 0x10000, 0x$2";
      echo "pc=0x10000"; echo "step 1"; echo "reg"; echo "quit"; } \
      | "$BIN" -V -x -E mvme88k -e mvme187 -M 64 "0x10000:$DUM" > "$f" 2>&1
    local rc=$? seg r2
    seg="$(awk '/GXemul> reg/{c=NR} {a[NR]=$0} END{for(i=c;i<=NR;i++)print a[i]}' "$f")"
    r2="$(printf '%s\n' "$seg" | grep -oE 'r2 *= *0x[0-9a-fA-F]+' | head -1)"
    echo "  $1 (ld.bu +$1): rc=$rc  $r2   $(grep -m1 -oE 'mvme187_memc[^]]*' "$f")"
}

echo "===== 2. declined-read return values (r2 after one ld.bu) ====="
rd 0x0c 0c43000c
rd 0x7c 0c43007c
rd 0xff 0c4300ff
rd 0x10c 0c43010c

echo "===== 3. memconf: st.b 0x7 to +0x08, then ld.bu +0x08 in the SAME session ====="
f="$OUT/memconf_wr_then_rd.txt"
{ echo "r3=0xfff43000"; echo "r2=0x7";
  echo "put w 0x10000, 0x2c430008";   # st.b  r2,r3,0x08  (store 0x7 to memconf)
  echo "put w 0x10004, 0x0c430008";   # ld.bu r2,r3,0x08  (read memconf back)
  echo "pc=0x10000"; echo "step 2"; echo "reg"; echo "quit"; } \
  | "$BIN" -V -x -E mvme88k -e mvme187 -M 64 "0x10000:$DUM" > "$f" 2>&1
rc=$?
seg="$(awk '/GXemul> reg/{c=NR} {a[NR]=$0} END{for(i=c;i<=NR;i++)print a[i]}' "$f")"
echo "  rc=$rc  $(printf '%s\n' "$seg" | grep -oE 'r2 *= *0x[0-9a-fA-F]+' | head -1)  (0x3 = memconf unchanged)"
echo "  announce: $(grep -m1 -oE 'mvme187_memc[^]]*' "$f")"
echo "PLAIN_MEASURE_DONE"
