# PASS 1 (DESIGN) -- `fbdeclinefive`, round 2 of the footbridge campaign: five register accesses in a direction the datasheet does not define stop ending the process; the #539 kill bridge retires; the durable harness controls land

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated
wrongly, and the previous round of THIS campaign found seven defects in its own pass-1 brief.
**Check the premises, not just the derivations.**  Where I state something as fact, ask
whether it is true.  A seat that re-derives a premise from something this brief did NOT give
it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\src\` at HEAD f685d75 (#539 shipped at 7836071; f685d75 and 9c28ca5 are RECORDS-ONLY commits, so every source and regress file named here is byte-identical at 9c28ca5 -- the pass-1 packet said "HEAD 9c28ca5" and the kimi seat caught the label).**  Copies of
`dev_footbridge.c` that are NOT this fork exist under the project root -- the live hazard is
`_scratchpad/r6pass2_fb/src/devices/dev_footbridge.c` (744 lines, a STALE FORK copy: lines off by tens, the dangerous
kind); the fork's file is 899 lines.  If your line numbers disagree with mine by tens or hundreds, say so rather than
reconciling.  Scope your reading to `GXEMUL-SEC/src/`, `GXEMUL-SEC/regress/*.py` and the named datasheet; do not read
`regress/artifacts/`, `tools/pipeline/ledger.json`, CHANGELOG.md or OUTSTANDING_BUGS.md.  Ordinary engineering
language: these are terminating calls, declines and error paths.

**If you cannot read files that is expected** — every fact you need is inlined.  Name any premise you cannot settle
from this packet rather than guessing at it.

**Where this brief states an ARITHMETIC claim — an offset, a count — ENUMERATE it rather than reasoning about it.**

**VERDICT LINE FIRST**, so your answer survives truncation.

## 1. THE DEFECT, AND WHY THIS ROUND TAKES FIVE SITES AS ONE
`DEVICE_ACCESS(footbridge)` (the DC21285 core-logic device of `-E cats`, at physical `0x42000000`) still ends the
emulator process at SEVEN guest-reachable sites after #539.  FIVE are accesses in a direction the datasheet does not
define for the register: a WRITE to a read-only status register (IRQ_STATUS +0x180, IRQ_RAW_STATUS +0x184, FIQ_STATUS
+0x280, FIQ_RAW_STATUS +0x284) and a READ of a write-only register (IRQ_ENABLE_CLEAR +0x18c).  The other two are READS
of SDRAM_BA_MASK/OFFSET (+0x100/+0x104), documented READ/WRITE registers whose write arms discard the value -- a
different class (a missing value, not an undefined direction) and a SEPARATE round (`fbsdrampair`).  The five are ONE
class under the reopening rule: same device, same semantic class (undefined direction -> the model refuses), same
detector (`regress/footbridge_sites_probe.py`), one fix design.

The datasheet, verbatim (`_scratchpad/dc21285.txt`, Intel 278115-001):
{{INLINE _scratchpad/dc21285.txt 6820 6833}}
{{INLINE _scratchpad/dc21285.txt 6886 6896}}
{{INLINE _scratchpad/dc21285.txt 6903 6909}}
{{INLINE _scratchpad/dc21285.txt 6936 6947}}
and the CSR access rule:
{{INLINE _scratchpad/dc21285.txt 1651 1653}}

## 2. PREMISES ALREADY SETTLED, RE-INLINED SO NOBODY SPENDS AN ANSWER RE-DERIVING THEM
Settled by #539 (n6): pass 1 `panel_20260919_005103`, pass 2 `panel_20260919_021100`, F2 `panel_20260919_035324`, the
fable5 rulings `_scratchpad/n6/fable5_p1_20260919.md` / `fable5_f2_20260919.md`, the codex M1/M2/K4 readings:
* **#539's kill bridge is TEMPORARY and THIS round retires it** -- fable5 D1: the three probes' "the device can still
  end the process" control is a READ of +0x18c (`ldr r7,[r0,#396]` = 0xE590718C, complaint text `ENABLE CLEAR`, K rows
  require the complaint AND exit 1); the round that declines +0x18c builds the durable harness legs IN THE SAME COMMIT.
* **The durable legs (codex M1's oracle table, adopted by fable5 as the spec):** K1 startup-rejection -- launch with an
  unused `-E` name through each probe's OWN launcher; no prompt; the unknown-emulation diagnostic names that input;
  `WIFEXITED && WEXITSTATUS == 1`.  K2 death-after-execution -- the prologue verified complete and live by a fresh
  `reg` (MMU bit clear, RAM 0x11223344, VENDOR 0x1011, the timer-mask value), then `quit`; the next ordinary interaction
  fails with `dead` BEFORE cleanup; `WEXITSTATUS == 0`.  Every surviving arm reaps exit 0.  There are THREE separately
  implemented launchers (sites' nested helpers; drain's and witness's `Session` classes): the legs go in each.
* **Device reachability is carried by value rows, not by a kill** -- A1 (VENDOR_ID 0x1011), A2 (TIMER_1_LOAD masked
  to 24 bits), and #539's E rows (E1/E2 `|=` accumulation at +0x188).  `quit` exits 0 through normal shutdown
  (`debugger_cmds.c` sets `emul_shutdown`/`exit_debugger`; `main()` returns 0).
* **The teardown as shipped by #539** (all three probes): `quit`, drain the pty to EOF (bounded 20 s; `rd()` returns
  True on a select timeout and False only on EOF/EIO), close, bounded WNOHANG reap (10 s), SIGKILL only if still
  there and not already reaped, `exit`/`signal` on every session-return path, harness kills labelled
  `HARNESS-KILL(9)` / `HARNESS-CLOSE(<sig>)`.
* **+0x18c's decline must ALSO stop returning `d->irq_enable`** (codex M2, K4 D3): today the read branch computes it
  before terminating; a decline that keeps that assignment leaks the enable mask through a write-only address.
* **The DIRECT datasheet sentence for all five is `:6803`**: "The Status and RawStatus are read-only, and EnableClear and
  Soft are write-only."  Cite it FIRST.  Table 7-1's legend ("R = Read only. Writes have no effect.") is §7.1's PCI
  CONFIGURATION SPACE legend at `:4505-4520`, extracted STAGGERED (abbreviations in one column, definitions in the other,
  pairing strictly in order); the CSR sections reuse its `R`/`WO` codes, so it TRANSFERS but is not a sentence about
  these registers (fable5 narrowing codex's C1).  For the +0x18c READ Table 7-10's read column is `--`, so in the read
  direction no CSR is selected and `:1652` ("nonexistent CSR ... zeros are read") plus Figure 7-2 (`:6814`, only RawStatus
  drives the CSR read path) are the NEAREST datasheet support -- keep the word POLICY (fable5 narrowing B4), and
* **the value a declined READ returns is 0 as POLICY, warranted by the file's own silent-decline siblings** --
  `case FIQ_ENABLE_CLEAR` and `case TIMER_1_CLEAR` already fall through on a read with `odata` 0, and `default:` returns 0
  (pass 1: grok, glm, deepseek, minimax -- the datasheet's `:1652` 'nonexistent CSR ... zeros' is an ANALOGY, these
  registers exist; `:1644` says an unsupported WRITE's data is discarded, no error action).  For a declined WRITE the
  model leaves `irq_status`/`fiq_status`/the enables and the interrupt output UNCHANGED.  FAULT is NOT available on
  ARM: `memory_rw.c` dispatches a guest exception on a failed device access for MIPS and M88K only (agy, grok, pass 1).
* **The house announce idiom** (censused 2026-09-17): a per-instance latch field + `fatal()` whose text carries an
  explicit suppression marker, `(once)` being the majority spelling; `fatal()` cannot be silenced by `-q`, which is why
  a guest-drivable diagnostic needs a latch and not a verbosity flag.  K4 proposed ONE `uint32_t warned_access`
  bit-field (bits 0-4 for these five) rather than five ints -- a proposal, not settled.
* **The default arm** (`default:` in the same switch) prints `[ footbridge: read from 0x%x ]` on every read that
  reaches it and returns 0 -- unlatched, per access, no exit.  Not this round's site; named so a decline is not
  modelled on it by accident.
* **Sub-word accesses**: the handler receives `len` and the unaligned `relative_addr`; word-aligned cases only.  The
  E3/E6 rows measured that a byte/halfword read at an aligned offset returns the low lanes.
* **What `exit_census.py` counts**: dev_footbridge.c carries NINE live `exit(1)` at HEAD 9c28ca5 (HEAD lines 565, 574,
  606, 615, 624 -- this round; 714, 739 -- the SDRAM pair; 843 and 879 in DEVINIT, construction-time) -- the pass-1 packet
  said TEN and every seat counted nine (a carried number from the pre-#539 census; corrected).  After this round: 4.
* **The file has NO latch field today** (`struct footbridge_data`, 15 fields, none a warning latch -- codex q1b, agy,
  grok); the house idiom is per-site `int` latches (`dev_wdc.c` `warned_*`, eleven of them); `dev_pcc2.c` has a
  bit-field precedent (`warned_unimpl`).  FIVE `int` fields are the choice (agy, grok: no aggregate-boolean hazard).
* **A sixth same-class site already declines SILENTLY**: `case FIQ_ENABLE_CLEAR`'s READ (+0x28c, write-only per
  7.3.33) falls through with 0, no announce, no exit -- member 2 (opus5 measured on HEAD: 0 announces over two reads;
  190h/290h reads reach `default:` and announce on EVERY access, 2 over two).  **OPEN QUESTION for adjudication, two
  seats opposed:** grok -- leave it (addition licence: it does not terminate, a new announce on a silent path is an
  addition with no measured delta); opus5 -- give 28Ch the same latched announce IN THIS COMMIT (datasheet `:6801`: the
  nFIQ and nIRQ control registers are identical; same device, same file, same class, one more bit/field and one more
  row; otherwise the controller carries FOUR dispositions for one question -- latched at 18Ch, silent at 28Ch,
  unlatched at 190h/290h -- and the SIBLING PARITY check owes a written reason).  The main loop's provisional
  disposition, UPHELD by fable5 on the reopening rule's WITNESS clause (not on the addition licence, whose transferred-
  warrant leg `:6801` IS available): a +0x28c read returns 0 on HEAD and 0 after any announce is added -- no red-pre/
  green-post symptom, only a host log line, which is a detector channel and not a defect symptom; and one field takes
  the controller from four dispositions to three (190h/290h stay unlatched), so parity is not restored -- the honest
  disposition for the whole FIQ half is ONE FIQ round, `fiqenableread`.  THREE OBLIGATIONS: the D8 contract line goes
  in the PROBE HEADER (not only PRETABLE.out); `fiqenableread` facet (2) carries Opus's sentence VERBATIM as the
  dissent; the latch form is chosen for SIX sites.
* **The IRQSoft/FIQSoft LEGAL writes (190h/290h, documented write direction `:6952-6960`) print `[ footbridge: write to
  0x190: ... ]` on EVERY access, unlatched, and do nothing** -- a documented register announced as unknown, member 7
  territory and a guest-drivable unlatched log line (opus5).  NOT this round; a sixth facet for `fiqenableread`.
* **The whole FIQ side is state with no observable consequence** (`fiq_status` never written; `fiq_enable` read only
  by the AND against it).  NOT this round; facets (3)-(5) of the filed row `fiqenableread`.
* **No guest-controllable path sets `irq_status` under single-step** (the timer assert is host-timer-driven and
  `timer_stop()` holds it at the debugger prompt; IRQ_SOFT has no case), so every status READ the rows can make returns
  0 -- a decline that also swallows the LEGAL status read (constant 0) is caught by NO step-based row (Q2(f), all seats).
  SETTLED (fable5): NO free-running row (a load-sensitive oracle the sites probe's header refuses); the P-rows in
  `diff_footbridge.c` pin it OFFLINE with a seeded `irq_status`; clause (e) reads "no GUEST row observes a nonzero
  status".  The guest route to a nonzero status is IRQSoft (7.3.34 sets RawStatus bit 1) -- `fbirqsoftunimpl`'s round.

## 3. THE CODE -- the FULL enclosing function at HEAD 9c28ca5, every exit path and the common tail
{{INLINE GXEMUL-SEC/src/devices/dev_footbridge.c 498 762}}

## 4. THE PROPOSED ROUND
**Fix (option-set member 3 for all five, DECLINE + LATCHED ANNOUNCE; member 2 silent decline is the alternative
per site):** each of the five arms stops calling `exit(1)`; the WRITE arms leave every field untouched; the +0x18c
READ arm returns 0 and no longer assigns `odata = d->irq_enable`; each arm announces ONCE per device instance with a
`(once)` marker.  Storage: K4's `uint32_t warned_access` (one bit per site, cleared by DEVINIT's memset) -- or five
`int` latches in the file's existing style; the panel chooses.  Texts (K4, verbatim):
  `[ WARNING: footbridge write to irq status? (once) ]`, `[ footbridge write to irq_raw_status (once) ]`,
  `[ WARNING: footbridge read from ENABLE CLEAR? (once) ]`, `[ WARNING: footbridge write to fiq status? (once) ]`,
  `[ footbridge write to fiq_raw_status (once) ]`.  0/5 share an exact message, so one aggregate boolean would let the
  first site suppress the other four -- one bit each.
**Detector rows -- K4's design RENAMED (A1/A2/D1 already exist on the probe and are gate-pinned: agy) and put in ONE NEW
arm `S` (not arm L, whose I1 row asserts no diagnostics: grok; and a shared latch bit is detectable only when two
sites announce in the SAME process: deepseek, agy).  The SDRAM rows are NOT this round:**
  S1 IRQ_STATUS read +0x180 -> 0 with enable 0x30 (accept side; catches masked-AND -> OR: 0x30)
  N1 write 0x10 to +0x180, a legal read of +0x184 between, write 0x10 again: state unchanged, the announce text ONCE
     across the arm (catches a store into irq_status: raw/status 0x10; the interleaved read catches a clear-on-read
     latch: grok, agy Q2(j))
  S2 IRQ_RAW_STATUS read +0x184 -> 0 (catches `odata = irq_enable`: 0x30)
  N2 two writes of 0x10 to +0x184 with a legal read between: unchanged, announce once
  S3 IRQ_ENABLE_CLEAR write 0x10 with enable 0x30 -> enable 0x20 (read at +0x188); a zero write preserves 0x20
  N3 two reads of +0x18c with enable 0x30 -> 0, 0; enables unchanged; announce once (catches the retained
     `odata = d->irq_enable`: 0x30 -- and a clear-on-read)
  S4/N4 FIQ_STATUS +0x280 with fiq enable 0xc0 (set via +0x288), the N writes carry 0x40 -- INSIDE the 0xc0 mask, so a
     store-into-fiq_status mutant moves BOTH +0x280 and +0x284 (the packet's 0x10 & 0xc0 == 0 would have moved only the
     raw register: opus5, measured);  S5/N5 FIQ_RAW_STATUS +0x284 likewise.  NOTE the FIQ enable is UNOBSERVABLE from the
     guest by any route today (opus5 measured: enable 0xc0 set, +0x280/+0x284/+0x288 all read 0 -- `fiqenableread`, and
     `d->fiq_status` has NO WRITER anywhere in the tree), so S4/S5 pin the VALUE 0 and catch `odata = fiq_enable`
     (measured red at 0xc0) but CANNOT see the read EXPRESSION (`m_fiqraw`, drop the `&`, escaped 29/29).
  N0 ALL FIVE sites in ONE process (this is the arm itself): the count of DISTINCT announce texts is 5 -- measured 5 on
     the fix, 4 under a two-site shared latch, 1 under a single aggregate latch (opus5, `s8_all5.out`).  Per-site
     one-process-per-row designs are BLIND to a shared latch BY CONSTRUCTION (two total escapes, 29/29 each).
     With five `int` fields a shared bit is impossible, but a copy-paste testing the WRONG field is not -- N0 catches it.
  N6 one BYTE write (strb) to +0x180: declined and announced under the same latch -- the predicate is `writeflag`,
     not `len`, so a `&& len == 4` conjunct on the decline would escape word-only rows (grok)
  Each N row's "once" is a COUNT of that site's announce text across the whole arm (0 = silent decline or a shared
     latch, 2 = unlatched); the arm must SURVIVE with exit 0 (a remaining terminating path = missing continuation).
  EVERY N row reads back BOTH register families (+0x180/+0x184/+0x188 and +0x280/+0x284/+0x288) so a FIQ-site decline
     storing into IRQ state cannot escape FIQ-only checks (codex Q2 e); the announce text is matched ACCESS-LOCALLY per
     row, never by a combined count (codex Q2 g).
  P-rows (rung-1 DETECTOR; `regress/diff_footbridge.c:99` already #includes the device and callocs an instance, and
     `:382-603` call `dev_footbridge_access` directly): seed `irq_status = 0x10`, `irq_enable = 0x30` BY DIRECT FIELD
     WRITE -- never through a +0x188/+0x18c write, because `d->irq`'s interrupt callbacks are NULL under calloc and the
     enable arms call INTERRUPT_ASSERT(d->irq) (the carrier's NULL-callback stub artefact; fable5) -- then drive each of
     the five declined accesses and the legal status READS through the handler; assert every field unchanged and
     IRQ_STATUS == `irq_status & irq_enable`.  Kills `m_swallow` and the store-into-status class as MEASURED kills;
     `m_fiqraw` is only NARROWED (seeding `fiq_status` pins an expression no product code feeds; clause (e) keeps
     "no guest can reach a nonzero FIQ status").  The differential's `fatal()` stub COUNTS and discards the text, so the
     misname check stays a GUEST-row obligation.  The SPLIT is named in the contract: guest rows = reachability,
     survival, latch count, TEXT; differential rows = preservation, expression.
  Harness corrections riding in the same commit (codex): arm T's exit status is recorded but never required == 0;
     row C4 accepts a MISSING vendor value (`None != 0x1011`); sites `send()` drops its timeout argument; the K2
     prologue check is SCORED (drain's old K discarded `step_and_check()`'s result; witness's ignored badis/nsteps).
  PRETABLE mutants for the legs: move `close()` ahead of the death observation (must red K2); omit K2's `quit` (the
     next `reg` must SUCCEED and K2 must FAIL); K1 on a matching diagnostic with exit != 1 (must red).
  CONTRACT disclosure (clause e): no GUEST row observes a NONZERO status (Q2(f): `m_swallow`, a constant-0 IRQ_STATUS read,
     escaped 29/29 -- opus5 armed timer 1 and spun 24 steps, +0x184 still 0, host timers are stopped at the prompt);
     the FIQ read EXPRESSIONS are unpinned (`fiq_status` has no writer); S1/S2/S4/S5 pin the value 0 and catch a
     WIDENING (`&`->`|`, `odata = enable`), never a NARROWING to a constant.  +0x28c: see the OPEN QUESTION below.
     IRQ_SOFT/FIQ_SOFT reach `default:`.
  ZEROING: `DEVINIT`'s memset (:771) is ONE of TWO zeroing paths -- `regress/diff_footbridge.c:151` and
     `regress/diff_fbpending_bound.c:143` `#include` the device and `calloc` their own instance (opus5); both zero the
     new fields, so neither differential changes.
**The kill bridge retires and the harness legs land in the same commit:** arm K's +0x18c read (sites), the drain's and
the witness's K arms are REPLACED by the K1/K2 legs (through each probe's own launcher, against THAT launcher's register
map -- the timer-mask value is in r1 on sites and r7 on drain/witness: grok), and `gate_arm.sh`'s "the one-instruction
kill arm still dies" check is replaced by checks pinning the legs' PREDICATES (K1: `WIFEXITED && status == 1` AND the
`Sorry, emulation "<name>"` text naming the input -- `-H`/usage also exit 1; K2: `dead` observed on the interaction
after `quit` and BEFORE close(), after a fresh `reg` proved the prologue live).  The drain and witness probes are not
gate-run; their legs are enforced by their own verdict lines.  After this round no footbridge access these probes make
ends the process; the function still terminates on the two SDRAM reads (`fbsdrampair`).
**Witness (rung 3):** the new rows on HEAD 9c28ca5 -- D1..D5 and D3's read die at their first undefined-direction
access (exit 1 with the site's complaint) -- red pre-fix, green post-fix with the same script.
**Gate:** `gate_arm.sh`'s footbridge section gains count + value pins for the new rows (the same shape as the E pins).

## 5. THE THREE CONTROLS' CURRENT KILL ARMS (what this round removes), verbatim
{{GREPN GXEMUL-SEC/regress/footbridge_sites_probe.py KILL_LOAD}}
{{GREPN GXEMUL-SEC/regress/fbpending_drain_probe.py 0xE590718C}}
{{GREPN GXEMUL-SEC/regress/fbpending_witness.py 0xE590718C}}
and the sites probe's K row:
{{GREPN GXEMUL-SEC/regress/footbridge_sites_probe.py k_ok}}

## 6. QUESTIONS
**Q1 -- premise audit, as questions.**
 (a) For each of the five sites: is the datasheet direction as stated (quote the section)?  Is member 3 right for it,
     or is there a site where member 2 (silent) or member 4/5 (the model already computes something; a fault) is
     the honest disposition?  Is FAULT even available on ARM for this machine (grep the fork: `dev_unreadable`,
     `memory_rw` exception dispatch for ARM)?
 (b) One `warned_access` bit-field vs five per-site `int` latches: which matches the file's existing idiom (grep its
     latch fields), and does the bit-field create a "who else writes this field" collision hazard?
 (c) The K1/K2 legs: do they establish what the old kill arm established (death detected; death detected AFTER guest
     steps) in each of the THREE launchers, and is "the next ordinary interaction fails with `dead` before cleanup"
     observable through each probe's `send()`/`wait()` as written?  Quote the helper you checked.
 (d) After this round, is the statement "no footbridge access these probes make ends the process" TRUE?  Enumerate
     every `exit(` in the function and say which guest access reaches it.
 (e) Does anything in the tree read or depend on the five complaint texts or on `ENABLE CLEAR` (a gate grep, a
     hygiene allowlist, `gate_hygiene.sh`'s boot-log rules)?
**Q2 -- candidate weakenings (which row reds first, or escapes).**
  (a) a decline that keeps `exit(1)` at ONE of the five sites   (b) the announce unlatched (fires every access)
  (c) one latch bit shared by two sites (the second never announces)   (d) +0x18c decline that keeps
  `odata = d->irq_enable`   (e) a WRITE decline that stores the written value into irq_status anyway
  (f) a decline that ALSO swallows the legal direction of the same register (IRQ_STATUS READ returns 0 always)
  (g) the announce text misnames the register   (h) K1's startup leg passing on ANY nonzero exit
  (i) K2's quit leg passing when the child died BEFORE the prologue completed   (j) the latch cleared by a read
  (k) the harness legs implemented in one launcher only
**Q3 -- option-set completeness.**  DELETE / DECLINE / DECLINE + LATCHED ANNOUNCE / ACCEPT / FAULT / BACKED ACCEPT /
  IMPLEMENT.  Member 3 is proposed for all five.  Is there a member this brief did not weigh for any site?  Grep the
  fork for the sibling handlers' dispositions (`dev_footbridge.c`'s other arms; `dev_unreadable.c`).
**Q4 -- the harness change's own risk.**  Replacing a kill arm with two legs in three launchers is the largest
  harness edit of the campaign.  What is the smallest edit to the LEGS that leaves them green while proving nothing?
  Name the row you expect to stay green.
If, while verifying a claim, you found something ELSE -- say so.
End with the seat record: model, what you read, what you ran (nothing).
