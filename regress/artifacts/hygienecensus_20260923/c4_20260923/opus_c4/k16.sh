#!/bin/bash
# K16 (reasoned, not measured, in the brief): when the token classifier yields NOTHING, does the census fail closed?
# The brief's claim: the gate reds (43 and 3 pinned) and the deriver refuses (every grandfathered name is GONE; the
# whole-buffer pins would need a ruling).  Measured here on /tmp copies under WSL, four failure shapes:
#   k_missing   census_tokens.py deleted from the copy
#   k_py3fail   `python3` shimmed to exit 1, `python` shimmed to the real interpreter (= git-bash's layout: the Store
#               stub is python3, a working python is python; the deriver picks `python` for its own writer)
#   k_py3empty  `python3` shimmed to exit 0 and print nothing
#   k_partial   census_tokens.py prints its first 10 names and then raises
# For each: the gate's readiness FAIL rows; the deriver report's promptless/GONE lines; --write; --release <name>.
set -u
P=/mnt/c
SEC=$P/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
FROZ=$P/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/c4_frozen
OUT=$P/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/opus_c4/k16
rm -rf "$OUT"; mkdir -p "$OUT"; S=$OUT/SUMMARY.txt; : > "$S"
REALPY=$(command -v python3)
mk() {
  local W=/tmp/gxc4_k16_$1; rm -rf "$W"; mkdir -p "$W/GXEMUL-SEC/regress" "$W/GXEMUL-SEC/tools" "$W/logs" "$W/shim"
  (cd "$SEC/regress" && find . -maxdepth 1 -type f -exec cp -p {} "$W/GXEMUL-SEC/regress/" \;)
  cp -p "$FROZ/gate_hygiene.sh" "$FROZ/census_tokens.py" "$W/GXEMUL-SEC/regress/"
  cp -p "$FROZ/derive_hygiene_pins.sh" "$W/GXEMUL-SEC/tools/"
  printf '#!/bin/sh\nexec %s "$@"\n' "$REALPY" > "$W/shim/python"; chmod +x "$W/shim/python"
  echo "$W"; }
listn() { python3 -c '
import io,sys; s=io.open(sys.argv[1],encoding="utf-8").read()
i=s.index("GRANDFATHERED_PROMPTLESS=\"")+len("GRANDFATHERED_PROMPTLESS=\""); j=s.index("\"",i); print(len(s[i:j].split()))' "$1"; }
one() {  # one <tag> <W> [PATH-prefix]
  local tag=$1 W=$2 pre=${3:-} g
  g=$W/GXEMUL-SEC/regress/gate_hygiene.sh
  local PATHX=$PATH; [ -n "$pre" ] && PATHX="$pre:$PATH"
  { echo "== $tag"
    echo "   gate readiness FAIL rows:"
    ( cd "$W/GXEMUL-SEC/regress" && PATH="$PATHX" LOGDIR="$W/logs" bash ./gate_hygiene.sh ) 2>&1 | sed 's/\x1b\[[0-9;]*m//g' \
        | grep -E '^\s*FAIL.*(readiness|whole-buffer)' | sed 's/^\s*/      /'
    echo "   deriver report (key lines):"
    ( PATH="$PATHX" GXROOT="$W" bash "$W/GXEMUL-SEC/tools/derive_hygiene_pins.sh" ) > "$OUT/$tag.report" 2>&1; echo "      rc=$?"
    grep -E '^(promptless vs|EXPECT_WHOLE_FULL|GRANDFATHERED BUT|DERIVE_FAIL|NEW PROMPTLESS)' "$OUT/$tag.report" | sed 's/^/      /'
    echo "      GONE names listed by the report: $(awk '/^GRANDFATHERED BUT NO LONGER PROMPTLESS/{f=1;next} /^[A-Z]/{f=0} f' "$OUT/$tag.report" | grep -c .)"
    echo "   deriver --write:"
    ( PATH="$PATHX" GXROOT="$W" bash "$W/GXEMUL-SEC/tools/derive_hygiene_pins.sh" --write ) > "$OUT/$tag.write" 2>&1; echo "      rc=$?  $(grep -m1 -E '^(REFUSED|WRITTEN|DERIVE_FAIL)' "$OUT/$tag.write" | cut -c1-110)"
    echo "   deriver --release gdrom_cond_probe.py (a probe that IS still promptless):"
    local before; before=$(listn "$g")
    ( PATH="$PATHX" GXROOT="$W" bash "$W/GXEMUL-SEC/tools/derive_hygiene_pins.sh" --release gdrom_cond_probe.py ) > "$OUT/$tag.release" 2>&1
    echo "      rc=$?  $(grep -m1 -E '^(REFUSED|RELEASED|DERIVE_FAIL)' "$OUT/$tag.release" | cut -c1-110)   list $before -> $(listn "$g") names"
    echo "   gate AFTER that release, with a WORKING classifier (real python3):"
    ( cd "$W/GXEMUL-SEC/regress" && LOGDIR="$W/logs" bash ./gate_hygiene.sh ) 2>&1 | sed 's/\x1b\[[0-9;]*m//g' \
        | grep -E '^\s*FAIL.*(readiness|whole-buffer)' | sed 's/^\s*/      /'
    echo; } >> "$S"
}
W=$(mk missing); rm -f "$W/GXEMUL-SEC/regress/census_tokens.py"; one k_missing "$W"
W=$(mk py3fail); printf '#!/bin/sh\necho "Python was not found (shim)" >&2\nexit 49\n' > "$W/shim/python3"; chmod +x "$W/shim/python3"; one k_py3fail "$W" "$W/shim"
W=$(mk py3empty); printf '#!/bin/sh\nexit 0\n' > "$W/shim/python3"; chmod +x "$W/shim/python3"; one k_py3empty "$W" "$W/shim"
W=$(mk partial)
python3 - "$W/GXEMUL-SEC/regress/census_tokens.py" <<'PY'
import io,sys
p=sys.argv[1]; s=io.open(p,encoding="utf-8").read()
old="    for line in sys.stdin.read().split(\"\\n\"):"
assert s.count(old)==1, s.count(old)
new="    _n = [0]\n    for line in sys.stdin.read().split(\"\\n\"):\n        _n[0] += 1\n        if _n[0] > 10: raise RuntimeError(\"simulated classifier crash\")"
io.open(p,"w",encoding="utf-8").write(s.replace(old,new))
PY
one k_partial "$W"
rm -rf /tmp/gxc4_k16_*
echo "K16_DONE $(date '+%F %T')" >> "$S"
cat "$S"
