#!/bin/bash
# GATE 9 -- every machine type AND EVERY SUBTYPE constructed under AddressSanitizer,
# three-way.
#
# This is the BREADTH gate. Everything else in this harness executes four machines; the
# fork changed 117 source files, 27 of them specific to architectures (alpha, ARM, i960,
# PowerPC, SGI) that no rig touches at all. This gate builds every machine type, attaches
# its devices, and lets ASan watch.
#
# It revives an instrument the project already used -- the CHANGELOG records a "run every
# machine under ASan sweep (23 machine types)" that found the macppc heap OOB (#23) -- but
# as a STANDING GATE rather than a one-off, and comparatively rather than absolutely.
#
# THE ASSERTION IS DIRECTIONAL, and that matters. The fork exists partly to FIX memory
# errors, so upstream being dirty where HEAD is clean is success, not failure. Only the
# reverse is a regression:
#
#     clean under pristine, dirty under HEAD   -> REGRESSION (this gate fails)
#     dirty under pristine, clean under HEAD   -> the fork doing its job
#     dirty under both                         -> pre-existing, reported not failed
#
# A MACHINE MUST BE HANDED A FILE OR IT NEVER CONSTRUCTS. Measured: `-E testmips` with no
# file prints usage and aborts before any device is attached -- a sweep built that way
# would test nothing and pass every time. With a dummy image the machine reports
# `model:`, `cpu:`, `memory:` and attaches devices. Machines with subtypes additionally
# need `-e <subtype>`; without it 15 of the 41 types never construct.  (This line said
# "13 of 37" until #444 re-measured it. The counts drift with the machine list; that is
# why nothing below asserts one.)
#
# ############################################################################
# #444 asansweepblind -- THREE MEASURED BLIND SPOTS, all of which left this gate GREEN
# while it was reporting things that were not true. Each fix below is annotated with the
# measurement that forced it; none of them is reasoned-from-source.
#
#  B1. IT COULD NOT SEE A CONSTRUCTION ABORT AT ALL.
#      sanhit() greps for ASan/UBSan text. A machine that calls abort() is not a
#      sanitizer hit, so it scored ZERO -- and the only construction assertion was a
#      FLOOR (`check_min "machine types constructed" 20`), which a handful of corpses
#      cannot breach.
#      MEASURED, by running the shipped gate against the same binaries this one uses:
#      **PASS (3 checks)** while 15 machine/subtype combinations were dying by SIGABRT.
#      It touched two of the fifteen (hpcmips/be-300, mvmeppc/mvme1600); both scored the
#      row `no  0  0` -- BYTE-IDENTICAL to the row a machine that merely wants a subtype
#      produces -- and both were absorbed by "machine types constructed 38 (>= 20)".
#      *** AND THE ABORT MESSAGE WAS NOT EVEN ON DISK. ***  core/interrupt.c:191-198 does
#      `printf("Aborting.\n"); abort();`, and abort() DOES NOT FLUSH STDIO. With stdout
#      redirected to a file glibc block-buffers it, so the whole diagnostic died with the
#      process: MEASURED, the log of `-E decstation -e 5400` was **0 bytes**. The gate then
#      read that empty file as `constructed=no, sanhit=0` -- INDISTINGUISHABLE from a
#      machine that merely needs a subtype. A dead machine and a fine one scored alike.
#      Fix: classify by EXIT STATUS (diedby(), below), which no buffering can lose, and
#      run under `stdbuf -o0 -e0` so the reason text survives for the human.
#
#  B2. IT SWEPT ONLY EACH TYPE'S *FIRST* SUBTYPE, so a defect in any later one was
#      invisible by construction. MEASURED: the shipped gate ran 14 subtypes in total,
#      one per type that needs one. Sweeping every subtype runs 58 and finds **15** dying
#      machines where a first-subtype-only sweep of the same 41 types finds **2** -- and
#      finds 4 ASan hits each on sgi/ip28, sgi/ip30 and sgi/ip35, which nothing in this
#      harness had ever executed.
#      The full sweep is 99 combinations and the whole gate -- both binaries, 198 launches
#      -- costs 55 s wall (measured), so there is no reason to bound it. It is not
#      bounded. If a future edit does bound it, the gate must SAY what it dropped -- do
#      not cap coverage silently.
#
#  B3. THE ALIAS PARSER SILENTLY RE-ATTRIBUTED ONE MACHINE'S SUBTYPES TO ANOTHER.
#      The old awk required the primary alias to match `[a-z0-9_.-]+`. **SGI's primary
#      alias is "silicon graphics" -- WITH A SPACE** (`gxemul -H`: `SGI ("silicon
#      graphics", "sgi")`), so the type line matched the line pattern, failed the alias
#      pattern, and fell through WITHOUT running `next` and WITHOUT updating `type`.
#      Its ten subtypes then attached to whatever type came before it in the help text,
#      which is `rpi`:
#          BEFORE:  S rpi ip12 .. S rpi ip35   (10 rows), `T sgi` absent, `S sgi *` = 0
#          AFTER :  T sgi, S sgi ip12 .. S sgi ip35 (10 rows), `S rpi *` = 0
#      Consequence measured, and it is worse than a wrong label: because no `T sgi` line
#      existed, THE TYPE LOOP NEVER RAN A SINGLE SGI MACHINE. Ten subtypes carrying a
#      real heap-buffer-overflow (arcbios.c:2391 set_env <- machine_setup_sgi) were not
#      swept at all, and no row anywhere was red.
#      Fix: firstalias() takes the first SHELL-SAFE alias out of the trailing
#      parenthesised group -- so `sgi`, not `silicon graphics`. And a line that yields NO
#      usable alias now emits an explicit `X`/`Y` marker that a check asserts to be zero,
#      so the next multi-word alias is RED instead of silent. THAT is the fix for the
#      class; renaming one machine would only have fixed the instance.
#      (Why not the true primary `silicon graphics`? Two reasons, both measured: the type
#      list is consumed by word-splitting shell loops, and `sgi` is what every other
#      record in this project calls it. `-E "silicon graphics"` does work -- verified --
#      it is just not a usable row key.)
# ############################################################################
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
. "$HERE/lib.sh"

