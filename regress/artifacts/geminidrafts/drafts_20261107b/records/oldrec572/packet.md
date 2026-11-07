# Reading task: oldrec572 (Gemini web; 2026-11-06)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBOLDREC572-85f9` on a line of its own.

# GXemul hardened fork -- RECORDS CHECK of one landed round's CHANGELOG block: #572 wdclbaaddr (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator and this fork records each
fix in a CHANGELOG round block.  The block below has landed; a flagship review of it is still owed.  You cannot read files, so
judge the block AS WRITTEN.  Do not simply ratify it.  A bracketed dated note inside the block is this project's in-place
correction form (it quotes the text it corrects); it is not by itself a contradiction.

## The round block (verbatim, CHANGELOG.md lines 1702-1874 at HEAD 116c5aa9)

```markdown
# `#572` (wdclbaaddr): the IDE model decoded the select byte's LBA flag from bit 5 and left the LBA28 address arms compiled out, so every LBA-mode request was served from the cylinder/head/sector reading of the same taskfile bytes -- bit 6 now selects LBA, both arms compute the LBA28 offset in 64-bit arithmetic, the select byte reads back byte-exact, and IDENTIFY word 49 stays 0

**The defect** (`wdclbaaddr`, HIGH; filed 2026-10-22 from the external-fixes research, T4 of its batch; class
GUEST-DATA, graded "latent" there because IDENTIFY word 49 advertises no LBA).  `src/devices/dev_wdc.c`'s SDH arm
(`case wd_sdh:`) decoded the select byte as `sectorsize` = bits 7-6, `lba` = bit 5, `drive` = bit 4, `head` = bits 3-0
and composed the readback the same way; ATA puts the LBA flag in bit 6 (`WDSD_LBA 0x40`, the fork's own
`src/include/thirdparty/wdcreg.h:195`) with bits 7 and 5 reserved, so the classic CHS select byte 0xa0 set `lba = 1` and
the LBA select byte 0xe0 was head 0 -- and it did not matter, because `d->lba` reached no address: the LBA28 formula sat
inside `#if 0` in both `wdc__read()` and `wdc__write()`, whose live offsets were pure CHS.  A guest issuing READ SECTORS
or WRITE SECTORS with the LBA bit set was served `512 * (sector - 1 + head * spt + heads * spt * cyl)` instead of
`512 * LBA`.  The rung-3 witness (`regress/artifacts/wdclbaaddr/witness_20261024/`, cold debugger on the UNMODIFIED
`evbmips -e malta`, whose committed piix4_ide path adds the wdc when a disk is attached; the committed-equivalent binary's
`dev_wdc.c` md5 `71407161` == HEAD `cc1f69cc`) measured it on 2026-10-24 17:03, BEFORE any edit, on a 4096-sector image
whose sector n carries the tag `(n, ~n)`: with the device's own IDENTIFY geometry 16/63, LBA 70 was served as tag 69 (CHS
sector 70), LBA 256 as tag 1007 (H*S - 1), LBA 0 as zeros (CHS "sector 0", a negative offset that `diskimage.c` zero-fills),
and a WRITE SECTORS at LBA 70 landed at index 69 -- `RESULTS_base.txt` 19/19 against the HEAD column, the five `lba *` rows
red against the FIX wants; the CHS rows (tags 0, 1 and 63), the byte-exact readback (0xe5, 0xb3), the RAM liveness row in
every session and 490/490 hand-encoded words against the emulator's disassembler green.

