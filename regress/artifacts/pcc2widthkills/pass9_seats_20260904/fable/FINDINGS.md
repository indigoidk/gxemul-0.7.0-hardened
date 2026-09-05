# pcc2widthkills PASS 9 -- Fable 5 seat findings (IN PROGRESS)
PASS9_SEAT_ALIVE_20260904
Started: 2026-09-04
Status: reading brief (1341 lines); tree = GXEMUL-SEC uncommitted on b78bb0f

## MEASUREMENTS VERIFIED (part8/*.out row counts vs driver.log) -- ALL MATCH
BASE 190/190 (sentinel PCC2W_PROBE_DONE present, 190 rows emitted)
M_TXCTL_OVFHI  184  red: ovfhi2 decl,ovfhi2 rb,ovfhi1 decl,ovfhi1 rb,rb t2ctl b27,rb t1ctl b27  (6)
M_PEND2_LT2    188  red: pendn2 decl,pendn2 rb  (2)
M_IDATA_NE0_QUAL 170 red=20: wwr sccerr dcl,pend2 decl,pend2 rb,pend1 decl,pend1 rb,ovf2 decl,ovf2 rb,ovf1 decl,ovf1 rb,ipl wset,ovfhi2 decl,ovfhi2 rb,ovfhi1 decl,ovfhi1 rb,pendn2 decl,pendn2 rb,pendn1 decl,pendn1 rb,latch all zero,ipl rset
M_W4FALL_ALL   164  red=26 (rb4/rb8 x nine storing + t1ctl + t1icr = 22, + pscale noig4/8 + ipl noig4/8 = 4)
M_TXICR_IL4    188  red: rb t2icr il4,rb t1icr il4  (2)
M_WARNX_GENCTL 189  red: latch all rev  (1)
M_IPLR         189  red: ipl rset  (1)
M_TXCTL_COVF   188  red: rb t2ctl b27,rb t1ctl b27  (2)
Build freshness verified in driver.log: every mutant binary mtime > source mtime; restore+rebuild+cmp, sentinel cleared, KILLPCC2B_PART8_DONE.
mtime order: PRETABLE_pass8.out 08:02:23 < part8/driver.log 10:10:59 -- predictions precede table. GOOD.

## PREMISES CHECKED FROM SOURCE (not the packet)
P2 alignment: cpu_m88k_instr_loadstore.c:168-184 -- non-byte (LS!=1) access with addr&(size-1) raises
   M88K_EXCEPTION_MISALIGNED_ACCESS and returns BEFORE memory_rw. LS_1 (byte) skips the check entirely.
   Confirms: guest wide access only reaches even offsets; byte reaches all; operator put h bypasses (debugger path).
P3 memory_rw dispatch: memory_rw.c:585 gates side-effect suppression on DM_READS_HAVE_NO_SIDE_EFFECTS;
   pcc2 registers DM_DEFAULT (dev_pcc2.c:736) so put h/w/d DO dispatch. debugger_cmds.c:716 put b path uses NO_EXCEPTIONS.
P.timer_stop: debugger.c:800 timer_stop() during step, :840 timer_start() after -- confirms SIGALRM stopped during `step`,
   so free-running (continue) rows are the only ones that see pending/overflow. Load-sensitivity real.

## MECHANISM VERIFICATION (from GXEMUL-SEC source, not the packet)
- BREAKPOINT token: ONLY source of uppercase "BREAKPOINT" is cpu_dyntrans.c:1833/1837 fatal("BREAKPOINT: pc=..") on breakpoint HIT.
  `breakpoint add`/`show` print lowercase. So until="BREAKPOINT" discriminates a real hit by construction, not by luck. SOUND.
- memory_rw.c:584: device handler f() called iff (!no_exceptions || DM_READS_HAVE_NO_SIDE_EFFECTS). pcc2=DM_DEFAULT.
  put b (debugger_cmds.c:1507) and debugger reads (:716,:1918) use NO_EXCEPTIONS -> NO dispatch to pcc2. CONFIRMS premise 3.
