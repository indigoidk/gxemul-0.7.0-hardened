#!/bin/bash
cd /tmp/gxo549f2m || exit 2
for f in var/v/T_*.c; do echo "=== $(basename "$f")"; diff var/fix.c "$f"; done
