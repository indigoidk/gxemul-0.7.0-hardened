#!/bin/sh
#
#  #569: does generate_m88k_loadstore.c fill the 24 scaled-byte slots of the
#  m88k_loadstore[512] dispatch table, and does the COMMITTED generated table
#  (src/cpus/tmp_m88k_loadstore.c) carry the same text?
#
#  WHY THIS EXISTS.  The generator printed NULL for every scaled BYTE slot
#  (size 0 with scaledness set), while cpu_m88k_instr.c indexes the table with
#  no NULL check: xmem_slow() calls the slot, and the register-form ld/st
#  decoder installs it as ic->f.  A byte's scale factor is 1, so a scaled byte
#  access is the unscaled one, and print_function_name() already omits
#  "_scaled" for size 0; the fix deletes the NULL arm and the slots name the
#  unscaled byte handlers -- the alias this table already uses for the
#  big-endian byte slots.
#
#  TWO ARTIFACTS, AND EACH IS A FIXED SITE.  The build regenerates the table
#  only when the generator binary or the template is newer (Makefile.skel), so
#  a build compiles EITHER the committed copy or fresh output.  A reader of the
#  committed table alone stays green when only the generator is reverted; a run
#  of the generator alone stays green when only the committed table is.  So
#  this compiles and runs the REAL generator in a scratch copy -- NEVER in the
#  repo: it prints the table to stdout and the table is TRACKED -- reads the
#  committed table separately, pins BOTH with the same rows, and asserts the two
#  are byte-identical.
#
#  THE EXPECTED NAMES ARE HARD-CODED BELOW, never read from either artifact: a
#  tracked generated file is not evidence about its own generator (#406), and
#  slot[i] == slot[i-32] holds under a joint rename and under NULL == NULL.
#
#  CONTRACT -- what this detector is designed to catch:
#    * the deleted arm's 24 cells, by ABSOLUTE name equality in both artifacts.
#      ALL 24 ARE THE FLOOR: main()'s own loops emit every one of them, so an
#      escape at any of the 24 is a floor breach.  16 are today's GUEST-
#      CONSUMER subset, marked "(consumer)": the sync ld/st cells, both
#      endians, plain and .usr (160 164 168 176 180 184 224 228 232 240 244
#      248), and the no-PC-sync plain ld.bu/st.b cells (416 420 432 436).  The
#      other 8 (424 440 480 484 488 496 500 504) are marked "(no consumer)" --
#      a fact about today's callers, not a weaker pin; xmem becomes the
#      consumer of 480 484 496 500 if m88kxmemusr is fixed;
#    * the accept side of the deleted predicate (size == 0 && scaledness), by
#      the de-escalation rule's row per adjacent modelled value: the scaled
#      HALFWORD cells 161/177 (size 1, the adjacent size; with the `size > 0`
#      in print_function_name moved by one they are the name rows that
#      change), scaled word xmem 418 422 434 438, and the unscaled byte cells;
#    * 54 DISTINCT NAME PINS PER ARTIFACT: the 24 repairs, their 24 unscaled
#      counterparts at index-32, and 6 further accepts (161 177 418 422 434
#      438).  Three counterparts are also accept cells (144 400 404); each of
#      those indices is emitted ONCE, as an accept row, so 21 rows are
#      "counterpart" rows;
#    * structure: one 512-entry initializer; 272 NULL entries, SUPPLEMENTARY (a
#      MOVED NULL keeps the count -- the absolute pins carry the floor);
#    * a NARROW SUPPRESSION-COUNT CONTROL, NOT a definition-integrity check: 198
#      `#define LS_N` blocks and the generator's stderr generated_functions ==
#      198 see the deletion of loadstore()'s kept size-0-scaled early return
#      (12 more blocks) and nothing finer -- duplicate or wrong definition
#      NAMES keep both counts;
#    * fresh == committed, byte for byte;
#    * the generator compiles and links, exits 0 and prints something, and the
#      committed table is present and parseable -- each an explicit RED row,
#      never a skip.
#  ROWS: 4 generator status rows + 2 x (5 structural + 54 name pins) + 1 cmp =
#  123, every row emitted on every run.  EVERY ROW CARRIES AN IDENTITY, its
#  first field (gen_*, fresh_*, committed_*, cmp_fresh_committed), which
#  occurs exactly once in the output; gate 2 pins each identity, the total and
#  the sentinel.
#  NOT OBSERVED, deliberately: handler BODIES and the xmem exchange itself (the
#  exchanged byte, neighbour preservation, zero extension) -- guest-path
#  channels that belong to the BLOCKED rung-3 witness record,
#  regress/artifacts/m88kscaledbyte/witness_attempt_20261022/WITNESS_ATTEMPT.md;
#  per-slot positions of the other three NULL arms (held only by the count);
#  scaled doubleword names; the immediate-form byte cells; the size tests in
#  print_function_name beyond the halfword edge; the generated DEFINITIONS
#  beyond their count (unique names, flags, references -- the generated file
#  is not compiled here).  A name swap among UNPINNED cells (e.g. the scaled
#  word/halfword cells not in the accept set, 185/186), made in both
#  artifacts, keeps every row green: outside the contract.
#
#  (c): measured at regress/artifacts/m88kscaledbyte/table1_20261022/L3_commentgen.out
#  (a comment-only generator: the compile row and every fresh-side row red) and
#  .../L4_commenttable.out (a comment-only table: every committed-side row red).
#  .../L8_allnull.out (an all-NULL initializer) is supplementary.  SCORES.txt there.
#
#  Overrides, so a table of variants runs WITHOUT touching the repo:
#  GEN=<generator source>, TABLE=<committed table>, CC=<compiler> (default cc,
#  else gcc; gate 2 passes its own).  Gate 2 clears GEN and TABLE so it always
#  tests the committed files.
#
#  Offline: a C compiler, no guest, no build tree.  Wired into gate 2.
set -u