- put h/w/d: store_16/32/64bit_word. store_16bit_word (core/memory.c:827) uses CACHE_DATA (NOT NO_EXCEPTIONS) -> DISPATCHES,
  and composes big-endian. operator_reach_20260903.out: even_h/odd_h -> exit1 pre-fix. CONFIRMS put h reaches the arm.
- m88k alignment (cpu_m88k_instr_loadstore.c:168): non-byte access with addr&(size-1) raises MISALIGNED before memory_rw; LS_1 skips. CONFIRMS reachability premise 2.
- timer_stop() debugger.c:800 during step, timer_start :840 after -> SIGALRM dead during `step`; only `continue` rows see pending/overflow. CONFIRMS load-sensitivity.

## session() TRACE (repaired form) -- verdict: SOUND, no silent mis-attribution, no hang
- tuple read order fixed (line 410 reads c[2] BEFORE line 411 unpacks c[0],c[1]).
- rd() returns: True(early until-found) / False(EOF) / "timeout"(until missed at wall clock) / True(non-until normal).
  Caller: `if r is False` (identity, EOF->alive=False) then `if r=="timeout"` (missed bp -> how="no-breakpoint", stop stream). Distinct. Missed token STOPS the command stream (break). GOOD.
- companion rows: free-run decl/rb use cval(how,..) -> "no-breakpoint (FAILED FOR SOME OTHER REASON)" on miss; arm rows use armval (checks "BREAKPOINT" in t). VERIFIED in M_IDATA_NE0_QUAL.out: arm rows GREEN with real armed values (0x31/0x11/0x81), decl/rb RED with landed values (0x20/0x10/0x80) -- attributable, NOT no-breakpoint.
- killed guest keeps label: reaped flag; kill; bounded 2nd reap; final WIF* block guarded by `how in (no-breakpoint,unreaped,killed): pass` so "killed" is NOT overwritten by WIFEXITED(0). Fixes pass-8 F2. GOOD.
- gate hang: all waitpid use WNOHANG; 2 reap loops bounded 30x0.1s; rd bounded by wall clock; continue until-wait <=20s; old blocking waitpid(pid,0) dead-coded under `if False`. CANNOT HANG.
- survival rows report distinguishable exit codes (exit0/exit1/exit127/sigN) -> an apparatus failure reds with a distinct token, never silently mis-attributed as the width kill.

## VALUE-DOMAIN WALK (12 arms) -- stop condition HONEST
- idata (10 bodies): held 0,1,3 (latch all/one/zero at every arm) + per-arm lanes. `idata!=0` killed(latch all zero), `idata!=1` killed(latch all one), `idata>0xff` killed(rb genctl lo). "any other constant" (idata!=2, !(idata&4)) DISCLOSED. Honest.
  * ADVERSARIAL: `!(idata&0x04)` at GENCTL passes 190 (all GENCTL lanes keep bit0x04 clear for pcc2c040kill). BUT it is (i) the disclosed value-test family and (ii) BENIGN: any escaping wide write has low-lane bit0x04 set -> stores C040 -> exit(1) (pcc2c040kill), so it cannot silently land a neighbour lane. At TxICR/SCCICR/etc the same guard is CAUGHT by rb4 rows (lane 0xdd has bit2). Not a floor breach.
