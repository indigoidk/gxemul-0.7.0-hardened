# PASS-2 DIFF REVIEW -- round `#569`, ledger row `m88kscaledbyte` (GXemul hardened fork)
**Brief v1, COMPACT form -- for seats that cannot read files: self-contained.**  Drafted 2026-10-23 ~10:50 -0500.
Tree under review: the `GXEMUL-SEC/` WORKING TREE over HEAD `5986c137` -- the round is IN FLIGHT and UNCOMMITTED
(S0).  Built from `GXEMUL-SEC/tools/BRIEF_TEMPLATE.md` (working tree).  The file-reading form, with the whole-file
inlines, is `brief2_FULL.md`; the QUESTIONS (section 11) and the premises-as-questions (section 6) are identical.


> **THIS PACKET (packet-fed seat): Q1 ONLY (the fix diff)**  Sections not carried here are omitted by number; nothing omitted is needed for the questions carried.

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

