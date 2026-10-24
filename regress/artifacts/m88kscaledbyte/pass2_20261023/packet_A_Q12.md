# PASS-2 DIFF REVIEW -- round `#569`, ledger row `m88kscaledbyte` (GXemul hardened fork)
**Brief v1, COMPACT form -- for seats that cannot read files: self-contained.**  Drafted 2026-10-23 ~10:50 -0500.
Tree under review: the `GXEMUL-SEC/` WORKING TREE over HEAD `5986c137` -- the round is IN FLIGHT and UNCOMMITTED
(S0).  Built from `GXEMUL-SEC/tools/BRIEF_TEMPLATE.md` (working tree).  The file-reading form, with the whole-file
inlines, is `brief2_FULL.md`; the QUESTIONS (section 11) and the premises-as-questions (section 6) are identical.


> **THIS PACKET (packet-fed seat): Q1 AND Q2 ONLY (the fix diff; the detector as shipped); Q3-Q5 travel in packet B**  Sections not carried here are omitted by number; nothing omitted is needed for the questions carried.

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated
wrongly.  **Check the premises, not just the derivations.**  Where I state something as
fact, ask whether it is true.  A seat that re-derives a premise from something this brief
did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.**  There are THREE pristine-2021-upstream
copies of GXemul under the project root (`./src/` and two under
`_archive/audit-results-*/builds/`).  They are NOT this fork.  If your line numbers
disagree with mine by hundreds you are reading one of them — say so rather than
reconciling.

**If you cannot read files that is expected** — every fact you need is inlined.  Name any
premise you cannot settle from this packet rather than guessing at it.

**Where this brief states an ARITHMETIC claim — an index range, an offset, a count of
reachable addresses — ENUMERATE it rather than reasoning about it.**  Walk the values.
A derivation that skips one masking line reads exactly like a correct one.

**And ENUMERATE THE RIGHT DOMAIN — a domain is itself a premise.**  Ask what the PRODUCER of
these values can actually emit before you walk them.  Walking every member of a set you have
not audited is not enumeration; it is a derivation with more steps, and it reads exactly like
a correct one.

**VERDICT LINE FIRST**, so your answer survives truncation.

---

## 0. What this is, what this pass is for, and how to answer

**The project.**  GXemul is a computer-architecture emulator: a developer tool that runs legacy operating systems
inside a software sandbox.  This fork is a hardening effort -- ordinary software-correctness work on the emulator's own
C code: out-of-bounds accesses, missing checks, crash-on-unusual-input defects, and the regression tests that keep them
fixed.  The *guest* is a program or OS running INSIDE the emulator; the *host* is the emulator process on the developer's
own machine.  A *variant* or *leg* below is a deliberately altered copy of the code, used to measure whether the
regression test notices the alteration (standard mutation testing); a row that notices it goes *red* under that leg.

**This pass.**  PASS 2: a review of the ACTUAL DIFF and of the MEASUREMENTS, before anything is committed.  The fix and
its regression detector were designed on pass 1 and that design was adjudicated (section 3).  The builder implemented
both, measured a 16-run table against the detector, propagated the two source files to the four fork trees, and ran
GATE 2 and GATE 11 once each, alone (section 9).  Review effort is scoped to THIS diff; the settled design is not
re-argued unless you find one of its premises false -- then say so loudly (R21, section 10).

**Hard limits.**  READ-ONLY.  Do not build, run, copy or modify anything in the repository; do not run the generator,
the driver or any gate.  No seat is asked to design or run a guest-path reproduction (section 2 says why).

**This is the PACKET form: you are not expected to read any file.**  Every fact a question depends on -- the four
diffs line for line, the decisive measurement lines, the rulings, the rules -- is inlined below.  Where a question needs
a fact this packet does not show, answer NOT CHECKABLE and name the fact; do not guess it.

**The working tree is NOT the round alone (section 4).**  21 tracked files differ from HEAD.  THIS ROUND'S: the
generator, the table, and ONE hunk of `regress/gate_offline.sh`, plus the new untracked `regress/diff_m88k_loadstore_gen.sh`
and the untracked `regress/artifacts/m88kscaledbyte/`.  The other 18, other sessions' in-flight work NOT under review:
regress/ `diff_wdc_identify.c` `gate_sh_rounding.sh` `gdrom_default_probe.py` `sh4_chcr_probe.py` `wdc_addtoinbuf_probe.py`;
src/ `cpus/cpu_alpha_palcode.c` `devices/dev_lca.c` `devices/dev_pcc2.c` `devices/dev_sh4.c`
`include/thirdparty/mvme_pcctworeg.h`; tools/ `BRIEF_TEMPLATE.md` `CLAUDE.md` `PIPELINE.md` `adjudicate.sh` `panel.sh`
`pipeline/check_probe_wiring.py` `pipeline/ledger.json` (other rows only) `pipeline/matrix.html`.  `regress/gate_offline.sh`
also carries THREE foreign hunks (HEAD lines ~1738, ~1832, ~2273: +58 -3); the file to commit is the staged copy
`table1_20261022/staged/gate_offline.sh` = HEAD + this round's one hunk (7.3).  Every other cited source file == HEAD.

**Answer format -- VERDICT LINE FIRST:**
~~~~
VERDICT: <SHIP | SHIP WITH CHANGES | DO NOT SHIP> -- <one sentence>
Q1: <one line>   Q2: <one line>   Q3: <one line>   Q4: <one line>   Q5: <one line>
~~~~
Then one section per question.  Mark EVERY claim READ (you opened the file or artifact), REASONED (from this packet
alone) or NOT CHECKABLE.  A change you ask for names its file and its grep anchor, and says which licence it is under:
L1 pre-ship construction, L2 floor breach, L3 undischarged obligation, L4 wrong record -- or FILE (section 10, R16).

---

## 1. The defect and the fix -- as the records describe them (VERBATIM)

Ledger row `m88kscaledbyte`, `title` (HEAD == working tree; the row is unchanged so far -- state `open`, witness `none`,
commits empty, NO `entries` field):
~~~~
cpus/generate_m88k_loadstore.c table + cpu_m88k_instr.c:X(xmem_slow) -- the generator emits NULL for every scaled byte-size entry; scaled `xmem.bu rD,rS1[rS2]` calls that NULL pointer (host SIGSEGV), scaled `ld.b/ld.bu/st.b` decode to `ic->f == NULL` (CPU stop) -- HOST-STOP
~~~~

The queue, `OUTSTANDING_BUGS.md` (HEAD == working tree), lines 28-29 and 25260-25263:
~~~~
   28| > 1. `m88kscaledbyte` (HIGH, new) -- m88k scaled byte ld/st/xmem use NULL table slots; a user-mode xmem calls a NULL
   29| >    function in the host.  T1; the fix shape is disputed and pass 1 settles it.
  ...
25260| * **`m88kscaledbyte` (HIGH, open)** -- new.  cpus/generate_m88k_loadstore.c table + cpu_m88k_instr.c:X(xmem_slow) -- the
25261|   generator emits NULL for every scaled byte-size entry; scaled `xmem.bu rD,rS1[rS2]` calls that NULL pointer (host
25262|   SIGSEGV), scaled `ld.b/ld.bu/st.b` decode to `ic->f == NULL` (CPU stop) -- HOST-STOP.  TRIAGE.md T1; report rows
25263|   A7-29, A7-30, A(c)#1; port: yes (ajfa mvme187 4a01173).  Batch 1 of 10 (fix shape disputed; pass 1 settles it).
~~~~

The committed critical-items ruling (`CRIT_RULINGS.md` line 13, committed in `cb2eba1e`) rules the same repair that
A1-A3 below record.  **Evidence level:** the defect is established by READING the source (S3, 8.2) and by the offline
detector's pre-fix red (9.6); it has NOT been measured on a guest path (section 2).  The queue lines and the ledger row
still say "fix shape disputed" / "witness: none" -- the landing owes their correction (Q5).

---

## 2. The witness disposition -- rung-3 attempt BLOCKED; detector-only by owner ruling (VERBATIM)

`regress/artifacts/m88kscaledbyte/witness_attempt_20261022/WITNESS_ATTEMPT.md`, its title and its last two paragraphs (lines 1, 18-23).  **It is UNTRACKED at
HEAD** (section 4, part 3), and the new driver's header cites it.
~~~~
  1| # m88kscaledbyte -- the rung-3 witness ATTEMPT, 2026-10-22: BLOCKED (recorded so `none` never means "did not think to")
  ...
 18| **Owner ruling (2026-10-22, by question):** "Detector-only, attempt recorded" -- ship the agreed fix with an offline
 19| regression detector under the ledger's `detector:` witness term, record this attempt as BLOCKED, and leave a guest-path
 20| witness to the owner (or a session they drive) by another route if one is wanted.  The probe shape for that later run
 21| is the one the two seat answers specify; nothing here restates it.
 22| 
 23| **Status:** rung-3 attempt BLOCKED (classifier), not "not tried".  Witness term for the round: `detector:<path>`.
~~~~
*Lines 7-16, condensed: a measuring seat was briefed to make a cold-debugger probe on the unmodified in-tree `testm88k` machine with the ladder's liveness and device-signature controls; the coordinator's response was stopped by the harness safety classifier while the brief was being written; the agent was killed at once and had written nothing; per the standing rule the brief was not re-issued.*
**So, for this pass:** do NOT design, sketch or run a guest-path reproduction.  The round ships under the ledger's
`detector:<path>` witness term (R18) with an OFFLINE regression detector; the guest-path channels (the exchanged byte,
neighbour preservation, zero extension) are listed in the driver's own NOT-OBSERVED paragraph (section 7.4, lines 66-74).

---

## 3. The settled design and its adjudication (VERBATIM where marked)

Pass 1's rulings (`pass1_20261022/PASS1_RULINGS.md`), then GPT-6 Astra's ADJUDICATION of them (verdict AMEND, the repair
UPHELD), whose section E SUPERSEDES the rows it names.  The Fable stage is HELD by the owner (`fable5.HELD.txt`), so
every ruling is provisional on its face.

### 3.1 `PASS1_RULINGS.md` -- section A's ruling cells (VERBATIM; the seat-citation columns omitted), the five section-B
### 3.2 GPT-6 Astra, `pass1_20261022/adj/codex_t1p1adj.txt` -- the verdict line and the whole Q3 section (VERBATIM)
~~~~
  1| VERDICT: AMEND -- On the evidence of four reviewing seats (Astra-as-reviewer, Grok, GLM and DeepSeek), uphold the repair but correct the floor classification, acceptance rationale, variant specification and ancillary findings.
  ...
 52| Q3. Changes to **BUILD_SPEC.md**, by section:
 53| 
 54| - **§2:** make `PRETABLE.out` distinguish the 24 generator-output cells from the 16 current guest-consumer cells; use R12 for the halfword acceptance warrant.
 55| - **§3:** correct the contract header’s floor split; explicitly check generator execution success; implement B10’s independently specified row identities, each occurring exactly once. A total and sentinel alone do not establish those identities (`BUILD_SPEC.md:66-76`). State the limited definition-count coverage.
 56| - **§3, with corresponding score denominators in §6:** enumerate the actual row total. The current lists contain **54 distinct name pins per artifact**, or 57 checks if the three overlapping accept/counterpart indices are emitted twice, before structural and status checks. That is 24 repairs + 24 counterparts + six additional accepts (`BUILD_SPEC.md:60-64`).
 57| - **§6:** resolve L5 to `grok_t1p1.txt:76`; correct L7’s characterization without removing its halfword pins. The frozen specification ends at L7, despite the adjudication packet saying an extra L8 was requested. Add that promised all-NULL table leg as supplementary evidence, with its receipt, rather than treating it as a prerequisite for B6.
 58| - **§7:** qualify regeneration as dependency-driven; preserve explicit propagation and byte comparisons (`BUILD_SPEC.md:111`).
 59| - **§9:** report the corrected classifications, actual receipts and C1/C2 dispositions.
 60| 
 61| **§5’s repair does not change.** The baseline agreement prerequisite in §2 and the pre-fix red requirement in §4 remain.
