#!/bin/bash
# fmtbb_kill.sh -- the format round's output row (fmt_bootblock_probe.py) on: HEAD + the stage (want 3/3), and the two
# type-compatible mutants of bootblock.c's loading line (want the row red).  Scratch clone in /tmp with a clone-local .MUTANT;
# after each mutant the staged bootblock.c is restored and cmp-verified.  Writes only under /tmp and _scratchpad/codescan/fmtfix.
set -u
C=/tmp/gxfmtbb_$$; O=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/codescan/fmtfix; TAR=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/codescan/head2_src.tar
PR=$O/stage_regress/fmt_bootblock_probe.py; BB=src/disk/bootblock.c; OUT=$O/bb_kill.out
{
echo "# $(date -u +%FT%TZ) fmtbb_kill: HEAD 79df4277 + stage, then 2 mutants of $BB"
mkdir -p "$C" && tar -xf "$TAR" -C "$C" || { echo "EXTRACT FAILED"; exit 1; }
echo "format-round output-row table" > "$C/.MUTANT"
for f in $(cd "$O/stage" && find src -type f); do cp "$O/stage/$f" "$C/$f"; done
( cd "$C" && ./configure > "$O/bb_configure.log" 2>&1 && make -j4 > "$O/bb_make.log" 2>&1 ); echo "base build rc=$?"
[ -x "$C/gxemul" ] || { echo "NO BASE BINARY"; exit 2; }
echo "== base (HEAD + stage)"; python3 -u "$PR" "$C/gxemul" base | grep -E '^(loading offset|FMTBB_)' | cut -c1-170
for m in M1_radix M2_narrow; do
  cp "$O/bb_mutants/$m.c" "$C/$BB" && rm -f "$C/src/disk/bootblock.o"
  ( cd "$C" && make -j4 > "$O/bb_make_$m.log" 2>&1 ); rc=$?
  [ "$C/gxemul" -nt "$C/$BB" ] && fresh=yes || fresh=NO
  echo "== $m (build rc=$rc, binary newer than the mutant source: $fresh)"
  python3 -u "$PR" "$C/gxemul" "$m" | grep -E '^(loading offset|FMTBB_)' | cut -c1-170
  cp "$O/stage/$BB" "$C/$BB" && cmp -s "$O/stage/$BB" "$C/$BB" && echo "   restored $BB (cmp clean)" || echo "   RESTORE FAILED"
done
rm -f "$C/.MUTANT"; cd / && rm -rf "$C"; [ -d "$C" ] && echo "CLONE NOT REMOVED" || echo "clone removed"
echo "FMTBB_KILL_DONE"
} > "$OUT" 2>&1
cat "$OUT"