ASAN_HEAD=/tmp/gx-asan-head/gxemul
ASAN_PRI=/tmp/gx-asan-pristine/gxemul
DUMMY=$LOGDIR/dummy.elf
SHELLERR=$LOGDIR/asan_sweep_shellerr.txt

gate_begin "asan-machine-sweep"

[ -x "$ASAN_HEAD" ] || gate_skip "no ASan build -- see regress/README.md (build_asan)"

# Leak reporting off: the emulator is killed mid-run, so exit-time leaks are expected and
# say nothing about correctness. ASan's memory-error detection is unaffected.
#
# verify_asan_link_order=0 is REQUIRED, not cosmetic. `stdbuf` works by LD_PRELOADing
# libstdbuf.so, which then precedes the ASan runtime in the initial library list; ASan
# refuses to start and prints "ASan runtime does not come first in initial library list".
# MEASURED both ways on decstation/5400: without the flag the run produced 155 bytes of
# that complaint and never entered main(); with it, 582 bytes of real emulator output
# ending in the abort diagnostic. Controls that the flag does not weaken detection:
# decstation/pmax still constructs (695 bytes, cpu:+memory:) and sgi/ip12 still reports
# its 4 sanitizer diagnostics.
#
# *** DO NOT TAKE "ASAN ACCEPTED THE FLAG" AS PROOF THE FLAG IS REAL. *** The discriminator
# this project uses for CLI effort tiers was tried here and FAILED to discriminate: this
# ASan silently ignores `no_such_asan_flag_xyz=0` and runs normally. The proof above is
# BEHAVIOURAL -- the flag changes what happens -- which is the only kind available.
export ASAN_OPTIONS=detect_leaks=0:abort_on_error=0:print_summary=1:verify_asan_link_order=0
export UBSAN_OPTIONS=print_stacktrace=0

# 15 machines abort here by design (see AB_EXEMPT). This host already has `ulimit -c 0`,
# but a host that does not would drop fifteen cores of a 93 MB ASan binary into $LOGDIR.
ulimit -c 0 2>/dev/null || true

