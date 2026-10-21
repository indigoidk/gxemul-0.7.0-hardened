#!/bin/bash
# kt568c.sh -- the M_IDATA measurement for #568 (vmedefaultkill): kt568.sh (table 1) with ONLY its locations changed -- the clone
# is /tmp/gxkt568c, outputs go to killtable1/idata, and the probe and the machine_mvme88k.c reference are table 1's
# frozen copies (the same instrument for both tables).  Run under WSL Gentoo:
#     MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash /mnt/c/.../killtable1/idata/kt568c.sh <subcommand> [args]
# Mutates ONLY the scratch clone /tmp/gxkt568c; writes ONLY under $OUT.  Every subcommand ends in echo, never in a
# comparison (a trailing diff/cmp status once killed a runner before its measurements).
#   setup            tar of `git archive 1a59a47e' on STDIN -> /tmp/gxkt568c (refuses an existing dir); pristine md5s;
#                    an md5 manifest of every archived file; configure; make -j4 (the HEAD build)
#   fix              install dev_vme.fix568.c (md5 4e3e7fc2) -> BASE; sentinel; rebuild
#   leg <LEG>...     per LEG: the sentinel names it; install legs/src/<LEG>.*; rebuild; a fresh binary -> run the frozen
#                    probe as <LEG>; no fresh binary -> the compiler error is recorded as legs/<LEG>.raw
#   run <LABEL>      the frozen probe on the current binary -> legs/<LABEL>.raw (+ .exit); one re-run if the
#                    completion line is missing (the incomplete output is kept as .incomplete1)
#   snapdrift        (once, right after setup) md5s of the archived files the HEAD build regenerates (src/*/.index)
#   restore          fix568 + the pristine machine_mvme88k.c back; cmp both against their sources; rebuild; every
#                    other archived file re-checked against the manifest (the build-regenerated ones against their
#                    post-HEAD-build snapshot); freshness -> build/RESTORE.status
#   clearsentinel    removes .MUTANT ONLY if RESTORE_OK, legs/BASE_FINAL.raw is 34/34 CONTROL=OK with its completion
#                    line, both sources still cmp clean, and the binary is newer than both
#   cleanup          removes /tmp/gxkt568c ONLY if no .MUTANT is present
# Every build first removes dev_vme.o, machine_mvme88k.o and gxemul, so a failed build leaves NO binary: a stale one can
# never be measured, and `[ gxemul -nt <source> ]' is checked anyway (make's status has read 0 on a failed build).
set -u
OUT=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/vme/killtable1/idata
T1=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/vme/killtable1
FIX=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/vme/fix/dev_vme.fix568.c
FIXMD5=4e3e7fc220062b429f7d9d6e140fec9e
HEADVMEMD5=2516a82bc777fe780f2dc6ccc00fd6c3
MACHREF=$T1/ref/machine_mvme88k.head.c
MACHMD5=c1edc233de21c6fbd7494f34c05be759
PROBE=$T1/vme_default_probe.frozen.py
PROBEMD5=19de15b3ea69af28e437cdf92e22c97e
MANIFEST=$OUT/ref/archive_1a59a47e.md5
DRIFTSNAP=$OUT/ref/postbuild_HEAD_regenerated.md5
W=/tmp/gxkt568c
VME=src/devices/dev_vme.c
MACH=src/machines/machine_mvme88k.c
LOG=$OUT/RUNLOG.txt
BUILD_FRESH=NO

say() { echo "$(date '+%F %T') $*" | tee -a "$LOG"; }
m5() { md5sum "$1" 2>/dev/null | cut -d' ' -f1; }

#  archived files whose md5 no longer matches the manifest, one per line (dev_vme.c included)
tree_drift() { (cd "$W" && md5sum -c "$MANIFEST" 2>/dev/null | grep -v ': OK$'); }

