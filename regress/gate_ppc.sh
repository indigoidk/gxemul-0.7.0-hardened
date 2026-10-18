#!/bin/bash
# GATE 13 -- PowerPC single-precision conversion fidelity, on real guest instructions.
#
# What this protects
# -----------------
# #304 gave `frsp` the rounding mode it never read (the narrowing was a host C cast,
# nearest-always, so the three directed modes were unreachable) and taught `stfs` the
# ISA's denormalization band, which it had been flushing to signed zero. #305 stopped
# `lfs`/`stfs` from destroying a NaN's sign and payload: the value-domain transport
# (interpret -> host double -> store) structurally cannot carry them, so the NaN classes
# are handled by bit surgery on the pattern instead.
#
# Why this gate had to exist BEFORE the fixes
# ------------------------------------------
# There is no PowerPC OS rig -- no guest boots on this path -- so the defects were found
# by a cold-debugger spike and every one of them could only be believed once an
# instrument measured it. The rows below were run against the COMMITTED build first and
# their committed bytes recorded; the fix then had to flip exactly the DISC rows and
# leave every PIN untouched. That baseline sweep is what makes "the fix worked" a
# measurement rather than a claim, and it caught three of the author's own wrong
# predictions before any code changed (frsp's RN overflow to Infinity is ISA-correct,
# and the negative band row keeps its sign through the flush).
#
# Three row classes, and why PINs are not decoration
# -------------------------------------------------
#   PIN  -- correct today, must stay. Includes two POLICY pins: for finite values at
#           and above ~2^129 the letter of Book I would splice-WRAP the exponent, and
#           this fork deliberately keeps #287's +/-Inf instead (the letter turns a
#           finite overflow into a NaN pattern: 1.5*2^128 -> 0x7FC00000). A policy pin
#           failing means someone changed a known divergence without updating the
#           record -- worth knowing either way.
#   DISC -- discriminator: committed byte is the defect, want flips with the fix.
#   DIV  -- known divergence left to a later round, pinned so it cannot drift.
#   [#556, 2026-10-02 -- a records correction; the text above is kept as it was written] The DISC classification
#   includes 7 negative controls in CAUSE_ROWS that verify non-raising of exception flags (yielding identical values
#   before and after #330), contrary to :32 defining DISC as values that flip with the fix.  (hbundle_regress27:F11:
#   regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md)
#
# #310's eighteen rows cover the eight float UPDATE forms, every one of which
# stopped the emulator before this round -- neither the primary opcodes
# 0x31/0x33/0x35/0x37 nor the indexed 567/631/695/759 were defined or decoded.
# Each form gets BOTH halves of its contract: a value row and a base-register
# row. A diff-review seat caught the first version giving five forms a base row
# only, which would have passed an implementation with the wrong transfer size
# that still advanced the base.
#
# The two non-update rows assert the mirror image, that the base is UNCHANGED --
# and their displacement and index are NONZERO on purpose. With a zero offset
# the effective address equals the base, so a wrongly-updating implementation
# would write back exactly the value the row expects: the same seat found both
# controls vacuous that way.
#
# The control row is load-bearing: `msr=0x2000` must take or every FP instruction
# raises FPU-unavailable and the probe measures nothing. A dead probe SKIPs; it never
# passes quietly. The mode rows additionally read FPSCR back, because a mode that
# silently failed to take would turn every directed-mode row into a second copy of
# the RN row.
# [#556, 2026-10-02 -- a records correction; the text above is kept as it was written] Absence of PPC_CONV_RESULT=
# invokes gate_skip, preserving earlier failures. With a result present, missing control or mode-readback tokens
# fail; PPC_CONV_CONTROL=DEAD also fails. FPSCR writes are verified in four separate sessions, once per rounding
# mode.  (hbundle_regress27:F12: regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md)
#
# Those rows set FPSCR by DEBUGGER WRITE rather than through the guest's own `mtfsf`,
# which used to be necessary: #324 found that instruction building its write mask with
# an eight-bit stride across four-bit fields, so half the FM bits wrote nothing and the
# rest wrote the wrong fields. It is fixed and has six rows of its own now. The
# debugger write stays because it keeps the mode rows independent of a second
# instruction's correctness -- which is the property that let #324 be found at all.
#
# The `mtfsf` rows used to record a DIVERGENCE here: FM=0x80 selects field 0, whose bits
# 1 and 2 are FEX and VX, and mtfsf copied them straight out of frB although Book I
# lists it among the five instructions that "cannot alter FPSCR FEX / VX explicitly".
# #327 closed that, and the row now expects hardware's 90000000 instead of the
# emulator's old f0000000. THREE MORE ROWS MOVED WITH IT, because VX and FEX are
# DERIVED and the recompute re-establishes them from whatever mtfsf did write: FM=0x40
# gains VX from VXSNAN, FM=0x0f gains both from VXSOFT/VXSQRT/VXCVI plus VE, and
# `mtfsf clears` keeps both because its preloaded causes and enables survive the
# field-0 write. FM=0xff is unchanged only by coincidence -- with every cause and
# enable set, derivation reproduces the copy -- and FM=0x01 selects a field with no
# causes in it at all.
#
# All four bytes were PRE-REGISTERED from Book I before the code was written, which is
# what makes this gate the fix's acceptance test rather than a transcript of it.
# FM=0x40 stays the clean companion row for field PLACEMENT: it holds VXSNAN, which
# the guest could not clear at all until #324 (its nibble landed above bit 31).
#
# #325's `fctiwz` rows carry a warning of their own. That row was pinned as a known
# DIVERGENCE from #304 onward with its answer recorded as 00000000 -- and it was never
# measuring the instruction it named: its word had frB = 0, so it converted f0 while
# the probe seeded f1, and the zero came from an empty register. The `fctiwz 1.0
# control` row exists because of it: a wrong register field yields zero for ANY
# operand, so rows expecting 0x80000000 or 0 can be satisfied by accident and a row
# expecting 1 cannot.
set -u
cd "$(dirname "$0")"
. ./lib.sh

