#!/bin/bash
# GATE 10 -- SuperH floating-point rounding mode, measured on real guest instructions.
#
# What this protects
# -----------------
# #296 wired FPSCR.RM into thirteen of the sixteen single-precision store sites in
# cpu_sh_instr.c. Before it, the field was guest-writable and decoded NOWHERE: every store
# truncated. Truncation is round-toward-zero, which is the mode the SH-4 resets into, so
# there was no visible defect until you look at a guest that CHANGES the mode -- and
# OpenBSD/landisk installs round-to-nearest at every exec.
#
# Why the vectors look the way they do
# -----------------------------------
# Each one runs under BOTH modes and expects DIFFERENT answers, so reverting #296 turns the
# gate red. Two vectors are deliberately mode-INDEPENDENT and named PIN: they record limits
# that are real and are NOT fixed (double precision cannot be fixed at the store, and the
# host-double double-rounding is shared by every CPU core). A pin failing means someone
# changed a known limitation without updating the record -- which is worth knowing either
# way, and is the opposite of a check that cannot fail.
#
# The gate asserts on the number of discriminating vectors as well as on the results,
# because a table where every vector wants the same answer in both modes would pass
# vacuously. That is the failure mode this harness has now been bitten by five times.
set -u
cd "$(dirname "$0")"
. ./lib.sh

gate_begin "gate 10: SuperH rounding mode (#296)"

PMAX=${PMAX:-$ROOT/build/gxemul}
KERNEL=$IMAGES/openbsd76-landisk-bsd.rd
LOG=$LOGDIR/gate_sh_rounding.log

need_exec "$PMAX"
need_file "$KERNEL"
command -v python3 >/dev/null || gate_skip "python3 not available"

note "binary : $PMAX"
note "kernel : $KERNEL (loaded so the machine constructs; never executed)"
note "cold debugger, no media, no console -- the SCIF drops host->guest writes (#293)"

python3 sh_rounding_probe.py "$PMAX" "$KERNEL" > "$LOG" 2>&1 || true

if ! grep -q "SH_ROUND_RESULT=" "$LOG"; then
    note "probe produced no result line; last lines follow"
    tail -5 "$LOG" | sed 's/^/       /'
    gate_skip "probe did not complete"
fi

sed -n '1,/SH_ROUND_DISCRIMINATING/p' "$LOG" | grep -E "ok$|FAIL" | sed 's/^/       /'

res=$(grep -o "SH_ROUND_RESULT=[0-9]*/[0-9]*" "$LOG" | tail -1 | cut -d= -f2)
got=${res%/*}; want=${res#*/}
disc=$(grep -o "SH_ROUND_DISCRIMINATING=[0-9]*" "$LOG" | tail -1 | cut -d= -f2)

# 36 vector-mode pairs: 17 vectors x 2 modes (9 from #296, 6 ftrc rows from #297, and
# #299 turned the double-rounding PIN into a discriminating row and added the fmac
# tie-band witness) + #303's two single-mode subnormal-operand rows (RN pinned; DN
# STRIPPED by their NODN marker -- a DN=1 numeric expectation would bless a value
# real silicon flushes; committed bytes 0x32000001 / 0x3f800001 measured live).
check     "vector-mode pairs run"                  "$want" 36
check     "vector-mode pairs correct"              "$got"  "$want"
# EXACTLY 9 of the 17 vectors discriminate between the two modes: the 7 from #296 plus
# the #299-fixed fsub band row and the #300-fixed D-division row (each a PIN until its
# fix landed; each flip was that fix's acceptance test). If this number drops, someone weakened the table; if it RISES,
# someone made a mode-independent row (an ftrc row, or the fmac tie whose two modes
# genuinely agree) depend on FPSCR.RM, which is drift in the other direction.
# (#303's two rows are single-mode by design and cannot enter this count.)
check     "vectors that discriminate the two modes" "$disc" 9

