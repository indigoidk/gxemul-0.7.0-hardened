VERDICT: RATIFY the defect reading, the disposition, the `<= 3` bound and every measured score -- I re-derived all twelve legs from the source by hand and each one reconciles exactly. DO NOT SHIP `regress/alpha_tbi_probe.py`'s CONTRACT as written: two of its "ROWED, each with a MEASURED kill" bullets are false, one of them provably unkillable and actively misdirecting, and the product comment's NO-ANNOUNCE warrant cites the one arm in the file that is not an instance of the shape while four contrary in-file precedents go unmentioned. All four findings are L4 wrong records; none touches the executable line.

OPUS_ASSESS_520_20260910

Verbatim first line of `C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\CHECKPOINT.md`, **as I read it when this
seat opened**:

> `# CHECKPOINT — overwritten at every round boundary and around every build-tree mutation`

*** AND THE FILE CHANGED UNDER ME DURING THIS REVIEW, WHICH IS BETTER EVIDENCE OF FILE ACCESS THAN EITHER
QUOTE ALONE. *** Re-read at the end of the pass it is 4827 bytes, mtime `Sep 10 12:27`, and its first line
is now `# CHECKPOINT -- 2026-09-10` with `HEAD: 4eac0b1` on line 3 (it was `7d7e055` when I started). Both
quotes are genuine; the file was rewritten at a round boundary between them. **That is this round's own
decayed-citation class, live, in the liveness token** -- the same failure the round's third L4 corrects in
product code. A citation into a file that changes under you decays silently, and a liveness quote is a
citation.

Tree check: I am in `GXEMUL-SEC`. `src/cpus/cpu_alpha_palcode.c` is **484 lines** with the arm at
`case 0x33:` line 327 and the guard at line 403. The pristine copy at the project root
(`C:\DocumentNoSnc\CC\GXEMUL\src\cpus\cpu_alpha_palcode.c`) is **393 lines**. `est/`'s copy is 484 and
`cmp` against SEC is **CLEAN**, so the fix is propagated byte-identically as step 4 requires -- worth
recording because `est/` is not a git tree and `git status` cannot show it, so nothing else in this round
says so. (The `GXEMUL-SEC/_scratchpad/CHECKPOINT.md` decoy is handled: it is untracked and its first line
is `*** THIS IS NOT THE CHECKPOINT. DO NOT READ STATE OUT OF THIS FILE. ***`. Good.)

---

# 1. IS THE DEFECT READING RIGHT?

**Yes, on every clause, and the ASM direction is right -- I settled it from a source the brief did not
point me at for this purpose.**

**The header.** `cpu_alpha_palcode.c:333-337` reads exactly:

```
 *	a0 = 1: ITB invalidate
 *	a0 = 2: DTB invalidate
 *	a0 = 3: both ITB and DTB
 *	a0 = -1: invalidate everything with ASM=0.
 *	a0 = -2: invalidate everything
```

So S1 quotes the header correctly.

**The ASM direction, which the brief says was written backwards once.** The shipped in-code sentence at
`:385-387` -- *"-1 invalidates the ASM=0 entries and SPARES the ASM=1 ones, -2 invalidates both"* -- is
**RIGHT WAY ROUND**, and I did not settle that from the header (which would be circular, since the header
is the thing under test). `_scratchpad/21066_66a_hrm.txt:1486`, §on the ITB:

> *"Write operations to the ITBASM register invalidate all entries that do not have the ASM bit set. This
> is a simple way to preserve entries that map operating system regions while invalidating all other
> entries."*

ASM=1 is the GLOBAL/OS mapping and is the set SPARED by an ASM-sensitive flush; ASM=0 is the
process-private set that goes. That is exactly what `-1`/TBIAP means and exactly what the comment says.
S1's parenthetical *(sparing ASM=1)* is correct.

