#!/bin/bash
#  inline_diff.sh <sha> [-- <path>...]
#
#  Emit a commit's DIFF for inlining into a panel brief, and REFUSE (exit 2) if it
#  would be empty.  Prints only the diff; nothing decorative goes to stdout.
#
#  *** WHY THIS EXISTS.  `git show <sha> -- <file> | head -N' inlines the COMMIT
#  MESSAGE, not the diff: git show prints the full message first, so a 50-line
#  message and head -60 yields ZERO diff lines.  Measured 2026-08-31 --
#  `git show 938b328 -- src/devices/dev_sgi_re.c | head -60' gives 0 hunks while
#  the whole diff has 20.  An earlier brief the same session got 34 hunks from the
#  identical command with `sed -n 1,200p', which cleared the message.  Same
#  command, different cut, opposite outcome, which is why it read as intermittent
#  rather than as a bug.  THREE PANELS WERE BLINDED BY IT IN ONE SESSION. ***
#
#  *** AND THE SECOND HALF IS WHY THIS REFUSES RATHER THAN WARNS.  The brief that
#  blinded the third panel PRINTED `diff hunks inlined: 0' in its own output,
#  immediately above the line that launched six seats, and it was read past.  A
#  count printed beside an action is not a check unless something declines to
#  proceed on it. ***
set -u
if [ $# -lt 1 ]; then
    echo "usage: inline_diff.sh <sha> [-- <path>...]" >&2
    exit 64
fi
SHA="$1"; shift
git rev-parse --verify --quiet "${SHA}^{commit}" >/dev/null || {
    echo "inline_diff: '$SHA' is not a commit in this repo" >&2; exit 3; }

#  --format= suppresses the message entirely.  No line-count cut anywhere: the cut
#  would have to exceed a message length the caller does not control.
OUT=$(git show --format= "$SHA" "$@")
HUNKS=$(printf '%s' "$OUT" | grep -c '^[+-][^+-]')

if [ "$HUNKS" -eq 0 ]; then
    echo "inline_diff: REFUSING -- 0 diff hunks for $SHA ${*:-(all paths)}" >&2
    echo "inline_diff: a brief that inlines nothing blinds every packet-fed seat." >&2
    echo "inline_diff: check the sha and the pathspec; --format= is already applied." >&2
    exit 2
fi
printf '%s\n' "$OUT"
exit 0