# Per-instruction closure: naming them individually means a single site silently reverting
# cannot hide behind an aggregate count. The ftrc rows are #297's regression checks; the
# "fsub band" and "fmactie" rows are #299's (the pre-#299 build fails the band's RZ arm
# and the tie's RN arm).
for v in "fdiv" "float" "fadd " "fmac " "fmactie" "fipr" "ftrv" "fmul" \
         "fsub band" "faddinf" "Ddiv" "ftrcS-inf" "ftrcS-ovf" "ftrcS-nan" "ftrcS-edge" \
         "ftrcD-2p31" "ftrcD-neghalf"; do
    n=$(grep -c "^$v.*ok$" "$LOG")
    check "  $v: both modes correct" "$n" 2
done
# #303's subnormal rows are SINGLE-mode (RN pinned; see the probe) -- one line each.
for v in "subn fmul" "subn fdiv"; do
    n=$(grep -c "^$v.*ok$" "$LOG")
    check "  $v: RN row correct" "$n" 1
done

# ---- #314: legal encodings must not stop the emulator ------------------------
# The SH decoder answered an unimplemented encoding with `goto bad`, which sets
# cpu->running = 0. All eight rows below were measured HALTING the committed
# build; three of them are BASE ISA (MAC.L, MAC.W, TST.B), present since
# SH-1/SH-2 and legal on the SH7751R this rig models -- so this is not a
# question about accepting SH-4A extensions on an SH-4 core.
#
# The probe classifies the outcome from the dyntrans halt MESSAGE, not from a
# memory marker: after the fix the exception is raised and any store placed
# after the test instruction is legitimately never reached, so a marker-only
# check called every repaired row a failure (and called SLEEP, which is
# implemented and simply sleeps, a halt). See the probe's header.
HLOG=$LOGDIR/gate_sh_halt.log
python3 sh_halt_probe.py "$PMAX" "$KERNEL" > "$HLOG" 2>&1 || true

if ! grep -q "SH_HALT_RESULT=" "$HLOG"; then
    note "halt probe produced no result line; last lines follow"
    tail -5 "$HLOG" | sed 's/^/       /'
    #  a CHECK, not a gate_skip: the rounding section above has already
    #  recorded results and a skip here would discard them.
    check "halt probe completed" "no" "yes"
    gate_end; exit $?
fi

grep -E " ok$| FAIL$" "$HLOG" | sed 's/^/       /'

hctrl=$(grep -o "SH_HALT_CONTROL=[A-Z]*" "$HLOG" | tail -1 | cut -d= -f2)
check "halt-probe control proves it measures" "${hctrl:-missing}" "OK"

hres=$(grep -o "SH_HALT_RESULT=[0-9]*/[0-9]*" "$HLOG" | tail -1 | cut -d= -f2)
hgot=${hres%/*}; hwant=${hres#*/}
check "halt rows run"     "$hwant" 26
check "halt rows correct" "$hgot"  "$hwant"

# Named, so one encoding regressing cannot hide behind a total. Two spaces after
# the name: the probe pads to a fixed column and a name that is a PREFIX of
# another would otherwise match both rows (the trap that made two of gate 14's
# checks unsatisfiable and two of gate 13's count the wrong rows).
for v in "MAC.L" "MAC.W" "TST.B" "STC SGR" "STC.L DBR" "MOVLI.L" "SYNCO" "PREFI"; do
    n=$(count "$HLOG" "^$v  .*ok$")
    check "  survives: $v" "$n" 1
done

