VERDICT: UPHOLD WITH CHANGES (2) -- H1/H2/H3 file as HIGH rows (H1 and H2 carry the rung-3 measurement in meas_D/); sections 3, 5 and 6 stand; section 4's "adopt as written" is narrowed to anchor-and-re-derive, and one same-kind termination path the pre-screens missed is added (SH prom_emul default, cpu_sh_instr.c:3833-3834).

Fable 5.1, own verdict, written after the fallback run. Verbatim line from meas_main/libcq.out: `malloc(0) -> non-NULL`. Every site below I opened at HEAD e483d931 myself (READ). The one measurement cited, meas_D/witness_hostexit.out, was made in the fallback run by claude-opus-4-8 on a private build of e483d931 (binary md5 579abef4); I cite it as that model's measurement, not mine, and nothing in the fallback answer file is relied on without my own read.

## H1, H2, H3 (file as new rows? severity? fold?)

- H1 `ofemulnodata` -- FILE, HIGH, SEPARATE row (may share one round with ofopenexit/ofpeerexit). of.c:1098-1101 exits when md.of_data is NULL; the only writer is of_emul_init (of.c:1078) from machine_macppc.c:99 behind the prom_emulation gate, and md is a union zeroed by machine_new, so of_data is NULL on every non-macppc machine; the ARM/PPC magic words decode with no machine/mode test. No row covers :1100 (ofopenexit=:448, ofpeerexit=:394). MEASURED: testarm `swi 0xef8c64be` ends the host (exit 1), nop control survives.
- H2 `mipssyscallprom` -- FILE, HIGH, separate row. syscall code 0x30378 at any PC routes to promemul whose default exits (cpu_mips_instr.c:4651, :2649-2650); #235 gated the BREAK twin only. Not mipsresetalias. MEASURED: testmips `syscall 0x30378` ends the host (exit 1), nop control survives.
- H3 `asccmdwidecount` -- FILE, HIGH, fold into ONE round with ascwidecount. Command-phase DMA computes `int len` from the guest's unmasked reg_wo[NCR_TCL/TCM] (dev_asc.c:987) and hands it to scsi_transfer_allocbuf, whose huge size_t request returns NULL and exits (diskimage_scsicmd.c:151-155); no span clamp on this path. Same register and store (:1154-1155) as ascwidecount, so one mask/bound fix covers both. Witness REASONED (buildable on pmax; not built).

## Other new rows + section 3

- MIPS X(ei_or_di) skips cop0_availability_check (MED) -- UPHOLD FILE.
- armcp15c1fallthrough (MED) -- UPHOLD FILE (cpu_arm_coproc.c:124-129 falls through to the control write at :134-135).
- ARM TTB/L2 mask 0x0fffffff (armdesc3kill F17) -- UPHOLD FILE; a real address bug for tables above 256 MB (rpi 512 MB).
- coarse domain fault before the L2 fetch (LOW) -- UPHOLD FILE.
- Thumb LDR(3) raises Prefetch not Data Abort -- UPHOLD FILE (sibling); mark ledger:48071 UNVERIFIED verified.
- coarse-L2 type-3 treated as a 1 KB tiny page (N2) -- UPHOLD FILE candidate.
- MB89352 len!=1 diagnostic, 3 conversions for 2 args (N1, LOW) -- UPHOLD FILE; note it is a real guest-reachable format-string UB, not cosmetic.
- DEC21143 unbudgeted RX drain under TAP (net_three F8) -- UPHOLD FILE or fold into ne2krxbudget (dev_dec21143.c:356-366, :301-306 verified).
- BE case-4 byte-lane shift "Filed" with no slug -- UPHOLD FILE as coverage debt.
- pvr/gdrom F15 -- UPHOLD fold into gdromcondhow.
- two harness-builder faults, one row each (mk_briefs4.py:17 severity-vs-sev; the #554 governing-text windows, 221 rows / 117 misaligned) -- UPHOLD FILE.
- Section 3: NO fix spec is ready to build. Every draft has a confirmed defect (RED control can't redden under root; a word token aborts `$(( ))` under set -u; nothing invokes nightly_check.sh and every verdict is TREE_DIRTY so a FAIL-keyed caller is permanently red; the SessionStart hook exits before emitting its JSON; Argon's heredoc diff does not compile). Each row stays open with those defects as the next draft's premises. UPHOLD.

## Sections 4 and 5 (adopting record corrections and brief premises)

Sound in substance: I re-derived 27 corrections at HEAD (5+ per pre-screen file) and every DISPOSED/REFUTED/LIVE grade held; 0 wrong. The verb "adopt as written" is narrowed on two points, both the carrier's own rules:
- Land each line-citation correction as a GREP ANCHOR, not a re-keyed line number -- a re-keyed number rots at the next edit (CC16 is live proof: the cited fatal is :2507 at HEAD, :2635 in the working tree).
- Re-run the DERIVER at commit time for the counts; the corrections as written disagree with each other (PDF inventory 20 vs 26; the marker census), so a verbatim adoption would commit contradictory numbers. The counts rule already requires deriver-plus-demoted-prose, never a fresh literal.
Also keep the ruling-shaped items (null-medium labels, charter/wording, the pass2_ledger schema, the owner D2/ROUTE-PARITY questions) OUT of the L4-correction batch; they are rulings, not records fixes, and the coordinator already routes them separately. Section 5 (premises recorded by pointer only, no code action) is sound.

## Section 6 (the three libc readings)

All three correct for the rows they are applied to, on this host (x86-64 glibc 2.42):
- arcbios F9 / arczeroalloc / dectxzero (malloc(0) leg): malloc(0) is non-NULL, so the NULL-means-OOM exit is NOT reached here -- portability exposure only; other libcs stay CANNOT SETTLE. Right.
- net_three F16 (realloc(p,0) leg): realloc(p,0) is NULL with the block freed, so a site treating that NULL as OOM IS reached here; dev_dec21143.c:788-789 feeds CHECK_ALLOCATION, so the exit is live. Right.
- loaders_four F7 (negative fseek): fseek(-8) returns -1 EINVAL with the position unchanged, so the ECOFF loaders (which ignore the fseek return and exit only on a short fread) read from the current offset -- the "wrong bytes" the row names. Right; consequence depends on the caller's return check.

## What the pre-screens missed

- A same-kind process-termination path in no row: SH prom_emul default. cpu_sh_instr.c:4150-4152 installs instr(prom_emul) on `iword == SH_INVALID_INSTR`, a machine-independent decode; X(prom_emul) (:3819-3835) serves only DREAMCAST and LANDISK and its default is `fatal("SH prom_emul: unimplemented machine type."); exit(1);` (:3833-3834). So on BARESH/TESTSH/HPCSH one guest PROM-trap instruction ends the host -- the H1/H2/arcsgiprivate pattern. No ledger or OB row (grep 0); the sh_two pre-screen scoped itself to memory_sh.c and never opened cpu_sh_instr.c's prom_emul arm. FILE a new candidate; severity MED-to-HIGH (reachable, but on SH types not commonly booted) for the owner to rank against the HIGH promemul siblings. READ, not built.
- H1/H2/H3 were graded READ-only by the pre-screens; a rung-3 witness was one guest instruction away and was built for H1 and H2 in the fallback run (meas_D/). The lifecycle's "ask one seat to try a rung-3 probe before recording a witness-less row" step was not applied to these three; it is cheap and it turns a reading into a measured host death.
- Correctly NOT a miss: the dreamcast_scramble.c exits (the largest single-file exit count) run only at image load (file.c:339), under the host-side image charter, not from a guest instruction.
