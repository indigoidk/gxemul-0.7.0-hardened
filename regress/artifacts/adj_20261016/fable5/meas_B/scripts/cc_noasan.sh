#!/bin/bash
# SIMULATED toolchain without libasan: any invocation carrying -fsanitize=address fails the way ld does.
for a in "$@"; do
  if [ "$a" = "-fsanitize=address" ]; then
    echo "/usr/bin/ld: cannot find -lasan: No such file or directory (SIMULATED by cc_noasan.sh)" >&2
    echo "collect2: error: ld returned 1 exit status" >&2
    exit 1
  fi
done
exec gcc "$@"