# ---- #315/#316/#317: execute-time halts, and one dropped store ---------------
# These need a state prologue (FPSCR.SZ/PR, SR.FD, a branch), so the bare
# encoding sweep above is structurally blind to them -- which is why they
# outlived #314. Three of them killed the gxemul PROCESS rather than setting
# cpu->running = 0, so the probe distinguishes a host exit from an emulator
# halt from a live run; a check that only looked for the halt message would
# have scored those as passes.
#
# The two XD rows are load-bearing. The register-pair handlers redirect an ODD
# register field to the XF bank, and an earlier draft computed that redirect
# then still transferred through the original pointer -- which every DR test
# passes. Only a row that seeds fr and xf differently can tell them apart.
#
# `movca.l` carries its own trap: r12 is the DECODER's default source for that
# encoding, so the row seeds r12 with a decoy and fails if the R0 override is
# ever dropped.
# ---- #318: the store-queue flush with the MMU on -----------------------------
# `pref` into the SQ range is a write-back, and with MMUCR.AT set the
# destination comes from the UTLB, not from QACR. That path used to run
# ABORT_EXECUTION.
#
# The probe installs the UTLB entry and MMUCR through GUEST stores to the
# architectural MMIO windows, because the debugger's register names for those
# fields exist but do not reach them -- an earlier version set them by name,
# never entered the AT branch, and would have passed against an unfixed build.
#
# `sq at1 ok` is the composition witness, not just a survival check: the operand
# has nonzero bits in BOTH [9:5] and [4:0], and the architectural destination is
# the translated page plus [9:5] with [4:0] zeroed -- an address that is neither
# the operand nor the page base.
#
# `sq at1 clean` pins the WRITE-type judgement the panel split on: a clean page
# owes an initial-page-write fault, so a build that judged this access as a read
# would complete the copy and fail this row alone.
#
# `sq at0 qacr` is the regression guard: with the MMU off the QACR composition
# must be exactly as before.
for v in "sq at1 ok" "sq at1 miss" "sq at1 prot" "sq at1 clean" "sq at0 qacr"; do
    n=$(count "$HLOG" "^$v  .*ok$")
    check "  round 81: $v" "$n" 1
done

for v in "movca.l" "fmovd @r1" "fmovd @r2" "fmovd xd st" "fmovd xd ld" \
         "fmovd r0idx" "fmovs SZ=0" "fsrra PR=1" "fneg odd PR=1" \
         "fabs odd PR=1" "fp in slot" "trapa in slot"; do
    n=$(count "$HLOG" "^$v  .*ok$")
    check "  round 80: $v" "$n" 1
done

# ------------------------------------------------------------------ #443 sh4_pcic
#  A guest 32-bit LOAD to an unimplemented PCIC offset used to END THE HOST PROCESS.  A
#  MEASURED census of all 137 word offsets in both directions found 116 killing on a read
#  and 125 on a write; post-fix both are 0.
#
#  *** WIRED HERE IN THE SAME COMMIT AS THE PROBE, WHICH IS THE WHOLE POINT. ***  Both
#  sh_halt_probe.py above and sh4_bsc_width_probe.py (#441) shipped UNWIRED, and gate 6's
#  own structural note says a probe that ships with its wiring cannot skip its census pin,
#  because the wiring forces a gate run.  #441's did not, and the pin then went latently
#  red between two commits.
#
#  Note the existing halt probe is blind to this by construction: it classifies from the
#  dyntrans HALT message, and exit(1) is not a halt.
PCLOG=$LOGDIR/gate_sh4_pcic.log
python3 sh4_pcic_probe.py "$PMAX" "$KERNEL" > "$PCLOG" 2>&1 || true

if ! grep -q "SH4_PCIC_RESULT=" "$PCLOG"; then
    note "sh4_pcic probe produced no result line; last lines follow"
    tail -5 "$PCLOG" | sed 's/^/       /'
    check "sh4_pcic probe completed" "no" "yes"
else
    grep -E "^  (ok|FAIL) " "$PCLOG" | sed 's/^/       /'
    check "sh4_pcic: no offset kills the host"           "$(grep -c 'SH4_PCIC_PASS' "$PCLOG")" "1"
    #  The census rows are the ONLY thing that sees a latch sharing one word between
    #  offsets 32 apart -- a mutant a measuring seat built which passes both the
    #  per-offset and the per-device rows.  So pin that they ran, not merely that the
    #  verdict was green.
    #  29 -> 38 in the same edit that grew the probe: a pass-2 seat measured SEVEN mutants
    #  all scoring 29/29 -- including one that reinstated the original host kill -- and the
    #  nine new rows are what kill them.  This is a FLOOR, so it would have stayed green at
    #  38 with no edit at all, which is exactly how a floor stops noticing.
    check_min "sh4_pcic: rows actually run"           "$(grep -cE '^  (ok|FAIL) ' "$PCLOG")" 38
fi

gate_end
