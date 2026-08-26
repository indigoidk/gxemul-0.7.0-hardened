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
check "halt rows run"     "$hwant" 34
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
# *** THIS BLOCK USED TO PIN THE OPPOSITE OF THE MANUAL, and it said so plainly:
# "a build that judged this access as a read would complete the copy and fail
# this row alone."  It would have.  Corrected in #454. ***
#
# SH7750 Hardware Manual Rev.7.00 4.7.4 "SQ Protection", p. 144 --
# `_scratchpad/sh7750_hardware.txt:11744-11746`, identically in the SH-4
# programming manual 4.6.4 at `sh4_programming.txt:3561-3563`:
#
#     "Write type exception judgment is performed for writes to the SQs, and
#      read type for transfer from the SQs to external memory (PREF
#      instruction), and a TLB miss exception, protection violation exception,
#      or initial page write exception is generated."
#
# Quoted in full because these rows were previously pinned to a panel VERDICT
# rather than to a document, and a future seat must be able to re-derive them
# without trusting this round.  The manual was not in the tree when they were
# first pinned; it is now.
#
# So `sq pr00 rdok` and `sq d0 rdok` FLUSH: privileged read is permitted by
# PR=00 and is indifferent to D.  The three `evt` rows carry the exception
# channel, which is the only channel that can see the change once the copy
# completes either way -- and MEASURED, two one-token mutants scored full marks
# without them, one of which lands the payload at PHYSICAL ZERO in silence.
# The two `itlb` rows kill FLAG_INSTR, which escapes the value rows AND the
# EXPEVT rows because it also yields 0x040.
#
# *** `sq at0 qacr` WAS CALLED "the regression guard: the QACR composition must be
# exactly as before".  MEASURED FALSE in #454 -- the composition can be DELETED
# OUTRIGHT and that row stays green. ***  It pins `addr & 0x03ffffe0` and nothing
# more.  Two structural reasons, neither of them bad luck: no row in the probe ever
# wrote QACR0 or QACR1 and dev_sh4.c seeds them nowhere, so the term under test was
# identically ZERO in every row; and every SQ operand had bit 5 SET, so `sq_nr` was
# 1 in all ten rows and QACR0 was never the register consulted, ever.
#
# The three `sq qacr*` rows are the real guard, and they were added because the
# escape is WITNESSED guest-visible corruption rather than a hypothesis: with AT=0,
# the ordinary store-queue mode without paging, the destination AREA comes entirely
# from QACR, so dropping the term or swapping the two registers lands 32 bytes on
# the wrong physical page.  Measured 34/34 on the fix, 31/34 on each mutant.
#  Row names are capped at 13 CHARACTERS and that is not cosmetic: the probe
#  prints them through %-14s and this pattern demands two spaces after the name,
#  so a 14-character name leaves ONE and the check becomes unsatisfiable -- it
#  counts 0 against an expected 1 and reddens for a reason unrelated to the code.
#  Two of #454's first-draft names broke it.  Measure after any rename.
for v in "sq at1 ok" "sq at1 miss" "sq pr00 rdok" "sq d0 rdok" "sq miss evt" "sq pr00 evt" "sq d0 evt" "sq itlb utlb" "sq itlb decoy" "sq qacr1 dst" "sq qacr1 neg" "sq qacr0 sel" "sq at0 qacr"; do
    n=$(count "$HLOG" "^$v  .*ok$")
    check "  round 81: $v" "$n" 1
done

for v in "movca.l" "fmovd @r1" "fmovd @r2" "fmovd xd st" "fmovd xd ld" \
         "fmovd r0idx" "fmovs SZ=0" "fsrra PR=1" "fneg odd PR=1" \
         "fabs odd PR=1" "fp in slot" "trapa in slot"; do
    n=$(count "$HLOG" "^$v  .*ok$")
    check "  round 80: $v" "$n" 1
done

# ---- #457: a UTLB associative write matching two entries ended the host -------
#  Wired in the SAME commit as the fix, per gate 6's structural note.
#
#  SIX ROWS, and two of them exist because a survival-only oracle was MEASURED
#  passing six different mutants.  `expevt` + `pc` kills four of them; the other two
#  need rows nothing else provides:
#    * `tlbm sr` pre-sets SR to 0x40008000 so the reset transition's THIRD statement
#      is observable.  From the reset-default SR that statement is a NO-OP, which is
#      why an arm that sets pc and vbr and forgets it passes every other row.
#    * `tlbm single` gives entry 1 a different VPN so nothing should fire.  It is the
#      only row that sees a `n_hits >= 1` mutant, and it doubles as the liveness
#      control -- it proves the three stores execute and the session survives them.
#
#  landisk and not testsh, deliberately: landisk's PROM leaves vbr = 0x8c000000, so
#  `vbr == 0` is a real transition.  On testsh vbr is already 0 and that row would be
#  vacuous.
TMLOG=$LOGDIR/gate_sh_tlbmulti.log
#  *** -u ON ALL SIX PROBES IN THIS GATE. ***  `probeslow` recorded the streaming
#  mitigation as APPLIED and called it "the general fix" -- and it had been applied to
#  NONE of them: the -u lived only in ad-hoc measurement scripts.  These six are exactly
#  the six probes `probetimebased` names as having no prompt detection, so they are also
#  the six whose runs are longest and most worth not losing.  Redirected to a file,
#  stdout is block buffered and a killed run loses everything it had already measured.
python3 -u sh_tlbmulti_probe.py "$PMAX" "$KERNEL" > "$TMLOG" 2>&1 || true

if ! grep -q "SH_TLBMULTI_RESULT=" "$TMLOG"; then
    note "sh_tlbmulti probe produced no result line; last lines follow"
    tail -5 "$TMLOG" | sed 's/^/       /'
    check "sh_tlbmulti probe completed" "no" "yes"
else
    grep -E " ok$| FAIL$" "$TMLOG" | sed 's/^/       /'
    tmctrl=$(grep -o "SH_TLBMULTI_CONTROL=[A-Z]*" "$TMLOG" | tail -1 | cut -d= -f2)
    check "sh_tlbmulti control proves it measures" "${tmctrl:-missing}" "OK"
    tmres=$(grep -o "SH_TLBMULTI_RESULT=[0-9]*/[0-9]*" "$TMLOG" | tail -1 | cut -d= -f2)
    check "sh_tlbmulti rows run"     "${tmres#*/}" 6
    check "sh_tlbmulti rows correct" "${tmres%/*}" "${tmres#*/}"
    for v in "tlbm alive" "tlbm expevt" "tlbm pc" "tlbm vbr" "tlbm sr" "tlbm single"; do
        n=$(count "$TMLOG" "^$v  .*ok$")
        check "  $v" "$n" 1
    done
fi

# ---- #455: an interrupt at priority 0 ended the host process -----------------
#  Wired in the SAME commit as the fix.  Gate 6's structural note says a probe that
#  ships with its wiring cannot skip its census pin, because the wiring forces a
#  gate run -- #441's did not, and its pin then went latently red between two
#  commits.
#
#  This probe drives BOTH SH rigs, and which row uses which is forced rather than
#  stylistic.
#
#  The PRIMARY witness is `-E testsh`, where the kill is reached SYNCHRONOUSLY --
#  one guest store to the mp device's IPI register -- because the test machine wires
#  its whole interrupt tree to a line the priority loop never assigns.  Being
#  synchronous is what lets a cheap `step` see it.
#
#  The SECONDARY rows (`prio0 tmu`, `prio0 tmuq`) drive the landisk TMU route and
#  must FREE-RUN, because a TMU underflow is produced by a HOST timer and
#  debugger.c stops those for the duration of a `step`.  They exist because a
#  MEASURED mutant that repaired only the testsh route scored full marks without
#  them.  See the probe header.
IPLOG=$LOGDIR/gate_sh_intprio.log
python3 -u sh_intprio_probe.py "$PMAX" "$KERNEL" > "$IPLOG" 2>&1 || true

