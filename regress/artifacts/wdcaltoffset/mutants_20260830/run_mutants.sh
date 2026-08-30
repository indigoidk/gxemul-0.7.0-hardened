#!/bin/bash
#
#  wdcaltoffset -- build the fix leg and four mutants and score them against the
#  SHIPPED witness.  Run as a FILE (`wsl ... -c` strips $VARS), from git-bash:
#
#    MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash \
#      /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/wdcaltoffset/mutants_20260830/run_mutants.sh
#
#  NOTHING UNDER THE PROJECT TREE IS BUILT OR MUTATED.  Every tree comes from
#  `git archive HEAD` into $O, so no .MUTANT sentinel is owed and the baseline is
#  MECHANICAL rather than remembered: a `cp -a` of a working tree inherits whatever
#  .o files and untracked residue sit there; `git archive` cannot.
#
#  BUILD ORDER IS DELIBERATE.  base is configured and built from scratch; each
#  mutant is then a copy of the FINISHED base tree with one source file edited, so
#  make recompiles dev_wdc.o and relinks.  That is ~30 s per leg instead of ~4 min,
#  and the stale-object hazard it trades against is closed by the three checks each
#  leg must pass: the marker is read back OFF DISK by mkmutants, the binary must
#  POSTDATE the source, and the binary must DIFFER from base's.
#
set -u
SEC=${GXSEC:-/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC}
ART="$SEC/regress/artifacts/wdcaltoffset/mutants_20260830"
O=${OUT:-/tmp/gxaltoff2}
J=${J:-8}
LOG="$O/BUILD.log"
MUTANTS="fix m1 m2 m3 m4"

mkdir -p "$O"; : > "$LOG"
say () { echo "$@" | tee -a "$LOG"; }

say "=============================================================================="
say "wdcaltoffset -- MUTANT TABLE build"
say "=============================================================================="
say "date       $(date '+%Y-%m-%d %H:%M:%S')"
say "workdir    $O"
HEAD=$(git -C "$SEC" rev-parse HEAD)
say "baseline   HEAD = $HEAD"
BUILDDIRT=$(git -C "$SEC" status --porcelain | grep -c -E '^.. (src/|configure$|Makefile\.skel$)')
say "build inputs differing from HEAD: $BUILDDIRT   (want 0)"
say ""

#  ---- 1. the baseline tree and its build --------------------------------------
for l in $MUTANTS; do rm -rf "$O/$l"; done
#  REUSE a base tree only if it is PROVABLY the one we want: its source must cmp
#  against HEAD's and its binary must postdate that source.  Otherwise rebuild from
#  scratch -- a reused tree that cannot prove itself IS the stale-binary trap.
REUSE=no
if [ -x "$O/base/gxemul" ] && [ -f "$O/base/src/devices/dev_wdc.c" ]; then
    git -C "$SEC" show HEAD:src/devices/dev_wdc.c > "$O/head_dev_wdc.c" 2>/dev/null
    if cmp -s "$O/head_dev_wdc.c" "$O/base/src/devices/dev_wdc.c"; then
        if [ "$O/base/gxemul" -nt "$O/base/src/devices/dev_wdc.c" ]; then REUSE=yes; fi
    fi
fi
if [ "$REUSE" = yes ]; then
    say "  REUSING $O/base -- source cmps against HEAD and [ binary -nt source ] holds"
else
    rm -rf "$O/base"; mkdir -p "$O/base"
    git -C "$SEC" archive HEAD | tar -x -C "$O/base" || { say "git archive FAILED"; exit 1; }
fi
if cmp -s "$O/base/src/devices/dev_wdc.c" "$SEC/src/devices/dev_wdc.c"; then
    say "  base/src/devices/dev_wdc.c == SEC working tree     IDENTICAL"
else
    say "  base/src/devices/dev_wdc.c != SEC working tree     *** DIFFERS ***"
fi
cp "$O/base/src/devices/dev_wdc.c" "$O/dev_wdc.c.pristine"

say "------------------------------------------------------------ BUILD base"
if [ "$REUSE" = yes ]; then
    say "  (reused -- not rebuilt)"
