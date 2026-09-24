# fbdeclinefive PASS 1 -- consolidated findings and dispositions (main loop, 2026-09-19 07:2x)

Panel dir: `_scratchpad/panel_20260919_070130/` (see p1_panel_launch.log for the exact stamp).  Brief as sent:
`brief_sent.md` (24,985 b).  Seats: codex (panel, IN FLIGHT), agy 22 KB, grok 13 KB, kimi CLI 150 KB (answered, verdict
PROCEED AMENDED), glm 12 KB, deepseek 4.6 KB, minimax 9.5 KB, kimi-k3 substitute 10.9 KB (fired alongside the CLI: the
CLI IS the seat; the substitute is a second transport of the same seat and is recorded as such), opus5 measuring agent
a5dd96173544461dc (IN FLIGHT, verify with agent_models.py), dedicated codex fbd5p1 (IN FLIGHT), fable5 LAST (not fired).

## Brief defects the seats found (records: the packet as sent is preserved; the TEMPLATE is corrected)
B1 "ten live exit(1)" -- the file has NINE (every seat; kimi, agy, grok each counted).  Template corrected.
B2 HEAD label "9c28ca5" -- HEAD is f685d75 (records-only commits since 7836071; sources identical).  kimi.  Corrected.
B3 Table 7-10 excerpt cut at 6831 -- dropped 28Ch FIQEnableClear / 290h FIQSoft.  grok, kimi.  Extended to 6833.
B4 The "zeros are read" warrant (`:1652`) is about NONEXISTENT CSRs; these registers exist.  Zero is POLICY, warranted
   by the file's own silent siblings (FIQ_ENABLE_CLEAR read, TIMER_1_CLEAR read, default:).  grok, glm, deepseek, minimax.

## Design corrections ADOPTED into the template
D1 Row ids A1/A2/D1 collide with rows the sites probe already emits and gate_arm pins -> S1..S5 / N1..N6.  agy, kimi.
D2 All decline rows in ONE new arm (a shared latch bit is only detectable when two sites announce in one process); not
   arm L, whose I1 row asserts no diagnostics.  deepseek, agy, grok.
D3 Interleave a LEGAL read between the two writes of each N row (catches a clear-on-read latch).  grok, agy (Q2 j).
D4 One byte-width (strb) decline row -- the predicate is `writeflag`, not `len`.  grok.
D5 Five per-site `int` latches (house idiom; file has no latch today, 15 fields).  agy, grok, kimi, codex q1b.
D6 K1 pins `WIFEXITED && status==1` AND `Sorry, emulation "<name>"` (usage/-H also exit 1); K2 observes `dead` before
   close() after a fresh `reg`; legs use each launcher's own register map (r1 sites / r7 drain+witness).  grok, kimi.
D7 Q2(f) -- no step-based row can observe a NONZERO status (irq_status is set only by the host-timer assert path,
   stopped at the prompt) -> DISCLOSED under clause (e), or a free-running raw-status row in the drain probe; pass 2
   decides.  All seats named it; kimi calls it "the f-hole".
D8 +0x28c (FIQ_ENABLE_CLEAR read) already declines silently: NOT changed (addition licence), recorded in the contract as
   a non-uniform disposition.  grok.
D9 FAULT is unavailable on ARM (memory_rw dispatches a device-access exception for MIPS/M88K only).  agy, grok, kimi.
D10 Gate pins must grep the legs' DISCRIMINATING tokens, and the drain/witness legs must be in each probe's own
    results rollup -- neither probe is gate-run (gate_offline.sh "NOT run here").  kimi.