#############################################################################
#  AB_EXEMPT -- THE KNOWN-DEAD SET, DATED AND NAMED.
#
#  Same idiom as gate_offline.sh's SM_EXEMPT/SC_EXEMPT, and for the same reason: a gate
#  that carries debt must carry it OUT LOUD. Entries are `type/subtype:YYYY-MM-DD`.
#
#  WHY A LIST AND NOT A FLOOR. A floor cannot express "none of them died" -- that was
#  B1's second half. A hard count could, but it is brittle: it breaks every time the
#  machine list changes, for no defect. A NAMED list is neither. Adding a machine that
#  works changes nothing; a machine that starts dying is red the same day; and a machine
#  that stops dying is ALSO red (see the "no longer die" check), so the list cannot rot
#  into a lie the way SM_COVERED did before it was cross-checked against real work.
#
#  WHY THESE FIFTEEN, AND WHY THE DIRECTIONAL FRAME DOES NOT COVER THEM.
#  All fifteen were MEASURED on both binaries: they abort IDENTICALLY under pristine
#  39748e3 and under HEAD (rc=134, SIGABRT, same reason text). So the directional rule --
#  the one at the top of this file -- classifies every one of them as "pre-existing,
#  reported not failed", and a purely directional gate would print them and pass. That is
#  right for attributing blame and WRONG for knowing what is dead, which is why this gate
#  now asserts BOTH: `died on HEAD but constructs upstream` (directional, blame) and
#  `died and is not on this list` (absolute, inventory).
#
#  They are upstream's own unported-legacy markers, not fork damage. THREE shapes, each
#  read at the cited line rather than guessed, and the table's `reason` column prints
#  which one a given row hit:
#    * `fatal("TODO: ... rewrite\n"); abort();`  -- machines/machine_pmax.c:365,536;
#      machines/machine_sgi.c:170,218,226,238. The machine's interrupt wiring was never
#      ported to the current interrupt API and the port is commented out directly below
#      the abort. Hit by decstation/{3maxplus,maxine} and sgi/{ip20,ip22,ip24}.
#    * `interrupt_handler_lookup("...") failed. / Aborting.` -- core/interrupt.c:191-198,
#      reached from the same unported wiring via INTERRUPT_CONNECT (interrupt.h:77-80),
#      which DISCARDS the lookup's return value, so a miss cannot be handled by the caller.
#      This is the printf-then-abort() that B1 could not see.
#    * `bus_pci_add(): pci_data == NULL!` -- devices/bus_pci.c:220-222, a machine adding
#      PCI devices to a bus it never created. Hit by mvmeppc/mvme1600.
#
#  *** THE DATE IS MINE, NOT THE OWNER'S, AND IT WANTS CONFIRMING. ***  gate_offline.md's
#  own lesson is that "a deadline nobody chose is a deadline nobody owns"; the owner has
#  previously chosen tighter dates than proposed. 2026-11-30 is a placeholder chosen
#  because these are whole machine ports rather than one-line fixes -- it is not a
#  judgement that they may wait that long.
#
#  hpcmips/{be-300,e-105,agenda} are being worked in a concurrent round. When that lands,
#  the "no longer die" check goes RED and the fix is to DELETE those three lines. That
#  friction is the point: it is how the inventory stays true.
AB_EXEMPT="
    alpha/3000/300:2026-11-30
    decstation/3maxplus:2026-11-30
    decstation/maxine:2026-11-30
    decstation/5400:2026-11-30
    decstation/5500:2026-11-30
    hpcmips/be-300:2026-11-30
    hpcmips/e-105:2026-11-30
    hpcmips/agenda:2026-11-30
    mvmeppc/mvme1600:2026-11-30
    mvmeppc/mvme2100:2026-11-30
    sgi/ip19:2026-11-30
    sgi/ip20:2026-11-30
    sgi/ip22:2026-11-30
    sgi/ip24:2026-11-30
    sgi/ip27:2026-11-30
"

#  A DELIBERATE COPY of gate_offline.sh's exempt_expired(). It belongs in lib.sh and this
#  round may not edit lib.sh, so the duplication is recorded rather than hidden -- see the
#  residual note at the end of this file. The behaviour it encodes was learned the hard
#  way there: an entry with NO date, an UNPADDED date, or a non-date never expired, and
#  still satisfied the coverage check. A malformed entry is RED and names itself.
ab_expired () {          # ab_expired <today> <entries...>
    local today="$1"; shift
    local out="" e d
    for e in "$@"; do
        case "$e" in
            *:*) ;;
            *) out="$out $e(NO-DATE)"; continue ;;
        esac
        d=${e##*:}
        case "$d" in
            [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]) ;;
            *) out="$out ${e%%:*}(BAD-DATE:${d:-empty})"; continue ;;
        esac
        [ "$d" \< "$today" ] && out="$out ${e%%:*}"
    done
    printf '%s' "${out:-none}"
}

ab_is_exempt() {         # ab_is_exempt <type/subtype>
    local e
    for e in $AB_EXEMPT; do [ "${e%%:*}" = "$1" ] && return 0; done
    return 1
}

# Minimal file so machine construction proceeds past the loader.
printf '\x7fELF\x01\x02\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x08\x00\x00\x00\x01' > "$DUMMY"
head -c 512 /dev/zero >> "$DUMMY"

#  stdbuf is what makes an aborting machine's reason text reach the log at all (B1). The
#  assertions do not depend on it -- they are exit-status based -- but the human-readable
#  half of this gate does, so its absence is a row rather than a silent downgrade.
check "stdbuf present (abort diagnostics survive the abort)" \
      "$(command -v stdbuf >/dev/null 2>&1 && echo yes || echo no)" "yes"

# Build the "type[ subtype]" work list from the emulator's own help text.
"$ASAN_HEAD" -H > "$LOGDIR/help.txt" 2>"$LOGDIR/help_err.txt"

#  firstalias(): the first SHELL-SAFE alias inside the LAST parenthesised group on the
#  line. Both halves of that sentence are load-bearing:
#    * LAST group, because a machine's *name* may itself contain quotes and parentheses --
#      `Generic "bare" ARM machine ("barearm")`, `ARM-based "Android" machines
#      ("android-arm")`, `DECstation 3100 (PMAX) ("pmax", "3100", "2100")`. Harvesting
#      every quoted token on the line would pick up `bare` and `Android`.
#    * SHELL-SAFE, because the alias becomes a word in an unquoted `for` list and a row
#      key. `silicon graphics` is the primary alias for SGI and is unusable as either;
#      `sgi` is the next one and is what the rest of this project calls it.
#  An unusable line emits X (type) or Y (subtype) and is asserted to zero below, so the
#  NEXT machine with a space in its primary alias is red rather than mis-attributed. A
#  failed type line also sets type="?" so its subtypes cannot silently inherit the
#  PREVIOUS type -- that inheritance is precisely how SGI's ten became rpi's ten.
awk '
  function firstalias(line,   p,i,seg,n,arr) {
      p = 0
      for (i = length(line); i >= 1; i--) if (substr(line,i,1) == "(") { p = i; break }
      if (p == 0) return ""
      seg = substr(line, p)
      n = split(seg, arr, "\"")
      for (i = 2; i <= n; i += 2)
          if (arr[i] ~ /^[A-Za-z0-9_.+\/-]+$/) return arr[i]
      return ""
  }
  /^        [A-Za-z].*\("/ { a = firstalias($0)
        if (a != "") { type = a; print "T " a } else { type = "?"; print "X " $0 }
        next }
  /^            - .*\("/   { a = firstalias($0)
        if (a != "") print "S " type " " a; else print "Y " $0 }
