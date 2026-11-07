# Reading task: oldrec450 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBOLDREC450-972f` on a line of its own.

# GXemul hardened fork -- RECORDS CHECK of one landed round's CHANGELOG block: #450 arcbiosubsan (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator and this fork records each
fix in a CHANGELOG round block.  The block below has landed; a flagship review of it is still owed.  You cannot read files, so
judge the block AS WRITTEN.  Do not simply ratify it.  A bracketed dated note inside the block is this project's in-place
correction form (it quotes the text it corrects); it is not by itself a contradiction.

## The round block (CHANGELOG.md lines 29608-29720 of CHANGELOG_8d9df658.md; each line carries its own number -- cite those numbers)

```text
29608| ## R19 (#450) — ten uncast shifts, and the author had already cast four of them
29609| 
29610| `src/promemul/arcbios.c`. `buf[]` is `unsigned char`; `buf[3] << 24` promotes to `int`, and with
29611| `buf[3] >= 0x80` the result is unrepresentable — C99 6.5.7p4, undefined behaviour. **Fourteen
29612| sites, four already cast correctly** — and line 580 sits between two uncast siblings at 570 and
29613| 590, so the author knew the idiom and applied it to 4 of 14. A class, not a typo.
29614| 
29615| At the three 64-bit-assembly sites the wrapped-negative `int` converts to `uint64_t` before the
29616| high-byte terms are added, so the assembled pointer is **`V − 2^32`: low word correct, high word
29617| one too small**. Concrete witnessed value: `FIRST_ARC_COMPONENT` is `0xffffffffbfca8000`, whose
29618| swapped `buf[3]` is `0xBF = 191` — the exact number in the UBSan message.
29619| 
29620| MEASURED on a freshly rebuilt instrumented tree: 2 shift lines on each reaching subtype
29621| (`:570/:590` on ip12/ip32/ip35, `:737/:784` on ip28/ip30), ASan 0 everywhere — the rebuild also
29622| independently re-confirmed `#446`.
29623| 
29624| ### Scope was contested in pass 1, and adjudicated ALL TEN
29625| 
29626| One seat argued for the four witnessed sites only, under the round rule's witness clause. Two
29627| argued all ten, and the decisive form of the argument: **the cast is provably value-neutral
29628| wherever the UB is not firing, so there is nothing per-site for a witness to adjudicate** — and
29629| leaving six known-UB sites means the next image or subtype reopens the identical round. The
29630| coverage objection (six fixes no sweep can exercise) is answered by the census row below, and the
29631| kill table proves that answer rather than asserting it.
29632| 
29633| Width-matched casts per the house idiom. A seat corrected the brief's arithmetic here: the four
29634| pre-existing casts split **3-to-1** (`(uint64_t)` at `:1349/:1400/:1449`, `(uint32_t)` only at
29635| `:580` [corrected 2026-11-02, records: said `:600`; at f39b8984^, the tree this round started from, `src/promemul/arcbios.c:580` is the one pre-existing `((uint32_t)buf[3]<<24)` and `:600` is the end of a commented-out debug]), not 2-and-2 as the brief claimed — the house rule is *the cast matches the width of the
29636| value being assembled*, and the fix follows it.
29637| 
29638| ### Two gate-9 rows, because the existing three-way CANNOT pin this
29639| 
29640| `sanhit()` already counted these `runtime error:` lines — but gate 9's assertion is
29641| **directional**, and reverting the casts lands on dirty-upstream/dirty-HEAD, which is scored
29642| "pre-existing, reported but not failed". A revert is invisible to it.
29643| 
29644| * **Behavioural**: the five reaching SGI subtypes must produce ZERO left-shift lines and zero
29645|   ASan (which re-pins `#446` through the same fresh binary). Inherits gate 9's staleness caveat
29646|   (`asanstale`), stated in the row rather than hidden.
29647| * **Static census**: every `buf[3] << 24` in the file carries a width-matched cast — 14 casts,
29648|   0 uncast. Deliberately binary-independent, so it stays load-bearing when the instrumented
29649|   binary is stale, and it is the only row that can see the six sites no current image drives
29650|   with `buf[3] >= 0x80`. It also kills the mutant no sanitizer can: `(buf[3]&0x7f)<<24` is
29651|   UB-free, silently drops bit 31, and passes every sweep — the census counts 13 and reddens.
29652| 
29653| KILL TABLE, measured (census cast/uncast; sweep5 = shift lines over the five reaching subtypes):
29654| clean 14/0, 0 · revert witnessed `:737` → 13/1 **and** sweep 2 (both rows) · revert unwitnessed
29655| `:1413` → 13/1, sweep 0 (**census only — the measurement that proves it load-bearing**) ·
29656| `&0x7f` at `:570` → 13/0, sweep 0 (census only).
29657| 
29658| ### *** A VOID MEASUREMENT CAUGHT MID-ROUND: build_asan.sh BUILDS FROM GIT HEAD ***
29659| 
29660| Its first "post-fix" sweep reported the PRE-fix counts with rc=0 — because `build_one` runs
29661| `git archive "$src"`, so an uncommitted fix silently measures the committed source. Rule 4
29662| ("did it fail for the reason under test?") caught it: the UBSan lines still named the OLD
29663| sites. The real verification used a private tree with the working-tree file installed and
29664| **verified by cmp before building**. Recorded here because rc=0 from that script means "HEAD
29665| built", never "your edit built".
29666| 
29667| ### Per-site truth table, as corrected by the panel
29668| 
29669| The round's own pass-1 analysis was WRONG twice and the seats fixed it: the claimed
29670| "mis-linked component tree" was a **counterfactual about `:751`** (the witnessed site `:737`
29671| feeds only `== 0` tests, which sign extension cannot change — corruption forces the low word
29672| ≥ 2^31, so a corrupted value can never alias zero); and the 64-bit `parent` parameter is
29673| `uint64_t`, not a promoted `uint32_t`. A seat also completed the trace: both mis-link
29674| directions exist (false negative at true-high-word 0, **false positive at true-high-word 1**),
29675| data-dependent. The Get* trio (`:1362/:1413/:1462`) is value-benign because the 4-byte branch
29676| and the `(int64_t)(int32_t)` truncation are keyed on the SAME `arc_64bit` condition — read and
29677| confirmed, not assumed.
29678| 
29679| ### Residual filed, not fixed: `arcbioswalk64`
29680| 
29681| The 64-bit component walker reads `peeraddr + 0x34` for "IdentifierLength". With the
29682| 0x18-byte pointer header (`ptr_peer/ptr_child/ptr_parent`) ahead of `arcbios_component64`
29683| (which is why the walker steps `+0x50`), **`+0x34` falls inside AffinityMask (+0x30..0x37);
29684| IdentifierLength is at `+0x40`.** The walker reads a slice of the wrong field, masks it, and
29685| skips accordingly — a wrong-offset defect, different semantic class, its own round.
29686| 
29687| Gates: gate 9's two new rows green post-commit (behavioural row requires the committed tree by
29688| construction); census + kill table measured pre-commit. Twin tree and both NO-VPATH trees carry
29689| `arcbios.c` byte-identically; `build/` rebuilt, rc=0, zero warnings.
29690| 
29691| ### Pass 2: FOUR seats killed the census v1 with one token each, and v2 is a frozen table
29692| 
29693| The first census was two greps ("14 cast spellings, 0 uncast"). Four seats independently
29694| returned DEFECT-IN-DETECTOR against it, each with a concrete escape: `& 0x7fffffff` appended
29695| after a cast (keeps the spelling, passes every sanitizer, silently drops bit 31);
29696| `~(uint32_t)` one character before it; a comma-expression smuggling a signed shift behind a
29697| cast match; and an ADDED dead statement `(int)buf[3]<<24` that reintroduces the exact UB while
29698| both counts hold. *** A PATTERN PINS WHAT ITS AUTHOR THOUGHT OF. ***
29699| 
29700| The replacement is `regress/arcbios_shift_probe.py` — the `#444` S4 precedent: every
29701| buf[]-assembly statement, whitespace-normalised and comment/string-stripped, exact-matched as a
29702| multiset against a **frozen table of 14 canonical statements** (generated from the reviewed
29703| file, not typed — the hand-assembled-encoding trap has five recorded incidents). MEASURED: all
29704| four seat escapes, plus the earlier three mutants, die to C1; a comment quoting the uncast
29705| idiom no longer false-positives (v1's known loud cost, closed by the stripper). The accepted
29706| trade is S4's: a legitimate edit to any of the fourteen must update the table in the same
29707| commit.
29708| 
29709| A fifth seat point landed on the behavioural row: **zero matching lines from a run that never
29710| constructed is an absent measurement, not a clean one** — so each subtype must now show its own
29711| `model: SGI-` banner or the row reddens. *** THE FIRST TOKEN CHOSEN FOR THAT CHECK WAS ITSELF
29712| MEASURED WRONG BEFORE SHIPPING *** — it returned 0 on a live construction because the probe run
29713| lacked gate 9's `detect_leaks=0` environment; verified present on all five subtypes under the
29714| gate's exact env before landing. A liveness token nobody verified is how a row goes
29715| permanently red — or worse, how "never ran" reads as clean.
29716| 
29717| Grok also completed the `arcbioswalk64` picture: the misaligned `+0x34` read is WHY 64-bit
29718| construction witnesses `:784` at all — the bytes it decodes are AffinityMask `0xffffffff`,
29719| which is what supplies a `buf[3] >= 0x80`.
29720| 
```

## Questions -- verdict line first

1. Does the block contradict itself anywhere -- two different numbers for one quantity, a total that its own parts do not sum
   to, a claim in one paragraph that another paragraph undoes?  Quote both places, with their line numbers.
2. Which claims are stated as MEASURED but cite no artifact, or cite one only by a bare file name that could be ambiguous?
3. Which sentences overclaim -- 'every', 'all', 'never', 'exactly' -- where the block's own evidence covers less?
4. What would a reviewer checking this block against its artifacts most likely find wrong?
When you count items the block enumerates, list them by name before giving the count.

End with one line: `RECBLOCK_450: <c> CONTRADICTIONS, <u> UNCITED, <o> OVERCLAIMS`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBOLDREC450: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
