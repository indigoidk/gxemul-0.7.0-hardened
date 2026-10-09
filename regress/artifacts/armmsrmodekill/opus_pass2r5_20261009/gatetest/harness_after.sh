#!/bin/bash
# harness_after.sh <fixture> -- the LITERAL reading of "appended to gate_arm.sh": the section placed
# AFTER the file's final `gate_end', with an earlier gate-14 check already FAILED.  The script's exit
# status (what run.sh reads) is printed by the caller.
set -u
H=$(cd "$(dirname "$0")" && pwd)
FX=$1
export ROOT=$H LOGDIR=$H/logdir
. "$H/lib.sh"
PMAX=/nonexistent/gxemul
python3() { cat "$H/fx/$FX"; return 0; }
gate_begin "gate 14 with the section AFTER gate_end ($FX)"
check "an EARLIER gate-14 check that fails" "no" "yes"
gate_end
. "$H/../gate_section.sh"
