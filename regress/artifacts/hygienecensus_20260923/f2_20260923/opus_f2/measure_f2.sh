#!/bin/bash
# opus measuring seat, hygienecensus F2 (adjudication) pass -- gate_hygiene.sh readiness rows + the deriver, on
# COPIES only.  One read-only snapshot of GXEMUL-SEC/regress (top-level files) + tools/derive_hygiene_pins.sh, one
# fresh copy per case, ONE named edit per case (edits.py), the UNMODIFIED gate and deriver run in the copy.
# Never writes under GXEMUL-SEC, est, build or build-asan.
set -u
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
HERE_ME=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/opus_f2
EDITS=$HERE_ME/edits.py
W=/tmp/opus_censusf2
OUT=$HERE_ME/runs
S=$OUT/SUMMARY.txt
T=$OUT/TABLE.txt
rm -rf "$W"; mkdir -p "$W/snap/GXEMUL-SEC/regress" "$W/snap/GXEMUL-SEC/tools" "$W/c" "$OUT"
: > "$S"; : > "$T"

# ---- the snapshot: every case starts from the SAME bytes ----
(cd "$SEC/regress" && find . -maxdepth 1 -type f -exec cp -p {} "$W/snap/GXEMUL-SEC/regress/" \;)
cp -p "$SEC/tools/derive_hygiene_pins.sh" "$W/snap/GXEMUL-SEC/tools/"
{
  echo "snapshot $(date '+%F %T') from $SEC (regress top-level files + tools/derive_hygiene_pins.sh)"
  echo "HEAD $(git -C "$SEC" rev-parse --short HEAD 2>/dev/null || echo '?')   files: $(ls "$W/snap/GXEMUL-SEC/regress" | wc -l)   .py: $(ls "$W/snap/GXEMUL-SEC/regress"/*.py | wc -l)"
  echo "tree .py recursive-minus-artifacts: $(find "$SEC/regress" -name '*.py' -type f ! -path "$SEC/regress/artifacts/*" | wc -l)  (must equal the flat count above, or the copy is not the population)"
  (cd "$W/snap/GXEMUL-SEC" && md5sum regress/gate_hygiene.sh tools/derive_hygiene_pins.sh regress/luna_absentcpu_probe.py \
      regress/arm_bdt_probe.py regress/arm_flags_probe.py regress/crime_width_probe.py regress/pcc2_width_probe.py \
      regress/arm_endian_probe.py regress/mips_rounding_probe.py regress/mips_subnorm_probe.py regress/m88k_exc_probe.py \
      regress/gdrom_cond_probe.py)
  echo "--- pins in the snapshot's gate:"
  grep -nE '^(EXPECT_[A-Z_]+|WHOLE_FULL_FILES|WHOLE_RE)=' "$W/snap/GXEMUL-SEC/regress/gate_hygiene.sh"
} > "$OUT/00_snapshot.txt" 2>&1

# the census intermediates, computed by the gate's OWN lines (everything up to its last readiness check) + one echo
cat > "$W/raw_tail.sh" <<'EOF'
_wocc=$(pty_code "$WHOLE_RE" | grep -o "$WHOLE_RE" | wc -l)
_pdn=$(pty_driving | grep -c .)
_pdx=$(LC_ALL=C comm -23 <(pty_driving | sed 's|.*/||' | LC_ALL=C sort) <(printf '%s\n' "$_ptylist" | grep . | LC_ALL=C sort) | tr '\n' ' ' | sed 's/ $//')
echo "RAW allends=$allends bare=$bare full=$full unknown=$unknown | whole_full(lines)=$whole_full whole_occurrences=$_wocc whole_files=[$whole_files] | ptyn=$_ptyn promptless=$_got/$_want new=[$_new] gone=[$_gone] | pty_driving=$_pdn in_pty_driving_not_ptylist=[$_pdx] | conv=$conv_anchor/$conv_echo/$conv_mark"
exit 0
EOF

mk() { rm -rf "$W/c/$1"; cp -a "$W/snap" "$W/c/$1"; }
rdir() { echo "$W/c/$1/GXEMUL-SEC/regress"; }
raw() {  # raw <tag> <label>
  local d n; d=$(rdir "$1")
  n=$(grep -n 'check "readiness: send takes a fresh mark (#392)"' "$d/gate_hygiene.sh" | cut -d: -f1)
  { head -n "$n" "$d/gate_hygiene.sh"; cat "$W/raw_tail.sh"; } > "$W/c/$1/zz_raw_gate.sh"
  mkdir -p "$W/c/$1/logs_raw"
  ( cd "$d" && LOGDIR="$W/c/$1/logs_raw" bash "$W/c/$1/zz_raw_gate.sh" 2>/dev/null | grep '^RAW' ) > "$OUT/$1.$2.raw"
  rm -f "$W/c/$1/zz_raw_gate.sh"
}
gate() {  # gate <tag> <label>   run the unmodified gate in the copy, grade its readiness rows
  local tag=$1 lab=$2 d; d=$(rdir "$1"); mkdir -p "$W/c/$1/logs_$lab"
  ( cd "$d" && LOGDIR="$W/c/$1/logs_$lab" bash ./gate_hygiene.sh ) > "$OUT/$tag.$lab.out" 2>&1
  grep -E 'readiness|whole-buffer' "$OUT/$tag.$lab.out" | sed 's/\x1b\[[0-9;]*m//g' > "$OUT/$tag.$lab.rows"
  raw "$tag" "$lab"
  local nf nr; nf=$(grep -cE '^\s*FAIL' "$OUT/$tag.$lab.rows"); nr=$(grep -cE '^\s*(ok|FAIL)' "$OUT/$tag.$lab.rows")
  {
    echo "   gate [$lab]: $nf FAIL of $nr readiness rows$( [ "$nf" -eq 0 ] && echo '   <-- ALL GREEN')"
    grep -E '^\s*FAIL' "$OUT/$tag.$lab.rows" | sed 's/^\s*/      /'
    sed 's/^/      /' "$OUT/$tag.$lab.raw"
  } >> "$S"
  LAST_NF=$nf
}
drv() {  # drv <tag> <label> [deriver args...]   (env WHOLE_FULL_RULING passes through if the caller exported it)
  local tag=$1 lab=$2; shift 2
  local r=$W/c/$tag g; g=$(rdir "$tag")/gate_hygiene.sh
  cp -p "$g" "$r/gate.before.$lab"
  ( GXROOT="$r" bash "$r/GXEMUL-SEC/tools/derive_hygiene_pins.sh" "$@" ) > "$OUT/$tag.$lab.drv" 2>&1; local rc=$?
  {
    echo "   deriver [$lab] $* -> rc=$rc"
    grep -E '^(EXPECT_|promptless vs|WHOLE_FULL_FILES|[[:space:]]+pinned)' "$OUT/$tag.$lab.drv" | sed 's/^/      | /'
    grep -E '^(REFUSED|WRITTEN|DERIVE_FAIL|DERIVE_DONE|GRANDFATHERED|RELEASED|WHOLE_FULL_RULING|NEW PROMPTLESS)' "$OUT/$tag.$lab.drv" | cut -c1-230 | sed 's/^/      /'
    if cmp -s "$r/gate.before.$lab" "$g"; then echo "      gate file UNCHANGED by this run"
    else echo "      gate file CHANGED by this run:"; diff "$r/gate.before.$lab" "$g" | grep '^[<>]' | cut -c1-220 | sed 's/^/         /'; fi
  } >> "$S"
  LAST_RC=$rc
}
begin() {  # begin <tag> <group>
  mk "$1"
  { echo; echo "===== $1  [$2]  $(python3 "$EDITS" --desc "$1" 2>/dev/null || echo 'unmodified copy')"; } >> "$S"
  if [ "$1" != real ]; then
    python3 "$EDITS" "$1" "$(rdir "$1")" > "$OUT/$1.edit" 2>&1 || { echo "   EDIT FAILED -- case void:"; sed 's/^/      /' "$OUT/$1.edit"; } >> "$S"
    sed 's/^/   edit:/' "$OUT/$1.edit" | cut -c1-240 >> "$S"
  fi
}
row() { printf '%-7s %-5s %s\n' "$1" "$2" "$3" >> "$T"; }   # row <tag> <verdict> <note>

# =========================== (3) the real tree, unmodified ===========================
begin real "tree"
gate real before
drv real report
drv real write --write
gate real after_write
row real "$( [ "$LAST_NF" -eq 0 ] && echo GREEN || echo "RED" )" "unmodified copy of the current tree"

# =========================== (1) the fourteen, re-measured ===========================
for c in e_c1 e_e1 e_e2 e_e3 e_e4 e_e5 e_e6 e_e7 e_e9 e_e14; do
  begin "$c" "pass-2 fourteen, gate-only"; gate "$c" gate
  row "$c" "$( [ "$LAST_NF" -eq 0 ] && echo PASS || echo "red$LAST_NF" )" "$(python3 "$EDITS" --desc "$c")"
done
for c in e_dL1 e_dL2 e_dL3 e_dL5; do
  begin "$c" "pass-2 fourteen, edit + --write"; gate "$c" before; b=$LAST_NF
  drv "$c" write --write; w=$LAST_RC
  gate "$c" after; a=$LAST_NF
  row "$c" "$( [ "$a" -eq 0 ] && echo PASS || echo "red$a" )" "before=$b FAIL, --write rc=$w, after=$a FAIL -- $(python3 "$EDITS" --desc "$c")"
done

# =========================== (2) new edits ===========================
for c in n1a n1b n1c n1d n3a n3b n3c n3d n3e n3f n3g n3h n3i n3j n3m n3k n3k2 n4a n10; do
  begin "$c" "new, gate-only"; gate "$c" gate
  row "$c" "$( [ "$LAST_NF" -eq 0 ] && echo PASS || echo "red$LAST_NF" )" "$(python3 "$EDITS" --desc "$c")"
done
for c in n2a n2b n5a n6 n8; do
  begin "$c" "new, edit + --write"; gate "$c" before; b=$LAST_NF
  drv "$c" write --write; w=$LAST_RC
  gate "$c" after; a=$LAST_NF
  row "$c" "$( [ "$a" -eq 0 ] && echo PASS || echo "red$a" )" "before=$b FAIL, --write rc=$w, after=$a FAIL -- $(python3 "$EDITS" --desc "$c")"
done
# n5b: the subdirectory copy under a grandfathered basename -- --write refuses, --grandfather accepts the name a SECOND time
begin n5b "new, edit + --grandfather + --write"; gate n5b before; b=$LAST_NF
drv n5b write1 --write; w1=$LAST_RC
drv n5b grandfather --grandfather gdrom_cond_probe.py; g1=$LAST_RC
drv n5b write2 --write; w2=$LAST_RC
gate n5b after; a=$LAST_NF
echo "      gdrom_cond_probe.py occurrences in GRANDFATHERED_PROMPTLESS after: $(awk '/^GRANDFATHERED_PROMPTLESS="/,/"$/' "$(rdir n5b)/gate_hygiene.sh" | grep -o 'gdrom_cond_probe\.py' | wc -l)" >> "$S"
drv n5b release --release gdrom_cond_probe.py; rl=$LAST_RC
row n5b "$( [ "$a" -eq 0 ] && echo PASS || echo "red$a" )" "before=$b FAIL, --write rc=$w1, --grandfather rc=$g1, --write rc=$w2, after=$a FAIL, then --release rc=$rl -- $(python3 "$EDITS" --desc n5b)"
# n7: the ruling escape hatch takes ANY non-empty value
begin n7 "new, edit + --write under WHOLE_FULL_RULING=no"; gate n7 before; b=$LAST_NF
drv n7 write_noruling --write; w0=$LAST_RC
export WHOLE_FULL_RULING=no; drv n7 write_ruling_no --write; w=$LAST_RC; unset WHOLE_FULL_RULING
gate n7 after; a=$LAST_NF
echo "      does the gate file record the ruling anywhere? lines matching WHOLE_FULL_RULING in the gate: $(grep -c 'WHOLE_FULL_RULING' "$(rdir n7)/gate_hygiene.sh")" >> "$S"
row n7 "$( [ "$a" -eq 0 ] && echo PASS || echo "red$a" )" "before=$b FAIL, --write (no ruling) rc=$w0, --write (WHOLE_FULL_RULING=no) rc=$w, after=$a FAIL"
# n9: --release trusts the lexical proxy
begin n9 "new, edit + --release + --write"; gate n9 before; b=$LAST_NF
drv n9 write1 --write; w1=$LAST_RC
drv n9 release --release gdrom_cond_probe.py; r1=$LAST_RC
drv n9 write2 --write; w2=$LAST_RC
gate n9 after; a=$LAST_NF
row n9 "$( [ "$a" -eq 0 ] && echo PASS || echo "red$a" )" "before=$b FAIL, --write rc=$w1, --release rc=$r1, --write rc=$w2, after=$a FAIL -- $(python3 "$EDITS" --desc n9)"

#  the copies under $W are LEFT for inspection (they are /tmp, outside every project tree)
echo "MEASURE_F2_DONE $(date '+%F %T')" >> "$S"
echo "MEASURE_F2_DONE" >> "$T"
echo MEASURE_F2_DONE