gate_begin "gate 13: PowerPC FP conversion + FPSCR (#304/#305/#324-#330) + rlwimi/rldimi/rldicl"

PMAX=${PMAX:-$ROOT/build/gxemul}
LOG=$LOGDIR/gate_ppc.log

need_exec "$PMAX"
command -v python3 >/dev/null || gate_skip "python3 not available"

# ---- ppcrlwimiwidth: X(rlwimi) at 32-bit width + the wrapping mask's high half --------
# BEFORE the NetBSD prerequisite ON PURPOSE.  These rows are register-to-register on
# `-E bareppc -M 64` and need no image; behind need_file a missing image would turn a
# red detector into a silent SKIP.  Placed here, a red row is recorded first, and #371's
# gate_skip then reports FAIL rather than absorbing it.  PARSE BEFORE SCORE: gates grep
# the result line, never the exit status, and a missing or DUPLICATED protocol line is a
# FAIL.  Both halves of the score are pinned to a literal so a shrunk table cannot pass.
RLWLOG=$LOGDIR/ppc_rlwimi.log
python3 ppc_rlwimi_probe.py "$PMAX" gate > "$RLWLOG" 2>&1 || true
#  Each KEY must occur exactly once in ANY form, and that one line must be well formed --
#  counting only well-formed lines let a malformed EXTRA `RESULT=' through (codex review).
rlwres=$(grep -c '^PPC_RLWIMI_RESULT=' "$RLWLOG")
rlwresok=$(grep -cE '^PPC_RLWIMI_RESULT=[0-9]+/[0-9]+$' "$RLWLOG")
rlwctl=$(grep -c '^PPC_RLWIMI_CONTROL=' "$RLWLOG")
rlwctlok=$(grep -cE '^PPC_RLWIMI_CONTROL=(OK|FAIL)$' "$RLWLOG")
rlwdone=$(grep -c '^PPC_RLWIMI_PROBE_DONE' "$RLWLOG")
if [ "$rlwres" = 1 ] && [ "$rlwresok" = 1 ] && [ "$rlwctl" = 1 ] && [ "$rlwctlok" = 1 ] &&
   [ "$rlwdone" = 1 ] && grep -qx 'PPC_RLWIMI_PROBE_DONE' "$RLWLOG"; then
    check "rlwimi protocol parsed" "yes" "yes"
    grep -E " ok$| FAIL$" "$RLWLOG" | sed 's/^/       /'
    rlw=$(grep '^PPC_RLWIMI_RESULT=' "$RLWLOG" | cut -d= -f2)
    check "rlwimi controls prove the probe measures" \
          "$(grep '^PPC_RLWIMI_CONTROL=' "$RLWLOG" | cut -d= -f2)" "OK"
    check "rlwimi rows run"     "${rlw#*/}" 28
    check "rlwimi rows correct" "${rlw%/*}" 28
else
    note "rlwimi: protocol lines missing or duplicated (result=$rlwres control=$rlwctl done=$rlwdone)"
    tail -5 "$RLWLOG" | sed 's/^/       /'
    check "rlwimi protocol parsed" "no" "yes"
fi