## Out-of-scope finds -> FILE at end-of-round triage
F1 `memory_arm.c:254` -- `default:` of the L1 descriptor switch: `fatal("TODO: descriptor ... unimplemented type %i")`
   then `exit(1)`.  Descriptor type 3 (ARMv4/v5 FINE page table) is a legal value a guest can write into its own L1
   table, so this is a GUEST-DRIVABLE HOST KILL.  Not filed anywhere (grep OUTSTANDING_BUGS/ledger: :254 absent).
   Candidate id `armdesc3kill`; options IMPLEMENT (member 7: 1 KB fine pages) or translation FAULT; needs a rung-3
   witness (cats, MMU on, one L1 entry with bits[1:0]=11).  kimi.  Also `:79` (`arm_check_access` dav==2) -- reachable?
   dav comes from the domain access control register (2 = reserved) -> a guest can write DACR=2 for a domain and touch
   it -> CONFIRMED guest-drivable: `cpu_arm_coproc.c:203` stores MCR's operand into `dacr` unfiltered and
   `memory_arm.c:153` derives `dav` from it.  TWO kills, one file, two different guest values (a reserved DACR
   field vs a legal fine-page-table descriptor): file as two rows (`armdacr2kill`, `armdesc3kill`) -- different
   fix shapes (the first is a DECLINE/treat-as-reserved, the second is IMPLEMENT or FAULT).
F2 fiqenableread -- already filed (OUTSTANDING_BUGS:21824, :21982) WITH FIVE FACETS: (1) +0x288 read 0; (2) +0x28c
   silent vs +0x18c kill; (3) fiq_status never written; (4) no FIQ output; (5) FIQSoft has no case.  So the planned
   `fbfiqdead`, `fbfiqclearsilent` ARE THAT ROW and are NOT filed; `fbirqsoftunimpl` is a sixth facet (IRQSoft +0x190,
   the IRQ twin of (5), legal write announced unlatched every access) -> ADD AS FACET (6) with opus5's measurement and
   codex q2's census (`_scratchpad/cxfarm7_20260919/out/codex_q2_fiq_csrlanes_census.txt`: 10/10 assert sites use the
   IRQ output, 0 FIQ; §7.3.30 says the two raw registers always hold identical data -> one shared raw field; IRQSoft/
   FIQSoft are aliases for shared raw bit 1).  q2 part B for `fbcsrdecodelanes`: 26/27 case labels word-aligned
   (DEVICE_ID +0x002 the exception), 767/768 non-aligned offsets reach default:.

## Held for the remaining seats
* codex panel seat: final block not yet emitted (file 327 KB at 07:07, process alive).
* dedicated codex fbd5p1 (premise audit + Q1-7): .txt 0 b, .err 578 KB at 07:10 (streaming reasoning; alive).
* opus5 measuring seat: s1 clone-build, s2 witness HEAD, s3 accept HEAD, s4 fix -- in progress.
* fable5: LAST, short neutral packet, identity verified from the subagent jsonl before crediting.

## Opus5 measuring seat (agent a5dd96173544461dc, VERIFIED claude-opus-5 121/121 writes, no refusal) -- MEASURED
Answer: `_scratchpad/fbd5/opus_p1_20260919/OPUS_P1_ANSWER.md` (48 KB); clone /tmp/gxopusfbd5 restored, cmp-clean,
rebuilt, md5 == HEAD binary, no sentinel.  Witness rung 3 on HEAD: five arms HOST-DIED exit 1 with five DISTINCT texts.
Fix prototype (bit-field form): all five SURVIVE exit 0, announce once over two accesses, registers untouched, shipped
sites probe 18/19 with K1 the only red (19/19 on the restored HEAD).  Eleven-mutant table against the packet's rows:
  caught: keepexit, unlatch, leak18c, store180, misname, latchrd, fiqleak (A4 red at 0xc0)
  TOTAL ESCAPES (29/29): m_sharebit (Q2 c), m_onebit (aggregate latch), m_swallow (Q2 f), m_fiqraw (drop the & at +0x280)
M1 Shared latch: one-process-per-row is blind BY CONSTRUCTION -> N0 all-five-in-one-process count row (5 / 4 / 1).
   -> template.  (With five ints a shared bit is impossible; N0 still catches a copy-paste testing the wrong field.)
M2 N4/N5 write value 0x40 (inside 0xc0), not 0x10 -> template.
M3 fiq_status has NO WRITER in the tree; FIQ enable unobservable from the guest (measured) -> clause (e) disclosure;
   FILE fbfiqdead.
M4 m_swallow escapes: irq_status stays 0 under stepping even with timer 1 armed (24 steps) -> clause (e), matches D7.
M5 28Ch twin: opus5 says fix in this commit; grok says leave (addition licence) -> OPEN QUESTION for Fable; provisional:
   not this round, FILE fbfiqclearsilent, PRETABLE.out records the reason.