HERE=$(cd "$(dirname "$0")" && pwd)
SEC=$(cd "$HERE/.." && pwd)
GEN=${GEN:-$SEC/src/cpus/generate_m88k_loadstore.c}
TABLE=${TABLE:-$SEC/src/cpus/tmp_m88k_loadstore.c}
CC=${CC:-$(command -v cc >/dev/null 2>&1 && echo cc || echo gcc)}

WORK=${TMPDIR:-/tmp}/gxsec-m88klsgen.$$
#  A killed run must not reach the sentinel: the signal trap EXITS (and the exit
#  trap cleans up), it does not resume the script.
trap 'rm -rf "$WORK"' 0
trap 'exit 1' 1 2 3 15
rm -rf "$WORK"; mkdir -p "$WORK"

rows=0
fails=0
row() {   # $1 identity  $2 description  $3 got  $4 want -- equality; every row counts
    rows=$((rows + 1))
    if [ "$3" = "$4" ]; then
        printf '  ok   %-20s %-50s %s\n' "$1" "$2" "$3"
    else
        fails=$((fails + 1))
        printf '  FAIL %-20s %-50s got=%s want=%s\n' "$1" "$2" "$3" "$4"
    fi
}
note() { printf '  --   %s\n' "$1"; }

note "GEN   $GEN"
note "TABLE $TABLE"