build() {   # $1 = label; the caller has installed the sources
    local L="$1" BL="$OUT/build/$1.build.log" rc t0 t1
    cd "$W" || { say "BUILD $L NO_CLONE"; BUILD_FRESH=NO; return 3; }
    rm -f src/devices/dev_vme.o src/machines/machine_mvme88k.o gxemul
    t0=$(date +%s)
    make -j4 > "$BL" 2>&1
    rc=$?
    t1=$(date +%s)
    if [ -f gxemul ] && [ gxemul -nt $VME ] && [ gxemul -nt $MACH ]; then BUILD_FRESH=yes; else BUILD_FRESH=NO; fi
    say "BUILD $L make_rc=$rc fresh=$BUILD_FRESH secs=$((t1 - t0)) gxemul=$(m5 gxemul) dev_vme.c=$(m5 $VME) machine=$(m5 $MACH) warnings=$(grep -ci warning "$BL")"
}

runprobe() {   # $1 = LABEL
    local L="$1" O="$OUT/legs/$1.raw" rc=99 a t0=0 t1=0
    cd "$W" || { say "RUN $L NO_CLONE"; return 3; }
    if [ "$(m5 "$PROBE")" != "$PROBEMD5" ]; then say "RUN $L PROBE_MD5_MISMATCH $(m5 "$PROBE")"; return 4; fi
    if [ ! -x gxemul ]; then say "RUN $L NO_BINARY"; return 3; fi
    for a in 1 2; do
        t0=$(date +%s)
        echo "PROBE_MD5 $(m5 "$PROBE")  BINARY_MD5 $(m5 gxemul)  DEV_VME_MD5 $(m5 $VME)  MACHINE_MD5 $(m5 $MACH)  LABEL $L  ATTEMPT $a  $(date '+%F %T')" > "$O"
        python3 -u -B -I "$PROBE" "$W/gxemul" "$L" >> "$O" 2>&1
        rc=$?
        t1=$(date +%s)
        echo "PROBE_EXIT=$rc" > "$O.exit"
        if [ "$(tail -n 1 "$O")" = "VME_DEFAULT_PROBE_DONE" ]; then break; fi
        if [ "$a" = 1 ]; then
            cp "$O" "$O.incomplete1"
            say "RUN $L attempt 1 INCOMPLETE (no completion line; kept as $L.raw.incomplete1) -- re-running"
        fi
    done
    say "RUN $L rc=$rc secs=$((t1 - t0)) $(grep -m1 '^VME_DEFAULT_RESULT=' "$O") $(grep -m1 '^VME_DEFAULT_CONTROL=' "$O") last=[$(tail -n 1 "$O")]"
}

do_setup() {
    local v m n rc
    if [ -e "$W" ]; then say "SETUP REFUSED: $W already exists -- not reusing a tree this run did not make"; return 3; fi
    mkdir -p "$W" && cd "$W" || { say "SETUP MKDIR_FAILED"; return 3; }
    tar -x || { say "SETUP TAR_FAILED"; return 3; }
    v=$(m5 $VME); m=$(m5 $MACH)
    if [ "$v" != "$HEADVMEMD5" ] || [ "$m" != "$MACHMD5" ]; then
        say "SETUP PRISTINE_MISMATCH dev_vme.c=$v machine=$m"; return 4
    fi
    find . -type f -print0 | sort -z | xargs -0 md5sum > "$MANIFEST"
    n=$(wc -l < "$MANIFEST")
    say "SETUP extracted 1a59a47e: $n files; dev_vme.c=$v (HEAD) machine=$m -- manifest ref/archive_1a59a47e.md5"
    ./configure > "$OUT/build/configure.log" 2>&1
    rc=$?
    say "SETUP configure rc=$rc"
    build HEAD
    say "SETUP archived files changed by configure+make (expected none): [$(tree_drift | tr '\n' ' ')]"
}

do_fix() {
    cd "$W" || { say "FIX NO_CLONE"; return 3; }
    echo "BASE: $VME = dev_vme.fix568.c (md5 $FIXMD5) over HEAD 1a59a47e -- scratch clone; cleared only after the final restore + BASE_FINAL ($(date '+%F %T'))" > "$W/.MUTANT"
    cp "$FIX" $VME || { say "FIX COPY_FAILED"; return 4; }
    if [ "$(m5 $VME)" != "$FIXMD5" ]; then say "FIX MD5_MISMATCH $(m5 $VME)"; return 4; fi
    say "FIX installed dev_vme.c=$(m5 $VME)"
    build BASE
}