M6 190h/290h LEGAL writes announce unlatched every access and do nothing -> FILE fbirqsoftunimpl.
M7 K1: five different startup refusals ALL exit 1 with no prompt -> only the naming diagnostic discriminates, and the
   search must cover the WHOLE buffer (two refusals print the banner first).  K2: `next-send fails` and `dead` are
   IDENTICAL for a child dead before the prologue and for a clean quit -> `exit == 0` AND fresh-`reg` prologue are both
   load-bearing.  Matches D6.
M8 Two zeroing paths (DEVINIT memset; diff_footbridge.c / diff_fbpending_bound.c calloc) -> template.
M9 gate_arm.sh is +67 uncommitted lines (#529's orphan section) -- known; partial-blob commit technique applies.
M10 exit census 9; HEAD f685d75 -- as B1/B2.

## Codex panel seat (GPT-6, max; 373 KB, final block after 'codex' marker; VERDICT: REVISE) -- READING, no runs
Converges with every finding above (nine exits, HEAD f685d75, row-id collision, shared-latch escape (c), constant-0 escape
(f), interleaved read (j), FAULT unavailable, K1 keyed on the naming text, K2 needs prologue + exit 0, legs per launcher).
NEW, adopted:
C1 WARRANT: Table 7-1's access legend (§7.1) reads "Read only. Writes have no effect." -- a DIRECT datasheet warrant that
   the four RO writes are no-effect accesses (member 4 ACCEPT-as-no-effect is defensible for them; it never licenses
   storing the value).  Cite it beside §7.3.29/.30/.33 instead of the nonexistent-CSR sentence.  -> template.
C2 NONZERO-STATE PRESERVATION via the OFFLINE DIFFERENTIAL: `regress/diff_footbridge.c` already #includes the device and
   callocs an instance; seed `irq_status` nonzero there, drive each declined access through the handler, assert every
   field unchanged and IRQ_STATUS reads the AND.  A rung-1 DETECTOR (never a witness) that closes Q2(f) and the
   store-into-status class WITHOUT free-running -- the guest rows keep reachability + survival.  -> template (pass 2 must
   name the split: guest rows = reachability/survival/latch; differential rows = state preservation/expression).
C3 K2 VACUOUS EDIT: move `close()` ahead of the death observation -- stays green (close() quits, drains, exits 0; the later
   send catches the closed descriptor).  NEGATIVE CONTROL: omit K2's `quit` -> the next `reg` must SUCCEED and K2 must
   FAIL.  -> PRETABLE mutant list.
C4 Sites probe defects in scope of the harness commit: arm T's exit status recorded but never required == 0; C4 accepts a
   MISSING vendor value (`None != 0x1011` is True).  Fix both.  -> template.
C5 Sites `send()` drops its timeout argument (drain/witness forward it); drain's old K discards `step_and_check()`'s
   result, witness's K predicate ignores `badis`/`nsteps` -- the K2 prologue check must be SCORED explicitly.  -> template.
C6 Row (g): match the announce text ACCESS-LOCALLY per row, not by a combined count.  -> template (N rows).
C7 Row (e): a FIQ-site decline that stores into IRQ state escapes FIQ-only checks -> every N row reads back BOTH families
   (+0x180/+0x184/+0x188 and +0x280/+0x284).  -> template.
C8 Gate coupling unsettled by the seat (scope excluded gate_*.sh): sites :208-212 documents a literal helper-call
   dependency in gate_hygiene.sh -- check at implementation time (opus5 measured gate_hygiene grades pmax/arc only).

## Fable5 adjudication (agent a150f578f96c06678, VERIFIED claude-fable-5-1 33/33, no fallback) -- PROCEED AMENDED
Answer: `_scratchpad/fbd5/FABLE_P1_ANSWER.md`.  Rulings applied to the template:
Q1 28Ch NOT this round -- UPHELD on the reopening rule's WITNESS clause (grok's addition-licence reason incomplete: the
   transferred-warrant leg `:6801` is available; opus's parity fact true but one field gives 3 dispositions, not 1).
   Obligations: D8 contract line in the PROBE HEADER; fiqenableread facet (2) carries Opus's sentence VERBATIM as the
   dissent; the latch form is chosen for six sites.
Q2 Offline P-rows ACCEPTED as rung-1 DETECTOR rows.  HAZARD: seed by DIRECT FIELD WRITE (d->irq callbacks are NULL under
   calloc; the enable arms call INTERRUPT_ASSERT(d->irq)); the fatal() stub discards text -> misname stays a guest row.
   m_swallow + store-into-status become MEASURED kills; m_fiqraw only narrowed (clause e keeps the FIQ sentence).
Q3 FIVE `int` fields; N0 STILL OWED (the sole carrier of the latch-operand (d) cell).
Q4 C1 NARROWED: cite `:6803` first ("The Status and RawStatus are read-only, and EnableClear and Soft are write-only");
   Table 7-1 is the PCI-config legend, staggered, transfers only.  B4 NARROWED: `:1652` + Figure 7-2 are the nearest
   support, keep POLICY.  D7 SETTLED now: no free-running row; P-row offline; clause (e) says "no GUEST row".  C2 adopted
   with the NULL-callback condition.  D6 token verified (`machine.c:240`); D1 ids verified (the probe emits no S*/N*).
Q5 armdesc3kill MED (member 5 IS available on the translation path: `fs = FAULT_TRANS_S; goto exception_return`, the
   idiom at memory_arm.c:158 -- fable cited :257, which is the `exception_return:` label; the substance holds);
   armdacr2kill MED-LOW (one `case 2:` as no-access); BOTH need a rung-3 witness with the MMU ON (arm T's scaffold).
   IRQSoft = its OWN row `fbirqsoftunimpl`, MED, the NEXT EASY item (member 7, ~8 lines: set/clear irq_status bit 1,
   reassert; witness: write +0x190, read +0x184 bit 1) -- and it is the guest route to a nonzero irq_status that turns
   D7's disclosure into a guest row in a later round.
PASS 1 COMPLETE: 9/9 roster seats answered (the dedicated codex extra is LATE, reconnecting since 07:10).  Ledger entries
for the assess stage are written at the round's records step, citing panel_20260919_070125 and the two agent ids.

## Dedicated codex premise audit (GPT-6 max, cxlaunch fbd5p1; LATE -- landed 07:5x after five reconnects) -- REVISE
Answer: `_scratchpad/fbd5/codex_p1/codex_fbd5p1.txt` (44 KB, verdict first).  cxlaunch.sh printed "SEAT WALLED" on the
`ERROR: Reconnecting` stderr lines although stdout carries a complete answer with a verdict -- the misreport class the
peer's #544 v7 fixes (a completed answer wins over stderr text).  Scored here as ANSWERED.
Converges on every adopted point (nine exits; no latch in the file, 0/15 fields; 0/5 new texts present; consumers of
`ENABLE CLEAR` are exactly S:402 D:612 W:489 plus gate_arm.sh:1104 indirectly; gate_hygiene has no footbridge coupling;
(f)/(h)/(i)/(k) have NO discriminator in the packet's ten rows; (c)/(j) depend on sequencing).  New, adopted:
X1 FIQ N-rows must be observed through the RAW register (+0x284): a stored 0x10/0x40 at +0x280 shows in raw, and
   `x & 0xc0` may hide it in the masked read -> arm S reads BOTH +0x280 and +0x284, and the N4/N5 value is 0x40.
X2 K2 completion = every prologue word stepped (badis empty, step count == len(prologue)) AND the fresh-reg values;
   the sites prologue ends at 0x28 (r1 = 0x00345678 there), drain 0x50 (r7), witness 0x44 (r7).
X3 After SIGKILL the reap is a BLOCKING waitpid(pid, 0) -- bounded only because a SIGKILLed child always reaps;
   recorded, not changed (a stopped/ptraced child is out of this harness's model).
X4 The per-instance boolean-int latch is in 5/121 device files; packed masks in 6/121; process-static ints in the rest
   -- the "house idiom" is a plurality of FORMS, and the choice (five ints) is Fable's Q3 ruling, not a census result.