**What ships** (one product file, byte-identical in `GXEMUL-SEC/` and `est/`; six harness files).
* `src/devices/dev_wdc.c` -- five `#572` sites.  The SDH arm decodes `lba` from bit 6, `drive` from bit 4, `head` from
  bits 3-0, and keeps bits 7 and 5 in the field formerly named `sectorsize`, renamed `sdh_resv` (`idata & 0xa0`; its only
  readers were this arm and its two debug lines); the readback composes `sdh_resv | lba << 6 | drive << 4 | head`, so every
  one of the 256 select bytes reads back as written (the four parts are disjoint and cover the byte); the debug lines print
  the byte and the decoded fields.  `wdc__read()` and `wdc__write()` enable the LBA arm: `if (d->lba) offset = 512 *
  (int64_t)(((d->head & 0xf) << 24) + (cyl << 8) + d->sector);` -- the CHS line's own `(int64_t)` idiom, because the
  compiled-out form multiplied in `int` and overflows for ANY request with a nonzero head nibble (head 1 is LBA 2^24 + s;
  `512 * 16,777,221` wraps, in two's-complement arithmetic, to 2,560 = sector 5 -- an undefined operation that a build may
  lower that way or widen; the source now widens).  The two `printf`s inside the old blocks are DELETED, not converted:
  `debug()` prints whenever the verbosity is non-negative and single-stepping raises it, so the witness command line would
  have logged every media command.  The write arm stays above the three `write_*` assignments, so the drain writes at the
  LBA offset.  IDENTIFY word 49 stays 0 and its comment says why: LBA28 is honoured but NOT advertised in this round -- the
  advertisement switches every word-49-honouring guest from CHS to LBA and needs its own measured warrant (filed,
  `wdclbaadvertise`); words 60-61 already carry the capacity.  The SDH arm's label comment names the bits.  Nothing else
  moves: the CHS formula and its casts, the no-disk and `default:` ABRT arms (the 48-bit opcodes stay there), the `#481`
  control-register arm, `wdc_altstatus`, ATAPI, the `#484` ring cap, the drain, sector-count 0 = 256, every IDENTIFY word.
  Option set: member 7 IMPLEMENT (the path was compiled out; member 4 ACCEPT presumes a computed value, and the
  compiled-out value keyed off the wrong bit and overflowed); the `WDCE_ABRT` decline idiom the file already has
  (`:947-954`, `:1155`) was available and not chosen -- the measured defect is the wrong sector, and refusing LBA while word
  49 is 0 would leave a guest that ignores word 49 with no disk; member 1 DELETE (remove the dead text, keep CHS) was named
  as the honest minimal alternative and not chosen (`pass1_20261024/ADJ_PACKET.md` A5, both adjudicators).
