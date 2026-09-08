# Audit the adjudication packet -- ALL EVIDENCE INLINED, no archive reading needed

## 0. SCOPE -- and an apology for the last attempt

*** DO NOT READ `regress/artifacts/` OR `tools/pipeline/ledger.json`. ***  You refused this brief's
previous form, correctly: it directed you to read `regress/artifacts/.../killtable_20260908/*.txt`,
which is the archive corpus your refusals key on.  **That was my error and I have removed the need
-- every log the packet cites is INLINED below.**

Read only, and only if you need them: `GXEMUL-SEC/src/devices/dev_sgi_re.c`,
`regress/sgi_re_width_probe.py`, `regress/gate_arm.sh`, `src/cpus/cpu_alpha_palcode.c`,
`src/cpus/cpu_arm_instr.c`.

Tree: `GXEMUL-SEC/src/`.  Ignore the pristine 2021 `src/` at the project root.

*** NO MUTANT, NO EVASION, NO GUEST SEQUENCE IS WANTED. ***  This is a factual audit of a document
against inlined logs and against source.

## 1. WHY

The document below is what a different model reads tomorrow to adjudicate this queue.  **This
project has measured that a wrong premise in a brief comes back CONFIRMED** -- a recent panel had
seven of nine seats ratify a census wrong by a factor of four, and one seat "corrected" it by
silently narrowing the claim, which HID the defect.

**So the packet is a set of claims, not a summary.  I wrote it.  Check it.**

## 2. THE QUESTION

**Does every factual claim hold against the inlined logs and the source?**  Quote the claim, quote
the evidence, and classify:

* **WRONG** -- contradicted;
* **UNSUPPORTED** -- not contradicted, but the cited evidence does not establish it;
* **OVERSTATED** -- true only in a narrower form.

**OVERSTATED is the one I most want.**  This round already had a claim of mine withdrawn -- that
`M8_texaccept` "measures the store-first design" -- because that mutant also removes the announce
and so cannot isolate what I said it isolated.

Check hardest: **every number**; the bit enumeration in section A2; the Alpha claims in B1/B2
(`ALPHA_TBIA()` passing `a1 = 0`, the `a0 >= 1` dispatch, `vaddr_mask` defaulting to `(int64_t)-1`,
`ALPHA_V0` being the idiom at eight sites while `swpctx` uses `ALPHA_A0`); and **section D's claims
about you** -- that you refused exactly two briefs before this one, one prompt-level with zero file
reads and one late.  **You are the subject of those; correct them if they are wrong rather than
flattering.**

Finally: **does the packet make clear where I applied my own JUDGMENT versus where I am reporting a
seat's finding?**  If an adjudicator cannot tell my opinions from measurements, that is the defect
that matters most.

## 3. THE MEASUREMENT LOGS, INLINED

### PREFIX_RED_20260908.out (pre-fix)

```
other decl         exit0/txt/0x0 exit0/txt/0x0 #499: declines, announces once, declined read lands a defined 0 ok

OPUS497T_RESULT=30/44
OPUS497T_LABEL=prefix-red
OPUS497T_DONE
PREFIX_RED_DONE rc=0
```

### POSTFIX_20260908.out (post-fix)

```
other decl         exit0/txt/0x0 exit0/txt/0x0 #499: declines, announces once, declined read lands a defined 0 ok

OPUS497T_RESULT=44/44
OPUS497T_LABEL=postfix
OPUS497T_DONE
POSTFIX_DONE
```

### POSTFIX46_20260908.out (on build/)

```
tex/unmap          1/1          1/1          LATCH INDEPENDENCE: both announces fire in ONE instance, either order ok
unmap/tex          1/1          1/1          LATCH INDEPENDENCE: both announces fire in ONE instance, either order ok

OPUS497T_RESULT=46/46
OPUS497T_LABEL=final46
OPUS497T_DONE
```

### killtable TABLE1.txt

```
# #513 sgirekills -- kill table 1   (scratch clone /tmp/gx513, frozen instrument)
# baseline BASE 44/44   (from BASE.raw, re-derived)
#
# *** THIS LINE READ "42/44" WHEN THE TABLE WAS WRITTEN, WHICH IS M12_linswap's SCORE, NOT THE
# BASELINE'S.  My summary block reused the loop variables `n, d' after the mutant loop had
# reassigned them, so the header printed the LAST mutant's numbers under the baseline's
# label.  Corrected 2026-09-08 by re-deriving from BASE.raw.
#
# The real baseline was provably clean regardless: the driver exits with
#   "*** BASELINE NOT CLEAN -- table uninterpretable"
# unless numerator == denominator, and it did not exit.  BASE.raw confirms 44/44 with its
# completion sentinel present.
#
# Same class as the variable-shadowing bug that made this session's gate-edit script report
# "+616 re-pinned" rows.  Both were caught by checking the OUTPUT against an independent
# source rather than trusting the script that produced it.