if ! grep -q "SH_INTPRIO_RESULT=" "$IPLOG"; then
    note "sh_intprio probe produced no result line; last lines follow"
    tail -5 "$IPLOG" | sed 's/^/       /'
    check "sh_intprio probe completed" "no" "yes"
else
    grep -E " ok$| FAIL$" "$IPLOG" | sed 's/^/       /'
    ipctrl=$(grep -o "SH_INTPRIO_CONTROL=[A-Z]*" "$IPLOG" | tail -1 | cut -d= -f2)
    check "sh_intprio control proves it measures" "${ipctrl:-missing}" "OK"
    ipres=$(grep -o "SH_INTPRIO_RESULT=[0-9]*/[0-9]*" "$IPLOG" | tail -1 | cut -d= -f2)
    check "sh_intprio rows run"     "${ipres#*/}" 7
    check "sh_intprio rows correct" "${ipres%/*}" "${ipres#*/}"
    #  Named individually, and every one earns its place against a MEASURED mutant.
    #  `tmu`/`tmuq` (#455) kill a PARTIAL FIX that repairs only the route the witness
    #  drives -- measured passing 4/4 before they existed -- and they carry #455's
    #  priority-0 coverage now that #456 moved the testsh line off priority 0.
    #  `accept` (#455) is the de-escalation clause's cost: it pins that a LEGAL
    #  priority-1 interrupt is still delivered, and is the only row that reddens
    #  under `if (prio <= 1) return;` (measured 6/7).
    #
    #  `irq14 deliv` / `irq14 imask` (#456) REPLACED #455's `prio0 kill`/`prio0 quiet`,
    #  which #456 made vacuous -- silently, since they stayed green.  They kill
    #  DIFFERENT families and neither covers the other's: reverting to IRQ15 is caught
    #  by `deliv` alone (6/7), while IRQ13 and IRQ0 both still DELIVER and are caught
    #  by `imask` alone (6/7 each), because only bracketing IMASK pins the level to
    #  exactly 1.
    for v in "irq14 deliv" "irq14 imask" "prio0 live" "prio0 devsig" "prio0 tmu" "prio0 tmuq" "prio0 accept"; do
        n=$(count "$IPLOG" "^$v  .*ok$")
        check "  $v" "$n" 1
    done
fi

# ------------------------------------------------------------------ #458 sh4_iprbcd
#  sh_update_interrupt_priorities() read two of the four IPR registers, and took SCIF
#  from INTPRI00 -- an SH7750R/SH7760 register this machine never even MAPS, so SCIF's
#  priority was a guest-immutable 3 while the boot witness shows OpenBSD asking for 12.
#
#  Two of these rows read the priority TABLE rather than a delivery, and that is not
#  decoration: WDT, REF, SCI, GPIO, DMAC, H-UDI and RTC have NO `INTERRUPT_ASSERT`
#  anywhere in this tree, so a mutant dropping their mapping scores a clean 10/10
#  against every behavioural row that can be written.  Nothing a guest can DO depends
#  on those priorities -- only what the table SAYS.
IBLOG=$LOGDIR/gate_sh_iprbcd.log
python3 -u sh_iprbcd_probe.py "$PMAX" "$KERNEL" > "$IBLOG" 2>&1 || true

if ! grep -q "IPRBCD_RESULT=" "$IBLOG"; then
    note "sh_iprbcd probe produced no result line; last lines follow"
    tail -5 "$IBLOG" | sed 's/^/       /'
    check "sh_iprbcd probe completed" "no" "yes"
else
    grep -E " ok$| FAIL$" "$IBLOG" | sed 's/^/       /'
    ibctrl=$(grep -o "IPRBCD_CONTROL=[A-Z]*" "$IBLOG" | tail -1 | cut -d= -f2)
    check "sh_iprbcd control proves it measures" "${ibctrl:-missing}" "OK"
    ibres=$(grep -o "IPRBCD_RESULT=[0-9]*/[0-9]*" "$IBLOG" | tail -1 | cut -d= -f2)
    check "sh_iprbcd rows run"     "${ibres#*/}" 18
    check "sh_iprbcd rows correct" "${ibres%/*}" "${ibres#*/}"
    #  `naive` is pinned deliberately as a LABELLED row: writing one IPR and expecting
    #  delivery is GREEN on the unfixed build, so it fails vacuity floor clause (a).  It
    #  ships so nobody re-invents it; `iprc_hi`/`iprc_lo`/`iprc_lo1` are what discriminate,
    #  by BRACKETING IMASK -- delivery needs IMASK < int_level, so a pair of rows at two
    #  IMASK values pins the level to a range instead of to "nonzero".
    #
    #  `iprb wdt` / `ipra rtc` are the two table-reading rows.  MEASURED: dropping the
    #  IPRB+RTC mapping reddens THESE TWO AND NOTHING ELSE (10/12 -- a TWELVE-ROW-ERA
    #  number, measured before the iprd pair was added), and dropping only the
    #  three RTC lines reddens `ipra rtc` alone.  Without them the settings exposure
    #  added by #458 would be an unused convenience.
    #
    #  `raise` isolates the rescan half: it is the only row red on an IPR-only build.
    #
    #  `iprd hold` / `iprd ctl` defend the round's central DECISION rather than its
    #  code.  #458 declines to read IPRD, and a pass-2 seat observed that the decision
    #  lived only in a comment: the obvious "read all four registers per Table 19.6"
    #  completion scored a clean pass against every other row while masking four landisk
    #  PCIC lines.  MEASURED, not predicted -- `m_iprdread` (apply IPRD's nibbles to
    #  IRL0-3) scores 13/14, red on `iprd hold` ALONE.  A guest `IPRD := 0` must leave
    #  IRQ2/IRL0 (0x240) at 0xd; IRQ10 (0x340) is outside IPRD and stays 0x5 under fix
    #  and mutant alike, which is what makes the red attributable to IPRD rather than to
    #  a broken session.
    #
    #  *** `scif eri/rxi/bri/txi` ARE THE ONE ESCAPE THAT WAS NOT COVERAGE DEBT. ***
    #  A measuring seat narrowed the IPRC SCIF loop to TXI alone -- one identifier --
    #  and MEASURED 14/14.  Unlike every other escape this round, that one reaches a
    #  LIVE line: SCIF RXI (0x720) is asserted by dev_sh4.c:250-256 on RIE && DR and
    #  connected at :1912, which is CONSOLE INPUT on landisk.  Measured, the mutant
    #  leaves iprio_720 at priority 0 with the line asserted, and RX delivery at
    #  IMASK=3 goes from delivered to refused -- console input silently deleted, gate
    #  green.  The ten behavioural rows all drive TXI, so nothing saw the RX side.
    #  These four pin the loop's WHOLE membership, killing every narrowing of it.
    for v in "live" "devsig" "naive" "iprc_hi" "iprc_lo" "iprc_lo1" \
             "raise" "raise_lo" "lower" "deassert" "iprb wdt" "ipra rtc" \
             "iprd hold" "iprd ctl" "scif eri" "scif rxi" "scif bri" "scif txi"; do
        n=$(count "$IBLOG" "^$v  .*ok$")
        check "  $v" "$n" 1
    done
fi

