# ADJUDICATION PACKET for 2026-09-09 -- Fable 5

Written 2026-09-08 by the main loop, for the session in which Fable's usage resets.
Nothing in this file is a substitute for the ledger rows; it is an index with dispositions,
so the adjudication spends its budget on decisions rather than on reconstruction.

## *** READ THIS BEFORE ANY CLAIM BELOW: THE OPENING GUARANTEE WAS FALSE AND IS WITHDRAWN. ***

This packet used to open: *"Every claim here is either MEASURED (with its log named) or marked as
MY JUDGMENT."*  **Two audits of this document found that false**, and the second stated the defect
precisely: the packet contains at least FIVE evidentiary categories, and the boundary breaks
wherever *"the facts are the seats'", "settled by me", "therefore"* and *"proven"* turn a REPORT or
an INFERENCE into an apparently measured fact.

    1  MEASURED          a named, VERSION-SPECIFIC log result.  Version matters: "46/46" is true
                         of five different probe versions in this round, one of which did nothing.
    2  SOURCE-DERIVED    read from code, with its assumptions stated.  Not run.
    3  SEAT FINDING      an attributed answer, ideally quoted.  A seat's reasoning, not a fact.
    4  PREDICTION        asserted, not verified.  The M13 44/44 escape is the clearest example --
                         it is a prediction with a mechanism and was never re-measured.
    5  MY JUDGMENT       severity, priority, policy, routing.  Recognisable in the B1 severity
                         raise, the A2 disclosure decision, and the C no-checker decision.

**WHERE THAT LEAVES THE READER:** treat every unlabelled claim as category 2, 3 or 4 until its log
is named.  The measurements that ARE version-specific and logged are listed in A1 and A2 and were
independently verified line-by-line by a separate audit that read the archive
(`codex_packetaudit_20260908.txt`); every headline number held.

**AND A SCOPING NOTE THAT IS NOT A DEFECT:** the second audit marks many claims UNSUPPORTED --
seat totals, tree cleanliness, commit `7a41b3f`, the pass-3 vote, the unread-review instance.  **It
was forbidden from reading `regress/artifacts/` and the ledger**, and says so: *"This is a scoping
finding, not a claim that they are false."*  The FIRST audit read the archive and verified those.
*The two are complementary: one checked the measurements, the other checked the epistemics.*

**SEATS USED TONIGHT, by name, per the seat-ledger rule:**

    codex GPT-6 Astra (max)   5 substantive answers, 1 PROMPT-LEVEL REFUSAL (see D1)
    grok 4.6 (xhigh)          3 substantive answers, including two that overturned my designs
    glm / deepseek / minimax  answered the sgirandomcolour design pass
    kimi                      CLI walled; covered by the kimi-k3:cloud substitute (PACKET-FED)
    agy                       DELIBERATELY NOT FIRED -- measurement reserve, 2026-08-30 ruling
    Opus 5, Fable 5           DELIBERATELY NOT FIRED -- preserved for THIS adjudication

**No seat failed unexpectedly.**  The one refusal is a characterised, reproducible capability limit.

---

## A. THE ROUND IN FLIGHT

### A1. `#513 sgirekills` -- fix applied and measured, NOT YET COMMITTED

    witness       PREFIX_RED_20260908.out   30/44  committed build, re-pinned oracles
                  POSTFIX_20260908.out      44/44  same script after the fix
    kill table    killtable_20260908/       12 mutants, scratch clone, frozen instrument
    trees         part 1 CLEAN on all four; build/ PART2_CLEAR; **build-asan/ PART2 STALE**

Five read arms became ACCEPT; `CRIME_RE_TEX` became a latched decline on its own bit.

