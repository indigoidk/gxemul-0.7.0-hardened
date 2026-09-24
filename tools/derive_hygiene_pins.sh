#!/bin/bash
#  derive_hygiene_pins.sh -- re-derive gate_hygiene.sh's census pins FROM THE GATE'S OWN ENUMERATORS, instead of
#  hand-editing numbers.  (hygienecensus, 2026-09-19: EXPECT_PTY_PROBES sat at 46 while 24 pty probes were committed
#  over two weeks, and nothing said so until a pre-flight read of the weekly battery.)
#
#  The COUNTS are the gate's own: it extracts the gate's enumerator functions (py_code, probe_code, pty_driving,
#  pty_code) and assignment lines (bare/allends/full/unknown, _ptylist/_ptyn/_promptless, conv_*, whole_files,
#  whole_full) out of gate_hygiene.sh by name and evaluates them -- so an edit to how the gate counts flows in here.
#  An enumerator it cannot find is a hard error, never a zero.  (The promptless NAME comparison -- NEW and GONE -- is
#  its own code, written to agree with the gate's names row.)
#
#    derive_hygiene_pins.sh                           report: got vs pinned per census, the promptless names that
#                                                     differ, and the untracked files the censuses count
#    derive_hygiene_pins.sh --write [--ruling TEXT]   rewrite EXPECT_BARE and EXPECT_UNKNOWN (only ever DOWN),
#                                                     EXPECT_PTY_PROBES, EXPECT_CONVERTED, EXPECT_WHOLE_FULL and
#                                                     WHOLE_FULL_FILES
#    derive_hygiene_pins.sh --grandfather F [F...]    append NAMED new promptless probes to GRANDFATHERED_PROMPTLESS
#    derive_hygiene_pins.sh --release F [F...]        remove NAMED grandfathered probes that are no longer promptless
#      Both REFUSE a missing name list, a name given twice, a name that is empty or holds any byte but ASCII
#      letters, digits, '.', '_', '-' and '/' (the list is space-separated, it is written into a double-quoted shell
#      string where `$`, a backtick, a double quote or a backslash is live, and a glob character expands wherever a
#      list is expanded unquoted (this tool's NEW and GONE lists and the gate's NEW list run under `set -f` since F6b,
#      this tool's UNTRACKED list since F6c; the gate's `whole_full` sum still expands its list unquoted -- filed,
#      hygienecensusexotic; no real probe name needs one) -- so all of those are refused: rename the probe), and a
#      name that is not eligible
#      (already grandfathered / not a NEW promptless probe; not a grandfathered name that is no longer promptless).
#      --release matches names EXACTLY.  And Python's own parser is asked at the decision: --grandfather refuses a
#      probe it finds a readiness call in, or cannot read; --release refuses a probe still in the pty census that it
#      finds none in, and one that left the census but still makes a pty another way (forkpty, pty.spawn).
#
#  --write REFUSES, each with its reason printed, and the refusals are the point of the tool:
#    * the pty denominator is 0 -- the enumerators saw nothing (wrong tree, moved file);
#    * the three #392 counts (anchor, echo, fresh mark) disagree -- one pin, and a disagreement IS a defect;
#    * a whole-buffer entry is not "name:count" with the name in the names' allow-list below and naming a FILE --
#      WHOLE_FULL_FILES is the other double-quoted string this tool writes names into;
#    * a census value is not a count, or the token classifier fails its canaries (DERIVE_FAIL, before any report);
#  and BOTH writers check every field against its grammar immediately before writing -- counts, name:count tokens,
#  names, the ruling (printable ASCII without `"`, `\`, `$` or a backtick) and the change note (printable ASCII) --
#  so a value no check above anticipated is refused at the sink;
#    * a promptless probe is neither grandfathered nor given prompt detection, or a grandfathered probe is no longer
#      promptless -- the gate grades the NAMES, so --grandfather / --release first;
#    * EXPECT_BARE or EXPECT_UNKNOWN would RISE -- defects the gate freezes at their pins (they may fall);
#    * WITHOUT A RULING: EXPECT_CONVERTED would FALL (a #392 guard removed -- or an enumerator narrowed until it sees
#      nothing), or EXPECT_WHOLE_FULL / WHOLE_FULL_FILES would change AT ALL (#392 measured the whole-buffer form at
#      0/80; a site added, moved, respelled or converted is a decision, not a recount).
#  --ruling "YYYY-MM-DD: <who ruled and why>" names that decision; it must look like one -- non-empty, printable
#  ASCII only (so ONE line), a real calendar day (in UTC; its age is not checked), at least 16 letters or digits of
#  reason, no double quote, backslash, `$` or backtick; these check the FORM of a warrant, not who gave it -- and
#  --write writes it
#  into the gate as a comment line above each pin change that needed it, so that change carries its warrant in the
#  diff.  (A pin that moves without needing one -- the denominator, a rising #392 count -- gets no note.)
#  (hygienecensus 2026-09-23, two measured passes: the first version raised EXPECT_UNKNOWN and EXPECT_WHOLE_FULL, never
#  derived WHOLE_FULL_FILES, re-pinned to zero on an empty population and reported success after its writer failed;
#  the second let EXPECT_CONVERTED fall silently, re-pinned two censuses to 0 after a one-character enumerator edit,
#  and took its escape hatch from an environment variable that left no record and accepted "no".  The closing pass
#  found the ruling's replacement accepting a NEWLINE -- the format check matched one line, and the rest landed in
#  the gate as live shell (controls_c2/t_rnl) -- and --release matching `foo.py` inside `pref-foo.py`.  That
#  repair's own pass found an impossible date, a punctuation-only reason and non-ASCII blanks or separators accepted
#  in a ruling (each landed inside the comment line; none reached a pin), and a name holding `$`, a backtick, a
#  quote or a backslash -- or no name at all -- written into the double-quoted list.  And that repair's own pass
#  found a name whose one disallowed byte was a LINE FEED accepted (one argument grandfathered two names), a real
#  date refused where the
#  local calendar skips a midnight, the gate's census lines run by a `python3` that did nothing (git-bash's Store
#  stub: --release then accepted a probe still promptless), a list writer that would have written into a comment
#  quoting the assignment, and whole-buffer FILE names written into WHOLE_FULL_FILES with no allow-list at all.)
#
#  Run it from anywhere; HERE is the regress directory beside this script's tools/ directory ($GXROOT overrides).
set -u
PY=""; for c in python3 python; do "$c" -c "import sys" >/dev/null 2>&1 && { PY=$c; break; }; done   # RUN it: a Windows Store stub exists and fails
[ -n "$PY" ] || { echo "DERIVE_FAIL: no working python"; exit 2; }
ROOT=${GXROOT:-$(cd "$(dirname "$0")/../.." && pwd)}
HERE="$ROOT/GXEMUL-SEC/regress"
[ -d "$HERE" ] || HERE="$(cd "$(dirname "$0")/../regress" 2>/dev/null && pwd)"
G="$HERE/gate_hygiene.sh"
[ -f "$G" ] || { echo "DERIVE_FAIL: no gate_hygiene.sh at $G"; exit 2; }
MODE=report; GF=(); RULING=""
case "${1:-}" in
    --write) MODE=write; shift
             if [ "${1:-}" = --ruling ]; then
                 [ -n "${2:-}" ] || { echo "REFUSED: --ruling needs its text -- an empty ruling is no ruling"; exit 2; }
                 RULING="$2"; shift 2
             fi
             [ $# -eq 0 ] || { echo "usage: $0 --write [--ruling \"YYYY-MM-DD: text\"]"; exit 2; } ;;
    --grandfather) MODE=grandfather; shift; GF=("$@") ;;
    --release) MODE=release; shift; GF=("$@") ;;
    "") ;;
    *) echo "usage: $0 [--write [--ruling TEXT] | --grandfather FILE... | --release FILE...]"; exit 2 ;;