# ---- ppcrldimimask: X(rldimi) mask bounds + wrap (same shape, same reasons) ------------
RLDLOG=$LOGDIR/ppc_rldimi.log
python3 ppc_rldimi_probe.py "$PMAX" gate > "$RLDLOG" 2>&1 || true
#  Each KEY must occur exactly once in ANY form, and that one line must be well formed --
#  counting only well-formed lines let a malformed EXTRA `RESULT=' through (codex review).
rldres=$(grep -c '^PPC_RLDIMI_RESULT=' "$RLDLOG")
rldresok=$(grep -cE '^PPC_RLDIMI_RESULT=[0-9]+/[0-9]+$' "$RLDLOG")
rldctl=$(grep -c '^PPC_RLDIMI_CONTROL=' "$RLDLOG")
rldctlok=$(grep -cE '^PPC_RLDIMI_CONTROL=(OK|FAIL)$' "$RLDLOG")
rlddone=$(grep -c '^PPC_RLDIMI_PROBE_DONE' "$RLDLOG")
if [ "$rldres" = 1 ] && [ "$rldresok" = 1 ] && [ "$rldctl" = 1 ] && [ "$rldctlok" = 1 ] &&
   [ "$rlddone" = 1 ] && grep -qx 'PPC_RLDIMI_PROBE_DONE' "$RLDLOG"; then
    check "rldimi protocol parsed" "yes" "yes"
    grep -E " ok$| FAIL$" "$RLDLOG" | sed 's/^/       /'
    rld=$(grep '^PPC_RLDIMI_RESULT=' "$RLDLOG" | cut -d= -f2)
    check "rldimi controls prove the probe measures" \
          "$(grep '^PPC_RLDIMI_CONTROL=' "$RLDLOG" | cut -d= -f2)" "OK"
    check "rldimi rows run"     "${rld#*/}" 29
    check "rldimi rows correct" "${rld%/*}" 29
else
    note "rldimi: protocol lines missing or duplicated (result=$rldres control=$rldctl done=$rlddone)"
    tail -5 "$RLDLOG" | sed 's/^/       /'
    check "rldimi protocol parsed" "no" "yes"
fi

# ---- ppcrldiclzero (#522) + #565: X(rldicl) wrote ZERO on every execution -- its 24-row detector --------
# Shipped EXEMPT with e777ff06 (2026-09-10) and re-dated three times by owner ruling (2026-09-18 with
# ten others, eec0f4a3; 2026-09-24 with nine others; 04f3e7c0 on 2026-10-09) because no block here
# scored it; #565 discharges that exemption.  BEFORE the NetBSD prerequisite for the reason the rlwimi block gives: `-E bareppc -M 64`
# needs no image, so a red row is recorded first.  A stalled guest cannot hang the gate: the probe's
# own subprocess backstops (90 s; 60 s for the bogus-machine and 32-bit sessions) turn it into
# failing rows.  The probe prints no RESULT/CONTROL protocol, so it is scored as gate_arm.sh scores
# mk48's: its completion sentinel, then EVERY row by name, then the run/green/red counts and its own
# SCORE line, each pinned to a literal so a shrunk or renamed table cannot pass -- 30 checks when
# green.  Names sit in a %-18s column and none is longer than 15, so `^name  ' cannot match a
# neighbour (the padded-column trap).  The rows-run line is in the form check_score_claims.py pins.
# CONTRACT: the block TRANSMITS the probe's verdicts and re-derives none -- each row's ok/FAIL and its
# SCORE come from one comparison in the probe's row(), so an edit there (Grok 4.7's `ok = True', GPT-6
# Astra's `>=', #565 pass 2) lets a mutant through, as it would through any block that scores only a
# probe's ok/FAIL tokens (some gate_arm.sh blocks also pin a got= value; this one, like mk48's, does not).
# The exit status is ignored on purpose: this probe exits 0 with failed rows (probeexitzero).
# Floor (c), measured (regress/artifacts/ppcrldiclzero/gatewire_20261018/nullmedium/): an IDENTITY
# BODY for X(rldicl) -- decode and retire, write nothing -- reds 11 of the 30 (identity/), and
# /bin/true 22 of the 30.  An absent binary reds the sentinel check in this block's scoring text, but
# in gate 13 need_exec turns it into a SKIP before any check.
RLCLOG=$LOGDIR/ppc_rldicl.log
python3 -u ppc_rldicl_probe.py "$PMAX" gate > "$RLCLOG" 2>&1 || true
if [ "$(grep -cx 'PPC_RLDICL_PROBE_DONE' "$RLCLOG")" != 1 ]; then
    note "ppc_rldicl: completion sentinel missing or duplicated; last lines follow"
    tail -5 "$RLCLOG" | sed 's/^/       /'
    check "ppc_rldicl probe completed" "no" "yes"