' "$LOGDIR/help.txt" > "$LOGDIR/mtypes.txt"

run_machine() {   # binary, type, subtype(may be empty), outfile  -> exit status of the run
    local bin=$1 t=$2 s=$3 out=$4 rc
    if [ -n "$s" ]; then
        timeout 25 stdbuf -o0 -e0 "$bin" -V -E "$t" -e "$s" "$DUMMY" </dev/null > "$out" 2>&1
    else
        timeout 25 stdbuf -o0 -e0 "$bin" -V -E "$t" "$DUMMY" </dev/null > "$out" 2>&1
    fi
    rc=$?
    return $rc
}

# constructed? -- did devices actually attach
constructed() { grep -qa "cpu:" "$1" && grep -qa "memory:" "$1" && echo yes || echo no; }
# sanitizer hit? -- ASan or UBSan diagnostic present. These go to stderr, which is
# unbuffered, so unlike the emulator's own stdout they survive an abort.
sanhit() { grep -acE "AddressSanitizer|runtime error:|SEGV|heap-buffer-overflow|stack-buffer|use-after-free" "$1"; }

#  diedby(): ONE DISTINGUISHABLE TOKEN per outcome, keyed on exit status only -- the same
#  shape as lib.sh's budget_class() and run_emu_progress()'s reason=. Exit status is the
#  one signal buffering cannot destroy, which is why the verdict rests on it and the
#  printed reason does not.
#    ok        exited under its own power. gxemul exits 1 on the dummy ELF ("incorrect
#              phentsize? 0, should be 32"), so 0 and 1 are both normal here.
#    abort     SIGABRT: an assert, or one of the `fatal(); abort();` legacy markers.
#    segv/...  killed by some other signal.
#    timeout   timeout(1) fired at 25 s. No machine here takes more than a second, so this
#              means a construction hang -- a defect, not load.
#    harness   *** NEVER EXEMPTIBLE. *** 125/126/127 are timeout(1)'s own failures: it
#              could not run, or the binary is missing or not executable. Scoring that as
#              a machine result would be the ABSENT class from run_emu_progress -- a
#              harness fault wearing a machine's name.
#    exitN     any other status. Unexpected from this binary, so it is a death too.
diedby() {
    case "$1" in
    0|1)         echo ok ;;
    124)         echo timeout ;;
    125|126|127) echo harness ;;
    132)         echo sigill ;;
    134)         echo abort ;;
    136)         echo sigfpe ;;
    139)         echo segv ;;
    *)           if [ "$1" -gt 128 ] 2>/dev/null; then echo "sig$(( $1 - 128 ))"
                 else echo "exit$1"; fi ;;
    esac
}

#  The reason text for a death: the last two things the emulator managed to write.
#  Only meaningful because of stdbuf; if it is empty, say so rather than print nothing.
#
#  TWO FILTERS, both added after reading the first real output rather than guessing at it:
#   * drop `timeout: ...` -- that is timeout(1)'s own stderr ("the monitored command dumped
#     core"), which is about the harness, not the machine, and it crowded out the useful
#     line in every one of the fifteen deaths.
#   * do NOT drop indented lines. The first draft did (`grep -av '^ '`) and it threw away
#     exactly the line that names the cause: `    TODO: Legacy rewrite` is indented, so
#     four of the fifteen reported a bare `machine:` and said nothing at all.
death_reason() {
    local r
    r=$(grep -av '^timeout:' "$1" 2>/dev/null | grep -av '^[[:space:]]*$' \
        | tail -2 | sed 's/^[[:space:]]*//' | tr '\n' '|' | sed 's/|$//')
    printf '%s' "${r:-<no output -- diagnostic lost, check stdbuf>}"
}

n_unparsed=$(grep -c '^[XY] ' "$LOGDIR/mtypes.txt")
n_types=$(grep -c '^T ' "$LOGDIR/mtypes.txt")
[ "$n_unparsed" != 0 ] && {
    note "machine lines in -H that yielded no usable alias:"
    grep '^[XY] ' "$LOGDIR/mtypes.txt" | sed 's/^/       /'
}

n_total=0; n_built=0; n_regress=0; n_fixed=0; n_both=0
n_died=0; n_die_regress=0; n_harness=0
died_list=""; died_unexempt=""; built_types=""
: > "$LOGDIR/asan_findings.txt"
: > "$SHELLERR"

