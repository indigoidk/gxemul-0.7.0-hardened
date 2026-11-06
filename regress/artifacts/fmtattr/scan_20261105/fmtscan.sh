#!/bin/bash
# fmtscan.sh -- a HEAD-accurate re-scan of the printf-format class: HEAD's sources (head_src.tar, HEAD f58105b7) in a scratch dir,
# misc.h's four printf-like declarations given __attribute__((format(printf, ...))) so GCC's -Wformat checks every call, then a
# full build with -k.  Writes only under /tmp and _scratchpad/codescan/.
set -u
D=/tmp/gxfmt_$$; O=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/codescan
{
echo "# $(date -u +%FT%TZ) fmtscan: HEAD sources + format attributes, scratch build in $D"
mkdir -p "$D" && tar -xf "$O/head_src.tar" -C "$D" || { echo "EXTRACT FAILED"; exit 1; }
H=$D/src/include/misc.h
sed -i -E \
  -e 's/^void debug\(const char \*fmt, \.\.\.\);/void debug(const char *fmt, ...) __attribute__((format(printf, 1, 2)));/' \
  -e 's/^void fatal\(const char \*fmt, \.\.\.\);/void fatal(const char *fmt, ...) __attribute__((format(printf, 1, 2)));/' \
  -e 's/^(void debugmsg\(int subsystem, const char \*name, int verbosity_required, const char \*fmt, \.\.\.\));/\1 __attribute__((format(printf, 4, 5)));/' \
  -e 's/^(void debugmsg_cpu\(struct cpu\* cpu, int subsystem, const char \*name, int verbosity_required, const char \*fmt, \.\.\.\));/\1 __attribute__((format(printf, 5, 6)));/' \
  "$H"
echo "attributes added: $(grep -c '__attribute__((format(printf' "$H") of 4"
( cd "$D" && ./configure > "$O/fmt_configure.log" 2>&1 ); echo "configure rc=$?"
( cd "$D" && make -k -j4 > "$O/fmt_make.log" 2>&1 ); echo "make rc=$?"
[ -x "$D/gxemul" ] && echo "binary built: yes" || echo "binary built: NO"
echo "format warnings: $(grep -c -E 'warning: .*\[-Wformat' "$O/fmt_make.log")"
echo "FMTSCAN_DONE"
rm -rf "$D"; [ -d "$D" ] && echo "SCRATCH NOT REMOVED" || echo "scratch removed"
} > "$O/fmtscan.out" 2>&1
cat "$O/fmtscan.out"