**WHAT I WANT ADJUDICATED:** the TEX asymmetry.  Five siblings accept and one declines, and the
warrant is `sgitexindex` -- the TEX write index is a missing factor of four, only 31 of 112 cells
are reachable, `re_tex` has NO consumer, and `sgitexindex` carries a do-not-code ruling.  **Is
declining the read the right disposition, or does it entrench an asymmetry a later round must
undo?**  The row's own `hold_question` puts the counter-case: a MIRRORED accept would round-trip
per frame while shipping hardware-wrong reads at overlapping offsets.

**MEASURED, and it is the reason I am not treating the design as settled by me:** the design panel
REFUSED my first row set with two floor-shaped holes, and the kill table then measured both:

    M4_readshift  43/44   read-side index re-map -- caught ONLY by the window's LAST-SLOT row
    M7_farbound   43/44   far-bound shrink      -- caught ONLY by the last-slot row
    M8_texaccept  40/44   TEX -> ACCEPT         -- reds all four TEX rows, but see below

**Under my original base-only design, M4 and M7 would both have swept clean.**

*** TWO CORRECTIONS TO THE LINE ABOVE, from the packet audit. ***  **Only TWO of the four TEX rows
are store-first** (`tex ld lo`, `tex ld hi`); the other two are announcement-count rows and fail M8
simply as 0-against-1.  **And M8 does NOT establish the value of the store-first shape at all** --
its two value rows also lose the announcement, so it cannot isolate what I said it isolated.  That
withdrawal was recorded in the ledger and had NOT been carried into this packet until now.

---

### A2. *** THE `#513` REPAIR CHAIN -- THREE PASSES, AND THE THIRD FOUND THAT MY REPAIR
### CLOSED ONE CELL OF FIVE.  This is the item most worth an adjudication. ***

    pass 2   6 seats, ALL answered.  codex named ONE latch-collision cell (bit 8) with a
             predicted 44/44 sweep and its mechanism.  Repaired: 2 same-instance rows, both
             orderings.  MEASURED: BASE 46/46 clean, M13 44/46 KILLED.
    pass 3   6 fired, 5 answered (codex REFUSED -- see D3).  **ALL FIVE said DO NOT CLOSE**
             (grok "DO NOT SHIP", glm/kimi "DO NOT CLOSE THE CHAIN", deepseek "NOT CLOSED",
             minimax "NOT CLEAN CLOSE").  An earlier draft said FOUR; I undercounted my own panel.
             The repair closed bit 8 and left bits 6, 7, 9, 10 -- the SAME one-token operator
             on the SAME edited line.  kimi: "L2 stands, unrepaired."
    closure  tex xbit widened from bits 0-5 to **bits 0-10** -- ONE row, not four -- and made
             SELF-CHECKING (it wants `1/11`: the TEX decline once AND all eleven other announces).
             MEASURED: BASE_fixed 46/46; M_bit6/7 45/46 KILLED; M_bit9/10 45/46 KILLED.
             *** THE CLASS IS CLOSED.  An intermediate form covered bits 0-8 and DISCLOSED 9 and
             10; that disclosure was WITHDRAWN AND REPLACED BY COVERAGE, so the rule-conflict this
             section used to raise for adjudication NO LONGER EXISTS. ***

**THREE THINGS I GOT WRONG, all recorded in the row:**

1. **My `#392` rebuttal was a strawman.**  I argued that rowing latch pairs is unbounded; kimi
   showed the cover is **LINEAR** -- the edited latch against each other used bit -- not quadratic.
   I had imagined all pairs; the closure needs only the edited one.
2. *** I REPRODUCED THE `#499` SHAPE WHILE CLAIMING TO AVOID IT. ***  I rowed both ORDERINGS of one
   colliding bit and called that the symmetric-cell repair.  The symmetry that mattered was across
   BITS, not across orderings.
3. **THE UNREAD-REVIEW CLASS, FOURTH INSTANCE, AND THE COST WAS A FULL PASS.**  grok's PASS-2
   answer had already named bits 6, 8, 9 AND 10.  codex named only bit 8.  I integrated the
   narrower answer and shipped it.  **I had the file open** -- I quoted grok's resolution of glm's
   objection from twenty lines above the passage I missed.  *When two seats answer one question,
   DIFF them.*