else
    check "ppc_rldicl probe completed" "yes" "yes"
    for v in "session" "live" "seed holds" "src intact" "disasm xcheck" "zx32 rldicl" "zx32 rldicr" "rot8 rldicl" "rot8 rldicr" "naive fix wrong" "neg apparatus" "bits32 live" "bits32 rld bad" "vacuous cell" "vac neighbour" "census run" "census wrong" "census zero" "disasm total" "cand session" "cr parsed" "sh63 rldicl" "sh32 rldicl" "rc cr0"; do
        check "ppc_rldicl row: $v" "$(count "$RLCLOG" "^$v  .*ok$")" "1"
    done
    rlcok=$(count "$RLCLOG" " ok$"); rlcbad=$(count "$RLCLOG" " FAIL$"); rlcrun=$((rlcok + rlcbad))
    check "ppc_rldicl rows run"   "$rlcrun" 24
    check "ppc_rldicl rows green" "$rlcok" 24
    check "ppc_rldicl rows red"   "$rlcbad" 0
    #  EVERY SCORE line is counted, then the one is read: counting only `SCORE 24/24' lines let an
    #  appended contradictory `SCORE 0/24' pass (GPT-6 Astra, pass 1).
    check "ppc_rldicl score lines"  "$(grep -c '^SCORE ' "$RLCLOG")" "1"
    check "ppc_rldicl score 24/24"  "$(grep -c '^SCORE 24/24 ' "$RLCLOG")" "1"
fi

need_file "$IMAGES/netbsd401-macppc-GENERIC"

note "binary : $PMAX"
note "machine: macppc/G4, NetBSD kernel loaded so the machine constructs; never executed"
note "cold debugger; big-endian (dump renders value order); msr=0x2000 required for FP"

python3 ppc_rounding_probe.py "$PMAX" "$IMAGES" > "$LOG" 2>&1 || true

if ! grep -q "PPC_CONV_RESULT=" "$LOG"; then
    note "probe produced no result line; last lines follow"
    tail -5 "$LOG" | sed 's/^/       /'
    gate_skip "probe did not complete"
fi

grep -E " ok$| FAIL$" "$LOG" | sed 's/^/       /'

# A probe whose control row failed has measured NOTHING, and no other row may be
# believed -- this harness has been bitten by a probe that reported a defect off
# sentinel reads while its guest code had never run.
ctrl=$(grep -o "PPC_CONV_CONTROL=[A-Z]*" "$LOG" | tail -1 | cut -d= -f2)
check "control rows prove the probe measures" "${ctrl:-missing}" "OK"

# The rounding-mode WRITE channel is proven once per mode, in its own sessions, by
# reading FPSCR back through the guest's own mffs. Both numbers are asserted, because
# "0 bad" is also what a probe reports when it never read FPSCR at all: the first
# version parsed the debugger's plain `reg`, which does not print FPSCR on this CPU,
# so the check passed vacuously on every run until a diff-review seat predicted the
# hole and the rewrite measured it (43 rows of "unparsed").
modebad=$(grep -o "PPC_CONV_MODEWRITES_BAD=[0-9]*" "$LOG" | tail -1 | cut -d= -f2)
modereads=$(grep -o "PPC_CONV_MODEREADS=[0-9]*" "$LOG" | tail -1 | cut -d= -f2)
check "every rounding-mode write took"    "${modebad:-missing}"   "0"
check "all four modes read back by guest" "${modereads:-0}"       "4"

res=$(grep -o "PPC_CONV_RESULT=[0-9]*/[0-9]*" "$LOG" | tail -1 | cut -d= -f2)
got=${res%/*}; want=${res#*/}
check "rows run"     "$want" 138
check "rows correct" "$got"  "$want"

# The table must keep enough of each class to be worth running: a gate whose rows are
# all pins cannot detect a reverted fix, and one with no pins cannot detect collateral
# damage. Both counts are asserted rather than trusted.
disc=$(grep -c " DISC " "$LOG")
pins=$(grep -c " PIN " "$LOG")
# Both floors are set to the ACTUAL counts, not below them. They had drifted to 47/26
# against real counts of 50/36, which means a whole class could have lost rows without
# the floor noticing -- the same "a check that cannot fail" species this gate's header
# warns about twice. The two numbers must also sum to the asserted `rows run` above
# (94 + 44 = 138); if they stop summing, a row lost its class rather than the table
# losing a row.
# #335 added two DISC (fmadd/fmsub fusion) and one PIN (the 2by3+1 control that
# proves the hand-assembled A-form register fields land where intended).
check_min "discriminating rows present" "$disc" 94
check_min "pinned rows present"         "$pins" 44