**`a1` is the address consumed by the selective branch.** Three independent confirmations:
* `:165` -- `uint64_t a0 = cpu->cd.alpha.r[ALPHA_A0], a1 = cpu->cd.alpha.r[ALPHA_A1];`
* `:404` -- `cpu->invalidate_translation_caches(cpu, a1, INVALIDATE_VADDR);`
* `src/include/thirdparty/alpha_cpu.h:478-489` -- `alpha_pal_tbi(unsigned long op, vaddr_t va)` pins
  `a0 __asm("$16") = op` and `a1 __asm("$17") = va`, i.e. `op` in A0 and the VA in A1.

**And the third-party wrapper is what makes the defect's premise exact rather than merely plausible:**
`op` is declared `unsigned long`, so `ALPHA_TBIA()` = `alpha_pal_tbi(-2, 0)` delivers
`0xfffffffffffffffe` in `$16`. The guest side and the model side are unsigned at both ends; there was no
sign information anywhere for the old `a0 >= 1` to have used.

**The consequence is stated correctly too, and I checked the mechanism rather than taking it.**
`cpu_dyntrans.c:1228-1255` -- `INVALIDATE_VADDR` walks `vph_tlb_entry[]` and clears only entries whose
`(vaddr_page & cpu->vaddr_mask) == (addr_page & cpu->vaddr_mask)`; `:1276-1289` -- `INVALIDATE_ALL` clears
every valid entry. With `a1 = 0` on both TBIA and TBIAP, the pre-fix arm flushed **virtual page zero and
nothing else**. S1 is exact.

**One small imprecision, sub-L4, noted for completeness:** the comment's *"0 and 4.. are undefined and
fall to the conservative arm with the negatives"* reads as though the fix moved `0`. It did not -- the
pre-fix `if (a0 >= 1)` already sent `a0 == 0` to the `else`. Nothing hangs on it; the sentence is a
statement about the post-fix state, which is true.

# 2. IS THIS THE RIGHT MEMBER OF THE OPTION SET?

**The MEMBER is right. The WARRANT is mis-cited, and I am correcting a finding of my own that this round
adopted.**

The disposition is right, and I will say so plainly before I attack the reasoning: there is no value to
decline (the arm must do *something* with the cache), there is nothing to fault (the ladder's FAULT member
needs `memory_rw`'s failed-device exception, which `PASS2_FINDINGS`'s own S4 correctly records as
MIPS/M88K-only -- there is no Alpha delivery path), and ACCEPT/BACKED-ACCEPT are category errors for a
control operation with no return value. IMPLEMENT-the-conservative-default is the only member that fits,
and over-invalidation is the safe direction because a flushed-but-still-valid translation costs time while
a retained-but-stale one costs correctness.

**Now the grep the brief asked for, and it does not say what the comment says it says.** Every site in
this file that meets a SELECTOR IT DOES NOT MODEL announces loudly and halts:

| site | shape |
|---|---|
| `:136-138` | GXemul PROM `getenv` `default:` -- `fatal(... %i: TODO ...)`, `cpu->running = 0` |
| `:147-149` | GXemul PROM call `default:` -- `fatal(... a0=0x%PRIx64 ...)`, `cpu->running = 0` |
| `:410-417` | **`PAL_OSF1_wrent`** -- `if (a1 < N_ALPHA_KENTRY) ... else { fatal("attempt to write to non-implemented selector %i"); cpu->running = 0; }` |
| `:472-473` | `alpha_palcode()` `default:` -- `fatal("PALcode 0x%x unimplemented!")`, `cpu->running = 0` |

**Four for four**, and `wrent` at `:410` is the closest structural sibling this file has: same function, same
`switch`, an unrecognised *selector* arriving in a guest register, guarded by a *bound* -- and it announces
and dies. The comment at `:392-395` cites none of them. It cites **`#514`**, and says *"Same file, same
architecture, same shape."*