**WHAT I WANT ADJUDICATED:**
* ~~**Is the bits 9/10 DISCLOSURE acceptable, or a breach?**~~  **WITHDRAWN -- the cells are now
  COVERED and MEASURED KILLED, so there is nothing to adjudicate.**  The rule conflict was real
  (the class-closure amendment permits disclosure; kimi and grok held that an in-closure cell on
  the edited line is a breach regardless) and I resolved it by closing the cells rather than
  asking anyone to choose.  *The "settling fact" I had recorded as unknown was one grep away, in a
  shipped probe that already drives the drawing engine.*
* **Does the chain close at pass 4?**  The amendment says the closing pass VERIFIES THE ENUMERATION
  rather than hunting cells, which terminates.  Pass 4 is owed and not yet fired.

### A3. *** THIS PACKET WAS AUDITED BY codex AGAINST THE LOGS, AND IT FOUND FOUR DEFECTS. ***

`regress/artifacts/sgirekills/codex_packetaudit_20260908.txt`.  Every headline number was verified
against a named log with a line citation and **all of them hold**: 30/44, 44/44, 46/46, 12 of 12,
M4/M7 43/44, M8 40/44, M13 44/46, M_bit6/7 45/46, and the row arithmetic
`35 - 6 + 14 + 1 + 2 = 46`.

**What it found wrong is above, corrected in place:** the four-vs-two store-first rows, the stale
bits-0-8 description, the undercounted pass-3 verdicts, and an M8 claim I had withdrawn in the
ledger without propagating here.

*** AND ONE HAZARD I CREATED THAT SURVIVES THE CORRECTIONS: "46/46" IS CORRECT FOR SEVERAL
DIFFERENT INSTRUMENT VERSIONS, AND THEY MUST NOT BE CONFLATED. ***  `POSTFIX46`, `BASE_pass2`,
`BASE_pass3`, `BASE_pass3b` and `BASE_fixed` all read 46/46 against *different* probes -- including
one whose drawing-engine setup did nothing.  **A reader who treats them as one measurement will
conclude the self-check was always present.**  The only 46/46 that proves the setup fires is
`BASE_fixed`, whose row reports `1/11`.

## B. CRITICAL ROWS ADVANCED TONIGHT -- ready for a disposition

### B1. `alphatbinegsel` -- *** I RAISED THIS med -> high AND THE RANKING IS MY JUDGMENT ***

**The defect is source-confirmed by two seats independently, with citations I re-verified myself:**
`ALPHA_TBIA()` -- the OS primitive meaning *invalidate every TLB entry* -- is
`alpha_pal_tbi(-2, 0)`.  `a0` is `uint64_t`, the dispatch is `if (a0 >= 1)`, so `-2` compares as
`0xff..fe` and takes the **VADDR** branch with `a1 = 0`.  **It therefore invalidates cached virtual
page ZERO and nothing else.**  Every other mapping survives a flush the guest OS believes succeeded,
and the Alpha fast path keeps consuming the surviving `host_load`/`host_store` pointers.

*** AND MY OWN SENTENCE UNDERSTATED IT, WHICH THE ASSESS PANEL CAUGHT: `ALPHA_TBIAP()` IS
`alpha_pal_tbi(-1, 0)` AND MISDISPATCHES IDENTICALLY. ***  So it is not one primitive but two, and
the second is the **per-process flush used on context switch** -- glm: *"the context-switch
primitive is equally broken; this strengthens Q1 and matters for the ordering."*  agy's verdict
line names both wrappers independently.

    verified by me:  ALPHA_TBIA macro passes a1=0; the a0 >= 1 dispatch; vaddr_mask defaults to
                     (int64_t)-1 on 64-bit; the alpha binding site
    repair           if (a0 >= 1 && a0 <= 3)   -- COARSE: it does not give TBIAP its ASM=0 semantics
    witness          DESIGNED by grok, NOT BUILT