#  index class expected-name description.  R repair with a guest consumer today,
#  N repair with none, A accept, C counterpart (index - 32) of a repair.
#  index = no_pc_sync + registeroffset + usr + scaledness + endianness +
#  signedness + store + size: a SUM of the generator's flag-VALUED loop
#  variables, each 0 or its flag (256, 128, 64, 32, 16, 8, 4), size 0..3.
cat > "$WORK/spec" <<'EOF'
160 R m88k_instr_ld_u_1_le_regofs scaled ld.bu le sync
164 R m88k_instr_st_1_le_regofs scaled st.b le sync
168 R m88k_instr_ld_1_le_regofs scaled ld.b le sync
176 R m88k_instr_ld_u_1_le_regofs scaled ld.bu be sync
180 R m88k_instr_st_1_le_regofs scaled st.b be sync
184 R m88k_instr_ld_1_le_regofs scaled ld.b be sync
224 R m88k_instr_ld_u_1_le_usr_regofs scaled ld.bu le usr sync
228 R m88k_instr_st_1_le_usr_regofs scaled st.b le usr sync
232 R m88k_instr_ld_1_le_usr_regofs scaled ld.b le usr sync
240 R m88k_instr_ld_u_1_le_usr_regofs scaled ld.bu be usr sync
244 R m88k_instr_st_1_le_usr_regofs scaled st.b be usr sync
248 R m88k_instr_ld_1_le_usr_regofs scaled ld.b be usr sync
416 R m88k_instr_ld_u_1_le_regofs_nopcsync scaled ld.bu le nosync
420 R m88k_instr_st_1_le_regofs_nopcsync scaled st.b le nosync
424 N m88k_instr_ld_1_le_regofs_nopcsync scaled ld.b le nosync
432 R m88k_instr_ld_u_1_le_regofs_nopcsync scaled ld.bu be nosync
436 R m88k_instr_st_1_le_regofs_nopcsync scaled st.b be nosync
440 N m88k_instr_ld_1_le_regofs_nopcsync scaled ld.b be nosync
480 N m88k_instr_ld_u_1_le_usr_regofs_nopcsync scaled ld.bu le usr nosync
484 N m88k_instr_st_1_le_usr_regofs_nopcsync scaled st.b le usr nosync
488 N m88k_instr_ld_1_le_usr_regofs_nopcsync scaled ld.b le usr nosync
496 N m88k_instr_ld_u_1_le_usr_regofs_nopcsync scaled ld.bu be usr nosync
500 N m88k_instr_st_1_le_usr_regofs_nopcsync scaled st.b be usr nosync
504 N m88k_instr_ld_1_le_usr_regofs_nopcsync scaled ld.b be usr nosync
161 A m88k_instr_ld_u_2_le_scaled_regofs scaled ld.hu le sync (halfword)
177 A m88k_instr_ld_u_2_be_scaled_regofs scaled ld.hu be sync (halfword)
418 A m88k_instr_ld_u_4_le_scaled_regofs_nopcsync scaled word ld le nosync (xmem)
422 A m88k_instr_st_4_le_scaled_regofs_nopcsync scaled word st le nosync (xmem)
434 A m88k_instr_ld_u_4_be_scaled_regofs_nopcsync scaled word ld be nosync (xmem)
438 A m88k_instr_st_4_be_scaled_regofs_nopcsync scaled word st be nosync (xmem)
144 A m88k_instr_ld_u_1_le_regofs unscaled ld.bu be sync
400 A m88k_instr_ld_u_1_le_regofs_nopcsync unscaled ld.bu be nosync
404 A m88k_instr_st_1_le_regofs_nopcsync unscaled st.b be nosync
128 C m88k_instr_ld_u_1_le_regofs unscaled ld.bu le sync
132 C m88k_instr_st_1_le_regofs unscaled st.b le sync
136 C m88k_instr_ld_1_le_regofs unscaled ld.b le sync
148 C m88k_instr_st_1_le_regofs unscaled st.b be sync
152 C m88k_instr_ld_1_le_regofs unscaled ld.b be sync
192 C m88k_instr_ld_u_1_le_usr_regofs unscaled ld.bu le usr sync
196 C m88k_instr_st_1_le_usr_regofs unscaled st.b le usr sync
200 C m88k_instr_ld_1_le_usr_regofs unscaled ld.b le usr sync
208 C m88k_instr_ld_u_1_le_usr_regofs unscaled ld.bu be usr sync
212 C m88k_instr_st_1_le_usr_regofs unscaled st.b be usr sync
216 C m88k_instr_ld_1_le_usr_regofs unscaled ld.b be usr sync
384 C m88k_instr_ld_u_1_le_regofs_nopcsync unscaled ld.bu le nosync
388 C m88k_instr_st_1_le_regofs_nopcsync unscaled st.b le nosync
392 C m88k_instr_ld_1_le_regofs_nopcsync unscaled ld.b le nosync
408 C m88k_instr_ld_1_le_regofs_nopcsync unscaled ld.b be nosync
448 C m88k_instr_ld_u_1_le_usr_regofs_nopcsync unscaled ld.bu le usr nosync
452 C m88k_instr_st_1_le_usr_regofs_nopcsync unscaled st.b le usr nosync
456 C m88k_instr_ld_1_le_usr_regofs_nopcsync unscaled ld.b le usr nosync
464 C m88k_instr_ld_u_1_le_usr_regofs_nopcsync unscaled ld.bu be usr nosync
468 C m88k_instr_st_1_le_usr_regofs_nopcsync unscaled st.b be usr nosync
472 C m88k_instr_ld_1_le_usr_regofs_nopcsync unscaled ld.b be usr nosync
EOF

#  The #375 reader (gate_offline.sh's ls_entry), parametrized by file, array
#  name and size, and run ONCE per artifact: every entry of the FIRST
#  `(*<array>[<size>])(...) = {` initializer, one per line, in index order.
#  This table ends `<last entry> };` on the entry's own line, so the end test is
#  "the line holds the closing brace" rather than ls_entry's `^};`.
#  Prints "<initializers> <entries> <NULL entries>".
parse() {   # $1 file  $2 array  $3 size  $4 entries-out
    : > "$4"
    if [ ! -f "$1" ]; then echo "0 0 0"; return; fi
    awk -v arr="$2" -v size="$3" -v out="$4" '
        index($0, "(*" arr "[" size "])") && /= *[{]/ {
            inits++; if (inits == 1) f = 1; next }
        f { last = ($0 ~ /[}]/); gsub(/[ \t,};]/, "")
            if ($0 != "") { n++; print > out; if ($0 == "NULL") nul++ }
            if (last) f = 0 }
        END { printf "%d %d %d\n", inits, n, nul }' "$1"
}
ent() { sed -n "$(($2 + 1))p" "$1"; }   # $1 entries file  $2 index

