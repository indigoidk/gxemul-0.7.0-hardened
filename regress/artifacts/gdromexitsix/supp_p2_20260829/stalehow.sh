#!/bin/bash
#  #490 SUPP: give `stale how` its MEASURED RED.
#
#  THE CHANNEL, as the row states it: "a death the budget-window read pattern
#  CANNOT SEE -- any build that exits after the last budget check".
#
#  session()'s last budget check is rd(spin) after the final command.  It then
#  writes `quit`, calls rd(0.6) AND DISCARDS THE RESULT, closes the fd, and only
#  then waitpid()s.  So anything that changes the process's exit STATUS during or
#  after the quit is invisible to `alive` and visible to `how`.
#
#  H1 = src/core/main.c's final `return 0;`  ->  `return 1;`
#  That line runs after emul_run() returns, i.e. after the debugger processed
#  `quit` -- strictly after the last budget check.  It is the minimal edit that
#  exercises the named channel.
set -u
SRC=/tmp/gxopus490p2
T=/tmp/gxsupp490_h1
BINS=/tmp/gxsupp490_bins
OUT=/tmp/gxsupp490_out
PROBE=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/gdrom_default_probe.py
FROZEN=/tmp/gxsupp490_defprobe.py
KERNEL=/mnt/c/DocumentNoSnc/cc/GXEMUL/_images/openbsd76-landisk-bsd.rd
mkdir -p "$BINS" "$OUT"

echo "=== clone (never GXEMUL-SEC, never build/) ==="
rm -rf "$T"; cp -a "$SRC" "$T"
printf 'src/core/main.c  final return 0 -> return 1  (#490 supp, stale how)\n' > "$T/.MUTANT"
echo "  sentinel dropped: $(cat "$T/.MUTANT")"

#  FREEZE the instrument -- a comparison run owes ONE instrument, and the live
#  probe sits in a tree other sessions are editing today.
cp "$PROBE" "$FROZEN"
echo "  instrument frozen md5 $(md5sum "$FROZEN" | cut -d' ' -f1)"

cd "$T"
cp src/core/main.c /tmp/gxsupp490_main.c.ORIG

build_and_take () {   # $1 = tag
  rm -f src/core/main.o gxemul
  if ! make -j4 > "/tmp/gxsupp490_build_$1.log" 2>&1; then
      echo "  BUILD FAILED ($1); tail:"; tail -5 "/tmp/gxsupp490_build_$1.log"; return 1
  fi
  #  MAKE_RC has been observed 0 on a failed build -- check the artifact instead.
  [ -f gxemul ] || { echo "  NO BINARY ($1)"; return 1; }
  [ gxemul -nt src/core/main.c ] || { echo "  *** STALE BINARY ($1) ***"; return 1; }
  cp gxemul "$BINS/$1"
  echo "  $1 built: md5 $(md5sum "$BINS/$1" | cut -d' ' -f1)  binary-newer-than-source=YES"
}

echo
echo "=== 1. BASE rebuild in the clone (the apparatus control) ==="
build_and_take base || exit 1

echo
echo "=== 2. H1 mutant ==="
python3 - src/core/main.c <<'PYEOF'
import io, sys
p = sys.argv[1]
L = io.open(p, encoding="utf-8").read().split(chr(10))
#  the LAST `return 0;` in the file, which is main()'s -- assert uniqueness of the
#  anchor pair so a miss is a hard failure, never a silent no-op.
hits = [i for i, s in enumerate(L) if s.strip() == "return 0;"]
assert hits, "no `return 0;` found"
i = hits[-1]
assert L[i+1].strip() == "}", "last `return 0;` is not the final one (next=%r)" % L[i+1]
L[i] = L[i].replace("return 0;", "return 1;")
io.open(p, "w", encoding="utf-8", newline=chr(10)).write(chr(10).join(L))
print("  mutated line %d -> %s" % (i+1, L[i].strip()))
PYEOF
diff /tmp/gxsupp490_main.c.ORIG src/core/main.c | sed 's/^/    /'
build_and_take H1_exit1 || exit 1

echo
echo "=== 3. RESTORE + verify against GXEMUL-SEC, then rebuild ==="
cp /mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/core/main.c src/core/main.c
if cmp -s src/core/main.c /mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/core/main.c; then
    echo "  cmp against SEC: CLEAN"
    rm -f src/core/main.o gxemul
    make -j4 > /tmp/gxsupp490_build_restore.log 2>&1
    if [ -f gxemul ] && [ gxemul -nt src/core/main.c ]; then
        echo "  restore rebuild: md5 $(md5sum gxemul | cut -d' ' -f1)  (want base md5 above)"
        rm -f "$T/.MUTANT"; echo "  sentinel CLEARED (source cmp-clean AND binary newer than source)"
    else
        echo "  *** restore rebuild did NOT produce a fresh binary -- SENTINEL LEFT IN PLACE ***"
    fi
else
    echo "  *** cmp FAILED -- SENTINEL LEFT IN PLACE ***"
fi

echo
echo "=== 4. MEASURE: gdrom_default_probe on base and H1 ==="
for tag in base H1_exit1; do
    log="$OUT/def_${tag}.log"
    { echo "PROBE_TAG=$tag"; echo "PROBE_BIN_MD5=$(md5sum "$BINS/$tag" | cut -d' ' -f1)"
      echo "PROBE_INSTRUMENT_MD5=$(md5sum "$FROZEN" | cut -d' ' -f1)"
      echo "PROBE_START=$(date -Is)"; } > "$log"
    python3 -u "$FROZEN" "$BINS/$tag" "$KERNEL" >> "$log" 2>&1
    { echo "PROBE_RC=$?"; echo "PROBE_END=$(date -Is)"; echo "STALEHOW_DONE"; } >> "$log"
    echo "--- $tag  $(grep -o 'GDROM_DEF_RESULT=[0-9]*/[0-9]*' "$log" | tail -1)  control=$(grep -o 'GDROM_DEF_CONTROL=[A-Z]*' "$log" | tail -1)"
done

echo
echo "=== 5. THE VERDICT ROWS ==="
for tag in base H1_exit1; do
  echo "--- $tag: $(grep -c ' FAIL$' "$OUT/def_${tag}.log") failing"
  grep ' FAIL$' "$OUT/def_${tag}.log" | sed 's/^/      /'
  grep -E "^stale how |^stale quiet |^nodata stale |^stale says |^stale idle " "$OUT/def_${tag}.log" | sed 's/^/      /'
done
echo
echo "STALEHOW_ALLDONE $(date -Is)"
