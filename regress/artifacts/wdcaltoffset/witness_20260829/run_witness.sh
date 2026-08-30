#!/bin/bash
#
#  wdcaltoffset -- build both legs of the rung-3 witness and measure them.
#
#      MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash \
#        /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/wdcaltoffset/witness_20260829/run_witness.sh
#
#  WHY IT IS A FILE AND NOT A `wsl ... -c '<string>'`:  that form strips $VARS even
#  inside single quotes.  And a Windows path handed to `wsl -- bash` fails while wsl
#  itself exits 0, which is why every path here is /mnt/c.
#
#  NOTHING UNDER THE PROJECT TREE IS WRITTEN except this artifacts directory.  Both
#  build trees come from `git archive HEAD` into $O (default /tmp/gxaltoff), so:
#    * no .MUTANT sentinel is owed -- no project build tree is mutated at all;
#    * the baseline is MECHANICAL rather than remembered.  A `cp -a` of the working
#      tree inherits whatever .o files and untracked residue sit there; `git archive`
#      cannot.  The cmp below then states, rather than assumes, that the tree measured
#      is the tree named.
#
#  THE TWO-PART CLEARANCE IS RUN, NOT ASSERTED, for each leg:
#      (1) the source cmps against the named baseline
#      (2) [ binary -nt source ]        -- MAKE_RC has been observed 0 on a failed build
#
set -u

SEC=${GXSEC:-/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC}
ART="$SEC/regress/artifacts/wdcaltoffset/witness_20260829"
O=${OUT:-/tmp/gxaltoff}
J=${J:-8}
BUILDLOG="$O/BUILD.log"

mkdir -p "$O"
: > "$BUILDLOG"
say () { echo "$@" | tee -a "$BUILDLOG"; }

say "=============================================================================="
say "wdcaltoffset rung-3 witness -- build + measure"
say "=============================================================================="
say "date       $(date '+%Y-%m-%d %H:%M:%S')"
say "SEC        $SEC"
say "workdir    $O   (scratch; nothing under the project tree is built or mutated)"
say ""

#  ---------------------------------------------------------------- 1. the baseline
say "------------------------------------------------------------------ BASELINE"
HEAD=$(git -C "$SEC" rev-parse HEAD 2>/dev/null)
say "  baseline             HEAD = $HEAD"
DIRT=$(git -C "$SEC" status --porcelain 2>/dev/null)
NDIRT=$(printf '%s' "$DIRT" | grep -c . )
say "  working-tree entries not matching HEAD: $NDIRT"
printf '%s\n' "$DIRT" | grep . | while IFS= read -r l; do say "      $l"; done
#  ONLY DIRT THAT CAN CHANGE THE BUILD MATTERS, and saying "the tree is dirty" when the
#  difference is a records file is crying wolf -- a warning that fires on every ordinary
#  session is a warning that gets ignored.  This run builds HEAD, so the question is
#  narrow: does any BUILD INPUT differ from HEAD?
BUILDDIRT=$(printf '%s\n' "$DIRT" | grep -c -E '^.. (src/|configure$|Makefile\.skel$)')
say "  of those, BUILD INPUTS (src/, configure, Makefile.skel): $BUILDDIRT   (want 0)"
if [ "$BUILDDIRT" != "0" ]; then
    say "  *** A BUILD INPUT DIFFERS FROM HEAD.  The tree built below is HEAD, so it is"
    say "  *** NOT what sits in $SEC.  Say so in any record citing this run."
else
    say "  so the build below is byte-identical to the working tree's build inputs;"
    say "  any other differences are records/harness files and cannot reach the binary."
fi
say ""

#  ------------------------------------------------------------------- 2. the trees
rm -rf "$O/base" "$O/fix"
mkdir -p "$O/base" "$O/fix"
git -C "$SEC" archive HEAD | tar -x -C "$O/base" || { say "  git archive FAILED"; exit 1; }
cp -a "$O/base/." "$O/fix/" || { say "  cp FAILED"; exit 1; }

say "------------------------------------------------------- SOURCE IDENTITY (cmp)"
if cmp -s "$O/base/src/devices/dev_wdc.c" "$SEC/src/devices/dev_wdc.c"; then
    say "  base/src/devices/dev_wdc.c  ==  SEC working tree            IDENTICAL"
else
    say "  base/src/devices/dev_wdc.c  !=  SEC working tree            *** DIFFERS ***"
    say "  (expected only if the working tree is dirty -- see the line above)"
fi

python3 "$ART/mkfixleg.py" "$O/fix/src/devices/dev_wdc.c" 2>&1 | tee -a "$BUILDLOG"
[ ${PIPESTATUS[0]} -eq 0 ] || { say "  mkfixleg.py FAILED -- the anchor did not match"; exit 1; }
diff -u "$O/base/src/devices/dev_wdc.c" "$O/fix/src/devices/dev_wdc.c" > "$O/fixleg.diff"
say "  fix leg diff         $(grep -c '^+' "$O/fixleg.diff") added / $(grep -c '^-' "$O/fixleg.diff") removed lines (incl. the ---/+++ header lines)"
#  Every OTHER file must be byte-identical between the legs.  A fix leg that
#  accidentally differs somewhere else measures something other than the fix.
OTHER=$(diff -rq "$O/base/src" "$O/fix/src" | grep -v 'dev_wdc\.c' | wc -l)
say "  other src/ files differing between the legs: $OTHER   (want 0)"
say ""