do_leg() {   # $1 = LEG
    local L="$1" S
    cd "$W" || { say "LEG $L NO_CLONE"; return 3; }
    if [ "$L" = NULL ]; then
        S="$OUT/legs/src/NULL.machine_mvme88k.c"
        [ -f "$S" ] || { say "LEG $L NO_SOURCE"; return 3; }
        echo "MUTANT $L: $MACH = legs/src/NULL.machine_mvme88k.c (vme device_add removed, md5 $(m5 "$S")); $VME = fix568 -- restore with idata/kt568c.sh restore ($(date '+%F %T'))" > "$W/.MUTANT"
        cp "$FIX" $VME && cp "$S" $MACH || { say "LEG $L COPY_FAILED"; return 4; }
        if [ "$(m5 $VME)" != "$FIXMD5" ] || [ "$(m5 $MACH)" != "$(m5 "$S")" ]; then say "LEG $L INSTALL_MD5_MISMATCH"; return 4; fi
    else
        S="$OUT/legs/src/$L.dev_vme.c"
        [ -f "$S" ] || { say "LEG $L NO_SOURCE"; return 3; }
        echo "MUTANT $L: $VME = legs/src/$L.dev_vme.c (md5 $(m5 "$S")), a one-edit variant of fix568 -- restore with idata/kt568c.sh restore ($(date '+%F %T'))" > "$W/.MUTANT"
        if [ "$(m5 $MACH)" != "$MACHMD5" ]; then
            cp "$MACHREF" $MACH
            say "LEG $L machine_mvme88k.c was not pristine -- restored from ref first ($(m5 $MACH))"
        fi
        cp "$S" $VME || { say "LEG $L COPY_FAILED"; return 4; }
        if [ "$(m5 $VME)" != "$(m5 "$S")" ]; then say "LEG $L INSTALL_MD5_MISMATCH"; return 4; fi
    fi
    say "LEG $L installed: dev_vme.c=$(m5 $VME) machine=$(m5 $MACH)"
    build "$L"
    if [ "$BUILD_FRESH" = yes ]; then
        runprobe "$L"
    else
        {
            echo "BUILD_FAILED $L -- no fresh binary (gxemul was removed before the build, so nothing stale was measured)"
            echo "dev_vme.c md5 $(m5 $VME)  machine md5 $(m5 $MACH)  make log: build/$L.build.log  $(date '+%F %T')"
            grep -nE 'error|Error' "$OUT/build/$L.build.log" | head -20
            echo "KT568_BUILD_FAILED_RECORDED"
        } > "$OUT/legs/$L.raw"
        say "LEG $L BUILD FAILED -- recorded in legs/$L.raw: $(grep -m1 -E 'error' "$OUT/build/$L.build.log")"
    fi
}