# ------------------------------------------------------------------ #459 sh4_pclock
#  ONE ORDINARY GUEST STORE to 0xffd80010 ended the host process on every SH machine
#  whose board never assigned a peripheral clock.  cpu_sh.c:233-234 adds the sh4 device
#  from `arch == 4`, so the CPU brings the TMU and the BOARD brings the clock, and
#  nothing checked that the two agree.  MEASURED dead on THREE machine types --
#  -e jornada680, -E baresh and -E testsh -- while dreamcast and landisk, the only two
#  that assign pclock, were fine.
#
#  This gate section is the de-escalation clause's cost, paid in full.  #459 removed a
#  host-fatal guard, which DELETES the accidental tripwire that made the behaviour
#  self-announcing, so the rows below rebuild it deliberately on both sides.
PCLOG=$LOGDIR/gate_sh_pclock.log
python3 -u sh_pclock_probe.py "$PMAX" "$KERNEL" > "$PCLOG" 2>&1 || true

if ! grep -q "SH_PCLOCK_RESULT=" "$PCLOG"; then
    note "sh_pclock probe produced no result line; last lines follow"
    tail -5 "$PCLOG" | sed 's/^/       /'
    check "sh_pclock probe completed" "no" "yes"
else
    grep -E " ok$| FAIL$" "$PCLOG" | sed 's/^/       /'
    pcctrl=$(grep -o "SH_PCLOCK_CONTROL=[A-Z]*" "$PCLOG" | tail -1 | cut -d= -f2)
    check "sh_pclock control proves it measures" "${pcctrl:-missing}" "OK"
    pcres=$(grep -o "SH_PCLOCK_RESULT=[0-9]*/[0-9]*" "$PCLOG" | tail -1 | cut -d= -f2)
    check "sh_pclock rows run"     "${pcres#*/}" 16
    check "sh_pclock rows correct" "${pcres%/*}" "${pcres#*/}"
    #  THREE machines, because the brief that opened the round said two.  Two pass-1
    #  seats independently caught that machine_test.c:535 is MACHINE_DEFAULT_CPU(baresh),
    #  not testsh -- so `baresh kill`/`baresh diag` pin a machine the round nearly missed.
    #
    #  `accept hz` / `accept dc hz` use TWO DIFFERENT CLOCK VALUES on purpose.  A single
    #  row pinned at landisk's 33.33 MHz is passed by a mutant that HARDCODES 33333333
    #  in place of cpu->cd.sh.pclock; dreamcast's 50 MHz is the discriminator, and no
    #  hardcode satisfies both.  (dreamcast needs -x or it exits before the debugger
    #  prompt -- two console inputs, console.c:994-1007.  Its first draft read "died",
    #  the SAME STRING the trigger rows produce, which would have been scored as a
    #  fourth reproduction.  The probe passes -x for that machine only.)
    #
    #  The last four are the rebuilt tripwire and none is decoration.  Without them a
    #  mutant that declines SILENTLY passes every other row: `says` pins that the
    #  refusal names itself, `once` that the same timer twice yields ONE line, `pertmr`
    #  that TCR0 and TCR1 yield TWO (the latch instance is per-timer, not shared), and
    #  `unlatch` that the refused write does NOT land -- #447's own comment cites that
    #  read-back as how "the guest can see the rejection", so it is the guest's channel
    #  where the diagnostic is the operator's.
    for v in "live" "devsig" "hpcsh kill" "hpcsh diag" "baresh kill" "baresh diag" "testsh kill" "testsh diag" "accept hz" "accept tcr" "accept dc hz" "accept dc tcr" "hpcsh says" "hpcsh once" "hpcsh pertmr" "hpcsh unlatch"; do
        n=$(count "$PCLOG" "^$v  .*ok$")
        check "  $v" "$n" 1
    done
fi

# ------------------------------------------------------------------ #460 gdrom_data
#  FOUR guest-reachable exit(1) sites in ONE register's access arm.  `cond` and `busy`
#  are both zero on a fresh device, so THERE WAS NO LEGAL FIRST TOUCH of GDROM_DATA:
#  any non-16-bit access in either direction, the first 16-bit read, and the first
#  16-bit write each ended the host process.  Measured 5/23 pre-fix, 23/23 post-fix,
#  the pre-fix build rebuilt from `git show HEAD:` and not from build/.
#
#  Dreamcast needs -x or it exits before the debugger prompt (two console inputs,
#  console.c:994-1007).  Without it a session dies for a CONFIGURATION reason and
#  prints the same "died" the defect prints -- that cost #459 a false positive.
GDLOG=$LOGDIR/gate_gdrom_data.log
python3 -u gdrom_data_probe.py "$PMAX" "$KERNEL" > "$GDLOG" 2>&1 || true

if ! grep -q "GDROM_RESULT=" "$GDLOG"; then
    note "gdrom_data probe produced no result line; last lines follow"
    tail -5 "$GDLOG" | sed 's/^/       /'
    check "gdrom_data probe completed" "no" "yes"
else
    grep -E " ok$| FAIL$" "$GDLOG" | sed 's/^/       /'
    gdctrl=$(grep -o "GDROM_CONTROL=[A-Z]*" "$GDLOG" | tail -1 | cut -d= -f2)
    check "gdrom_data control proves it measures" "${gdctrl:-missing}" "OK"
    gdres=$(grep -o "GDROM_RESULT=[0-9]*/[0-9]*" "$GDLOG" | tail -1 | cut -d= -f2)
    check "gdrom_data rows run"     "${gdres#*/}" 23
    check "gdrom_data rows correct" "${gdres%/*}" "${gdres#*/}"
    #  THE `x1` COUNT ROWS ARE THE POINT, not the survival rows.  The first oracle
    #  asserted the OLD fatal text must be ABSENT -- but the fix KEEPS the diagnostic
    #  and drops only exit(1), so DELETING the whole register arm scored 13/13 while
    #  the real fix scored 8/13.  Re-pinned to "the diagnostic appears EXACTLY ONCE":
    #  pre-fix dies, the fix says it once, a deleted arm says it zero times.
    #
    #  THE LOAD VARIANTS ARE LOAD-BEARING.  A rebuild once wrapped the width rows
    #  around stores only, and a seat named the mutant that walks that gap: restore
    #  exit(1) on WRONG-WIDTH READ ONLY, which scored a clean 14/14 while one guest
    #  MOV.B read from the register still ended the host.
    #
    #  `two sites x2` is the ONLY row separating a per-site latch from ONE SHARED
    #  BIT; every other row drives one site per session and cannot see the axis.
    #
    #  `accept d0`/`accept d1` are the de-escalation accept for four removed
    #  predicates -- a legal TOC PIO returning 0x0010 then 0xffff9600 (mov.w
    #  sign-extends, and 0x9600 has bit 15 set).  Without them, a mutant that strips
    #  the whole success path scores full marks.  `declined val` pins what a DECLINED
    #  read returns; without it 0xffff -> 0 passes while the diagnostic claims 0xffff.
    for v in "live" "devsig" "gdrom map" "w8 store" "w8store x1" "w32 store" "w32store x1" "w8 load" "w8load x1" "w32 load" "w32load x1" "w16 load" "w16load x1" "w16 store" "w16store x1" "two sites" "two sites x2" "accept d0" "accept d1" "declined val" "overread" "overread x1" "accept w8"; do
        n=$(count "$GDLOG" "^$v  .*ok$")
        check "  $v" "$n" 1
    done
fi