**QUESTION 1 (severity):** the facts are the seats'; the med -> high raise is mine.  A documented
*invalidate everything* primitive clearing one page, silently, with a guest reaching stale physical
backing -- I put that in the same class as the other HIGH rows.  **Confirm or correct.**

**QUESTION 2 (ordering):** codex ranked `alphaswpctxreg` FIRST and labelled that *"a confidence
judgment, not a claim that it has the greatest potential severity"* -- explicitly because this row's
consequences were then unverified.

*** AN EARLIER DRAFT SAID "THEY ARE NOW VERIFIED".  THAT OVERCLAIMED, and the assess panel caught
it: what is verified is the DISPATCH; the witness is DESIGNED, NOT BUILT, and codex's own status
line was "source-confirmed functional defect; witness unvalidated". ***  glm: *"'witness
constructible, shape known' is not verification -- do not promote this row to first on the packet
as written."*

*** THE FIVE ASSESS SEATS SPLIT 2-3 AGAINST PROMOTION -- AND I FIRST WROTE THAT TALLY AS "3-1 IN
FAVOUR", FROM MEMORY RATHER THAN FROM THE FILES.  Corrected before this packet shipped. ***

    kimi        THIS ROW FIRST    "the ranking variable was uncertainty; it is now zero"
    agy         THIS ROW FIRST    on a severity comparison it made itself from source
    glm         NOT YET           "constructibility is not verification"
    deepseek    NOT ESTABLISHED   cannot rank without alphaswpctxreg's severity
    minimax     NOT YET           "ready to elevate once the witness actually RUNS"

**But the count is the least informative part, and you should not adjudicate on it.  All three
NOT-YET seats give ONE reason and it is the same reason: the witness has not been RUN.  None
disputes the severity or the mechanism.**  So the panel did not split on the ordering -- it stated
unanimously the CONDITION under which the ordering flips, and that condition is exactly what
opus5's hold on this row is for.  minimax put the trap best: *"the previous ranking was honest;
flipping it on the strength of 'constructible in principle' is the same shape of error in
reverse."*

**So the question for you is narrower than "which row first": is CONDITIONAL promotion -- first
once the witness runs red-then-green, not before -- the right disposition, or does the med -> high
severity alone already justify reordering now?**

**QUESTION 3 (claim scope):** the repair is coarse.  codex supplied the accurate CHANGELOG sentence
and its limit.  **Is shipping the coarse repair right, or does the round owe ASM=0 handling?**

*** THE PANEL ANSWERED THIS MORE STRONGLY THAN I ASKED IT, AND THE TWO HALVES CAME FROM DIFFERENT
SEATS THAT COULD NOT SEE EACH OTHER. ***  kimi named the fact that would decide it -- *"do tc
entries carry an ASN/ASM field?  If they do not, the fine semantics are not even implementable
here"* -- and agy, reading the source, established that **they do not: `vph_tlb_entry` and `l1_64`
carry no ASM or ASN tag at all.**

So the honest disclosure is not *"we shipped a coarse repair and deferred the finer semantics"* but
**"the finer semantics have no representation in this emulator's translation cache to be
implemented in"**, and over-invalidation is conservative in the safe direction: it costs re-walks,
never stale data.  **Confirm that this is the sentence the CHANGELOG should carry.**

*** AND SINCE THAT WAS WRITTEN, BOTH HALVES HAVE BEEN NAILED DOWN -- ONE FROM A PRIMARY SOURCE
THAT ARRIVED ON A DIFFERENT ROW, ONE FROM A ONE-LINE GREP. ***

**Hardware.**  The Alpha 21066 Hardware Reference Manual (fetched at codex's citation while
reviewing `lcaconfbus1kill`; `machine_alpha.c:61` installs the LCA, so it is this machine's
chipset) says at `21066_66a_hrm.txt:1486` and `:1685`, read locally:

