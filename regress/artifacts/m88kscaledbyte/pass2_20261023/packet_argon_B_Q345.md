# PASS-2 DIFF REVIEW -- round `#569`, ledger row `m88kscaledbyte` (GXemul hardened fork)
**Brief v1, COMPACT form -- for seats that cannot read files: self-contained.**  Drafted 2026-10-23 ~10:50 -0500.
Tree under review: the `GXEMUL-SEC/` WORKING TREE over HEAD `5986c137` -- the round is IN FLIGHT and UNCOMMITTED
(S0).  Built from `GXEMUL-SEC/tools/BRIEF_TEMPLATE.md` (working tree).  The file-reading form, with the whole-file
inlines, is `brief2_FULL.md`; the QUESTIONS (section 11) and the premises-as-questions (section 6) are identical.


> **THIS PACKET (packet-fed seat): Q3, Q4 AND Q5 ONLY (the legs; wiring/clearance/gates; records)**  Sections not carried here are omitted by number; nothing omitted is needed for the questions carried.

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

## 9. THE MEASUREMENTS (DECISIVE LINES, VERBATIM; `regress/artifacts/m88kscaledbyte/table1_20261022/` unless stated)

Every `.out` cited ends with its completion sentinel (`M88KLS_DONE`), checked by the drafter with `tail -1` (R19).
Subsections keep the FULL form's numbers.  BUILD_REPORT.md, SCORES.txt, PRETABLE*.out and CLEARANCE.out are inlined
WHOLE in `brief2_FULL.md`; here only the lines a question depends on.  FULL-only: 9.5 RUNS.log (every v3 run used driver
md5 `cc2f3cf1`; it records each run's GEN/TABLE md5), 9.8 the per-run score lines (all 18 outputs end `M88KLS_DONE`),
9.9 DUPNAMES.out (L7's generated definitions carry 24 duplicated `#define LS_N` names, S1's 12, HEAD and the fix 0),
9.10 FIX.out, 9.14 BASELINE.out, 9.15 the battery counts (quoted in P2).

### 9.1 `BUILD_REPORT.md` -- sections 7-8: the disagreements D-1..D-10 and the open questions
~~~~
 93| ## 7. What disagreed with the spec or a ruling (by id), and deviations
 94| * **D-1 (BUILD_SPEC section 6, L5; B7).**  The spec's L5 pointer named `grok_t1p1.txt:76` and `codex_t1p1.txt:100`,
 95|   which are two different predicates (first differences 416 and 256).  The adjudication (B7) resolved L5 to Grok's;
 96|   Codex's is kept only as the labelled supplementary L5b.
 97| * **D-2 (B8; PRETABLE.out section 0).**  The 16-floor / 8-clause-(e) split is superseded: all 24 are floor; 16 is the
 98|   consumer subset.  PRETABLE.out is left as written; `PRETABLE_v3.out` records the change.
 99| * **D-3 (B3, B4, B5, B10, B12).**  Applied as the adjudication amended them (section 3).  B10's per-identity pins raise
100|   GATE 2 from 376 to 502 checks; nothing in `tools/` or `regress/` pins that count (searched).
101| * **D-4 (BUILD_SPEC section 4).**  v3's pre-fix run (`prefix_HEAD_v3.out`) went through the GEN/TABLE overrides on the
102|   byte-exact HEAD blobs AFTER the step-5 edit, because the adjudication arrived after the fix.  The authentic
103|   pre-edit-dated receipt is `driver_v1/prefix_HEAD.out` (09:46:19, before the 09:46:58 generator edit).  The repo
104|   was not reverted to re-date it.
105| * **D-5 (PRETABLE.out, two small inaccuracies, not rewritten).**  Section 5 predicted `0` for L3's fresh LS_N row and the
106|   driver reports `absent` (red either way).  Section 1 says "four sites index unguarded" while listing three; the
107|   fourth, the immediate form at `cpu_m88k_instr.c:3087`, cannot form a scaled index.
108| * **D-6 (supplementary legs beyond the spec).**  L5b and S1 (from PRETABLE.out), S2-S5 (added for the B5 rows).
109| * **D-7 (section 7).**  `make -j8`, one make job, instead of a plain `make`.
110| * **D-8 (coordinator's L8 expectation).**  The measured red set also includes the 21 committed-side counterpart rows
111|   (all NULL by construction): 56, as `PRETABLE_L8.out` predicted.
112| * **D-9 (placement, observation).**  The block sits before `gate_offline.sh`'s compiler check, as specified.  On a host
113|   with no C compiler it reds via `gen_compiles` (B5's explicit red), and the gate's later "no C compiler" `gate_skip`
114|   then reports FAIL, not SKIP (`lib.sh`: a skip after failures is a FAIL).
115| * **D-10 (trees).**  The five peer files are uncommitted in GXEMUL-SEC and byte-identical in every build tree (already
116|   compiled into the old binaries); `rm src/cpus/*.o` recompiled `cpu_alpha` with the peer's `cpu_alpha_palcode.c` as it
117|   stands.  Both gates therefore measured the working tree, `gate_offline.sh`'s foreign hunks included.
118| * **C1 / C2:** filed outside T1 only (adjudication C1/C2); nothing here touches them.  The adjudication's corrections
119|   to PASS1_RULINGS (roster line) and CHECKS #4/#6/#7 are records work for the main loop.  CHECKS #6 is discharged by
120|   `BASELINE.out` section 3.
121| 
122| ## 8. Open questions for the main loop
123| 1. Is the post-edit v3 pre-fix run (D-4) acceptable beside the v1 pre-edit receipt?
124| 2. 123 individual identity checks (as amended) or one aggregated check that names any failing identity?  (Each adds
125|    one gate line; GATE 2 now prints 123 more.)
126| 3. The helper scripts (variant builder, runners, scorer) live only in the session scratchpad
127|    `t1/build/`.  Any `.py` copied under `regress/artifacts/` needs a `check_probe_wiring.py` MANIFEST line.  The diff
128|    files already specify every variant.
129| 4. The Fable stage is HELD (`fable5.HELD.txt`), so the rulings this build follows are provisional on their face.
~~~~

### 9.2 `SCORES.txt` -- the summary table (lines 12-30), then every run's MEASURED red set (each run's header line and its "measured red" line)
~~~~
 12| run  red/rows artifact                pred  match   ids once  role -- reason the red is the reason under test
 13| PRE   50/123  prefix_HEAD_v3.out      50    YES     123/123   (a) -- the HEAD blobs: the 24 repaired slots are NULL in BOTH artifacts (296 NULLs); fresh == committed holds
 14| FIX    0/123  fixed.out               0     YES     123/123   -- -- the fixed generator and the regenerated table (repo defaults, as gate 2 runs it): every row green
 15| L1    26/123  L1_headgen.out          26    YES     123/123   (b) gen site -- HEAD's generator re-emits NULL at the 24 slots; the committed (fixed) table stays green; cmp differs
 16| L2    26/123  L2_headtable.out        26    YES     123/123   (b) table site -- HEAD's table carries NULL at the 24 slots; the fresh (fixed) output stays green; cmp differs
 17| L3    64/123  L3_commentgen.out       64    YES     123/123   (c) measured -- comment-only generator source: no main(), the link fails -> compile, exit, stdout, count rows and every fresh row red
 18| L4    60/123  L4_commenttable.out     60    YES     123/123   (c) measured -- comment-only table: no initializer -> every committed-side row red; the generator side green
 19| L5    14/123  L5_v2nopcsync.out       14    YES     123/123   (d) -- grok_t1p1.txt:76's v2 -- the arm re-introduced under `&& no_pc_sync`: the 12 no-PC-sync repairs NULL, first at 416
 20| L6    14/123  L6_lehalf.out           14    YES     123/123   (d) -- the arm re-introduced on the LITTLE-endian half only (glm Q12:52): the 12 LE repairs NULL, BE repairs green
 21| L7     3/123  L7_v6halfword.out       3     YES     123/123   accept (R12) -- the `size > 0` in print_function_name -> `size > 1` (grok :80 / codex :130): 161/177 lose `_scaled`; word pins green; NOT silent -- see DUPNAMES.out
 22| L8    56/123  L8_allnull.out          56    YES     123/123   suppl. medium -- all-NULL initializer, structure kept (deepseek Q34:20): every committed NAME row and the count red, structure green
 23| L5b   30/123  L5b_codexnopcsync.out   30    YES     123/123   suppl. only -- NOT L5: codex_t1p1.txt:100's predicate (no_pc_sync alone, after the exclusions), first overall difference 256
 24| S1     3/123  S1_noearlyreturn.out    3     YES     123/123   suppl. B4 -- loadstore()'s kept early return deleted: 12 more blocks -> gen_count and fresh_lsn 210; every name pin green
 25| S2     1/123  S2_exit1.out            1     YES     123/123   suppl. B5 -- the generator exits 1 after printing the whole table: gen_exit red, nothing else
 26| S3    62/123  S3_emptyout.out         62    YES     123/123   suppl. B5 -- the generator returns before printing anything (exit 0): gen_stdout red, and every fresh row
 27| S4    60/123  S4_notable.out          60    YES     123/123   suppl. B5 -- TABLE names an absent file: committed_present 'absent' and every committed row red -- not a skip
 28| S5    64/123  S5_nogen.out            64    YES     123/123   suppl. B5 -- GEN names an absent file: gen_compiles 'no -- source absent', every generator and fresh row red -- not a skip
 29| 
 30| ALL RUNS: measured red set == predicted, the same 123 identities, each once, sentinel present: YES
  ...
 44| PRE  prefix_HEAD_v3.out  sentinel present  ROWS=123 FAIL=50
 45|     measured red: committed_nulls; committed_pin[24: 160 164 168 176 180 184 224 228 232 240 244 248 416 420 424 432 436 440 480 484 488 496 500 504]; fresh_nulls; fresh_pin[24: 160 164 168 176 180 184 224 228 232 240 244 248 416 420 424 432 436 440 480 484 488 496 500 504]
  ...
 51| FIX  fixed.out  sentinel present  ROWS=123 FAIL=0
 52|     measured red: (none)
 53| L1  L1_headgen.out  sentinel present  ROWS=123 FAIL=26
 54|     measured red: cmp_fresh_committed; fresh_nulls; fresh_pin[24: 160 164 168 176 180 184 224 228 232 240 244 248 416 420 424 432 436 440 480 484 488 496 500 504]
  ...
 59| L2  L2_headtable.out  sentinel present  ROWS=123 FAIL=26
 60|     measured red: cmp_fresh_committed; committed_nulls; committed_pin[24: 160 164 168 176 180 184 224 228 232 240 244 248 416 420 424 432 436 440 480 484 488 496 500 504]
  ...
 64| L3  L3_commentgen.out  sentinel present  ROWS=123 FAIL=64
 65|     measured red: cmp_fresh_committed; fresh_acc[9: 144 161 177 400 404 418 422 434 438]; fresh_cp[21: 128 132 136 148 152 192 196 200 208 212 216 384 388 392 408 448 452 456 464 468 472]; fresh_entries; fresh_inits; fresh_lsn; fresh_nulls; fresh_pin[24: 160 164 168 176 180 184 224 228 232 240 244 248 416 420 424 432 436 440 480 484 488 496 500 504]; fresh_present; gen_compiles; gen_count; gen_exit; gen_stdout
  ...
 79| L4  L4_commenttable.out  sentinel present  ROWS=123 FAIL=60
 80|     measured red: cmp_fresh_committed; committed_acc[9: 144 161 177 400 404 418 422 434 438]; committed_cp[21: 128 132 136 148 152 192 196 200 208 212 216 384 388 392 408 448 452 456 464 468 472]; committed_entries; committed_inits; committed_lsn; committed_nulls; committed_pin[24: 160 164 168 176 180 184 224 228 232 240 244 248 416 420 424 432 436 440 480 484 488 496 500 504]; committed_present
  ...
 87| L5  L5_v2nopcsync.out  sentinel present  ROWS=123 FAIL=14
 88|     measured red: cmp_fresh_committed; fresh_nulls; fresh_pin[12: 416 420 424 432 436 440 480 484 488 496 500 504]
  ...
 92| L6  L6_lehalf.out  sentinel present  ROWS=123 FAIL=14
 93|     measured red: cmp_fresh_committed; fresh_nulls; fresh_pin[12: 160 164 168 224 228 232 416 420 424 480 484 488]
  ...
 98| L7  L7_v6halfword.out  sentinel present  ROWS=123 FAIL=3
 99|     measured red: cmp_fresh_committed; fresh_acc[2: 161 177]
  ...
103| L8  L8_allnull.out  sentinel present  ROWS=123 FAIL=56
104|     measured red: cmp_fresh_committed; committed_acc[9: 144 161 177 400 404 418 422 434 438]; committed_cp[21: 128 132 136 148 152 192 196 200 208 212 216 384 388 392 408 448 452 456 464 468 472]; committed_nulls; committed_pin[24: 160 164 168 176 180 184 224 228 232 240 244 248 416 420 424 432 436 440 480 484 488 496 500 504]
  ...
108| L5b  L5b_codexnopcsync.out  sentinel present  ROWS=123 FAIL=30
109|     measured red: cmp_fresh_committed; fresh_acc[6: 400 404 418 422 434 438]; fresh_cp[10: 384 388 392 408 448 452 456 464 468 472]; fresh_nulls; fresh_pin[12: 416 420 424 432 436 440 480 484 488 496 500 504]
  ...
113| S1  S1_noearlyreturn.out  sentinel present  ROWS=123 FAIL=3
114|     measured red: cmp_fresh_committed; fresh_lsn; gen_count
  ...
118| S2  S2_exit1.out  sentinel present  ROWS=123 FAIL=1
119|     measured red: gen_exit
  ...
121| S3  S3_emptyout.out  sentinel present  ROWS=123 FAIL=62
122|     measured red: cmp_fresh_committed; fresh_acc[9: 144 161 177 400 404 418 422 434 438]; fresh_cp[21: 128 132 136 148 152 192 196 200 208 212 216 384 388 392 408 448 452 456 464 468 472]; fresh_entries; fresh_inits; fresh_lsn; fresh_nulls; fresh_pin[24: 160 164 168 176 180 184 224 228 232 240 244 248 416 420 424 432 436 440 480 484 488 496 500 504]; fresh_present; gen_count; gen_stdout
  ...
134| S4  S4_notable.out  sentinel present  ROWS=123 FAIL=60
135|     measured red: cmp_fresh_committed; committed_acc[9: 144 161 177 400 404 418 422 434 438]; committed_cp[21: 128 132 136 148 152 192 196 200 208 212 216 384 388 392 408 448 452 456 464 468 472]; committed_entries; committed_inits; committed_lsn; committed_nulls; committed_pin[24: 160 164 168 176 180 184 224 228 232 240 244 248 416 420 424 432 436 440 480 484 488 496 500 504]; committed_present
  ...
142| S5  S5_nogen.out  sentinel present  ROWS=123 FAIL=64
143|     measured red: cmp_fresh_committed; fresh_acc[9: 144 161 177 400 404 418 422 434 438]; fresh_cp[21: 128 132 136 148 152 192 196 200 208 212 216 384 388 392 408 448 452 456 464 468 472]; fresh_entries; fresh_inits; fresh_lsn; fresh_nulls; fresh_pin[24: 160 164 168 176 180 184 224 228 232 240 244 248 416 420 424 432 436 440 480 484 488 496 500 504]; fresh_present; gen_compiles; gen_count; gen_exit; gen_stdout
~~~~

### 9.3 `PRETABLE_v3.out` -- the PREDICTED red sets (section 4) and the changed rows' channels (section 5); written 10:02:21, before any v3 run
~~~~
 53| ## 4. Predicted red sets for driver v3 (rows red of 123)
 54|   PRE  (HEAD blobs via GEN/TABLE)  50   fresh_pin x24, committed_pin x24, fresh_nulls, committed_nulls
 55|   FIX  (repo defaults)              0
 56|   L1   26   fresh_pin x24, fresh_nulls, cmp_fresh_committed
 57|   L2   26   committed_pin x24, committed_nulls, cmp_fresh_committed
 58|   L3   64   gen_compiles gen_exit gen_stdout gen_count, all 59 fresh_* rows, cmp_fresh_committed
 59|   L4   60   all 59 committed_* rows, cmp_fresh_committed
 60|   L5   14   fresh_pin{416 420 424 432 436 440 480 484 488 496 500 504}, fresh_nulls (284), cmp
 61|   L6   14   fresh_pin{160 164 168 224 228 232 416 420 424 480 484 488}, fresh_nulls (284), cmp
 62|   L7    3   fresh_acc161, fresh_acc177, cmp
 63|   L8   56   committed_pin x24, committed_acc x9, committed_cp x21, committed_nulls (512), cmp
 64|   L5b  30   fresh_pin (the 12 no-PC-sync), fresh_acc{400 404 418 422 434 438}, fresh_cp{384 388 392 408 448 452 456
 65|             464 468 472}, fresh_nulls (392), cmp
 66|   S1    3   gen_count (210), fresh_lsn (210), cmp
 67|   S2    1   gen_exit (1)
 68|   S3   62   gen_stdout ("no -- stdout empty"), gen_count ("not reported"), all 59 fresh_* rows, cmp
 69|   S4   60   all 59 committed_* rows (committed_present "absent"), cmp ("committed table absent")
 70|   S5   64   as L3, with gen_compiles reading "no -- source absent"
 71| 
 72| ## 5. CHANNEL for the changed rows (the rest as PRETABLE.out section 5)
 73|   gen_exit     S2 (1); L3/S5 ("not run")            -- the exit status
 74|   gen_stdout   S3 ("no -- stdout empty"); L3/S5 ("not run")   -- stdout emptiness
 75|   identities   any deleted or renamed row: its identity's count 0 at the gate; a duplicated row: 2.  Not a table leg
 76|                (the gate pins it); checked by construction when the gate block is read, and by the green GATE 2 run.
~~~~

### 9.4 `PRETABLE.out` (2026-10-22 23:45, before the driver existed) -- section 2 CLAIM -> ROW (its section 5 CHANNEL list is in `brief2_FULL.md`; here the measured red sets in 9.2 show every row's red legs)
~~~~
 60| ## 2. CLAIM -> ROW, for every sentence the #569 comment in the generator will assert
 61| (the comment replaces :254-257; its sentences, as they will be written:)
 62|   C1 "no NULL arm for scaled byte accesses"                 -> A6 (24 pins, both artifacts) and A4 (NULL == 272)
 63|   C2 "A byte's scale factor is 1, so a scaled byte access   -> NO ROW: an architecture statement the offline detector
 64|       is the unscaled one"                                     cannot observe; its warrant is mc88100.txt:2960-2965 and
 65|                                                                :6458-6460 (scale factor one for byte), cited in the
 66|                                                                CHANGELOG/report, not in product code
 67|   C3 "print_function_name() already omits "_scaled" for     -> A6: every expected pin name lacks "_scaled" (a size-0
 68|       size 0"                                                  "_scaled" name reds all 24); A7 161/177: the size-1 EDGE
 69|                                                                keeps "_scaled" (L7 moves that edge)
 70|   C4 "these 24 slots name the unscaled byte handlers"       -> A6 by absolute equality; A7/A8 pin the same 12 names
 71|                                                                independently at index-32 (relative row NOT used, B2)
 72|   C5 "They were NULL"                                       -> historical; its rows are the clause-(a) reds:
 73|                                                                prefix_HEAD.out (A6 x48 and A4 x2 red) and BASELINE.out
 74|                                                                section 5 (24 of 24 NULL at HEAD)
 75|   C6 "which xmem_slow() calls unguarded and the ld/st       -> NO ROW in this detector: a guest-path consequence (B11);
 76|       decoder installs as ic->f (cpu_m88k_instr.c)"            source-established (CHECKS #3, cpu_m88k_instr.c :2395,
 77|                                                                :2426, :3622; cpu_dyntrans.c :1906); the rung-3 witness
 78|                                                                is BLOCKED (witness_attempt_20261022/WITNESS_ATTEMPT.md)
~~~~

### 9.6 The pre-fix and fixed receipts, and the key mtimes
`driver_v1/prefix_HEAD.meta` (whole):
~~~~
## prefix_HEAD run 2026-10-23 09:46:18 -0500  HEAD 5986c137d783b0d7b0104dbc6b652dfab781b7a7
driver    47086d1981f81ef1afcf2a9e01932e3c  (frozen copy: scratchpad t1/build/driver_v1.sh 47086d1981f81ef1afcf2a9e01932e3c)
generator bebaf43992929256de4f187e6b7c27b3  HEAD-blob bebaf43992929256de4f187e6b7c27b3
table     269e6e6f7b5ba4849202b61443bfb9af  HEAD-blob 269e6e6f7b5ba4849202b61443bfb9af
command   GEN= TABLE= /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/diff_m88k_loadstore_gen.sh > prefix_HEAD.out 2>&1
rc        1
summary   ROWS=122 FAIL=50  last line: M88KLS_DONE

~~~~
Key mtimes, the files' own:
~~~~
2026-10-23 09:46:19.436  driver_v1/prefix_HEAD.out -- v1 on the UNMODIFIED repository, repo defaults: ROWS=122 FAIL=50
2026-10-23 09:46:58.650  the generator EDITED
2026-10-23 09:47:51.562  the table REGENERATED
2026-10-23 09:59:58.756  the driver file = v3 (md5 cc2f3cf1)
2026-10-23 10:02:21.316  PRETABLE_v3.out (the v3 predictions)
2026-10-23 10:03:08.950  prefix_HEAD_v3.out -- v3 via GEN=/TABLE= on byte-exact HEAD blob copies: ROWS=123 FAIL=50
2026-10-23 10:03:13.525  the last of the 16 v3 runs
~~~~

### 9.7 How the shipped driver v3 differs from v1, which made the pre-edit-dated receipt
`driver_v1/RERUN_v2.txt` lines 1-4 (v1 -> v2 added 5 comment lines and nothing else):
~~~~
  1| # RERUN_v2.txt -- 2026-10-23 09:51:39 -0500
  2| # driver v1 md5 47086d1981f81ef1afcf2a9e01932e3c (every artifact in this dir)   driver v2 md5 302e6259dca9981362c50eec3caaed18 (the file to be committed)
  3| # v1 -> v2 diff: driver_v1_to_v2.diff -- 5 added line(s), 0 removed;
  4| #   added lines that are not comments: 0
~~~~
`driver_v2_to_v3.diff` (14 KB) is NOT inlined in this packet.  What it changes, by the drafter's reading and the
mechanical check S18(d): the header's CONTRACT paragraph is rewritten (all 24 floor; the consumer subset; the 54-pin
enumeration; the narrow-count wording; the NOT-OBSERVED list adds "the generated DEFINITIONS beyond their count");
`row()` gains a first IDENTITY argument and a fixed-width identity column; the spec block's class letters change F/E ->
R/N and four accept descriptions change -- the 54 index -> expected-name pairs are UNCHANGED; the `gen_stdout` row
(execution: stdout non-empty) is added; every literal row label becomes an identity (`gen_compiles`, `gen_exit`,
`gen_count`, `cmp_fresh_committed`, `<a>_present/_inits/_entries/_nulls/_lsn`, `<a>_pin<i>/_acc<i>/_cp<i>`).

### 9.11 `CLEARANCE.out` -- the clearance block (lines 22-36) and the in-tree regeneration (lines 38-42)
~~~~
 22|    est         part 1  cmp src/cpus/generate_m88k_loadstore.c   : CLEAN
 23|    est         part 1  cmp src/cpus/tmp_m88k_loadstore.c        : CLEAN
 24|    est         part 2  est/: source tree, part 2 N/A (no binary exists)
 25|    build       part 1  cmp src/cpus/generate_m88k_loadstore.c   : CLEAN
 26|    build       part 1  cmp src/cpus/tmp_m88k_loadstore.c        : CLEAN
 27|    build       part 2  [ gxemul -nt src/cpus/generate_m88k_loadstore.c ] : yes   (gxemul 2026-10-23 09:54:12.016, file 2026-10-23 09:53:36.707)
 28|    build       part 2  [ gxemul -nt src/cpus/tmp_m88k_loadstore.c ] : yes   (gxemul 2026-10-23 09:54:12.016, file 2026-10-23 09:53:53.585)
 29|    build-asan  part 1  cmp src/cpus/generate_m88k_loadstore.c   : CLEAN
 30|    build-asan  part 1  cmp src/cpus/tmp_m88k_loadstore.c        : CLEAN
 31|    build-asan  part 2  [ gxemul -nt src/cpus/generate_m88k_loadstore.c ] : yes   (gxemul 2026-10-23 10:06:40.775, file 2026-10-23 10:04:41.557)
 32|    build-asan  part 2  [ gxemul -nt src/cpus/tmp_m88k_loadstore.c ] : yes   (gxemul 2026-10-23 10:06:40.775, file 2026-10-23 10:05:37.884)
 33|    gxsec-build part 1  cmp src/cpus/generate_m88k_loadstore.c   : CLEAN
 34|    gxsec-build part 1  cmp src/cpus/tmp_m88k_loadstore.c        : CLEAN
 35|    gxsec-build part 2  [ gxemul -nt src/cpus/generate_m88k_loadstore.c ] : yes   (gxemul 2026-10-23 10:07:16.286, file 2026-10-23 10:06:47.242)
 36|    gxsec-build part 2  [ gxemul -nt src/cpus/tmp_m88k_loadstore.c ] : yes   (gxemul 2026-10-23 10:07:16.286, file 2026-10-23 10:07:02.262)
  ...
 38| ## did make regenerate the table IN-TREE? (dependency-driven: only when the generator binary or the template is
 39| ## newer -- here the generator source was newer, so its binary was rebuilt and the rule fired; shown, not assumed)
 40|    build       rule ran: 1 time(s) (log line 113)   generator stderr: ./generate_m88k_loadstore: generated_functions = 198
 41|    build-asan  rule ran: 1 time(s) (log line 113)   generator stderr: ./generate_m88k_loadstore: generated_functions = 198
 42|    gxsec-build rule ran: 1 time(s) (log line 112)   generator stderr: ./generate_m88k_loadstore: generated_functions = 198
~~~~

### 9.12 and 9.13 -- GATE 2 (`GATE2_tail.out`) and GATE 11 (`GATE11_tail.out`), each run once, alone: run records, the block's three aggregate checks, the verdict lines
~~~~
 10| gate 2: start 2026-10-23 10:09:00 -0500; HEAD ref: refs/heads/main; LOGDIR=/tmp/gxregress (lib.sh default)
 11| concurrent jobs at start: 0
 12| gate 2: rc=0  end 2026-10-23 10:11:51 -0500  wall=171s  lines 2596
  ...
143|   ok   m88k loadstore generator: row failures               0
144|   ok   m88k loadstore generator: rows run (the denominator is the pin) 123
145|   ok   m88k loadstore generator: completion sentinel        1
  ...
272| offline-differential: PASS (502 checks)
  ...  (GATE11_tail.out)
  9| gate 11: start 2026-10-23 10:12:46 -0500; HEAD ref: refs/heads/main; LOGDIR=/tmp/gxregress (lib.sh default)
 10| concurrent jobs at start: 0
 11| gate 11: rc=0  end 2026-10-23 10:16:53 -0500  wall=247s  lines 359
  ...
132| gate 11: m88k rounding mode (#298): PASS (111 checks)
~~~~

---

## 11. QUESTIONS -- VERDICT LINE FIRST (format in section 0)

**Q3 -- THE LEGS: do the measurements say what the records say they say?**

(a) Do the measured red sets equal PRETABLE_v3 section 4's predictions ROW BY ROW?  SCORES.txt's per-run "measured red"
lines are the measured side.  Walk all 16 runs.

(b) Is each red for the reason under test (SCORES.txt's got= values -- e.g. L3's `gen_compiles` reads "no -- the compile
or link failed", L5's `fresh_pin416` reads `NULL`)?

(c) The floor, clause by clause, each with its named receipt (R1-R4): (a) pre-fix red -- PRE; (b) verbatim
reinstatement at BOTH fixed sites -- L1 (generator), L2 (table); (c) null media -- L3, L4, recorded in R2's
"(c): measured at" form; (d) the nulled repair -- L5, L6.  Is each discharged?  Does any clause rest on a SUPPLEMENTARY
leg (L8, L5b, S1-S5)?

(d) Answer P5 against R17 -- note its sentence "a retrospective run against a reconstructed pre-fix tree supplies a red
but not an authentic pre-edit DATE", and its bound "one measured red per oracle a ROW CONSUMES".

**Q4 -- WIRING, CLEARANCE, GATES**

(a) The GATE 2 block (7.3): its placement (after `#375`, before `b1w`), the `-x` check, `row failures == 0` and
`rows run == 123` by EQUALITY, the sentinel, the 123 identity pins -- is anything wrong or unsupported?  Answer P3 and
P4.  The new file must be committed mode 100755 (S19): what, at landing, verifies that it was?

(b) Does the staged `gate_offline.sh` carry ONLY this round's hunk?  (7.3: one hunk, +45 -0; the builder's
`staged/insert_HEAD.diff` and `staged/insert_WT.diff` differ only in their two `---`/`+++` header lines.)

(c) The four-tree clearance (9.11): part 1 on all four trees, part 2 on the three build trees, `est/: source tree, part 2
N/A`; the in-tree regeneration fired once per build tree.  Sound?

(d) GATE 2 `PASS (502 checks)` and GATE 11 `PASS (111 checks)` (9.12, 9.13): answer P2 -- which tree do these results
describe, and what may the record and the commit message claim?  (BUILD_REPORT D-10.)

(e) Answer P7.  And S20: is anything owed, or worth FILING, because nothing outside the GATE 2 block notices if that
block, or the driver's execution, goes away?

**Q5 -- RECORDS, AND ANYTHING ELSE**

(a) What must the CHANGELOG `#569` block, OUTSTANDING_BUGS.md (lines 28-29 and 25260-25263) and the ledger row say at
landing?  At least: the witness term `detector:regress/diff_m88k_loadstore_gen.sh` with the BLOCKED rung-3 attempt named
(R18); the two filed rows `m88kxmemaddrovl` and `m88klepsrbo` (S16); a state_note no longer saying "DISPUTED"; the
witness record and the round's artifacts directory TRACKED.  Check also what this packet shows: the ledger row has NO
`entries` field yet (the pass-1 seats, the adjudication and their directories are unrecorded); the Fable stage is HELD
(`fable5.HELD.txt` carries its hold question), and HEAD's newest round `#568` landed "held for Fable" (section 4, part 1,
`2ca79b90`); `PASS1_RULINGS.md` lines 3-11 still carry the pre-adjudication roster -- "3 of 4 rostered seats", "NOT FIRED
by owner roster: agy, kimi, deepseek, minimax, opus5", "Every seat answered; no seat failure" -- although DeepSeek
answered on 2026-10-23 and Argon was a seat failure (section 3.1; the adjudication asked for that replacement at
`adj/codex_t1p1adj.txt:73`).  What else does the landing owe?

(b) The builder's disagreements D-1..D-10 and open questions 1-4 (BUILD_REPORT sections 7-8, inlined in 9.1): which need
a disposition, and what should it be?

(c) **The standing licence.**  If, while verifying a claim, you found something ELSE -- say so, with the file and the
grep anchor (or line) that settles it.

---