**It is not the same shape, and the ledger records that I am the seat that proposed it** -- `#520`'s
pass-2 note credits the Opus seat with *"named the in-file `#514` precedent as the transferred warrant the
option-set rule actually wanted."* The adjudication step asks a seat whose position was adopted to
scrutinise it harder, so:

> **`#514` is about an OUTPUT the architecture marks UNPREDICTABLE, where the model declines to define a
> value nobody may read. `#520` is about an INPUT the guest supplied that the model does not recognise and
> for which it silently substitutes a different action.** *Leaving a don't-care register alone* and
> *silently re-interpreting a guest request* are different acts. The first hides nothing, because nothing
> was asked; the second hides a guest asking for something this model has never heard of.

**There IS a genuine in-file precedent for silence on an out-of-range guest INPUT, and it is two arms
away.** `PAL_OSF1_swpipl` at `:423` does `cpu->cd.alpha.ps |= (a0 & ALPHA_PSL_IPL_MASK);` -- an IPL the
model cannot represent is silently truncated, no announce. `PAL_OSF1_wrmces` at `:208-212` does the same
with `& 7` and `& 0x18`. **That is the transfer the option-set rule wanted**: same file, same function,
same act (normalise a guest value the model cannot honour exactly, say nothing).

**SHOULD IT ANNOUNCE AT ALL? No, and I will not ask for one.** The honest ledger:
* No guest can reach the unrecognised region through the ABI: `alpha_cpu.h:281-285` defines exactly five
  selectors and every OSF/1-ABI kernel goes through those macros.
* The diff deletes no `exit(`/`fatal(`, so the de-escalation clause's tripwire-deletion hazard does not
  arise -- the pre-fix code was silent here too. The fix removes no announce because there was none.
* The addition licence forbids the diagnostic: no measured delta, and the `(once)` marker convention is
  correctly identified in the comment as a `src/devices` idiom with zero occurrences under `src/cpus`.
* The commented-out `debug()` at `:339-340` is already the cheapest possible hedge and leaving it commented
  is defensible on the same licence.

**So the fix stands and the WARRANT PARAGRAPH is an L4.** What it should say, in one sentence each:
`swpipl`/`wrmces` are the in-file precedent for silence on an unrepresentable guest input; and this arm
*deliberately departs* from the file's four `fatal()`-and-halt selector sites, in the fork's
de-fatalising direction. As written, a future reader concludes this file has no contrary practice. It has
four instances of it.

# 3. WHICH OF THE ROUND'S ACCEPTED DISPOSITIONS IS WRONG?

**The weakest is L4-2 -- *"the casts are MEASURED REDUNDANT ... do not describe them as the fix."* The
correction is RIGHT. It was applied in ONE artifact and its SIBLING SURVIVES IN THE SHIPPED DELIVERABLE,
saying the opposite.**

`regress/alpha_tbi_probe.py:56-57`, inside the block headed *"ROWED, each with a MEASURED kill recorded
in regress/artifacts/alphatbinegsel/killtable_20260910/"*:

```
  * loss of the signed cast -- the original defect, an unsigned compare that
    admitted the -1 / -2 invalidate-everything selectors;
```

**Three things are wrong with that bullet and they compound:**

1. **It contradicts the corrected product comment**, which now says in capitals *"THE LOAD-BEARING
   PROPERTY IS THE TWO-SIDEDNESS, NOT THE SIGNEDNESS."*
2. **The edit it names is UNKILLABLE, and the round itself proved it.** Apply "loss of the signed cast" to
   the *shipped* line and you get `a0 >= 1 && a0 <= 3`, which is the exact form measured equivalent over
   300,037 values. It cannot redden anything. It is a claim of a measured kill for an edit that scores
   15/15 by construction -- `pos obs`'s vacuity, one level up, in the contract instead of in a row. The
   round's only measured evidence for that bullet is the HEAD null medium, and HEAD is not "loss of the
   cast": it is loss of the cast **and** loss of the upper bound. The bullet mis-describes its own
   evidence.