> *"Write operations to the ITBASM register invalidate all entries that do not have the ASM bit
> set."*

So the selectivity `ALPHA_TBIAP()` is supposed to have is real, documented, and the repair is
genuinely coarse rather than merely conservative.

**Tree.**  `grep -rn ALPHA_PTE_ASM src/` returns **ONE hit -- the `#define` at
`alpha_cpu.h:223`.**  Nothing consumes it.  `apcb_asn` is written by `swpctx` and read by a debug
print, and no translation lookup consults it.

**So the disclosure sentence writes itself, and it is stronger than "deferred": the finer
semantics have no representation in this emulator's translation cache at all.**  Q3 is, I think,
answered -- but the sentence is yours to ratify, because it is the one that will stand in the
CHANGELOG.

### B2. `alphaswpctxreg` -- the easiest resolvable HIGH-adjacent item in the queue

One character.  `cpu->cd.alpha.r[ALPHA_A0] = ctx` should be `ALPHA_V0`; the comment directly above
it already says v0.

    idiom      grep -n 'ALPHA_V0] =' src/cpus/cpu_alpha_palcode.c  ->  EIGHT sites on 2026-09-08.
               swpctx is the LONE OUTLIER among nine return-value sites in its own file.
    oracle     v0_after == ctx_before, printable by the debugger `reg` command -- so guest code
               need not consume the return value
    vacuity    requires pre-call v0 != outgoing ctx, or a stale v0 looks correct

**codex refuted my premise:** I claimed this both loses the return value AND clobbers `a0`.  The
clobber is NOT a defect -- in the wrapper `a0` is an output tied to an input, so its incoming value
need not survive.  One defect, two register-state effects.

**QUESTION:** anything against just doing this one?  It has a design, an oracle, a vacuity
condition, eight precedents, and no in-tree dependency.

### B3. `sgirandomcolour` (HIGH, open, never held) -- design pass 1 complete, 5 seats

Twelve of sixteen encodable colour modes reach a `default:` arm that fills a buffer with `random()`
and writes it to guest memory; one of the twelve (`YCRCB 0xf0`) is documented in `crmfbreg.h`.

    disposition   member 3 (decline + latched announce) via candidate (b) -- skip the PUT's
                  memory_rw.  NEVER an early return.
    scope         TWO rounds, not one with sgirebufuninit.  5 of 5 seats.
    settled by me there is NO mode validation: the store is unconditional and unmasked, the
                  MODE_DST case only debug()s, and the file says "Treat all registers as
                  read/write, by default".  **So the witness IS constructible.**
    settled by me the function has NO common tail, and fatal() does not exit

**grok reframed it better than my brief did:** the PUT's output is the STORE, not `buf`, so this is
not a fill policy at all.  And it declined to certify its own recommendation until the tail was
checked -- I checked it.

**A DETECTOR HOLE, and three of five seats were in it:** pinning the test to `0xf0` alone is
escapable by `case 0xf0: put_ok = 0; break;` with `default:` still random.  The primary vector must
be an UNDOCUMENTED value.

**QUESTION:** this is the highest-severity row I can start immediately after `#513`.  **Does it go
next, or does `alphatbinegsel` / `alphaswpctxreg` outrank it?**

### B4. `armbfcdecode` -- *** BLOCKED ON A DOCUMENT, and this is the one thing I cannot resolve ***

codex verified the implementation half: the decoder does not exclude source field 15, so BFC is
dispatched as BFI reading `r[15]`.  **And it corrected me twice** -- `r[15]` is NOT the PC in this
interpreter (translation reconstructs into `cpu->pc`, PC+8 lives in a separate `tmp_pc`), and
DDI 0100I covers ARMv6, not just ARMv5.

**BFI/BFC appear in NONE of the fifteen manuals in `_scratchpad/`.**  codex explicitly refused to
cite the architecture from memory -- correctly, given `#357`/`#362`/`#365` shipped page citations
that came from model output.

