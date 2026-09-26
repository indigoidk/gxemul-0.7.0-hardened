#!/bin/bash
#  #551 pass 1, opus seat: build every harness variant against every dev_wdc.c variant, run, save.
set -u
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus551p1
W=/tmp/opus551p1
ORIG=$W/sec/regress/diff_wdc_identify.c
export W
export FLAGS="-std=c99 -I$W/sec/src/include -I$W/sec/src/include/thirdparty -ffunction-sections -fdata-sections -Wl,--gc-sections"

mkdir -p $W/h
echo 'int quiet_mode = 0;' > $W/stub_qm.c
X() { python3 $SP/xform.py make "$ORIG" "$W/h/$1.c" "$2" "${@:3}" > /dev/null || echo "XFORM FAILED $1"; }
X ORIG      ORIG
X A         A
X Abad      Abad
X Ahard     A+hard
for e in E_ret0 E_noret E_nocnt E_eq1 E_uchar E_after3 E_rows; do
    X "$e"      "$e"
    X "${e}_h"  "$e+hard"
done
X Tdrop     A+drop    1576
X Tdouble   A+double  1576
X ORIGF     ORIG+force
X AF        A+force
X AhardF    A+hard+force
X TdropF    A+drop+force   1576
X TdoubleF  A+double+force 1576
echo "variants: $(ls $W/h | wc -l)"

for dev in $W/dev/*/; do cp $W/h/*.c "$dev/regress/"; done

one() {   # harness dev opt
    local h=$1 dev=$2 opt=$3 d=$W/dev/$2/regress
    local out=$d/$h.$opt
    rm -f "$out" "$out.log" "$out.rc"
    local stub=""
    #  -O0 does not LINK with gate 2's flags at HEAD (3 x undefined quiet_mode): both arms
    #  get the same one-line stub object, and only at -O0.
    [ "$opt" = O0 ] && stub="$W/stub_qm.c"
    if cc -$opt $FLAGS -o "$out" "$d/$h.c" $stub > "$out.cc" 2>&1 && [ "$out" -nt "$d/$h.c" ]; then
        timeout 300 "$out" > "$out.log" 2>&1
        echo $? > "$out.rc"
    else
        echo BUILD_FAIL > "$out.rc"
    fi
}
export -f one

{
    for dev in pristine selfmut rev255 cyl13 srstbit; do
        for o in O0 O1 O2; do echo "ORIG $dev $o"; echo "A $dev $o"; echo "Ahard $dev $o"; done
        for e in E_ret0 E_noret E_nocnt E_eq1 E_uchar E_after3 E_rows; do
            echo "$e $dev O2"; echo "${e}_h $dev O2"
        done
        echo "Tdrop $dev O2"; echo "Tdouble $dev O2"
    done
    echo "Abad pristine O2"
    for h in ORIGF AF AhardF TdropF TdoubleF; do echo "$h pristine O2"; done
} > $W/jobs.txt
echo "jobs: $(wc -l < $W/jobs.txt)"
t0=$(date +%s)
xargs -P 6 -L 1 bash -c 'one "$@"' _ < $W/jobs.txt
echo "built+ran in $(( $(date +%s) - t0 )) s"
grep -l BUILD_FAIL $W/dev/*/regress/*.rc | sed "s|$W/dev/||" | tr '\n' ' '; echo
echo RUNALL_DONE
