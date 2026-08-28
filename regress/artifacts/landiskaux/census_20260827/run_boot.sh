#!/bin/bash
#  run_boot.sh <binary> <outfile> <seconds> [extra gxemul args...]
#  Boots OpenBSD 7.6 on UNMODIFIED -E landisk and captures everything the
#  emulator prints.  No pty: the landisk console is the SH4 SCIF routed to
#  the main console, which works on a plain pipe.
BIN="$1"; OUT="$2"; SECS="$3"; shift 3
IMG=/mnt/c/DocumentNoSnc/CC/GXEMUL/_images
#  `iR:` -- ALL prefix chars before a SINGLE colon (diskimage.c takes the FIRST
#  colon).  R: = read-only with a pid-unique discard overlay, so repeated runs
#  cannot inherit state.
timeout -s KILL "$SECS" "$BIN" -E landisk -M 64 \
    -d "iR:$IMG/wdc-scratch-64m.img" "$@" \
    "$IMG/openbsd76-landisk-bsd.rd" > "$OUT" 2>&1 < /dev/null
echo "TIMEOUT_RC=$?" >> "$OUT"
echo "BYTES=$(wc -c < "$OUT")" >> "$OUT"
