#!/bin/bash
# opus measuring seat, hygienecensus F2 (adjudication) pass -- gate_hygiene.sh readiness rows + the deriver, on
# COPIES only.  One read-only snapshot of GXEMUL-SEC/regress (top-level files) + tools/derive_hygiene_pins.sh, one
# fresh copy per case, ONE named edit per case (edits.py), the UNMODIFIED gate and deriver run in the copy.
# Never writes under GXEMUL-SEC, est, build or build-asan.
set -u
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
HERE_ME=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/opus_f2
EDITS=$HERE_ME/edits.py
W=/tmp/opus_censusf2c
OUT=$HERE_ME/runs3
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
  #  THE SCRIPT MUST SIT IN THE REGRESS DIR: the gate sets HERE from its OWN location (dirname "$0"), and the
  #  promptless classifier reads basenames relative to HERE.  Run 1 placed it one level up, so HERE was wrong and
  #  every probe read as promptless in the RAW line (73/43) while the real gate's rows said 43/43 -- the diagnostic,
  #  not the gate, was broken.  A .sh file is outside every .py census, so it cannot perturb what it measures.
  local d n; d=$(rdir "$1")
  n=$(grep -n 'check "readiness: send takes a fresh mark (#392)"' "$d/gate_hygiene.sh" | cut -d: -f1)
  { head -n "$n" "$d/gate_hygiene.sh"; cat "$W/raw_tail.sh"; } > "$d/zz_raw_gate.sh"
  mkdir -p "$W/c/$1/logs_raw"
  ( cd "$d" && LOGDIR="$W/c/$1/logs_raw" bash ./zz_raw_gate.sh 2>/dev/null | grep '^RAW' ) > "$OUT/$1.$2.raw"
  rm -f "$d/zz_raw_gate.sh"
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

# =========================== follow-up cases (run 3) ===========================
begin clone "fresh-clone simulation"; gate clone gate
row clone "$( [ "$LAST_NF" -eq 0 ] && echo GREEN || echo "red$LAST_NF" )" "$(python3 "$EDITS" --desc clone)"
for c in n11 n8b; do
  begin "$c" "new, edit + --write"; gate "$c" before; b=$LAST_NF
  drv "$c" write --write; w=$LAST_RC
  gate "$c" after; a=$LAST_NF
  row "$c" "$( [ "$a" -eq 0 ] && echo PASS || echo "red$a" )" "before=$b FAIL, --write rc=$w, after=$a FAIL -- $(python3 "$EDITS" --desc "$c")"
done
echo "MEASURE_F2C_DONE $(date '+%F %T')" >> "$S"
echo "MEASURE_F2C_DONE" >> "$T"
echo MEASURE_F2C_DONE
