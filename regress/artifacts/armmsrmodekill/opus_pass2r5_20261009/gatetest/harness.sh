#!/bin/bash
# harness.sh <fixture> <rc> -- run the brief's gate-14 section VERBATIM against a canned probe log.
# `python3' is shadowed by a function that prints the fixture and returns <rc>; everything else
# (lib.sh's check/note/gate_end, the section's greps and seds) is the real code.
set -u
H=$(cd "$(dirname "$0")" && pwd)
FX=$1; RC=$2
export ROOT=$H LOGDIR=$H/logdir
. "$H/lib.sh"
PMAX=/nonexistent/gxemul
python3() { cat "$H/fx/$FX"; return "$RC"; }
gate_begin "msrmode section vs $FX (rc=$RC)"
. "$H/../gate_section.sh"
gate_end
echo "GATE_EXIT=$?"