3. **It actively misdirects, in the one direction that costs something.** The equivalence is not just
   measured, it is provable in two lines by case split -- for `a0` in `[0x8000000000000000, 2^64)` the
   unsigned reading fails `<= 3` exactly where the signed reading fails `>= 1`, and the other three
   intervals agree trivially. And the unsigned form is the **more portable** of the two: converting a
   `uint64_t` above `INT64_MAX` to `int64_t` is *implementation-defined* under C99 6.3.1.3p3, while
   `a0 >= 1 && a0 <= 3` is strictly conforming. (`int64_t`'s existence forces a two's-complement
   *representation* per 7.18.1.1, but the *conversion* is still implementation-defined; every real
   compiler does the obvious thing, so this is a comment-level point and **not** a reason to touch the
   line.) So a future reader who simplifies the casts away has made a small portability *improvement* --
   and this bullet tells them they have just reinstated the original defect.

**Measured, so this is checkable rather than argued:** `grep -n "two-sided\|TWO-SIDED\|redundant\|
REDUNDANT" regress/alpha_tbi_probe.py` returns **zero lines**. The correction reached `cpu_alpha_palcode.c`
and `CHANGELOG.md` and did not reach the probe. This is mechanical rule #2 -- *when correcting a claim,
grep for its siblings before calling it fixed* -- with the sibling sitting in the round's own deliverable.

**What would settle it:** that grep, plus one word. Make the probe's contract match the CHANGELOG's, which
is already correct: *"any edit to either bound of the window, in either direction; loss of either reject
side; an added conjunct on `a0` or on `a1`; and a narrowing of either comparison's width."* Note that the
CHANGELOG's contract and the probe's contract **already disagree**, and the shipped one is the wrong one.

*The other three dispositions I checked and would not touch:* the TODO-line removal is plainly right; the
citation re-point to the frozen witness is right and is vindicated by this very answer's liveness quote
decaying under me; and the clause-(e) disclosure of `-1` vs `-2` is not merely defensible but forced --
`vph_tlb_entry[]` carries `valid`, `vaddr_page`, `paddr_page`, `writeflag` and nothing else, and
`grep -n "asn\|ASN\|ASM" src/include/cpu_alpha.h` is empty, so there is no metadata to spare anything by
and any such row would be vacuous by construction. S6 is correct.

# 4. IS `<= 3` RIGHT?

**Yes, exactly right -- and the authority is in the tree, is stronger than the header comment, and is
still uncited in the shipped source.**

`src/include/thirdparty/alpha_cpu.h:281-285`:

```c
#define	ALPHA_TBIA()	alpha_pal_tbi(-2, 0)		/* all TB entries */
#define	ALPHA_TBIAP()	alpha_pal_tbi(-1, 0)		/* all per-process */
#define	ALPHA_TBISI(va)	alpha_pal_tbi(1, (va))		/* ITB entry for va */
#define	ALPHA_TBISD(va)	alpha_pal_tbi(2, (va))		/* DTB entry for va */
#define	ALPHA_TBIS(va)	alpha_pal_tbi(3, (va))		/* all for va */
```

**Exactly five selectors, three of them selective, the largest is 3.** The true set is not smaller and the
fix admits nothing it should refuse. This is a better warrant than the arm's own header for the reason the
prior review pass gave and which I re-checked: *a header comment you are simultaneously editing is not an
authority over the edit*, whereas `alpha_cpu.h` is imported third-party material this round does not touch.
It should be cited in the source comment; it is not.