- TxCTL reg byte: held 0,0x03,0x11,0x81,0xfc -> every bit 0-7 set in some held value. `!(reg&0xe0)` killed(ovfhi via M_TXCTL_OVFHI), `!(reg&COVF)` killed(rb b27 via M_TXCTL_COVF). bits2-3 only via filed pcc2counter8 (disclosed; E if fixed). Covered.
- TxICR reg byte: held 0,0x13,0x17,0x31 -> bits0,1,2,4,5 held; bits3,6,7 DEAD (body &0x17, reassert bit5) => E. `!(reg&0x04)` killed(rb il4 via M_TXICR_IL4). Honest.
- pending1/2: held 0,1,thousands. `pending<2` killed(pendn via M_PEND2_LT2), `pending==0` killed(pend). Covered.
- overflow count: held 0,1,8. Covered (ovf,ovfhi).
- IPL write static: held set (ipl wset). read-branch static out-of-closure, held anyway (ipl rset via M_IPLR). Covered.
- warned: own bit (rb2), all 132 ordered foreign pairs (latch all + latch all rev via M_WARNX_GENCTL). Covered.
- relative_addr (TxCTL/TxICR RMW index): T1 vs T2 pinned by rb t1ctl/rb t1icr + op t1* dcl. Covered.
- SCCERR: constant store, value-identical, message channel (E, disclosed). GENCTL/VECBASE/PSCALEADJ/SCC*/MASK: idata-only.
=> Every body-read lvalue now holds >=2 values spanning its reachable range; the only escapes are the DISCLOSED unbounded "any other constant" family + disclosed out-of-scope (c040/default/counter8/announce-severity/bit-translation). STOP CONDITION HONEST.

## RECORD HONESTY (Q5)
- FINDING (L4, records): CHANGELOG pass-8 block header (line 3) says "Detector 171 -> 186 rows". WRONG: the detector is 190
  (19 rows added: ovfhi x6, pendn x6, latch all zero, rb t2icr/t1icr il4, ipl rset, latch all rev, rb t2ctl/t1ctl b27).
  The SAME block says "190-row instrument" (line 70) and the gate is 190/190. "186" is the M_TXCTL_OVFHI/M_IDATA_NE0_QUAL
  PREDICTED SCORE (186/190) mis-copied as the row count. Internal contradiction; frozen-number class. Correct in the pass-9 block. Does NOT block closure (L4, not a floor breach; the gate/driver/brief all use 190).
- Two mispredictions honestly diagnosed and both SAFE-direction (more red):
  * M_TXCTL_OVFHI 184 vs 186: rb t2ctl/t1ctl b27 (reg=0xfc) ALSO land under `!(reg&0xe0)` (0xfc&0xe0!=0 -> conjunct false -> not declined). Pre-table note had polarity backwards; CHANGELOG admits it. Verified from code.
  * M_IDATA_NE0_QUAL 170 vs 186: every free-run row + ipl wset wide-write value 0 (r9=0), so `idata!=0` lands all; pre-table counted only 4. Verified (M_IDATA_NE0_QUAL.out shows 20 red, all value-0 wide writes). Rows are correct; prediction undercounted.
- mtime order: PRETABLE_pass8.out 08:02:23 < part8/driver.log 10:10:59 -> predictions precede table. BASE 190/190 before mutant 1; aborted 188/190 first launch correctly caught + preserved (part8_aborted).

## SWEPT (denominator for the closing zero)
- 12 arms x body-read lvalues, value-domain (analytic from source).
- 8 mutants cross-checked ROW-BY-ROW vs raw part8/*.out (not just driver.log): BASE 190, OVFHI 184, PEND2_LT2 188, IDATA_NE0 170, W4FALL 164, TXICR_IL4 188, WARNX 189, IPLR 189, TXCTL_COVF 188. All match.
- gate14_p9.log: 190 per-row checks + 3 denominators green vs LIVE tree.
- 5 source premises re-derived; session() traced; 6 pass-8 extremes each -> row + killing mutant.
NOT swept (disclosed, out of contract): fatal->debug severity, 1u<<(bit+1) translation (E), pcc2c040kill/defaultkill/counter8, "any other integer constant" value-test family (unbounded, filed).

## VERDICT: GO -- zero FLOOR breaches. Chain CAN close. One L4 records correction owed (186->190 in pass-8 CHANGELOG header).