* `regress/wdc_lba_probe.py` (new; 840 lines, 35,862 bytes, md5 `96e5fbc5817ab26e19edd4f5335a184f`; the FROZEN witness revision is
  637 lines, md5 `8f3632ffc1c982fd523c7fd28d86f15d`, preserved byte-identical as `witness_20261024/wdc_lba_probe.frozen.py`
  with its base run) -- the detector: the witness probe revised on pass 1 (L1, pre-ship construction).  Seven
  debugger-driven guest sessions on `-E evbmips -e malta` with the tagged image attached `-d iR:`, every instruction from the
  probe's own encoders and checked against the emulator's disassembler: IDENTIFY (words 3, 6 and 49), the CHS rows (sectors
  1 and 2, head 1, cylinder 1 -> index 1008), the select-byte readbacks (0xe5, 0xb3, 0x4c, 0x00 after 0xe5), the LBA reads
  (70, 256, 0, the bare 0x40 select, head 1 -> LBA 16,777,221 past the file with poisoned capture registers and a tagged
  companion read, cylinder-high 1 -> past the file), and one write session whose eight touched sectors are pairwise
  disjoint: LBA 70, LBA 256 (sector 0, cyl_lo 1), head-1 LBA (refused past the file), CHS sector 10, cylinder-high 1
  (refused) -- each read back through valid CHS triples at BOTH candidate destinations so a write that lands at the other
  reading's sector, or at a head-dropped or width-wrapped sector, is seen.  Every CHS readback uses a triple ATA defines
  (sector 1..S); the frozen witness read index 70/69 through sector numbers 71/70, which the model does not validate --
  the shipped rows use (head 1, sector 8) and (head 1, sector 7).  33 scored rows; the constant
  `neg appar` row of the witness is gone from the score (a `neg`-mode row whose pass is `got != want` on the constants 1
  and 0 -- it passes on every run that delivers them, so the witness's 19/19 counts one row that could not fail), replaced
  by a comparator self-check at startup; a `None` observation or want fails its row; the pty driver survives a dead child and still prints the result
  lines and the sentinel.  Modes: `<bin> - <outdir>` (the witness form), `<base> <fix> <outdir>` (two legs), `<bin> GATE
  <outdir>` (one leg against the FIX column, `WDC_LBA_RESULT=p/n`, `WDC_LBA_CONTROL=OK|FAIL`, sentinel `WDCLBA_PROBE_DONE`).
  Contract (the docstring): CATCHES the decode off bit 6 or qualified with bit 5 or 7; the LBA arm disabled, unconditional,
  or qualified on head, cylinder or sector at either site; the head term or `sector - 1` in the arm; a head shift that
  still lands inside the file; the `cyl_lo`-only cylinder term at either site; a readback losing a bit or forcing bits 7
  and 5; the write arm placed below the `write_offset` capture; word 49 nonzero.  MEASURED, NOT PROMISED: the unwidened
  32-bit product (undefined behaviour; its score on this build is recorded below and does not generalise).  BLIND: cylinder-
  high destinations (both readings past 4096 sectors; the cyl_hi-conditioned arm), head shifts that miss the file, drive 1,
  big-endian guests, MULTI counts, the 48-bit commands, the deleted printf text, out-of-range completion without an error
  bit, and the both-out-of-range subdomain where neither reading is in the file (the LBA 4096-5039 band is advertised
  capacity served as a short zero-filled read -- `#416`'s design -- while the CHS reading of the same bytes is refused;
  the guest sees zeros either way).  Anchor (measured, `SCORES2.txt` T_m1 / T_p1, 26/33 each): a -1 sector shift reds seven
  rows -- `lba 70`, `lba 256`, `sel 40`, `lba 0`, `lba wr`, `lba wr2`, `lba wr256`; a +1 shift reds seven -- the same without
  `lba wr2` and with `lba wr cylhi`; the write-site anchor is `lba wr` + `lba wr256`.  (The witness-era sentence "a -1 shift reds
  the five LBA rows; a +1 shift reds four" described the 19-row instrument and is replaced here, not repeated.)
* `regress/gate_sh_rounding.sh` (gate 10) -- a `#572` block beside the `wdc_altdigin_probe.py` block: the probe in `GATE`
  mode on `$PMAX` into `$LOGDIR`; the result line present, `CONTROL=OK`, the denominator pinned by EQUALITY to the literal
  33, the numerator equal to it, the sentinel once.  Run END TO END before landing, as committed (HEAD's script + this hunk, an LF copy md5 3f932e0f) with `PMAX` overridden to the fix clone (provenance measured, `pass2_20261024/CLONE_PROVENANCE.txt`: 496 of 505 tracked src files identical to HEAD plus this `dev_wdc.c`; the PowerPC decoder at its pre-#571 revision and the pmax layout's six declared divergence paths, none on the wdc path; the build trees were not used for the run and were propagated with the fix only before the landing, `CLEARANCE.out`): the block's five checks OK -- result parses, CONTROL=OK, 33 rows run, 33 correct, sentinel once (`pass2_20261024/GATE10_RUN.txt`, 2026-10-24 23:24 -> 2026-10-25 00:57; `gate10_wdc_lba.log`).  The gate's own verdict that run was FAIL 1 of 405 -- `gdrom_default rows run got=62 want=60`, the working tree's `gdrom_default_probe.py` carrying the peer session's uncommitted two extra rows against HEAD's pin; not this round's file.  The first attempt died in 2 s on a CRLF copy that `git apply` had written OUTSIDE the repo under the SYSTEM `core.autocrlf=true`; every committed gate script is LF (0 CR bytes), and the landing script now pins the conversion off and refuses a staged copy whose CR count differs from HEAD's.
* `regress/diff_wdc_identify.c` -- `row_no_lba_claim()` re-authored IN THE SAME CHANGE, as its own comment demanded: the
  assertion (both bytes of word 49 == 0), the row's name and its "ok" string (gate 2's pin) are unchanged; the comment no
  longer says the LBA arms are `#if 0` or that `d->lba` never reaches an offset, and the FAIL text says LBA is implemented by
  `#572` and deliberately not advertised while DMA is not implemented.  `regress/gate_offline.sh`'s comment beside that pin
  likewise.  Both files carry other sessions' uncommitted hunks; only these hunks are staged (HEAD-based copies, the `#548`
  recipe), located by comment text (the working-tree line numbers differ from HEAD's).
* `tools/pipeline/check_probe_wiring.py` -- MANIFEST lines: `wdc_lba_probe.py` CLASS_DETECTOR (gated in gate 10 in this
  commit); `artifacts/wdclbaaddr/witness_20261024/wdc_lba_probe.frozen.py` CLASS_WITNESS -- its mandatory base leg asserts
  the HEAD column, red once the defect is gone, which is the checker's own WITNESS line (both adjudicators; the `#533` pair);
  the kill-table instrument `artifacts/wdclbaaddr/detector_20261024/wdc_lba_probe.frozen.py` and the mutant applicator `mutants572.py` CLASS_TOOL.  `tools/precommit_check.sh`'s coverage pin raised 39 -> 40 with its dated line.

**Measured** (`regress/artifacts/wdclbaaddr/detector_20261024/`; every score against its instrument revision and log;
`PRETABLE.out` written before the first table ran).  The revised detector's two legs: base 33/33 against the HEAD column on the committed-equivalent binary, fix 33/33 against the FIX column on the fixed one (`final_96e5fbc5/RESULTS_twoleg.txt`, the shipped revision; the same at every earlier revision's `final_*/`).  The FROZEN witness instrument's fixed leg: 19/19, CONTROL=PASS (`witness_20261024/RESULTS_fix.txt`, a two-leg run dated 19:02:13) -- the "same script green afterwards" half of the `probe:` term.  GATE mode on the fix binary: 33/33, CONTROL=OK (`final_96e5fbc5/RESULTS_gate.txt`).  The dead run on `/bin/false`: 0/33, CONTROL=FAIL, sentinel present (clause (c): measured at `detector_20261024/dead_run.out`).  Kill table 1 (`SCORES.txt`, instrument fc878c42, GATE mode vs the FIX column): 18/18 KILLED -- V1 bit-5 decode reinstated 17/33, V2 bit-7 decode 17/33, V3 the bit-6-and-bit-5 conjunction 31/33, V4r/V4w head-conditioned arms 32/33 each, V5w cylinder-conditioned write arm 31/33, V6w sector-conditioned write arm 31/33, V8 head term dropped 32/33, V11 `sector - 1` in the arm 29/33, V13r/V13w unconditional arm 19/33 and 31/33, V14r/V14w one site reinstated 28/33 each (the applicator's suffix names the site DISABLED: V14w = the read arm disabled), V15 the unwidened product 32/33 on this gcc -O3 build (undefined in general; measured, not promised), V16 readback forcing bits 7 and 5 31/33, V17 the readback dropping bit 5 31/33, V18 readback losing bit 6 31/33, V20 the write arm below the write_offset capture 28/33.  Kill table 2 (`SCORES2.txt`, the contract claims at both sites): 9/9 KILLED -- V5r 32/33, V6r 31/33, V8w 32/33, V11w 30/33, V9r8 head shift by 8 32/33, V10r/V10w cylinder-low-only arms 32/33 each, the -1 and +1 sector translations 26/33 each.  Single builds: V12 (`& 0xf` dropped) 33/33 SURVIVED -- EQUIVALENT, one masked writer of `d->head`; V7 (the cylinder-high-conditioned arm) 33/33 SURVIVED -- the disclosed BLIND cell on this image (`SCORES_V12_V7.txt`); V17v, the VERBATIM pre-#572 readback composition over the new decode (clause (b) at the readback site, built after pass 2), 30/33 KILLED (`SCORES_V17v.txt`).  Escapes: none outside the two disclosed survivors.  Gate 2's offline differential rebuilt with this round's hunk against the fixed model: 128 rows, 0 failures (`offline_identify_hunk.out`).  Every MEASUREMENT ran on WSL scratch clones, never on a build tree (`/tmp/gxt2/base`, the pre-#571 HEAD lineage; `/tmp/gxt2/fix` = that clone + this `dev_wdc.c`, cmp CLEAN vs SEC with the binary newer than its source -- `pass2_20261024/CLONE_PROVENANCE.txt`; each mutant a `cp -a` clone under a `.MUTANT` sentinel, removed after a cmp-verified restore).  Before the landing the fix was PROPAGATED into `build/`, `build-asan/` and the WSL `/tmp/gxsec-build` tree, each rebuilt, with the two-part clearance recorded per tree in `detector_20261024/CLEARANCE.out` (est/ is a source tree: part 1 only).