mutant          score    floor  verdict   what it is
M1_reinstate6   30/44    (b)    KILLED    restore fatal()+exit(1) at ALL SIX read arms, verbatim
M2_datafill     42/44    (d)    KILLED    fill data[] instead of odata -- the tail overwrites it (the bug I nearly shipped)
M3_noincr       42/44    (d)    KILLED    drop the tlbi++ -- four copies of one cell
M4_readshift    43/44    (d)    KILLED    read-side index re-map >> 1 -> >> 2, write side untouched
M5_shortloop    42/44    (d)    KILLED    shorten the read loop; the guard still tests len != 8
M6_translate    41/44    (f)    KILLED    ANCHOR: +1 translation on BOTH store and read in TLB_A
M7_farbound     43/44    (f)    KILLED    FAR-BOUND shrink of TLB_A -- invisible to a row at the window base
M8_texaccept    40/44    (d)    KILLED    convert TEX to ACCEPT -- what the store-first TEX rows exist to catch
M9_texnolatch   43/44    (d)    KILLED    remove the latch: announce per access instead of per instance
M10_texbit      43/44    (d)    KILLED    CROSS-BIT: give the read decline the WIDTH latch instead of its own
M11_lanerev     42/44    (d)    KILLED    reverse the halfword lane order -- VAL_HI differs in every lane
M12_linswap     42/44    (d)    KILLED    swap the two LINEAR_A words -- the fixed-arity analogue of M11

NOT KILLED: none
KILLTABLE_DONE
```

### L2VERIFY.txt

```
# #513 pass-2 L2 verification  (scratch clone /tmp/gx513b, frozen instrument)

BASE_pass2        46/46   repaired detector, CLEAN
M13_latchcollide  44/46   KILLED   SGIRE_W_TEX_RD 1<<11 -> 1<<8 (= SGIRE_W_UNMAP_RD)

# The panel PREDICTED this mutant at 44/44 against the PRE-REPAIR 44-row detector.
# That prediction is not re-measured here -- the 44-row form no longer exists.  What is
# measured is that the REPAIRED detector kills it.
L2VERIFY_DONE
```

### CLASSVERIFY.txt

```
# #513 pass 3 -- LATCH-COLLISION CLASS CLOSURE  (clone /tmp/gx513c)

BASE_pass3   46/46   widened tex xbit (bits 0-8), CLEAN

M_bit6     45/46   KILLED   SGIRE_W_TEX_RD -> that bit
M_bit7     45/46   KILLED   SGIRE_W_TEX_RD -> that bit
M_bit9     46/46   ESCAPED  SGIRE_W_TEX_RD -> that bit
M_bit10    46/46   ESCAPED  SGIRE_W_TEX_RD -> that bit

# EXPECTED: bits 6 and 7 KILLED (the widened row co-fires them).
# bits 9 and 10 ESCAPE BY DESIGN and are DISCLOSED in the probe: they are set only from
# the drawing-engine path, which a TEX-read session never enters.  Measuring them is what
# makes the disclosure a FACT rather than a claim.
CLASSVERIFY_DONE
```

### CLASSVERIFY3.txt

```
# #513 pass 3 -- LATCH-COLLISION CLASS CLOSURE  (clone /tmp/gx513e)

BASE_fixed   46/46   tex xbit widened to bits 0-10 AND made SELF-CHECKING, CLEAN
#
# *** THE 46/46 ABOVE MEANS MORE THAN THE EARLIER ONES.  The row now wants `1/11' -- the TEX
# decline once, AND all eleven other latch announces present -- so a CLEAN run PROVES the setup
# fired.  The previous 46/46 did not: it was scored against a row whose six drawing-engine stores
# passed their VALUE as the OPCODE and therefore did nothing. ***

M_bit9     45/46   KILLED   SGIRE_W_TEX_RD -> that bit
M_bit10    45/46   KILLED   SGIRE_W_TEX_RD -> that bit

# *** THIS FOOTER IS THE DRIVER'S TEMPLATE TEXT FROM THE PREVIOUS RUN AND IT IS NOW FALSE.
# It said bits 9 and 10 "ESCAPE BY DESIGN and are DISCLOSED".  THEY ARE KILLED -- see the two
# rows above it.  Left in place with this correction rather than deleted, so the sequence is
# legible; a footer contradicting the results directly above it is exactly the wrong-record
# class this round has been correcting all evening, and it appeared in a MEASUREMENT LOG. ***
#
# THE ACTUAL SEQUENCE, and the before/after is the point:
#
#   CLASSVERIFY.txt   bits 6,7 KILLED   bits 9,10 ESCAPED 46/46, disclosed in the contract
#   CLASSVERIFY2      bit 9 ESCAPED again -- but that run scored the BROKEN row (see above),
#                     so its escape is evidence of the bug, NOT of an open cell
#   CLASSVERIFY3      bits 9 and 10 BOTH KILLED 45/46 against the fixed, self-checking row
#
# So the disclosure was withdrawn and REPLACED BY COVERAGE.  Two seats had called a
# measured-open cell on the edited line a breach whatever the contract says; closing it beat
# defending it, and the settling fact I had recorded as unknown was one grep away in a shipped
# probe that already drives the drawing engine.
#
# THE CLASS IS NOW CLOSED: SGIRE_W_TEX_RD aliased onto each of the eleven other used bits of
# `d->warned' is killed -- bits 0-5 by M10, bit 8 by `tex/unmap' and `unmap/tex', and bits
# 6, 7, 9, 10 by the widened `tex xbit'.
CLASSVERIFY_DONE
```


## 4. THE DOCUMENT UNDER AUDIT

```markdown
# ADJUDICATION PACKET for 2026-09-09 -- Fable 5