#  ------------------------------------------------------------------- 3. the builds
build () {
    local tree="$1" tag="$2"
    say "------------------------------------------------------------ BUILD  $tag"
    ( cd "$tree" \
      && rm -f src/cpus/*.o \
      && ./configure  > "$O/configure_$tag.log" 2>&1 \
      && make -j"$J" > "$O/make_$tag.log" 2>&1 )
    local rc=$?
    say "  make rc              $rc   (NOT trusted on its own -- see the freshness check)"
    if [ ! -x "$tree/gxemul" ]; then
        say "  *** no $tree/gxemul was produced.  tail of make log:"
        tail -20 "$O/make_$tag.log" | sed 's/^/      /' | tee -a "$BUILDLOG"
        return 1
    fi
    if [ "$tree/gxemul" -nt "$tree/src/devices/dev_wdc.c" ]; then
        say "  [ binary -nt source ] YES -- the binary postdates the source it was built from"
    else
        say "  *** [ binary -nt source ] NO -- STALE BINARY.  Refusing to measure it."
        return 1
    fi
    say "  binary               $(ls -la "$tree/gxemul" | awk '{print $5" bytes  "$6" "$7" "$8}')"
    return 0
}

build "$O/base" base || { say "BUILD FAILED (base)"; say "ALTOFF_BUILD_DONE"; exit 1; }
build "$O/fix"  fix  || { say "BUILD FAILED (fix)";  say "ALTOFF_BUILD_DONE"; exit 1; }

#  The two binaries must actually DIFFER, or the fix leg silently measured the base.
if cmp -s "$O/base/gxemul" "$O/fix/gxemul"; then
    say "  *** THE TWO BINARIES ARE IDENTICAL -- the fix leg did not take.  Stopping."
    say "ALTOFF_BUILD_DONE"
    exit 1
fi
say "  the two binaries differ                                    (as they must)"
say ""

#  --------------------------------------------------------------- 4. the disk image
IMG="$O/altoff-scratch.img"
if [ ! -f "$IMG" ]; then
    dd if=/dev/zero of="$IMG" bs=1M count=8 status=none
fi
say "  IDE image            $IMG ($(stat -c %s "$IMG") bytes), attached as iR: so the"
say "                       guest's writes go to a pid-unique overlay"
say ""
say "ALTOFF_BUILD_DONE"

#  ------------------------------------------------------------------- 5. the measure
#
#  FROZEN COPY.  bash reads a script incrementally and python reads its source at
#  startup, so a long job run from the file under edit can be corrupted (bash) or can
#  give two legs two different instruments (python).  Both legs run inside ONE python
#  invocation below, and that invocation is of a COPY.
#
mkdir -p "$O/run"
cp "$ART/wdcaltoff_rung3_probe.py" "$O/run/probe.frozen.py"
python3 -u "$O/run/probe.frozen.py" \
    "$O/base/gxemul" "$O/fix/gxemul" "$IMG" "$O/run" 2>&1 | tee "$O/run/console.log"

#  ------------------------------------------------------------------ 6. preserve
#
#  A PRESERVED LOG IS VERIFIED BY ITS COMPLETION SENTINEL, NOT BY ITS EXISTENCE.
#  A copy taken from a still-running job looks complete and is not.
#
for f in "$O/run/RESULTS.txt:ALTOFF_DONE" "$BUILDLOG:ALTOFF_BUILD_DONE"; do
    p=${f%:*}; want=${f#*:}
    if [ ! -f "$p" ]; then
        echo "  *** $p was never written -- NOT preserved"
    elif [ "$(tail -1 "$p")" != "$want" ]; then
        echo "  *** $p does not end in $want -- truncated, NOT preserved"
    else
        cp "$p" "$ART/$(basename "$p")"
        echo "  preserved $(basename "$p")  ($(stat -c %s "$p") bytes, sentinel ok)"
    fi
done
#  The pty transcripts and the raw guest program have no sentinel of their own, so they
#  are preserved only if RESULTS.txt has ITS sentinel -- which is what says both emulator
#  runs finished.  Preserving them matters because they are the only copies of the raw
#  evidence: RESULTS.txt is this probe's READING of the run, the transcripts are the run.
if [ -f "$ART/RESULTS.txt" ]; then
    for f in transcript_base.log transcript_fix.log wdcaltoff.bin; do
        cp "$O/run/$f" "$ART/$f" && echo "  preserved $f  ($(stat -c %s "$O/run/$f") bytes)"
    done
else
    echo "  *** RESULTS.txt was not preserved, so the transcripts are NOT preserved either"
fi
cp "$O/fixleg.diff" "$ART/fixleg.diff"
echo "  preserved fixleg.diff"
echo
echo "  scratch left at $O (make logs, configure logs, both build trees)"