do_restore() {
    local c1 c2 drift R
    cd "$W" || { say "RESTORE NO_CLONE"; return 3; }
    echo "RESTORE in progress ($(date '+%F %T')): $VME <- dev_vme.fix568.c, $MACH <- ref/machine_mvme88k.head.c; cleared only after BASE_FINAL passes" > "$W/.MUTANT"
    cp "$FIX" $VME && cp "$MACHREF" $MACH || { say "RESTORE COPY_FAILED"; echo "RESTORE_FAILED copy" > "$OUT/build/RESTORE.status"; return 4; }
    if cmp -s $VME "$FIX"; then c1=clean; else c1=DIFFERS; fi
    if cmp -s $MACH "$MACHREF"; then c2=clean; else c2=DIFFERS; fi
    build RESTORE
    #  After the rebuild: every archived file must match the archive, except dev_vme.c (the fix, by design) and the
    #  files the HEAD build itself regenerates (snapdrift: src/devices/.index, src/machines/.index), which must match
    #  their post-HEAD-build snapshot byte for byte.
    drift=$(tree_drift | grep -vx "./$VME: FAILED" | sed 's/: FAILED$//' | sort | tr '\n' ' ')
    want=$(cut -d' ' -f3- "$DRIFTSNAP" | sort | tr '\n' ' ')
    if (cd "$W" && md5sum -c --quiet "$DRIFTSNAP" > /dev/null 2>&1); then snap=match; else snap=DIFFERS; fi
    if [ "$c1" = clean ] && [ "$c2" = clean ] && [ "$drift" = "$want" ] && [ "$snap" = match ] && [ "$BUILD_FRESH" = yes ]; then
        R=RESTORE_OK
    else
        R=RESTORE_FAILED
    fi
    say "$R: dev_vme.c cmp vs fix568=$c1; machine_mvme88k.c cmp vs 1a59a47e=$c2; archived files differing from the archive (besides dev_vme.c)=[${drift}] want=[${want}] post-HEAD-build snapshot=$snap; rebuilt fresh=$BUILD_FRESH"
    echo "$R $(date '+%F %T') dev_vme=$c1 machine=$c2 drift=[${drift}] want=[${want}] snapshot=$snap fresh=$BUILD_FRESH" > "$OUT/build/RESTORE.status"
}

do_snapdrift() {   # record the md5s of the archived files the HEAD build regenerated (run once, right after setup)
    cd "$W" || { say "SNAPDRIFT NO_CLONE"; return 3; }
    if [ -e "$W/.MUTANT" ] || [ "$(m5 $VME)" != "$HEADVMEMD5" ]; then say "SNAPDRIFT REFUSED: the tree is not the HEAD build"; return 4; fi
    tree_drift | sed 's/: FAILED$//' | xargs -r md5sum > "$DRIFTSNAP"
    say "SNAPDRIFT post-HEAD-build md5s of the build-regenerated archived files: $(tr '\n' ' ' < "$DRIFTSNAP")"
}

do_clear() {
    local O="$OUT/legs/BASE_FINAL.raw"
    cd "$W" || { say "CLEAR NO_CLONE"; return 3; }
    if grep -q '^RESTORE_OK' "$OUT/build/RESTORE.status" 2>/dev/null \
        && [ "$(tail -n 1 "$O" 2>/dev/null)" = "VME_DEFAULT_PROBE_DONE" ] \
        && grep -qx 'VME_DEFAULT_RESULT=34/34' "$O" && grep -qx 'VME_DEFAULT_CONTROL=OK' "$O" \
        && cmp -s $VME "$FIX" && cmp -s $MACH "$MACHREF" && [ gxemul -nt $VME ] && [ gxemul -nt $MACH ]; then
        rm -f "$W/.MUTANT"
        say "SENTINEL CLEARED: RESTORE_OK, BASE_FINAL 34/34 CONTROL=OK, both sources cmp clean, binary newer than both"
    else
        say "SENTINEL KEPT -- a clearance condition failed"
    fi
}

do_cleanup() {
    if [ -e "$W/.MUTANT" ]; then say "CLEANUP REFUSED: $W/.MUTANT present"; return 3; fi
    case "$W" in
        /tmp/gxkt568c) rm -rf -- "$W" ;;
    esac
    if [ -e "$W" ]; then say "CLEANUP FAILED: $W still present"; else say "CLEANUP DONE: $W removed"; fi
}

cmd="${1:-}"
[ $# -gt 0 ] && shift
case "$cmd" in
    setup) do_setup ;;
    fix) do_fix ;;
    run) runprobe "${1:?label}" ;;
    leg) for L in "$@"; do do_leg "$L"; done ;;
    snapdrift) do_snapdrift ;;
    restore) do_restore ;;
    clearsentinel) do_clear ;;
    cleanup) do_cleanup ;;
    sentinel) if [ -e "$W/.MUTANT" ]; then echo "SENTINEL: $(cat "$W/.MUTANT")"; else echo "SENTINEL: none"; fi ;;
    *) echo "usage: kt568c.sh setup|fix|leg <LEG>...|run <LABEL>|restore|clearsentinel|cleanup|sentinel" ;;
esac
echo "KT568_SH_DONE $cmd"