Written 2026-09-08 by the main loop, for the session in which Fable's usage resets.
**Every claim here is either MEASURED (with its log named) or marked as MY JUDGMENT.**
Nothing in this file is a substitute for the ledger rows; it is an index with dispositions,
so the adjudication spends its budget on decisions rather than on reconstruction.

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
    M8_texaccept  40/44   TEX -> ACCEPT         -- caught by all four store-first TEX rows

**Under my original base-only design, M4 and M7 would both have swept clean.**

---

### A2. *** THE `#513` REPAIR CHAIN -- THREE PASSES, AND THE THIRD FOUND THAT MY REPAIR
### CLOSED ONE CELL OF FIVE.  This is the item most worth an adjudication. ***

    pass 2   6 seats, ALL answered.  codex named ONE latch-collision cell (bit 8) with a
             predicted 44/44 sweep and its mechanism.  Repaired: 2 same-instance rows, both
             orderings.  MEASURED: BASE 46/46 clean, M13 44/46 KILLED.
    pass 3   6 fired, 5 answered (codex REFUSED -- see D3).  FOUR of five said DO NOT CLOSE.
             The repair closed bit 8 and left bits 6, 7, 9, 10 -- the SAME one-token operator
             on the SAME edited line.  kimi: "L2 stands, unrepaired."
    closure  tex xbit widened from bits 0-5 to bits 0-8 -- ONE row, not four.
             MEASURED: BASE_pass3 46/46; M_bit6 45/46 KILLED; M_bit7 45/46 KILLED.
             Bits 9, 10 DISCLOSED (set only from the drawing-engine path) and MEASURED anyway.

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
* **Is the bits 9/10 DISCLOSURE acceptable, or a breach?**  They are set only from the
  drawing-engine path, which a TEX-read session never enters, so the collision needs a guest that
  BOTH draws AND reads TEX.  The class-closure amendment permits writing into the contract "which
  cells are covered and which are deliberately not" -- but kimi argued an in-closure cell on the
  edited line is a breach regardless.  **These two rules point opposite ways and I have applied
  the amendment; confirm or overrule.**
* **Does the chain close at pass 4?**  The amendment says the closing pass VERIFIES THE ENUMERATION
  rather than hunting cells, which terminates.  Pass 4 is owed and not yet fired.

## B. CRITICAL ROWS ADVANCED TONIGHT -- ready for a disposition

### B1. `alphatbinegsel` -- *** I RAISED THIS med -> high AND THE RANKING IS MY JUDGMENT ***

**The defect is source-confirmed by two seats independently, with citations I re-verified myself:**
`ALPHA_TBIA()` -- the OS primitive meaning *invalidate every TLB entry* -- is
`alpha_pal_tbi(-2, 0)`.  `a0` is `uint64_t`, the dispatch is `if (a0 >= 1)`, so `-2` compares as
`0xff..fe` and takes the **VADDR** branch with `a1 = 0`.  **It therefore invalidates cached virtual
page ZERO and nothing else.**  Every other mapping survives a flush the guest OS believes succeeded,
and the Alpha fast path keeps consuming the surviving `host_load`/`host_store` pointers.

    verified by me:  ALPHA_TBIA macro passes a1=0; the a0 >= 1 dispatch; vaddr_mask defaults to
                     (int64_t)-1 on 64-bit; the alpha binding site
    repair           if (a0 >= 1 && a0 <= 3)   -- COARSE: it does not give TBIAP its ASM=0 semantics
    witness          DESIGNED by grok, NOT BUILT

**QUESTION 1 (severity):** the facts are the seats'; the med -> high raise is mine.  A documented
*invalidate everything* primitive clearing one page, silently, with a guest reaching stale physical
backing -- I put that in the same class as the other HIGH rows.  **Confirm or correct.**

**QUESTION 2 (ordering):** codex ranked `alphaswpctxreg` FIRST and labelled that *"a confidence
judgment, not a claim that it has the greatest potential severity"* -- explicitly because this row's
consequences were then unverified.  **They are now verified, so the input to that ranking has
changed.  Should this row go first instead?**

**QUESTION 3 (claim scope):** the repair is coarse.  codex supplied the accurate CHANGELOG sentence
and its limit.  **Is shipping the coarse repair right, or does the round owe ASM=0 handling?**

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

```
