# Opus 5 seat, n6 pass 1 (2026-09-19 00:51-01:05) -- summary of the returned answer (full text in the agent transcript;
# every number below is from its measurements in /tmp/gxopus539p1, transcripts in this dir)

VERDICT: GO on the fix and on every E-row expectation (E0..E6 MEASURED correct on a post-fix build of the proposed
diff, applied in the clone under a sentinel; pre-fix control dies at E0).  GO on the +0x100 control move (exit 1 +
`footbridge read from sdram_ba_mask`, NO "WARNING:" prefix -- match on `sdram_ba_mask`).  The "three controls move in
the SAME commit" premise is MEASURED: on the post-fix build the unmodified sites probe reds K1 (exit=0, 9 of 10).

MUST CHANGE BEFORE COMMIT:
 1. Q2(j) `if (d->irq_status | d->irq_enable)` in the write arm = TOTAL ESCAPE of the whole proposed row set and every
    existing sites row (zero value differences, zero diagnostics).  No step-based row can catch it: cpu_dyntrans.c:204-206
    suppresses interrupts under single-step (ARM inside the block), and the guest CPSR has I,F set.  Catching it needs a
    FREE-RUNNING arm (sh_intprio_probe.py shape: marker at vector 0x18, CPSR I cleared, write P, bra ., breakpoint,
    continue) -- or a named clause-(e) disclosure.  Opus's own judgement: clause-(e) debt (sibling arm of the dominating
    writeflag predicate), but debt this round creates visibility for; build the arm or name the cell.
 2. The brief's REASON for P/Q inertness (the DC21285 bit table) is not operative: d->irq_status measures 0x00000000 at
    all five reads, so ANY enable pattern is inert under single-step.  State the measured warrant; the bit-table one
    would be wrongly reused.  Scope: single-stepped, host timers stopped -- not a booting guest.
 3. E3/E6 "the access width is a dominating input" is incomplete: the dominating input is the PAIR (exact byte
    address, len).  A sub-word read returns the LOW len bytes of odata (ldrb +0x300 -> 0xef, ldrh -> 0xcdef) and reaches
    the case only at the exact constant; +0x301/+0x302 fall to default:, return 0 with an UNLATCHED
    `[ footbridge: read from 0x30x ]`.  Pre-existing; belongs in the clause-(e) contract sentence.

ALSO MEASURED:
 * Mutant (e) keep fatal(), drop exit(1): SIX unlatched ENABLE SET diagnostics from six reads; E4 is the SOLE carrier
    (every value row green).  Argues for ACCEPT over member 3: a bounded announce would need a latch the site lacks.
 * +0x18c (IRQ_ENABLE_CLEAR read) dies today with exit 1 + `ENABLE CLEAR`: a ready DECLINE-class sibling, not a durable
    Q4 answer.
 * Q4: `-T` is NOT a failability control (reads of PA 0x90000000 / 0xe0000000 survive, exit 0, r=0).  BETTER CONTROL:
    an UNCLAIMED footbridge offset reaches default:, prints `[ footbridge: read from 0x301 ]` and does not exit -- a
    diagnostic-PRESENCE control proving the guest reaches the handler (the kill pair's stated purpose), costs one
    instruction, needs no future move, survives the whole eight-site campaign.  Could REPLACE the +0x100 move.  Must
    live in its own arm (sites I1 asserts `not L["fatals"]`).
 * Q1(d) tree-wide: `ENABLE SET` consumed by 0/21 regress/*.sh, 3/103 regress/*.py (the three probes), the site, the
    ledger/matrix (records), and frozen artifacts -- nothing else.
 * M4: drain :405 and witness :353 discard the waitpid status (no WEXITSTATUS anywhere in either file); sites :208/:291
    checks text AND status.  Only footbridge_sites_probe.py is gated (gate_arm.sh:1073).
 * Encoding: 0x188 is not an encodable rotated immediate and LDRH's offset caps at 255 -> `add r8,r0,#0x180`
    (0xE2808D06) then `ldrh r9,[r8,#8]` (0xE1D890B8).
 * Baseline discipline: it REVERTED the six uncommitted src/ edits of other rounds inside its clone, so its numbers are
    of the COMMITTED build 408accf + the proposed hunk (artifacts/dev_footbridge.PROPOSED_FIX.c).  Clone removed.
NOT CHECKED (by its own statement): fiqenableread joining the round; FAULT on ARM; mutants a,b,c,d,f,g,h,i,k; booting-guest behaviour.
