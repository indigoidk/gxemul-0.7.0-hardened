#!/bin/bash
# Q1 matrix -- which --ruling texts and which --grandfather names does the F4 deriver (23410fe1) accept or refuse?
# Runs under BOTH git-bash and WSL (usage: q1_matrix.sh <label> <workroot>).  One /tmp copy of SEC regress top-level +
# tools + the three F4 frozen files; the gate file is restored from a saved copy before every case, so an accepted
# write never leaks into the next case.  Nothing is written under GXEMUL-SEC.
set -u
LABEL=$1; WR=$2
#  detect by the REAL tree, not by /mnt/c: git-bash has its own /mnt/c (C:\Program Files\Git\mnt\c), which holds a
#  DocumentNoSnc directory but not this project -- a first run of this script picked it and measured nothing.
if [ -f /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/gate_hygiene.sh ]; then P=/c
elif [ -f /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/gate_hygiene.sh ]; then P=/mnt/c
else echo "Q1_MATRIX_FAIL: cannot find the project tree"; exit 9; fi
SEC=$P/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
FROZ=$P/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/c4_frozen
OUT=$P/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/opus_c4/q1_$LABEL
rm -rf "$WR" "$OUT"; mkdir -p "$WR/GXEMUL-SEC/regress" "$WR/GXEMUL-SEC/tools" "$OUT"
T=$OUT/TABLE.txt; : > "$T"
(cd "$SEC/regress" && find . -maxdepth 1 -type f -exec cp -p {} "$WR/GXEMUL-SEC/regress/" \;)
cp -p "$FROZ/gate_hygiene.sh" "$FROZ/census_tokens.py" "$WR/GXEMUL-SEC/regress/"
cp -p "$FROZ/derive_hygiene_pins.sh" "$WR/GXEMUL-SEC/tools/"
R=$WR/GXEMUL-SEC/regress; G=$R/gate_hygiene.sh; D=$WR/GXEMUL-SEC/tools/derive_hygiene_pins.sh
{ echo "Q1 matrix [$LABEL] $(date '+%F %T')  bash $BASH_VERSION  date: $(date --version | head -1)  tz: $(date +%Z)"
  (cd "$WR/GXEMUL-SEC" && md5sum regress/gate_hygiene.sh regress/census_tokens.py tools/derive_hygiene_pins.sh); } > "$OUT/HEADER.txt"

# a 4th whole-buffer site in the ALLOWLISTED arm_bdt (receiver ends in buf): a ruling-gated pin change, no new probe
printf '\n_c4 = lambda mybuf: mybuf.rstrip().endswith("GXemul>")\n' >> "$R/arm_bdt_probe.py"
cp -p "$G" "$WR/gate.orig"
NC() { grep -v '^[[:space:]]*#' "$1"; }   # non-comment lines

# ---------------- RULINGS (--write --ruling X) ----------------
rule() {  # rule <tag> <ruling-bytes> [env TZ]
  local tag=$1 txt=$2 tz=${3:-}
  cp -p "$WR/gate.orig" "$G"
  if [ -n "$tz" ]; then ( TZ=$tz GXROOT="$WR" bash "$D" --write --ruling "$txt" ) > "$OUT/r_$tag.out" 2>&1
  else ( GXROOT="$WR" bash "$D" --write --ruling "$txt" ) > "$OUT/r_$tag.out" 2>&1; fi
  local rc=$? msg added bn newnc
  msg=$(grep -m1 -E '^(REFUSED|WRITTEN|DERIVE_FAIL|usage)' "$OUT/r_$tag.out" | cut -c1-78)
  added=$(( $(grep -c '^#  RULING' "$G") - $(grep -c '^#  RULING' "$WR/gate.orig") ))
  bn=$(bash -n "$G" 2>/dev/null && echo ok || echo FAIL)
  newnc=$(diff <(NC "$WR/gate.orig") <(NC "$G") | grep -c '^>')
  printf 'R %-10s rc=%-2s ruling-lines+%-2s bash-n=%-4s new-noncomment=%-2s %s\n' "$tag" "$rc" "$added" "$bn" "$newnc" "$msg" >> "$T"
}
B() { printf '%b' "$1"; }    # build bytes from octal escapes
OK16="owner ruled to allowlist this site pending conversion"
rule base      "2026-09-23: $OK16"
rule apos      "2026-09-23: the owner's ruling to allowlist this site"
rule dquote    "2026-09-23: the owner said \"allowlist\" this site now"
rule bslash    "$(B '2026-09-23: owner ruled \\\\ allowlist this site now')"
rule dollar    '2026-09-23: owner ruled $HOME allowlist this site now'
rule backtick  '2026-09-23: owner ruled `x` allowlist this site now'
rule newline   "$(B "2026-09-23: $OK16\\nsecond line of text here")"
rule tab       "$(B "2026-09-23: $OK16\\tafter a tab")"
rule cr        "$(B "2026-09-23: $OK16\\rafter a cr")"
rule del       "$(B "2026-09-23: $OK16\\177")"
rule nbsp      "$(B "2026-09-23: owner\\302\\240ruled to allowlist this site")"
rule u0085     "$(B "2026-09-23: $OK16\\302\\205tail")"
rule u2028     "$(B "2026-09-23: $OK16\\342\\200\\250tail")"
rule eacute    "$(B "2026-09-23: d\\303\\251cision du propri\\303\\251taire ok")"
rule dots16    "2026-09-23: ................"
rule alnum16   "2026-09-23: abcdefghijklmnop"
rule alnum15   "2026-09-23: abcdefghijklmno ....."
rule dashed16  "2026-09-23: a-b-c-d-e-f-g-h-i-j-k-l-m-n-o-p"
rule long5000  "2026-09-23: $(printf 'reason%.0s ' $(seq 1 700))"
rule shellchr  "2026-09-23: owner ruled; && || (x) <y> {z} ! % * ? [a] ~ ^ # ok 1234567890"
rule mimicneed "2026-09-23: owner ruled x -- EXPECT_WHOLE_FULL(3->99) (tools/derive_hygiene_pins.sh --write)"
rule nospace   "2026-09-23:$OK16"
rule leadspace " 2026-09-23: $OK16"
rule empty     ""
# dates (valid reason)
for d in 2024-02-29 2025-02-29 2100-02-29 2000-02-29 2026-02-30 2026-99-99 2026-00-10 2026-09-00 \
         0001-01-01 0000-01-01 1582-10-10 1900-01-01 1969-12-31 2038-01-20 9999-12-31 2026-9-23 02026-09-23; do
  rule "d$d" "$d: $OK16"