esac
if [ -n "$RULING" ]; then
    #  PRINTABLE ASCII ONLY, byte by byte: `grep` tests LINES, so a newline let a valid first line carry live shell
    #  into the gate (the census closing pass, measured), and a [[:cntrl:]] test then let through what the locale does
    #  not call a control -- a non-breaking space, U+0085, U+2028 (the F3 pass; each stayed inside the comment line).
    [ $(( $(printf '%s' "$RULING" | LC_ALL=C tr -d ' -~' | wc -c) )) -eq 0 ] \
        || { echo "REFUSED: the ruling text must be printable ASCII, on one line"; exit 2; }
    printf '%s' "$RULING" | grep -qE '^[0-9]{4}-[0-9]{2}-[0-9]{2}: .{16,}$' \
        || { echo "REFUSED: a ruling reads \"YYYY-MM-DD: <who ruled and why>\" (16+ characters of reason) -- got [$RULING]"; exit 2; }
    _day=${RULING%%:*}
    #  in UTC: a local calendar can skip a midnight (a DST change), and GNU date then refuses a real day (the F4 pass)
    [ "$(date -u -d "$_day" +%F 2>/dev/null)" = "$_day" ] || { echo "REFUSED: [$_day] is not a calendar date"; exit 2; }
    case "$RULING" in *'"'*|*'\'*|*'$'*|*'`'*) echo "REFUSED: the ruling text may not contain a double quote, a backslash, \$ or a backtick"; exit 2 ;; esac
    _why=$(printf '%s' "${RULING#*: }" | LC_ALL=C tr -cd 'A-Za-z0-9')
    [ ${#_why} -ge 16 ] || { echo "REFUSED: a ruling needs at least 16 letters or digits of reason -- got [$RULING]"; exit 2; }
fi

fn() {  # extract a shell function definition by name: from `name() {` through the first line ending in `}`
    awk -v n="$1" 'index($0, n "() {")==1 {p=1} p {print} p && /}[[:space:]]*$/ {exit}' "$G"
}
asg() { # extract an assignment by variable name: continue while the line ends in a backslash OR a single quote is
        # still open (the gate writes `tr ' ' '<newline>'` with a LITERAL newline inside the quotes)
    awk -v n="$1" 'index($0, n "=")==1 {p=1}
        p {print; q += gsub(/\047/, "\047"); if ($0 !~ /\\$/ && q % 2 == 0) exit}' "$G"
}
CODE=""
for f in py_code probe_code pty_driving pty_code; do
    d=$(fn $f); [ -n "$d" ] || { echo "DERIVE_FAIL: enumerator $f() not found in gate_hygiene.sh"; exit 3; }
    CODE="$CODE$d"$'\n'
done
for v in bare allends full unknown _ptylist _ptyn _promptless conv_anchor conv_echo conv_mark whole_files whole_full; do
    a=$(asg $v); [ -n "$a" ] || { echo "DERIVE_FAIL: assignment $v= not found in gate_hygiene.sh"; exit 3; }
    CODE="$CODE$a"$'\n'
done
GP=$(awk 'index($0,"GRANDFATHERED_PROMPTLESS=")==1 {p=1} p {print} p && /"[[:space:]]*$/ && NR>1 && !/^GRANDFATHERED_PROMPTLESS="[^"]*$/ {exit}' "$G")
eval "$GP"
#  The gate's census lines call `python3` BY NAME.  Under git-bash that can be the Windows Store stub, which exits
#  without running anything: the classifier printed nothing, all 43 grandfathered names read as GONE, the report said
#  "--release them", and --release accepted a probe that is still promptless (the census F4 pass, the Opus seat,
#  measured).  So run them with the interpreter found above, and check that the classifier ANSWERS before using its
#  output -- in BOTH of its modes and on BOTH of its paths, on canaries in a fresh temp directory (the F5 canary
#  exercised only the unreadable-path branch, and a real file of its name would have failed it; codex, the F5 pass):
#  a file holding one whole-buffer call is NOT promptless and holds 1 whole site; a path that does not exist IS listed.
#  That is a LIVENESS check, not a proof: a classifier that dies part-way through the real tree, or misclassifies a
#  readable file, passes it (the F5 pass: grok, codex; the Opus seat measured a crash after ten inputs), and its
#  report can then be wrong.  So --release is re-checked by Python's own parser, and --write refuses while any
#  grandfathered name reads as no longer promptless -- but a broken classifier's WHOLE-BUFFER count still reaches
#  a --write that carries a ruling (the F6 pass, the Opus seat, S14).  The report, and a ruled write, stay unproven
#  against a broken classifier (filed LOW, owner ruling 2026-09-23).
#  ALWAYS through the interpreter found above, and with CRs stripped: Windows python writes CRLF, and under git-bash the
#  CRs rode into whole_files and refused every --write ("rename the probe"; the F5 pass, the Opus seat).  `command`
#  so a PY of "python3" does not call this function again.
python3() { command "$PY" "$@" | tr -d '\r'; }
_cd=$(mktemp -d 2>/dev/null) && [ -d "$_cd" ] || { echo "DERIVE_FAIL: no temp directory for the classifier canary"; exit 3; }
printf 'buf.rstrip().ends''with("GXemul>")\n' > "$_cd/zz_canary_call.py"
_c1=$(printf 'zz_canary_call.py\n' | python3 "$HERE/census_tokens.py" promptless "$_cd" 2>/dev/null)
_c2=$(printf 'zz_canary_call.py\n' | python3 "$HERE/census_tokens.py" whole "$_cd" 2>/dev/null)
_c3=$(printf 'zz_canary_absent.py\n' | python3 "$HERE/census_tokens.py" promptless "$_cd" 2>/dev/null)
rm -rf "$_cd"
[ -z "$_c1" ] && [ "$_c2" = "zz_canary_call.py:1" ] && [ "$_c3" = "zz_canary_absent.py" ] || {
    echo "DERIVE_FAIL: the token classifier failed its canaries (promptless [$_c1], whole [$_c2], absent [$_c3]); refusing"; exit 3; }
eval "$CODE"
#  every census value is a COUNT: an enumerator or classifier line that failed can leave an empty or garbled value,
#  and three empty #392 counts compare equal (codex, the F5 pass) -- refused here.  It can also leave a clean 0:
#  every census line ends in a counter, and this check cannot tell that 0 from an empty census (the F6 pass: codex,
#  the Opus seat's S14).
for _v in bare allends full unknown _ptyn conv_anchor conv_echo conv_mark whole_full; do
    case "${!_v}" in ''|*[!0-9]*) echo "DERIVE_FAIL: the census value $_v is [${!_v}], not a count -- a census line failed"; exit 3 ;; esac
done

pin() { sed -n "s/^$1=\([0-9]*\).*/\1/p" "$G" | head -1; }
spin() { sed -n "s/^$1=\"\(.*\)\"$/\1/p" "$G" | head -1; }
[ "${_ptyn:-0}" -gt 0 ] 2>/dev/null || { echo "DERIVE_FAIL: the pty denominator is ${_ptyn:-empty} -- the enumerators saw nothing; refusing to report or write"; exit 3; }
_want=$(printf '%s' "$GRANDFATHERED_PROMPTLESS" | tr ' ' '\n' | grep -c .)
_got=$(printf '%s' "$_promptless" | grep -c .)
GFS=$(printf '%s' "$GRANDFATHERED_PROMPTLESS" | tr ' ' '\n' | grep . | LC_ALL=C sort)
NEWP=$(LC_ALL=C comm -13 <(printf '%s\n' "$GFS") <(printf '%s\n' "$_promptless" | grep .))
GONE=$(LC_ALL=C comm -23 <(printf '%s\n' "$GFS") <(printf '%s\n' "$_promptless" | grep .))
#  paths are RELATIVE to regress/ (the gate's own form since 2026-09-23), so look each one up directly.
UNTR=$(printf '%s\n' "$_ptylist" | while IFS= read -r p; do [ -z "$p" ] || git -C "$HERE" ls-files --error-unmatch "$p" >/dev/null 2>&1 || echo "$p"; done)
WFP=$(spin WHOLE_FULL_FILES)

printf '%-34s %6s %6s\n' census got pinned
printf '%-34s %6s %6s\n' EXPECT_BARE "$bare" "$(pin EXPECT_BARE)"
printf '%-34s %6s %6s\n' EXPECT_UNKNOWN "$unknown" "$(pin EXPECT_UNKNOWN)"
printf '%-34s %6s %6s\n' EXPECT_PTY_PROBES "$_ptyn" "$(pin EXPECT_PTY_PROBES)"
printf '%-34s %6s %6s\n' "promptless vs GRANDFATHERED" "$_got" "$_want"
printf '%-34s %6s %6s\n' "EXPECT_CONVERTED (anchor)" "$conv_anchor" "$(pin EXPECT_CONVERTED)"
printf '%-34s %6s %6s\n' "EXPECT_CONVERTED (echo)" "$conv_echo" "$(pin EXPECT_CONVERTED)"
printf '%-34s %6s %6s\n' "EXPECT_CONVERTED (fresh mark)" "$conv_mark" "$(pin EXPECT_CONVERTED)"
printf '%-34s %6s %6s\n' EXPECT_WHOLE_FULL "$whole_full" "$(pin EXPECT_WHOLE_FULL)"
printf '%-34s got    [%s]\n%-34s pinned [%s]\n' WHOLE_FULL_FILES "$whole_files" "" "$WFP"
#  set -f: a tree file named with a glob character must print as itself, not as the files it matches (the F5 pass
#  named all three lists; F6b quoted two)
[ -n "$NEWP" ] && { echo "NEW PROMPTLESS (neither grandfathered nor prompt-detecting):"; ( set -f; printf '  %s\n' $NEWP ); }
[ -n "$GONE" ] && { echo "GRANDFATHERED BUT NO LONGER PROMPTLESS (--release them):"; ( set -f; printf '  %s\n' $GONE ); }
[ -n "$UNTR" ] && { echo "UNTRACKED files counted by these censuses (the battery counts what is lying in the tree):"; ( set -f; printf '  %s\n' $UNTR ); }

#  run the python writer and FAIL LOUDLY if it fails -- the first version printed DERIVE_DONE after a failed write
#  astcall FILE: rc 0 if Python's parser finds a CALL of the form X.endswith(...) in FILE, 1 if it parses and finds none,
#  anything else if it cannot read or parse it -- an independent check of the token census at the grandfather/release
#  decision, with its exit status read (the census lines' is not).  "utf-8-sig", as Python itself reads a script: a
#  real probe written with a byte-order mark (agy's wdcaltdigin witness) was unreadable here, and so could be
#  neither grandfathered nor released (the F6 pass, the Opus seat, F1).
astcall() { command "$PY" - "$1" <<'PY'
import ast, sys
try:
    t = ast.parse(open(sys.argv[1], encoding="utf-8-sig").read())     # a byte-order mark is not an error (F6e)
except Exception:
    sys.exit(2)
m = "ends" + "with"
sys.exit(0 if any(isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == m
                  for n in ast.walk(t)) else 1)
PY
}
#  rc 5 is the writer's own grammar check refusing BEFORE it writes anything (F6): a refusal, and the gate is untouched.
#  `command`: PY is the NAME python3 under WSL, which the CR-stripping shim above shadows, and a pipe's status is tr's
#  -- so from F6b to F6c a writer that refused or died read as success under WSL, and the tool printed DERIVE_DONE
#  (census F6c controls, t_pyopt0: the writer's own multiplicity check failed, rc 0).  astcall already bypassed it.
pywrite() { command "$PY" - "$@"; local rc=$?; [ $rc -eq 0 ] && return; [ $rc -eq 5 ] && exit 5
            echo "DERIVE_FAIL: the writer failed (rc=$rc); nothing to trust in $G"; exit 6; }

if [ "$MODE" = grandfather ] || [ "$MODE" = release ]; then
    [ ${#GF[@]} -gt 0 ] || { echo "REFUSED: --$MODE needs the file names, one by one"; exit 4; }
    #  a name given twice was appended twice (45 entries, 44 names) and --release then could not remove it -- the
    #  census F2 pass, codex, measured on the writer itself.  One name, once.
    dup=$(printf '%s\n' "${GF[@]}" | LC_ALL=C sort | uniq -d | tr '\n' ' ')
    [ -z "$dup" ] || { echo "REFUSED: a name given more than once: $dup"; exit 4; }
    for f in "${GF[@]}"; do
        #  the list is space-separated and written into a double-quoted shell string: a name with a blank cannot be
        #  recorded (codex, the closing pass), `$`, a backtick, a double quote or a backslash is live shell there, and an EMPTY
        #  name matched the blank line an empty NEWP prints (the F3 pass).  So an allow-list, COUNTED byte by byte with
        #  wc -c: the F4 version tested $(...) for emptiness, and command substitution strips trailing newlines, so a
        #  name whose ONLY disallowed byte was a LINE FEED passed -- and grandfathered two names at once, one of them
        #  no file (the F4 pass).
        [ -n "$f" ] && [ $(( $(printf '%s' "$f" | LC_ALL=C tr -d 'A-Za-z0-9._/-' | wc -c) )) -eq 0 ] \
            || { echo "REFUSED: [$f] -- a probe name here is ASCII letters, digits, '.', '_', '-' and '/' only; rename the probe"; exit 4; }
        if [ "$MODE" = grandfather ]; then
            #  a FILE in regress/: the census's enumerators are line-based, so a file name holding a newline reaches the
            #  classifier as fragments that do not exist -- and it lists what it cannot read (codex, the F5 pass)
            [ -f "$HERE/$f" ] || { echo "REFUSED: $f is not a file under regress/"; exit 4; }
            printf '%s\n' "$GFS" | grep -qxF -- "$f" && { echo "REFUSED: $f is already grandfathered"; exit 4; }
            printf '%s\n' "$NEWP" | grep -qxF -- "$f" || { echo "REFUSED: $f is not a NEW promptless probe"; exit 4; }
            #  and Python's own PARSER agrees: no `.endswith(...)` CALL in it (the token census is not a parser -- F6b)
            astcall "$HERE/$f"; _a=$?
            [ $_a -eq 1 ] || { [ $_a -eq 0 ] && echo "REFUSED: $f -- Python's parser finds a readiness call in it; the census missed it" \
                                || echo "REFUSED: $f -- Python's parser cannot read it (rc $_a); fix the file first"; exit 4; }
        else
            printf '%s\n' "$GONE" | grep -qxF -- "$f" || { echo "REFUSED: $f is not a grandfathered name that is no longer promptless"; exit 4; }
            #  a probe still in the PTY CENSUS must now make a real `.endswith(...)` CALL, by Python's own parser: a
            #  classifier that failed part-way, or a `match` class pattern it credits, let --release take a still-
            #  promptless probe off the list (the F5 pass, the Opus seat, measured).  A probe that LEFT the census --
            #  deleted, or moved onto drive_guest so it no longer forks its own pty -- is released, unless its file still
            #  makes a pty some other way the census does not enumerate (the F6 pass, the Opus seat, F2: F6b refused it
            #  and nothing but a hand edit could clear it; its FIX-A', measured).
            if printf '%s\n' "$_ptylist" | grep -qxF -- "$f"; then
                astcall "$HERE/$f"; _a=$?
                [ $_a -eq 0 ] || { [ $_a -eq 1 ] && echo "REFUSED: $f -- the parser finds no readiness call in it: it is still promptless" \
                                   || echo "REFUSED: $f -- Python's parser cannot read it (rc $_a); fix the file first"; exit 4; }
            elif [ -e "$HERE/$f" ] && grep -qE 'forkpty|pty\.spawn' "$HERE/$f"; then
                echo "REFUSED: $f no longer says pty.fork but still creates a pty (forkpty or pty.spawn), which the census does not enumerate -- keep pty.fork, or give it prompt detection"; exit 4
            fi
        fi
    done
    pywrite "$G" "$MODE" "${GF[@]}" <<'PY'
import io, re, sys
g, mode, names = sys.argv[1], sys.argv[2], sys.argv[3:]
if not all(re.fullmatch(r"[A-Za-z0-9._/-]+", n) for n in names):
    print("REFUSED: the writer's grammar check failed for a name -- nothing written"); sys.exit(5)
s = io.open(g, encoding="utf-8", newline="").read()
#  anchored at line start, as the reader above is: an unanchored search would write into the first COMMENT that
#  quotes the assignment and leave a gate that no longer parses (the census F4 pass, the Opus seat)
ms = list(re.finditer(r'(?m)^GRANDFATHERED_PROMPTLESS="', s))
assert len(ms) == 1, "GRANDFATHERED_PROMPTLESS assignments at line start: %d" % len(ms)
i = ms[0].end(); j = s.index('"', i)
body = s[i:j]
if mode == "grandfather":
    body = body + "\n" + " ".join(names)
else:
    #  EXACT names, per line: a boundary regex matched `foo.py` inside `pref-foo.py` (codex, the closing pass)
    lines = [l.split() for l in body.split("\n")]
    for n in names:
        k = sum(l.count(n) for l in lines)
        assert k == 1, (n, k)
        lines = [[w for w in l if w != n] for l in lines]
    body = "\n".join(" ".join(l) for l in lines if l)
#  `with`: a flush that fails when the file is closed (a full disk) raises here; an unclosed temporary's destructor
#  swallowed it, and the tool printed its success line over a truncated gate (codex, the F6 pass)
with io.open(g, "w", encoding="utf-8", newline="") as fh:
    fh.write(s[:i] + body + s[j:])
print("%s: %s" % ("GRANDFATHERED" if mode == "grandfather" else "RELEASED", " ".join(names)))
PY
    echo "DERIVE_DONE"
    exit 0
fi
if [ "$MODE" = write ]; then
    #  WHOLE_FULL_FILES is the other place this tool writes FILE NAMES into a double-quoted string in the gate, and it
    #  had no allow-list: a pty file named with `$(...)` would have become shell source there on the next read (grok,
    #  the F4 pass).  PER TOKEN, "name:count" with the name in the grandfather allow-list: the F5 byte set admitted a
    #  space or a colon INSIDE a name, since both are also its separators (codex, the F5 pass).
    [ -z "$(printf '%s' "$whole_files" | tr ' ' '\n' | LC_ALL=C grep -vxE '[A-Za-z0-9._/-]+:[0-9]+')" ] \
        || { echo "REFUSED: a whole-buffer entry is not name:count with the name in A-Za-z0-9._/- -- rename the probe: [$whole_files]"; exit 5; }
    #  and every entry names a FILE: a tree file named `zz:9 x.py` splits into two well-formed entries, `zz:9` and
    #  `x.py:1`, and wrote EXPECT_WHOLE_FULL=13 for 4 real sites with every row green (the F5 pass, the Opus seat)
    for _e in $(printf '%s' "$whole_files" | tr ' ' '\n'); do
        [ -f "$HERE/${_e%:*}" ] || { echo "REFUSED: the whole-buffer entry [$_e] names no file under regress/ -- a file name the census split; rename it"; exit 5; }
    done
    #  NOT refused, and filed LOW by owner ruling (2026-09-23: a CRAFTED name is filed, not fixed): a name whose
    #  space-split pieces each read as an existing file with a count -- `arm_bdt_probe.py:9 x.py` beside a real x.py
    #  (grok, the F5 pass, on the F6 draft).  Validating the TREE's names before the census serialises them closes it.
    [ "$conv_anchor" = "$conv_echo" ] && [ "$conv_echo" = "$conv_mark" ] || {
        echo "REFUSED: the three #392 counts disagree ($conv_anchor/$conv_echo/$conv_mark) -- a guard present but uncounted; fix the probe, not the pin"; exit 5; }
    [ -z "$NEWP" ] || { echo "REFUSED: new promptless probes must be grandfathered by NAME (--grandfather) or given prompt detection first"; exit 5; }
    [ -z "$GONE" ] || { echo "REFUSED: grandfathered names are no longer promptless -- --release them first"; exit 5; }
    [ "$bare" -le "$(pin EXPECT_BARE)" ] || { echo "REFUSED: bare endswith(\">\") grew -- a defect, never re-pinned"; exit 5; }
    [ "$unknown" -le "$(pin EXPECT_UNKNOWN)" ] || { echo "REFUSED: an unrecognised endswith( spelling appeared -- a defect, never re-pinned"; exit 5; }
    NEED=""
    [ "$conv_anchor" -ge "$(pin EXPECT_CONVERTED)" ] || NEED="$NEED EXPECT_CONVERTED($(pin EXPECT_CONVERTED)->$conv_anchor)"
    [ "$whole_full" = "$(pin EXPECT_WHOLE_FULL)" ] || NEED="$NEED EXPECT_WHOLE_FULL($(pin EXPECT_WHOLE_FULL)->$whole_full)"
    [ "$whole_files" = "$WFP" ] || NEED="$NEED WHOLE_FULL_FILES([$WFP]->[$whole_files])"
    if [ -n "$NEED" ] && [ -z "$RULING" ]; then
        echo "REFUSED: these pins change only by a named decision --$NEED -- a #392 guard removed, or a whole-buffer site added, moved, respelled or converted; fix the probe, or pass --ruling \"YYYY-MM-DD: <who ruled and why>\""
        exit 5
    fi
    pywrite "$G" "$bare" "$unknown" "$_ptyn" "$conv_anchor" "$whole_full" "$whole_files" "$RULING" "$NEED" <<'PY'
import io, re, sys
g, bare, unk, pty, conv, whole, files, ruling, need = sys.argv[1:]
#  F6: THE SINK checks every field it is about to write, whatever the shell above already checked -- the class the census
#  passes kept finding one member of at a time (a newline, a `$`, a space, an empty count)
_bad = [k for k, v, rx in (("EXPECT_BARE", bare, r"[0-9]+"), ("EXPECT_UNKNOWN", unk, r"[0-9]+"),
                           ("EXPECT_PTY_PROBES", pty, r"[0-9]+"), ("EXPECT_CONVERTED", conv, r"[0-9]+"),
                           ("EXPECT_WHOLE_FULL", whole, r"[0-9]+"),
                           ("WHOLE_FULL_FILES", files, r"(?:[A-Za-z0-9._/-]+:[0-9]+(?: [A-Za-z0-9._/-]+:[0-9]+)*)?"),
                           ("the ruling", ruling, r'[ !#%&-\[\]-_a-~]*'), ("the change note", need, r"[ -~]*"))
        if not re.fullmatch(rx, v)]
if _bad:
    print("REFUSED: the writer's grammar check failed for %s -- nothing written" % ", ".join(_bad)); sys.exit(5)
s = io.open(g, encoding="utf-8", newline="").read()
note = ("#  RULING %s -- %s (tools/derive_hygiene_pins.sh --write)\n" % (ruling, need.strip())) if (ruling and need.strip()) else ""
for k, v in (("EXPECT_BARE", bare), ("EXPECT_UNKNOWN", unk), ("EXPECT_PTY_PROBES", pty), ("EXPECT_CONVERTED", conv),
             ("EXPECT_WHOLE_FULL", whole)):
    pre = note if (note and k + "(" in need) else ""
    s, n = re.subn(r"(?m)^%s=\d+" % k, lambda m, k=k, v=v, pre=pre: pre + "%s=%s" % (k, v), s, count=1)
    assert n == 1, k
pre = note if (note and "WHOLE_FULL_FILES(" in need) else ""
s, n = re.subn(r'(?m)^WHOLE_FULL_FILES="[^"\n]*"', lambda m: pre + 'WHOLE_FULL_FILES="%s"' % files, s, count=1)
assert n == 1, "WHOLE_FULL_FILES"
with io.open(g, "w", encoding="utf-8", newline="") as fh:     # `with`: see the list writer above
    fh.write(s)
print("WRITTEN: EXPECT_BARE=%s EXPECT_UNKNOWN=%s EXPECT_PTY_PROBES=%s EXPECT_CONVERTED=%s EXPECT_WHOLE_FULL=%s "
      "WHOLE_FULL_FILES=\"%s\"%s" % (bare, unk, pty, conv, whole, files, ("  RULING: " + ruling) if note else ""))
PY
fi
echo "DERIVE_DONE"
