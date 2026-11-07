# Reading task: oldrec568 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBOLDREC568-6676` on a line of its own.

# GXemul hardened fork -- RECORDS CHECK of one landed round's CHANGELOG block: #568 vmedefaultkill (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator and this fork records each
fix in a CHANGELOG round block.  The block below has landed; a flagship review of it is still owed.  You cannot read files, so
judge the block AS WRITTEN.  Do not simply ratify it.  A bracketed dated note inside the block is this project's in-place
correction form (it quotes the text it corrects); it is not by itself a contradiction.

## The round block (CHANGELOG.md lines 2642-2787 of CHANGELOG_8d9df658.md; each line carries its own number -- cite those numbers)

```text
 2642| # `#568` (vmedefaultkill): the MVME187's VME2 controller model ended the emulator on any offset its switch did not name -- the 26 header-named registers it does not implement now DECLINE with one announce per register, every other unmatched offset FAULTS to the guest; with a 38-row rung-3 detector, gated in gate 14
 2643| 
 2644| **The defect** (`vmedefaultkill`, HIGH).  `DEVICE_ACCESS(vme)` named ten offsets of its 4 KiB window; every other offset
 2645| reached `default:`, which printed with `debug()` -- silent at default verbosity while free-running -- and called
 2646| `exit(1)`, so the emulator ended with no visible reason.  The device exists only on `-E mvme88k -e mvme187` (window
 2647| 0xfff40000-0xfff40fff).  The OpenBSD 2.2 mvme88k driver's attach reads MASTERCTL and writes MASTERCTL, MASTER3, MASTER4
 2648| and MASTER4MOD -- four of the unimplemented registers -- so on HEAD that guest's attach would end the emulator at its
 2649| first MASTERCTL read (read from the driver source; the witness measures the access sites, not a boot).  Witness, rung 3
 2650| on unmodified `-E mvme88k -e mvme187` at HEAD 5dbc000e: 7 of 7 guest access sites end the emulator (rc 1), and a
 2651| free-running MASTERCTL read dies with no `[ vme:` text (`regress/artifacts/vmedefaultkill/witness_20261020/SUMMARY.md`).
 2652| 
 2653| **The rulings it implements.**  Owner, 2026-09-11: population 1 (the word starts the header does not name) FAULTS --
 2654| `return 0`, which `memory_rw.c` turns into the m88k data-access exception for a guest data load or store.  Sub-word
 2655| starts take the same `return 0` only as an INTERIM: that ruling does not reach them (Fable 5.1's 7n-4), and
 2656| `vmewidthlanes` decides them.  Owner, 2026-10-09: population 2 (the 26 header-named registers with no case) DECLINE + ANNOUNCE ONCE --
 2657| reads served the preloaded word, writes dropped, one latched `fatal()` per register, `(once)`, `#501`'s shape.
 2658| 
 2659| **What ships.**
 2660| * `src/devices/dev_vme.c` -- 26 exact case labels (SADDR2 .. MISC) decline: a read is served `d->reg[]`'s word, which
 2661|   is 0 because nothing writes those words (odata is deliberately not forced to 0, so a store a later edit added would
 2662|   show in a read-back); a write is dropped; a new `uint64_t warned_unimpl` latch (one bit per register word,
 2663|   `relative_addr >> 2`, the highest 35) prints one `[ vme: unimplemented read from register 0x%x (len %d) -- served
 2664|   0x%llx.  (once) ]` or `... write to register 0x%x (len %d): 0x%llx -- declined.  (once) ]` per register per device,
 2665|   the first access's direction deciding the wording.  A compile-time check makes a field narrower than 36 bits an
 2666|   error (the `1ULL` in the shifts is NOT checked there; the probe's announce rows catch a narrowed literal at run time
 2667|   -- measured, leg M_ONENARROW).  `default:` keeps both `debug()` lines and returns 0 instead of `exit(1)`.  `est/`
 2668|   byte-identical; `build/`, `build-asan/` and `/tmp/gxsec-build` rebuilt and cleared both parts
 2669|   (`apply_20261021/APPLY568B.out`, kept whole: its failed probe copy and stale probe md5 are the apply script's,
 2670|   and the probe was installed by hand after it).
 2671| * `regress/vme_default_probe.py` (new, 38 rows, rev 3) -- controls (a bogus subtype, the session, a liveness `or`, the
 2672|   DEVINIT VBR seed as the device signature, the free-running proof); the ten cased offsets read and their write paths
 2673|   round-tripped; the 26 population-2 registers read and written (all 0, nothing stored, no fault) at word, sub-word
 2674|   and doubleword widths; the announce in two free-running two-pass sessions covering 26 labels x {read, write} x
 2675|   {latch clear, set}; the non-word first accesses and their second pass in the same process; a first-access ZERO store
 2676|   (`p2 zero wr`); population-1 faults at the edges, an interior sample, both directions, all 988 word starts free-running,
 2677|   eight widths and lanes, and no host text (`p1 quiet`); the interim sub-word pins `vmewidthlanes` will re-derive.
 2678|   CONTROL rows are prerequisites, not causes: a CONTROL=FAIL says a prerequisite failed.  Its CONTRACT and NOT CLAIMED
 2679|   list are its header; the store-data disclosure names its untested slice.  The shipped file differs from the copy kill
 2680|   table 2 ran (`killtable2_20261021/vme_default_probe.rev3.frozen.py`) in docstring and comment text only -- the
 2681|   repair-diff pass's and the records confirmation's corrections; AST-identical with the module docstring removed.
 2682| * `regress/gate_arm.sh` (gate 14) -- the probe's block after `#536`'s mk48 block: completion sentinel, `vme_default rows
 2683|   run` pinned at 38 (the score-claims pin), CONTROL `OK`, every row by name green exactly once, emitted/green/red pinned
 2684|   at 38/38/0.
 2685| * `regress/gate_hygiene.sh` (gate 6) -- by `tools/derive_hygiene_pins.sh`, never by hand: the probe GRANDFATHERED by name
 2686|   (`--grandfather`) and `EXPECT_PTY_PROBES` 76 -> 77 (`--write`).  The census counts what lies in the tree the weekly
 2687|   battery runs (the 2026-09-23 owner ruling), so 77 = 75 committed + this probe + another session's untracked
 2688|   `lca_isaphys_probe.py`.  The probe is not promptless in substance -- its pty driver waits for `GXemul> ` with `in` and
 2689|   `find` -- but the census keys on a code-level call of the ends-with method and cannot see that, as with
 2690|   `alpha_tbi_probe.py`; the block note says so.
 2691| * `tools/precommit_check.sh` -- `SCORE_CLAIMS_MANIFEST` 36 -> 37 (`vme_default rows run ... 38`).
 2692| * `tools/pipeline/check_probe_wiring.py` -- the probe's MANIFEST line (DETECTOR), the witness's two scripts (WITNESS)
 2693|   and the tables' instruments and frozen copies (RESEARCH, by the `#471` definition at `CLASS_RESEARCH`).
 2694| * `tools/pipeline/ledger.json` -- `vmedefaultkill` HELD on the two questions in its `hold_question`: Fable 5.1's regress
 2695|   review (FABLE-ONLY), and the research and review stages, which stand at 4/9 -- the five seats the owner's 2026-10-20
 2696|   roster did not fire carry the non-answer token and a held marker each, the form `sgirekills`' assess hold takes,
 2697|   until the owner rules on `untokenedanswers` (2).  The markers were added after precommit section H refused the first
 2698|   commit attempt (a stage short of nine with no hold).  With the pass-2, F2 and repair-pass seat entries and the
 2699|   not-fired seats named per phase (the five pass-1 not-fired entries tokened too); `vmewidthlanes` widened;
 2700|   `vmewarnedbit`, `vmeprobedebt` and `m88kpsrmxm` filed.  `matrix.html` and `fable_queue.md` re-rendered.
 2701| 
 2702| **Measured** (`regress/artifacts/vmedefaultkill/`; every MUTANT leg's prediction written first, in a `PRETABLE*` file
 2703| whose mtime is the order proof -- table 2's three reference runs and the object comparison were built before PRETABLE2,
 2704| which its section 0 discloses).
 2705| * Kill table 1 (`killtable1_20261020/`, rev 2, 34 rows, fix568): 24 legs -- every one red except the two predicted
 2706|   equivalents M_ODATA0 and M_SERVED0 (34/34: no population-2 word is ever non-zero); HEAD 14/34; clause (b) M_EXIT
 2707|   24/34; clause (c): measured at `killtable1_20261020/legs/NULL.raw` (the vme `device_add` removed) 5/34 CONTROL=FAIL;
 2708|   M_CAPNARROW fails to compile.  Eleven prediction misses, every one an incomplete prediction list
 2709|   (`KILLTABLE1_VS_PRETABLE.out`).  Table 1b (`table1b/`): the three legs observation (c) owed, all red as predicted.
 2710| * Pass 2's floor breach, measured BEFORE the repair (`killtable1_20261020/idata/`): M_IDATA -- the population-2 arm's
 2711|   `if (writeflag == MEM_WRITE)` read as `if (idata)` -- 34/34 on the frozen rev 2, because every population-2 store the
 2712|   probe made was non-zero.
 2713| * Kill table 2 (`killtable2_20261021/`, rev 3, 38 rows, fix568b): 34 legs (27 regenerated, 7 new) -- 32 killed
 2714|   (M_CAPNARROW by its failed build), the same 2 predicted survivors; M_IDATA red at `p2 zero wr` 0/1; one prediction
 2715|   miss, M_ONENARROW, killed by four rows instead of two because GCC 15.2.1 -O3 folded the undefined `1u << 35` to 0 at
 2716|   MISC (`obj/M_ONENARROW_codegen.txt`); BASE 38/38, HEAD 14/38, NULL 5/38 CONTROL=FAIL; no timeout red.  Its summary's
 2717|   "first build log 01:16:55" is configure's (the first build is 01:17:37); a correction is appended to the file.
 2718| * Table 2b (`table2b/`, the repair-diff pass's first seat): M_IDATABIT1 -- the direction test qualified by
 2719|   `&& !(idata & 2)` -- 38/38 as predicted: a clause-(e) survivor, every population-2 store value carrying bit 1 clear.
 2720| * Table 2c (`table2c/`, the repair-diff pass's GLM 5.3 seat): `default:`'s refusal conditioned on idata, both polarities
 2721|   -- M_DFLTIDNZ 29/38 and M_DFLTIDZ 36/38, killed as predicted (a read carries idata 0; every population-1 store is
 2722|   non-zero); M_DIRODATA, an odata conjunct on the direction test, 38/38 and compiled to the fix's own binary -- odata is
 2723|   assigned only on a read, so the conjunct is constant-true on the write path: an equivalent mutant, not a sampled slice.
 2724| * Table 2d (`table2d/`, the repair-diff pass's Argon answer): three predicted survivors, all 38/38 -- M_ZEROSET (the
 2725|   latch set skipped for a zero-valued store: `p2 zero wr` pins the announce's form, not the set; clause (e)), M_SETODATA
 2726|   (`!odata` on the set; equivalent under the fix's invariant), M_DFLTFFC (`default:` serving 0xffd..0xfff, which no row
 2727|   touches; clause (e)) -- each now named in the probe's NOT CLAIMED list.
 2728| * fix568b's object code is NOT identical to fix568's beyond the read announce's format: the comment lines moved
 2729|   DEVINIT's `__LINE__` (231 -> 234, via `CHECK_ALLOCATION`) and the `(unsigned long long)` cast changed `-O3`'s layout
 2730|   of the access function (`OBJDUMP_fix568_vs_fix568b.txt`).  Behaviour is what table 2 measured.
 2731| * Gate 14.  Rev 2 (`gate_20261020/`): the block alone FAIL 22 of 39 on a pre-fix binary and PASS 39/39 on the fix; the
 2732|   full gate PASS, 1264 checks -- on `build/gxemul`, which carried another session's uncommitted `dev_pcc2.c`,
 2733|   `mvme_pcctworeg.h`, `dev_lca.c`, `dev_sh4.c` and `cpu_alpha_palcode.c` (`build/` mirrors the working tree; gate 14 has
 2734|   PCC2 blocks), so that run is superseded.  Rev 3 (`gate_20261021/`): a CLEAN clone of HEAD 86114a90 (git archive, no
 2735|   uncommitted edits) built twice -- the block alone FAIL 27 of 45 on HEAD's binary (the 24 red rows are table 2's HEAD
 2736|   set) and PASS 45 on HEAD + fix568b (those two runs used an earlier text of the probe, md5 346c7813 -- docstring
 2737|   edits only, AST-identical with the module docstring removed); the FULL gate on that HEAD + fix568b binary PASS, 1270 checks, 0 FAIL, 0 SKIP
 2738|   (04:35:04-06:46:50, run alone; `gate_20261021/GATE14_FULL3.out`, whose first line names the binary, `gate_arm.sh` and
 2739|   the probe by md5: `gate_arm.sh` ships as run; the shipped probe (2cd87fc2) differs from the run's c896d079 only by
 2740|   the records confirmation's comment edits -- AST-identical with the module docstring removed -- and the block
 2741|   re-run on it PASSES 45, `gate_20261021/mini3_FIX_final.out`).
 2742| 
 2743| **Panel.**  Pass 1 (`pass1_20261020/`): GPT-6 Astra, Grok 4.7, GLM 5.3 (packet-fed) and Fable 5.1, plus Argon as a second
 2744| packet-fed lens -- all PROCEED WITH CHANGES; Fable's dissent for a bound test in `default:` was later withdrawn (M_ADD94
 2745| and M_ADD90 measured the label form's growth edit caught).  Pass 2 (`pass2_20261020/`): all four SHIP WITH CHANGES;
 2746| GPT-6 Astra's F8 named the floor breach (above).  Argon's pass-2 packet timed out three times while generating (00:08,
 2747| 01:03, 01:29; its controls passed) -- a seat failure, recorded so.  The adjudication pass (`f2_20261021/`): Fable 5.1,
 2748| GPT-6 Astra, GLM 5.3 and Grok 4.7 all PROCEED WITH CHANGES; the comment's reach count overturned to FOUR (IRQSTAT and
 2749| IRQCLR live only in `vme2abort()`, the ABORT-switch interrupt handler, which this model never triggers); D1 aligned the
 2750| read announce to `%llx`; Grok 4.7's reading that free-running faults print the CPU's DATA_ACCESS line refuted by
 2751| measurement (`probe_20261020/explore2_FIX.out` (b): 8 faults, no line).  The repair-diff pass (`r1_20261021/`, the
 2752| repair-chain rule; review scoped to the repair diff, the floor question asked of the shipped composite): Fable 5.1,
 2753| GPT-6 Astra and Grok 4.7 -- plus a second, adversarial Grok job -- CLOSE, zero floor breaches, each with its
 2754| denominator; GLM 5.3 REPAIR AGAIN on records only, its one floor item (`default:`'s refusal conditioned on idata)
 2755| refuted by table 2c; Argon's first send died on transport like pass 2's ("connection lost while generating", 02:46),
 2756| and its re-send with extended thinking OFF -- every Argon job since 2026-10-15 that ran without it returned, and #568's
 2757| pass-2 and repair-pass packets with it died at ~25 minutes (its pass-1 packet with it returned, in 383 s); recorded as a deviation from the owner's 2026-10-14 "thinking level High" --
 2758| answered REPAIR AGAIN: of its six "broken" items three are kill attributions (another row reds each named edit), and
 2759| three are survivors measured in table 2d and graded clause (e) or equivalent, so no floor breach survives; M_ZEROSET is a
 2760| cell no other seat named.  Its oracle audit of the probe: all 38 excerpted row oracles held against shapes (a)-(e); the omitted helper
 2761| definitions remained UNSETTLED.  Two of the first seat's kill attributions were wrong -- M_LATCHRDSET reds `p2 ann
 2762| wr` and `p2 nw wr 2`, not `p2 ann wr 2`; a latch set redirected into `d->reg[]` does not red `p2 rd census` (odata is
 2763| preloaded before the set) -- found by GPT-6 Astra and the adversarial Grok job; no survivor follows.  Opus 5.5 MEASURED
 2764| (tables 1, 1b, 2, 2b, 2c, 2d, the object comparison, the clean clone) and was not fired as a review seat; agy, kimi,
 2765| deepseek and minimax deliberately not fired (the owner's 2026-10-20 roster).
 2766| 
 2767| **Records corrected on the way.**  The pass-1 adjudication's D5 said the CPU already prints an INFO-level line for a
 2768| free-running fault: false at default verbosity (measured above).  The pass-2 brief's section 3 described another
 2769| unit's `check_probe_wiring.py` lines as this round's.  The repair-diff pass corrected the probe's docstring (no code
 2770| line): the ORDER DEPENDENCE paragraph had stated PRETABLE2's bit-3 prediction as this build's behaviour (table 2
 2771| measured the fold to 0), and its first correction's "a reorder of POP2 could move the kill" was wrong too (a reorder
 2772| changes which register is silenced, not the kill); the CONTROL definition contradicted two of its own CONTROL rows; the
 2773| store-data SAMPLED disclosure now names its untested slice (28 of 64 bits clear in all five store values, bit 1
 2774| measured; the sampled zero pins the announce's form, not the latch set -- M_ZEROSET).  "Object code otherwise identical" (the F2 owed list, the first seat's F2) is superseded by the object
 2775| comparison.  PRETABLE2.out:72's "the 20 population rows die on HEAD" omits the four rev-3 rows (its :236 and the
 2776| machine-readable predictions carry 24); it is not edited -- its mtime is the order proof.  Three seats read
 2777| `check_probe_wiring.py`'s `#471` comment as defining WITNESS; it defines RESEARCH (`git blame`: `#471`, 0a7c4687,
 2778| added `CLASS_RESEARCH` with that comment; `CLASS_WITNESS` dates from 85bc6ab4).
 2779| 
 2780| **Filed / recorded, not this round** (OUTSTANDING_BUGS, 2026-10-21).  `vmewidthlanes` widened (population-2 sub-word
 2781| starts; cased-word `ld.d`/`st.d` lane placement); `vmewarnedbit`, the shared latch-index macro (D5); `vmeprobedebt`,
 2782| the probe's coverage debt (`free quiet`, `vbr rt` and `t1count inc` carry no own-channel kill -- the absent legs: a
 2783| cased arm's `debug()` -> `fatal()` promotion, a VBR write-path break, a T1COUNT write-path break -- and the store-data
 2784| clause-(e) slice); `m88kpsrmxm` (MED): a guest that sets PSR.MXM stops the emulated CPU (`cpu_m88k.c`'s PSR store prints
 2785| `stcr: TODO: MXM support` and clears `cpu->running`), where the MC88100 rounds a misaligned address down -- pass 1
 2786| adjudicated it LOW as an unmodelled divergence before the arm was read.
 2787| 
```

## Questions -- verdict line first

1. Does the block contradict itself anywhere -- two different numbers for one quantity, a total that its own parts do not sum
   to, a claim in one paragraph that another paragraph undoes?  Quote both places, with their line numbers.
2. Which claims are stated as MEASURED but cite no artifact, or cite one only by a bare file name that could be ambiguous?
3. Which sentences overclaim -- 'every', 'all', 'never', 'exactly' -- where the block's own evidence covers less?
4. What would a reviewer checking this block against its artifacts most likely find wrong?
When you count items the block enumerates, list them by name before giving the count.

End with one line: `RECBLOCK_568: <c> CONTRADICTIONS, <u> UNCITED, <o> OVERCLAIMS`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBOLDREC568: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
