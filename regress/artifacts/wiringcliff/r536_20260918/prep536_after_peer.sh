#!/bin/bash
#  Run from git-bash AFTER the peer's receipt commit (HEAD moves; its check_probe_wiring.py gains
#  3 MANIFEST lines).  Regenerates #536's staged blobs from the NEW HEAD, re-verifies everything that
#  was verified against the old one, and emits the pass-2 brief's diff files.  Touches NO tracked file:
#  applying to the working tree is a separate, explicit step at the end (APPLY=1).
set -eu
P=/c/DocumentNoSnc/CC/GXEMUL
SEC=$P/GXEMUL-SEC
T=$P/_scratchpad/t536
O=$P/_scratchpad/p2_536_537
mkdir -p "$O"
cd "$SEC"
echo "HEAD: $(git log --oneline -1)"

#  1. staged blobs = NEW HEAD + #536
git show HEAD:regress/gate_arm.sh > "$T/ga_head.sh"
git show HEAD:tools/pipeline/check_probe_wiring.py > "$T/cpw_head.py"
python "$P/_scratchpad/apply536_gate.py" "$T/ga_head.sh"
python "$P/_scratchpad/apply536_exempt.py" "$T/cpw_head.py"
bash -n "$T/ga_head.sh"; python -m py_compile "$T/cpw_head.py"

#  2. working-tree versions = WT + #536, and they must COMMUTE with whatever else the WT carries
cp -p regress/gate_arm.sh "$T/ga_wt.pre"; cp -p tools/pipeline/check_probe_wiring.py "$T/cpw_wt.pre"
cp "$T/ga_wt.pre" "$T/ga_wt.sh"; cp "$T/cpw_wt.pre" "$T/cpw_wt.py"
python "$P/_scratchpad/apply536_gate.py" "$T/ga_wt.sh"
python "$P/_scratchpad/apply536_exempt.py" "$T/cpw_wt.py"
git diff HEAD -- regress/gate_arm.sh > "$T/pWT_ga.patch"
git diff HEAD -- tools/pipeline/check_probe_wiring.py > "$T/pWT_cpw.patch"
cp "$T/ga_head.sh" "$T/ga_chk"; cp "$T/cpw_head.py" "$T/cpw_chk"
[ -s "$T/pWT_ga.patch" ] && patch -s "$T/ga_chk" < "$T/pWT_ga.patch"
[ -s "$T/pWT_cpw.patch" ] && patch -s "$T/cpw_chk" < "$T/pWT_cpw.patch"
cmp "$T/ga_chk" "$T/ga_wt.sh" || { echo "gate_arm.sh: DOES NOT COMMUTE"; exit 5; }; echo "gate_arm.sh: commutes"
cmp "$T/cpw_chk" "$T/cpw_wt.py" || { echo "check_probe_wiring.py: DOES NOT COMMUTE"; exit 5; }; echo "check_probe_wiring.py: commutes"

#  3. scratch env = NEW HEAD's tracked regress scripts + artifact .py, with the staged blobs
E=$T/env2; rm -rf "$E"; mkdir -p "$E/tools/pipeline"
git archive HEAD -- regress ':(exclude)regress/artifacts' | tar -x -C "$E"
git archive HEAD -- ':(glob)regress/artifacts/**/*.py' | tar -x -C "$E"
cp "$T/ga_head.sh" "$E/regress/gate_arm.sh"
cp "$T/cpw_head.py" "$E/tools/pipeline/check_probe_wiring.py"
git show HEAD:tools/pipeline/check_probe_wiring.py > "$E/tools/pipeline/check_probe_wiring.HEAD.py"
cd "$E"
run() { echo "=== $*"; "$@" > "$T/o.txt" 2>&1; echo "rc=$?"; grep -E 'PROBEWIRING_|^  FAIL' "$T/o.txt" | cut -c1-150; }
set +e
run python tools/pipeline/check_probe_wiring.py --regress regress
run python tools/pipeline/check_probe_wiring.py --regress regress --today 2026-09-26
run python tools/pipeline/check_probe_wiring.py --regress regress --today 2026-09-28
run python tools/pipeline/check_probe_wiring.HEAD.py --regress regress
git -C "$SEC" show HEAD:regress/gate_arm.sh > regress/gate_arm.sh
run python tools/pipeline/check_probe_wiring.py --regress regress
cp "$T/ga_head.sh" regress/gate_arm.sh
python tools/pipeline/check_probe_wiring.py --selftest > "$T/selftest2.txt" 2>&1; echo "selftest rc=$?"
grep -E 'M5a|M5b|SELFTEST' "$T/selftest2.txt"
set -e
cd "$SEC"

#  4. the pass-2 brief's inlined files
git diff HEAD -- regress/diff_fbpending_bound.c regress/gate_offline.sh regress/selfmutants/fbpending_bound.why > "$O/diff_537.txt"
git show HEAD:regress/gate_arm.sh | diff -u --label "a/regress/gate_arm.sh (HEAD)" --label "b/regress/gate_arm.sh (#536 staged)" - "$T/ga_head.sh" > "$O/diff_536_gate_arm.txt" || true
git show HEAD:tools/pipeline/check_probe_wiring.py | diff -u --label "a/tools/pipeline/check_probe_wiring.py (HEAD)" --label "b/tools/pipeline/check_probe_wiring.py (#536 staged)" - "$T/cpw_head.py" > "$O/diff_536_checker.txt" || true
{
  echo "files this pass reviews (added/removed lines vs HEAD)  -- disposition"
  git diff --numstat HEAD -- regress/diff_fbpending_bound.c regress/gate_offline.sh regress/selfmutants/fbpending_bound.why | sed 's/$/   INLINED (2a)/'
  printf '%s\t%s\tregress/gate_arm.sh   INLINED (2b)\n' "$(grep -c '^+[^+]' "$O/diff_536_gate_arm.txt")" "$(grep -c '^-[^-]' "$O/diff_536_gate_arm.txt")"
  printf '%s\t%s\ttools/pipeline/check_probe_wiring.py   INLINED (2c)\n' "$(grep -c '^+[^+]' "$O/diff_536_checker.txt")" "$(grep -c '^-[^-]' "$O/diff_536_checker.txt")"
  echo "NOT SHOWN: the round's records (CHANGELOG block, ledger rows), written after this pass; the working tree's"
  echo "uncommitted #529 hunks in gate_arm.sh / check_probe_wiring.py are NOT part of either round and are not staged."
} > "$O/numstat.txt"
wc -l "$O"/*.txt

if [ "${APPLY:-0}" = 1 ]; then
  cmp regress/gate_arm.sh "$T/ga_wt.pre" && cmp tools/pipeline/check_probe_wiring.py "$T/cpw_wt.pre" \
    || { echo "WORKING TREE MOVED since step 2 -- NOT applying"; exit 4; }
  cp "$T/ga_wt.sh" regress/gate_arm.sh
  cp "$T/cpw_wt.py" tools/pipeline/check_probe_wiring.py
  cmp regress/gate_arm.sh "$T/ga_wt.sh" && cmp tools/pipeline/check_probe_wiring.py "$T/cpw_wt.py" && echo "APPLIED #536 to the working tree"
fi