**On the 21066 manual, answering the brief's sub-question directly: it does NOT bear on PALcode selectors
and should not be cited for the bound.** `grep -n -i "PALcode.*tbi\|CALL_PAL.*33\|OSF/1 PALcode"
_scratchpad/21066_66a_hrm.txt` returns nothing. What it documents is the *hardware* invalidate path --
`ITBIS`/`DTBIS` (`:2929`, `:2967`, `:3946`, `:5615`) reached by `HW_MTPR`, and the `ITBASM` register -- which
is the layer *underneath* PALcode, not the `CALL_PAL 0x33` entry point. **It is the right source for
exactly one thing in this round, the ASM direction (`:1486`), and the wrong source for the bound.**

**One refinement the round should state, because it changes what "conservative" means:** for an
architecturally *undefined* selector the exact behaviour is arguably a **no-op**, not invalidate-everything.
The `else` arm is therefore conservative rather than exact for `a0 = 0` and `a0 >= 4`, exactly as it is for
`-1`. The comment already uses the word "conservative" and is right to; it is worth noticing that the
EXACT/CONSERVATIVE split the comment draws for `-2`/`-1` applies to the undefined region too, and the same
sentence covers both.

# 5. IS ANY SHIPPED ROW UNKILLABLE?

**No -- the disclosed set is exact and complete, and I verified it independently. But the question has a
better answer one level up: TWO CONTRACT BULLETS are in `pos obs`'s position, and one of them was never
measured at all.**

**The row check, derived rather than taken.** Union of every `FAILING:` list across all twelve legs of
`killtable_20260910/t3/SCORES.txt`:

```
bnd lo, bnd hi, bnd out, bnd zero, bnd mid, bnd a1z, bnd a1hi, bnd wide, tbia obs, tbiap obs   = 10
```

15 - 10 = **5 rows with no kill: `live`, `tbia fill`, `tbiap fill`, `pos fill`, `pos obs`** -- byte for
byte the five the probe's docstring declares. The four `fill`/`live` rows are upstream of the guard by
construction (they observe the *warming* load, before `CALL_PAL 0x33` executes) and cannot vary under any
guard edit; `pos obs`'s own note says *"CONTROL: positive selector ... flushes vaddr on both builds"*.
**Every one of the eight `bnd *` rows' notes names a specific catch and every one of those catches is
measured** (`bnd lo`/M_A, `bnd hi`/M_B, `bnd out`/M_C, `bnd zero`/M_D, `bnd a1z`/M_E, `bnd mid`/M_F,
`bnd wide`/M_G and M_H, `bnd a1hi`/M_I). No row over-claims. The disclosure is honest and accurate.

**Now the defect the question's framing does not reach.** The probe's contract lists six bullets under
*"ROWED, each with a MEASURED kill recorded in ... killtable_20260910/"*. One of them is:

```
  * omission of the invalidation entirely;
```