# The one row that records a divergence this round deliberately does NOT fix.
div=$(grep -c " DIV " "$LOG")
# #325 retired the one DIV row this gate carried: fctiwz of a NaN answered zero,
# and now answers the most negative value the ISA owes. The count is asserted at
# zero rather than the check being deleted -- a gate that stops counting a class
# stops noticing when a member of it reappears.
check "divergence rows recorded" "$div" 0

# Named rows, one per contract, so a single site reverting cannot hide behind a total.
#
# The pattern demands TWO spaces after the name, not one: the probe pads names to a
# fixed column, so a name that is a PREFIX of another ("frsp qNaN" of "frsp qNaN
# payload") matched both rows and the check counted 2 where it wanted 1. A check that
# counts the wrong rows is the same species as a check that cannot fail -- it was
# passing for the wrong reason the moment the table grew a longer name.
for v in "frsp qNaN" "frsp sNaN" "frsp 1+3ulp/2 RZ" "frsp band RP" "frsp band- RM" \
         "frsp tiny RP" "frsp 2^128 RZ" "frsp carry-up RZ" \
         "stfs 2^-127" "stfs band tail" "stfs band-" "stfsx 2^-127" \
         "stfs qNaN payload" "stfs sNaN passthrough" "stfsx qNaN payload" \
         "lfs qNaN-" "composed frsp->stfs NaN" "lfsx qNaN-" "VXSNAN sticky" \
         "fctiwz qNaN" "fctiwz -qNaN" "fctiwz 1.0 control" \
         "fctiwz +Inf" "fctiwz -Inf" "fctiwz 2^31" "fctiwz -(2^31+1)" \
         "fctiwz 1.9 RTZ" "fctiwz -1.9 RTZ" \
         "VXISI fadd Inf-Inf" "VXIDI fdiv Inf/Inf" "VXZDZ fdiv 0/0" \
         "VXIMZ fmul Inf-by-0" "ZX fdiv 1/0" "VXSNAN fadd sNaN" \
         "VXSNAN fcmpu sNaN" "VXCVI fctiwz sNaN" "VXCVI fctiwz qNaN" \
         "clean fadd qNaN" "clean fadd Inf+Inf" "clean fdiv Inf/0" \
         "mtfsf FM=0xff" "mtfsf FM=0x80" "mtfsf FM=0x01" "mtfsf FM=0x0f" \
         "mtfsf FM=0x40" "mtfsf clears" \
         "VX falls on last clear" "VX rises on cause" \
         "FEX rises on enable" "FEX falls with its cause" \
         "FEX order: enable first" "FEX order: cause first" \
         "FX latches once only" \
         "lfsu value" "lfsu updates r3" "lfdu value" "lfdu updates r3" \
         "stfsu value" "stfsu updates r3" "stfdu value" "stfdu updates r3" \
         "fmadd fused 1+-2^-52" "fmsub fused 1+-2^-52" "fmadd 2by3+1 control" \
         "VXIMZ+VXSNAN fmadd" "VXIMZ fmadd Inf-by-0" "VXSNAN fmadd sNaN" \
         "VXISI fmadd Inf+-Inf" "clean fmadd Inf+Inf" \
         "VXISI fmsub Inf-Inf" "clean fmsub Inf--Inf" "clean fmadd 2by3+1" \
         "VXIMZ fmadd 0-by-Inf" "VXSNAN fmadd frC" "VXIMZ fmadd qNaN addend" \
         "VXIMZ not VXISI" "VXISI fmadd neg product" \
         "fnmadd 2by3+1 = -7" "fnmsub 2by3-1 = -5" \
         "fadd RZ mode ignored" "fadd RN control" \
         "lfsux value" "lfsux updates r3" "lfdux value" "lfdux updates r3" \
         "stfsux value" "stfsux updates r3" "stfdux value" \
         "stfdux updates r3" "lfs leaves r3" "lfsx leaves r3"; do
    n=$(count "$LOG" "^$v  .*ok$")
    check "  row: $v" "$n" 1
done

# The pins that record a DELIBERATE divergence from the letter of the ISA.
for v in "stfs 2^129 policy" "stfs 3\*2^128 policy" "frsp 2^128 RN"; do
    n=$(count "$LOG" "^$v .*ok$")
    check "  policy pin: $v" "$n" 1
done

gate_end