#  THE WORK LIST: every type BARE (coverage of the no-`-e` path, which is what most of
#  this gate used to be) followed by every type/subtype pair. MEASURED on the 2026-07-29
#  ASan build: 41 types + 58 subtypes = 99 combinations, and the whole gate -- both
#  binaries, 198 emulator launches -- runs in 55 s wall. Nothing here is bounded or
#  sampled; if a future edit bounds it, print what was dropped.
{ grep '^T ' "$LOGDIR/mtypes.txt" | awk '{print $2" "}'
  grep '^S ' "$LOGDIR/mtypes.txt" | awk '{print $2" "$3}' ; } > "$LOGDIR/worklist.txt"

printf "  %-14s %-16s %-9s %-8s %-8s %-8s %s\n" \
       "machine" "subtype" "built" "died" "pristine" "HEAD" "reason (if it died)"
while read -r t s; do
    key="$t/${s:--}"
    #  *** THE SHELL PRINTS "Aborted (core dumped)" FOR A SIGNAL-KILLED CHILD, ON ITS OWN
    #  STDERR, AT THE CALL SITE. ***  Measured: it is NOT suppressible from inside
    #  run_machine -- `( ... ) 2>/dev/null` around the command still leaks one line per
    #  death, because the shell doing the reporting is the one running the loop. Redirect
    #  it HERE, to a file, and report anything unexpected afterwards. Discarding it would
    #  hide a genuine harness error; leaving it interleaved makes fifteen deaths look like
    #  the gate itself crashing.
    run_machine "$ASAN_HEAD" "$t" "$s" "$LOGDIR/asan_head.txt" 2>>"$SHELLERR"
    rc=$?
    built=$(constructed "$LOGDIR/asan_head.txt")
    h=$(sanhit "$LOGDIR/asan_head.txt")
    d=$(diedby "$rc")
    reason=""; [ "$d" != ok ] && reason=$(death_reason "$LOGDIR/asan_head.txt")

    p="-"; pd="-"
    if [ -x "$ASAN_PRI" ]; then
        run_machine "$ASAN_PRI" "$t" "$s" "$LOGDIR/asan_pri.txt" 2>>"$SHELLERR"
        prc=$?
        p=$(sanhit "$LOGDIR/asan_pri.txt")
        pd=$(diedby "$prc")
    fi

    n_total=$((n_total+1))
    if [ "$built" = yes ]; then
        n_built=$((n_built+1))
        case " $built_types " in *" $t "*) ;; *) built_types="$built_types $t" ;; esac
    fi
    printf "  %-14s %-16s %-9s %-8s %-8s %-8s %s\n" \
           "$t" "${s:--}" "$built" "$d" "$p" "$h" "$(printf '%s' "$reason" | cut -c1-58)"

    if [ "$d" = harness ]; then
        n_harness=$((n_harness+1))
        echo "HARNESS $key -- timeout(1) could not run the binary (rc=$rc)" >> "$LOGDIR/asan_findings.txt"
    elif [ "$d" != ok ]; then
        n_died=$((n_died+1)); died_list="$died_list $key"
        ab_is_exempt "$key" || died_unexempt="$died_unexempt $key($d)"
        echo "DIED $key -- $d -- $reason" >> "$LOGDIR/asan_findings.txt"
        #  Directional half: a machine upstream can construct and HEAD kills is the fork's
        #  doing, whatever the exemption list says.
        if [ "$pd" = ok ]; then
            n_die_regress=$((n_die_regress+1))
            echo "DEATH-REGRESSION $key -- ok upstream, $d on HEAD" >> "$LOGDIR/asan_findings.txt"
        fi
    fi

    if [ "$p" != "-" ]; then
        if [ "$p" = 0 ] && [ "$h" != 0 ]; then
            n_regress=$((n_regress+1))
            echo "REGRESSION $key -- clean upstream, $h hit(s) on HEAD" >> "$LOGDIR/asan_findings.txt"
            grep -aE "AddressSanitizer|runtime error:" "$LOGDIR/asan_head.txt" | head -3 \
                | sed 's/^/       /'
        elif [ "$p" != 0 ] && [ "$h" = 0 ]; then
            n_fixed=$((n_fixed+1))
        elif [ "$p" != 0 ] && [ "$h" != 0 ]; then
            n_both=$((n_both+1))
        fi
    fi
done < "$LOGDIR/worklist.txt"

#  Every enumerated type must construct in AT LEAST ONE of its forms. This is what
#  replaces `check_min "machine types constructed" 20`: that floor was satisfiable by 20
#  healthy types while 21 others were dead, and it is exactly what B1 walked through.
#  Per-combination construction is NOT assertable -- plenty of bare forms legitimately
#  refuse without `-e` -- but a type with no working form at all is a dead machine.
dead_types=""
for t in $(grep '^T ' "$LOGDIR/mtypes.txt" | awk '{print $2}'); do
    case " $built_types " in *" $t "*) ;; *) dead_types="$dead_types $t" ;; esac