# --------------------------------------------------------------- #461 gdrom_default
#  dev_dreamcast_gdrom.c registers a 0x100 window and implements EIGHT offsets; every
#  other address fell to a `default:` arm that printed then exit(1)ed -- a read OR a
#  write, at any width.  MEASURED: 21 offsets sampled, 19 died.  One predicate, roughly
#  248 of 256 byte offsets lethal, so a driver scanning the register space died on its
#  first unhandled address.  The DMA window's own default arm joined the round on a
#  measurement: it died on committed HEAD AND on a build that fixed only the control
#  window.  *** 9/32 pre-fix, 32/32 post-fix, both measured AT 32 ROWS (pre461f.out).
#  ***
#
#  This line asserted `8/32 ... BOTH MEASURED` before that run existed, and the carried
#  8 was wrong as well as unmeasured -- the real figure is 9, because `dma accept`
#  reads five IMPLEMENTED DMA offsets and those work on the pre-fix build.  A seat
#  predicted 9 from the code and the measurement returned it.  Hence the carrier rule
#  that a score claim names its log: section U checks the DENOMINATOR against this
#  file's own pin, and nothing can check a NUMERATOR that was never run.
#
#  This line said "7/27 pre-fix, 27/27 post-fix -- both MEASURED at the final row
#  count, not carried over" while citing the earlier carried-over incident as the
#  thing it had learned from.  A seat found it FALSE THREE WAYS: the final count is
#  32, not 27; NO 7/27 measurement ever existed (the runs on record are 7/21, 7/25
#  and 8/32); and the honest pre-fix number is 8, not 7, because `dma seed` passes
#  pre-fix -- the implemented +0x04 always worked.
#
#  Third generation of the frozen-number defect, inside the sentence memorialising
#  the first two.  Section U now checks the DENOMINATOR against this file's own pin
#  mechanically; the NUMERATOR and the word "measured" still cannot be checked by
#  anything but a reader, which is exactly how this one survived.
#  after the probe had grown to 25, which is the stale-score class a seat caught
#  mid-answer and section U now checks mechanically.
GDDLOG=$LOGDIR/gate_gdrom_default.log
#  -u IS LOAD-BEARING.  `probeslow` recorded the streaming mitigation as APPLIED;
#  it was applied only in ad-hoc measurement scripts, never HERE -- and this is
#  the invocation that runs weekly.  Redirected to a file, stdout is block
#  buffered and the probe (no flush anywhere, a few KB of output) loses EVERY
#  row if the run is killed.  A killed run then looks like a run that produced
#  nothing, which is the silence this row was filed about.
python3 -u gdrom_default_probe.py "$PMAX" "$KERNEL" > "$GDDLOG" 2>&1 || true

if ! grep -q "GDROM_DEF_RESULT=" "$GDDLOG"; then
    note "gdrom_default probe produced no result line; last lines follow"
    tail -5 "$GDDLOG" | sed 's/^/       /'
    check "gdrom_default probe completed" "no" "yes"
else
    grep -E " ok$| FAIL$" "$GDDLOG" | sed 's/^/       /'
    gddctrl=$(grep -o "GDROM_DEF_CONTROL=[A-Z]*" "$GDDLOG" | tail -1 | cut -d= -f2)
    check "gdrom_default control proves it measures" "${gddctrl:-missing}" "OK"
    gddres=$(grep -o "GDROM_DEF_RESULT=[0-9]*/[0-9]*" "$GDDLOG" | tail -1 | cut -d= -f2)
    check "gdrom_default rows run"     "${gddres#*/}" 58
    check "gdrom_default rows correct" "${gddres%/*}" "${gddres#*/}"
    #  `scan uniq` IS AN IDENTITY ROW: 64 word keys minus 8 implemented offsets is
    #  exactly 56.  A ninth implemented register moves it to 55 in the same commit --
    #  the fail-closed ratchet, equality and not >=.  It kills a capped counter (4 !=
    #  56), a masked key (32 != 56), AND the raw-address indexing mutant (measured
    #  18/21 -- it reddens `scan uniq` too).
    #
    #  *** AN EARLIER DRAFT OF THIS COMMENT SAID THE SCAN CANNOT SEE THE
    #  RAW-ADDRESS MUTANT, 56/56 IDENTICAL TO CORRECT. That was the pass-1
    #  analysis of a design WITHOUT the bounds guard, and the round's own kill
    #  table refutes it. ***  With the guard, raw indexing pushes k to 255
    #  against 64 keys, the guard rejects, most offsets never report, and the
    #  count drops.  A seat caught the comment still carrying the pre-guard
    #  number beside a table that measured otherwise.
    #
    #  `granularity` is the one that does: at 4-byte stride byte- and word-indexing
    #  give equally many distinct keys, so only a SUB-WORD access exposes it.  That
    #  `granularity` pins the per-word keying directly, which is a DESIGN COMMITMENT
    #  worth one access.
    #
    #  *** THREE CLAIMS STOOD HERE AND A SEAT REFUTED ALL THREE. ***
    #
    #  It said the raw-address mutant "lands five words past the array, directly on
    #  dma_reg[], setting the two fields that authorise a DMA transfer".  A guardless
    #  bits[k] reaches dma_reg[0..3] -- count, destination and length -- but NOT
    #  dma_reg[5], the ENABLE, which needs word index 11 against a reachable maximum
    #  of 9.  Three of four, and the overreach is 4 words for the read row, 6 for the
    #  write row.  It also stated the landing in the INDICATIVE, as something that
    #  happens -- the shipped guard prevents any landing at all; it is a property of
    #  the guardless counterfactual only.
    #
    #  It said that re-opens "a host kill that is otherwise unreachable".  Both DMA
    #  +0x18 exits are reachable on the SHIPPED build through the front door: write
    #  count=1 at +0x0c and enable=1 at +0x14, both implemented cases, then any
    #  nonzero store to +0x18.
    #
    #  And it said "SHIP BOTH; neither subsumes the other, and that was measured".
    #  The measurement says the opposite: across six mutants `scan uniq` kills every
    #  one that anything kills, and `granularity`'s only kill (m_oob) reddens
    #  `scan uniq` too, at 15 against 56.  SHIP BOTH ANYWAY -- but because the
    #  granularity row states a commitment cheaply, not because it is a sole killer.
    #  scored a perfect 16/16 before it existed -- including DELETING case GDROM_DATA,
    #  which silently undoes #460.  Before this fix, deleting a case meant exit(1) on
    #  first use; after it, silently wrong forever.
    #
    #  `rd then wr` expects TWO.  Three seats voted that the read/write split was
    #  padding; a build measured offset-only keying producing ZERO write diagnostics
    #  across 31 offsets, because the read pass latches every offset first.
    #  *** THIS LIST HAD 27 NAMES AGAINST 32 ROWS, AND THE FIVE MISSING ONES WERE
    #  THE HIGHEST-VALUE ROWS IN THE FILE. ***  A seat noticed that #460's gate
    #  names all 23 of its rows while this one silently stopped at the pass-1 set --
    #  so `dma alias x1`, `dma align16`, `dma rdleak`, `both windows` and
    #  `dma accept`, every one of them added BECAUSE a mutant escaped, were pinned
    #  by the count check alone.  A row absent from this list still runs; it just
    #  stops being named, so a rename or a silent drop reads as green here.
    #
    #  ONE LINE, deliberately: assembling this with a backslash continuation through
    #  a heredoc mangled TWICE in one session and shipped a red gate with a bogus
    #  word `n` in it.
    for v in "live" "devsig" "impl ok" "rd lo" "rdlo x1" "wr lo" "wrlo x1" "rd hi" "rdhi x1" "rd w16" "rdw16 x1" "same twice" "two offs" "rd then wr" "granularity" "accept cnt" "accept cond" "scan" "scan uniq" "accept8" "data 0xffff" "dma rd" "dma rd x1" "dma two" "dma shadow" "dma seed" "dma alias" "dma alias x1" "dma align16" "dma rdleak" "both windows" "dma accept" "arm survive" "arm says" "arm idle" "arm once" "nodata live" "nodata says" "accept dma" "accept idle" "accept quiet" "nodata quiet" "accept event" "nodata idle" "arm halfarm" "nodata notx" "arm quiet" "arm twice" "nodata len" "arm bytetrig" "accept data" "both decl" "arm count2" "arm enable2" "nodata stale" "stale says" "stale idle" "nodata twice"; do
        n=$(count "$GDDLOG" "^$v  .*ok$")
        check "  $v" "$n" 1
    done
