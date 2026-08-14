#!/bin/bash
# GATE 1 -- both trees rebuild clean from committed source.
#
# There is NO VPATH in this project. `build/` is an in-place copy compiled from est/, and
# /tmp/gxsec-build is an in-place copy compiled from GXEMUL-SEC/. An edit that is not
# propagated into the compile tree silently tests the OLD binary, so this gate re-syncs
# both from their authoritative tree before building.
#
# Two failure modes this gate is shaped to catch, both of which have happened:
#
#  * cpus/*.o must be deleted explicitly. cpu_mips_instr.c is #included into cpu_mips.o
#    rather than compiled separately, so make does not see it as a dependency and a stale
#    object survives an ordinary rebuild.
#  * /tmp/gxsec-build's Makefile is GENERATED from Makefile.skel and is not tracked. A
#    tree recreated with `cp -a` has none, and make then exits rc=2 having built nothing
#    -- which looks like "0 errors" if you only grep for the word error. The object COUNT
#    is the real check, which is why it is asserted rather than reported.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
. "$HERE/lib.sh"

EST=$ROOT/est
SEC=$ROOT/GXEMUL-SEC
PMAX_TREE=$ROOT/build
ARC_TREE=/tmp/gxsec-build
RIG=$ROOT/gxemul_arc_rig

gate_begin "clean-build"

# #396: UNPUBLISH FIRST. The published arc binary is withdrawn here, at the very top,
# and republished only after gate_end returns 0. #395 removed it inside the publish
# block instead, which meant every route that never REACHED that block left the stale
# copies in place: `need_file` below exits 77 (SKIP) before it, and so does any signal,
# `set -u` abort, or death inside make. Measured by a seat replaying the gate: the SKIP
# route left both stale copies published, and run.sh:94-99 then calls the battery
# REGRESS_PASS_WITH_GAPS. That is not a hypothetical -- $ARC_TREE is /tmp/gxsec-build,
# in WSL's /tmp, which is cleared on reboot, while $RIG/gxsec-gxemul survives; so the
# first gate 1 after a reboot takes exactly this path.
#
# Withdraw-then-republish makes "a published binary exists" mean "the last gate 1 that
# ran, PASSED" for every termination route, not just the ones that reach the bottom.
rm -f /tmp/gxsec-gxemul
if [ -d "$RIG" ]; then rm -f "$RIG/gxsec-gxemul"; fi

need_file "$EST/src" "$SEC/src" "$PMAX_TREE" "$ARC_TREE"

# list_diffs <dirA> <dirB> -- relative paths of source files that differ, or exist on
# only one side.
#
# Deliberately NOT `diff -rq --include='*.c'`. diff has --exclude but NO --include (that
# is a grep option), so that command exits 2 with "unrecognized option" and prints
# nothing -- and with stderr discarded it looks exactly like "no differences". Both the
# divergence check and the sync check below were written that way, so both were comparing
# an empty list against an empty list and could never fail. Measured: the raw command
# produced 0 lines while the trees genuinely differ in 6 files.
list_diffs() {
    local A=$1 B=$2
    local la=$LOGDIR/.ld_a lb=$LOGDIR/.ld_b
    ( cd "$A" && find . \( -name '*.c' -o -name '*.h' -o -name '*.cc' -o -name '*.skel' \) \
        -print ) | sed 's|^\./||' | sort > "$la"
    ( cd "$B" && find . \( -name '*.c' -o -name '*.h' -o -name '*.cc' -o -name '*.skel' \) \
        -print ) | sed 's|^\./||' | sort > "$lb"
    comm -3 "$la" "$lb" | tr -d '\t'
    comm -12 "$la" "$lb" | while IFS= read -r f; do
        cmp -s "$A/$f" "$B/$f" || echo "$f"
    done
}

