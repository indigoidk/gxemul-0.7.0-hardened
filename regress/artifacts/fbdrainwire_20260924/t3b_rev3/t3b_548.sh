#!/bin/bash
# #548 revision 3: gate 2's harness (final text) x mutants, and x its own self-edits, compiled exactly as
# gate_offline.sh compiles it against build/'s objects.  Nothing in any tree is written: mutants live in /tmp.
set -u
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
MUT=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/opus548/out/p3/mutants
OUT=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/u3_cpp/pre548/t3b
T=/tmp/t3b548
rm -rf "$T"; mkdir -p "$T" "$OUT"
OBJS=$(find "$SEC/../build/src" -name '*.o' ! -name 'main.o' ! -name 'dev_footbridge.o' | sort)
PIN6='timer 0 at count 0 peak 762 end 286, timer 2 owing 4096 peak 762 end 286; want 762'
PIN6B='distinct rates: peaks 762 1525 3051 6103 want 762 1525 3051 6103'
md5sum "$SEC/regress/diff_fbpending_bound.c" "$SEC/src/devices/dev_footbridge.c" > "$OUT/INPUTS.md5"

# harness self-edits, generated from the final file
python3 - "$SEC/regress/diff_fbpending_bound.c" "$T" <<'PYEOF'
import io, sys
src, T = sys.argv[1], sys.argv[2]
s = io.open(src, encoding="utf-8", newline="").read()
d2 = "drive(r6, 2, 4096, &peak2, &trough2);"
assert s.count(d2) == 2, s.count(d2)
i = s.index(d2, s.index(d2) + 1)                     # the SECOND: after timer 2's re-arm
retarget = s[:i] + "drive(r6, 0, 4096, &peak2, &trough2);" + s[i + len(d2):]
cond = "owed0 == 0 && owed2 == 4096 && peak == 762 && peak2 == 762 &&"
assert s.count(cond) == 1
orr = s.replace(cond, "owed0 == 0 || owed2 == 4096 || peak == 762 || peak2 == 762 ||").replace(
    "end0 >= 1 && end0 <= 762 && end2 >= 1 && end2 <= 762,", "end0 >= 1 || end0 <= 762 || end2 >= 1 || end2 <= 762,")
assert orr != s
pre = s.replace("drive(r6, 2, 4096, &peak2, &trough2);\t\t/*  4096 owed  */", "drive(r6, 2, 0, &peak2, &trough2);\t\t/*  4096 owed  */")
assert pre != s
for name, text in (("H_retarget", retarget), ("H_or", orr), ("H_pre0", pre)):
    io.open(T + "/" + name + ".c", "w", encoding="utf-8", newline="").write(text)
print("harness variants written")
PYEOF

run() {   # label harness devdir
    local L=$1 H=$2 D=$3
    if ! cc -O2 -std=gnu99 -I"$D" -I"$SEC/src/include" -I"$SEC/src/include/thirdparty" -I"$SEC/src/devices" \
            -o "$T/bin_$L" "$H" $OBJS -lm -L/usr/X11R6/lib -lX11 > "$OUT/cc_$L.log" 2>&1; then
        echo "$L  COMPILE_FAILED"; return
    fi
    "$T/bin_$L" 2147487744 > "$OUT/run_$L.log" 2>&1
    printf '%-22s PASS=%s R6=%-4s R6b=%-4s IDENT=%-4s pinR6=%s pinR6b=%s | %s\n' "$L" \
        "$(grep -c '^FBBOUND_PASS$' "$OUT/run_$L.log")" \
        "$(grep -E '^  (ok|FAIL) +R6 a re-armed' "$OUT/run_$L.log" | awk '{print $1}')" \
        "$(grep -E '^  (ok|FAIL) +R6b ' "$OUT/run_$L.log" | awk '{print $1}')" \
        "$(grep -E '^  (ok|FAIL) +IDENTITY' "$OUT/run_$L.log" | awk '{print $1}')" \
        "$(grep -cF "$PIN6" "$OUT/run_$L.log")" "$(grep -cF "$PIN6B" "$OUT/run_$L.log")" \
        "$(grep -E 'R6 a re-armed' "$OUT/run_$L.log" | sed 's/.*Hz: //' | cut -c1-80)"
}

HF="$SEC/regress/diff_fbpending_bound.c"
run base "$HF" "$SEC/src/devices"
for m in M_eq M_idle M_pendguard M_frozen M_idx0 M_cmp0 M_pct3 M_rst2 M_neqB M_zge M_lowonly M_nobound M_x2; do
    mkdir -p "$T/mut_$m"; cp "$MUT/$m.c" "$T/mut_$m/dev_footbridge.c"
    run "$m" "$HF" "$T/mut_$m"
done
for h in H_retarget H_or H_pre0; do
    run "${h}_base" "$T/$h.c" "$SEC/src/devices"
    run "${h}_M_eq" "$T/$h.c" "$T/mut_M_eq"
done
echo T3B_DONE
