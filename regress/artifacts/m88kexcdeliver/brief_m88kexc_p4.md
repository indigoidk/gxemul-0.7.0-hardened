# PASS 4 -- `m88kexcdeliver` (#502): the closing pass on the ADJUDICATION-PASS REPAIR (probe v4).  Tree `GXEMUL-SEC/src/`, HEAD `83df95c` + the uncommitted round.  2026-09-06, ~08:45.  SHORT BY DESIGN: one diff, one table, one question.

## CONTEXT AND VOCABULARY
An ordinary correctness review of an open-source machine emulator's CPU model (GXemul 0.7.0, hardened fork): the MC88100
exception-delivery path in `cpu_m88k.c` and its detector `regress/m88k_exc_probe.py`.  The "guest" is the operating system
inside the emulator.  Plain engineering vocabulary.  **If you cannot read files that is expected -- every fact is inlined; name
any premise you cannot settle rather than guessing.**  Tree under review: `GXEMUL-SEC/src/` (three pristine-2021 copies under the
project root are NOT this fork).  **VERDICT LINE FIRST.**  Cite by grep anchor.

## WHY A FOURTH PASS, AND WHY IT IS THE LAST UNLESS IT FINDS A BREACH
The repair-chain rule: a repair made in response to a pass owes its own pass, scoped to THAT diff, and the chain closes on the
first VALID pass that finds zero floor breaches surviving adjudication -- with the denominator stated.  Pass 3 (the adjudication
pass, `pass3_panel_20260905_220902/`: codex, kimi, grok, deepseek, minimax answered; glm burned; the two Anthropic Agent seats died
on a session limit and answer HERE instead) ruled on F1..F24 and found TWO more detector gaps plus records defects.  This pass
reviews ONLY the repair for those two gaps.  Product code is UNCHANGED since 16:16 yesterday (comment-only edits at 23:00,
verified by a non-comment diff; `build/` rebuilt, 22/22 -> 23/23 on it).