~~~~

### 3.3 `pass1_20261022/BUILD_SPEC.md` section 10 -- the builder's copy of those amendments (VERBATIM)
~~~~
120| ## 10. AMENDMENTS from GPT-6 Astra's adjudication of pass 1 (2026-10-23 ~09:55, `adj/codex_t1p1adj.txt` Q3) -- these
121| ## override the sections they name; §5 (the repair) is unchanged.  Sent to the builder by message at ~10:00.
122| * §2: `PRETABLE.out` distinguishes the 24 generator-output cells (the FLOOR) from the 16 current guest-consumer cells;
123|   the halfword acceptance's warrant is R12 (adjacent modelled size), not D2.
124| * §3: the contract header states the floor as ALL 24 cells (16 = the current consumer subset; the 8 others are NOT
125|   coverage debt); an explicit RED row for unsuccessful generator EXECUTION (non-zero exit / empty stdout) beside the
126|   compile and missing-table rows; every row carries an identity string that occurs exactly once and the gate block pins
127|   each identity's presence (`== 1`) as well as the total and the sentinel; the row total is ENUMERATED in the driver
128|   header and in `SCORES.txt` (54 distinct name pins per artifact = 24 + 24 + 6, or 57 if the three overlapping accept /
129|   counterpart indices are emitted twice -- say which); the `#define LS_N == 198` and `generated_functions == 198` rows
130|   are described as a narrow suppression-count control, NOT a definition-integrity check (which is disclosed as outside
131|   the contract).
132| * §6: L5 is Grok's v2 at `grok_t1p1.txt:76` only (first difference 416; the `codex_t1p1.txt:100` variant first differs
133|   at 256 overall and is NOT L5); L7 keeps the halfword pins but is recorded as also producing duplicate definition NAMES
134|   that the driver does not compile -- the table token at 161 is its observable, not "silence"; L8 (all-NULL table) is
135|   SUPPLEMENTARY evidence with its own receipt, not a prerequisite of clause (c).
136| * §7: regeneration is dependency-driven -- after each rebuild `cmp` the tree's table against GXEMUL-SEC's and record
137|   whether the tree regenerated or kept the copied file.
138| * §9: the report carries the corrected classifications, every receipt by file, the actual row count, and C1/C2 as
139|   "filed outside T1" only.
~~~~

---

## 5. SETTLED PREMISES -- re-inlined so nobody spends an answer re-deriving them

Copied forward from the pass-1 brief, pruned, and appended with what pass 1 and the build settled; each RE-READ IN THIS
SCOPE (the working tree over HEAD `5986c137`) by the drafter.  `cpu_m88k_instr.c`, `cpu_m88k_instr_loadstore.c`,
`cpu_dyntrans.c`, `Makefile.skel`, `regress/lib.sh`, `regress/run.sh` are byte-identical to HEAD; in the generator every
line before 254 is unchanged and every line after it moved by +4.