**QUESTION FOR THE OWNER, not for Fable: fetch DDI 0406 (ARMv7-A ARM)?**  Until then this row
cannot ship a behavioural change.

---

### B5. ROWS ASSESSED LATE IN THE SESSION -- ready, and none of them blocked

**`lcaisalane` (med) -- SIX items, not the three filed.**  codex was given NO list and warned not to
manufacture three; it found four behavioural issues, an initialisation gap and a format mismatch,
and said *"the filed 'three' overstates the initialisation claim."*
*** THE TRAP: the guard is `if (ofs > len)` -- equality passes -- but the rejected arm is `exit(1)`,
so changing only `>` to `>=` EXPANDS the termination. ***  Boundary and disposition are one design
or neither.  It bounded the claim too: *"this is NOT a demonstrated buffer overrun."*
**AND IT FOUND A DOUBLE-COUNT:** `lcabadval`'s scope explicitly EXCLUDES range-guard analysis while
its later note records this exact termination site -- *"extract or reassign that site explicitly
rather than counting it twice."*  **That is an open obligation on both rows.**
*No in-tree regression drives this shim* -- `lca_irqstub_probe.py` reaches the downstream ISA
mapping directly -- so every item is a documented source candidate.

**`fbfiqsilent` -- both arms are member 4 ACCEPT, in separate rounds.**  The IRQ arm reads
`odata = d->irq_enable; fatal(...); exit(1);` -- **it computes the correct value and then ends the
host**, the same shape this project already found at that register's neighbour.  The FIQ twin
returns a silent zero, which *"is correct when disabled, but not for every configured state"*.
**This row is NOT blocked on a manual**: `_scratchpad/dc21285.txt` is present, which is why it was
chosen over the three that are.

**`sgirebufuninit` (med) -- enumerated, and it is REACHED IN-TREE.**  18 of 64 combinations send
uninitialised bytes to guest memory on PUT, 30 of 64 consume them on GET -- **and the tiled MTE
already constructs CI/2 and CI/8, two of the leaking cells.**  Fix is `uint8_t buf[8] = {0}`, with
no currently-defined path changed.  *** The oracle needs MemorySanitizer, and MSan is INCOMPATIBLE
with ASan -- so that round owes a THIRD sanitizer configuration, not a reuse of `build-asan/`. ***

### B6. *** A CARRIER-LEVEL FACT ESTABLISHED TONIGHT, AND I HAD IT WRONG TWICE BEFORE GETTING IT
### RIGHT: OPTION-SET MEMBER 5 (FAULT) IS AVAILABLE ON **MIPS AND M88K ONLY**. ***

`src/cpus/memory_rw.c`'s device-failure path has exactly two arms, `#ifdef MEM_MIPS` and
`#ifdef MEM_M88K`.  **No ARM, no Alpha, no PPC, no SH** -- every other architecture reaches
`return MEMORY_ACCESS_FAILED` with no exception delivered.

**Why this belongs in an adjudication packet:** the option set is what every de-fatalisation round
chooses from, and **member 5 is a phantom on most of this tree.**  A round that reaches for FAULT on
an ARM, SH, PPC or Alpha device is reaching for a round that does not exist yet -- the prerequisite
is building delivery, which a seat priced as *"a new IMPLEMENT round, not a de-fatalisation."*

*My own error trail, recorded because it shows how easily this spreads: I first wrote "FAULT is
unavailable on Alpha" onto three `dev_lca.c` rows -- too narrow.  Then, assessing an ARM row, I told
a seat that "member 5 may genuinely be available here, `memory_rw` has an ARM arm."  It does not.
**I was one brief away from spreading the false version across the ARM queue, having just corrected
the Alpha version of the same mistake.**  All three rows now carry the general form.*

## C. RECORDS CORRECTIONS MADE TONIGHT -- for review, not decision