fi

#  ---------------------------------------------------------------- #463
#  asic_badaddr: dev_dreamcast_asic.c ended the host process on a SINGLE
#  guest load.  `r = (relative_addr / 4) & 3` then `exit(1)` when r == 3 --
#  above the switch and above the writeflag test, so no store, no staging
#  and no command sequence was needed.
#
#  THE DENOMINATOR IS 13.  FOUR OF THOSE ROWS EXIST BECAUSE A PANEL FOUND
#  THE FIRST NINE INSUFFICIENT.  `alias`, `alias2` and `crossarr` pin the INDEXING
#  half of the bound on r; the other nine pin the kill and the accept side.
#  They are COMPLEMENTARY on purpose -- neither catches the other's mutant:
#    & 3 -> & 2  aliases +0x14 onto +0x10   -> only `alias` sees it
#    & 3 -> & 7  reaches mask_13[4], which IS mask_11[1] (the struct declares
#                pending_irq[3], mask_13[3], mask_11[3], mask_9[3]
#                CONSECUTIVELY) -> only `crossarr` sees it
#    & 3 -> & 1  aliases +0x18 onto +0x10   -> only `alias2` sees it
#    / 4 -> / 2  aliases +0x18 onto +0x10   -> only `alias2` sees it
#  A same-array distinctness row CANNOT see `& 7`: under it the three mask_13
#  words map to [4],[5],[6], three distinct cells that still round-trip.
#
#  THE UNIT OF COVERAGE IS THE COLLISION PAIR, not "aliasing" in the abstract.
#  Three register words admit distinct pairs and ONE distinctness row pins ONE
#  pair.  `alias` pins words 0 and 1; `& 1` and `/ 2` both collide words 0 and
#  TWO, so it was blind to both until `alias2` was added.  Four seats found
#  these four escapes against a table that was already green.
#
#  -u IS LOAD-BEARING, for the reason the gdrom section above records: with
#  stdout redirected to a file it is block buffered, and a killed run then
#  loses every row and looks like a run that produced nothing.
ASLOG=$LOGDIR/gate_asic_badaddr.log
python3 -u asic_badaddr_probe.py "$PMAX" "$KERNEL" > "$ASLOG" 2>&1 || true

if ! grep -q "ASIC_BADADDR_RESULT=" "$ASLOG"; then
    note "asic_badaddr probe produced no result line; last lines follow"
    tail -5 "$ASLOG" | sed 's/^/       /'
    check "asic_badaddr probe completed" "no" "yes"
else
    grep -E " ok$| FAIL$" "$ASLOG" | sed 's/^/       /'
    asres=$(grep -o "ASIC_BADADDR_RESULT=[0-9]*/[0-9]*" "$ASLOG" | tail -1 | cut -d= -f2)

    #  *** THE PARSE MUST BE CHECKED BEFORE THE SCORE IS READ. ***  Three panel
    #  seats independently found the same false pass here: if the result line
    #  exists but is MALFORMED (no slash, truncated digits), the outer grep -q
    #  still succeeds, `asres` is EMPTY, and then `${asres%/*}` and
    #  `${asres#*/}` BOTH expand to the empty string -- so
    #  `check "rows correct" "" ""` PASSES while nothing was measured.  The
    #  `rows run` sibling would still redden the gate, so this was never a
    #  silent green overall; it was a false GREEN ROW, which is worse than
    #  useless because a reader scanning check output is misled about which
    #  part failed.  This is the project's own "a pattern that matched nothing
    #  reports zero for everything" class, wearing shell-expansion clothes.
    if [ -z "$asres" ]; then
        note "asic_badaddr result line present but unparseable; last lines follow"
        tail -3 "$ASLOG" | sed 's/^/       /'
        check "asic_badaddr result parses" "no" "yes"
    else
        check "asic_badaddr result parses" "yes" "yes"
        check "asic_badaddr rows run"     "${asres#*/}" 13
        check "asic_badaddr rows correct" "${asres%/*}" "${asres#*/}"

        #  Per-row presence.  A row that silently stops being tested is the
        #  padded-column class; every name here is <= 10 chars against the
        #  probe's %-14s column, so the two-space anchor cannot become
        #  unsatisfiable.  The `count "$ASLOG"` on the NEXT line is what
        #  identifies this section -- every section's list opens "live" "devsig".
        #
        #  `alias` IS A PREFIX OF `alias2`, which is the sibling of the
        #  padded-column trap: one name's pattern matching two rows, or none.
        #  CHECKED EMPIRICALLY against probe-formatted lines rather than reasoned
        #  about -- each of alias / alias2 / crossarr matches EXACTLY ONE. The
        #  two-space anchor cannot span the collision because the character after
        #  `alias` is the digit 2, not a space. If a future row is named so that a
        #  SPACE follows an existing name's prefix, re-run that check before
        #  trusting this loop.
        #
        #  *** AND THERE IS A HARD LENGTH BOUND: ROW NAMES MUST BE <= 13 CHARS. ***
        #  The probe's format is "%-14s " -- fourteen columns plus one literal
        #  space -- so a name of length L is followed by (15 - L) spaces.  At L=13
        #  that is two spaces and the anchor still matches; at L=14 it is ONE, the
        #  `^$v  ` anchor can never match, and THE ROW SILENTLY STOPS BEING TESTED
        #  while the gate stays green.  Longest name here is `kill store` (10), so
        #  there are three characters of headroom.  Named by a panel seat, which
        #  computed the threshold rather than just warning about the class.
        for v in "live" "devsig" "asic ok" "safe 8" "kill word" "kill byte" "kill store" "safe 4" "kill far" "alias" "crossarr" "alias2" "mask9 rt"; do
            n=$(count "$ASLOG" "^$v  .*ok$")
            check "asic_badaddr $v" "$n" 1
        done
    fi
fi

#  NOTE ON CHECK NAMING: the sections above use `check "  $v"`, a bare padded
#  row name. Every section has a `live` row, so those names COLLIDE in the
#  gate's own output and a reader cannot tell which section a failing `live`
#  belongs to. This section prefixes with `asic_badaddr` deliberately.

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

# ------------------------------------------------------------------ #447 sh4 value guards
#  A SIBLING OF THE BLOCK ABOVE, NOT AN EXTENSION OF IT -- and the reason is the row title
#  three lines up.  That check is named "sh4_pcic: no offset kills the host".  Folding
#  #447's rows under it would make the gate's own check name UNTRUE, because these are four
#  DIFFERENT sites (TCR, DMATCR, ICR, RCR1) reached by VALUE rather than by offset.  A check
#  whose title does not describe what it checks is the same defect as a green row that means
#  nothing, and it is harder to see because the number still moves.
#
#  WHAT #447 FIXED: four guards in DEVICE_ACCESS(sh4) called exit(1) on a value the model
#  does not implement.  A guest STORE of an unmodelled bit ended the host process.  They now
#  DIAGNOSE AND SURVIVE, latched per (class, INSTANCE, offending BIT) -- three parts, each
#  earned: per-class alone reports timer 0 and silences timers 1-2 and channels 1-7, and
#  per-(class,instance) still swallows the second feature at one register, because RCR1's
#  single guard covers TWO features and TCR's covers SIX.
#
#  THE STORE POSITION DIFFERS THREE WAYS OUT OF FOUR, which is why "move the store below the
#  guard" is not a file-wide rule: DMATCR's store is already downstream, ICR has no store on
#  any path, RCR1's was upstream (the #443 shape), and TCR is a third case -- `timer_hz` is
#  set from `idata & 3` BEFORE the guard, so a naive fix would install pclock/4 for a write
#  asking for a clock source the model cannot provide, turning a loud fault into a silent one.
VALOG=$LOGDIR/gate_sh4_val.log
python3 sh4_val_probe.py "$PMAX" "$KERNEL" > "$VALOG" 2>&1 || true

