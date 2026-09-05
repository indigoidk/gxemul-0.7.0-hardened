# Opus 5 seat -- pcc2widthkills PASS 7 findings (in progress)

Tree: GXEMUL-SEC uncommitted on b78bb0f.  Verified cwd = /c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC,
git log HEAD = b78bb0f "#500 pass 15 + pcc2widthkills ...".  dev_pcc2.c = 748 lines,
pcc2_width_probe.py = 813 lines.  These are the FORK, not a pristine copy.

## RUNNING NOTES (updated as I go)

### F-A (Q1): reassert_interrupts() is a CALLEE of SEVEN of the twelve guarded bodies, and the
contract's operand enumeration does not mention it.
Guarded write bodies that call reassert_interrupts(d): GENCTL, TxICR, SCCICR, SCCTX, SCCRX,
SCSIICR, MASK  (7 of 12).  reassert_interrupts (dev_pcc2.c:~260-338) READS:
  d->pcctwo_reg[PCCTWO_GENCTL]  (C040 at top, MIEN at bottom)
  d->pending_timer1_interrupts, d->pending_timer2_interrupts
  d->pcctwo_reg[PCCTWO_T1ICR], [PCCTWO_T2ICR]
  d->pcctwo_reg[PCCTWO_SCCTX], [PCCTWO_SCCRX], [PCCTWO_SCSIICR]
  d->pcctwo_reg[PCCTWO_IPL]   <-- read at `if (d->pcctwo_reg[PCCTWO_IPL] < intlevel)' AND at
                                   the final `(reg[IPL] & MASK) > (reg[MASK] & MASK)'
  d->pcctwo_reg[PCCTWO_MASK]
  d->cpu_irq