**No mutant in any of the three tables touches the invalidation call.** `mutate.py:28-40` defines nine
mutants and every one is a text replacement on the GUARD string; `t1` has five, `t2` six, `t3` nine, plus
BASE and the HEAD null medium. The string *"omission of the invalidation"* occurs **exactly once in the
tree** -- in the claim itself. It is very likely true (deleting the `else` call would leave `bnd zero`'s
`obs X` stale and redden it), but the contract does not say *derivable*; it says *recorded in
killtable_20260910/*, and it is not there.

> **Together with the "loss of the signed cast" bullet from Q3, the contract has two false entries in its
> ROWED list: one unmeasured and one unmeasurable.** The CLAIM -> ROW check in `PRETABLE.out` was run --
> and run well -- **against the product-code comment only**. Nothing applied it to the detector's own
> contract, which is itself a set of observable-consequence claims. That is the structural finding: *the
> pre-table block's CLAIM -> ROW row should name the probe header as a claim source, not just the diff's
> added comments.*

Cost to fix: one `else ;` mutant (one build) converts the first bullet into a true statement; one clause
(*"derivable from `bnd zero`'s `obs X`, not separately measured"*) is the honest alternative. The second
bullet needs deleting, not measuring.

# 6. WHAT ELSE I FOUND

**(a) THE ITB/DTB CONFLATION IS UNDISCLOSED, AND TWO SHIPPED ROWS SILENTLY PIN IT.** `alpha_tbi_probe.py:538`
labels `bnd lo` *"a0=1 ITB selective"* and `:540` labels `bnd mid` *"a0=2 DTB selective"*. **The model has
one unified translation cache and treats 1, 2 and 3 identically** -- one arm, same arguments, no
instruction/data split. So those labels describe behaviour the model does not have, and worse, the rows
*depend* on its absence: if a future round implements the split correctly, `tbi(1, 0x6000)` would flush only
the ITB entry, the DATA observing load in `bnd lo` would return the stale `VAL_E`, and **`bnd lo` would go
RED on a CORRECT implementation.** That is the oracle-correction rule's setup being built into a fresh
detector. One disclosure sentence in the contract costs nothing now; found later it costs the whole
re-pin-first dance.

**This finding is not new to the round -- it is new to the ARTIFACT.** The ledger's pass-2 note records the
Opus review seat *"found that `bnd lo' silently PINS THE ITB/DTB CONFLATION, so implementing the split
would red it on a CORRECT implementation."* `grep -n "ITB\|DTB\|conflat\|unified" regress/alpha_tbi_probe.py`
returns only the two mislabelling lines and one session banner. **A finding that reached the ledger and not
the deliverable is the unread-review class with an extra step**, and it is the same shape as L4-2 in Q3:
the round's corrections are landing in one artifact at a time.

**(b) `tally_kills.py` DECIDES WHAT AN ACCEPT ROW IS BY ITS NAME.** `ACCEPT_PREFIX = "bnd "`. That is a
correlate, not the defining property, and it is wrong in both directions: three of the eight rows it grades
as accept rows (`bnd zero`, `bnd out`, `bnd wide`) are REJECT-side rows, and **a future accept row not named
`bnd *` is silently exempt from the only check that exists for accept-row vacuity.** The tool's own docstring
is scrupulous about two *parsing* traps and does not ask what makes a member a member. Secondary: a row that
reddens **only** on the HEAD null-medium leg counts as "carrying a measured kill", which is not what the
vacuity floor means -- not live here (every `bnd` row has a real mutant kill), but the check would not say so.
Minor, round-local, not a gate. Recorded, not demanded.

**(c) THE `a0` x `a1` JOINT DISCLOSURE IS CORRECT UNDER THE STANDING BOUND -- I derived that before reading
`PRETABLE.out`, and I am naming the sweeping mutant so the next pass measures instead of arguing.** The
guarded body is a single call with **no conditionals at all**, so under the 2026-09-04 joint-cell ruling it
induces no partition on `a1` and there are no joint cells to enumerate; under the pass-11 refinement the
floor is the guard's predicates crossed with *device-state* lvalues the repair path reads, and `a1` is a
second guest input, i.e. a single-operand marginal. Clause (e) is the right disposition and `PRETABLE.out`'s
`GUARD FIELD vs BODY FIELD` section reaches it in the same words. **The residual doubt is real and belongs
to the next pass, not to me:** the measuring seat's alternative bound (*the cross-product of the value
classes the rows establish*) would call it floor, because `a1` is exercised at `a0 = 2` only. The
discriminating mutant is

```c
if ((int64_t)a0 >= 1 && (int64_t)a0 <= 3 && !((int64_t)a0 == 1 && a1 == 0))
```

which I predict **15/15, a total escape** -- `bnd lo` drives `a1 = 0x6000` and `bnd a1z` drives `a0 = 2`, so
no row enters the cell. One build settles which bound is right, and the answer generalises past this round.

**(d) THE DISCLOSURE'S SEVERITY IS UNDERSTATED, WHICH IS FREE TO FIX.** The contract says *"multi-axis
joints, where `a0` and `a1` are perturbed in one edit"* are not rowed. A reader takes that for a corner. It
is a **clean sweep of the whole instrument**. Clause (e) exists so a later escape lands as *"outside the
contract, as stated"* rather than as a breach -- and that only works if the statement conveys the size. One
clause: *"such a mutant is predicted to sweep 15/15."*

**(e) POSITIVE, AND I checked it rather than assuming it: EVERY LEG OF THE KILL TABLE RECONCILES FROM THE
SOURCE BY HAND.** I derived each score from the guard text and the row set without reading `RESULTS.txt`:

| leg | my derivation | recorded |
|---|---|---|
| HEAD `a0 >= 1` | `-2`/`-1` take selective with `a1=0` so `tbia obs`+`tbiap obs` red; `a0=4` and `0x100000001` take selective so `bnd out`+`bnd wide` red; `a0=0` still reaches ALL so `bnd zero` green | **11/15** ✓ |
| M_F `&& a0 != 2` | all three `a0=2` rows red: `bnd mid`, `bnd a1z`, `bnd a1hi`; `pos obs` green because ALL flushes its target too | **12/15** ✓ |
| M_H `>= 1 && != 4` | `bnd out` GREEN (4 still refused), `bnd wide` red | **14/15** ✓ |
| M_A/B/C/D/E/G/I | one row each, as the axis table predicts | **14/15** each ✓ |

The `0x100000001` row is the sharpest thing in the instrument and it is right: `load_const()` genuinely
cannot build that value (it composes `LDAH`+`LDA`, a sign-extended 32-bit range), and the `LDQ`-off-the-
pointer-vector workaround adds no new encoder. `bnd a1hi`'s `load_const(A1, 0x8000)` also checks out
(`LDAH 1` then `LDA -32768` = 32768), and both `a0` sources are one instruction so the `step N` count is
stable across rows -- which matters, because a drifting step count would silently truncate a session.

**(f) `PRETABLE.out` IS THE BEST ONE I HAVE READ IN THIS PROJECT, and it earned its keep twice.** It
predicted M_D and M_E as clean sweeps *before table 1 ran* (mtime 10:34 vs the first t3 log at 11:39), the
rows it prescribed were added, and both mutants now die. The mandated diff of the shipped row list against
its prescribed rows is clean. That is the `#490` failure -- prescribed rows lost in a later rewrite -- not
happening, and it is worth saying out loud on a round where I am otherwise finding L4s.

---

## SUMMARY OF WHAT I WOULD CHANGE BEFORE THIS SHIPS

Nothing in the executable line. Four L4s, all in prose, none requiring a re-table:

1. **`alpha_tbi_probe.py:56-57`** -- delete the *"loss of the signed cast -- the original defect"* bullet;
   it contradicts the corrected comment, names an unkillable edit, and tells a future simplifier they are
   reintroducing a bug when they are improving portability. Make the probe's contract match the
   CHANGELOG's, which is already right.
2. **`alpha_tbi_probe.py:58`** -- *"omission of the invalidation entirely"* is listed as measured and is
   not. Build the `else ;` mutant, or say *derivable, not separately measured*.
3. **`cpu_alpha_palcode.c:392-402`** -- replace the `#514` warrant with `swpipl:423` / `wrmces:208-212`
   (silent normalisation of an unrepresentable guest input, same file, same function) and state that the
   arm deliberately departs from this file's four `fatal()`-and-halt selector sites. Cite
   `alpha_cpu.h:281-285` for the `[1,3]` window while you are there.
4. **`alpha_tbi_probe.py`** -- disclose the ITB/DTB conflation and stop labelling `bnd lo`/`bnd mid` as
   "ITB"/"DTB" selective; note that both rows would red on a correct future split. Add the one clause
   saying the disclosed `a0`x`a1` joint is a predicted **total** sweep.

Two things I explicitly do **not** ask for: an announce (the addition licence is right and I would refuse
one), and any change to `(int64_t)` (implementation-defined is not undefined, every real compiler is fine,
and churn needs a warrant too).
