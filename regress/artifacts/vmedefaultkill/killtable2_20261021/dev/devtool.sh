#!/bin/bash
# devtool.sh -- #568 REPAIR 1, the DEVELOPMENT clone /tmp/gxkt568dev (WSL Gentoo).  Two jobs only:
#   (1) the fix568 / fix568b dev_vme.o comparison (objdump), and
#   (2) the rev-3 probe's DEVELOPMENT runs -- BASE (fix568b), HEAD and NULL only.  NO mutant leg is ever built here:
#       mutants are table 2's, and table 2 runs in its own fresh clone AFTER PRETABLE2 is written.
# Mutates ONLY /tmp/gxkt568dev; writes ONLY under rev3/.  The clone carries a .MUTANT sentinel naming what it holds
# while it exists and is DELETED at the end (cleanup) -- nothing in it is measured again, so no restore is owed.
# Every build removes dev_vme.o, machine_mvme88k.o and gxemul first and checks `[ gxemul -nt <source> ]' after.
# Ends in echo, never in a comparison.
#   setup                         tar of `git archive 1a59a47e' on STDIN -> the clone; pristine md5s; configure; make
#   objcmp                        build dev_vme.o from fix568 and from fix568b; objdump both; diff -> rev3/obj/
#   install head|fix568b|null     sources in place (null = fix568b + machine_mvme88k.c without the vme device_add)
#   run <label> <probe.py>        the given probe on the current binary -> rev3/dev/<label>.raw (+ .exit)
#   cleanup                       delete the clone
set -u
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/vme
R=$S/rev3
FIX568=$S/fix/dev_vme.fix568.c
FIX568MD5=4e3e7fc220062b429f7d9d6e140fec9e
FIX568B=$R/dev_vme.fix568b.c
FIX568BMD5=beb120eae1be112b682bd528f103191c
HEADVMEMD5=2516a82bc777fe780f2dc6ccc00fd6c3
MACHREF=$S/killtable1/ref/machine_mvme88k.head.c
MACHMD5=c1edc233de21c6fbd7494f34c05be759
NULLMACH=$S/killtable1/legs/src/NULL.machine_mvme88k.c
NULLMD5=d820d3b3a61f93930ba87b97edcc486a
W=/tmp/gxkt568dev
VME=src/devices/dev_vme.c
MACH=src/machines/machine_mvme88k.c
LOG=$R/dev/DEVLOG.txt
BUILD_FRESH=NO

say() { echo "$(date '+%F %T') $*" | tee -a "$LOG"; }
m5() { md5sum "$1" 2>/dev/null | cut -d' ' -f1; }

build() {   # $1 = label
    local L="$1" BL="$R/dev/build_$1.log" rc t0 t1
    cd "$W" || { say "BUILD $L NO_CLONE"; BUILD_FRESH=NO; return 3; }
    rm -f src/devices/dev_vme.o src/machines/machine_mvme88k.o gxemul
    t0=$(date +%s); make -j4 > "$BL" 2>&1; rc=$?; t1=$(date +%s)
    if [ -f gxemul ] && [ gxemul -nt $VME ] && [ gxemul -nt $MACH ]; then BUILD_FRESH=yes; else BUILD_FRESH=NO; fi
    say "BUILD $L make_rc=$rc fresh=$BUILD_FRESH secs=$((t1 - t0)) gxemul=$(m5 gxemul) dev_vme.c=$(m5 $VME) machine=$(m5 $MACH) warnings=$(grep -ci warning "$BL")"
}

do_setup() {
    if [ -e "$W" ]; then say "SETUP REFUSED: $W exists"; return 3; fi
    mkdir -p "$W" && cd "$W" || { say "SETUP MKDIR_FAILED"; return 3; }
    tar -x || { say "SETUP TAR_FAILED"; return 3; }
    if [ "$(m5 $VME)" != "$HEADVMEMD5" ] || [ "$(m5 $MACH)" != "$MACHMD5" ]; then say "SETUP PRISTINE_MISMATCH"; return 4; fi
    say "SETUP extracted 1a59a47e: $(find . -type f | wc -l) files; dev_vme.c and machine_mvme88k.c pristine"
    ./configure > "$R/dev/configure.log" 2>&1; say "SETUP configure rc=$?"
    build HEAD
}

do_install() {   # $1 = head | fix568b | null
    cd "$W" || { say "INSTALL NO_CLONE"; return 3; }
    case "$1" in
        head)    git_free_head ;;
        fix568b) echo "DEV: $VME = fix568b (md5 $FIX568BMD5), machine pristine -- development clone, deleted at the end" > .MUTANT
                 cp "$FIX568B" $VME && cp "$MACHREF" $MACH ;;
        null)    echo "DEV: $VME = fix568b, $MACH = NULL (vme device_add removed) -- development clone, deleted at the end" > .MUTANT
                 cp "$FIX568B" $VME && cp "$NULLMACH" $MACH ;;
        *) say "INSTALL unknown $1"; return 2 ;;
    esac
    say "INSTALL $1: dev_vme.c=$(m5 $VME) machine=$(m5 $MACH)"
    build "$1"
}

