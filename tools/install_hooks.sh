#!/bin/bash
#  Install precommit_check.sh as a REAL git pre-commit hook.
#
#  *** WHY THIS EXISTS: THE CHECKER WAS ONLY EVER ADVISORY, AND I COMMITTED THROUGH A RED ONE
#  TWICE IN A SINGLE DAY, BY TWO DIFFERENT MECHANISMS. ***
#
#    1.  `precommit_check.sh | tail -3 && git commit ...`
#        A pipeline's exit status is the LAST command's, so `tail` succeeding masked the
#        checker failing.
#    2.  `precommit_check.sh 2>&1 | grep -E "FAIL|PRECOMMIT_" && git commit ...`
#        Worse, and it looked safer: grep SUCCEEDS when it FINDS failures, so the `&&` fired
#        precisely because the gate was red.
#
#  Both were caught after the fact, by the next run.  A check a human has to remember to
#  respect is a check that eventually does not happen -- the same sentence this project already
#  wrote about the nightly battery before building its dead-man switch.  The general lesson is
#  that `tools/README.md` records which failure each gate was built after; this one was built
#  after the gate itself being bypassed.
#
#  Git hooks live in .git/hooks, which is NOT tracked, so the hook cannot simply be committed.
#  This installer is the tracked half; run it once per clone.
#
#  Usage:   bash tools/install_hooks.sh          install (refuses to clobber a different hook)
#           bash tools/install_hooks.sh --force  overwrite whatever is there
#           git commit --no-verify               the documented escape hatch, deliberately loud
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/.." && pwd)
HOOK="$ROOT/.git/hooks/pre-commit"

if [ ! -d "$ROOT/.git" ]; then
    echo "install_hooks: $ROOT is not a git working tree" >&2
    exit 1
fi
mkdir -p "$ROOT/.git/hooks"

if [ -e "$HOOK" ] && ! grep -q "precommit_check.sh" "$HOOK" 2>/dev/null; then
    if [ "${1:-}" != "--force" ]; then
        echo "install_hooks: $HOOK exists and is NOT ours -- refusing to clobber." >&2
        echo "               re-run with --force if you mean to replace it." >&2
        exit 1
    fi
fi

cat > "$HOOK" <<'HOOKEOF'
#!/bin/bash
#  Installed by tools/install_hooks.sh -- do not edit here; edit the installer.
#  Runs the full precommit gate and BLOCKS the commit if it is red.
ROOT=$(git rev-parse --show-toplevel)
OUT=$(mktemp)
bash "$ROOT/tools/precommit_check.sh" > "$OUT" 2>&1
rc=$?
if [ $rc -ne 0 ]; then
    echo "" >&2
    echo "=========================================================" >&2
    echo "  COMMIT BLOCKED -- precommit_check.sh is RED." >&2
    echo "=========================================================" >&2
    grep -E '^  FAIL|^  WARN|PRECOMMIT_' "$OUT" >&2
    echo "" >&2
    echo "  full output: $OUT" >&2
    echo "  to bypass deliberately:  git commit --no-verify" >&2
    exit 1
fi
grep -E 'PRECOMMIT_' "$OUT"
rm -f "$OUT"
exit 0
HOOKEOF
chmod +x "$HOOK"

echo "installed: $HOOK"
echo
echo "NEGATIVE CONTROL -- prove it can BLOCK, not just that it exists."
echo "A hook nobody has seen refuse a commit is a hook nobody knows works:"
echo
echo "    printf 'x' >> CHANGELOG.md      # or any change that reddens a gate"
echo "    git add -A && git commit -m x   # must print COMMIT BLOCKED and fail"
echo
echo "Run it once. This project has shipped more than one control that had never"
echo "been observed to fail."
