# n6 (#539) PASS 1 -- ADJUDICATION PACKET FOR THE FLAGSHIP SEAT (fable5), fired LAST after all other seats answered

Open your answer with the token FABLE_SEAT_ALIVE_20260919_N6P1 and the verbatim first line of
`C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\CHECKPOINT.md`.  VERDICT LINE FIRST.  You hold two hats here: the ninth review
seat, and the adjudicator of the panel's findings.  Read-only: no edits, no builds, no gate runs.  The tree is
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\` at HEAD 408accf; pristine 2021 copies under the project root are not this fork.

## THE ROUND
Design brief (rebuilt at 408accf, then corrected by this pass -- read the CORRECTED template for the current design):
`C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\n6\brief_n6_design.tpl.md` (template) / `brief_n6_design_BUILT.md` (the packet
the seats saw, with the defects they found).  One site: `dev_footbridge.c` `case IRQ_ENABLE_SET` read branch --
delete the `fatal()` + `exit(1)`, keep `odata = d->irq_enable` (option-set member 4, ACCEPT: the DC21285 says +0x188
IRQEnable is readable, reset 0, changed only via Set/Clear).  Rows E0-E6 on `footbridge_sites_probe.py`; the three
probes' "the device can still end the process" control arms move off +0x188 in the same commit.

## THE SEATS (all answered; read the bodies, not only the verdict lines)
  `_scratchpad/panel_20260919_005103/`: agy.txt GO-WITH-CHANGES; grok.txt ACCEPT (4 defects in the brief); kimi.txt
  (kimi CLI, file-reading, 197 KB) CONFIRM ACCEPT + defects + a Q4 design; ollama_glm.txt ACCEPT after five fixes;
  ollama_deepseek.txt ACCEPT; ollama_minimax.txt ACCEPT (no verdict line; eight premises it could not settle);
  ollama_kimi.txt (kimi-k3:cloud, packet-fed) ACCEPT + defects.  codex.txt = REFUSED by the provider content filter
  (a SEAT FAILURE, not an answer; `_scratchpad/n6/CODEX_REFUSAL_p1_20260919.txt`); re-fired ONCE in pointer form:
  `_scratchpad/cxfarm2_20260919/out/codex_k5_n6panel_refire.txt` REVISE THE BRIEF (ACCEPT right; 9/11 variants
  distinguished).  Plus two dedicated codex jobs: `_scratchpad/n6/codex_dedicated_20260918/codex_n6ded.txt` (16 variants
  classified, the control-arm premise refuted) and `_scratchpad/n6/codex_p1_20260919/codex_n6p1.txt` (7/7 rows
  checked, 4/17 premises refuted, 3/3 controls verified).  Opus 5 (measuring seat): `_scratchpad/n6/opus_p1_20260919/
  OPUS_SUMMARY.md` -- E0-E6 MEASURED correct on a post-fix build in its own clone; mutants (e) and (j) built.

## CONSOLIDATED FINDINGS, WITH MY DISPOSITION ON EACH (16)
 F1  Q stated as both 0x20000000 and 0x60000000 (every seat).  ACCEPTED -> template fixed to 0x60000000 throughout.
 F2  "Q2(l)" cited but absent from the Q2 list (agy, glm, kimi, codex).  ACCEPTED -> (l) added: diagnostic kept only
     for bits 30/31; E2 with bit 30 set observes it.
 F3  E5/E6 order: E6 (halfword 0x2002) is true only while irq_enable == P|Q; listed after E5 it reds on CORRECT code
     (kimi, grok, ollama_kimi, codex check).  ACCEPTED -> order pinned E0,E1,E2,E3,E6,E5; E4 anywhere after E0.
 F4  The sites probe dumps registers ONCE per arm and rows C1/C2/A1/A2/A2b read r1-r6, so E-rows need r7+ or a new arm
     (grok, kimi).  ACCEPTED -> implementation constraint (a codex draft, cxfarm4 M3, is pending).
 F5  "Seven invalid-direction sites" is FALSE: five are (writes to RO status regs, a read of a WO reg); two are reads
     of SDRAM_BA_MASK/OFFSET, documented R/W (dc21285.txt:5853, :5906) whose write arms discard the value (grok,
     kimi, codex x2).  ACCEPTED -> template corrected; consequence: a control parked at +0x100 dies in the SDRAM
     round, probably the next one.  (cxfarm2 K4 codex dissents: keep 7/7 in one DECLINE round since 2/7 have no
     storage -- see D4.)
 F6  P/Q inertness: the bit-table reason is NOT the operative one -- Opus MEASURED d->irq_status == 0 at every read,
     so any pattern is inert under single-step.  ACCEPTED -> warrant restated as measured; P/Q kept.
 F7  Mutant (j) `irq_status | irq_enable` in the write arm: MEASURED TOTAL ESCAPE of every proposed and existing row;
     no step-based row can catch it (cpu_dyntrans.c:204-206 suppresses interrupts under single-step; CPSR I,F set).
     A free-running arm (marker at vector 0x18, CPSR I cleared, write P, breakpoint, continue) would.  Opus's own
     judgement: clause-(e) debt (sibling arm of the dominating writeflag predicate; the repair path reads only
     irq_enable) -- but debt this round CREATES visibility for.  MY DISPOSITION: build the free-running arm in this
     round if it costs one arm; else disclose the cell by name in the contract.  -> D2.
 F8  Mutant (e) keep fatal(), drop exit(1): six unlatched ENABLE SET diagnostics; E4 is the SOLE carrier (Opus).
     ACCEPTED -> E4 stays; and it argues for ACCEPT over member 3 (no latch exists at the site).
 F9  "Width is a dominating input" is incomplete: the pair (exact byte address, len) is; +0x189/+0x18a fall to
     default: and return 0 with an UNLATCHED per-access diagnostic (Opus, measured).  ACCEPTED -> clause-(e) contract
     sentence; pre-existing, no row owed.
 F10 The MMU-on zero is NOT a RAM alias: -M 32 ends at PA 0x02000000, the zero is memory_rw.c's out-of-RAM fill
     (codex check).  ACCEPTED -> template corrected; the expected value stands.
 F11 fbpending_drain :405 and fbpending_witness :353 DISCARD the waitpid status; only the sites probe checks text AND
     exit 1 (codex dedicated, Opus M4, deepseek).  ACCEPTED -> fix in THIS round (bind status; kill arm requires
     WIFEXITED && status 1, surviving arms status 0); the peer's class row `ptywaitstatus` names these two as
     "fixed in #539".
 F12 fiqenableread (+0x288 read returns 0, no odata assignment, no exit): SEPARATE round -- different class (a missing
     value, not a computed value discarded) (grok, agy, deepseek, codex check, kimi).  ACCEPTED -> stays filed; kimi's
     three FIQ facets (no fiq interrupt in the struct, dead FIQEnable writes, the read) fold into that row.
 F13 minimax: E0's "want 0" depends on DEVINIT not preloading irq_enable.  SETTLED by measurement: Opus E0 = 0 on the
     post-fix build (struct zeroed at :769).
 F14 kimi standing licence: IRQSoft (+0x190) / FIQSoft (+0x290) have NO case -- a guest softint write lands in default:
     and sets nothing (FILE as a new row, not this round); stale dev_footbridge.c line cites inside all three probes
     (:423, :486-499, :548 -> 514, 587-589, 640) and fbpending_witness.py:35's rationale, false once n6 lands (FIX
     in-round: the round touches all three files; cxfarm4 M4 is auditing every citation); gate_arm.sh:1074's excerpt
     grep will not echo E-rows (cosmetic).  ACCEPTED as stated.
 F15 (g) `reinstate only when irq_enable == 0` is caught ONLY by E0 (agy) -> E0 is load-bearing; keep.  ACCEPTED.
 F16 Process: the inline 26 KB brief was refused by codex's content filter; the pointer-form re-fire answered.  So the
     trigger is inlined kill-arm/exit code, not vocabulary.  RECORD as a seat failure + a BRIEF_TEMPLATE §C5 note
     candidate (not edited here: the template is a never-commit file with unreviewed deltas).

## DISAGREEMENTS (both sides in their own words)
 D1 THE FAILABILITY CONTROL for the three probes once +0x188 no longer exits.
    (a) the brief: move to a +0x100 read now (Opus VERIFIED it works: exit 1, `sdram_ba_mask`), move again later.
    (b) Opus: "an unclaimed footbridge offset reaches default:, prints `[ footbridge: read from 0x301 ]` and does not
        exit -- a diagnostic-PRESENCE control proving the guest reaches the handler ... costs one instruction, needs
        no future move, survives the whole eight-site campaign.  This is a better answer to Q4 than +0x100, and it
        could replace the move rather than following it."  (Must live in its own arm: I1 asserts no fatals in arm L.)
    (c) kimi CLI: "build the permanent control now, in this commit, and skip the +0x100 bridge ... Exit-status leg:
        spawn the binary once with a bad argument (unknown -E machine) ... pins the same plumbing K1 pins with zero
        dependence on any model defect.  Mid-session death leg: after the prologue steps, send debugger `quit` ...
        require s.dead on the next interaction AND bound status == 0 ... The 'guest actually reaches the device'
        function of the old kill pair is already subsumed by value rows -- A1/A2 today, and E2's |= accumulation."
    A codex comparison of the three (cxfarm4 M1) is pending.  MY LEAN: (b) for "the guest reaches the handler" plus
    (c)'s status legs for the harness plumbing, and NO +0x100 bridge -- but this is the round's design question and it
    is yours to rule.  Consider the round's SIZE (one site per round) when ruling.
 D2 Mutant (j): free-running arm THIS round (Opus's shape; ~one arm) vs disclose as clause-(e) debt (Opus's own
    grading).  My lean: build it if the m88k-style free-run shape ports to ARM in one arm; the cost is bounded.
 D3 FIQ read: separate (majority) vs "FIQ is unmodeled end-to-end, one item three facets" (kimi) -- I read these as
    compatible (separate round, one row); rule if you disagree.
 D4 Campaign order after n6: the SDRAM pair as BACKED ACCEPT (needs two state words -- addition licence: what
    warrant?) before or after the five declines; K4 codex: keep all seven in one DECLINE round because the two SDRAM
    sites "have no functional configuration storage" and legal writes cannot be claimed to implement the datasheet.
    Not this round's fix; rule for the record so the next brief starts right.

## QUESTIONS FOR THE ADJUDICATOR
 Q1 Rule D1-D4.
 Q2 WHICH OF MY 16 ACCEPTED DISPOSITIONS IS WRONG?  Name the number and what settles it.
 Q3 What does this round still OWE before implementation may start -- a PRETABLE (the round ships a kill-table-backed
    detector), the rung-3 witness (the sites probe's K arm dying at +0x188 with exit 1 IS the pre-fix red -- is that
    sufficient as the witness?), anything else?
 Q4 Standing licence: anything the nine seats and the three codex readings all missed.
End with the seat record line: model, what you read, what you ran (nothing), and where your answer is saved
(`C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\n6\fable5_p1_20260919.md`, write it there verbatim).