## THE PASS-3 RULINGS, APPLIED (each a QUESTION if you can check it)
* grok CLOSE, kimi CLOSE; codex / deepseek / minimax ONE MORE REPAIR.  What they found, and what changed:
  1. **IND never started clear** (grok, codex): every row's pre-fault PSR (0x80000002 / 0x00000002 / 0x90000002) already had
     IND set, so dropping `| M88K_PSR_IND` from the exception-path PSR write was a 22/22 escape -- the carry shape (F6) again.
     REPAIR: row `indclr` -- `stcr r5,cr1` with r5 = 0x80000000 (MODE only, IND CLEAR) then the overflowing add; wants PSR
     0x8000000b and EPSR 0x80000000.  Mutant M_NOIND (`| M88K_PSR_IND` -> `| 0`).
  2. **HALT was a diagnostic classification, not a verified stopped state** (codex): `halted` was `"unimplemented" in tr and
     "vector=" in tr` -- a fallback that keeps its message and drops the stop would classify as HALT, and ANY vector's diagnostic
     qualified (on HEAD, `sfu1h` "passed" at pc=0x10004 because the FIRST divu halted).  REPAIR: `halted` now requires the
     diagnostic AND the machine-stopped observation; an expected-HALT row (resid50, sfu1h) must see ITS vector named
     (0x032 / 0x072); sfu1h additionally requires pc == 0x40 (the first delivery happened) else BADREGS stage1.  Mutant
     M_NOSTOP (the fallback's `running = false` loop body -> `(void) j;`).
  3. **The LEVEL channel proves the ERROR/WARNING regression, not exact INFO** (codex: INFO and DEBUG are both silent at the
     post-startup WARNING floor) -> contract reworded.  4. **sfu1h's channel restated** (kimi, grok): the nested SFU1 halts at
     the FALLBACK, which runs before the SFRZ re-route; with the fallback off it is RE-ROUTED TO ERROR (0x50), not delivered to
     0x390 -- the row pins "SFU1 inside a handler still halts", not "SFU1 is not delivered to its vector".  5. **M_TAILOFF is
     EQUIVALENT for every vector** (deepseek, codex, kimi: `< MISALIGNED` still admits 0..3; the seven arms are bare breaks) --
     the Opus pass-2 attribution was wrong; the debt is "vectors 0..3 unrowed", carried by m88kexcdebt with that wording.
     6. **Census** (grok, codex): 11 of 128 low vectors BYPASS the fallback (0..10), 10 are DELIVERED (1..10), vector 0 still
     stops every CPU in the RESET tail arm, 117 halt at the fallback, 118 stop overall.  7. **Three rows this round CITED were
     never FILED** -- `m88kexctaildefault`, `m88ktbnd`, `m88kmxmkill` (kimi, grok) -> filed as documented-only LOW rows.
     8. Gate comment 2/22 -> 3/22 (kimi, grok, codex).  9. PRETABLE's pre-pass-2 "LEVEL unobservable" / "M_DSLOT = else-arm SFIP
     wrong" sentences -> dated correction appended, originals left in place.  10. Table-1 tally: 11 killed + 2 survivors, not
     "12 killed" (codex).  11. minimax: the seven table-1 shapes table 3 carried forward by construction are RE-MEASURED on v4.
* D1 (the delay-slot else-arm): every pass-3 seat that ruled rules with Fable/codex/grok against kimi (grok: "kimi's 6.4.3.1.2
  quote is FIP while the BRANCH is in XIP -- one stage early"; kimi itself: "rule for Fable/codex/grok; kimi's dissent is refuted
  from the primary source").  FILED m88kdslotshadow MEDIUM with the dissent verbatim; the dslot row pins the arm AS IMPLEMENTED and
  says so (grok: "labelled + filed is the oracle-correction rule deferred to the round that will edit that arm"; minimax wanted a
  visible banner -- the row table carries one).

## THE REPAIR DIFF (probe v3 -> v4; `regress/m88k_exc_probe.py`, md5 0d5c0f33), VERBATIM WHERE IT MATTERS
```python
PSR_INDCLR = 0x80000000                          # MODE only, IND CLEAR: the indclr row's pre-fault PSR
    ("indclr",   [STCR_R5_CR1, ADD_R2_R3_R4],   {"r3": 0x7fffffff, "r4": 1, "r5": PSR_INDCLR}, V_OVF, 0x10008, PSR_INDCLR, None),
EXPECT_VECTOR = {"resid50": 0x032, "sfu1h": 0x072}   # the vector the fallback diagnostic must NAME for an expected-HALT row
    diag = re.search(r"unimplemented[^\r\n]*vector=0x([0-9a-f]+)", tr)
    halted = diag is not None and ("machines stopped" in tr or "stopped" in tr)
    if halted and name in EXPECT_VECTOR and int(diag.group(1), 16) != EXPECT_VECTOR[name]:
        halted = False                              # halted on some OTHER vector: not the row's answer
    if halted:
        res["result"] = "HALT"
        if name == "sfu1h" and pc != 8 * V_DIV0:
            res["result"] = "BADREGS"; res["bad"] = ["stage1"]   # halted before the handler ran (the pre-fix shape)
```
(indclr wants the default PSR_EXC 0x8000000b; `PSR_WANT` is unchanged.)  Gate 11 pins `M88KEXC_RESULT=23/23` and adds a named
indclr pin (`psr=0x8000000b .*epsr=0x80000000`).

## TABLE 4, MEASURED (`killtable4/`, frozen v4 md5 0d5c0f33, clone re-baselined from SEC and rebuilt, BASE 23/23 before and after,
clone clean, no sentinel; 08:01-08:11)
      M_NOIND        22/23  killed: indclr bad=psr                 M_NOSTOP     21/23  killed: resid50 STOP, sfu1h STOP
      M_NOSHADOW      3/23  killed (20 rows bad=sxip,snip,sfip)     M_SNIPX       3/23  killed (20 rows bad=snip,sfip)
      M_NOEPSR        2/23  killed                                  M_VEC4        1/23  killed (22 rows STOP; resid50 the 1)
      M_NOMODE       19/23  killed: priv privtb unimpl udiv0 (the four user-mode rows -- as pass 1 predicted)
      M_NOSFRZ        2/23  killed                                  M_CARRYCLR   22/23  killed: ovfc bad=psr
      M_LEVEL         3/23  killed (20 rows bad=level)              M_DELIVERALL 21/23  killed: resid50 sfu1h
      M_TAILRETURN    2/23  killed (table 4b, `killtable4b/`: its find-text had moved with the 23:00 comment edit, so table 4's
                     driver skipped it as MUTANT-TEXT-NOT-FOUND; repaired and re-measured 08:21-08:23, BASE 23/23 both ends)
HEAD with the final instrument: **2/23** (`probe_v4_head.out`): usertb DELIVER (pre-existing user vector) and resid50 HALT (HEAD halts
on vector 0x032 exactly as expected) are the 2; sfu1h now reads STOP on HEAD because the first divu halts on vector 0x008, not 0x072
-- the hardened classifier refusing to call that a pass is repair 2 working.  The fix on the rebuilt `build/`: **23/23**
(`probe_v4_fix_final.out`).

## THE ONE QUESTION
**Does any floor breach survive in the v4 detector?**  The denominator claimed closed: `implemented` per class x route
(M_ISTRAP 17/22 in table 3; BOUNDS/ERROR trap-only by construction, M_TRAPONLY equivalent, disclosed); the fallback predicate
(M_REVERT 3/22, M_DELIVERALL 21/23) and its STOP (M_NOSTOP 21/23); the tail labels (M_NAIVE 3/22) and guard bound (M_TAILLE
21/22); {SFRZ} x {is_trap} four cells (error, errortb, trapfrozen; M_SFRZTRAP 21/22, M_ERRORDROP 21/22); VBR (M_NOVBR 21/22);
the PSR write's four bits -- SFRZ (M_NOSFRZ), IND (M_NOIND), SFD1 (the exact compare; every pre-fault PSR has SFD1 CLEAR, so a
dropped `| SFD1` gives 0x80000003 != 0x8000000b -> bad=psr on every row: is that right?), MODE (M_NOMODE, user rows) -- and carry
(M_CARRYCLR); EPSR (M_NOEPSR 2/23; M_EPSRAFTER 0/10 on pass 2); the shadow update (M_NOSHADOW, M_SNIPX, M_DSLOT, M_SFIPNOTGT,
M_DSLOTSWAP); the level (M_LEVEL).  Disclosed, not closed: M_DELAYALWAYS, vectors 0..3 unrowed, DMT under a frozen trap
(m88kexcfrozendmt), SSBR, fcr2/4/5, first-exception SFU1 (m88kexcsfu1), the dslot ARCHITECTURAL values (m88kdslotshadow),
exact INFO (only "not ERROR/WARNING" is pinned).  **Name a cell in that enumeration with no row, or a body-tested lvalue the
enumeration omits, or say CLOSE with your own denominator.**  One ask-again is already spent (pass 2); this pass is the repair's
own review, not a new hunt -- but if while verifying you find something ELSE, say so.

VERDICT LINE FIRST (CLOSE THE CHAIN / ONE MORE REPAIR: <which> / DO NOT SHIP), then the two repairs each UPHOLD/OVERTURN/REFINE with
a reason, then the SFD1 question, then anything else.  Keep it under a page: a packet-fed seat that spends its budget re-deriving
the whole round burns out (glm did, twice).