**Panel.**  Pass 1 (`pass1_20261024/`): GPT-6 Astra (ultra, file-reading, pointer form), Grok 4.7 (xhigh, plan mode,
working tree), Gemini 4 Argon through agy (file-reading), GLM 5.3 and DeepSeek v4-pro (packet-fed, Q1-2 / Q3-4 each) on a
brief drafted by an Opus sub-agent from pointer inputs (35 drafter notes, `drafter_NOTES.md`): six READY WITH CHANGES and
DeepSeek's Q1-2 NOT READY on detector-spec points (all adopted).  The panel converged on the fix and corrected the brief
on four load-bearing points: the "five rigs would switch" rationale for keeping word 49 at 0 was FALSE (only the optional
landisk disk, all zeros, reaches this model; the decision is re-warranted by the addition licence), the head-nibble overflow
needs no large disk, the brief's head-1 write row as drafted could not separate the committed build from the head-conditioned
variant until it read back both candidate sectors, and the anchor claim overstated the +1 case.  Argon's Q1/Q2(a-c)/Q3(a,c-e)/Q4
were verified and credited; its Q2(d) P15, Q3(b) and Q1(c) trace described a `--expect` flag, a STANDALONE list in a checker
that lives elsewhere, a gate section, a gate-2 row and five source identifiers that do not exist (0 hits each at HEAD) --
the `#571` F25 pattern, not credited.  Adjudication (`ADJ_PACKET.md`, 22 dispositions, seven disputes): GPT-6 Astra CONFIRM
WITH CHANGES (no wrong disposition; Argon's trace credit withdrawn; the `probe:` term needs the frozen instrument's own fixed
leg) and Grok 4.7 CONFIRM WITH CHANGES (one disposition corrected -- with the cylinder-high read row in the contract the
read-site cell is rowed and a write twin at sector 71 was added; the gate-2 edits go by comment text; the 4096-5039 band is
`#416`'s design).  Disputes settled by both: the readback field renamed rather than a field added (D1); two local arms, no
helper (D2); `neg appar` out of the score (D3); the width variant measured, not promised (D4); clause (c) by measurement
(D5); the frozen copy CLASS_WITNESS (D6); the completion-status defect filed, not folded (D7).  Pass 2 (`pass2_20261024/`): the same five seats on the real diff, the revised detector and the four hunks -- seven answers, six LAND WITH CHANGES and DeepSeek's Q3-4 READY TO LAND; NO product-code defect.  Fourteen consolidated findings (`PASS2_RULINGS.md` K1-K14), every owed change a record, a contract sentence or one unmeasured floor leg, all applied before landing: the pre-table's per-row kill predictions were wrong at several rows and are corrected in a dated section of `PRETABLE.out` (the block itself kept verbatim); the clause-(b) mutant at the readback site was built verbatim and KILLED (V17v 30/33); further single-edit variants no row sees (the head mask narrowed, a sector-count qualification, a joint cylinder/sector cell) are DISCLOSED under clause (e) -- the arm tests none of those fields, so their body-induced partition is empty and the cells are coverage debt above the floor (a row on this image could see the narrowed mask, as Astra's F2 corrected; `wdclbaimage` carries only the cylinder-high cells); the wiring MANIFEST text and the detector's 'every want is a literal' sentence corrected; the gate-10 block, which the seats noted had never run INSIDE `gate_sh_rounding.sh`, was run end to end as it is committed here -- the five wdc_lba checks OK, 33/33 CONTROL=OK, sentinel once; the gate's own verdict FAIL 1 of 405 on the peer session's uncommitted 62-row gdrom_default probe against HEAD's 60-row pin, not this round's file; PMAX = the fix clone, provenance measured in CLONE_PROVENANCE.txt; GATE10_RUN.txt.  Two disputes: D1 (row or disclose the head-nibble cell) ruled DISCLOSE, GLM's reasoning adopted; D2 (are the pre-table's wrong predictions a defect of the shipped detector) ruled L4 in place, Astra and Grok agreeing.  F2 adjudication (`F2_PACKET.md`, Astra and Grok on the fourteen dispositions and the two disputes): Astra CONFIRM WITH CHANGES (wrong dispositions: K3, K4, K8); Grok CONFIRM WITH CHANGES (wrong dispositions: K1, K8, K11).  Every correction both adjudicators named was applied before the landing and is listed in PASS2_RULINGS.md's F2 section.  A first F2 firing at 21:50-22:00 (on the packet before the gate-10 result) had also returned CONFIRM WITH CHANGES from both seats; its answer files were overwritten by the 00:58 re-fire -- an apparatus error of the main loop, recorded rather than hidden.  The shipped detector is revision 96e5fbc5, docstring-only over the pass-2 bytes (`final_96e5fbc5/ast_equivalence.txt`), re-measured: GATE 33/33 CONTROL=OK, two-leg base 33/33 vs HEAD / fix 33/33 vs FIX.  A landing-tool defect found on the way and fixed before use: `git apply` run in a temp directory OUTSIDE the repo honours the SYSTEM `core.autocrlf=true` and wrote a CRLF copy of an LF gate script (bash under WSL died on it in 2 s); the landing script now pins `-c core.autocrlf=false` and refuses any staged copy whose CR count differs from HEAD's blob -- every committed gate script is LF (0 CR bytes, counted with `tr -cd`).
Fable 5.1 HELD on every stage by owner ruling (its question on the row); kimi, minimax and the Opus review seat NOT FIRED by
the owner's roster (recorded by name in each stage).

**What the records claim, and do not.**  Claimed: the witness and its order (base leg red against the FIX wants on the
committed `dev_wdc.c` before the edit; the same frozen script green on the fixed build afterwards); the decode moved to bit 6
with the readback byte-exact; both arms enabled with the product widened; the printfs gone; LBA28 honoured for READ, READ
MULTIPLE, WRITE and WRITE MULTIPLE (0x20, 0xc4, 0x30, 0xc5) only; word 49 unchanged and why; the 48-bit commands still ABRT
in `default:`.  NOT claimed: that any guest now uses LBA (NetBSD and the in-tree OpenBSD stay on CHS while bit 9 is clear;
"FreeBSD 10+" rests on a 2013 ports commit message, unverified here; "Linux" has no support in the record); ATA-2
conformance (the interim -- honoured, not advertised -- violates the bit-9 indication the way the previous state violated
the words-60-61 rule); that every changed address changes the served bytes; coverage of the cylinder-high-conditioned arm or
of head shifts that miss the file.  Two sentences elsewhere become false and are re-worded here rather than repeated:
`CHANGELOG.md`'s `#405` block says `d->lba` "never reaches an offset computation" (true until this round); the
`&& !d->lba` mutant described under `wdcaltfixture` (`OUTSTANDING_BUGS.md`, `CHANGELOG.md`'s `#481` records) "defeats the
abort on every LBA-mode driver" -- true only after this round, since before it `d->lba` was 1 on every 0xa0 select as well;
no recorded score is re-interpreted.  The research adjudication (`research_20261022/adj_20261022/ADJ_RULINGS.md` B) called a
source reading "the measurement"; it was a reading, and this round's witness is the measurement -- the dated artifact is not
rewritten.  `dev_wdc.c:1081-1082` (`#485`) and `regress/gate_offline.sh`'s self-consistency comment say no ATA document is
in the tree while `:640` (`#525`) cites `_scratchpad/ata2_x3t10_948d.txt` (on disk since 2026-09-10, outside the git tree):
not this round's edit, noted for the next round that touches them.

**Filed** (ledger rows): `wdclbaadvertise` (MED -- advertise LBA in word 49; gate: a word-49-honouring guest on a
content-bearing image with a checked sector, truthful capacity words, DMA bit clear; `wdccylwrap` revisited then);
`wdcmediastatus` (LOW -- `diskimage_access()`'s failure return is discarded at the read site and in the write drain and the
command completes with no error bit, CHS and LBA alike, pre-existing; the 4096-5039 short-read band is not a specimen);
`wdclbaimage` (LOW -- the detector's medium cannot observe cylinder-high destinations or sector 65,536; a larger image with
a wider tag is owed if that cell is rowed).  The word-53 candidate the brief raised was REJECTED by both adjudicators on the
ATA-2 draft (bit 0 clear means words 54-58 MAY be valid); Astra's note that words 54-56 are zero while 57-58 are populated
is recorded, not filed.

**Records.**  The ledger row's witness is `probe:regress/wdc_lba_probe.py -- rung 3, unmodified evbmips -e malta,
regress/artifacts/wdclbaaddr/witness_20261024/`; state `held` (the Fable 5.1 review is owed under the owner's hold; its
question is on the row); commits named by the follow-up records commit, as every landing in this batch.  Pass-2 receipt:
`regress/pass2_ledger.tsv`, added by the follow-up records commit.  Classifier note for the record: this round's probe,
brief, rulings and build spec were all written in-session without a stop -- a decode row; the day's two host-stop rows
(N5, T11) remain held for the owner.

# Records, 2026-10-24: `ppcdsformxo` names its landing commit cb21331c, and cb21331c's committed-tree proofs and pass-2 receipt

`#571` landed as `cb21331c561253dc2e86d3c79a0ff6d214b5cbd4`.  Committed-tree proofs: `git ls-tree cb21331c regress/ppc_dsform_probe.py` -> `100644 blob 3c845404bbb039ea810007b48cd57945ef6a5e97` (the
detector, mode 100644 -- a `.py` probe run by `gate_ppc.sh`; its committed blob md5 is `e0a1e67eb0283abccde3bbd53952487a`, the shipped revision 3 --
the measured revision `0266228894811ba6c51cff82585753c9`, revision 1 `59e83491a5819a599c610b1aa8e8b847` and revision 2
`3efd8cbec746b8224c32d6827b42db46` are preserved under `regress/artifacts/ppcdsformxo/table1_20261024/repair_p2/` with the
three docstring-only diffs and their re-measures);
the committed `regress/gate_ppc.sh` blob md5 is `5761a84d014a422f8e9381eba9412511` and the committed `tools/pipeline/check_probe_wiring.py` blob md5 is
`3cedc47eb34321dcc99e13184629efae`, each equal to the round's staged copy (`regress/artifacts/ppcdsformxo/table1_20261024/staged/gate_ppc.sh.txt`,
`staged/check_probe_wiring.py.txt` -- the HEAD-based copies carrying only this round's edits; the working tree's peer lines
were not committed); `git diff --numstat cb21331c^ cb21331c` on those two files = `41 1 regress/gate_ppc.sh; 2 0 tools/pipeline/check_probe_wiring.py`.  Pass-2 receipt: `pass2_20261024/`
(Astra, Grok, Argon via agy, GLM 5.3 x2, DeepSeek x2 -- seven LAND WITH CHANGES, records only; `PASS2_RULINGS.md`;
`adj/codex_t2p2adj.txt` AMEND and `adj/grok_t2p2adj.txt` AMEND, both LANDING GO WITH THE CHANGES NAMED, all applied before
the landing; `adj/final/codex_t2final*.txt`, Astra's exact-text readings of the landed records -- each reading's corrections were applied
before the next, and the last cleared the commit).  The row's `commits` field
now names `cb21331c`; its state stays `held` for Fable 5.1 with its question.

