#!/bin/bash
# fable5 adj B -- F4's row, directly: (1) a TRIGGER refusal row `SYSASIC_TRIGGER_EVENT(1 ? 200 : 5)' and its ADDR twin,
# compiled -c under PROD and POL flags on BASE / e1noparen / e2noparen, scored by the instrument's own oracle shape
# (exactly one `error:' line, bit-field-width class, RANGE_OK note); (2) the IN-DOMAIN low-precedence raise
# `1 ? 33 : 0' RUN through the recording stub on BASE / A_enoparen / B_enoparen / e1 / e2 -- the half of the
# argument-shape class the coordinator's row does not reach.
set -u
W=/tmp/gxfable_adjB
P=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/adjB
T=$W/latent; rm -rf "$T"; mkdir -p "$T"
MIRROR="-Wshadow -Wcast-align -Wstrict-aliasing -Wall -Wextra -Wno-unused-parameter -Wno-cast-align -fstrict-aliasing -fomit-frame-pointer -fpeephole -fgnu89-inline -O3 -DNDEBUG"
POL="-std=c99 -pedantic-errors -Wall -Wextra -O0"
DIAG="-fno-diagnostics-show-caret -fdiagnostics-color=never"
pre() {
  echo '#include <stdint.h>'
  echo '#include <stddef.h>'
  echo 'struct memory; struct cpu { struct memory *mem; int (*memory_rw)(struct cpu *, struct memory *, uint64_t, unsigned char *, size_t, int, int); };'
  echo '#define MEM_WRITE 1'
  echo '#define PHYSICAL 32'
  echo 'void memory_writemax64(struct cpu *cpu, unsigned char *buf, int len, uint64_t data);'
  echo '#include "thirdparty/dreamcast_sysasicvar.h"'
}
echo "== (1) refusal rows, oracle-shaped"
for m in BASE e1noparen e2noparen; do
  for route in TRIG ADDR; do
    f=$T/${m}_${route}.c
    { pre
      if [ "$route" = ADDR ]; then echo 'unsigned long f(void); unsigned long f(void) { return SYSASIC_EVENT_TO_ADDR(1 ? 200 : 5); }'
      else echo 'void g(struct cpu *cpu); void g(struct cpu *cpu) { SYSASIC_TRIGGER_EVENT(1 ? 200 : 5); }'; fi
    } > "$f"
    for leg in PROD POL; do
      if [ $leg = PROD ]; then FL=$MIRROR; else FL=$POL; fi
      LC_ALL=C cc $FL $DIAG -I"$W/media/$m" -c -o "$f.$leg.o" "$f" > "$f.$leg.err" 2>&1
      rc=$?
      nerr=$(grep -c ': error: ' "$f.$leg.err")
      cls=$(grep -m1 -oE 'negative width in bit-field|zero width for bit-field|width of .* exceeds its type' "$f.$leg.err")
      note=$(grep -c "note: in expansion of macro .SYSASIC_EVENT_RANGE_OK." "$f.$leg.err")
      if [ $rc = 0 ]; then verdict=ACCEPTED; else verdict="refused"; fi
      echo "  $m $route $leg: rc=$rc errors=$nerr class=[$cls] range_ok_note=$note -> $verdict"
    done
  done
done
echo "== (2) the in-domain low-precedence raise 1 ? 33 : 0, RUN (want addr 0x5f6904, pay 0x100000002)"
python3 -I "$P/mk_indomain.py" "$W"
for m in BASE A_enoparen B_enoparen e1noparen e2noparen; do
  LC_ALL=C cc $MIRROR $DIAG -I"$W/media/$m" -o "$T/indomain_$m" "$T/indomain.c" > "$T/indomain_$m.err" 2>&1
  rc=$?
  if [ $rc = 0 ]; then
    "$T/indomain_$m" | sed "s/^/  $m: /" | cut -c1-150
  else
    echo "  $m: did not compile: $(grep -m1 ': error: ' $T/indomain_$m.err)"
  fi
done
echo LATENT_DONE