done

#  An AB_EXEMPT entry whose machine no longer dies is a lie in the inventory, and the
#  SM_COVERED lesson from gate_offline.sh is that a manifest nothing cross-checks verifies
#  the LEDGER, not the WORK. Deleting the line is a one-line fix and the message says so.
ab_stale=""
for e in $AB_EXEMPT; do
    k=${e%%:*}
    case " $died_list " in *" $k "*) ;; *) ab_stale="$ab_stale $k" ;; esac
done

echo
note "machine types enumerated  : $n_types"
note "combinations swept        : $n_total  (every type bare, plus every subtype)"
note "of which constructed      : $n_built"
note "died (signal/timeout)     : $n_died  ->${died_list:- none}"
[ -x "$ASAN_PRI" ] && {
    note "fixed by the fork         : $n_fixed  (dirty upstream, clean on HEAD)"
    note "pre-existing, still dirty : $n_both   (reported, not failed)"
}
note "findings                  : $LOGDIR/asan_findings.txt"
#  ASan build provenance. NOT an assertion: a stale ASan tree is a build-freshness
#  question this gate cannot answer without rebuilding, and build_asan.sh is expensive.
#  It is printed because "HEAD" in the table means "HEAD as of this binary", and a reader
#  who does not know the date will over-read every green row in it.
note "ASan HEAD binary built    : $(date -r "$ASAN_HEAD" '+%Y-%m-%d %H:%M' 2>/dev/null || echo unknown)"
[ -x "$ASAN_PRI" ] && \
note "ASan pristine binary built: $(date -r "$ASAN_PRI" '+%Y-%m-%d %H:%M' 2>/dev/null || echo unknown)"

#  Anything the shell wrote while reaping the sweep that is NOT the expected job-status
#  line for a death we already counted.
unexpected=$(grep -av 'Aborted\|Segmentation fault\|Killed\|Floating point\|Illegal instruction' \
             "$SHELLERR" 2>/dev/null | grep -av '^$' | head -5)
[ -n "$unexpected" ] && { note "unexpected shell diagnostics during the sweep:"
                          printf '%s\n' "$unexpected" | sed 's/^/       /'; }

# ---- assertions ----------------------------------------------------------
#
#  *** FAILABILITY CONTROLS. ***  A gate nobody has watched fail is a gate nobody knows
#  works -- this harness's own "a green row means nothing" class. Eight mutants were BUILT
#  AND RUN against these binaries on 2026-08-21, each as a copy under /tmp (the tracked
#  file was checksummed before and after and never changed). Results, verbatim:
#
#    M0  the SHIPPED gate, unmodified          PASS (3 checks)  <- the defect, reproduced
#    M1  drop decstation/5400 from AB_EXEMPT   FAIL  "died and are NOT on AB_EXEMPT"
#    M2  put it back                           PASS (11 checks)
#    M3  list decstation/pmax, which lives     FAIL  "entries whose machine no longer dies"
#    M4  hpcmips/be-300 dated 2026-08-01       FAIL  "past its deadline OR malformed"
#    M5  hpcmips/be-300 with no date at all    FAIL  "... hpcmips/be-300(NO-DATE)"
#    M6  alias class reverted to [a-z0-9_.-]   FAIL  x2: unparsed=1 AND alpha/3000/300
#                                                    unbacked (the `/` in "3000/300")
#    M7  first-subtype-only sweeping           FAIL  x3: 56 swept; hpcmips/mvmeppc/sgi have
#                                                    no constructing form; 13 unbacked
#    M8  firstalias takes ONLY the primary     FAIL  x3: unparsed=1; ?/ip19..?/ip27 died
#        alias (the shipped B3 semantics)            unexempted; sgi/ip19..ip27 unbacked
#
#  M3 is the arm that fires when a machine gets FIXED, and M1 the arm that fires when one
#  starts dying, so the list has teeth in both directions. M8 is the one that matters most:
#  it is a ONE-TOKEN revert (`i <= n` -> `i <= 2`) and it does NOT merely re-lose SGI -- the
#  ten subtypes land under type `?` and are reported, where the shipped code silently filed
#  them under `rpi`. Losing a machine is now loud however the parse fails.
#
#  ENUMERATION IS COMPLETE. This is the B3 fix's teeth: it ties the row set to the
#  emulator's own help text instead of to a number, so it stays true when machines are
#  added or removed and goes red the moment a line stops parsing.
check "every -H machine line yielded a usable alias" "$n_unparsed" "0"

#  Floors, kept only as the "a broken enumeration cannot pass by sweeping nothing" guard
#  the original comment wanted. They are deliberately slack: the check above is the one
#  that carries correctness. A count that PINS obstructs legitimate shrinkage -- that
#  mistake is recorded in gate_offline.sh -- so these are floors and stay floors.
check_min "machine types enumerated"      "$n_types" 40
check_min "combinations swept"            "$n_total" 90