if ! grep -q "SH4_VAL_RESULT=" "$VALOG"; then
    note "sh4_val probe produced no result line; last lines follow"
    tail -5 "$VALOG" | sed 's/^/       /'
    check "sh4_val probe completed" "no" "yes"
else
    grep -E "^  (ok|FAIL) " "$VALOG" | sed 's/^/       /'
    check "sh4_val: no guest VALUE kills the host"           "$(grep -c 'SH4_VAL_PASS' "$VALOG")" "1"
    #  33, and the floor is pinned because two mutants initially scored 32/32 against an
    #  earlier draft of this probe -- one collapsing all four fault classes into one, one
    #  turning fatal() into debug() at every site.  Both are now killed by single rows, so
    #  a row count that quietly drops is a real loss of coverage rather than tidying.
    check_min "sh4_val: rows actually run"           "$(grep -cE '^  (ok|FAIL) ' "$VALOG")" 33
fi

# ------------------------------------------------------------------ #448 CHCR decoders
#  A THIRD SIBLING, and the same reasoning that kept #447 out of #443's block keeps this
#  out of both: the checks above are named "no offset kills the host" and "no guest VALUE
#  kills the host", and these four sites are reached by neither -- they are CHCR FIELD
#  ENCODINGS decoded inside sh4_dmac_transfer(), on the far side of a call.
#
#  *** THIS WAS EASIER TO REACH THAN ANYTHING #447 REPAIRED. ***  Only `case 0x200:`
#  survives the CHCR_RS switch, so fifteen of the sixteen resource-select encodings ended
#  the host -- and a wholly legal configuration (4-byte transfers, both addresses
#  incrementing) died on its resource-select alone.
#
#  THE ACCEPT-SIDE ROWS (A1-A4) ARE THE DE-ESCALATION CLAUSE, and this is the first round
#  to owe them: a fatal->survive fix DELETES the accidental tripwire that made guard growth
#  self-announcing, so the detector must pin that legal encodings are still ACCEPTED, not
#  merely that illegal ones are declined.  #447 shipped without those rows and a review
#  seat then found a ONE-IDENTIFIER escape scoring full marks.
CHCRLOG=$LOGDIR/gate_sh4_chcr.log
python3 sh4_chcr_probe.py "$PMAX" "$KERNEL" > "$CHCRLOG" 2>&1 || true

if ! grep -q "SH4CHCR_RESULT=" "$CHCRLOG"; then
    note "sh4_chcr probe produced no result line; last lines follow"
    tail -5 "$CHCRLOG" | sed 's/^/       /'
    check "sh4_chcr probe completed" "no" "yes"
else
    grep -E "^  (ok|FAIL) " "$CHCRLOG" | sed 's/^/       /'
    check "sh4_chcr: no guest CHCR ENCODING kills the host"           "$(grep -c 'SH4CHCR_PASS' "$CHCRLOG")" "1"
    #  *** THIS COMMENT WAS CORRUPTED BY A CARELESS sed AND SHIPPED THAT WAY. ***  A
    #  flagship review found it: it said "16" against the floor of 18 one line below, "TWO
    #  rows" against a record of five, "round.s" (the `.` in the pattern matched the
    #  apostrophe), and it spliced two sentences into one that says nothing.  A wrong
    #  record in a committed gate file, caused by editing prose with a regex.
    #
    #  What it should have said: the floor is 18, and FIVE rows were measured vacuous
    #  across this round and rebuilt.  R2 carried the ACCEPTED resource select, so a
    #  `return`->`break` mutant printed one line either way.  L1's second store was a
    #  BIT-SUBSET of its first, so a whole-register latch computed fresh==0 and stayed
    #  silent.  R5 was byte-identical to R4.  R6 proves channel 3 REACHES the guard, not
    #  that the latch DISTINGUISHES channels, so L3 was added.  And R1 had R2's exact
    #  defect, fixed at R2/R3 in the same session and not carried across -- with a comment
    #  left behind claiming it was covered.  A pass-2 seat found that one.
    check_min "sh4_chcr: rows actually run"           "$(grep -cE '^  (ok|FAIL) ' "$CHCRLOG")" 27
fi

# ------------------------------------------------------------------ #449 RTCSR refresh
#  A FOURTH SIBLING, and it is the first in this file whose defect is NOT at a store.
#
#  *** THE GUEST WRITE LANDS AND RETURNS NORMALLY.  THE HOST DIED ~9 ms LATER, INSIDE
#  sh4_timer_tick() AT 110 Hz. ***  Every other probe wired above -- #443's, #447's, #448's
#  -- observes the STORE SITE: issue one store, ask whether the host survived that
#  instruction.  All three are blind to this by construction, and the witness keeps a row
#  (S0) recording exactly that: the store alone leaves the host alive.
#
#  F1 IS THE ROW THAT NEEDED THE NEW SHAPE.  The diagnostic comes from a callback that
#  fires many times during one free run, and fatal() has no quiet_mode early-out, so an
#  unlatched complaint is a flood -q cannot stop.  F1 spins long enough for many ticks and
#  requires EXACTLY ONE line.  No store-site row can measure that: none lets the callback
#  run twice.
#
#  The TMU half is covered OFFLINE instead, in gate 2: regress/diff_sh4_tmu.c's
#  `rtcsr_falls_through` row sets CMIE and requires the timer to keep counting, which is
#  what catches an early `return` -- the obvious fix, and the wrong one.  Measured there:
#  clean 0 failures, early-return 1 failure.  It costs microseconds and needs no pty.
RTLOG=$LOGDIR/gate_sh4_rtcsr.log
python3 sh4_rtcsr_probe.py "$PMAX" "$KERNEL" > "$RTLOG" 2>&1 || true

if ! grep -q "SH4RTCSR_RESULT=" "$RTLOG"; then
    note "sh4_rtcsr probe produced no result line; last lines follow"
    tail -5 "$RTLOG" | sed 's/^/       /'
    check "sh4_rtcsr probe completed" "no" "yes"
else
    grep -E "^  (ok|FAIL) " "$RTLOG" | sed 's/^/       /'
    check "sh4_rtcsr: a refresh-interrupt enable does not kill the host"           "$(grep -c 'SH4RTCSR_PASS' "$RTLOG")" "1"
    #  10, and two of those rows exist because the round's own mutation run measured them
    #  needed: L1 (two stores in ONE process) after a latch mutant scored a clean 9/9
    #  against every single-session row, and A1 re-valued after it was written against
    #  RTCSR_CMF -- a bit that is write-1-to-KEEP and that nothing in the device ever sets,
    #  so a guest cannot set it and the row could never trip a widened guard.
    check_min "sh4_rtcsr: rows actually run"           "$(grep -cE '^  (ok|FAIL) ' "$RTLOG")" 10
fi