git_free_head() {   # restore the two files to 1a59a47e's bytes (the references are md5-pinned copies of HEAD)
    echo "DEV: restoring HEAD's dev_vme.c and machine_mvme88k.c -- development clone, deleted at the end" > .MUTANT
    cp "$S/fix/dev_vme.head.c" $VME && cp "$MACHREF" $MACH
    if [ "$(m5 $VME)" != "$HEADVMEMD5" ] || [ "$(m5 $MACH)" != "$MACHMD5" ]; then say "HEAD RESTORE MD5 MISMATCH"; fi
}

do_objcmp() {
    local O=$R/obj v src want
    cd "$W" || { say "OBJCMP NO_CLONE"; return 3; }
    echo "DEV: objcmp in progress (dev_vme.c swapped fix568 / fix568b) -- development clone, deleted at the end" > .MUTANT
    for v in fix568 fix568b; do
        if [ $v = fix568 ]; then src=$FIX568; want=$FIX568MD5; else src=$FIX568B; want=$FIX568BMD5; fi
        cp "$src" $VME
        if [ "$(m5 $VME)" != "$want" ]; then say "OBJCMP $v SOURCE MD5 MISMATCH"; return 4; fi
        build "obj_$v"
        if [ "$BUILD_FRESH" != yes ] || [ ! src/devices/dev_vme.o -nt $VME ]; then say "OBJCMP $v BUILD NOT FRESH"; return 4; fi
        cp src/devices/dev_vme.o "$O/dev_vme.$v.o"
        objdump -d "$O/dev_vme.$v.o" > "$O/$v.objdump-d.txt"
        objdump -dr "$O/dev_vme.$v.o" > "$O/$v.objdump-dr.txt"
        objdump -s -j .rodata.str1.1 -j .rodata.str1.8 "$O/dev_vme.$v.o" > "$O/$v.rodata.txt" 2>&1
        size -A "$O/dev_vme.$v.o" > "$O/$v.size.txt"
        grep -E ' -c -o dev_vme\.o dev_vme\.c' "$R/dev/build_obj_$v.log" | head -1 > "$O/$v.compile_line.txt"
        say "OBJCMP $v: dev_vme.c=$(m5 $VME) dev_vme.o=$(m5 "$O/dev_vme.$v.o")"
    done
    {
        echo "HOST $(uname -srm)"
        echo "COMPILER $(cc --version | head -1)"
        echo "OBJDUMP $(objdump --version | head -1)"
        echo "FLAGS fix568:  $(cat "$O/fix568.compile_line.txt")"
        echo "FLAGS fix568b: $(cat "$O/fix568b.compile_line.txt")"
    } > "$O/toolchain.txt"
    say "OBJCMP done (diffs are written by the caller)"
}

do_run() {   # $1 = label, $2 = probe path
    local L="$1" P="$2" O="$R/dev/$1.raw" rc
    cd "$W" || { say "RUN NO_CLONE"; return 3; }
    [ -x gxemul ] || { say "RUN $L NO_BINARY"; return 3; }
    echo "PROBE_MD5 $(m5 "$P")  BINARY_MD5 $(m5 gxemul)  DEV_VME_MD5 $(m5 $VME)  MACHINE_MD5 $(m5 $MACH)  LABEL $L  $(date '+%F %T')" > "$O"
    python3 -u -B -I "$P" "$W/gxemul" "$L" >> "$O" 2>&1; rc=$?
    echo "PROBE_EXIT=$rc" > "$O.exit"
    say "RUN $L rc=$rc $(grep -m1 '^VME_DEFAULT_RESULT=' "$O") $(grep -m1 '^VME_DEFAULT_CONTROL=' "$O") last=[$(tail -n 1 "$O")]"
}

do_cleanup() {
    local held="none"
    [ -e "$W/.MUTANT" ] && held="$(cat "$W/.MUTANT")"
    case "$W" in /tmp/gxkt568dev) rm -rf -- "$W" ;; esac
    if [ -e "$W" ]; then say "CLEANUP FAILED"; else say "CLEANUP DONE: $W deleted (its sentinel said: $held)"; fi
}

cmd="${1:-}"
[ $# -gt 0 ] && shift
case "$cmd" in
    setup) do_setup ;;
    objcmp) do_objcmp ;;
    install) do_install "${1:?what}" ;;
    run) do_run "${1:?label}" "${2:?probe}" ;;
    cleanup) do_cleanup ;;
    *) echo "usage: devtool.sh setup|objcmp|install head|fix568b|null|run <label> <probe>|cleanup" ;;
esac
echo "DEVTOOL_DONE $cmd"