| what | evidence |
|---|---|
| `sgirergbroundtrip` CLOSED -- was `open` while `#505` had fixed it | tree carries the fix + a `#505:` comment; commit `7a41b3f` |
| `#505`'s CHANGELOG cited a witness path that does not exist | corrected to `regress/sgi_re_rgb_probe.py` |
| `lcaconfwidth`, `alphaswpctxptbr`, `alphapfnoffset` -- `commits` was None | each verified: `7a41b3f` carries the matching round tag in the right file |
| `armbfiwidth` -- title said 468, note said 499 | enumerated all 1024 pairs: **468**.  `1 << 0` is DEFINED, so the 31 zero-width pairs are not undefined.  The two sets OVERLAP by 465; the title's "a DIFFERENT 496" was wrong |
| `ledgerstatelies` -- open, held, NO question | three-part question written |

**THE CLASS behind three of those:** `7a41b3f` shipped FOUR rounds and **not one of the four rows
carried its commit**.  A multi-round commit is ONE act to the committer and N rows to the ledger.
A single-round commit cannot fail this way.

**I proposed NO checker** -- the attribution gap has consumed zero decisions, and a check firing on
legitimate `in work` rows would be switched off.  The *state* gap HAS now consumed one (recorded in
`ledgerstatelies`), which is the pre-specified escalation trigger.

---

## D. SEAT FINDINGS

### D1. *** codex CANNOT DESIGN WITNESSES FOR THIS PROJECT -- a routing fact, not a failure ***

Four briefs on the SAME defect: three answered in full, the witness-design brief refused.

    brief                    .err bytes   file reads   outcome
    ARM decode                   70,308   many         ANSWERED
    alphatbinegsel VERIFY        20,210   many         ANSWERED
    alphatbinegsel Q3           167,085   many         ANSWERED
    alphatbinegsel WITNESS        6,291   *** ZERO *** REFUSED (0-byte txt)

**Zero file-read lines = it refused before opening anything.**  The prompt's TEXT tripped it.  The
brief used no `kill`/`host dies`/`exploit` vocabulary: **neutral language was NOT sufficient.**  The
distinction is ANALYSING existing code versus CONSTRUCTING a guest sequence that reaches the defect
-- and witness design is inherently the second.

**Rerouted to grok BYTE-FOR-BYTE**, which delivered a full design.  That is what makes this a
capability finding rather than a prompt-quality one.

**A THREE-STATE DISCRIMINATOR, one `grep -c`:**

    refusal line + ZERO reads              PROMPT-LEVEL.  Reroute; a retry will not help.
    refusal line + MANY reads              LATE (archive/subject).  Scoping may help.
    NO refusal line, 0-byte txt, alive     MID-RUN.  Not a refusal.
    NO txt and NO err at all               THE RUN NEVER STARTED -- a launcher fault, not a refusal.

*** CORRECTED after I wrote it: an earlier form keyed the first state on "small .err + zero reads",
and that MATCHED A HEALTHY SEAT twenty minutes later -- the pass-2 brief inlines the whole diff, so
codex legitimately read nothing while streaming 39 KB of reasoning.  THE REFUSAL LINE IS THE TEST;
the read count only says WHERE it refused. ***

The third state was measured separately tonight: a relative artifacts path in a background shell,
where **the harness reported "completed (exit code 0)"** from the wrapper while the command exited 1
and codex was never invoked.  Only an explicit `echo "EXIT=$?"` caught it.

### D3. *** A FOURTH codex TRIGGER: THE ASK-AGAIN QUESTION ITSELF -- and it is a MANDATED step ***

codex ANSWERED the `#513` pass-2 diff review and REFUSED the pass-3 one.  Same round, same file,
same neutral vocabulary, one hour apart.  **The refusal is LATE** (133 KB `.err`, 30,706 tokens,
many file reads), so it is the archive/subject shape, not the chain shape.

The difference is pass 3's Q3: *"name the smallest edit that keeps a guard and makes these two rows
GREEN while the latch behaviour is WRONG."*  **That is evasion construction, not source review.**

