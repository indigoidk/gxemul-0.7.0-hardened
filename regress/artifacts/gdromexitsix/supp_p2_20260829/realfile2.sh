#!/bin/bash
#  R1 came back REFUSED while the standalone S1 COMPILED.  Neither check is
#  broken -- they are DIFFERENT EDITS, and the first transcription conflated
#  them.  An explicit initialiser RENUMBERS EVERY LATER ENUMERATOR, so where the
#  aliased enumerator SITS decides whether NBITS lands back on the OR's width.
#
#    in-place  FMT_B = OVERREAD_B  ->  CMD_B=4, NBITS=5, OR=0x7f vs 0x1f  REFUSED
#    moved     FMT_B next to OVERREAD ->  CMD_B=7, NBITS=8, OR=0xff vs 0xff ESCAPE
#    in-place  CMD_B = FMT_B (LAST enumerator, nothing after it to renumber)
#                                  ->  NBITS=8, OR=0xff vs 0xff            ESCAPE
#
#  So the escape needs the alias to lose exactly as many trailing positions as
#  bits.  The LAST enumerator does that with a ONE-TOKEN in-place edit.
set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
BLD=/mnt/c/DocumentNoSnc/CC/GXEMUL/build
T=/tmp/gdromreal2
rm -rf "$T"; mkdir -p "$T"
INC="-I $BLD -I $SEC/src/include -I $SEC/src/include/thirdparty"

mk () {  # $1 outfile, $2 shape, $3 candidate(yes|no)
  cp "$SEC/src/devices/dev_dreamcast_gdrom.c" "$1"
  python3 - "$1" "$2" "$3" <<'PYEOF'
import io, sys
p, shape, cand = sys.argv[1], sys.argv[2], sys.argv[3]
L = io.open(p, encoding="utf-8").read().split(chr(10))

def find(tok):
    h = [i for i, s in enumerate(L) if s.strip().startswith(tok)]
    assert len(h) == 1, "want one %s, got %d" % (tok, len(h))
    return h[0]

if shape == "cmd_inplace":          # ONE TOKEN, last enumerator
    i = find("GDROM_W_CMD_B,")
    L[i] = L[i].replace("GDROM_W_CMD_B,", "GDROM_W_CMD_B = GDROM_W_FMT_B,")
elif shape == "fmt_moved":          # deliberate share, enumerator relocated
    i = find("GDROM_W_FMT_B,")
    line = L[i].replace("GDROM_W_FMT_B,", "GDROM_W_FMT_B = GDROM_W_OVERREAD_B,")
    del L[i]
    j = find("GDROM_W_OVERREAD_B,")
    L[j+1:j+1] = [line]
elif shape == "fmt_inplace":        # the shape R1 actually tested
    i = find("GDROM_W_FMT_B,")
    L[i] = L[i].replace("GDROM_W_FMT_B,", "GDROM_W_FMT_B = GDROM_W_OVERREAD_B,")
elif shape == "none":
    pass
else:
    raise SystemExit("unknown shape " + shape)

if cand == "yes":
    i = find("typedef char gdrom_w_masks_disjoint[") + 4
    L[i:i] = [
      "typedef char gdrom_w_masks_pairwise[",
      "    ((GDROM_W_LEN + GDROM_W_NODATA + GDROM_W_NOTWAIT + GDROM_W_OVERREAD +",
      "      GDROM_W_DMANODATA + GDROM_W_DMAARM + GDROM_W_TOCLEN + GDROM_W_FMT +",
      "      GDROM_W_CMD) ==",
      "     (GDROM_W_LEN | GDROM_W_NODATA | GDROM_W_NOTWAIT | GDROM_W_OVERREAD |",
      "      GDROM_W_DMANODATA | GDROM_W_DMAARM | GDROM_W_TOCLEN | GDROM_W_FMT |",
      "      GDROM_W_CMD)) ? 1 : -1];",
    ]
io.open(p, "w", encoding="utf-8", newline=chr(10)).write(chr(10).join(L))
PYEOF
}

run () {  # $1 label, $2 want, $3 shape, $4 cand
  mk "$T/f.c" "$3" "$4"
  if gcc -O2 -std=gnu99 -c "$T/f.c" -o "$T/f.o" $INC 2>"$T/err"; then
    got=COMPILES; extra=""
  else
    got=REFUSED; extra="$(grep -m1 -o "array '[a-z_]*' is negative" "$T/err")"
  fi
  if [ "$got" = "$2" ]; then mark=ok; else mark="*** ESCAPE ***"; fi
  printf '  %-50s want=%-9s got=%-9s %-14s %s\n' "$1" "$2" "$got" "$mark" "$extra"
}

echo "=== REAL FILE, SHIPPED ASSERT ONLY -- which enum-side aliases escape? ==="
run "P0. unmodified"                                COMPILES none        no
run "P1. CMD_B = FMT_B, in place (ONE TOKEN)"       REFUSED  cmd_inplace no
run "P2. FMT_B = OVERREAD_B, enumerator MOVED"      REFUSED  fmt_moved   no
run "P3. FMT_B = OVERREAD_B, in place (=R1)"        REFUSED  fmt_inplace no
echo
echo "=== SAME FOUR, WITH THE CANDIDATE sum==or ADDED ==="
run "Q0. unmodified + candidate"                    COMPILES none        yes
run "Q1. CMD_B = FMT_B, in place + candidate"       REFUSED  cmd_inplace yes
run "Q2. FMT_B = OVERREAD_B, moved + candidate"     REFUSED  fmt_moved   yes
run "Q3. FMT_B = OVERREAD_B, in place + candidate"  REFUSED  fmt_inplace yes
echo
echo "=== confirm P1/P2 really are live aliases, not just compiling noise ==="
for s in cmd_inplace fmt_moved; do
  mk "$T/g.c" "$s" no
  sed -n '/^enum {/,/^};/p' "$T/g.c" | sed 's/^/      /'
  gcc -E -P "$T/g.c" $INC 2>/dev/null | grep -c . >/dev/null
  echo "      ^ shape=$s"
done
echo
md5sum "$SEC/src/devices/dev_dreamcast_gdrom.c"
echo "REALFILE2_DONE"