#  B1's replacement for `check_min "machine types constructed" 20`, in two halves.
check "every machine type constructs in at least one form" "${dead_types:-none}" "none"
check "machine/subtype combinations that died and are NOT on AB_EXEMPT" \
      "${died_unexempt:-none}" "none"
check "AB_EXEMPT entries whose machine no longer dies (delete the line)" \
      "${ab_stale:-none}" "none"
check "AB_EXEMPT: no entry past its deadline OR malformed" \
      "$(ab_expired "$(date +%Y-%m-%d)" $AB_EXEMPT)" "none"
check "harness faults (timeout(1) could not run the binary)" "$n_harness" "0"

if [ -x "$ASAN_PRI" ]; then
    check "machines clean upstream but dirty on HEAD"      "$n_regress" "0"
    check "machines that construct upstream but die on HEAD" "$n_die_regress" "0"
else
    degrade "no ASan pristine build -- HEAD swept, but no three-way comparison"
fi

# ------------------------------------------------------------------ #446 sgi_eaddr
#  THE VALUE CLASS, WHICH THIS GATE'S OWN INSTRUMENT CANNOT SEE.
#
#  This gate owns "every machine and every subtype is constructed correctly", and ASan is
#  its instrument for one class of wrongness: memory safety.  #446 was exactly that class
#  -- machine_sgi.c handed arcbios_init() a 40-byte buffer it never initialised, and
#  set_env() -> strdup() read 41 bytes off the end on ip12/ip28/ip30/ip35.  ASan sees that,
#  and this sweep would catch its return.
#
#  *** WHAT ASan CANNOT SEE IS A BUFFER THAT IS TERMINATED AND WRONG. ***  `snprintf(buf,
#  1, ...)` writes only the NUL: no overflow, no report, and the guest is handed an EMPTY
#  MAC address.  `sizeof(eaddr_string)` is 8 on this host and yields "08:20:3".  Both are
#  silent here and both are real defects, so the sweep needs a second oracle of a different
#  kind rather than another ASan row.
#
#  This probe is that oracle.  It breaks on arcbios_init() in a real construction of the
#  five subtypes that reach it and requires the ethernet STRING to be the formatting of the
#  MAC BYTES passed alongside it -- a provenance check, so uninitialised garbage, an empty
#  string, a truncated string and a right-shaped wrong-octet string all fail.
#
#  IT RUNS THE NORMAL BINARY, NOT THE INSTRUMENTED ONE, and that is deliberate: the
#  property is about the value the code computes, which does not depend on the sanitizer,
#  and an ASan binary under gdb buys nothing here while costing startup time.
#
#  *** IT REPLACES A DETECTOR THAT WAS VACUOUS.  ***  The first version matched six regexes
#  over machine_sgi.c.  A pass-2 panel built SIXTEEN mutants and ALL SIXTEEN SCORED 7/7 --
#  among them `0*ETHERNET_STRING_MAXLEN` (two characters, zero compiler warnings, the full
#  overflow restored and ASan-measured), `#if 0`, a comment wrapper, and -- decisively -- a
#  217-BYTE FILE CONTAINING NOTHING BUT A C COMMENT.  Every one of those dies here.
EADDRLOG=$LOGDIR/sgi_eaddr.log
EADDRBIN=${GX:-$ROOT/build/gxemul}
if [ ! -f "$HERE/sgi_eaddr_probe.py" ]; then
    check "sgi_eaddr: probe present" "no" "yes"
elif [ ! -x "$EADDRBIN" ] || ! command -v gdb > /dev/null 2>&1; then
    #  degrade(), NOT gate_skip(), and the difference is load-bearing.  gate_skip() EXITS
    #  (lib.sh:137) -- calling it here would throw away the eleven checks this sweep has
    #  already recorded and report the whole gate as SKIP, which is worse than the gap it
    #  announces.  degrade() records the gap and still reaches gate_end.  Either way the
    #  missing coverage is NAMED: silent coverage loss scored green is the class this
    #  harness exists to refuse.
    degrade "sgi_eaddr: needs build/gxemul and gdb -- NOT run, so #446 is UNCOVERED here"
else
    python3 "$HERE/sgi_eaddr_probe.py" --binary "$EADDRBIN" > "$EADDRLOG" 2>&1 || true
    sed 's/^/       /' "$EADDRLOG"
    check "sgi_eaddr: the eaddr string is the formatting of its own MAC bytes" \
          "$(grep -c 'SGI_EADDR_PASS' "$EADDRLOG")" "1"
    check_min "sgi_eaddr: rows actually run" \
          "$(grep -cE '^  \[(ok|FAIL)\] ' "$EADDRLOG")" 10
fi

