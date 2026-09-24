# #545 (fbdeclinefive) -- THE ADJUDICATION PASS (the panel shares its findings) + THE REPAIR'S OWN PASS 2

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY
Check the premises, not just the derivations.  This round's own records were wrong NINE times after pass 2 (listed below),
so a sentence here being confident is not evidence.  **THE TREE UNDER REVIEW IS `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\`**
at HEAD {{HEAD}} plus the uncommitted #545 working set; ignore any other `src/` under the project root.  If you cannot read
files, that is expected: the repair diff and every result are inlined.  Name any premise you cannot settle from the packet.
Ordinary engineering language: declines, latches, detector rows.  **VERDICT LINE FIRST.**

## 1. WHAT HAPPENED SINCE YOU LAST SAW THIS ROUND
Pass 2 (nine seats; Fable HELD by the owner, recorded as held, not failed) reviewed a fix that changes five footbridge
register accesses from ending the process to a declined, once-announced access, plus its detector.  **No seat found a
defect in the product change.**  Two seats found the DETECTOR below the floor:
* the Opus measuring seat MEASURED nine one-edit mutants passing every row (`len == 4` on four of five decline guards; a
  legal read re-arming a latch; a guard widened to swallow a legal narrow read);
* a dedicated codex reading found, against the already-repaired detector: `&& idata` on any latch guard (a zero-data first
  write never announces), `writeflag` rewritten as `!idata`/`idata`, a SEED COLLISION (0x18&0x30 == 0x50&0x30 == 0x10, so
  swapping `irq_status` for `fiq_status` in the IRQ_STATUS read passed), N rows that count texts over the whole arm (two
  sites exchanging texts stayed green), and gate count pins a duplicated green line could satisfy.
The main loop repaired all of it in ONE diff (section 3) and re-measured it (section 4).

## 2. EVERY FINDING AND MY DISPOSITION (full text: P2_FINDINGS.md F1-F50/D1-D10, CODEX_DED_TRIAGE.md R1-R6/W1-W6/D1-D4;
## both are inlined only in summary here -- file-reading seats: `C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\fbd5\p2\`)
REPAIRED IN-ROUND (L2 floor / row validity), each re-measured in section 4:
* F1/F20 width at every site -> X1 (len 1 and 2 as the FIRST access, every site); F2 narrowed dominating predicate -> X2;
  F3 legal read re-arms -> X3; F4 re-arm by writes/other registers -> X3 widened; F5 seed collision -> fiq_status 0x60
  (enumerated: only the correct field pair gives 0x10 / 0x40); F6 narrow declined read value -> X1 value rows; F7/R1
  `&& idata`, `&& irq_enable` -> X4 (zero data / zero enable as the first access); R2 `writeflag` -> `!idata`/`idata` -> X4 +
  X5 (a legal ZERO Clear write must not announce); R4 text exchange -> row NO (announces arrive in site order N1..N5);
  F8 floor (b) at every site -> measured (M1, M1b-M1e); F9/F45/F48 gate pins -> distinct-green-id pins, ROWS=37 of 37,
  `count=1 ` with a field boundary; F10 C4 pin added; D2-tightening: pending probes' H1 now requires no prompt ANYWHERE.
CORRECTED IN PLACE (L4): F18/F19 teardown-first claim; F22 pending headers' arm K; F23 FIQ "unpinned everywhere"; F24 S3/E5;
  F25 arms L/T/K; F26 "sibling" read for N4/N5; F27 arm E's zeros; F28 NULL-callback comment; F29 0x70; F30 device comment
  ("no register changes, only this site's warn-once latch is set"); F36 gate display line; F37 send() comment; F38 table
  wording; F31/F32/F33/F39/F40 appended as dated corrections to PRETABLE.out (never edited in place).
  **F34: #539's own record claimed its E0-E6 distinct-GREEN-id gate fix shipped; HEAD never had it (the partial-blob commit
  dropped it).  #545's commit carries it and the CHANGELOG corrects #539's record.**
DISCLOSED, NOT ROWED (contract, clause e): F11 drain/witness legs are not gate-run (their own verdict rows enforce them);
  F12-F17 the legs cannot defend their own predicates (harness edits); M13 teardown-first stays green in all three launchers;
  F41 H1/H2 do not reproduce a device-initiated mid-session exit (none remains reachable except the SDRAM pair);
  F44 the seeds violate 7.3.30's identical-raw-status rule -- synthetic state, by design (the product has no fiq_status
  writer: fiqenableread); F47 arm S loads sp/lr (safe in stepped code); F50 DEVINIT's memset half is not rowed (calloc is).
NOTED, NO ACTION: F35 (a brief citation), F42 (send() now honours 30 s), F43 (the H1 text pin reads the probe's echo --
  it fails closed), F46 (SELFCHECK lines are deliberate), F49 (cosmetic).  Out-of-scope finds already FILED: armdesc3kill,
  armdacr2kill, fbirqsoftunimpl, hygienecensus.
DISAGREEMENTS D1-D10 are in P2_FINDINGS.md; my rulings: D1 L2 (the X-repair shipped); D2/D3 inside the closure (measured
  escape, cheap row); D4 re-seeded; D5 measured at every site; D6 H1/H2 replace the harness-failability property, not the
  old device channel (disclosed); D7 fixed; D8 600f9c4b; D9 policy, :1652 + Figure 7-2 nearest; D10 wrong record, fixed.

## 3. THE REPAIR DIFF -- 22 hunks, from EXACTLY what pass 2 reviewed (HEAD + the pass-2 patches) to the tree now
(md5 {{MD5}}; the gate_arm hunk is its footbridge block only -- the working file also carries an unrelated uncommitted
section from another round, which will not be staged)

```diff
{{FILE _scratchpad/fbd5/p2r/repair.patch}}
```

## 4. THE MEASUREMENTS (table 3, scratch trees only; logs durable in regress/artifacts/fbd5/table3_20260919/)
Offline differential, 149 rows, against FIX and 34 mutants: FIX 149/149; EVERY mutant red except M9 and Z9, which change
only an announce TEXT and are guest-only by design (the differential's fatal() is a counter).
Guest (sites probe 37 rows + the two pending probes), in a clone of build/: FIX 37/37 PASS, witness and drain H1/H2/R0 ok;
Z9 (IRQ_STATUS and IRQ_RAW_STATUS exchange texts) red on NO only; M1b-M1e (exit(1) reinstated at each other site) 21/37 --
arm S dies.  gate_offline PASS 348 on the repaired tree (pins 149/78/38).  gate_arm on the repaired gate file: NOT YET
RUN (it runs alone after this pass).  The sites probe's send() comment changed after table 3 (text only).

{{FILE _scratchpad/fbd5/impl/table3/TABLE3.log}}

## 5. QUESTIONS
Q1 ADJUDICATE F1-F50 / D1-D10 / R1-R6 as disposed in section 2 -- UPHOLD / OVERTURN / REFINE / CANNOT SETTLE, one line each
   for any you would change (silence = uphold).  **WHICH OF MY ACCEPTED DISPOSITIONS IS WRONG?**  I accepted essentially
   every finding and repaired or disclosed all of them; that is a suspicious number, and agreement is not evidence.
Q2 THE REPAIR'S OWN FLOOR, on the SHIPPED COMPOSITE (guest rows + differential + gate pins): name the smallest edit to the
   FIXED device source that passes all of it now, and the row you expected to catch it.  Candidates I did NOT build: a
   latch guard conditioned on a register field NOT seeded nonzero in X4; a decline that changes the INTERRUPT OUTPUT on a
   repeated or narrow access (only the first word decline counts asserts); a legal Set/Clear write that re-arms a latch
   only when its data is NONZERO (X3's widened writes carry 0).
Q3 THE ROWS AND PINS I ADDED: can any of X1-X5, NO, or the new gate pins pass while the thing it names is false?  (The
   earlier pins failed that test; mine were written the same day.)
Q4 WHAT DID ALL NINE OF US MISS?  Standing licence: anything else you found while verifying.
End with a seat record: model, files read, nothing run / what you ran.