#  #451: the two command-byte validators in sh4_sci_cmd().  This is the first SH-4 site
#  in this tree that a single store CANNOT reach -- the guest must clock a byte in through
#  SHREG_SCSPTR, seventeen mov.b stores, and only the eighth rising edge calls the
#  function.  Every SH-4 probe before it observes a store site, so all of them were blind.
#
#  *** THE ORACLE IS THE TRANSFER, NOT SURVIVAL, and that is the whole design. ***  This
#  fix deleted two exit(1) calls, and with them the accidental tripwire that made a
#  missing `return` or a grown guard LOUD.  After it, both are silent: a missing `return`
#  performs an invented transfer against the RS5C313 and says nothing.  So the rows watch
#  dev_sh4.c:664/:685's `[ SCI: read|write addr=.. data=.. ]` lines, with a legal pair
#  (0xa5 sets address 5, 0x9c writes data c) proving the oracle is LIVE -- otherwise every
#  "no transfer occurred" row would pass for the wrong reason rather than the right one.
#
#  MEASURED KILL TABLE, 14 mutants, no survivors.  Two carry a lesson worth the line:
#    *  M2 (site 1 `return` deleted) is invisible to byte 0x00 -- 0x00 also fails site 2,
#       which catches what site 1 dropped.  Row R1 uses 0x10 instead: bit 7 clear but a
#       LEGAL transfer field, so the fall-through reaches the write arm and really writes.
#       Three pass-1 seats converged on this independently.
#    *  M9 (the `sci_bits_outputed = 0` moved into the callee below the returns) was first
#       built at the TOP of the callee, where it runs on every call -- an EQUIVALENT
#       mutant that "survived".  Rebuilt as described, it jams the shifter and row J
#       reddens.  A mutant that does not model the defect measures the detector's silence,
#       not its blindness.
SCILOG=$LOGDIR/gate_sh4_sci.log
python3 sh4_sci_probe.py "$PMAX" "$KERNEL" > "$SCILOG" 2>&1 || true

if ! grep -q "SH4SCI_RESULT=" "$SCILOG"; then
    note "sh4_sci probe produced no result line; last lines follow"
    tail -5 "$SCILOG" | sed 's/^/       /'
    check "sh4_sci probe completed" "no" "yes"
else
    grep -E "^  (ok|FAIL) " "$SCILOG" | sed 's/^/       /'
    check "sh4_sci: a clocked-in command byte does not kill the host"           "$(grep -c 'SH4SCI_PASS' "$SCILOG")" "1"
    check_min "sh4_sci: rows actually run"           "$(grep -cE '^  (ok|FAIL) ' "$SCILOG")" 14
fi

#  #452: the two TLB data-array-2 sites.  Both `da1` devices are registered for SIXTEEN
#  megabytes and each handler ended the host on `relative_addr & 0x800000` -- EIGHT
#  megabytes, the upper half of a range the device itself claimed.  One guest load or
#  store was enough, and the guard sat ABOVE the writeflag test so direction did not
#  matter.  The discriminator is a single ADDRESS BIT, sharper than any earlier SH-4
#  round here: the same device at the same width answers at 0xf3000000 and died at
#  0xf3800000.
#
#  MEASURED KILL TABLE, 10 mutants: 9 die, 1 is EQUIVALENT.  Two are worth the lines:
#    *  M1 -- dropping the declined-read's memory_writemax64() -- was predicted by THREE
#       seats to hand the guest stale host bytes.  It does not, and the reason is in this
#       tree: memory_rw.c:484-491, correction #95, already zeroes the caller's buffer
#       before every device read.  Measured in five contexts, identical on both builds.
#       It carries NO row, because a row that cannot fail is decoration.
#    *  G1 -- the guard grown from 0x800000 to 0xc00000, with its latch operand widened
#       jointly -- reddens A3 and NOTHING ELSE.  A1/A2 sit at offset 0 and cannot see it;
#       A3 sits at +0x400000, bit 22 set, which is exactly the range such a growth starts
#       refusing.  That is the de-escalation clause discharged by measured kill.
DA2LOG=$LOGDIR/gate_sh4_tlbda2.log
python3 sh4_tlbda2_probe.py "$PMAX" "$KERNEL" > "$DA2LOG" 2>&1 || true

if ! grep -q "SH4TLBDA2_RESULT=" "$DA2LOG"; then
    note "sh4_tlbda2 probe produced no result line; last lines follow"
    tail -5 "$DA2LOG" | sed 's/^/       /'
    check "sh4_tlbda2 probe completed" "no" "yes"
else
    grep -E "^  (ok|FAIL) " "$DA2LOG" | sed 's/^/       /'
    check "sh4_tlbda2: a TLB data-array-2 access does not kill the host"           "$(grep -c 'SH4TLBDA2_PASS' "$DA2LOG")" "1"
    check_min "sh4_tlbda2: rows actually run"           "$(grep -cE '^  (ok|FAIL) ' "$DA2LOG")" 10
fi

#  sh4_tlbda2_witness.py is DELIBERATELY NOT RUN HERE -- same rule as the four below it.
#  7/7 pre-fix and 4/7 after, the three differences being exactly the three kill rows
#  (an ITLB load, a UTLB load, and an ITLB store).  Its two controls assert EQUALITY with
#  the value each device's own mask folds 0xffffffff to -- 0x1ffffdfa and 0x1ffffdff,
#  which DIFFER -- after a panel seat pointed out that the first draft asserted only
#  INEQUALITY against three wrong values, which any fourth wrong value would have passed.

#  sh4_sci_witness.py is DELIBERATELY NOT RUN HERE -- same rule as the three below it.
#  8/8 pre-fix, 5/8 after, the three differences being exactly the three bytes that used
#  to end the host (0x00, 0x80 and 0xb0).  0xb0 was NOT in the first draft of that witness:
#  a pass-1 seat pointed out that `(cmd & 0x30)` reaches the else arm for BOTH 0x00 and
#  0x30, so the second site had two reachable faults and only one of them was measured.

#  sh4_rtcsr_witness.py is DELIBERATELY NOT RUN HERE: 8/8 pre-fix, 6/8 after, the two
#  differences being the two kill rows.  A gated witness reddens the day its fix lands.

#  sh4_chcr_witness.py is DELIBERATELY NOT RUN HERE, for the same reason as #447's:
#  it asserts the PRE-FIX symptom (13/13 pre-fix, 8/13 post-fix, the five differences
#  being exactly the five sites repaired) and would go red the day its fix landed.

#  sh4_val_witness.py is DELIBERATELY NOT RUN HERE.  It asserts the PRE-FIX symptom -- that
#  the host process dies -- so it correctly goes RED the moment the fix is present.  Wiring
#  a witness into a gate manufactures a phantom regression on the day the fix lands, and
#  check_probe_wiring.py treats a gated witness as a HARD failure for exactly that reason.