Ledger (one field), this block, the `regress/pass2_ledger.tsv` receipt line and `matrix.html` only.

**Follow-up correction, 2026-10-25 (gate 6 -- L4, a wrong record in the harness).**  The landing commit `0901b388` added
`regress/wdc_lba_probe.py`, a pty-forking probe with no prompt predicate (it drains on timeouts and watches for the breakpoint
banner), and moved neither `regress/gate_hygiene.sh`'s `EXPECT_PTY_PROBES` pin (77) nor its `GRANDFATHERED_PROMPTLESS` list --
so gate 6 was RED at HEAD from `0901b388` on, latent because no battery ran in between (the weekly battery is due 2026-10-25
18:00).  Found by running `tools/derive_hygiene_pins.sh` read-only while drafting the next round's brief: `EXPECT_PTY_PROBES got
78 pinned 77`, `promptless vs GRANDFATHERED 46 45`, `NEW PROMPTLESS: wdc_lba_probe.py`.  Corrected with the tool itself --
`--grandfather wdc_lba_probe.py`, then `--write --ruling "2026-10-25: #572 follow-up ..."` -- and re-derived afterwards: every
census reads got == pinned (pty probes 78/78, promptless 46/46, converted 26/26 on all three counts, whole-full 3/3).  The
gate's own comments record this class (a probe landing in the same commit as its wiring with the pin unmoved) and prescribe the
remedy; the tool was simply not run at landing.  The next landing's checklist runs it before the commit.

```

## Questions -- verdict line first

1. Does the block contradict itself anywhere -- two different numbers for one quantity, a total that its own parts do not sum
   to, a claim in one paragraph that another paragraph undoes?  Quote both places, with their line numbers.
2. Which claims are stated as MEASURED but cite no artifact, or cite one only by a bare file name that could be ambiguous?
3. Which sentences overclaim -- 'every', 'all', 'never', 'exactly' -- where the block's own evidence covers less?
4. What would a reviewer checking this block against its artifacts most likely find wrong?
When you count items the block enumerates, list them by name before giving the count.

End with one line: `RECBLOCK_572: <c> CONTRADICTIONS, <u> UNCITED, <o> OVERCLAIMS`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBOLDREC572: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
