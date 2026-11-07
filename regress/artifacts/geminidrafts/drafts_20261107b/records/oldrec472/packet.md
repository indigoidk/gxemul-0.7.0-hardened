# Reading task: oldrec472 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBOLDREC472-c55d` on a line of its own.

# GXemul hardened fork -- RECORDS CHECK of one landed round's CHANGELOG block: #472 b115 (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator and this fork records each
fix in a CHANGELOG round block.  The block below has landed; a flagship review of it is still owed.  You cannot read files, so
judge the block AS WRITTEN.  Do not simply ratify it.  A bracketed dated note inside the block is this project's in-place
correction form (it quotes the text it corrects); it is not by itself a contradiction.

## The round block (CHANGELOG.md lines 21601-21732 of CHANGELOG_8d9df658.md; each line carries its own number -- cite those numbers)

```text
21601| ## Round 472 (#472) -- an unaligned overlay read took its bytes from the wrong layer
21602| 
21603| `fread_helper()` picks an overlay layer for the block containing `curofs`, then reads up to a
21604| whole block from that layer **without clamping to what remains in the block**.  With an
21605| unaligned offset the read runs past that block's end into blocks that may belong to a different
21606| layer, while `buf` advances on a fixed `OVERLAY_BLOCK_SIZE` stride.
21607| 
21608| **MEASURED, on the committed build, before any edit:** a 1024-byte read at offset 511 of a disk
21609| whose overlay holds only block 0 returned **512 overlay bytes where exactly one was correct**,
21610| and returned **1 = success**, so nothing surfaced to the caller.  Silent wrong data.
21611| 
21612| ### The asymmetry is what makes it unambiguous
21613| 
21614| `fwrite_helper()` explicitly REFUSES a non-multiple length and an unaligned offset, both under
21615| `#164`.  `fread_helper()` has no such guard anywhere.  The read path was never given the check
21616| the write path has -- and the loop's own advance expression proves unaligned starts were
21617| anticipated: `curofs = (curofs | (OVERLAY_BLOCK_SIZE-1)) + 1` rounds UP to the next boundary,
21618| which would simply be `curofs + OVERLAY_BLOCK_SIZE` if offsets were always aligned.
21619| 
21620| A panel seat supplied the algebra that makes the clamp provably consistent with that advance:
21621| `curofs + remain` **is** `(curofs | (OVERLAY_BLOCK_SIZE-1)) + 1`, identically.
21622| 
21623| ### The fix
21624| 
21625| Clamp `lentoread` to the current block's remainder, and advance `buf` by what was consumed.
21626| 
21627| > *** 'WHAT WAS CONSUMED' IS CORRECTED BY `#488`, WHICH FOUND THE SAME WORDING IN THE
21628| > PRODUCT COMMENT THIS ROUND SHIPPED. ***  `buf` advances by `lentoread`, which is what was
21629| > REQUESTED.  The two are equal on a full read and differ on a SHORT one -- and the short
21630| > case is the defect `#488` fixed.  What tips this from ambiguity to a wrong record is the
21631| > sentence below pairing it with *"indexes the buffer by bytes actually delivered"*, which
21632| > is the file-side reading; the two halves of this block cannot both be right.  Corrected
21633| > here rather than only at the code, because `#488` corrected the code and left these
21634| > siblings standing for several hours -- the grep-for-siblings rule, broken by the round
21635| > that was applying it.
21636| Same shape as `diskimage_access__cue()` in the same file, which already clamps to the remainder
21637| of the current sector and indexes the buffer by bytes actually delivered.
21638| 
21639| **`buf += OVERLAY_BLOCK_SIZE` appears TWICE.** `fwrite_helper()` has it too, and there the
21640| fixed stride is CORRECT because that path refuses unaligned access outright.  Patching the
21641| first occurrence would have broken the write path; an anchor-count guard caught it.
21642| 
21643| ### The detector, and the mutant that pass 1 found
21644| 
21645| Six rows in `regress/diff_diskimage_io.c`, which `#include`s the real `diskimage.c` and builds
21646| with one compiler invocation in under a second.  The oracle is a COUNT, not a value: a
21647| value-only oracle can be satisfied by reading the same byte twice.
21648| 
21649| **Two seats independently named a mutant that ESCAPED the first draft** -- apply the length
21650| clamp and keep the fixed stride.  Under it the wrong-layer row reads 1, which is the CORRECT
21651| answer, because iteration 1 writes one byte and the stride then skips 511 positions.  The
21652| buffer does not receive wrong bytes; it receives HOLES.  So a second row counts bytes the read
21653| never wrote.
21654| 
21655| **The kill table, measured in a copied tree so no repo file was mutated:**
21656| 
21657| ```
21658|   arm                        wrong-layer row      never-wrote row
21659|   PRISTINE (committed)       FAIL 512, want 1     ok 0
21660|   MUTANT   (clamp only)      ok 1  <- ESCAPES     FAIL 511, want 0
21661|   FIXED    (clamp + stride)  ok 1                 ok 0
21662| ```
21663| 
21664| The two rows are measurably non-redundant: each catches what the other misses.
21665| 
21666| ### The floor breach pass 2 found, and the panel I misread
21667| 
21668| *** THE FIRST DETECTOR BREACHED VACUITY FLOOR CLAUSE (d), AND I ARGUED THE WRONG CLAUSE WHEN
21669| DECLINING TO FIX IT. ***
21670| 
21671| The fix INTRODUCES the predicate `len > remain`.  Clause (d) says weaken an introduced
21672| predicate to the least-restrictive form that still READS like the same check.  Two such
21673| mutants passed all six rows:
21674| 
21675| ```
21676|   len > OVERLAY_BLOCK_SIZE ? remain : len     the bound relaxed
21677|   remain = inblock ? 1 : OVERLAY_BLOCK_SIZE   the remainder faked
21678| ```
21679| 
21680| Both survived because the section produced only `inblock` in {0,511} and `len > 512`.  **The
21681| uncovered caller is real, and this round's own census had named it**: `bootblock_iso9660.c`
21682| reads 256 bytes at an offset snapped only to 2048 -- arbitrary mod 512.
21683| 
21684| I declined a fixture change on an L1 argument (*these rows are not vacuous*).  True, and the
21685| WRONG CLAUSE: this is (d)/L2, replaced in-round however late.  ONE row closes both, MEASURED:
21686| 
21687| ```
21688|   arm        short-unaligned row (510+3, want 2)   total
21689|   fixed      ok                                    53 rows, 0 failures
21690|   pristine   FAIL                                  2 failures
21691|   relaxed    FAIL  <- GREEN before this row        1 failure
21692|   faked      FAIL  <- GREEN before this row        1 failure
21693| ```
21694| 
21695| *** AND I REPORTED THE PANEL AS THREE RATIFICATIONS WHEN IT WAS NOT UNANIMOUS. ***  grok said
21696| **DETECTOR IS NOT DONE**; minimax said **NO RATIFICATION**, twice; codex said GO WITH CHANGES.
21697| I carried that misreading INTO A BRIEF, so a later seat was told the panel agreed.
21698| 
21699| **The dissenting seats were right, and their objection IS the clause-(d) breach above.**  Not
21700| merely failing to read a dissent, but propagating the misreading forward.
21701| 
21702| ### Assessed, not changed
21703| 
21704| * **The short-read path is UNCHANGED and still has a pre-existing concern**: on a short read in
21705|   a non-final iteration, `len` decrements by the requested amount while `totallenread` grows by
21706|   the actual, so the caller's zero-fill can cover the wrong region.  **The patch WEAKLY HELPS**
21707|   -- the hole shrinks from `BS - lenread` to `lentoread - lenread`.  An earlier draft said it
21708|   "neither helps nor worsens", which is wrong in the safe direction.  Filed as `shortread`.
21709| * **The aligned path is byte-for-byte unchanged**, proven rather than asserted: when `curofs` is
21710|   aligned, `remain` is the block size and both expressions reduce to the originals.
21711| * **RUNG 1 IS A DETECTOR, NEVER A WITNESS.**  This harness calls the function directly, so it
21712|   is graded by the vacuity taxonomy, not the witness clauses.  A rung-3 witness still needs a
21713|   real emulator run, which the machine embargo forbids.
21714| 
21715| ### Collateral, and a build tree I missed
21716| 
21717| *** THE WSL ARC TREE WAS NEVER PROPAGATED TO, AND I REPORTED THE OPPOSITE. *** I said
21718| "both build trees byte-identical", counting `build/` and `build-asan/` and **forgetting
21719| the WSL arc tree at `/tmp/gxsec-build` entirely**.  It was still at 2386 lines with ZERO
21720| `#472` markers against SEC's 2400 and two.  Found by the adjudicating seat, verified, then
21721| propagated and confirmed by `cmp` against SEC -- never against a backup -- with the stale
21722| `.o` removed.
21723| 
21724| **This is the no-VPATH rule's exact hazard**: any arc measurement taken meanwhile would
21725| have measured unfixed code and looked clean.  The correct statement is now FOUR trees --
21726| `est/`, `build/`, `build-asan/` and the WSL arc tree -- all byte-identical to SEC.
21727| 
21728| Eleven offline differentials run in ten seconds total; all green afterwards.  One of them
21729| needs `-Wl,--wrap=fsync -Wl,--wrap=fflush` and reads as failing without them -- it passes
21730| clean with the fix and the right flags.
21731| 
21732| 
```

## Questions -- verdict line first

1. Does the block contradict itself anywhere -- two different numbers for one quantity, a total that its own parts do not sum
   to, a claim in one paragraph that another paragraph undoes?  Quote both places, with their line numbers.
2. Which claims are stated as MEASURED but cite no artifact, or cite one only by a bare file name that could be ambiguous?
3. Which sentences overclaim -- 'every', 'all', 'never', 'exactly' -- where the block's own evidence covers less?
4. What would a reviewer checking this block against its artifacts most likely find wrong?
When you count items the block enumerates, list them by name before giving the count.

End with one line: `RECBLOCK_472: <c> CONTRADICTIONS, <u> UNCITED, <o> OVERCLAIMS`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBOLDREC472: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
