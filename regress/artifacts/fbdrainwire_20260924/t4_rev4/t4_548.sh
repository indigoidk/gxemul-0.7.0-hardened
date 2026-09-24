#!/bin/bash
# #548 revision 4: gate 2's harness (final text) x mutants and x its own self-edits, compiled exactly as
# gate_offline.sh compiles it against build/'s objects; the two gate_offline pins read exactly as the gate reads them.
set -u
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
M3=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/opus548/out/p3/mutants
MF2=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/opus548/out/f2/mutants
OUT=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/u3_cpp/pre548/t4
T=/tmp/t4548
rm -rf "$T"; mkdir -p "$T" "$OUT"
OBJS=$(find "$SEC/../build/src" -name '*.o' ! -name 'main.o' ! -name 'dev_footbridge.o' | sort)
md5sum "$SEC/regress/diff_fbpending_bound.c" "$SEC/src/devices/dev_footbridge.c" "$SEC/regress/gate_offline.sh" > "$OUT/INPUTS.md5"
# the two pins, read out of the gate script itself so this table measures what the gate greps
PIN6=$(sed -n 's/.*grep -cxF "\(  ok   R6 a re-armed[^"]*\)".*/\1/p' "$SEC/regress/gate_offline.sh")
PIN6B=$(sed -n 's/.*grep -cxF "\(  ok   R6b each[^"]*\)".*/\1/p' "$SEC/regress/gate_offline.sh")
echo "PIN6 =[$PIN6]"; echo "PIN6B=[$PIN6B]"
[ -n "$PIN6" ] && [ -n "$PIN6B" ] || { echo "PINS NOT FOUND IN gate_offline.sh"; exit 9; }

python3 - "$SEC/regress/diff_fbpending_bound.c" "$SEC/src/devices/dev_footbridge.c" "$T" <<'PYEOF'
import io, sys
hsrc, dsrc, T = sys.argv[1], sys.argv[2], sys.argv[3]
h = io.open(hsrc, encoding="utf-8", newline="").read()
post = "drive(r6, t, 8192, &pk[s][t], &trough);"
assert h.count(post) == 1
cond = "if (owed[s][t] != owe || pk[s][t] != want ||"
assert h.count(cond) == 1
pre = "drive(r6, t, 8192, &peak, &trough);"
assert h.count(pre) == 1
V = {"H_retarget": h.replace(post, "drive(r6, 0, 8192, &pk[s][t], &trough);"),
     "H_and":      h.replace(cond, "if (owed[s][t] != owe && pk[s][t] != want &&"),
     "H_pre0":     h.replace(pre, "drive(r6, t, 0, &peak, &trough);")}
for k, v in V.items():
    assert v != h
    io.open(T + "/" + k + ".c", "w", encoding="utf-8", newline="").write(v)
d = io.open(dsrc, encoding="utf-8", newline="").read()
st = "d->pending_bound[timer_nr] = (int) bound;"
assert d.count(st) == 1
import os
os.makedirs(T + "/mut_M_mask16", exist_ok=True)
io.open(T + "/mut_M_mask16/dev_footbridge.c", "w", encoding="utf-8", newline="").write(
    d.replace(st, "d->pending_bound[timer_nr] = (int) bound & ~(timer_nr << 16);"))
print("variants written")
PYEOF

run() {   # label harness devdir
    local L=$1 H=$2 D=$3
    if ! cc -O2 -std=gnu99 -I"$D" -I"$SEC/src/include" -I"$SEC/src/include/thirdparty" -I"$SEC/src/devices" \
            -o "$T/bin_$L" "$H" $OBJS -lm -L/usr/X11R6/lib -lX11 > "$OUT/cc_$L.log" 2>&1; then
        echo "$L  COMPILE_FAILED"; sed -n '1,5p' "$OUT/cc_$L.log"; return
    fi
    "$T/bin_$L" 2147487744 > "$OUT/run_$L.log" 2>&1
    printf '%-18s PASS=%s R5=%-4s R6=%-4s R6b=%-4s IDENT=%-4s pinR6=%s pinR6b=%s | %s\n' "$L" \
        "$(grep -c '^FBBOUND_PASS$' "$OUT/run_$L.log")" \
        "$(grep -cE '^  FAIL +R5 ' "$OUT/run_$L.log")" \
        "$(grep -E '^  (ok|FAIL) +R6 a re-armed' "$OUT/run_$L.log" | awk '{print $1}')" \
        "$(grep -E '^  (ok|FAIL) +R6b ' "$OUT/run_$L.log" | awk '{print $1}')" \
        "$(grep -E '^  (ok|FAIL) +IDENTITY' "$OUT/run_$L.log" | awk '{print $1}')" \
        "$(grep -cxF "$PIN6" "$OUT/run_$L.log")" "$(grep -cxF "$PIN6B" "$OUT/run_$L.log")" \
        "$(grep -E 'R6 a re-armed' "$OUT/run_$L.log" | sed 's/.*structs: //' | cut -c1-100)"
}

HF="$SEC/regress/diff_fbpending_bound.c"
run base "$HF" "$SEC/src/devices"
for m in M_eq M_idle M_pendguard M_frozen M_idx0 M_cmp0 M_pct3 M_rst2 M_neqB M_zge M_lowonly M_nobound M_x2; do
    mkdir -p "$T/mut_$m"; cp "$M3/$m.c" "$T/mut_$m/dev_footbridge.c"; run "$m" "$HF" "$T/mut_$m"
done
for m in M_eq_n2 M_pend_n0 M_upskip; do
    mkdir -p "$T/mut_$m"; cp "$MF2/$m.c" "$T/mut_$m/dev_footbridge.c"; run "$m" "$HF" "$T/mut_$m"
done
run M_mask16 "$HF" "$T/mut_M_mask16"
for h in H_retarget H_and H_pre0; do
    run "${h}_base" "$T/$h.c" "$SEC/src/devices"
    run "${h}_M_eq" "$T/$h.c" "$T/mut_M_eq"
done
echo T4_DONE
