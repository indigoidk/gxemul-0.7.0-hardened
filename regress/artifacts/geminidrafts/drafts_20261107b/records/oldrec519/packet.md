# Reading task: oldrec519 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBOLDREC519-2865` on a line of its own.

# GXemul hardened fork -- RECORDS CHECK of one landed round's CHANGELOG block: #519 sgirandomcolour (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator and this fork records each
fix in a CHANGELOG round block.  The block below has landed; a flagship review of it is still owed.  You cannot read files, so
judge the block AS WRITTEN.  Do not simply ratify it.  A bracketed dated note inside the block is this project's in-place
correction form (it quotes the text it corrects); it is not by itself a contradiction.

## The round block (CHANGELOG.md lines 8896-9080 of CHANGELOG_8d9df658.md; each line carries its own number -- cite those numbers)

```text
 8896| # `#519` (sgirandomcolour): unsupported colour PUTs replaced guest pixel data with host-PRNG bytes and flooded diagnostics
 8897| 
 8898| **THE DEFECT.** The DE colour default included documented YCRCB among 12 of 16 type encodings.
 8899| `fatal()` returned; drawing continued into the store and could announce per pixel. The MTE path
 8900| did not reach this arm. Width matters: four PRNG bytes at 32 bpp, one at 8 bpp, and at depth 8
 8901| four PRNG bytes plus an uninitialised tail. The source comment still says “four HOST-PRNG bytes”
 8902| without that qualification; the probe header and ledger review supply it.
 8903| 
 8904| **THE FIX.** In `src/devices/dev_sgi_re.c`, the PUT default clears `ok` outside the warning latch;
 8905| `if (ok)` guards `memory_rw`. A declined PUT preserves the destination. `SGIRE_W_BADCOLOR`
 8906| announces once on its own bit, retaining the attribution prefix. GET and accepted-width buffer
 8907| initialisation remain separate concerns (`sgirebufuninit`).
 8908| 
 8909| **WITNESS — MEASURED, as reported by the ledger.** Rung 3, agy's independent-transport fallback:
 8910| `regress/artifacts/sgirandomcolour/witness_20260910/HEAD_run1.out`: committed `1ce8296`, **2/5**;
 8911| `regress/artifacts/sgirandomcolour/fix_20260910/FIX519_run1.out`: same script on the fix, **5/5**.
 8912| The unsupported YCRCB and reserved PUTs destroyed the paint; the supported RGBA control landed.
 8913| Paint `0x11223344` became `0x56e8857a` and `0x38abc4e1` across runs; the control was `0xaabbccdd`.
 8914| 
 8915| **THE REPAIR CHAIN — historical measurements reported by the ledger.**
 8916| `regress/artifacts/sgirandomcolour/killtable_20260910/`: frozen BASE **14/14**; all twelve planned
 8917| mutants killed, including reinstatement `M1` and whole-file pre-fix `M11`, each **6/14**.
 8918| The frozen source differed from the later source by the announce's extra closing bracket;
 8919| the record says no row or mutant read that token. Codex could not authenticate saved-log binaries.
 8920| Opus's `M13_widthdecline` and `M14_lineardecline` escaped **14/14** and **19/19** in that directory
 8921| (the probe names `M13_widthdecline.raw` and `M14l_lineardecline_vs19.raw`). These are distinct
 8922| from the coordinate mutants later assigned the same numeric prefixes.
 8923| 
 8924| Grok's non-origin guard escape and latch-bit collision prompted the coordinate row, missing
 8925| RGB/RGBA drop-case controls and `allbits` priming. The latter exercises all twelve other latch
 8926| bits in one session; the earlier one-session-per-bit cost premise was false. The remaining
 8927| width/addressing escapes required the mode/depth expansion; clean earlier tables did not close it.
 8928| `regress/artifacts/sgirandomcolour/pass2_20260911/`: `M30`, `M31`, `M32`, `M33`, `M28r`, `M37`
 8929| each **59/59**; the offset/x/y negative controls each **58/59**, killed by `ycrcb x4y1` alone.
 8930| 
 8931| The ledger's subsequent `/tmp/gxop519p2` run reports BASE **77/77**, `M30/M31` **74/77**,
 8932| `M32/M33` **75/77**, and `M28/M37` **67/77** (no preserved artifact).
 8933| It also reports pre-fix `M11` and reinstatement `M1` at **28/77** each, previously **22/59** each
 8934| (no preserved artifact). These reports do not establish the exact historical M28/M28r edit.
 8935| Four redundant `ann cum` assertions were removed and 22 added, taking 59 assertions to 77.
 8936| The ledger records that `M1` lost only those cumulative-count kills; `M38_acceptannounce`
 8937| independently justified retaining `silent`, failing those rows while leaving `ann1` green.
 8938| 
 8939| **WRONG RECORDS, CORRECTED — the ledger retains the claims and their rebuttals.**
 8940| 
 8941| * CHANNEL omitted `ann1`'s drop-case kills: those mutants consume the latch before the marker.
 8942|   The ledger's CHANNEL/red-list audit supplies that attribution; absent markers fail closed.
 8943| * The measuring seat's “sentinel absent” was a false negative: the ledger records that git-bash
 8944|   and WSL resolved `/tmp` to different filesystems.
 8945| * “Skip rather than return” was not observable: after the PUT switch only the guarded store
 8946|   remains. The alleged shared tail belongs to `DEVICE_ACCESS(sgi_re)`. Codex, grok and minimax
 8947|   challenged the claim; the current source confirms it. The later unconditional-return proposal
 8948|   is still absent from the source, which retains the guard.
 8949| * “PUT arms assign four bytes” excludes CI, which assigns one; “does not read the nibble” ignores
 8950|   the diagnostic. The later claim that `color_mode` cannot feed a body-read value also fails:
 8951|   accepting arms fill `buf`. The store reads `tileptr`, `ofs`, `buf`, `bufdepth`; tile indices
 8952|   feed its address. The ledger's source-reading and packet-fed reviews refuted the narrow warrant.
 8953| * Codex/glm corrected the brief's **2 hunks / 58 lines** to **3 hunks, 48 additions + 13 deletions
 8954|   = 61 changed lines**; 58 was the nonblank count. Minimax's missing witness rows were a packet
 8955|   defect. The extra announce bracket and missing RGB/RGBA growth mutants were repaired in-round.
 8956| * Deepseek and the earlier PRETABLE assigned `M8_declineall` to `live silent`. The ledger's
 8957|   table red lists show `live/ci8/rgb/abgr` failing; `live silent` remains **0**, not **1**.
 8958| * The initial linear-offset explanation was wrong: linear x is a byte offset and y is ignored.
 8959|   `indep paint` cannot observe the LIN_B half after setup repaints it. Overlap concerns the next
 8960|   word's most significant byte and only a possible change, not a guaranteed failure.
 8961|   The later “xofs always zero” comment was also false: `ycrcb x4y1` has `xofs = 16`.
 8962| * Codex's records audit corrected fourteen sessions to nine, identified the demotions as
 8963|   PRIM_OP/BADMODE, and replaced a guessed timestamp/mtime warrant with the brief's verbatim copy.
 8964|   The ledger's final adjudication nevertheless repeats “fourteen pre-existing sessions”.
 8965| * The “colour selector cannot feed the store” warrant was withdrawn. Grok argued clause (e)
 8966|   from body-tested labels (all twelve nibbles share default); deepseek and the kimi substitute
 8967|   argued a floor breach. A later
 8968|   symmetry argument changed the loop's disposition. The **192-cell** scare was wrong; the
 8969|   one-row proposal and then eleven-row costing were superseded: **ten** other-nibble rows
 8970|   sufficed because **two** default nibbles were already driven. Proposed row totals were plans.
 8971| * “Six position-selector escapes” was wrong, and that brief listed only five: `M28` concerns
 8972|   the nibble, `M37` the foreground; at most four concern position. Printable “chin” was also
 8973|   not provenance proof. The later codex audit grounded the issue in uninitialised storage.
 8974| * “Complete” coverage omitted descriptor payloads and treated sampled coordinates/values as
 8975|   exhausted. The later codex review applied the body's actual partitions and rejected closure
 8976|   over arbitrary predicates. The controlling probe CONTRACT expressly supersedes those claims.
 8977|   The audit allegation that earlier latch mutants were omitted was itself rejected by the ledger:
 8978|   they were present in the regression tail.
 8979| * The witness was first labelled research, producing a phantom research panel; the ledger
 8980|   corrects it to review/measurement. Design evidence first went to the shadow scratchpad;
 8981|   the ledger records verbatim preservation under `panel_design_20260908/`.
 8982| 
 8983| **CLOSING INSTRUMENT.** The controlling `regress/sgi_re_colourdefault_probe.py` CONTRACT covers
 8984| `{TLB_A, TLB_B, TLB_C, LIN_A} × {1,2,4,8 bytes} × {BADCOLOR clear,set on entry}`: **32 cells**
 8985| that actually reach the PUT default through valid mappings. Entry state precedes the warning.
 8986| PRETABLE records **89 assertions / 29 sessions**: twelve additions occupy eleven missing cells
 8987| and add the M28-family observation; four existing depth-eight readbacks now inspect both words.
 8988| Accept controls prove the destination mapping, each decline is read before repainting, and
 8989| all transferred paint bytes differ from zero. Announcement counts alone cannot detect these
 8990| store-permission controls. The bounded improvement does not prove that equal bytes mean no write.
 8991| 
 8992| **MEASURED — closing table.** Every score below is from
 8993| `regress/artifacts/sgirandomcolour/killtable5_20260912/SCORES.txt`.
 8994| 
 8995| | Leg | Score | Recorded failures |
 8996| |---|---|---|
 8997| | BASE | **89/89** | none |
 8998| | HEAD | **28/89** | 61 rows |
 8999| | FIRST_*_ZERO (ten controls); REPEAT_L1_ZERO | **88/89 each** | each control's own row only |
 9000| | NIB_OTHER_ZERO | **78/89** | ten other-nibble rows plus `M28 nib60` |
 9001| | TAIL8_ZERO | **81/89** | all eight depth-eight rows |
 9002| 
 9003| The table records fresh builds, CLEAN baseline/restoration comparisons and cleared sentinel.
 9004| RESTORE has no recorded probe score. The separate earlier BASE **89/89** is reported by PRETABLE
 9005| at `regress/artifacts/sgirandomcolour/base_20260912/BASE.log`; it is not this table's BASE artifact.
 9006| 
 9007| **DERIVED / PREDICTED — closing pass.**
 9008| `regress/artifacts/sgirandomcolour/killtable5_20260912/codex_passE_20260912.txt` maps every cell:
 9009| **21 previously occupied + 11 added = 32; 0/32 unoccupied. Eleven isolated-cell kills MEASURED;
 9010| the other 21 isolated-cell kills PREDICTED.** NIB_OTHER_ZERO and TAIL8_ZERO are additional
 9011| measurements spanning multiple cells. An isolated TLB_B/4/set control is **PREDICTED 88/89**,
 9012| `tB ycrcb d4` alone, by that pass; it was not built in this table.
 9013| The pass contains source-derived readback predictions; SCORES contains no raw readback values.
 9014| HEAD's 28 green rows are acceptance, setup, attribution or warning controls, not credited
 9015| with detecting the historical colour-default defect.
 9016| 
 9017| **THE POST-TABLE L4s — corrections, not silent replacements.**
 9018| `regress/artifacts/sgirandomcolour/killtable5_20260912/PRETABLE.out` retains both wrong claims
 9019| and appends codex pass E's corrections:
 9020| 
 9021| * **GUARD/BODY:** “every control field is body-read or dominating” was false for `d->warned`.
 9022|   It controls the diagnostic; neither branch determines `ok`, and they merge before the store.
 9023|   The latch is an explicitly chosen axis for erroneous coupling, not a DEPENDS-ON consequence.
 9024| * **CLAIM → ROW:** attributing the entire projection to the additions and widening was incomplete.
 9025|   The twelve additions plus four widened observations cover **16 of 32 cells**; **the other 16**
 9026|   require unchanged rows. Pass E supplies the complete mapping. Sibling parity holds for the
 9027|   combined instrument, not the additions alone.
 9028| 
 9029| **DISAGREEMENTS AND UNPROVED RECORD CLAIMS.** The ledger reports M28/M28r escapes and later kills;
 9030| the controlling CONTRACT and pass E say the exact edit is absent. Family coverage is established
 9031| only to the extent above; historical-mutant identity remains unresolved. The ledger's glm design
 9032| entry says skip-write, while its design adjudication attributes zero-fill-and-store to glm.
 9033| Earlier entries place GET under `sgirebufuninit`; the later residual note calls its fatal unfiled.
 9034| Those attributions disagree. PRETABLE claimed "mtime proves order" -- which the row had withdrawn
 9035| once already -- and then its own post-table append REWROTE the mtime, destroying that basis.  The
 9036| surviving order evidence is the pre-append mtime 02:26:35 CDT observed before launch and SCORES.txt's
 9037| header 07:27:41Z (02:27:41 CDT); recorded as an L4 in PRETABLE.out.  Post-table notes now go in a
 9038| separate file.
 9039| 
 9040| **CLAUSE (e) / STILL OPEN.** Bare `ok = (<pred>)` mutants leave `buf` uninitialised; an identical-byte
 9041| write is invisible, and their kills require measurement. The exact historical M28/M28r remains
 9042| unproved. No exhaustive claim covers coordinates, tile indices, descriptor payloads, raw mode
 9043| bits, foreground values, other device/CPU/memory state or their interactions. Default nibbles
 9044| are driven but not crossed with the full projection; coordinate/width/label joins remain outside.
 9045| GET, accepted-type width semantics, invalid-input paths, per-instance/reset behaviour, cold/warm
 9046| memory paths and every warning property independently in each cell remain open.
 9047| The colour-first reverse-latch `SET_OTHER(j)` check is still owed in the ledger; later-added warn
 9048| bits are also outside the existing priming set. The historical regression tail has no recorded
 9049| completion result. The sibling addressing-mode blind spot remains
 9050| a reading, not a measurement. Fixed polling windows can yield loud false reds under load.
 9051| The ledger's unconditional-return and companion buffer-initialisation proposals have not landed;
 9052| the latter's hardware semantics and performance cost remain unmeasured. Its landing hold has
 9053| no recorded discharge. These limits survive the narrower deterministic-control coverage result.
 9054| 
 9055| **SEATS, by stage — ledger entries and later notes.**
 9056| 
 9057| * Research: codex filed the scope reading.
 9058| * Design pass 1: grok, glm, deepseek, kimi via `kimi-k3:cloud`, minimax answered.
 9059|   Codex, agy, opus5 and fable5 were deliberately not fired at that stage. Codex subsequently
 9060|   answered DESIGN2; fable5, the main loop as Fable 5.1, adjudicated the design.
 9061| * Witness: agy measured as fallback while both Anthropic transports were walled; codex's witness
 9062|   brief was refused. The intended Opus witness assignment is not an Opus witness result.
 9063| * Review pass 2: codex, grok, glm, deepseek, minimax and kimi via `kimi-k3:cloud` answered;
 9064|   kimi's CLI was walled, its substitute covered the seat. Opus5 measured after the reset.
 9065|   Codex also answered the PRETABLE records audit and allbits check. Agy was deliberately not fired
 9066|   for review, having measured the witness; fable5/Fable 5.1 adjudicated.
 9067| * Later pass 2 notes name grok, deepseek and the kimi substitute; the symmetry seat is not named.
 9068|   Opus 5 measured the subsequent expansion; codex answered the later class-closure review.
 9069|   Codex's closure-design brief was refused once, then answered when reworded; codex also answered
 9070|   closing pass E. Table 5 was built and run by the main loop in a scratch clone.
 9071| 
 9072| **GATE / COMMIT.** `regress/gate_arm.sh` now runs the probe in
 9073| a new section after `sgirandompixel`, pinning **89 rows**. This supersedes the ledger's “gate
 9074| wiring OWED; pin 77” note.
 9075| Gate result: gate 14 PASS (914 checks) with the new section green -- protocol parsed, liveness row, rows run 89, rows
 9076| correct 89, 0 FAIL; log preserved at
 9077| `regress/artifacts/sgirandomcolour/killtable5_20260912/gate_arm_89rows.log`.  The gated probe is
 9078| byte-identical to the frozen table-5 instrument (`cmp` in the gate driver). Commit: this block's own commit; its pass-2 receipt is keyed to that SHA in the commit after it, as the
 9079| tree's precedent requires.
 9080| 
```

## Questions -- verdict line first

1. Does the block contradict itself anywhere -- two different numbers for one quantity, a total that its own parts do not sum
   to, a claim in one paragraph that another paragraph undoes?  Quote both places, with their line numbers.
2. Which claims are stated as MEASURED but cite no artifact, or cite one only by a bare file name that could be ambiguous?
3. Which sentences overclaim -- 'every', 'all', 'never', 'exactly' -- where the block's own evidence covers less?
4. What would a reviewer checking this block against its artifacts most likely find wrong?
When you count items the block enumerates, list them by name before giving the count.

End with one line: `RECBLOCK_519: <c> CONTRADICTIONS, <u> UNCITED, <o> OVERCLAIMS`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBOLDREC519: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