* **S0 -- section C0: the round is IN FLIGHT, not shipped** (section 4; this brief's `C0_OUTPUT.txt`): no CHANGELOG hit
  for `m88kscaledbyte` or `#569` at HEAD or in the working tree (HEAD's newest round block is `#568`); both src files last
  committed at the upstream import `39748e3c`; the driver and the whole `regress/artifacts/m88kscaledbyte/` are
  UNTRACKED; the ledger row is unchanged (state `open`, witness `none`, commits empty, no `entries`); HEAD's
  `regress/gate_offline.sh`, generator and table are all mode 100644; `core.fileMode=false`, `core.autocrlf=false`.
* **S1 -- the generation early return is KEPT:** `loadstore()` still returns on `if (size == 0 && scaledness)` (generator
  :104-105, untouched), so no scaled-byte handler and no size-0 `_scaled` name is generated (A2).
* **S2 -- the deleted arm and its siblings:** HEAD's table printer had four `NULL` arms -- `store && signedness`
  (:239-242), `!registeroffset && usr` (:244-247), `!registeroffset && scaledness` (:249-252), all unchanged -- and
  `size == 0 && scaledness` (HEAD :254-257), deleted whole.  MEASURED: 296 `NULL` of 512 at HEAD (BASELINE.out), split
  128 + 96 + 48 + 24 by arm (pass-1 census; PRETABLE.out section 1); 272 after the fix (FIX.out; S18a).
* **S3 -- the consumers (unchanged; 8.2):** `X(xmem_slow)` indexes the table for its load (:2377-2382) and store
  (:2411-2417) halves, ALWAYS adding NO_PC_SYNC and NEVER SIGNEDNESS, `scaled` from `iword & 0x200` (:2357), `user` from
  `iword & 0x80` (:2359), and calls both with no NULL test (:2395, :2426).  The register-form `ld`/`st` decoder installs
  the slot as `ic->f` (:3622-3629: adds SCALEDNESS and USR, never NO_PC_SYNC); a NULL `ic->f` hits `fatal("INTERNAL
  ERROR: ic->f == NULL!\n"); goto bad;` (cpu_dyntrans.c:1906-1908), which stops the CPU.  The immediate form (:3087-3091)
  never adds SCALEDNESS, USR or REGISTEROFFSET.  These four sites are the only ones (CHECKS #3).
* **S4 -- consumers of the 24 today (A6; B8 as amended by E):** 16 -- 160 164 168 176 180 184 224 228 232 240 244 248 (the
  decoder, both endians, plain and `.usr`) and 416 420 432 436 (`xmem_slow`, `ld.bu`/`st.b`, both endians).  480 484 496
  500 gain `xmem_slow` only if `m88kxmemusr` is fixed (the decoder sends bit `0x80` to `fatal("wt bit not yet
  implemented! TODO\n"); goto bad;`, :3606-3614, before `xmem_slow`; the immediate form forces `user = 0`, :2372).  424
  440 488 504: none (`xmem_slow` never adds SIGNEDNESS).  The little-endian half IS reachable (A6).  **ALL 24 ARE THE
  FLOOR** (E/B8); 16 is the guest-consumer SUBSET.
* **S5 -- the alias is the architecture:** MC88100 manual (`mc88100.txt:2961-2965`, OCR): "When the source 2 operand is
  scaled, it is shifted by 0, 1, 2, or 3 bits (multiplied by scale factor 1, 2, 4, or 8) for byte, half-word, word, or
  double-word accesses, respectively. For byte accesses, the 5UBOPCODE [SUBOPCODE] field is distinctly different from
  the register indirect with index (unscaled) cases but the result is identical."  The handlers compute
  `reg(ic->arg[1]) + LS_SIZE * reg(ic->arg[2])` under `LS_SCALED` (cpu_m88k_instr_loadstore.c:65-70), LS_SIZE 1 for a
  byte.  `print_function_name()` appends `_scaled` only `if (scaledness && size > 0)` (:80-81) and prints `_le` for every
  byte entry (:74-75), so each repaired slot prints its index-32 counterpart's existing name (12 distinct names) -- the
  idiom the table already uses for big-endian byte slots (`loadstore()` :101-102 generates no big-endian byte function).
* **S6 -- two fixed sites, both live:** the table is TRACKED, and `Makefile.skel:134-135` regenerates it only when the
  template or the generator binary is newer, so a build compiles EITHER the committed copy OR fresh output (A5; B1).
* **S7 -- the decoder is not edited** (A3).  **S8 -- the witness:** rung-3 attempt BLOCKED; witness term
  `detector:<path>` (section 2; R18).
* **S9-S15 -- the detector as ruled, inlined VERBATIM in 3.1:** shape B1/B2/B10 (the REAL generator run in a scratch
  copy, the COMMITTED table read separately, ABSOLUTE name pins hard-coded in the driver, a `cmp`; `slot[i] == slot[i-32]`
  is NOT a pin); clause (c) B6 (comment-only generator and table, "measured at"); clause (d) B7 + E (re-introduction under
  a different predicate; L5 = `grok_t1p1.txt:76` only, first difference 416; L5b supplementary; L6 = the little-endian
  half); accept B3/B9 + E (161/177 under R12, not rule D2; v6 not silent); counts B4 + E (272 supplementary; 198/198 a
  narrow suppression-count control, not definition integrity); B5 + E (explicit red for compile, exit, stdout and missing
  inputs, never `need_file`, which calls `gate_skip`); B12 + E (54 distinct pins per artifact = 24 + 24 + 6, with 144 400
  404 emitted once as accepts; 4 + 2 x (5 + 54) + 1 = **123** rows).
* **S16 -- C1 and C2 are FILED outside T1 in T1's landing** as `m88kxmemaddrovl` (MED; wrong-address access with possible
  secondary fault behaviour; unmeasured) and `m88klepsrbo` (CPU-STOP / MED; source-established; unmeasured).  Neither
  row exists yet in the ledger or OUTSTANDING_BUGS.md.
* **S17 -- propagation:** `tools/precommit_check.sh` section A compares only `src/` paths with `est/`; neither src file is
  in the derived divergence set; `est/` has no `regress/`.
* **S18 -- the drafter's own derivations (CHECK THEM; computed from the files):** (a) in HEAD's and the working tree's
  512-entry initializer exactly 24 entries differ, at 160 164 168 176 180 184 224 228 232 240 244 248 416 420 424 432
  436 440 480 484 488 496 500 504, all `NULL` at HEAD, each now equal to its index-32 entry in BOTH trees (12 distinct
  names), `NULL` 296 -> 272, the declaration at line 3738 in both; (b) all 54 expected names in the driver's spec equal
  `print_function_name()`'s rule applied to their index (0 differ); (c) the gate block's three lists equal the driver's
  classes R+N (24), A (9), C (21) and, with its 5 fixed ids, yield exactly 123 identities; (d) the 54 index->name pairs
  are identical in drivers v2 and v3; (e) GATE 2's driver log is byte-identical to `fixed.out` (md5 `5f803a73`).
* **S19 -- modes:** HEAD's `regress/gate_offline.sh` is 100644 and run by `bash` (`regress/run.sh:85`); the GATE 2 block
  EXECUTES the driver directly, so the driver needs the executable bit; the precedent `regress/diff_autodev_gen.sh` is
  committed 100755; `core.fileMode=false` here.
* **S20 -- coverage outside the block:** `tools/pipeline/check_probe_wiring.py` governs `.py` files only ("A `.sh' path
  can therefore NEVER be in the domain", :1248); GATE 2's self-variant manifest loops over `"$HERE"/diff_*.c` only
  (HEAD `gate_offline.sh:1155`).  Neither covers a `.sh` driver, the committed `diff_autodev_gen.sh` included; no `.py`
  exists under the round's artifacts directory.

---

## 6. PREMISES STATED AS QUESTIONS -- check these; ratification is not wanted

* **P1 -- the `#569` comment's scope (-> Q1c).**  The comment (generator :254-261, section 7.1) says the 24 slots "were
  NULL, and xmem_slow() calls them unguarded while the ld/st decoder installs them as ic->f (both in cpu_m88k_instr.c)".
  S4: 8 of the 24 have no consumer today, and the driver's own header marks them "(no consumer)".  PRETABLE.out section 2
  maps this sentence (C6) to NO ROW, as a guest-path consequence.  Is the sentence true as written, or does it over-state
  -- and is that an L4 matter or acceptable shorthand?
* **P2 -- which tree GATE 2's `PASS (502 checks)` describes (-> Q4d).**  The builder ran GATE 2 on the WORKING TREE
  (BUILD_REPORT D-10).  Its `gate_offline.sh` carries three foreign hunks that add 17 `check` calls (the drafter's count:
  58 added lines; no added line opens a loop; the 17 are named-row presence checks inside the existing WDC IDENTIFY
  block, whose added comment reads "#563: the #473 class, closed.  Seventeen rows" -- another session's in-flight work),
  and GATE 2 also compiles `regress/diff_wdc_identify.c`, which is foreign-modified in the working tree.  The weekly
  battery's GATE 2 counts (quoted in section 9.15 of `brief2_FULL.md`): `offline-differential: PASS (359 checks)` on
  2026-10-04 at HEAD `1329d894`, whose `TREE_DIRTY` list (alphabetical) names neither `regress/gate_offline.sh` nor
  `regress/diff_wdc_identify.c`; `PASS (376 checks)` on 2026-10-11 and 2026-10-18, both verdicts `TREE_DIRTY=YES` WITH
  both files modified.  `1329d894` is the last commit to touch `regress/gate_offline.sh`, `regress/diff_wdc_identify.c`
  or `regress/lib.sh` (`git log 1329d894..HEAD` on those paths is empty).  So I believe HEAD's GATE 2 reports 359,
  376 = 359 + those 17, and the COMMITTED form (the staged copy: HEAD + this round's 126 checks) would report **485**,
  not 502.  That is DERIVED, not measured: the staged copy was never run.  Is the derivation right, and what may the
  record and the commit message claim?
* **P3 -- the block runs BEFORE GATE 2's compiler detection (-> Q4a).**  The block sits after the `#375` block (HEAD :72);
  GATE 2 sets `CC=$(command -v cc || command -v gcc)` only at HEAD :185 (after a `gate_skip "no C compiler on PATH"` at
  :183-184), and `regress/lib.sh` does not export `CC`; the driver uses `CC=${CC:-cc}`.  So I believe that on a host with
  `gcc` but no `cc` the block reds at `gen_compiles` while the gate's own compiled differentials would still run, and that
  on a host with no compiler at all GATE 2 now reports FAIL instead of SKIP (BUILD_REPORT D-9: `gate_skip` prints FAIL
  when any check has already failed, `regress/lib.sh:137-145`).  The `b1w` comment just below the insertion says
  compiler-free checks sit before the compiler check "on purpose".  Is either consequence a defect, and is the placement
  right?
* **P4 -- the `-x` row on this machine (-> Q4a).**  BUILD_REPORT section 2: the driver "must be added with mode 100755
  (the gate tests `-x`; `core.fileMode=false` here, and WSL shows rwx regardless)".  If so, the "driver is executable"
  row cannot go red on this machine, and the committed mode is observable only by `git ls-files -s` after staging or on
  a host that honours file modes.  Is the row sound, and what does the landing owe?
* **P5 -- the pre-fix order (-> Q3d).**  The only pre-edit-DATED red is driver v1's (122 rows; `driver_v1/prefix_HEAD.out`
  09:46:19, run on the unmodified repository; the generator edit is 09:46:58).  The SHIPPED driver v3 (123 rows) was
  measured pre-fix at 10:03:08, AFTER the edit, through `GEN=`/`TABLE=` pointing at byte-exact copies of the HEAD blobs
  (`RUNS.log`, md5 `bebaf439` / `269e6e6f`).  S18(d): the 54 expected pairs are unchanged v1 -> v3; v3 adds the
  `gen_stdout` row (green pre-fix) and the identity column.  Does v1's dated red discharge the order discriminator for
  every v3 row that is red pre-fix, or does the record owe something?
* **P6 -- no per-run self-check (-> Q2e).**  The `#406` driver re-runs its own variant lane on every gate run (the gate
  checks `MUTANT killed: full revert` and `MUTANT killed: noglob only`, section 8.6), and GATE 2 re-runs a self-variant
  for every `diff_*.c` (S20).  The `#569` driver's 16 legs ran ONCE (`table1_20261022/`).  Is the one-time table
  sufficient for a detector of this shape, or is a per-run self-check owed or worth filing?
* **P7 -- the 123 identity pins (-> Q4e).**  PRETABLE_v3 section 5: "checked by construction when the gate block is
  read, and by the green GATE 2 run" -- no leg deletes, renames or duplicates a row.  Is that by-construction reading
  sound (R2's record forms)?  BUILD_REPORT open question 2: 123 individual checks, or one aggregated check that names any
  failing identity?
* **P8 -- the partition outside the 24 (-> Q2d).**  PRETABLE.out section 3 says the guard cell (`size == 0 &&
  scaledness`) is EXHAUSTED by the 24 pins, and lists as SAMPLED or unrowed: halfword kinds other than `ld.hu` sync
  (`ld.h`, `st.h`, `.usr`, no-PC-sync), scaled word with PC-sync, scaled doubleword, and the immediate-form byte cells.
  Is any of those a FLOOR cell under R7 as E amended it (S4: "all 24"), or are they all clause-(e) disclosure?

---

## 7. THE DIFF -- every hunk of the round's four files, INLINED

The numstat was computed WITHOUT touching the git index -- `git show HEAD:<path> | diff -u - <path>`, and for the gate
HEAD's blob against the staged copy.  `git diff` was deliberately not run (another process may hold the index).

    file                                          +     -   form in this brief
    src/cpus/generate_m88k_loadstore.c            8     4   INLINED (7.1) -- the one hunk, whole
    src/cpus/tmp_m88k_loadstore.c                24    24   INLINED (7.2) -- all 8 hunks, whole
    regress/gate_offline.sh   (HEAD -> staged)   45     0   INLINED (7.3) -- the one hunk, whole
    regress/diff_m88k_loadstore_gen.sh          276     0   INLINED (7.4) -- the whole NEW file (untracked), numbered
    -------------------------------------------------------
    regress/gate_offline.sh   (staged -> WT)     58     3   NOT SHOWN -- the three foreign hunks; not this round's and not
                                                            to be committed with it (section 0)
    regress/artifacts/m88kscaledbyte/**          (new)      SUMMARIZED -- section 9 inlines the decisive artifacts; the leg
                                                            variant files L*.diff / S*.diff are NOT SHOWN (each leg is
                                                            named by its id, description and score)

md5 (first 8) of what is shown: generator `bebaf439` -> `6a1fec41`; table `269e6e6f` -> `d222e737`; gate HEAD `8161cafe`
-> staged `7a7fd8bc` (the working-tree file, with the foreign hunks, is `74d84bc1`); driver `cc2f3cf1` -- the instrument
every v3 run used (`RUNS.log`: "want md5 cc2f3cf1575b99459c27f6bdcdaf2abe").

### 7.1 `src/cpus/generate_m88k_loadstore.c` (HEAD -> working tree)
~~~~diff
--- a/src/cpus/generate_m88k_loadstore.c
+++ b/src/cpus/generate_m88k_loadstore.c
@@ -251,10 +251,14 @@
 				continue;
 			}
 
-			if (size == 0 && scaledness) {
-				printf("\tNULL");
-				continue;
-			}
+			/*  #569: no NULL arm for scaled byte accesses.  A
+			    byte's scale factor is 1, so a scaled byte access
+			    is the unscaled one, and print_function_name()
+			    already omits "_scaled" for size 0: these 24 slots
+			    name the unscaled byte handlers.  They were NULL,
+			    and xmem_slow() calls them unguarded while the
+			    ld/st decoder installs them as ic->f (both in
+			    cpu_m88k_instr.c).  */
 
 			printf("\tm88k_instr_");
 			print_function_name(size, store, signedness,
~~~~

### 7.2 `src/cpus/tmp_m88k_loadstore.c` (HEAD -> working tree; regenerated by the fixed generator, never hand-edited -- FIX.out)
The initializer's declaration is at line 3738 in both versions; each hunk changes three entries of one 16-entry
group.  Index of a changed line = (its line number) - 3739.
~~~~diff
--- a/src/cpus/tmp_m88k_loadstore.c
+++ b/src/cpus/tmp_m88k_loadstore.c
@@ -3896,15 +3896,15 @@
 	NULL,
 	NULL,
 	NULL,
-	NULL,
+	m88k_instr_ld_u_1_le_regofs,
 	m88k_instr_ld_u_2_le_scaled_regofs,
 	m88k_instr_ld_u_4_le_scaled_regofs,
 	m88k_instr_ld_u_8_le_scaled_regofs,
-	NULL,
+	m88k_instr_st_1_le_regofs,
 	m88k_instr_st_2_le_scaled_regofs,
 	m88k_instr_st_4_le_scaled_regofs,
 	m88k_instr_st_8_le_scaled_regofs,
-	NULL,
+	m88k_instr_ld_1_le_regofs,
 	m88k_instr_ld_2_le_scaled_regofs,
 	m88k_instr_ld_4_le_scaled_regofs,
 	m88k_instr_ld_8_le_scaled_regofs,
@@ -3912,15 +3912,15 @@
 	NULL,
 	NULL,
 	NULL,
-	NULL,
+	m88k_instr_ld_u_1_le_regofs,
 	m88k_instr_ld_u_2_be_scaled_regofs,
 	m88k_instr_ld_u_4_be_scaled_regofs,
 	m88k_instr_ld_u_8_be_scaled_regofs,
-	NULL,
+	m88k_instr_st_1_le_regofs,
 	m88k_instr_st_2_be_scaled_regofs,
 	m88k_instr_st_4_be_scaled_regofs,
 	m88k_instr_st_8_be_scaled_regofs,
-	NULL,
+	m88k_instr_ld_1_le_regofs,
 	m88k_instr_ld_2_be_scaled_regofs,
 	m88k_instr_ld_4_be_scaled_regofs,
 	m88k_instr_ld_8_be_scaled_regofs,
@@ -3960,15 +3960,15 @@
 	NULL,
 	NULL,
 	NULL,
-	NULL,
+	m88k_instr_ld_u_1_le_usr_regofs,
 	m88k_instr_ld_u_2_le_scaled_usr_regofs,
 	m88k_instr_ld_u_4_le_scaled_usr_regofs,
 	m88k_instr_ld_u_8_le_scaled_usr_regofs,
-	NULL,
+	m88k_instr_st_1_le_usr_regofs,
 	m88k_instr_st_2_le_scaled_usr_regofs,
 	m88k_instr_st_4_le_scaled_usr_regofs,
 	m88k_instr_st_8_le_scaled_usr_regofs,
-	NULL,
+	m88k_instr_ld_1_le_usr_regofs,
 	m88k_instr_ld_2_le_scaled_usr_regofs,
 	m88k_instr_ld_4_le_scaled_usr_regofs,
 	m88k_instr_ld_8_le_scaled_usr_regofs,
@@ -3976,15 +3976,15 @@
 	NULL,
 	NULL,
 	NULL,
-	NULL,
+	m88k_instr_ld_u_1_le_usr_regofs,
 	m88k_instr_ld_u_2_be_scaled_usr_regofs,
 	m88k_instr_ld_u_4_be_scaled_usr_regofs,
 	m88k_instr_ld_u_8_be_scaled_usr_regofs,
-	NULL,
+	m88k_instr_st_1_le_usr_regofs,
 	m88k_instr_st_2_be_scaled_usr_regofs,
 	m88k_instr_st_4_be_scaled_usr_regofs,
 	m88k_instr_st_8_be_scaled_usr_regofs,
-	NULL,
+	m88k_instr_ld_1_le_usr_regofs,
 	m88k_instr_ld_2_be_scaled_usr_regofs,
 	m88k_instr_ld_4_be_scaled_usr_regofs,
 	m88k_instr_ld_8_be_scaled_usr_regofs,
@@ -4152,15 +4152,15 @@
 	NULL,
 	NULL,
 	NULL,
-	NULL,
+	m88k_instr_ld_u_1_le_regofs_nopcsync,
 	m88k_instr_ld_u_2_le_scaled_regofs_nopcsync,
 	m88k_instr_ld_u_4_le_scaled_regofs_nopcsync,
 	m88k_instr_ld_u_8_le_scaled_regofs_nopcsync,
-	NULL,
+	m88k_instr_st_1_le_regofs_nopcsync,
 	m88k_instr_st_2_le_scaled_regofs_nopcsync,
 	m88k_instr_st_4_le_scaled_regofs_nopcsync,
 	m88k_instr_st_8_le_scaled_regofs_nopcsync,
-	NULL,
+	m88k_instr_ld_1_le_regofs_nopcsync,
 	m88k_instr_ld_2_le_scaled_regofs_nopcsync,
 	m88k_instr_ld_4_le_scaled_regofs_nopcsync,
 	m88k_instr_ld_8_le_scaled_regofs_nopcsync,
@@ -4168,15 +4168,15 @@
 	NULL,
 	NULL,
 	NULL,
-	NULL,
+	m88k_instr_ld_u_1_le_regofs_nopcsync,
 	m88k_instr_ld_u_2_be_scaled_regofs_nopcsync,
 	m88k_instr_ld_u_4_be_scaled_regofs_nopcsync,
 	m88k_instr_ld_u_8_be_scaled_regofs_nopcsync,
-	NULL,
+	m88k_instr_st_1_le_regofs_nopcsync,
 	m88k_instr_st_2_be_scaled_regofs_nopcsync,
 	m88k_instr_st_4_be_scaled_regofs_nopcsync,
 	m88k_instr_st_8_be_scaled_regofs_nopcsync,
-	NULL,
+	m88k_instr_ld_1_le_regofs_nopcsync,
 	m88k_instr_ld_2_be_scaled_regofs_nopcsync,
 	m88k_instr_ld_4_be_scaled_regofs_nopcsync,
 	m88k_instr_ld_8_be_scaled_regofs_nopcsync,
@@ -4216,15 +4216,15 @@
 	NULL,
 	NULL,
 	NULL,
-	NULL,
+	m88k_instr_ld_u_1_le_usr_regofs_nopcsync,
 	m88k_instr_ld_u_2_le_scaled_usr_regofs_nopcsync,
 	m88k_instr_ld_u_4_le_scaled_usr_regofs_nopcsync,
 	m88k_instr_ld_u_8_le_scaled_usr_regofs_nopcsync,
-	NULL,
+	m88k_instr_st_1_le_usr_regofs_nopcsync,
 	m88k_instr_st_2_le_scaled_usr_regofs_nopcsync,
 	m88k_instr_st_4_le_scaled_usr_regofs_nopcsync,
 	m88k_instr_st_8_le_scaled_usr_regofs_nopcsync,
-	NULL,
+	m88k_instr_ld_1_le_usr_regofs_nopcsync,
 	m88k_instr_ld_2_le_scaled_usr_regofs_nopcsync,
 	m88k_instr_ld_4_le_scaled_usr_regofs_nopcsync,
 	m88k_instr_ld_8_le_scaled_usr_regofs_nopcsync,
@@ -4232,15 +4232,15 @@
 	NULL,
 	NULL,
 	NULL,
-	NULL,
+	m88k_instr_ld_u_1_le_usr_regofs_nopcsync,
 	m88k_instr_ld_u_2_be_scaled_usr_regofs_nopcsync,
 	m88k_instr_ld_u_4_be_scaled_usr_regofs_nopcsync,
 	m88k_instr_ld_u_8_be_scaled_usr_regofs_nopcsync,
-	NULL,
+	m88k_instr_st_1_le_usr_regofs_nopcsync,
 	m88k_instr_st_2_be_scaled_usr_regofs_nopcsync,
 	m88k_instr_st_4_be_scaled_usr_regofs_nopcsync,
 	m88k_instr_st_8_be_scaled_usr_regofs_nopcsync,
-	NULL,
+	m88k_instr_ld_1_le_usr_regofs_nopcsync,
 	m88k_instr_ld_2_be_scaled_usr_regofs_nopcsync,
 	m88k_instr_ld_4_be_scaled_usr_regofs_nopcsync,
 	m88k_instr_ld_8_be_scaled_usr_regofs_nopcsync,
~~~~

### 7.3 `regress/gate_offline.sh` -- HEAD's blob -> the staged copy `table1_20261022/staged/gate_offline.sh` (the ONE hunk to commit)
The three lines above and below the insertion are HEAD's: the end of the `#375` block (`done`) and the start of the
`b1w` block, whose comment says it is "Placed BEFORE the compiler check on purpose".
~~~~diff
--- a/regress/gate_offline.sh
+++ b/regress/gate_offline.sh
@@ -71,6 +71,51 @@
         "$([ "$(ls_entry $arr 5)" != "$(ls_entry $arr 21)" ] && echo differ || echo same)" "differ"
 done
 
+# ---- #569: the m88k load/store dispatch-table generator --------------------------
+# generate_m88k_loadstore.c printed NULL for the 24 scaled-byte slots of
+# m88k_loadstore[512], which cpu_m88k_instr.c indexes with no NULL check
+# (xmem_slow() calls the slot; the register-form ld/st decoder installs it as
+# ic->f). The fix deletes that NULL arm, so the slots name the unscaled byte
+# handlers. The driver compiles and runs the REAL generator in a scratch copy and
+# reads the COMMITTED table separately -- each alone stays green when only the
+# other is reverted -- against names hard-coded in the driver, never read from
+# either artifact. GEN and TABLE are cleared so this always tests the committed
+# files. A missing or non-compiling generator, one that fails to run, and a
+# missing table are each a red row inside the driver, never a skip.
+MLSLOG=$LOGDIR/diff_m88k_loadstore_gen.log
+if [ ! -x "$HERE/diff_m88k_loadstore_gen.sh" ]; then
+    check "m88k loadstore generator: driver is executable" "no" "yes"
+else
+    GEN= TABLE= "$HERE/diff_m88k_loadstore_gen.sh" > "$MLSLOG" 2>&1
+    sed 's/^/       /' "$MLSLOG"
+    check     "m88k loadstore generator: row failures" \
+              "$(sed -n 's/^ROWS=[0-9]* FAIL=\([0-9]*\)$/\1/p' "$MLSLOG")" "0"
+    check     "m88k loadstore generator: rows run (the denominator is the pin)" \
+              "$(sed -n 's/^ROWS=\([0-9]*\) FAIL=[0-9]*$/\1/p' "$MLSLOG")" "123"
+    check     "m88k loadstore generator: completion sentinel" \
+              "$(grep -c '^M88KLS_DONE$' "$MLSLOG")" "1"
+    #  EVERY ROW BY IDENTITY, each exactly once, from lists held HERE and not read
+    #  from the driver: a deleted, renamed or duplicated row is red by name, which
+    #  the total alone cannot say.  The lists are the driver's contract -- the 24
+    #  repaired slots; the 6 further accepts plus the 3 counterparts that are also
+    #  accepts; the other 21 counterparts -- in both artifacts, plus the generator
+    #  status rows and the cmp row: 4 + 2 x (5 + 24 + 9 + 21) + 1 = 123.
+    _mls_pin="160 164 168 176 180 184 224 228 232 240 244 248 416 420 424 432 436 440 480 484 488 496 500 504"
+    _mls_acc="161 177 418 422 434 438 144 400 404"
+    _mls_cp="128 132 136 148 152 192 196 200 208 212 216 384 388 392 408 448 452 456 464 468 472"
+    _mls_ids="gen_compiles gen_exit gen_stdout gen_count cmp_fresh_committed"
+    for _a in fresh committed; do
+        _mls_ids="$_mls_ids ${_a}_present ${_a}_inits ${_a}_entries ${_a}_nulls ${_a}_lsn"
+        for _i in $_mls_pin; do _mls_ids="$_mls_ids ${_a}_pin$_i"; done
+        for _i in $_mls_acc; do _mls_ids="$_mls_ids ${_a}_acc$_i"; done
+        for _i in $_mls_cp;  do _mls_ids="$_mls_ids ${_a}_cp$_i"; done
+    done
+    for _id in $_mls_ids; do
+        check "m88k loadstore generator: row $_id, exactly once" \
+              "$(grep -ow -- "$_id" "$MLSLOG" | wc -l | tr -d ' ')" "1"
+    done
+fi
+
 #  b1w: the pty record parser's selftest, and a POSITIVE CONTROL that proves the selftest can
 #  still catch something.  Placed BEFORE the compiler check on purpose: it needs only python3,
 #  and a machine without cc must not silently lose parser coverage as well as the
~~~~

### 7.4 `regress/diff_m88k_loadstore_gen.sh` -- the WHOLE new file (276 lines, untracked; md5 `cc2f3cf1`)
~~~~
  1| #!/bin/sh
  2| #
  3| #  #569: does generate_m88k_loadstore.c fill the 24 scaled-byte slots of the
  4| #  m88k_loadstore[512] dispatch table, and does the COMMITTED generated table
  5| #  (src/cpus/tmp_m88k_loadstore.c) carry the same text?
  6| #
  7| #  WHY THIS EXISTS.  The generator printed NULL for every scaled BYTE slot
  8| #  (size 0 with scaledness set), while cpu_m88k_instr.c indexes the table with
  9| #  no NULL check: xmem_slow() calls the slot, and the register-form ld/st
 10| #  decoder installs it as ic->f.  A byte's scale factor is 1, so a scaled byte
 11| #  access is the unscaled one, and print_function_name() already omits
 12| #  "_scaled" for size 0; the fix deletes the NULL arm and the slots name the
 13| #  unscaled byte handlers -- the alias this table already uses for the
 14| #  big-endian byte slots.
 15| #
 16| #  TWO ARTIFACTS, AND EACH IS A FIXED SITE.  The build regenerates the table
 17| #  only when the generator binary or the template is newer (Makefile.skel), so
 18| #  a build compiles EITHER the committed copy or fresh output.  A reader of the
 19| #  committed table alone stays green when only the generator is reverted; a run
 20| #  of the generator alone stays green when only the committed table is.  So
 21| #  this compiles and runs the REAL generator in a scratch copy -- NEVER in the
 22| #  repo: it prints the table to stdout and the table is TRACKED -- reads the
 23| #  committed table separately, pins BOTH with the same rows, and asserts the two
 24| #  are byte-identical.
 25| #
 26| #  THE EXPECTED NAMES ARE HARD-CODED BELOW, never read from either artifact: a
 27| #  tracked generated file is not evidence about its own generator (#406), and
 28| #  slot[i] == slot[i-32] holds under a joint rename and under NULL == NULL.
 29| #
 30| #  CONTRACT -- what this detector is designed to catch:
 31| #    * the deleted arm's 24 cells, by ABSOLUTE name equality in both artifacts.
 32| #      ALL 24 ARE THE FLOOR: main()'s own loops emit every one of them, so an
 33| #      escape at any of the 24 is a floor breach.  16 are today's GUEST-
 34| #      CONSUMER subset, marked "(consumer)": the sync ld/st cells, both
 35| #      endians, plain and .usr (160 164 168 176 180 184 224 228 232 240 244
 36| #      248), and the no-PC-sync plain ld.bu/st.b cells (416 420 432 436).  The
 37| #      other 8 (424 440 480 484 488 496 500 504) are marked "(no consumer)" --
 38| #      a fact about today's callers, not a weaker pin; xmem becomes the
 39| #      consumer of 480 484 496 500 if m88kxmemusr is fixed;
 40| #    * the accept side of the deleted predicate (size == 0 && scaledness), by
 41| #      the de-escalation rule's row per adjacent modelled value: the scaled
 42| #      HALFWORD cells 161/177 (size 1, the adjacent size; with the `size > 0`
 43| #      in print_function_name moved by one they are the name rows that
 44| #      change), scaled word xmem 418 422 434 438, and the unscaled byte cells;
 45| #    * 54 DISTINCT NAME PINS PER ARTIFACT: the 24 repairs, their 24 unscaled
 46| #      counterparts at index-32, and 6 further accepts (161 177 418 422 434
 47| #      438).  Three counterparts are also accept cells (144 400 404); each of
 48| #      those indices is emitted ONCE, as an accept row, so 21 rows are
 49| #      "counterpart" rows;
 50| #    * structure: one 512-entry initializer; 272 NULL entries, SUPPLEMENTARY (a
 51| #      MOVED NULL keeps the count -- the absolute pins carry the floor);
 52| #    * a NARROW SUPPRESSION-COUNT CONTROL, NOT a definition-integrity check: 198
 53| #      `#define LS_N` blocks and the generator's stderr generated_functions ==
 54| #      198 see the deletion of loadstore()'s kept size-0-scaled early return
 55| #      (12 more blocks) and nothing finer -- duplicate or wrong definition
 56| #      NAMES keep both counts;
 57| #    * fresh == committed, byte for byte;
 58| #    * the generator compiles and links, exits 0 and prints something, and the
 59| #      committed table is present and parseable -- each an explicit RED row,
 60| #      never a skip.
 61| #  ROWS: 4 generator status rows + 2 x (5 structural + 54 name pins) + 1 cmp =
 62| #  123, every row emitted on every run.  EVERY ROW CARRIES AN IDENTITY, its
 63| #  first field (gen_*, fresh_*, committed_*, cmp_fresh_committed), which
 64| #  occurs exactly once in the output; gate 2 pins each identity, the total and
 65| #  the sentinel.
 66| #  NOT OBSERVED, deliberately: handler BODIES and the xmem exchange itself (the
 67| #  exchanged byte, neighbour preservation, zero extension) -- guest-path
 68| #  channels that belong to the BLOCKED rung-3 witness record,
 69| #  regress/artifacts/m88kscaledbyte/witness_attempt_20261022/WITNESS_ATTEMPT.md;
 70| #  per-slot positions of the other three NULL arms (held only by the count);
 71| #  scaled doubleword names; the immediate-form byte cells; the size tests in
 72| #  print_function_name beyond the halfword edge; the generated DEFINITIONS
 73| #  beyond their count (unique names, flags, references -- the generated file
 74| #  is not compiled here).
 75| #
 76| #  (c): measured at regress/artifacts/m88kscaledbyte/table1_20261022/L3_commentgen.out
 77| #  (a comment-only generator: the compile row and every fresh-side row red) and
 78| #  .../L4_commenttable.out (a comment-only table: every committed-side row red).
 79| #  .../L8_allnull.out (an all-NULL initializer) is supplementary.  SCORES.txt there.
 80| #
 81| #  Overrides, so a table of variants runs WITHOUT touching the repo:
 82| #  GEN=<generator source>, TABLE=<committed table>, CC=<compiler>.  Gate 2
 83| #  clears GEN and TABLE so it always tests the committed files.
 84| #
 85| #  Offline: a C compiler, no guest, no build tree.  Wired into gate 2.
 86| set -u
 87| 
 88| HERE=$(cd "$(dirname "$0")" && pwd)
 89| SEC=$(cd "$HERE/.." && pwd)
 90| GEN=${GEN:-$SEC/src/cpus/generate_m88k_loadstore.c}
 91| TABLE=${TABLE:-$SEC/src/cpus/tmp_m88k_loadstore.c}
 92| CC=${CC:-cc}
 93| 
 94| WORK=${TMPDIR:-/tmp}/gxsec-m88klsgen.$$
 95| #  A killed run must not reach the sentinel: the signal trap EXITS (and the exit
 96| #  trap cleans up), it does not resume the script.
 97| trap 'rm -rf "$WORK"' 0
 98| trap 'exit 1' 1 2 3 15
 99| rm -rf "$WORK"; mkdir -p "$WORK"
100| 
101| rows=0
102| fails=0
103| row() {   # $1 identity  $2 description  $3 got  $4 want -- equality; every row counts
104|     rows=$((rows + 1))
105|     if [ "$3" = "$4" ]; then
106|         printf '  ok   %-20s %-50s %s\n' "$1" "$2" "$3"
107|     else
108|         fails=$((fails + 1))
109|         printf '  FAIL %-20s %-50s got=%s want=%s\n' "$1" "$2" "$3" "$4"
110|     fi
111| }
112| note() { printf '  --   %s\n' "$1"; }
113| 
114| note "GEN   $GEN"
115| note "TABLE $TABLE"
116| 
117| #  index class expected-name description.  R repair with a guest consumer today,
118| #  N repair with none, A accept, C counterpart (index - 32) of a repair.
119| #  index = 256*no_pc_sync + 128*registeroffset + 64*usr + 32*scaledness +
120| #  16*endianness + 8*signedness + 4*store + size, the generator's loop order.
121| cat > "$WORK/spec" <<'EOF'
122| 160 R m88k_instr_ld_u_1_le_regofs scaled ld.bu le sync
123| 164 R m88k_instr_st_1_le_regofs scaled st.b le sync
124| 168 R m88k_instr_ld_1_le_regofs scaled ld.b le sync
125| 176 R m88k_instr_ld_u_1_le_regofs scaled ld.bu be sync
126| 180 R m88k_instr_st_1_le_regofs scaled st.b be sync
127| 184 R m88k_instr_ld_1_le_regofs scaled ld.b be sync
128| 224 R m88k_instr_ld_u_1_le_usr_regofs scaled ld.bu le usr sync
129| 228 R m88k_instr_st_1_le_usr_regofs scaled st.b le usr sync
130| 232 R m88k_instr_ld_1_le_usr_regofs scaled ld.b le usr sync
131| 240 R m88k_instr_ld_u_1_le_usr_regofs scaled ld.bu be usr sync
132| 244 R m88k_instr_st_1_le_usr_regofs scaled st.b be usr sync
133| 248 R m88k_instr_ld_1_le_usr_regofs scaled ld.b be usr sync
134| 416 R m88k_instr_ld_u_1_le_regofs_nopcsync scaled ld.bu le nosync
135| 420 R m88k_instr_st_1_le_regofs_nopcsync scaled st.b le nosync
136| 424 N m88k_instr_ld_1_le_regofs_nopcsync scaled ld.b le nosync
137| 432 R m88k_instr_ld_u_1_le_regofs_nopcsync scaled ld.bu be nosync
138| 436 R m88k_instr_st_1_le_regofs_nopcsync scaled st.b be nosync
139| 440 N m88k_instr_ld_1_le_regofs_nopcsync scaled ld.b be nosync
140| 480 N m88k_instr_ld_u_1_le_usr_regofs_nopcsync scaled ld.bu le usr nosync
141| 484 N m88k_instr_st_1_le_usr_regofs_nopcsync scaled st.b le usr nosync
142| 488 N m88k_instr_ld_1_le_usr_regofs_nopcsync scaled ld.b le usr nosync
143| 496 N m88k_instr_ld_u_1_le_usr_regofs_nopcsync scaled ld.bu be usr nosync
144| 500 N m88k_instr_st_1_le_usr_regofs_nopcsync scaled st.b be usr nosync
145| 504 N m88k_instr_ld_1_le_usr_regofs_nopcsync scaled ld.b be usr nosync
146| 161 A m88k_instr_ld_u_2_le_scaled_regofs scaled ld.hu le sync (halfword)
147| 177 A m88k_instr_ld_u_2_be_scaled_regofs scaled ld.hu be sync (halfword)
148| 418 A m88k_instr_ld_u_4_le_scaled_regofs_nopcsync scaled word ld le nosync (xmem)
149| 422 A m88k_instr_st_4_le_scaled_regofs_nopcsync scaled word st le nosync (xmem)
150| 434 A m88k_instr_ld_u_4_be_scaled_regofs_nopcsync scaled word ld be nosync (xmem)
151| 438 A m88k_instr_st_4_be_scaled_regofs_nopcsync scaled word st be nosync (xmem)
152| 144 A m88k_instr_ld_u_1_le_regofs unscaled ld.bu be sync
153| 400 A m88k_instr_ld_u_1_le_regofs_nopcsync unscaled ld.bu be nosync
154| 404 A m88k_instr_st_1_le_regofs_nopcsync unscaled st.b be nosync
155| 128 C m88k_instr_ld_u_1_le_regofs unscaled ld.bu le sync
156| 132 C m88k_instr_st_1_le_regofs unscaled st.b le sync
157| 136 C m88k_instr_ld_1_le_regofs unscaled ld.b le sync
158| 148 C m88k_instr_st_1_le_regofs unscaled st.b be sync
159| 152 C m88k_instr_ld_1_le_regofs unscaled ld.b be sync
160| 192 C m88k_instr_ld_u_1_le_usr_regofs unscaled ld.bu le usr sync
161| 196 C m88k_instr_st_1_le_usr_regofs unscaled st.b le usr sync
162| 200 C m88k_instr_ld_1_le_usr_regofs unscaled ld.b le usr sync
163| 208 C m88k_instr_ld_u_1_le_usr_regofs unscaled ld.bu be usr sync
164| 212 C m88k_instr_st_1_le_usr_regofs unscaled st.b be usr sync
165| 216 C m88k_instr_ld_1_le_usr_regofs unscaled ld.b be usr sync
166| 384 C m88k_instr_ld_u_1_le_regofs_nopcsync unscaled ld.bu le nosync
167| 388 C m88k_instr_st_1_le_regofs_nopcsync unscaled st.b le nosync
168| 392 C m88k_instr_ld_1_le_regofs_nopcsync unscaled ld.b le nosync
169| 408 C m88k_instr_ld_1_le_regofs_nopcsync unscaled ld.b be nosync
170| 448 C m88k_instr_ld_u_1_le_usr_regofs_nopcsync unscaled ld.bu le usr nosync
171| 452 C m88k_instr_st_1_le_usr_regofs_nopcsync unscaled st.b le usr nosync
172| 456 C m88k_instr_ld_1_le_usr_regofs_nopcsync unscaled ld.b le usr nosync
173| 464 C m88k_instr_ld_u_1_le_usr_regofs_nopcsync unscaled ld.bu be usr nosync
174| 468 C m88k_instr_st_1_le_usr_regofs_nopcsync unscaled st.b be usr nosync
175| 472 C m88k_instr_ld_1_le_usr_regofs_nopcsync unscaled ld.b be usr nosync
176| EOF
177| 
178| #  The #375 reader (gate_offline.sh's ls_entry), parametrized by file, array
179| #  name and size, and run ONCE per artifact: every entry of the FIRST
180| #  `(*<array>[<size>])(...) = {` initializer, one per line, in index order.
181| #  This table ends `<last entry> };` on the entry's own line, so the end test is
182| #  "the line holds the closing brace" rather than ls_entry's `^};`.
183| #  Prints "<initializers> <entries> <NULL entries>".
184| parse() {   # $1 file  $2 array  $3 size  $4 entries-out
185|     : > "$4"
186|     if [ ! -f "$1" ]; then echo "0 0 0"; return; fi
187|     awk -v arr="$2" -v size="$3" -v out="$4" '
188|         index($0, "(*" arr "[" size "])") && /= *[{]/ {
189|             inits++; if (inits == 1) f = 1; next }
190|         f { last = ($0 ~ /[}]/); gsub(/[ \t,};]/, "")
191|             if ($0 != "") { n++; print > out; if ($0 == "NULL") nul++ }
192|             if (last) f = 0 }
193|         END { printf "%d %d %d\n", inits, n, nul }' "$1"
194| }
195| ent() { sed -n "$(($2 + 1))p" "$1"; }   # $1 entries file  $2 index
196| 
197| #  Every row is emitted on every run -- a missing artifact turns its rows RED,
198| #  it never removes them -- so the row count is constant and gate 2 pins it.
199| artifact_rows() {   # $1 label  $2 file
200|     lbl=$1; file=$2
201|     counts=$(parse "$file" m88k_loadstore 512 "$WORK/$lbl.ent")
202|     #  The trailing zeros keep $1..$3 set (set -u) if the parse printed nothing.
203|     set -- $counts 0 0 0
204|     if [ ! -f "$file" ]; then present=absent
205|     elif [ "$1" -ge 1 ]; then present=yes
206|     else present="no m88k_loadstore[512] initializer"; fi
207|     row "${lbl}_present" "present and parseable" "$present" "yes"
208|     row "${lbl}_inits" "m88k_loadstore[512] initializers" "$1" "1"
209|     row "${lbl}_entries" "initializer entries" "$2" "512"
210|     row "${lbl}_nulls" "NULL entries (supplementary)" "$3" "272"
211|     if [ -f "$file" ]; then nls=$(grep -c '^#define LS_N ' "$file"); else nls=absent; fi
212|     row "${lbl}_lsn" "#define LS_N blocks (suppression count)" "$nls" "198"
213|     while read -r i c name desc; do
214|         case $c in
215|         R) id=${lbl}_pin$i; d="repair $desc (consumer)" ;;
216|         N) id=${lbl}_pin$i; d="repair $desc (no consumer)" ;;
217|         A) id=${lbl}_acc$i; d="accept $desc" ;;
218|         *) id=${lbl}_cp$i;  d="counterpart $desc" ;;
219|         esac
220|         row "$id" "$d" "$(ent "$WORK/$lbl.ent" "$i")" "$name"
221|     done < "$WORK/spec"
222| }
223| 
224| # ------------------------------------------------- the generator, run for real
225| compiled=no
226| if [ ! -f "$GEN" ]; then
227|     gres="no -- source absent"
228| elif ! cp "$GEN" "$WORK/generate_m88k_loadstore.c" 2>/dev/null; then
229|     gres="no -- source unreadable"
230| elif ( cd "$WORK" && $CC -o generate_m88k_loadstore generate_m88k_loadstore.c ) \
231|         > "$WORK/cc.log" 2>&1 && [ -x "$WORK/generate_m88k_loadstore" ]; then
232|     gres=yes; compiled=yes
233| else
234|     gres="no -- the compile or link failed"
235| fi
236| row gen_compiles "generator: compiles and links" "$gres" "yes"
237| if [ "$compiled" != yes ] && [ -s "$WORK/cc.log" ]; then
238|     sed -e "s|$WORK/||g" -e 's/^/  --   cc: /' "$WORK/cc.log" | head -6
239| fi
240| 
241| #  EXECUTION is its own pair of rows: a generator that compiles and then exits
242| #  non-zero, or prints nothing, is red here and not only downstream.
243| if [ "$compiled" = yes ]; then
244|     ( cd "$WORK" && ./generate_m88k_loadstore > fresh.c 2> gen.err ); grc=$?
245| else
246|     grc="not run"
247| fi
248| row gen_exit "generator: exit status" "$grc" "0"
249| if [ "$compiled" != yes ]; then sres="not run"
250| elif [ -s "$WORK/fresh.c" ]; then sres=yes
251| else sres="no -- stdout empty"; fi
252| row gen_stdout "generator: stdout non-empty" "$sres" "yes"
253| if [ -f "$WORK/gen.err" ]; then
254|     gf=$(sed -n 's/^.*: generated_functions = \([0-9][0-9]*\)$/\1/p' "$WORK/gen.err" | head -1)
255|     [ -n "$gf" ] || gf="not reported"
256| else
257|     gf=absent
258| fi
259| row gen_count "generator: stderr generated_functions" "$gf" "198"
260| 
261| # ---------------------------------------------------- both artifacts, same rows
262| artifact_rows fresh "$WORK/fresh.c"
263| artifact_rows committed "$TABLE"
264| 
265| if [ ! -f "$WORK/fresh.c" ]; then cres="fresh output absent"
266| elif [ ! -f "$TABLE" ]; then cres="committed table absent"
267| elif cmp -s "$WORK/fresh.c" "$TABLE"; then cres=identical
268| else cres=differ; fi
269| row cmp_fresh_committed "fresh == committed, byte for byte (cmp)" "$cres" "identical"
270| if [ "$cres" = differ ]; then
271|     diff "$WORK/fresh.c" "$TABLE" | head -8 | sed 's/^/  --   diff: /'
272| fi
273| 
274| printf '\nROWS=%d FAIL=%d\n' "$rows" "$fails"
275| printf 'M88KLS_DONE\n'
276| if [ "$fails" = 0 ]; then exit 0; else exit 1; fi
~~~~

---

## 8. SOURCE CONTEXT (EXCERPTS) -- working tree, byte-identical to HEAD except the generator

### 8.1 The FIXED generator -- `print_function_name()` whole, `loadstore()`'s early returns, and `main()`'s table printer (the edited block's enclosing loop, to the end of `main()`)
~~~~
 58| void print_function_name(int size, int store, int signedness,
 59| 	int endianness, int scaledness, int usr, int registeroffset,
 60| 	int no_pc_sync)
 61| {
 62| 	if (store)
 63| 		printf("st");
 64| 	else {
 65| 		printf("ld");
 66| 		if (!signedness)
 67| 			printf("_u");
 68| 	}
 69| 	printf("_%i", 1 << size);
 70| 
 71| 	if (endianness >= 0) {
 72| 		/*  Special case so that Byte loads/stores are only
 73| 		    included ones (for little endian):  */
 74| 		if (size == 0 && endianness)
 75| 			printf("_le");
 76| 		else
 77| 			printf(endianness? "_be" : "_le");
 78| 	}
 79| 
 80| 	if (scaledness && size > 0)
 81| 		printf("_scaled");
 82| 
 83| 	if (usr)
 84| 		printf("_usr");
 85| 
 86| 	if (registeroffset)
 87| 		printf("_regofs");
 88| 
 89| 	if (no_pc_sync)
 90| 		printf("_nopcsync");
 91| }
  ...
 98| 	if (store && signedness)
 99| 		return;
100| 
101| 	if (size == 0 && endianness)
102| 		return;
103| 
104| 	if (size == 0 && scaledness)
105| 		return;
106| 
107| 	if (!registeroffset && usr)
108| 		return;
109| 
110| 	if (!registeroffset && scaledness)
111| 		return;
  ...
218| 	/*  Array of pointers to fast load/store functions:  */
219| 	printf("\n\nvoid (*m88k_loadstore[512])(struct cpu *, struct "
220| 	    "m88k_instr_call *) = {\n");
221| 	for (no_pc_sync=0; no_pc_sync<=M88K_LOADSTORE_NO_PC_SYNC;
222| 		      no_pc_sync+=M88K_LOADSTORE_NO_PC_SYNC)
223| 	 for (registeroffset=0; registeroffset<=M88K_LOADSTORE_REGISTEROFFSET;
224| 		      registeroffset+=M88K_LOADSTORE_REGISTEROFFSET)
225| 	  for (usr=0; usr<=M88K_LOADSTORE_USR; usr+=M88K_LOADSTORE_USR)
226| 	   for (scaledness=0; scaledness<=M88K_LOADSTORE_SCALEDNESS;
227| 			scaledness+=M88K_LOADSTORE_SCALEDNESS)
228| 	    for (endianness=0; endianness<=M88K_LOADSTORE_ENDIANNESS;
229| 			  endianness+=M88K_LOADSTORE_ENDIANNESS)
230| 	      for (signedness=0; signedness<=M88K_LOADSTORE_SIGNEDNESS;
231| 			    signedness+=M88K_LOADSTORE_SIGNEDNESS)
232| 	        for (store=0; store<=M88K_LOADSTORE_STORE;
233| 			      store+=M88K_LOADSTORE_STORE)
234| 		  for (size=0; size<=3; size++) {
235| 			if (store || size || signedness || endianness
236| 			    || scaledness || usr || registeroffset || no_pc_sync)
237| 				printf(",\n");
238| 
239| 			if (store && signedness) {
240| 				printf("\tNULL");
241| 				continue;
242| 			}
243| 
244| 			if (!registeroffset && usr) {
245| 				printf("\tNULL");
246| 				continue;
247| 			}
248| 
249| 			if (!registeroffset && scaledness) {
250| 				printf("\tNULL");
251| 				continue;
252| 			}
253| 
254| 			/*  #569: no NULL arm for scaled byte accesses.  A
255| 			    byte's scale factor is 1, so a scaled byte access
256| 			    is the unscaled one, and print_function_name()
257| 			    already omits "_scaled" for size 0: these 24 slots
258| 			    name the unscaled byte handlers.  They were NULL,
259| 			    and xmem_slow() calls them unguarded while the
260| 			    ld/st decoder installs them as ic->f (both in
261| 			    cpu_m88k_instr.c).  */
262| 
263| 			printf("\tm88k_instr_");
264| 			print_function_name(size, store, signedness,
265| 			    endianness, scaledness, usr, registeroffset,
266| 			    no_pc_sync);
267| 		}
268| 	printf(" };\n");
~~~~

### 8.2 The consumers (`src/cpus/cpu_m88k_instr.c`, not edited): `X(xmem_slow)`, the register-form decoder, the immediate form; then `cpu_dyntrans.c`
~~~~
2357| 	int scaled = iword & 0x200;
2358| 	int size   = iword & 0x400;
2359| 	int user   = iword & 0x80;
  ...
2368| 	if (!regofs) {
2369| 		/*  immediate offset:  */
2370| 		scaled = 0;
2371| 		size = (iword >> 26) & 1;
2372| 		user = 0;
2373| 	}
  ...
2377| 	xmem_load = m88k_loadstore[ (size? 2 : 0)
2378| 	    + (cpu->byte_order == EMUL_BIG_ENDIAN? M88K_LOADSTORE_ENDIANNESS : 0)
2379| 	    + (scaled? M88K_LOADSTORE_SCALEDNESS : 0)
2380| 	    + (user? M88K_LOADSTORE_USR : 0)
2381| 	    + (regofs? M88K_LOADSTORE_REGISTEROFFSET : 0)
2382| 	    + M88K_LOADSTORE_NO_PC_SYNC ];
  ...
2395| 	xmem_load(cpu, &call);
  ...
2411| 	xmem_store = m88k_loadstore[ (size? 2 : 0)
2412| 	    + M88K_LOADSTORE_STORE
2413| 	    + (cpu->byte_order == EMUL_BIG_ENDIAN? M88K_LOADSTORE_ENDIANNESS : 0)
2414| 	    + (scaled? M88K_LOADSTORE_SCALEDNESS : 0)
2415| 	    + (user? M88K_LOADSTORE_USR : 0)
2416| 	    + (regofs? M88K_LOADSTORE_REGISTEROFFSET : 0)
2417| 	    + M88K_LOADSTORE_NO_PC_SYNC ];
  ...
2426| 	xmem_store(cpu, &call);
~~~~
~~~~
3604| 			if (iword & 0x100)
3605| 				user = 1;
3606| 			if (iword & 0x80)
3607| 				wt = 1;
3608| 			if (iword & 0x200)
3609| 				scaled = 1;
3610| 
3611| 			if (wt) {
3612| 				fatal("wt bit not yet implemented! TODO\n");
3613| 				goto bad;
3614| 			}
  ...
3622| 				ic->f = m88k_loadstore[ opsize
3623| 				    + (op==1? M88K_LOADSTORE_STORE : 0)
3624| 				    + (signedness? M88K_LOADSTORE_SIGNEDNESS:0)
3625| 				    + (cpu->byte_order == EMUL_BIG_ENDIAN?
3626| 				       M88K_LOADSTORE_ENDIANNESS : 0)
3627| 				    + (scaled? M88K_LOADSTORE_SCALEDNESS : 0)
3628| 				    + (user? M88K_LOADSTORE_USR : 0)
3629| 				    + M88K_LOADSTORE_REGISTEROFFSET ];
  ...
3654| 				/*  xmem:  */
3655| 				ic->f = instr(xmem_slow);
3656| 				ic->arg[0] = iword;
3657| 				if (d == M88K_ZERO_REG)
3658| 					ic->f = instr(nop);
~~~~
~~~~
3087| 			ic->f = m88k_loadstore[ opsize
3088| 			    + (store? M88K_LOADSTORE_STORE : 0)
3089| 			    + (signedness? M88K_LOADSTORE_SIGNEDNESS:0)
3090| 			    + (cpu->byte_order == EMUL_BIG_ENDIAN?
3091| 			       M88K_LOADSTORE_ENDIANNESS : 0) ];
  ...  (src/cpus/cpu_dyntrans.c)
1906| 	if (ic->f == NULL) {
1907| 		fatal("INTERNAL ERROR: ic->f == NULL!\n");
1908| 		goto bad;
~~~~

### 8.3-8.6 (condensed) The build rule (8.3, `Makefile.skel`), the scaled address (8.4, `cpu_m88k_instr_loadstore.c`), GATE 2's frame (8.5: HEAD `gate_offline.sh` compiler detection; `lib.sh` `gate_skip`), the `#406` precedent (8.6: its wiring and per-run variant checks)
~~~~
134| tmp_m88k_loadstore.c: cpu_m88k_instr_loadstore.c generate_m88k_loadstore
135| 	./generate_m88k_loadstore > tmp_m88k_loadstore.c
  ...  (cpu_m88k_instr_loadstore.c)
 65| 	uint32_t addr = reg(ic->arg[1]) +
 66| #ifdef LS_REGOFS
 67| #ifdef LS_SCALED
 68| 	    LS_SIZE *
 69| #endif
 70| 	    reg(ic->arg[2]);
~~~~
~~~~
 183| command -v cc >/dev/null 2>&1 || command -v gcc >/dev/null 2>&1 || \
 184|     gate_skip "no C compiler on PATH"
 185| CC=$(command -v cc || command -v gcc)
  ...  (regress/lib.sh)
137| gate_skip() {
138|     echo
139|     if [ "${_fails:-0}" != 0 ]; then
140|         echo "${C_BAD}$GATE_NAME: FAIL${C_OFF} ($_fails of $_checks checks failed" \
141|              "before this section could not run: $*)"
142|         exit 1
143|     fi
144|     echo "${C_SKIP}$GATE_NAME: SKIP${C_OFF} -- $*"; exit $EXIT_SKIP
145| }
~~~~
~~~~
1899| if [ ! -x "$HERE/diff_autodev_gen.sh" ]; then
1900|     check "autodev generator: driver is executable" "no" "yes"
1901| else
1902|     "$HERE/diff_autodev_gen.sh" > "$AGLOG" 2>&1
  ...
1914|     check     "autodev generator: the full-revert mutant is present" \
1915|               "$(grep -c 'MUTANT killed: full revert' "$AGLOG")" "1"
1916|     check     "autodev generator: the HALF-FIX mutant is present" \
1917|               "$(grep -c 'MUTANT killed: noglob only' "$AGLOG")" "1"
  ...
1925|     check     "autodev generator: no mutant survives" \
1926|               "$(grep -c 'SURVIVES' "$AGLOG")" "0"
~~~~

---

## 10. The project rules the questions apply -- quoted VERBATIM with their bounds

From the WORKING-TREE carrier `GXEMUL-SEC/tools/CLAUDE.md` (== the root `CLAUDE.md`); R2 (owner ruling of 2026-10-09)
is NOT committed at HEAD.  Numbering as in `brief2_FULL.md`.  Omitted here because no question depends on their TEXT:
R5 (its bound is restated in S9-S15: a callee compare is outside the DEPENDS-ON walk), R6 (joint cells), R8 (rule D2:
S12 says the halfword rows do NOT rest on it), R11 (the anchor rule: B2 applies it, S9), R13 (accept-row failability:
B3 + E settle the accept rows), R14 (the pre-table rewrite rule: PRETABLE_v3 section 1 discharges it), R19 (applied in
section 9's preamble), R20.

**R1 -- THE FLOOR** -- `tools/CLAUDE.md` 1328-1333:
~~~~
1328| > **THE FLOOR.** A detector is VACUOUS — replace it IN-ROUND — unless it (a) fails on the
1329| > pre-fix build, (b) fails on a **VERBATIM REINSTATEMENT of the removed defect at EVERY fixed
1330| > site**, and (c) fails on a **NULL MEDIUM** -- a product medium carrying none of the behaviour under
1331| > test (the clause-(c) block below says what that is per instrument kind). Below the floor, the
1332| > round's own claim to have "shipped a detector with the fix" is a WRONG RECORD, which the
1333| > stopping rule already fixes in-round.
~~~~

**R2 -- clause (c): the null medium by instrument kind, and the record forms (EXCERPT)** -- `tools/CLAUDE.md` 1340-1349, 1358-1362:
~~~~
1340| > **ONE criterion -- a product medium carrying none of the behaviour under test -- and its object
1341| > differs by instrument kind:**
1342| > * an offline differential that `#include`s the product: a COMMENT-ONLY product source, which must
1343| >   fail to COMPILE, with a gate that reds on the compile failure (measured for `#488`:
1344| >   `regress/artifacts/shortread/nullmedium_20261009/RECEIPT.txt`);
1345| > * a runtime probe: an ABSENT or NON-EMULATOR binary (every session dies), or a build WITHOUT the
1346| >   device for a device round;
1347| > * an instruction-handler round: an IDENTITY BODY (decode and retire, write nothing) -- the
1348| >   recommended default, two measured legs at `#527`.
1349| >
  ...
1358| > **RECORD CLAUSE (c) IN ONE OF EXACTLY TWO FORMS, never as a bare clause letter beside a row name:**
1359| > * `(c): measured at <artifact>` -- the leg was run and its receipt is durable;
1360| > * `(c): by construction via <row/pin>, leg not run` -- e.g. the gate pins the row count by EQUALITY
1361| >   and a named row reds on a dead run, or the differential `#include`s the product and its gate reds
1362| >   on a compile failure.  **A by-construction claim is checked by READING that shape; where the reading
~~~~

**R3 -- clause (d)** -- `tools/CLAUDE.md` 1376-1377:
~~~~
1376| > **(d) The detector must also fail when the fix is PRESENT but its REPAIR IS NULLED —
1377| > the guard kept, its effect removed.**
~~~~

**R4 -- the two (d) shapes, including the pure-deletion form** -- `tools/CLAUDE.md` 1428-1433:
~~~~
1428| > **The two shapes, once the enumeration is right:**
1429| > * **fix ADDS a predicate** -> weaken the added one (unchanged; the original rule).
1430| > * **fix adds none** -> the (d) mutant reroutes an EXISTING guard's repair. For a
1431| >   de-fatalisation: **swap the guard's operand for a field the guarded BODY reads.**
1432| >   For a pure deletion: **re-introduce the removed behaviour under a DIFFERENT predicate**
1433| >   -- not the same one widened, which is (b) wearing (d)'s clothes.
~~~~

**R7 -- the floor (cells a row is OWED for) versus clause-(e) disclosure** -- `tools/CLAUDE.md` 1517-1522:
~~~~
1517| > > **The rule ENUMERATES joint cells wherever the body distinguishes them; the FLOOR -- the cells a row
1518| > > is OWED for -- is the cross-product of the guard's dominating predicates with the device-STATE lvalues
1519| > > the fix's own repair path reads that are JOINTLY REACHABLE through its own data flow.**  The bits of
1520| > > the single value being written are single-operand MARGINALS, not floor; joint cells outside the floor
1521| > > are clause-(e) coverage debt, subject to the one ask-again.  A filter may reject or discharge a cell
1522| > > but may demand a new row only for a floor cell -- so it cannot grow unbounded.
~~~~

**R9 -- the pre-table check: CLAIM -> ROW and CHANNEL** -- `tools/CLAUDE.md` 1725, 1741:
~~~~
1725| > | **CLAIM -> ROW** | every ADDED comment sentence asserting an OBSERVABLE CONSEQUENCE owes a row or an explicit no-row sentence. Claim verbs (*observes, controls, pins, proves, the X control*) are EXAMPLES, not the test | a "device-signature control" claimed in prose and implemented by nothing |
  ...
1741| > | **CHANNEL** | for each row, name **the mutant it kills** and **the observable that differs under that mutant**. A row whose named channel cannot vary under its named mutant is VACUOUS BY CONSTRUCTION, and that is knowable at writing time, before any table runs | a survival oracle at a REFUSAL-EFFECT site: guarded and unguarded code both survive |
~~~~

**R10 -- clause (e): the contract** -- `tools/CLAUDE.md` 1801-1805:
~~~~
1801| > **(e) THE CONTRACT.** The probe header names which edits this detector is designed
1802| > to catch. *A detector that says so is falsifiable; one claiming completeness is
1803| > not* -- and a later escape becomes "outside the contract" or "a breach of it",
1804| > which are different dispositions, rather than an argument about overclaiming.
1805| > Two lines in a header.
~~~~

**R12 -- the de-escalation clause** -- `tools/CLAUDE.md` 2406-2415:
~~~~
2406| > **A fatal→survive fix DELETES THE ACCIDENTAL TRIPWIRE that made guard-mask growth
2407| > self-announcing.** Before #447, adding `| TCR_UNIE` to a guard mask meant `exit(1)` on the
2408| > first legal write — unmissable. After it, the same edit means a **silently refused write** and
2409| > nothing anywhere notices.
2410| >
2411| > So: **when a fix removes a host-fatal guard, enumerate from the diff every predicate that used
2412| > to gate death, and the detector shipping with that fix must pin the ACCEPT SIDE of each** — a
2413| > row per adjacent modelled bit or value, proving legal writes still land. Those rows are part
2414| > of the FIX'S COST, not future strengthening, because the fix itself destroyed the old
2415| > (accidental) detector for that class.
~~~~

**R15 -- the ask-again: capped at ONE ask; the cap counts asks, not findings** -- `tools/CLAUDE.md` 2471-2475, 2481-2483:
~~~~
2471| > **CAPPED AT ONE ASK-AGAIN PER DETECTOR PER ROUND.** This is not the #392 chain — #392 was
2472| > unbounded fix-of-fix passes with no stop condition; this is a single extra adversarial query
2473| > against a clean table with a measured stop: nothing found, done; something found, row added
2474| > under L1, done. **The cap IS the anti-#392 clause.** A second ask-again after an empty first
2475| > is exactly where the chain starts, and anything found past the cap is FILED, never fixed.
  ...
2481| > > Everything ONE ask returns is disposed of INDIVIDUALLY under L1–L4 and the floor — and **a
2482| > > floor breach among the findings is L2, repaired in-round however late it is found.** A
2483| > > second ASK is where the #392 chain starts; the number of rows one ask yields is not.
~~~~

**R16 -- the four licences for an in-round fix of detector material (everything else is FILED)** -- `tools/CLAUDE.md` 2608-2618:
~~~~
2608| > Everything else is FILED. Named so no round has to re-argue it:
2609| >
2610| > * **L1 — pre-ship construction.** The row is part of the deliverable still being built. A row
2611| >   measured vacuous before commit is unfinished, not a reopening. **The stopping rule governs
2612| >   findings against SHIPPED material only.**
2613| > * **L2 — floor breach.** The shipped detector fails vacuity-floor clause (a), (b) or (c) —
2614| >   replace in-round however late it is found.
2615| > * **L3 — undischarged obligation.** The row is the sole carrier of something the round OWES
2616| >   (a de-escalation accept row; the "shipped a detector" claim itself). A vacuous sole carrier
2617| >   makes the round's record false.
2618| > * **L4 — wrong record.** Prose or comments claiming coverage a measurement refutes.
~~~~

**R17 -- the oracle-order discriminator and its "the code does not move" clause** -- `tools/CLAUDE.md` 2511-2513, 2518-2523:
~~~~
2511| > > **Re-pin the oracle FIRST. Measure the COMMITTED build RED under the new expectations.
2512| > > THEN change the code.** Same scripts, opposite colour. If you cannot show that red, you
2513| > > do not have test-first, and the re-pin collapses into laundering.
  ...
2518| > > While the defect is still open, the committed build IS the pre-fix build: re-pin the oracle, measure
2519| > > HEAD RED at one input in the corrected region, and keep that receipt at a durable path dated before
2520| > > any handler edit -- it is the order discriminator AND the row's witness.  A divergence argument or a
2521| > > documentary provenance record (a CHANGELOG passage, a commit message) is CORROBORATION, never a
2522| > > substitute for that red, and a retrospective run against a reconstructed pre-fix tree supplies a red
2523| > > but not an authentic pre-edit DATE.  **Bound: one measured red per oracle a ROW CONSUMES**; a helper no
~~~~

**R18 -- the bound on the `detector:` witness term** -- `tools/CLAUDE.md` 2963-2967:
~~~~
2963| > **THE BOUND: `detector:` IS NOT A RUNG.** It records that a fix shipped with a MEASURED
2964| > DETECTOR and no guest-path witness. It ranks BELOW every access witness, and it does NOT
2965| > satisfy the reproduce-before-you-edit step: **a round using it still owes the rung-3 ATTEMPT**
2966| > the 2026-08-27 lifecycle ruling requires, and must record that the attempt was made and what
2967| > it found. The one thing it may never mean is *we did not think to ask*.
~~~~

**R21 -- the repair chain: effort on the diff, the floor question on the composite** -- `tools/CLAUDE.md` 2686-2688:
~~~~
2686| > > **Review EFFORT is scoped to the repair diff, so settled design is not re-litigated. The
2687| > > FLOOR QUESTION -- does a clean-sweep mutant exist in the (d) enumeration -- is asked of the
2688| > > SHIPPED COMPOSITE on every pass.**
~~~~

---

## 11. QUESTIONS -- VERDICT LINE FIRST (format in section 0)

**Q1 -- THE FIX: exactly the agreed repair, and nothing else?**

(a) Is the generator diff (7.1) exactly the agreed repair -- the WHOLE arm removed (A1: the condition, its
`printf("\tNULL")`, the `continue`, the brace), `loadstore()`'s early return kept (A2, S1), the decoder untouched (A3;
`cpu_m88k_instr.c` is byte-identical to HEAD) -- and nothing else?  Walk the 4 removed and the 8 added lines.

(b) Is the regenerated table (7.2) exactly the 24 `NULL` -> name lines and nothing else -- 24 of 24 changed lines, 272
`NULL`, 512 entries?  WALK THE 24: for each index decode (kind, endianness, `.usr`, PC-sync) from the index formula in
the driver's header (7.4, lines 117-120), and say whether the new name is the handler the architecture requires for that
cell (S5).  Every big-endian slot carries an `_le` name -- confirm that this is the existing byte idiom (S5), not an error.

(c) CLAIM -> ROW (R9): for each sentence of the `#569` comment (generator :254-261) -- "no NULL arm for scaled byte
accesses"; "A byte's scale factor is 1, so a scaled byte access is the unscaled one"; "print_function_name() already omits
"_scaled" for size 0"; "these 24 slots name the unscaled byte handlers"; "They were NULL"; "xmem_slow() calls them
unguarded while the ld/st decoder installs them as ic->f (both in cpu_m88k_instr.c)" -- does a row observe it, or does it
carry an explicit no-row basis (PRETABLE.out section 2, C1-C6)?  Answer P1.  Then the same for the GATE 2 block's
comment (7.3) and for the driver header's CONTRACT sentences (7.4, lines 30-74).

(d) Does deleting the arm change any OTHER generated output -- the separator logic (generator :235-237), the stderr
`generated_functions` count, the other three `NULL` arms?  The measured facts are `gen_count` 198 and `fresh_lsn` 198
green in `fixed.out`, and, in each build tree, make regenerated the table and it `cmp`s clean against GXEMUL-SEC's
(CLEARANCE.out).

**Q2 -- THE DETECTOR AS SHIPPED: do the 123 rows discharge what pass 1 ruled, and is any of them vacuous?**

(a) Do the 123 rows discharge B1-B12 AS AMENDED BY E?  Walk them: the absolute per-index pins at all 24 cells in BOTH
artifacts (B2); the accept pins 161 177 434 438 418 422 144 400 404 (B3); the 21 counterpart rows; the structural rows
(B4); the generator compile AND execution status rows `gen_compiles`, `gen_exit`, `gen_stdout`, `gen_count` (B5); fresh
== committed (B1 iii); one identity per row, each pinned by the gate (B10); the enumerated total 123 (B12; S15).

(b) VACUOUS BY CONSTRUCTION (R9, the CHANNEL line): is any row's named observable unable to vary under its named leg?
PRETABLE.out section 5 names the channel per row group; PRETABLE_v3 section 5 the changed rows.  PRETABLE.out says
`committed_lsn` and both sides' `_present` / `_inits` / `_entries` rows have no red leg except a null medium -- disclosed,
or vacuous?

(c) THE CONTRACT (R10): does the header (7.4, lines 30-79) state the floor (all 24), the guest-consumer subset (16) and
what the detector does NOT observe?  Does it claim anything no row observes (an L4 candidate)?

(d) Answer P8.

(e) Answer P6.

(f) **THE ONE ASK-AGAIN** (R15: the project allows exactly one after a clean table; everything it returns is disposed of
individually, and a floor breach among the findings is L2).  Is there a change to the generator or to the committed
table under which all 123 rows stay green while a cell the CONTRACT claims dispatches differently?  Say whether one
exists.  If it does, name WHERE it acts (the generator line, or the table index), the row you expect to stay green, and
why that row's observable cannot vary under it -- describe it; do not write patch text.  If none exists inside the
contract, say so and give the partition argument (which inputs the repair changes the answer for, and which rows see
each).