build_tree() {   # label, source tree, compile tree, expected object count
    local lab=$1 src=$2 tree=$3 want=$4
    local log=$LOGDIR/build_$lab.log

    ( cd "$src/src" && find . \( -name '*.c' -o -name '*.h' -o -name '*.cc' \) \
        -exec cp -f --parents {} "$tree/src/" \; ) 2>/dev/null

    # VERIFY THE SYNC. The copy above discards its exit status and all stderr, and
    # `find -exec ... \;` continues past per-file failures -- so a single unwritable file
    # in the compile tree would silently leave the OLD source in place and the gate would
    # then report a clean build of the wrong code. That is precisely the failure this gate
    # exists to prevent, so it is asserted rather than assumed.
    list_diffs "$src/src" "$tree/src" > "$LOGDIR/unsynced_$lab.txt"
    local unsynced; unsynced=$(grep -c '^' < "$LOGDIR/unsynced_$lab.txt")
    check "$lab: source tree fully synced into compile tree" "$unsynced" "0"
    [ "$unsynced" = 0 ] || head -8 "$LOGDIR/unsynced_$lab.txt" | sed 's/^/       /'

    cd "$tree" || return 1
    [ -f Makefile ] || { note "$lab: no Makefile, running ./configure"
                         ./configure > "$LOGDIR/configure_$lab.log" 2>&1; }
    find src -name '*.o' -delete
    rm -f gxemul
    make -j12 > "$log" 2>&1
    local rc=$?
    local warn err objs
    warn=$(grep -ciE 'warning:' "$log")
    err=$(grep -ciE 'error:' "$log")
    objs=$(find src -name '*.o' | wc -l)

    check     "$lab: make exit status"  "$rc"   "0"
    check     "$lab: warnings"          "$warn" "0"
    check     "$lab: compiler errors"   "$err"  "0"
    # EXACT, not >=. The object count is the documented tell for "make exited 2 having
    # built nothing", and >= would also miss an object that should have been removed.
    check     "$lab: objects built"     "$objs" "$want"
    check     "$lab: binary produced"   "$([ -x gxemul ] && echo yes || echo no)" "yes"
    [ "$warn" = 0 ] || grep -iE 'warning:' "$log" | head -12 | sed 's/^/       /'
    [ "$err"  = 0 ] || grep -iE 'error:'   "$log" | head -12 | sed 's/^/       /'
}

# ---- the twin trees must agree outside the known divergent set ----------
# est/ and GXEMUL-SEC/ are separate source trees, each compiled into its own build tree.
# Nothing else in this harness would notice a correction applied to one and not the other:
# both would build clean, both would boot, and pmax would quietly run the old code. The
# divergence set is a fixed, documented list, so anything outside it is an un-propagated
# edit and is asserted here rather than left to be discovered later.
# #394: every entry now carries its REASON. An unexplained exemption is how a real
# divergence gets silenced -- the list said WHICH files may differ but never WHY, so a
# stale entry and a legitimate one were indistinguishable. Only the first whitespace-
# separated field is the filename; the rest is prose for the reader. Filenames here
# contain no spaces, so `awk '{print $1}'` splits it exactly.
# *** ONE LINE PER ENTRY. NEVER WRAP A REASON. *** A wrapped reason donates the
# continuation line's first word to the allowlist -- measured, that took a genuine
# divergence from RED to GREEN. The "every allowlist entry names a real file" check
# below is what enforces this; keep the reasons terse rather than defeating it.
#
# #396 corrected three of these reasons. They were written from what the divergence was
# BELIEVED to be, and two panel seats measured the actual est<->SEC diffs and found the
# belief wrong in each case. A reason that is itself false is worse than no reason: it
# is an exemption that LOOKS justified.
DIVERGENT="devices/dev_jazz.c      arc-only EXT_IMASK IP3/IP4/IP6 interrupt-gating split; CHANGELOG.md:653-656 records it as not affecting pmax. That passage is in the #251/#252 round and carries no number of its own -- do NOT tag it #257, which is the unrelated R4030 interval-timer rate (CHANGELOG.md:726) and is present in BOTH trees.
devices/Makefile.skel   mechanically tied to the SEC-only dev_ne2000.o
disk/diskimage.c        SUSPECT: the whole diff is trailing whitespace on one blank line, from root import 39748e3. The #115 fix beneath it is byte-identical in both trees. Normalise it and drop this entry -- the stale-entry check below now makes that safe to do.
machines/machine_arc.c  7 hunks, +33/-5. NOT wholly conditional: the ne2000 device_add at machine_arc.c:209-212 is UNCONDITIONAL inside machine_arc_init, and the fb_console rewrite applies to every ARC subtype; only :140-141 is PICA-gated. It is the SEC-only ARC/Jazz bring-up layer. Foundation commit 9d18d15.
promemul/arcbios.c      SEC-only ARC/Jazz bring-up plus later hardening (9d18d15). NOT wholly MACHINE_ARC-gated: CHECK_ALLOCATION(boot_string) at arcbios.c:2654 sits in a SEC-only hunk outside that test, and other hunks key off vgaconsole / x11_md.in_use.
devices/dev_ne2000.c    SEC-exclusive: the file does not exist in est at all
devices/autodev.c       GENERATED by enumerating dev_*.c (makeautodev.sh:56-64,81-90 globs the directory and greps DEVINIT). dev_ne2000.c is the only device file SEC has and est lacks, so this diff is exactly its declaration plus its device_register() call. Under the current generator it cannot be made identical while the device sets differ."

