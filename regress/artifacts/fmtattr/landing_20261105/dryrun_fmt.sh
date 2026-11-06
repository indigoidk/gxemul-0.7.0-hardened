#!/bin/bash
#  dryrun_fmt.sh <head.tar> -- gate 1's fmtattr block, run ALONE over fifteen legs, before the landing window (the pvr kit's
#  dryrun, in the form this block allows: the block is cheap, so each leg RUNS it instead of replaying a banked log).
#  Writes only a WSL /tmp scratch clone (clone-local .MUTANT sentinel, removed with the clone) and DRYRUN_fmt.out beside this
#  script.  The two HEAD legs READ /tmp/gxsec-build and build/ (both hold HEAD's sources) and write nothing there.
#  The predicted red set per leg is PRETABLE_fmt.out, written before this ran; dryrun_fmt.py compares the two.
#  RUN (via dryrun_fmt.py, which makes the tar):  MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash \
#       /mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/wfmt/landing/dryrun_fmt.sh /mnt/c/.../dry/head.tar      (never under timeout)
set -u
R=/mnt/c/DocumentNoSnc/cc/GXEMUL
L=$R/_scratchpad/wfmt/landing
SEC=$R/GXEMUL-SEC
MUT=$R/_scratchpad/codescan/fmtfix/bb_mutants
TAR=${1:?usage: dryrun_fmt.sh <head.tar>}
D=/tmp/gxfmt_dry_$$
OUT=$L/DRYRUN_fmt.out
: > "$OUT"
log() { echo "$(date -u +%FT%TZ) $*" | tee -a "$OUT"; }
die() { log "ABORT: $*"; echo "DRYRUN_FMT_DONE aborted" | tee -a "$OUT"; rm -rf "$D"; exit 2; }
( cd "$L/staged" && md5sum -c --quiet MD5SUMS ) >> "$OUT" 2>&1 || die "staged/ does not match staged/MD5SUMS -- re-run build_staged_fmt.py"
log "dryrun_fmt.sh: gate 1's fmtattr block alone; kit HEAD $(sed -n 's/^HEAD //p' "$L/staged/HEAD.txt"), round #$(sed -n 's/^ROUND //p' "$L/staged/HEAD.txt"); tar $TAR md5 $(md5sum < "$TAR" | cut -c1-12)"
mkdir -p "$D/tree" "$D/regress" "$D/legs" || die "mkdir"
tar -xf "$TAR" -C "$D/tree" || die "tar"
echo "dryrun_fmt.sh scratch clone: the fmtattr gate block's legs; removed with the clone" > "$D/tree/.MUTANT"
cp "$D/tree/src/disk/bootblock.c" "$D/bootblock.HEAD.c"
n=0; bad=0
while read -r sm rel; do
  case "$rel" in src/*) cp "$L/staged/$rel" "$D/tree/$rel" && n=$((n+1)); cmp -s "$L/staged/$rel" "$D/tree/$rel" || bad=$((bad+1)) ;; esac
done < "$L/staged/MD5SUMS"
log "baseline: the archive + $n staged src files overlaid ($bad failed cmp); overlay md5 $(grep '  src/' "$L/staged/MD5SUMS" | md5sum | cut -c1-12) (of staged/MD5SUMS's src lines)"
[ "$n" = 47 ] && [ "$bad" = 0 ] || die "the overlay is not the 47 staged files"
( cd "$D/tree" && ./configure > "$D/configure.log" 2>&1 && make -j4 > "$D/make_base.log" 2>&1 ); rc=$?
w=$(grep -c 'warning:' "$D/make_base.log"); e=$(grep -c ': error:' "$D/make_base.log")
[ -x "$D/tree/gxemul" ] && bin=yes || bin=no
fresh=yes; for f in $(cd "$L/staged" && find src -type f); do [ "$D/tree/gxemul" -nt "$D/tree/$f" ] || fresh=NO; done
log "base build: make rc=$rc, warnings $w, errors $e, binary $bin, binary newer than all 47 sources: $fresh"
[ "$rc" = 0 ] && [ "$w" = 0 ] && [ "$e" = 0 ] && [ "$bin" = yes ] && [ "$fresh" = yes ] || die "the baseline did not build clean"
cp "$D/make_base.log" "$L/dry/make_base.log" 2>/dev/null

#  the block, extracted by its header and end marker from the STAGED gate_build.sh, beside HEAD's lib.sh and the staged probe
num=$(sed -n 's/^ROUND //p' "$L/staged/HEAD.txt")
awk -v h="#  ------------------------------------------------------------ fmtattr (#$num)" \
    -v e="#  ------------------------------------------------------------ end fmtattr (#$num)" \
    '$0==h{f=1} f{print} $0==e{exit}' "$L/staged/regress/gate_build.sh" > "$D/regress/fmt_block.sh"
log "the staged block: $(wc -l < "$D/regress/fmt_block.sh") lines, md5 $(md5sum < "$D/regress/fmt_block.sh" | cut -c1-12), last '$(tail -n 1 "$D/regress/fmt_block.sh")'"
[ "$(tail -n 1 "$D/regress/fmt_block.sh")" = "#  ------------------------------------------------------------ end fmtattr (#$num)" ] || die "the block did not extract"
cp "$L/dry/lib.sh" "$L/staged/regress/fmt_bootblock_probe.py" "$D/regress/"
log "lib.sh: HEAD's blob (dry/lib.sh, md5 $(md5sum < "$L/dry/lib.sh" | cut -c1-12), written by dryrun_fmt.py)"
cat > "$D/regress/run_block.sh" <<'RUNEOF'
set -u
cd "$(dirname "$0")"
LOGDIR=$1
. ./lib.sh
HERE=$(pwd)
ARC_TREE=$2
gate_begin "fmtattr block (dry run)"
. ./fmt_block.sh
echo "DRY_BLOCK_DONE checks=$_checks fails=$_fails"
RUNEOF
for s in s1 s2; do mkdir -p "$D/regress_$s"; cp "$D/regress/lib.sh" "$D/regress/fmt_block.sh" "$D/regress/run_block.sh" "$D/regress_$s/"; done
cat > "$D/regress_s1/fmt_bootblock_probe.py" <<'S1EOF'
print("fmt_bootblock_probe label=stand-in S1: a fourth row")
for r in ("session ended", "voldir parsed", "loading offset", "a fourth row"):
    print("%-16s %-20s want %-20s ok" % (r, "x", "x"))
print("FMTBB_RESULT=4/4")
print("FMTBB_CONTROL=OK")
print("FMTBB_DONE")
S1EOF
cat > "$D/regress_s2/fmt_bootblock_probe.py" <<'S2EOF'
print("fmt_bootblock_probe label=stand-in S2: no sentinel")
for r in ("session ended", "voldir parsed", "loading offset"):
    print("%-16s %-20s want %-20s ok" % (r, "x", "x"))
print("FMTBB_RESULT=3/3")
print("FMTBB_CONTROL=OK")
print("a line where FMTBB_DONE belongs")
S2EOF

leg() {   # name  arc_tree  [regress dir]  -- one run of the block; its red check labels on one line
  local nm=$1 at=$2 rd=${3:-$D/regress}
  rm -rf "$D/log_$nm"; mkdir -p "$D/log_$nm"
  bash "$rd/run_block.sh" "$D/log_$nm" "$at" > "$D/leg_$nm.out" 2>&1
  local dn red
  dn=$(grep '^DRY_BLOCK_DONE ' "$D/leg_$nm.out" | tail -1)
  red=$(sed -n 's/^  FAIL \(.*\) got=.*$/\1/p' "$D/leg_$nm.out" | sed 's/ *$//' | paste -sd'|' -)
  echo "--- $nm :: ${dn:-NO DONE LINE} :: red: ${red:-none}" | tee -a "$OUT"
  sed 's/^/    /' "$D/leg_$nm.out" >> "$OUT"
  grep -E '^(loading offset|FMTBB_)' "$D/log_$nm/fmt_bootblock.log" 2>/dev/null | cut -c1-170 | sed 's/^/    probe> /' >> "$OUT"
  grep -E 'warning:|error:' "$D/log_$nm/fmtctl.log" 2>/dev/null | cut -c1-150 | sed 's/^/    ctl> /' >> "$OUT"
}
altree() {  # name  -- a stand-in tree: the base's include, Makefile and config.h, a binary named by the caller
  local a=$D/legs/$1
  rm -rf "$a"; mkdir -p "$a/src"
  cp -r "$D/tree/src/include" "$a/src/include"; cp "$D/tree/src/Makefile" "$a/src/Makefile"; cp "$D/tree/config.h" "$a/config.h"
  echo "$a"
}
sub() {   # file old new -- an exact, single replacement, or the leg aborts
  python3 -c 'import sys
p, o, n = sys.argv[1:4]
s = open(p, encoding="latin-1").read()
assert s.count(o) == 1, (o, s.count(o))
open(p, "w", encoding="latin-1").write(s.replace(o, n))' "$1" "$2" "$3"
}

log "legs (the predicted red sets are PRETABLE_fmt.out's):"
leg base "$D/tree"
leg head_wsl /tmp/gxsec-build
leg head_pmax "$R/build"
a=$(altree A1_nofatal); ln -s "$D/tree/gxemul" "$a/gxemul"
sub "$a/src/include/misc.h" 'void fatal(const char *fmt, ...) GX_PRINTF(1, 2);' 'void fatal(const char *fmt, ...);' || die "A1 mutation"
leg A1_nofatal "$a"
a=$(altree A2_empty); ln -s "$D/tree/gxemul" "$a/gxemul"
sub "$a/src/include/misc.h" '__attribute__((format(printf, f, a)))' '' || die "A2 mutation"
leg A2_empty "$a"
a=$(altree A3_noargs); ln -s "$D/tree/gxemul" "$a/gxemul"
sub "$a/src/include/misc.h" 'GX_PRINTF(4, 5);' 'GX_PRINTF(4, 0);' || die "A3 mutation"
leg A3_noargs "$a"
a=$(altree N1_true); ln -s /bin/true "$a/gxemul"; leg N1_true "$a"
a=$(altree N2_absent); leg N2_absent "$a"
a=$(altree N3_false); ln -s /bin/false "$a/gxemul"; leg N3_false "$a"
leg S1_extrarow "$D/tree" "$D/regress_s1"
leg S2_nodone "$D/tree" "$D/regress_s2"
a=$(altree S3_noheader); ln -s "$D/tree/gxemul" "$a/gxemul"; rm -f "$a/src/include/misc.h"; leg S3_noheader "$a"

#  the product legs: bootblock.c replaced in the clone, its object rebuilt, then restored and cmp-verified
BB=src/disk/bootblock.c
for m in M1_radix M2_narrow M0_revert; do
  case $m in M0_revert) src=$D/bootblock.HEAD.c ;; *) src=$MUT/$m.c ;; esac
  cp "$src" "$D/tree/$BB" && rm -f "$D/tree/src/disk/bootblock.o"
  ( cd "$D/tree" && make -j4 > "$D/make_$m.log" 2>&1 ); rc=$?
  [ "$D/tree/gxemul" -nt "$D/tree/$BB" ] && fresh=yes || fresh=NO
  log "$m: source md5 $(md5sum < "$src" | cut -c1-12); build rc=$rc, warnings $(grep -c 'warning:' "$D/make_$m.log"), binary newer than the mutant source: $fresh"
  grep 'warning:' "$D/make_$m.log" | sed 's/^/    build> /' | cut -c1-170 >> "$OUT"
  leg "$m" "$D/tree"
  cp "$L/staged/$BB" "$D/tree/$BB" && cmp -s "$L/staged/$BB" "$D/tree/$BB" && log "   restored $BB (cmp clean)" || die "restore of $BB"
  rm -f "$D/tree/src/disk/bootblock.o"; ( cd "$D/tree" && make -j4 > "$D/make_restore_$m.log" 2>&1 )
  [ "$D/tree/gxemul" -nt "$D/tree/$BB" ] || die "the restored build is not fresh"
done
leg base_restored "$D/tree"
rm -f "$D/tree/.MUTANT"; cd / && rm -rf "$D"; [ -d "$D" ] && log "CLONE NOT REMOVED: $D" || log "clone removed"
echo "DRYRUN_FMT_DONE" | tee -a "$OUT"