else
( cd "$O/base" && rm -f src/cpus/*.o && ./configure > "$O/configure_base.log" 2>&1 \
  && make -j"$J" > "$O/make_base.log" 2>&1 )
say "  make rc $?   (not trusted alone)"
fi
if [ ! -x "$O/base/gxemul" ]; then
    say "  *** no base/gxemul"; tail -25 "$O/make_base.log" | sed 's/^/      /' | tee -a "$LOG"
    say "MUTANTS_BUILD_DONE"; exit 1
fi
say "  binary  $(stat -c '%s bytes  %y' "$O/base/gxemul")"
say ""

#  ---- 2. the mutant trees -----------------------------------------------------
for l in $MUTANTS; do
    say "------------------------------------------------------------ BUILD $l"
    cp -a "$O/base" "$O/$l" || { say "  cp FAILED"; exit 1; }
    cp "$O/dev_wdc.c.pristine" "$O/$l/src/devices/dev_wdc.c"
    python3 "$ART/mkmutants.py" "$l" "$O/$l/src/devices/dev_wdc.c" 2>&1 | tee -a "$LOG"
    if [ ${PIPESTATUS[0]} -ne 0 ]; then say "  *** mkmutants FAILED for $l"; exit 1; fi
    diff -u "$O/dev_wdc.c.pristine" "$O/$l/src/devices/dev_wdc.c" > "$O/$l.diff"
    n=$(diff -rq "$O/base/src" "$O/$l/src" | grep -vc 'dev_wdc\.c')
    d=$(grep -c '^[+-][^+-]' "$O/$l.diff")
    say "  src files differing from base other than dev_wdc.c: $n   (want 0)"
    say "  changed lines in dev_wdc.c: $d"
    ( cd "$O/$l" && make -j"$J" > "$O/make_$l.log" 2>&1 )
    say "  make rc $?   (not trusted alone)"
    if [ ! -x "$O/$l/gxemul" ]; then
        say "  *** no $l/gxemul"; tail -25 "$O/make_$l.log" | sed 's/^/      /' | tee -a "$LOG"
        say "MUTANTS_BUILD_DONE"; exit 1
    fi
    if [ "$O/$l/gxemul" -nt "$O/$l/src/devices/dev_wdc.c" ]; then
        say "  [ binary -nt source ] YES"
    else
        say "  *** [ binary -nt source ] NO -- STALE BINARY, refusing to measure"
        say "MUTANTS_BUILD_DONE"; exit 1
    fi
    if cmp -s "$O/base/gxemul" "$O/$l/gxemul"; then
        say "  *** $l/gxemul is BYTE-IDENTICAL to base -- the edit did not reach the binary"
        say "MUTANTS_BUILD_DONE"; exit 1
    fi
    say "  differs from base binary: yes   $(stat -c '%s bytes' "$O/$l/gxemul")"
done

say ""
say "---- negative control: no two binaries may be identical ----"
BAD=0
for a in base $MUTANTS; do for b in base $MUTANTS; do
    [ "$a" \< "$b" ] || continue
    if cmp -s "$O/$a/gxemul" "$O/$b/gxemul"; then say "  *** $a == $b  IDENTICAL"; BAD=1
    else say "  $a != $b  ok"; fi
done; done
say "  identical pairs: $BAD (want 0)"

IMG="$O/altoff-scratch.img"
[ -f "$IMG" ] || dd if=/dev/zero of="$IMG" bs=1M count=8 status=none
say "  IDE image  $IMG ($(stat -c %s "$IMG") bytes)"
say ""
say "MUTANTS_BUILD_DONE"

#  ---- 3. TABLE A: the shipped witness, unmodified, against every leg ----------
mkdir -p "$O/run"
python3 -u "$ART/table_a.py" "$O/run" "$IMG" \
    base="$O/base/gxemul" fix="$O/fix/gxemul" m1="$O/m1/gxemul" \
    m2="$O/m2/gxemul" m3="$O/m3/gxemul" m4="$O/m4/gxemul" \
    2>&1 | tee "$O/run/console_a.log"

#  ---- 4. preserve, verified BY THE COMPLETION SENTINEL, not by existence ------
for f in "$O/run/TABLE_A.txt:TABLE_A_DONE" "$LOG:MUTANTS_BUILD_DONE"; do
    p=${f%:*}; want=${f#*:}
    if [ ! -f "$p" ]; then echo "  *** $p never written -- NOT preserved"
    elif [ "$(tail -1 "$p")" != "$want" ]; then
        echo "  *** $p does not end in $want -- truncated, NOT preserved"
    else cp "$p" "$ART/$(basename "$p")"; echo "  preserved $(basename "$p") ($(stat -c %s "$p") bytes, sentinel ok)"; fi
done
if [ -f "$ART/TABLE_A.txt" ]; then
    for l in $MUTANTS; do cp "$O/$l.diff" "$ART/leg_$l.diff"; done
    for l in base fix m1 m2 m3 m4; do
        cp "$O/run/transcript_$l.log" "$ART/transcript_$l.log" 2>/dev/null
    done
    echo "  preserved leg diffs and transcripts"
fi
