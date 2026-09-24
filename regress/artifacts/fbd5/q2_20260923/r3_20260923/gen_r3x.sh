#!/bin/bash
# #545 repair 3 (r3x) table, step 1: build every variant's MUTATED dev_footbridge.c into $V.
# The carried / closing / codex mutators are the same commands run_q2b_old.sh, run_closing2.sh and run_codexv.sh
# used; they mutate a scratch tree ($G), which carries a .MUTANT sentinel until it is restored and cmp'd against SEC.
# The Opus seat's 570 come from its own gen_variants.py (old -> new, each anchor exactly once in the fix).
set -u
R=/mnt/c/DocumentNoSnc/CC/GXEMUL
SEC=$R/GXEMUL-SEC
I=$R/_scratchpad/fbd5/impl
Z=$R/_scratchpad/fbd5/q2d/r3x
V=/tmp/fbd5r3x_var
G=/tmp/fbd5r3x_gen
rm -rf "$V" "$G"; mkdir -p "$V" "$G"; cp -a "$SEC/src" "$G/src"
cp "$SEC/src/devices/dev_footbridge.c" "$G/FIX.c"; cp "$G/FIX.c" "$V/FIX.c"
echo "#545 r3x variant generation -- restore from FIX.c" > "$G/.MUTANT"
F=$G/src/devices/dev_footbridge.c
X=$G
for M in Q1 Q2 Q3 Q4 Q5 W1 W2 T1 T2 M1 M2 M3 M4 M5 M6 M7 M8 M9 M10 M11 A1 A2 A3 A4 B1 B2 B3 G1 G2 Z1 Z1b Z2 Z3 Z4 Z5 Z6 Z7 Z7b Z8 Z9 M1b M1c M1d M1e F1 F1b F1c F2 F2b F3 F3b F4 F4b F4c F5 F5b F7 F7b S1 S2 S3 S4 S5 S6 S7 S8 S9 S10 S11 S12 S13 S14 V1 V2 V3 V4 V5 V6 V7 V8 V9 V10; do
    cp "$X/FIX.c" "$F"
    case $M in
        Q*|W*) python3 "$I/mkmut_q2.py" "$X" "$M" > /dev/null || { echo "$M NOAPPLY"; continue; } ;;
        T1)  sed -i 's/\t\t\todata = d->irq_status;$/\t\t\todata = d->irq_status \& 0xff;/' "$F" ;;
        T2)  sed -i 's/odata = d->fiq_status \& d->fiq_enable;/odata = (d->fiq_status \& d->fiq_enable) \& 0xff;/' "$F" ;;
        F*)  python3 "$R/_scratchpad/fbd5/opus_f2_20260919/mkmut_f2.py" "$X" "$M" > /dev/null || { echo "$M NOAPPLY"; continue; } ;;
        M1b|M1c|M1d|M1e|Z*) python3 "$I/mkmut_p2b.py" "$X" "$M" > /dev/null || { echo "$M NOAPPLY"; continue; } ;;
        M*)  python3 "$I/mkmut_fbd5.py" "$X" "$M" > /dev/null || { echo "$M NOAPPLY"; continue; } ;;
        A4)  sed -i 's/else if (!d->warned_fiq_status_w) {/else if (len == 4 \&\& !d->warned_fiq_status_w) {/' "$F" ;;
        S*)  python3 "$I/mkmut_closing.py" "$X" "$M" > /dev/null || { echo "$M NOAPPLY"; continue; } ;;
        V*)  python3 "$I/mkmut_codexv.py" "$X" "$M" > /dev/null || { echo "$M NOAPPLY"; continue; } ;;
        *)   python3 "$R/_scratchpad/fbd5/opus_p2_20260919/mkmut_p2.py" "$X" "$M" > /dev/null || { echo "$M NOAPPLY"; continue; } ;;
    esac
    if cmp -s "$X/FIX.c" "$F"; then echo "$M NOOP"; continue; fi
    cp "$F" "$V/$M.c"; echo "$M ok $(md5sum "$F" | cut -c1-8)"
done
cp "$X/FIX.c" "$F"
if cmp -s "$F" "$SEC/src/devices/dev_footbridge.c"; then rm -f "$G/.MUTANT"; echo "GEN TREE RESTORED (cmp == SEC)"; else echo "GEN TREE NOT RESTORED"; fi
python3 "$Z/gen_opus_r3x.py" "$V"
echo "VARIANT FILES: $(ls "$V" | grep -c '\.c$') (including FIX.c)"
echo GEN_DONE
