#!/bin/bash
for f in /tmp/gxopus501p4_*.out; do
  printf "%-46s rows=%s  last=%s\n" "$f" "$(grep -cE ' (ok|FAIL)$' "$f")" "$(grep -E ' (ok|FAIL)$' "$f" | tail -1 | cut -c1-20)"
done
ls -la /tmp/gxopus501p4/.MUTANT 2>/dev/null || echo "no sentinel"