#  Every row is emitted on every run -- a missing artifact turns its rows RED,
#  it never removes them -- so the row count is constant and gate 2 pins it.
artifact_rows() {   # $1 label  $2 file
    lbl=$1; file=$2
    counts=$(parse "$file" m88k_loadstore 512 "$WORK/$lbl.ent")
    #  The trailing zeros keep $1..$3 set (set -u) if the parse printed nothing.
    set -- $counts 0 0 0
    if [ ! -f "$file" ]; then present=absent
    elif [ "$1" -ge 1 ]; then present=yes
    else present="no m88k_loadstore[512] initializer"; fi
    row "${lbl}_present" "present and parseable" "$present" "yes"
    row "${lbl}_inits" "m88k_loadstore[512] initializers" "$1" "1"
    row "${lbl}_entries" "initializer entries" "$2" "512"
    row "${lbl}_nulls" "NULL entries (supplementary)" "$3" "272"
    if [ -f "$file" ]; then nls=$(grep -c '^#define LS_N ' "$file"); else nls=absent; fi
    row "${lbl}_lsn" "#define LS_N blocks (suppression count)" "$nls" "198"
    while read -r i c name desc; do
        case $c in
        R) id=${lbl}_pin$i; d="repair $desc (consumer)" ;;
        N) id=${lbl}_pin$i; d="repair $desc (no consumer)" ;;
        A) id=${lbl}_acc$i; d="accept $desc" ;;
        *) id=${lbl}_cp$i;  d="counterpart $desc" ;;
        esac
        row "$id" "$d" "$(ent "$WORK/$lbl.ent" "$i")" "$name"
    done < "$WORK/spec"
}

# ------------------------------------------------- the generator, run for real
compiled=no
if [ ! -f "$GEN" ]; then
    gres="no -- source absent"
elif ! cp "$GEN" "$WORK/generate_m88k_loadstore.c" 2>/dev/null; then
    gres="no -- source unreadable"
elif ( cd "$WORK" && $CC -o generate_m88k_loadstore generate_m88k_loadstore.c ) \
        > "$WORK/cc.log" 2>&1 && [ -x "$WORK/generate_m88k_loadstore" ]; then
    gres=yes; compiled=yes
else
    gres="no -- the compile or link failed"
fi
row gen_compiles "generator: compiles and links" "$gres" "yes"
if [ "$compiled" != yes ] && [ -s "$WORK/cc.log" ]; then
    sed -e "s|$WORK/||g" -e 's/^/  --   cc: /' "$WORK/cc.log" | head -6
fi

#  EXECUTION is its own pair of rows: a generator that compiles and then exits
#  non-zero, or prints nothing, is red here and not only downstream.
if [ "$compiled" = yes ]; then
    ( cd "$WORK" && ./generate_m88k_loadstore > fresh.c 2> gen.err ); grc=$?
else
    grc="not run"
fi
row gen_exit "generator: exit status" "$grc" "0"
if [ "$compiled" != yes ]; then sres="not run"
elif [ -s "$WORK/fresh.c" ]; then sres=yes
else sres="no -- stdout empty"; fi
row gen_stdout "generator: stdout non-empty" "$sres" "yes"
if [ -f "$WORK/gen.err" ]; then
    gf=$(sed -n 's/^.*: generated_functions = \([0-9][0-9]*\)$/\1/p' "$WORK/gen.err" | head -1)
    [ -n "$gf" ] || gf="not reported"
else
    gf=absent
fi
row gen_count "generator: stderr generated_functions" "$gf" "198"

# ---------------------------------------------------- both artifacts, same rows
artifact_rows fresh "$WORK/fresh.c"
artifact_rows committed "$TABLE"

if [ ! -f "$WORK/fresh.c" ]; then cres="fresh output absent"
elif [ ! -f "$TABLE" ]; then cres="committed table absent"
elif cmp -s "$WORK/fresh.c" "$TABLE"; then cres=identical
else cres=differ; fi
row cmp_fresh_committed "fresh == committed, byte for byte (cmp)" "$cres" "identical"
if [ "$cres" = differ ]; then
    diff "$WORK/fresh.c" "$TABLE" | head -8 | sed 's/^/  --   diff: /'
fi

printf '\nROWS=%d FAIL=%d\n' "$rows" "$fails"
printf 'M88KLS_DONE\n'
if [ "$fails" = 0 ]; then exit 0; else exit 1; fi