> **The vacuity floor MANDATES exactly that question of every clean kill table, and measured yield
> says it is where the real escapes come from.  So codex is unavailable for the highest-yield
> adversarial query in the round lifecycle, on top of being unavailable for witness design.**

**Across nine firings the pattern is consistent: codex reviews CODE THAT EXISTS; it will not
construct an edit or a sequence that defeats something.**  Mitigation is proven -- pass 3's five
other seats all answered it, and grok additionally prescribed the one-row class closure that I
implemented.  **Route the ask-again to grok and the Ollama transports.**

### D2. The scoping remedy has a measured NEGATIVE CONTROL

`codexsubjectrefusal`'s recorded remedy is neutral language AND reading scoped to `src/` +
`regress/*.py`.  Applied deliberately and singly to the `sgirekills` re-pin brief: **refused again.**
**Scoping reading to `src/` cannot help when `src/` IS the flagged content** -- a hardening fork's
product source reads to the filter like the archive does.

**And the remedy is not free:** on the Alpha VERIFY brief my scoping EXCLUDED the invalidation
callback, so the seat could not settle Q3 and said so.  **Narrowing scope to avoid the filter can
starve the question.**

---

## E. WHAT I DID NOT DO, deliberately

* **did not implement `alphaswpctxreg`**, though it is one character and fully designed -- `#513` is
  mid-round with an uncommitted working set, and mixing two rounds in one commit is not a shortcut
  I am willing to take;
* **did not rebuild `build-asan/`** -- part 1 is CLEAN but its binary predates the edit, and a
  rebuild would contend with the running kill table's wall-clock oracles.  **Recorded in
  CHECKPOINT.md with the remedy; owed before any ASan measurement and before `#513` closes;**
* **did not fire agy, Opus 5 or Fable 5**;
* **did not raise any severity except `alphatbinegsel`**, and that one is flagged as my judgment.

---

## Z. `gateworktree` -- *** A SEVERITY QUESTION I AM DELIBERATELY NOT ANSWERING MYSELF ***

**This one is about what the EVIDENCE BASE means, not about emulator behaviour, and it landed
after the rest of this packet was written.**

codex audited all 21 precommit sections against their actual inputs.  The gate picks files from
the INDEX and reads their CONTENTS from the FILESYSTEM -- there is no `git show :<path>` in any
invoked checking path -- so 18 of 21 sections can go green on a working-tree correction that is
not in the commit.  **Section D fails the other way: its input is `git diff -U0`, UNSTAGED
additions, so the more correctly you stage, the less it inspects.**

*** MEASURED ON THIS SESSION'S OWN COMMIT: at `#513`'s gate run, D's two green rows were computed
entirely from `regress/sgi_de_primop_probe.py` -- a file deliberately kept out of every commit and
absent from `e302c98` -- while the 129 staged files were invisible to it. ***  And codex found a
SHIPPED instance in history: `2956c7e` added a probe while its own `check_probe_wiring.py` carried
zero manifest entries for it.

**QUESTION Z1 (severity):** the row sits at `med`.  It changes no product code.  It changes what a
GREEN GATE MEANS on every round this project has recorded, and this session produced both a
measured vacuous check and a shipped invariant violation.  **Does it go to high?**

*I have deliberately NOT raised it.*  I raised `alphatbinegsel` med -> high myself today and
flagged that as my judgment; raising a second severity on ONE seat's reading in the same session is
the habit the panel exists to check.  **So this is referred, not decided.**

**QUESTION Z2 (scope):** codex's prescription is a snapshot MODE announced before the first
pipeline invocation, with an isolated worktree as the practical route because the helpers derive
paths from `__file__`.  That is a change to the script every commit runs, owing negative controls
in both directions.  **Is that the right size of round, or is there a cheaper partial -- e.g.
fixing section D alone, whose input is one command -- that buys most of it?**
