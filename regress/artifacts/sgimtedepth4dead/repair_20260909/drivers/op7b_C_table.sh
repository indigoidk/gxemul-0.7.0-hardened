#!/bin/bash
# Stage C: the whole kill table, eleven mutants, one frozen instrument.
#
# NO `set -e' anywhere: the probe exits 1 on a red row, and a driver that dies on a
# comparison is how a measurement silently does not happen.
#
# Order per mutant: sentinel FIRST -> restore from SEC -> apply -> verify the diff is the
# edit and nothing else -> rm the .o -> make -> check [ binary -nt source ] -> run.
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
CL=/tmp/gxopus7g1b
F=src/devices/dev_sgi_re.c
OUT=$CL/logs
P=sgi_mte_fill_probe.REPAIRED.py
MUT=/tmp/op7b_mutate.py

echo "=== STAGE C (TABLE)  $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "frozen probe md5: $(md5sum $CL/probe/$P | cut -c1-32)"

run_one () {
    NAME="$1"; KIND="$2"; OLD="$3"; NEW="$4"; WANTMARK="$5"
    echo
    echo "############################################################ $NAME  $(date -u +%H:%M:%SZ)"

    # --- sentinel BEFORE any mutation ---
    printf '%s\n' "/tmp/gxopus7g1b/.MUTANT: $F  $NAME: $KIND [$OLD] -> [$NEW].  RESTORE FROM $SEC/$F (NEVER from a local backup), then rm src/devices/dev_sgi_re.o and rebuild, then cmp vs SEC AND check [ gxemul -nt $F ] before clearing this file." > "$CL/.MUTANT"

    # --- restore from SEC, then apply ---
    cp "$SEC/$F" "$CL/$F" || { echo "$NAME-FAIL: restore cp"; return 9; }
    cmp -s "$CL/$F" "$SEC/$F" || { echo "$NAME-FAIL: restore differs"; return 9; }
    python3 "$MUT" "$CL/$F" "$KIND" "$OLD" "$NEW" || { echo "$NAME-FAIL: mutator"; return 9; }

    # --- verify the diff IS the edit ---
    diff "$SEC/$F" "$CL/$F" > "/tmp/op7b_$NAME.diff" 2>&1
    NMARK=$(grep -cE '^[<>]' "/tmp/op7b_$NAME.diff")
    echo "-- diff vs SEC --"; cat "/tmp/op7b_$NAME.diff"
    echo "CHANGED_LINE_MARKERS=$NMARK  want=$WANTMARK"
    [ "$NMARK" != "$WANTMARK" ] && { echo "$NAME-FAIL: unexpected diff size"; return 9; }

    # --- rebuild ---
    cd "$CL" || return 9
    rm -f src/devices/dev_sgi_re.o
    make -j4 > "/tmp/op7b_build_$NAME.log" 2>&1; MRC=$?
    echo "MAKE_RC=$MRC (not trusted alone)"
    if [ -x "$CL/gxemul" ] && [ "$CL/gxemul" -nt "$CL/$F" ]; then
        echo "FRESHNESS=OK"
    else
        echo "$NAME-FAIL: freshness"; ls -la --time-style=full-iso "$CL/gxemul" "$CL/$F"
        tail -5 "/tmp/op7b_build_$NAME.log"; return 9
    fi
    echo "BIN_MD5=$(md5sum $CL/gxemul | cut -c1-32)"

    # --- measure ---
    cd "$CL/probe" || return 9
    python3 -u ./$P "$CL/gxemul" "$NAME" > "$OUT/$NAME.raw" 2>&1
    echo "PROBE_RC=$?"
    echo "SENTINEL: $(tail -1 "$OUT/$NAME.raw")"
    grep -E '^MTEFILL_RESULT=' "$OUT/$NAME.raw"
    echo "RED ROWS ($(grep -c 'FAIL$' "$OUT/$NAME.raw")):"
    grep 'FAIL$' "$OUT/$NAME.raw" | cut -c1-100
    return 0
}

#          NAME          KIND     OLD                              NEW                                          MARKERS
run_one M_tlbA       replace 'if (depth == 32) {'          'if (depth == 32 && dst_tlb == MTE_TLB_A) {'   2
run_one M_tlbAB      replace 'if (depth == 32) {'          'if (depth == 32 && dst_tlb != MTE_TLB_C) {'   2
run_one M1_reinstate replace 'if (depth == 32) {'          'if (depth == 4) {'                            2
run_one M2_nodst     delete  'dst_mode |= DE_MODE_TYPE_RGBA;' ''                                          1
run_one M3_nosrc     delete  'src_mode |= DE_MODE_TYPE_RGBA;' ''                                          1
run_one M4_copyonly  replace 'if (depth == 32) {'          'if (depth == 32 && (mode & MTE_MODE_COPY)) {' 2
run_one M5_dstrgb    replace 'dst_mode |= DE_MODE_TYPE_RGBA;' 'dst_mode |= DE_MODE_TYPE_RGB;'             2
run_one M6_ge16      replace 'if (depth == 32) {'          'if (depth >= 16) {'                           2
run_one M7_ne8       replace 'if (depth == 32) {'          'if (depth != 8) {'                            2
run_one M8_srcrgb    replace 'src_mode |= DE_MODE_TYPE_RGBA;' 'src_mode |= DE_MODE_TYPE_RGB;'             2
run_one M9_ge32      replace 'if (depth == 32) {'          'if (depth >= 32) {'                           2

echo
echo "=== TABLE RUNS COMPLETE  $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "STAGE_C_DONE"
