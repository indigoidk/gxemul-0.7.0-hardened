#  #518 commit driver.  Usage: bash commit518.sh "<table summary sentence for the ledger>"
#  Preconditions: scratchpad/changelog_518.md has its OWED sections replaced with the measured text;
#  scratchpad/commit_518.txt exists.  Everything else is mechanical and asserted.
set -e
cd /c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
SP=/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad
PY=/c/Users/User00/AppData/Local/Programs/Python/Python312/python.exe
SUMMARY="${1:?table summary required}"
grep -q 'OWED' $SP/changelog_518.md && { echo "*** changelog_518.md still carries OWED markers -- fill them first"; exit 1; }
[ -f $SP/commit_518.txt ] || { echo "*** commit_518.txt missing"; exit 1; }
cp tools/pipeline/ledger.json $SP/ledger.bak_518.json
cp OUTSTANDING_BUGS.md $SP/OUTSTANDING_BUGS.bak_518.md
cp CHANGELOG.md $SP/CHANGELOG.bak_518.md
cp tools/pipeline/check_probe_wiring.py $SP/check_probe_wiring.bak_518.py
echo "=== ledger ==="
$PY $SP/ledger_labels.py 1ce8296
$PY $SP/ledger_518.py PENDING "$SUMMARY"
$PY $SP/ledger_mlf.py
$PY $SP/ledger_sgirc.py
$PY $SP/ledger_lcafollowups.py
$PY $SP/ledger_codex3.py
$PY $SP/ledger_isalane_witness.py
echo "=== bugs ==="
cat $SP/bugs_lcaiocstat0.md >> OUTSTANDING_BUGS.md
cat $SP/bugs_sgimtetlbdefault.md >> OUTSTANDING_BUGS.md
echo "entries: $(grep -c '^### `' OUTSTANDING_BUGS.md)"
echo "=== manifest ==="
$PY $SP/manifest_518.py
echo "=== CHANGELOG ==="
cat $SP/changelog_518.md > CHANGELOG.md.new
echo >> CHANGELOG.md.new
cat $SP/changelog_518_pass2.md >> CHANGELOG.md.new
echo >> CHANGELOG.md.new
cat $SP/CHANGELOG.bak_518.md >> CHANGELOG.md.new
mv CHANGELOG.md.new CHANGELOG.md
echo "head: $(head -1 CHANGELOG.md | cut -c1-80)"
echo "=== matrix ==="
python tools/pipeline/gen_dashboard.py --out tools/pipeline/matrix.html > $SP/gen_dashboard_518.out 2>&1
tail -1 $SP/gen_dashboard_518.out | cut -c1-100
echo "=== checkers ==="
python tools/pipeline/check_bugfile_sync.py 2>&1 | tail -1
python tools/pipeline/check_witness.py 2>&1 | tail -1
python tools/pipeline/check_probe_wiring.py 2>&1 | tail -1 | tee $SP/wiring_518.out
grep -q PROBEWIRING_PASS $SP/wiring_518.out
python tools/pipeline/check_stage_panels.py 2>&1 | tail -2
echo "=== stage ==="
git add src/devices/dev_lca.c regress/lca_badval_probe.py regress/lca_isalane_probe.py CHANGELOG.md OUTSTANDING_BUGS.md \
        tools/pipeline/ledger.json tools/pipeline/matrix.html tools/pipeline/check_probe_wiring.py \
        regress/artifacts/lcabadval regress/artifacts/lcaiocstat0 regress/artifacts/lcaisalane \
        regress/artifacts/multilabelfloor regress/artifacts/sgirandomcolour/panel_design_20260908 \
        regress/artifacts/lcairqedgepin regress/artifacts/wiringcliff/brief_fbpending_20260910.md \
        regress/artifacts/wiringcliff/codex_fbpending_20260910.txt regress/artifacts/wiringcliff/codex_fbpending_20260910.err
for b in $(git diff --cached --name-only | grep -E '[.]bin$' || true); do git reset -q -- "$b"; echo "unstaged binary stub: $b"; done
echo "index: $(git diff --cached --name-only | wc -l) files"
git diff --cached --name-only | grep -vE '^regress/artifacts/'
FORB=$(git diff --cached --name-only | grep -cE 'sgi_de_primop|gdromdefault_461|[.]bin$|_scratchpad' || true)
echo "forbidden staged: $FORB"
[ "$FORB" = "0" ]
echo "=== committing $(date) ==="
set +e
git commit -F $SP/commit_518.txt 2>&1 | grep -vE '^ (create|delete) mode' | tail -6
echo "--- HEAD now: $(git log --oneline -1 | cut -c1-100)"
echo "COMMIT518_DONE $(date)"