and WRITES cur_int_vec[] (never reads it -- the contract's cur_int_vec claim is TRUE).

CONSEQUENCE: `pending_timer1/2' is a body-read field at SEVEN arms under a transitive reading,
and the pend1/pend2 rows hold it non-zero at ONE arm (TxICR) only.  The (field, arm) cell
(pending_timer, GENCTL) has no row.  TO MEASURE.

### F-B (Q1/Q5): the reg[IPL] out-of-closure disclosure is scoped to the IPL guard and
understates the escape.  reg[IPL] is read transitively by 7 bodies, and at GENCTL/MASK the
consequence of landing is a stored neighbour lane, not "one message".  TO MEASURE.

### F-C (Q2/Q5, MEASURED FROM THE ROUND'S OWN LOGS): `rb4 genctl` and `rb8 genctl` kill by
### HOST DEATH, and the probe still prints a NOROW line saying that cannot happen.
The len-4 pattern `0xaab8ccdd` has low lane 0xdd; the len-8 pattern `0xaab8ccdd00112244` has
low lane 0x44.  0xdd & 0x04 = 0x04 and 0x44 & 0x04 = 0x04 -- PCC2_C040 (mvme_pcctworeg.h:61).
GENCTL's write body calls reassert_interrupts(), whose FIRST statement is
`if (reg[GENCTL] & PCC2_C040) { fatal(...); exit(1); }` (dev_pcc2.c:~262).
MEASURED, in this round's own artifacts:
  part6b/M_W4FALL_ALL.out:85  rb4 genctl  got=died   want=0x82  FAIL
  part6b/M_W4FALL_ALL.out:86  rb8 genctl  got=died   want=0x82  FAIL
  part6 /M_W4FALL_ALL.out:86  rb8 genctl  got=0x33   want=0x82  FAIL     (0x33 & 0x04 == 0)
So the L1 value change 0x33 -> 0x44, made to de-vacuate `rb8 t2ctl`/`rb8 t2icr`, SILENTLY
converted `rb8 genctl`'s channel from a readback value into a host kill.  The probe's summary
still prints:  "NOROW  pcc2c040kill -- ... every GENCTL lane here keeps that bit clear"
and the contract repeats it.  FALSE for two of the 41 new rows.
Severity: the rows still red, so no floor breach.  But (i) the record is wrong, (ii) the
contract's stated CHANNEL for rb4/rb8 ("the readback value, which differs under the
fall-through mutant") is wrong at GENCTL, and (iii) Section 13's enumeration checked
"landed lane != preset" at all nine arms and did NOT check "landed lane trips pcc2c040kill",
which is the same class of unenumerated per-arm consequence the section was written to close.

### F-D (Q5): two arithmetic errors in the landed-lane enumerations, both at the `& 0x1f` arms.
PRETABLE_pass6b Section 13 says "SCCTX 0x44"; SCCTX's arm is `= idata & 0x1f`, so the landed
lane is 0x04.  PRETABLE_pass6 Section 12 says "GENCTL/MASK/SCC*: 0xdd" for len 4; SCCICR and
SCCTX are `& 0x1f`, so theirs is 0x1d.  Both still differ from the preset 0x1f, so no row is
vacuous -- but the table written to enforce "choose the value against THAT arm's mask" does
not itself apply that arm's mask.

### F-E (Q5): "only VECBASE 0x0f and PSCALEADJ 0xdf are non-zero at init" is FALSE.
dev_pcc2.c dev_pcc2_init: `d->pcctwo_reg[PCCTWO_CHIPID] = PCC2_ID;` and
mvme_pcctworeg.h:57 `#define PCC2_ID 0x20`.  Three registers are non-zero at init.

### F-F (Q1): the IPL arm's guarded write body reads a field NO row holds non-initial.
  case PCCTWO_IPL: ... if (writeflag == MEM_WRITE) { static int w = 0; if (!w) {...} }
`w` is read by the guarded body.  Every wide write to IPL is declined, so `w` is 0 at every
wide-write decision point in all 159 rows (ipl noig2/4/8, hwr ipl dcl, latch all/w/d).  The
only row that sets it is `acc ipl ro`, a BYTE write.  Not nameable at the guard without
hoisting the static, so low severity -- but it is a direct answer to Q1's own question.

### F-G (Q3): the pend rows' liveness and the apparatus/defect confusion.
VERIFIED premise 7: debugger.c:800 timer_stop(), :836 `if (exit_debugger_to_continue_single_
stepping) return;`, :840 timer_start().  `continue` exits the while loop normally and DOES
reach timer_start().  So the free-run gets SIGALRM and `step` never does.  CORRECT.
VERIFIED the 0x31 device signature: PCC2_TTIRQ_INT = 0x20 (mvme_pcctworeg.h:125) and the
TxICR body masks idata to 0x17, so no guest write can set 0x20; reassert_interrupts sets it
only under `pending_timerN > 0 && reg[TxICR] & IEN`.  RAM would answer 0x11 (what the byte
store put there) and the bb0 loop would never exit.  So 0x31 IS both liveness and signature.
VERIFIED the mis-encoded-bb0 claim: a bb0 that never branches falls straight into the
breakpoint at CODE+0x18 with r4 = 0x11.  Correct.
BUT: `pend* arm` CAN fail for a reason other than the one under test -- a missed SIGALRM, a
loaded host, or the 8.0 s budget -- and when it does it prints "died", the same token a real
defect produces, and it takes `pend* decl` and `pend* rb` down with it (all three come from
ONE session).  The probe ALREADY has the right token in the transcript and does not use it:
cpu_dyntrans.c:1832 `fatal("BREAKPOINT: pc = 0x%..." )`.  A row counting
`"BREAKPOINT: pc = 0x%x" % (CODE + 0x18)` at 1 would be red ONLY on an apparatus failure and
would separate the two.  RECOMMEND that row, and `noexit` rather than `died` for pend* arm.
ALSO: pass 6 put the FIRST host-timer-dependent rows into this detector, and gate_arm.sh
requires `pcc2 width rows red == 0`.  Gate 14 is therefore now LOAD-SENSITIVE in a way it was
not before, and neither the contract nor the CHANGELOG says so.
ALSO (unstated load-bearing premise): the pend rows work only because GENCTL's PCC2_MIEN
(0x02) is clear at init, so reassert_interrupts computes assert=1 and then zeroes it
(`if (!(reg[GENCTL] & PCC2_MIEN)) assert = 0;`).  If any future row set MIEN earlier in the
same session the guest would take an interrupt and the loop would exit for the wrong reason.

### MEASUREMENT APPARATUS (all logs under /tmp/p7logs, copied to this dir at driver end)
Clone /tmp/gxopus_p7 = `cp -a build`, dev_pcc2.c copied from SEC, cmp-clean, rebuilt.
Frozen probe md5 ef3f43b4 == part 6b's corrected instrument.
BASE  159/159, PCC2W_PROBE_DONE present  (/tmp/p7logs/base.out:165,167).  Apparatus reproduces.
Pre-table with predictions written 03:44:08; M1 built 03:49:17-18 (mutant text 12/12 in source,
binary FRESH).  Order witnessed.

### F-H (Q5): the pass-6 driver's PROOF-OF-MUTATION line is INERT and printed zeros for all six
### part-6 / part-6b mutants.
part5b/killpcc2b_part5b.asrun.sh:51 defines it as seven fixed greps -- `len != 0`, `len & 6`,
`warned = (1u`, `warned |= 1;`, `return 0;`, `warned == (1u`, `&& !(d->warned`.  Every one of
those is a PASS 3-5 mutant literal.  None matches a part-6 mutant: M_NOWRITECHK_* DELETES a
line, M_W4FALL_ALL inserts `if (len < 4) break;`, and M_PENDT1/2_TXICR insert
`&& d->pending_timer*_interrupts == 0` -- which the `qual` counter (`&& !(d->warned`) does not
match.  So part6/driver.log prints
  "[M_PENDT2_TXICR] mutant text: 0 len!=0, 0 len&6, 0 assign, 0 bit0, 0 ret0, 0 testeq, 0 qual"
for a mutant that IS a qualified guard.  Six mutants, six all-zero proof lines, unremarked.
This is the carrier's "a pattern that matched nothing reports zero for everything" class inside
the round's own kill-table driver.  It did not cost this round a wrong result, because four of
the six mutants moved the score; but an ESCAPE claim (the thing pass 3's `acc all` lesson is
about) would have had NO proof of mutation at all beyond a timestamp.

### F-I (Q5, provenance): part6 and part6b preserved NO driver script.
parts 1, 2, 3, 3b, 3c, 4, 5, 5b each carry `killpcc2b_part<N>.asrun.sh`.  part6 and part6b carry
only BASE.out / mutant .out / build logs / driver.log / frozen_probe.py.  The two tables this
pass's repair rests on are the two whose driver is not in the artifacts.

### F-J (Q5): CHANGELOG.md:106 truncates the part-6b RED list mid-token.
It ends `...,rb4 mask,rb8` -- dropping `mask,pscale noig4,pscale noig8,ipl noig4,ipl noig8`, and
ending on a bare `rb8` that is not a row name.  part6b/driver.log has all 22.  A transcription
where the deriver is one directory away.

### F-K (Q1, table warrant): the SWAP cell's `C` warrant is FORM-SPECIFIC and is stated
### generally.
The contract's `C` note reads "SWAP, its value 0x0003 fits a byte, so a value-test guard at ANY
arm lets it land and drops the count."  True for `idata > 0xff`.  FALSE as a general claim about
value-test guards: `len != 1` -> `idata != 1` is a one-token operand swap from a body-read field
and NO row performs a wide write of value exactly 1 (`latch all` 0x0003, `latch all w/d`
0x...0003, rb* 0xaabb/0xaab8/0x0022, rb4 0xaab8ccdd, rb8 0x...2244, `pend1 decl` 0x0000,
`wwr sccerr` 0x0).  `idata != 0` IS caught, by `wwr sccerr dcl` (r6 = 0) and `pend1 decl`
(put h 0x0000).  So the cardinality row catches ONE member of the value-test family, not the
family.

### VERIFIED-CORRECT (recorded so agreement is separated from unchecked assent)
* premise 7 (timer_stop / step returns before timer_start): debugger.c:800, :836, :840.  TRUE.
* `cur_int_vec[]` read by no guarded body: dev_pcc2.c writes it at :286,:292,:300,:308,:316
  (all inside reassert_interrupts) and READS it once, at :679, in DEVICE_ACCESS(mvme187_iack).
  TRUE.
* the 0x31 device signature: PCC2_TTIRQ_INT 0x20 (mvme_pcctworeg.h:125) is outside the TxICR
  body's `& 0x17` writable mask, so no guest write can set it.  TRUE.
* SCCERR's FALL = E: no writer anywhere stores a NONZERO SCCERR.  The counter memcpy's widest
  span is T2COUNT 0x10 + 8 = 0x18 < 0x1c; pcctwo_interrupt_common writes SCSIICR/SCCTX/SCCRX;
  reassert writes IPL/T1ICR/T2ICR; pcc_timer_tick writes T1COUNT/T2COUNT/T1CTL/T2CTL.  TRUE.
* the 15-char row-name ceiling: `%-16s` + the format's literal space gives a 15-char name
  exactly TWO trailing spaces, which is what the gate's `^$v  ` anchor needs.  `brd pscale noig`
  is 15 and MATCHES -- verified byte-for-byte with `cat -A` on base.out:83.  159 gate names,
  no duplicates.  The probe's `assert len(name) <= 15` is tuned to the exact boundary.
* the operator/name-gap disclosure: exactly SEVEN arms have a name-pinning row (GENCTL, TxCTL,
  TxICR, SCCTX, SCCERR, MASK, IPL) and FIVE do not (VECBASE, PSCALEADJ, SCCICR, SCCRX,
  SCSIICR).  The count is right.

### F-L (Q2): the width closure is complete per BLOCK and NOT per LABEL.  The T1CTL and T1ICR
### labels have no `rb4'/`rb8' row, and the round already paid for exactly this at width 2.
The contract's own THE SHARED BLOCKS paragraph: "a seat noted that a fall-through reaching only
the T1 labels (the block split in two) would leave `op t1ctl dcl' at 1 with nothing reading
T1CTL back.  So the T1 labels carry their own operator-path readbacks, `rb t1ctl' and
`rb t1icr'."  That reasoning is width-independent, and pass 6 did not repeat it:
  len 2  rb genctl, rb vecbase own, rb t2ctl, rb t2icr, rb scctx, rb sccicr, rb sccrx,
         rb scsiicr, rb mask, + rb t1ctl, rb t1icr, + op pscale noig / hwr ipl noig, SCCERR E
         -> TWELVE blocks AND both T1 labels.
  len 4  rb4 x9 (T2 offsets only) + pscale noig4 + ipl noig4, SCCERR E  -> twelve BLOCKS,
         but NOTHING reads T1CTL or T1ICR back after a 4-byte write.
  len 8  same gap.
So the answer to Q2's "unobservable at NO width and NO block" is: at no BLOCK, yes; at no
LABEL, no.  Severity: coverage debt of the same family as the already-FILED `pcc2latchwidth48`
(the latch-set check at widths 4/8) -- but unlike that one it is neither filed nor disclosed.
The block-vs-label units slip is the one this file's own comments record twice.

### F-M (Q2, enumerated): preset -> landed lane, all nine storing arms, both widths, derived
### against each arm's own mask.  NO vacuous readback remains on the current instrument.
len 4, low lane 0xdd:  GENCTL 0xdd(0x82) VECBASE 0xd0(0x50) TxCTL 0x01(0x03) TxICR 0x15(0x13)
  SCCICR 0x1d(0x1f) SCCTX 0x1d(0x1f) SCCRX 0xdd(0x1f) SCSIICR 0xdd(0x1f) MASK 0xdd(0x12)
len 8, low lane 0x44:  GENCTL 0x44(0x82) VECBASE 0x40(0x50) TxCTL 0x00(0x03) TxICR 0x04(0x13)
  SCCICR 0x04(0x1f) SCCTX 0x04(0x1f) SCCRX 0x44(0x1f) SCSIICR 0x44(0x1f) MASK 0x44(0x12)
  (TxCTL at len 8 additionally takes the COVF arm: 0x44 & PCC2_TCTL_COVF(0x04) is SET, so
   `reg &= ~(OVF|COVF)'; the result is still 0x00.)
All eighteen differ from their preset -> the L1 repair worked.  Two of the contract's own
entries are wrong (F-D) and the GENCTL pair's real channel is death, not value (F-C).

## DRAFT VERDICT (written before M1/M2 land; will be corrected if the measurement refutes it)

VERDICT: NOT A VALID CLOSING PASS.  Zero floor breaches is NOT established, and several
sentences in the shipped record are refuted by measurements this round already holds.

The single substantive issue: the contract's "THE GUARD'S OPERAND SPACE, CLOSED AS A CLASS"
is written PER FIELD and the rows close it PER (FIELD, ARM) CELL -- at ONE arm of twelve for
pending_timer1/2 and the TxICR INT bit.  Both pass-6 measurements were also at that one arm.
The class-closure amendment the round invokes demands the full space "from the function's own
inputs, close every cell in ONE diff"; the space here is (field x arm) because there are twelve
guards.  M1 measures the same conjunct at all twelve; if it scores 157/159 with exactly
`pend2 decl,pend2 rb' -- byte-identical to pass 6's TxICR-only mutant -- then eleven cells are
uncovered and "closed as a class" is measured false.

On the L2-vs-FILE adjudication (premise 10): the ruling is RIGHT and its own reasoning is what
creates the obligation.  "DIRECT read of the guarded body" is the correct standard -- the
carrier's DEPENDS-ON bound explicitly says clause (1) never walks into callees, and clause (2)
is the guard-field/body-field GREP, which cannot see a callee's reads.  Under that standard:
  * at TxICR pending_timer* IS a direct body read -> in closure -> L2, correctly ruled;
  * at the other eleven arms it is reached only through reassert_interrupts(), a CALLEE ->
    OUT of closure -> not owed a row;
  * therefore the contract owes a DISCLOSURE, not eleven rows.  The strict reading is also the
    only bounded one: reassert_interrupts reaches INTERRUPT_ASSERT and the whole interrupt
    subsystem, so a transitive closure is unbounded.
The honest sentence is one paragraph and it terminates the chain:
  "pending_timer1/2 and the TxICR INT bit are in closure at TxICR ONLY, where the body reads
   them directly; closed there by pend1/pend2.  At the other eleven arms these fields are
   reached only through reassert_interrupts(), a callee, and are OUT of the clause-(d) closure
   by the DEPENDS-ON bound.  The same conjunct at those arms escapes all 159 rows -- MEASURED
   (log named).  Disclosed, not owed."
That sentence is checkable, is what clause (e) exists for, and my M1 supplies its measured half.

### PREMISES RE-DERIVED FROM SOURCE THE BRIEF DID NOT GIVE ME (agreement that cost something)
* Premise 2 (big-endian compose, `(uint8_t) idata' is the HIGHEST-address lane): verified
  WITHOUT the M_DELETE measurement.  memory.c:818-828 store_16bit_word puts data16>>8 at
  data[0] and swaps only for EMUL_LITTLE_ENDIAN; m88k is big-endian.  memory_readmax64
  composes the same way.  TRUE.
* Premise 4 (put b does NOT reach a DM_DEFAULT arm; put h/w/d DO): verified from three sites.
  memory_rw.c:584-585 is exactly `if (!no_exceptions || (mem->devices[i].flags &
  DM_READS_HAVE_NO_SIDE_EFFECTS))'.  debugger_cmds.c:1507 passes `CACHE_NONE | NO_EXCEPTIONS'
  for `put b' and :717 for a debugger READ.  :1523/:1543/:1558 route put h/w/d through
  store_16/32/64bit_word, and memory.c:827-828 calls memory_rw with `CACHE_DATA' -- NO
  NO_EXCEPTIONS.  TRUE, and now derivable rather than only measured.
* Premise 3 parity: the six even blocks are 0x02,0x16,0x1a,0x1c,0x1e,0x3e (all 2-aligned);
  the eight odd offsets are 0x03,0x15,0x17,0x1b,0x1d,0x1f,0x2f,0x3f; PCC2 base 0xfff42000 is
  8-aligned so parity is preserved; only 0x1c is 4-aligned and NONE is 8-aligned, so even the
  one 4-aligned block is operator-only at len 8.  TRUE.
* "three other devices emit the same suffix": the exact literal `-- declined.  (once) ]'
  appears in dev_dreamcast_gdrom.c and dev_sgi_re.c only -- but dev_sgi_re.c carries BOTH
  DEVICE_ACCESS(sgi_re) and DEVICE_ACCESS(sgi_de), and :974 emits it with an `sgi_de:' prefix.
  Three DEVICES in two files.  TRUE as written; a reader counting FILES gets two.
* `latch all fail' carries a MEASURED kill: part5/M_RET0_VECBASE.out:53 got=1 want=0 FAIL.
  Not a vacuous row.

## ===================== MEASURED RESULT: M1 =====================
## THE CLASS IS NOT CLOSED.  Predicted 157/159 RED={pend2 decl, pend2 rb}; MEASURED EXACTLY.

    log: /tmp/p7logs/driver.log + /tmp/p7logs/M1_PENDT2_ALL12.out (copied into this dir)
    BASE                 159/159   PCC2W_PROBE_DONE          (base.out:165,167)
    M1_PENDT2_ALL12      157/159   RED = pend2 decl,pend2 rb (M1...out, 04:01:06)
    prediction written   03:44:08  (PRETABLE_opus_p7.out); mutant built 03:49:17
    mutation proven      "mutant text in source: 12 occurrences (want 12)"; binary FRESH

M1 appends `&& d->pending_timer2_interrupts == 0' to ALL TWELVE width guards.  Pass 6's
`M_PENDT2_TXICR' appended the same conjunct to ONE guard and scored 157/159 with RED =
`pend2 decl,pend2 rb' (part6/driver.log, 00:01:20).  THE TWO RESULTS ARE BYTE-IDENTICAL.
Adding the identical clause-(d) conjunct at ELEVEN MORE ARMS changed NOT ONE ROW.
The TxICR half is the self-control: it reproduces pass 6's kill, so the edit is live in the
binary and the eleven silent arms are a coverage fact, not a build failure.

DENOMINATOR for this cell: pending_timer1/2 + the TxICR INT bit are held non-initial at a
wide-write decision point at 1 of 12 arms.  11 of 12 cells are uncovered.
So the contract sentence "MEASURED by both Agent seats at TxICR ... and closed as a class"
is MEASURED FALSE as a statement about the class: what is closed is one CELL.

## M2 in flight.  Its mutation is VERIFIED IN THE SOURCE by an independent fixed-string check:
##   grep -cF "d->pcctwo_reg[PCCTWO_IPL] == 0"  -> 13  (12 guards + the pre-existing IPL
##   read-branch test), and grep -cF of the unmutated guard -> 0.  Line 445 verbatim:
##     if (len != 1 && writeflag == MEM_WRITE && d->pcctwo_reg[PCCTWO_IPL] == 0) {
##   binary 04:01:08 > source 04:01:07.
## DISCLOSED AGAINST MYSELF: my driver's own proof line printed "0 occurrences (want 12)" for
## M2, because it greps with `grep -c "$ADD"' and `[PCCTWO_IPL]' is a BRE character class.
## That is precisely the F-H class (a pattern that matched nothing reporting zero) occurring in
## MY driver, one hour after I wrote F-H up.  It cost nothing only because the number was
## SURPRISING and I opened the artifact.  The M1 count was correct (no metacharacters).