note "checking est/ vs GXEMUL-SEC/ divergence"
list_diffs "$EST/src" "$SEC/src" | sort > "$LOGDIR/divergent_actual.txt"
echo "$DIVERGENT" | awk '{print $1}' | sort > "$LOGDIR/divergent_expected.txt"
comm -23 "$LOGDIR/divergent_actual.txt" "$LOGDIR/divergent_expected.txt" \
    > "$LOGDIR/divergent_unexpected.txt"
n_actual=$(grep -c '^' < "$LOGDIR/divergent_actual.txt")
n_unexpected=$(grep -c '^' < "$LOGDIR/divergent_unexpected.txt")
if [ "$n_unexpected" != 0 ]; then
    note "UNEXPECTED divergence (likely an un-propagated correction):"
    sed 's/^/         /' "$LOGDIR/divergent_unexpected.txt"
fi
note "divergent files seen ($n_actual): $(tr '\n' ' ' < "$LOGDIR/divergent_actual.txt")"

# #396: THE OTHER DIRECTION. Only `comm -23` was computed -- actual-minus-expected -- so
# an entry that is allowlisted but NO LONGER DIVERGENT could never fail. Measured by a
# seat replaying this gate: normalise disk/diskimage.c (which is literally what its own
# reason instructs) and keep the entry, and the gate still reports PASS (14 checks). A
# silently-stale exemption is precisely the defect #394 claimed to be fixing, so #394
# shipped without the assertion that would have proved its own point.
comm -13 "$LOGDIR/divergent_actual.txt" "$LOGDIR/divergent_expected.txt" \
    > "$LOGDIR/divergent_stale.txt"
n_stale=$(grep -c '^' < "$LOGDIR/divergent_stale.txt")
if [ "$n_stale" != 0 ]; then
    note "STALE allowlist entries (listed as divergent, but the files now agree):"
    sed 's/^/         /' "$LOGDIR/divergent_stale.txt"
fi

# #396: AND THE ENTRIES MUST BE REAL PATHS. The parser takes the first whitespace field
# of each line, which silently turns any stray line into an allowlist entry. The
# dangerous instance is not exotic: a reason WRAPPED onto a second line donates that
# line's first word. Measured -- a genuine divergence went unexpected=1 (RED) to 0
# (GREEN) that way, and the reasons here run 100-300 characters in a file wrapped at
# about 90 columns, so wrapping one is an ordinary edit, not an act of sabotage.
# Requiring every parsed entry to exist in at least one tree makes prose fail loudly:
# "Normalise", "The" and "every" are not files. This also catches a blank line, a
# whitespace-only line, and a `# comment` line, none of which the comparison notices.
n_bogus=0
while IFS= read -r _e; do
    [ -n "$_e" ] || { n_bogus=$((n_bogus+1)); continue; }
    if [ ! -e "$EST/src/$_e" ] && [ ! -e "$SEC/src/$_e" ]; then
        note "ALLOWLIST ENTRY IS NOT A FILE IN EITHER TREE: '$_e'"
        n_bogus=$((n_bogus+1))
    fi
done < "$LOGDIR/divergent_expected.txt"

# A FLOOR as well as a ceiling. The divergence set is known to be non-empty, so an empty
# list means the comparison itself broke -- which is exactly how the previous version of
# this check passed while measuring nothing.
check_min "divergence comparison actually ran" "$n_actual" 1
check     "no divergence outside the documented set" "$n_unexpected" "0"
check     "no stale allowlist entries"               "$n_stale"      "0"
check     "every allowlist entry names a real file"  "$n_bogus"      "0"
echo

build_tree pmax "$EST" "$PMAX_TREE" 223
build_tree arc  "$SEC" "$ARC_TREE"  224

