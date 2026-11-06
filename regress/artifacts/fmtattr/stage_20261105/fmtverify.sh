#!/bin/bash
# fmtverify.sh -- HEAD's sources + the staged format fixes (fmtfix/stage/src) + the four printf-format attributes, built in a
# scratch dir; counts GCC's format warnings by kind.  The target is 0 -Wformat= and 0 -Wformat-extra-args.  Writes only under
# /tmp and _scratchpad/codescan/fmtfix/.  Usage: fmtverify.sh <head_tar>
set -u
D=/tmp/gxfmtv_$$; O=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/codescan/fmtfix; TAR=${1:?head tar}
{
echo "# $(date -u +%FT%TZ) fmtverify: $TAR + fmtfix/stage + format attributes, scratch build in $D"
mkdir -p "$D" && tar -xf "$TAR" -C "$D" || { echo "EXTRACT FAILED"; exit 1; }
n=0; for f in $(cd "$O/stage" && find src -type f); do cp "$O/stage/$f" "$D/$f" && n=$((n+1)); done; echo "staged files overlaid: $n"
H=$D/src/include/misc.h
sed -i -E \
  -e 's/^void debug\(const char \*fmt, \.\.\.\);/void debug(const char *fmt, ...) __attribute__((format(printf, 1, 2)));/' \
  -e 's/^void fatal\(const char \*fmt, \.\.\.\);/void fatal(const char *fmt, ...) __attribute__((format(printf, 1, 2)));/' \
  -e 's/^(void debugmsg\(int subsystem, const char \*name, int verbosity_required, const char \*fmt, \.\.\.\));/\1 __attribute__((format(printf, 4, 5)));/' \
  -e 's/^(void debugmsg_cpu\(struct cpu\* cpu, int subsystem, const char \*name, int verbosity_required, const char \*fmt, \.\.\.\));/\1 __attribute__((format(printf, 5, 6)));/' \
  "$H"
echo "attributes added: $(grep -c '__attribute__((format(printf' "$H") of 4"
( cd "$D" && ./configure > "$O/v_configure.log" 2>&1 ); echo "configure rc=$?"
( cd "$D" && make -k -j4 > "$O/v_make.log" 2>&1 ); echo "make rc=$?"
[ -x "$D/gxemul" ] && echo "binary built: yes" || echo "binary built: NO"
for k in '-Wformat=' '-Wformat-extra-args' '-Wformat-zero-length' '-Wformat-overflow='; do
  echo "warnings $k: $(grep -c -F -- "[$k]" "$O/v_make.log")"; done
echo "errors: $(grep -c ': error:' "$O/v_make.log")"
echo "FMTVERIFY_DONE"
rm -rf "$D"; [ -d "$D" ] && echo "SCRATCH NOT REMOVED" || echo "scratch removed"
} > "$O/fmtverify.out" 2>&1
cat "$O/fmtverify.out"
