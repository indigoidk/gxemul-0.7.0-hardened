#!/bin/bash
#  run_header_redate.sh <repo> -- the measured hazard behind section P2's "a block already in the file cannot fail
#  UNLESS its header line is edited": `git blame --contents` gives an EDITED old header line the all-zero sha, which the
#  checker dates TODAY, so the block becomes newly ENFORCED (never newly exempt).  Read-only: git show and git blame of
#  HEAD's CHANGELOG.md, plus a temporary copy outside the repo.
REPO=$1
cd "$REPO" || exit 9
export GIT_OPTIONAL_LOCKS=0
H=$(git rev-parse --short=8 HEAD)
ln=$(git show HEAD:CHANGELOG.md | grep -n '^# `#557`' | head -1 | cut -d: -f1)
[ -n "$ln" ] || { echo "no #557 header in HEAD's CHANGELOG.md"; exit 9; }
tmp=$(mktemp)
git show HEAD:CHANGELOG.md > "$tmp"
s0=$(git blame --porcelain -L "$ln,$ln" --contents "$tmp" -- CHANGELOG.md | head -1 | cut -d' ' -f1)
sed -i "${ln}s/\$/ /" "$tmp"
s1=$(git blame --porcelain -L "$ln,$ln" --contents "$tmp" -- CHANGELOG.md | head -1 | cut -d' ' -f1)
rm -f "$tmp"
echo "HEAD $H; #557's header is CHANGELOG.md line $ln: $(git show HEAD:CHANGELOG.md | sed -n "${ln}p" | cut -c1-90)"
echo "  the header unmodified:          blame sha $s0 ($(git log -1 --format='%h %cd' --date=short "$s0" 2>/dev/null))"
echo "  one space appended to it:       blame sha $s1"
if [ -n "$s0" ] && [ "${s0//0/}" != "" ] && [ -n "$s1" ] && [ "${s1//0/}" = "" ]; then
	echo "  => an edit to an archived block's header line re-dates the block to the editing commit (the checker reads"
	echo "     the all-zero sha as TODAY), so the block is enforced from then on"
else
	echo "  => NOT REPRODUCED"
fi
echo "HEADER_REDATE_DONE"