# ------------------------------------------------------------------ #450 arcbios shifts
#  TEN uncast `buf[3]<<24` sites in arcbios.c -- C99 6.5.7p4 UB whenever buf[3] >= 0x80,
#  and at three 64-bit-branch sites the sign-extension makes the assembled pointer's high
#  word one too small.  Fixed by width-matched casts at all ten (four sites already had
#  them: the author knew the idiom and applied it to 4 of 14).
#
#  *** WHY THE EXISTING THREE-WAY CANNOT PIN THIS. ***  sanhit() already counts
#  `runtime error:` lines, so these shifts fed the HEAD column above -- but the gate's
#  assertion is DIRECTIONAL, and reverting the casts lands on dirty-upstream/dirty-HEAD,
#  which is scored "pre-existing, reported but not failed".  A revert is INVISIBLE to it.
#  These two rows are the pin.
#
#  Row 1 is BEHAVIOURAL: the five SGI subtypes that reach arcbios construction must
#  produce ZERO left-shift lines (and zero ASan, which re-pins #446 through the same
#  fresh binary).  It inherits gate 9's staleness caveat -- the binary is built from git
#  HEAD by build_asan.sh, and nothing yet asserts its age (tracked as `asanstale`).
#  MEASURED while building this round: a sweep against the stale binary reported the
#  PRE-fix counts with rc=0, exactly the void that caveat names.
#
#  Row 2 is a STATIC census, deliberately binary-independent so it stays load-bearing
#  even when the instrumented binary is stale: every `buf[3] << 24` in the file must be
#  cast (14 casts, 0 uncast).  It is also the ONLY row that can see the six sites no
#  current image drives with buf[3] >= 0x80 -- the sweep cannot witness those, which two
#  pass-1 seats named as the reason a UBSan-only oracle is not enough.  And it catches
#  the mutant the sweep cannot: `(buf[3]&0x7f)<<24` kills the UB, silently drops bit 31,
#  and passes every sanitizer -- but drops the cast count to 13.
#  KNOWN LOUD FALSE-POSITIVE: a comment quoting the uncast idiom reddens the census.
#  That is the safe direction; #446's NUL-byte lesson says never quote mutant syntax
#  verbatim in comments anyway.
#  *** THE LIVENESS TERM IS LOAD-BEARING, added after a pass-2 seat named the hole: ***
#  zero matching lines from a run that never CONSTRUCTED the machine is not a clean run,
#  it is an absent measurement -- a binary that dies at startup would have scored green.
#  Each subtype must show its own model line, so "never ran" reads RED, not clean.
UB450=0
for s in ip12 ip28 ip30 ip32 ip35; do
    timeout 60 "$ASAN_HEAD" -E sgi -e "$s" /dev/null > "$LOGDIR/ub450.txt" 2>&1
    sh450=$(grep -ac 'left shift of' "$LOGDIR/ub450.txt")
    as450=$(grep -ac 'ERROR: AddressSanitizer' "$LOGDIR/ub450.txt")
    live450=$(grep -ac 'model: SGI-' "$LOGDIR/ub450.txt")
    if [ "$sh450" != 0 ] || [ "$as450" != 0 ] || [ "$live450" = 0 ]; then
        UB450=$((UB450+1))
        note "#450 $s: shift=$sh450 asan=$as450 constructed=$live450 -- sites: $(grep -oE 'arcbios\.c:[0-9]+' "$LOGDIR/ub450.txt" | sort -u | tr '\n' ' ')"
    fi
done
check "arcbios shifts: five reaching SGI subtypes construct AND give ZERO ubsan+asan lines" "$UB450" "0"

#  *** THE FIRST VERSION OF THIS ROW WAS TWO GREPS AND A PASS-2 SEAT KILLED IT WITH ONE
#  TOKEN. ***  `(((uint32_t)buf[3]<<24) & 0x7fffffff)` keeps the cast SPELLING, passes
#  every sanitizer, and silently drops bit 31 -- both #450 rows stayed green over a real
#  value defect.  A pattern pins what its author thought of; the replacement freezes the
#  WHOLE statement (#444's S4 precedent) and exact-matches the multiset, so a mask insert,
#  a cast swap, a wrapper or a reorder reddens whether or not anyone predicted it.  The
#  probe strips comments and strings first, closing v1's loud false-positive too.
ARCSLOG=$LOGDIR/arcbios_shift.log
python3 "$HERE/arcbios_shift_probe.py" "$SEC/src/promemul/arcbios.c" > "$ARCSLOG" 2>&1 || true
grep -E '^  (ok|FAIL) ' "$ARCSLOG" | sed 's/^/       /'
check "arcbios shifts: every assembly statement matches its frozen form" \
      "$(grep -c 'ARCSHIFT_PASS' "$ARCSLOG")" "1"
check_min "arcbios shifts: census rows actually run" \
      "$(grep -cE '^  (ok|FAIL) ' "$ARCSLOG")" 2

#  RESIDUALS, recorded rather than fixed here (this round may edit only this file):
#   * ab_expired() is a verbatim-in-behaviour copy of gate_offline.sh's exempt_expired().
#     It belongs in lib.sh; two copies is exactly the "grep for its siblings" shape.
#   * Nothing in this harness asserts that /tmp/gx-asan-* is not months old. The note
#     above prints the date; no gate reads it.
#   * sanhit() compares NONZERO-ness, not magnitude, so a partial fix (measured: sgi/ip32
#     goes 5 hits upstream -> 2 on HEAD) reads as "pre-existing, still dirty".
gate_end
exit $?