done
rule "dSaoPaulo" "2018-11-04: $OK16" America/Sao_Paulo
rule "dChicago"  "2018-11-04: $OK16" America/Chicago
# two --ruling flags
cp -p "$WR/gate.orig" "$G"
( GXROOT="$WR" bash "$D" --write --ruling "2026-09-23: $OK16" --ruling "2026-09-23: $OK16" ) > "$OUT/r_two.out" 2>&1
printf 'R %-10s rc=%-2s %s\n' two "$?" "$(grep -m1 -E '^(REFUSED|WRITTEN|usage)' "$OUT/r_two.out" | cut -c1-70)" >> "$T"

# ---------------- NAMES (--grandfather N) ----------------
cp -p "$WR/gate.orig" "$G"
name() {  # name <tag> <name-bytes> [make-file]
  local tag=$1 n=$2 mk=${3:-}
  cp -p "$WR/gate.orig" "$G"
  if [ -n "$mk" ]; then mkdir -p "$(dirname "$R/$n")"; cp -p "$R/pcc2_width_probe.py" "$R/$n"; fi
  ( GXROOT="$WR" bash "$D" --grandfather "$n" ) > "$OUT/n_$tag.out" 2>&1
  local rc=$? msg kind
  msg=$(grep -m1 -E '^(REFUSED|GRANDFATHERED|DERIVE_FAIL|usage)' "$OUT/n_$tag.out" | cut -c1-80)
  case "$msg" in *"ASCII letters, digits"*) kind=ALLOWLIST ;; *"not a NEW promptless"*) kind=ELIGIBILITY ;;
                 GRANDFATHERED*) kind=ACCEPTED ;; *) kind=OTHER ;; esac
  printf 'N %-10s rc=%-2s %-11s %s\n' "$tag" "$rc" "$kind" "$msg" >> "$T"
  [ -n "$mk" ] && rm -f "$R/$n"
}
name ok        "zz-legit_probe.py" mk
name upper     "ZZ_Upper_probe.py" mk
name leaddash  "-zz_dash_probe.py" mk
name subdir    "newsub/zz_sub_probe.py" mk
name long200   "zz_$(printf 'a%.0s' $(seq 1 190))_probe.py" mk
name empty     ""
name space     "zz opus.py"
name dollar    'zz$HOME.py'
name backtick  'zz`x`.py'
name dquote    'zz"q.py'
name squote    "zz'q.py"
name bslash    "$(B 'zz\\\\q.py')"
name star      'zz*.py'
name qmark     'zz?.py'
name brack     'zz[1].py'
i=0; for c in '+' '@' ',' '=' '%' '~' ':' '!' '#' '&' '(' ';' '<' '|' '^' '{'; do
  i=$((i+1)); name "chr$i" "zz${c}x.py"; printf '    ^ chr%s is the name zz%sx.py\n' "$i" "$c" >> "$T"; done
name utf8      "$(B 'zz\303\251.py')"
name nbspname  "$(B 'zz\302\240x.py')"
name tabname   "$(B 'zz\tx.py')"
name nlname    "$(B 'zz\nx.py')"
name dot       "."
name dotdot    ".."
name slash     "/"
name dash      "-"
name ddash     "--"
name dotslash  "./zz-legit_probe.py"
name parent    "../zz-legit_probe.py"
echo "Q1_MATRIX_DONE [$LABEL] $(date '+%F %T')" >> "$T"
cat "$T"