# Publish the arc binary where the rigs expect it -- but ONLY after the VERDICT says pass.
#
# HISTORY, because both earlier shapes looked right and neither was:
#
# Originally this tested `[ -x "$ARC_TREE/gxemul" ]` alone, under a comment claiming
# "only if it really built". That asks whether a binary EXISTS, never whether the gate
# PASSED, so a real run on 2026-08-13 published while reporting
# `clean-build: FAIL (1 of 14 checks)`.
#
# #395 replaced it with `[ "$_fails" != 0 ]`. That is the right QUANTITY read at the
# wrong TIME: it is positional, not semantic. A seat replaying this gate measured the
# consequence -- append ONE failing check after the `fi` and you get
# `clean-build: FAIL (1 of 15 checks)`, exit 1, AND THE BINARY PUBLISHED. The defect
# #395 existed to close reopens completely, one line lower, the next time anyone extends
# this gate. #395's own comment asserted "every check has already run by this point",
# which was true of the file that day and is not a property anything enforces.
#
# #396 keys publication off gate_end's RETURN VALUE instead. gate_end is the thing that
# decides PASS/FAIL (lib.sh:72-84), so nothing can be appended between the decision and
# the action -- the guard is now structural rather than a fact about line ordering.
#
# The withdrawal moved to the TOP of the gate (see the rm near gate_begin). Removing
# stale copies only on the failing branch here could not cover the routes that never
# reach this point at all: need_file's SKIP (exit 77), a signal, a `set -u` abort, or a
# death inside make.
#
# MUTANT THIS MUST FAIL, and it is the one a careful reviewer would write: "harden"
# `$_fails` to `${_fails:-0}` for consistency with lib.sh:102. Measured -- when unset
# that takes the PUBLISH branch. Defaulting an unknown state to "publish" is exactly
# backwards for a guard whose whole job is to withhold.
#
# On leaving nothing behind rather than leaving something stale: a stale-but-working
# binary is the worse lie, because downstream gates go green against code that is not
# the code under test -- the "build-tree residue is not evidence" trap that cost four
# rounds of #88. A missing file makes the downstream need_exec preflights SKIP loudly.
# gate_offline.sh:87-95 ("THE HONESTY LINK") and selftest_mutation_295.sh:51-52 show the
# project preferring a loud stop over a quiet stale pass -- though note both are
# CONSUMER-side freshness checks, not precedent for a producer deleting its own output.
gate_end
verdict=$?
fails_at_verdict=$_fails

if [ "$verdict" != 0 ]; then
    note "gate did not pass -- arc binary left UNPUBLISHED (withdrawn at gate start)"
elif [ -x "$ARC_TREE/gxemul" ]; then
    cp -f "$ARC_TREE/gxemul" /tmp/gxsec-gxemul
    published=$?
    if [ -d "$RIG" ]; then
        cp -f "$ARC_TREE/gxemul" "$RIG/gxsec-gxemul" || published=1
    fi
    # The copy's status was previously discarded, so "published" was printed whether or
    # not either copy landed -- a disk-full or unwritable rig would have been announced
    # as a success. Say what actually happened.
    if [ "$published" = 0 ]; then
        note "arc binary published to rig and /tmp/gxsec-gxemul"
    else
        note "*** PUBLISH FAILED -- the copy did not land; downstream will SKIP ***"
    fi
else
    note "gate passed but $ARC_TREE/gxemul is missing -- nothing published"
fi

# gate_end already ran above -- it is what decided `verdict`, and it prints the verdict
# line as a side effect. Calling it a second time here would print a SECOND verdict and
# (worse) a log-scraping consumer would see two, so exit on the value already captured.
#
# BUT DO NOT EXIT ON A STALE VERDICT. Moving gate_end earlier fixes the defect where an
# appended check could publish first and fail afterwards, but it introduces the mirror
# hazard: a check appended down here would now be IGNORED ENTIRELY, since both the
# printed verdict and the exit status were decided above. Neither shape is structurally
# immune -- publication and adjudication are simply adjacent -- so the honest move is to
# make the remaining hazard LOUD instead of silent. If _fails moved after the verdict
# was taken, the verdict on screen is wrong, and saying so is worth more than pretending
# the ordering is guaranteed.
if [ "$_fails" != "$fails_at_verdict" ]; then
    echo "  *** A CHECK RAN AFTER gate_end: the verdict printed above is STALE"
    echo "      (_fails was $fails_at_verdict at the verdict, $_fails now). Failing."
    verdict=1
fi
exit "$verdict"