#  ------------------------------------------------------------------ wdcflood
#  Six unlatched fatal() in dev_wdc.c, each guest-drivable without bound.  Measured
#  pre-fix: 20 stores -> 20 host lines with AND without -q, and the OVER-READ site at
#  500 iterations produced 2000 lines / 158,449 bytes.  Artifacts live at
#  regress/artifacts/wdcflood/witness_20260825/{fr_no__q,fr_with__q,n3}.out.
#  (An earlier wording said "the read path", which points at the non-8-bit READ guard;
#  n3.out is 2000x "reading too much", i.e. the ring over-read.  Same numbers, wrong
#  site named.)  fatal() has no early-out (core/debugmsg.c:384-390 against debug()'s
#  at :375), so -q cannot silence it.
#
#  THE DENOMINATOR IS 26 AND TWELVE OF THOSE ROWS EXIST BECAUSE A PANEL OR A KILL TABLE
#  FOUND THE FIRST FOURTEEN INSUFFICIENT.  Every one of the twelve closes a MEASURED or
#  PREDICTED escape, and each is the only row that sees its own:
#    overrun x2  the :145 reinstatement -- an L2 FLOOR BREACH until this row existed
#    interleave  a latch reset on a NORMAL operation, invisible to back-to-back rows
#    w16 reset   a latch operand a guest can CLEAR between fires
#    r16 reset   the same at the READ site -- sibling parity, and it was missing
#    fire3       a period-N latch; a two-fire oracle cannot see period 2
#    w32/r32     the width rows probed 16-bit only
#    r16/w16 value  BOTH fires, because a `return` after a latched fatal() corrupts
#                   the FIRST access and an earlier one-value form was VACUOUS
#    wr indep    TWO SITES IN ONE SESSION -- the only row that can see flag pairing
#    w mixed     a width-KEYED latch: alternating mov.w/mov.l floods forever, and no
#    r mixed     single-width row can see it.  Both came from the capped ask-again,
#                fired against a table that was already clean at 24 rows.
#
#  -u IS LOAD-BEARING, for the reason the gdrom section above records: with stdout
#  redirected to a file it is block buffered, and a killed run then loses every row and
#  looks like a run that produced nothing.
#
#  THE DISK IS REQUIRED AND ITS ABSENCE IS A SKIP, NEVER A PASS.  wdc_command()
#  early-returns before the opcode switch when no IDE image exists (grep
#  `but no disk image`), so without it the :583 rows cannot fire at all and would read
#  as green-on-nothing.  An earlier form cited :461-468, which is wdc_status() and was
#  wrong even before the fix moved every line in this file.
#
#  THAT EARLY RETURN'S OWN debug() REPEATS ONCE PER FAILED COMMAND and is NOT latched
#  here.  It is a DIFFERENT CHANNEL, and the reason is stronger than -q: debug()
#  computes v = verbose - (emul_executing ? 1 : 0) + (stepping ? 1 : 0) and returns at
#  core/debugmsg.c:375 when v < 0.  FREE-RUNNING AT DEFAULT VERBOSITY THAT IS v == -1,
#  so the arm emits NOTHING AT ALL; it becomes one line per command only under -v or
#  under stepping.  fatal() has no such early-out.  Outside this round's scope rather
#  than a missed site; it rides with `floodclass`.
#
#  (An earlier wording said FLOODS IDENTICALLY, full stop -- an overstatement, and the
#  qualifier was not missing from the evidence but from the summary: the original
#  filing already read "invisible free-running at verbosity 0".  Caught by the pass-2
#  codex seat re-deriving from debugmsg.c what our own record already said.)
WDCIMG=$IMAGES/wdc-scratch-64m.img
if [ ! -f "$WDCIMG" ]; then
    gate_skip "wdcflood: $WDCIMG absent (see regress/images.md -- it is a dd recipe, not a download)"
else
    WFLOG=$LOGDIR/gate_wdc_flood.log
    python3 -u wdc_flood_probe.py "$PMAX" "$KERNEL" "$WDCIMG" > "$WFLOG" 2>&1 || true

    if ! grep -q "WDC_FLOOD_RESULT=" "$WFLOG"; then
        note "wdc_flood probe produced no result line; last lines follow"
        tail -5 "$WFLOG" | sed 's/^/       /'
        check "wdc_flood probe completed" "no" "yes"
    else
        grep -E " ok$| FAIL$" "$WFLOG" | sed 's/^/       /'
        wfres=$(grep -o "WDC_FLOOD_RESULT=[0-9]*/[0-9]*" "$WFLOG" | tail -1 | cut -d= -f2)

        #  *** PARSE BEFORE SCORE. ***  If the result line exists but is MALFORMED, the
        #  outer grep still succeeds, `wfres` is EMPTY, and both `${wfres%/*}` and
        #  `${wfres#*/}` expand to the empty string -- so `check "rows correct" "" ""`
        #  PASSES while nothing was measured.  Three panel seats found that false pass
        #  in the asic section above; it is the project's own "a pattern that matched
        #  nothing reports zero for everything" class in shell-expansion clothes.
        if [ -z "$wfres" ]; then
            note "wdc_flood result line present but unparseable; last lines follow"
            tail -3 "$WFLOG" | sed 's/^/       /'
            check "wdc_flood result parses" "no" "yes"
        else
            check "wdc_flood result parses" "yes" "yes"
            check "wdc_flood rows run"     "${wfres#*/}" 26
            check "wdc_flood rows correct" "${wfres%/*}" "${wfres#*/}"

            #  Per-row presence.  A row that silently stops being tested is the
            #  padded-column class.  The probe's format is "%-14s " -- fourteen columns
            #  plus one literal space -- so a name of length L is followed by (15 - L)
            #  spaces; at L=13 that is two and the `^$v  ` anchor still matches, at L=14
            #  it is ONE and THE ROW SILENTLY STOPS BEING TESTED while the gate stays
            #  green.  Longest name here is `overread x2` / `unimpl 2op` (11), so there
            #  are two characters of headroom.  Checked: no name is a prefix of another
            #  followed by a space, so no pattern can match two rows.
            #  The `count "$WFLOG"` on the next line is what identifies this section --
            #  every section's list opens "live" "devsig".
            for v in "live" "devsig" "unimpl x2" "unimpl 2op" "abrt 2nd" "overread x2" "overread -1" "w16 x2" "r16 x2" "datawr x2" "fire3" "interleave" "w16 reset" "wr indep" "w mixed" "r mixed" "r16 reset" "w32 x2" "r32 x2" "r16 value" "w16 value" "overrun x2" "accept ec" "accept w8" "accept r8" "disjoint"; do
                n=$(count "$WFLOG" "^$v  .*ok$")
                check "wdc_flood $v" "$n" 1
            done
        fi
    fi
fi

#  *** A SOURCE GREP, BECAUSE A STEP-BASED PROBE CANNOT SEE CHANNEL SEMANTICS. ***
#  `fatal(` -> `debug(` at any of the six sites scores a CLEAN SWEEP against every row
#  above: they all single-step, and debug() always prints under stepping (its early-out
#  at core/debugmsg.c:375 fires on `v < 0`, which free-running at verbose 0 gives and
#  stepping does not).  A production guest would get SILENCE while the detector stayed
#  green -- quietly reversing this fork's own warrant for keeping fatal() (dev_asc.c:248-257:
#  under -q verbosity settles at VERBOSITY_ERROR, so a WARNING-level debugmsg is invisible
#  to the boot-log hygiene grep and an ERROR-level one trips #261's break-on-ERROR).
#  Named by a file-reading seat on the pass-2 panel.  Textual, cheap, and the only guard
#  that exists for this class.
#  *** PIN ON THE OPENING STRING LITERAL, AND THE REASON IS A NEAR MISS WORTH RECORDING. ***
#  A first draft pinned `grep -c 'fatal('` at 12.  That counts COMMENT lines mentioning
#  fatal() and gives 15 -- an UNSATISFIABLE check, red forever.  Narrowing to
#  `^[[:space:]]+fatal\(` gives 12 and looks correct -- but TWO of those matches are
#  comment CONTINUATION lines that happen to start with whitespace then "fatal()".  The
#  number would have been right BY COINCIDENCE, and any edit to that comment block would
#  have broken a check nobody would suspect.  `fatal("` cannot match a comment, and 10 is
#  the true census: 4 call sites latched by #337, 6 by this round.
check "wdcflood: ten fatal() call sites intact (channel not downgraded)" \
      "$(grep -cE '^[[:space:]]+fatal\("' ../src/devices/dev_wdc.c)" 10
check "wdcflood: six warned_ guards present (one set + one read each)" \
      "$(grep -cE 'd->warned_(inbuf_overrun|inbuf_overread|unimpl_cmd|nonbyte_write|nonbyte_read|data_unexpected)' ../src/devices/dev_wdc.c)" 12

gate_end
