# PASS-2 DIFF REVIEW -- round #570, ledger row `m88kbuserrregs` (research item T36) -- GXemul hardened fork
**Brief v1, FULL form (for seats that can read files; the diffs, the measured table, the pre-table check and the
detector are inlined whole).**  Drafted 2026-10-24 against HEAD `7fca7187` plus the round's UNCOMMITTED working-tree
edits.  Built from `GXEMUL-SEC/tools/BRIEF_TEMPLATE.md` (the WORKING-TREE copy, which differs from HEAD's -- section 4,
part 7).  Companion: `brief2_COMPACT.md` for the packet-fed seats -- identical premises and questions, evidence
condensed where it says so.

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

*This campaign's own record of premises stated as fact and then refuted: pass 1's adjudicator withdrew a main-loop
finding (C5) whose enclosing function had not been read; and the builder found the adjudicated rationale for the
include's position ("upstream's placement") false against the port source (section 6, P3).  Check this brief the same
way.*

---

## 0. What this is, what this pass is for, and how to answer

**The project.**  GXemul is a computer-architecture emulator: a developer tool that runs legacy operating systems
inside a software sandbox.  This fork is a hardening effort -- ordinary software-correctness work on the emulator's
own C code and the regression tests that keep each correction fixed.  The *guest* is a program or OS running INSIDE
the emulator; the *host* is the emulator process.  A *variant* (the records also say *mutant*) is a deliberately
altered copy of the code, used to measure whether a regression test notices the alteration (standard mutation
testing); a *leg* is one such measurement, named `L<n>`.

**The defect, in one paragraph.**  On the two 88K machines this tree models with MC88200 CMMUs (MVME187 and
LUNA-88K), when a guest access reaches a device that REFUSES it, the emulator raised the CPU's access exception but
left the CMMU's P-bus fault status register (PFSR, offset 0x108) and P-bus fault address register (PFAR, offset 0x10c)
holding whatever they held before, so a guest fault handler that reads them to classify the fault read stale values.
And at one LUNA-88K address (0x3ffffff0) the board device wrote PFSR itself and then SERVED the access: no exception,
no PFAR.  A WRONG-RESULT defect; the fixed code ends no host process anywhere.

**The fix, in one paragraph.**  Four product files (`src/cpus/memory_rw.c`, `src/cpus/cpu_m88k.c`,
`src/devices/dev_luna88k.c`, `src/devices/dev_m8820x.c`), byte-identical in `est/`.  `memory_rw.c`'s MEM_M88K
refused-device arm now selects the faulting side's CMMU by `cache`, and if that pointer is not NULL writes
PFSR = `CMMU_PFSR_BERROR << 16` and PFAR = `(uint32_t) orig_paddr`, before the unchanged exception; `cpu_m88k.c`
includes the header that defines those three names; `dev_luna88k.c`'s 0x3ffffff0 case returns 0 so the access is
refused through that arm; `dev_m8820x.c` gets comment-only corrections.  The detector is the rung-3 witness promoted
to 31 rows and wired into gate 14.

**This pass.**  PASS 2 on the ACTUAL DIFF and its MEASURED detector, against the pass-1 rulings AS ADJUDICATED
(`pass1_20261023/PASS1_RULINGS.md`: section E, GPT-6 Astra's adjudication, rules wherever it differs from A-D) and the
builder rulings that bound the build (`pass1_20261023/BUILD_SPEC.md` sections 10 and 11).  The builder (Opus 5.5,
a sub-agent) built the witness, this diff and the detector; it is not on this panel.  Roster at drafting time
(`pass2_20261023/roster_NOT_FIRED.txt`): GLM 5.3 and DeepSeek (packet-fed, COMPACT form) and Grok 4.7 (file-reading,
this form) review; Gemini 4 Argon is NOT FIRED (a transport failure -- a seat failure, not agreement); Fable 5.1 is
HELD by the owner with a filed hold question; agy, kimi, minimax and Opus are deliberately not fired by the owner's
roster; GPT-6 Astra adjudicates this pass's findings afterwards.

**Hard limits.**  READ-ONLY.  Do not build, run, copy or modify anything in the repository.  Nobody is asked to write
code, a guest program or a code variant.  The variants below are the records' own, described by leg id and the
records' one-line description; where a question needs a construction it asks you to CLASSIFY, never to build.

**Reading scope (seats that can read files).**  `GXEMUL-SEC/src/` and the top-level `GXEMUL-SEC/regress/*.py`,
`*.sh` and `*.c`.  **Do not read `GXEMUL-SEC/regress/artifacts/` or `GXEMUL-SEC/tools/pipeline/ledger.json`** --
everything this brief relies on from them is inlined below, and their paths are given so the record can be checked
later.  The detector under review is the UNTRACKED `regress/m88k_buserr_probe.py`, md5
`d57c12ab7ade903946c7d80a8e153ab7`; it is inlined WHOLE (sections 2.4 and 2.5) from the frozen copy the variant table
ran, which is byte-identical (`cmp` at drafting time).  If your md5 of the working file differs, say so and review the
inlined bytes.  Files outside the repository are named by ABSOLUTE path only.

**The working tree is NOT clean, and most of what is dirty is NOT this round** (section 4, part 7 lists every file).
This round's: the four product files; `regress/gate_arm.sh` (+31); 11 of the 26 added lines in
`tools/pipeline/check_probe_wiring.py`; the untracked `regress/m88k_buserr_probe.py`; the untracked
`regress/artifacts/m88kbuserrregs/`.  NOT this round (a peer's uncommitted work and pending records): `src/cpus/cpu_alpha_palcode.c`,
`src/devices/dev_lca.c`, `src/devices/dev_pcc2.c`, `src/devices/dev_sh4.c`, `src/include/thirdparty/mvme_pcctworeg.h`,
`regress/diff_wdc_identify.c`, `regress/gate_offline.sh`, `regress/gate_sh_rounding.sh`,
`regress/gdrom_default_probe.py`, `regress/sh4_chcr_probe.py`, `regress/wdc_addtoinbuf_probe.py`,
`regress/artifacts/recordfix_20261002/chk_hrec.py.txt`, `tools/BRIEF_TEMPLATE.md`, `tools/CLAUDE.md`,
`tools/PIPELINE.md`, `tools/adjudicate.sh`, `tools/panel.sh`, `tools/pipeline/ledger.json`, `tools/pipeline/matrix.html`,
the other 15 added lines of `check_probe_wiring.py`, and every other untracked file section 4 part 7 lists (e.g.
`regress/lca_isaphys_probe.py`, `tools/pipeline/check_fix_seats.py`).  Do not attribute any of them to #570.  **Line numbers below are the working tree's** unless marked HEAD; `src/cpus/cpu_m88k.c` is +4
relative to HEAD below its line 53 (the include); the other three product files' cited lines are unchanged above
their edits.

**Answer format -- VERDICT LINE FIRST:**
~~~~
VERDICT: SHIP | SHIP WITH CHANGES | DO NOT SHIP -- <one line>
Q1: <one line>   Q2: <one line>   Q3: <one line>   Q4: <one line>
~~~~
Then one section per question.  Number your findings F1, F2, ...; mark each claim READ (you opened the source),
DERIVED (from this packet) or NOT CHECKABLE; cite premises by number (S1.., P1..); grade any defect L1 / L2 / L3 / L4
(section 7, R16) and say whether it is a floor breach.

---

## 1. THE DIFF -- every file the round changes, and how this packet shows it

The template's pass-2 item: the numstat for the round's files, each marked.  **This drafter may not run `git diff`**,
so the counts are a plain `diff(1)` of `git show HEAD:<file>` against the working file (section 4, part 6).

| + | - | file | shown |
|---|---|---|---|
| 4 | 0 | `src/cpus/cpu_m88k.c` | INLINED whole, 1.1 |
| 24 | 5 | `src/cpus/memory_rw.c` | INLINED whole, 1.1; the region with its control flow, 1.4 |
| 7 | 3 | `src/devices/dev_luna88k.c` | INLINED whole, 1.1; the function's exits, 1.4 |
| 25 | 25 | `src/devices/dev_m8820x.c` | INLINED whole, 1.1 (comment-only; object byte-identical, S21) |
| 31 | 0 | `regress/gate_arm.sh` | INLINED whole, 1.2 (working tree == the staged HEAD-based copy, md5 `5ee94e61`) |
| 11 (of 26) | 0 | `tools/pipeline/check_probe_wiring.py` | #570's 11 lines INLINED, 1.3; the other 15 are a peer's -- NOT SHOWN, not this round |
| 836 | 0 | `regress/m88k_buserr_probe.py` (new, untracked) | INLINED whole, 2.4-2.5 |
| -- | -- | `regress/artifacts/m88kbuserrregs/` (new, untracked, 233 files) | evidence, not product: the load-bearing files are INLINED in section 3; the 20 variant source files (`L*.diff`) are NOT SHOWN by design -- each leg is described by id |
| -- | -- | `CHANGELOG.md`, `OUTSTANDING_BUGS.md`, `tools/pipeline/ledger.json` | NOT YET WRITTEN for #570 (Q3 asks what they must say) |

### 1.1 The four product files -- `regress/artifacts/m88kbuserrregs/table1_20261023/fix570.diff`, VERBATIM
*(Regenerated at drafting time from `git show HEAD:<file>` against the working file: byte-identical to the artifact.)*
~~~~
--- HEAD:src/cpus/cpu_m88k.c
+++ WT:src/cpus/cpu_m88k.c
@@ -51,6 +51,10 @@
 #include "symbol.h"
 
 #include "thirdparty/m8820x_pte.h"
+/*  #570: memory_rw.c's m88k refused-device arm, compiled into this unit through
+    tmp_m88k_tail.c, uses CMMU_PFSR, CMMU_PFAR and CMMU_PFSR_BERROR, which are
+    defined only in m8820x.h; upstream adds the same include to this file.  */
+#include "thirdparty/m8820x.h"
 #include "thirdparty/m88k_dmt.h"
 #include "thirdparty/mvmeprom.h"
 
--- HEAD:src/cpus/memory_rw.c
+++ WT:src/cpus/memory_rw.c
@@ -612,11 +612,30 @@
 					    0, vaddr, 0, 0, 0, 0);
 #endif
 #ifdef MEM_M88K
-					/*  TODO: This is enough for
-					    OpenBSD/mvme88k's badaddr()
-					    implementation... but the
-					    faulting address should probably
-					    be included somewhere too!  */
+					/*  #570: record the bus error in the
+					    faulting side's CMMU first: PFSR =
+					    BERROR << 16 (the field OpenBSD/mvme88k's
+					    trap.c extracts) and PFAR = orig_paddr,
+					    the PHYSICAL address saved before paddr
+					    was made device-relative.  cmmu[0] is the
+					    instruction CMMU, cmmu[1] the data CMMU
+					    (memory_m88k.c's index); the other CMMU
+					    is not written.  A cpu without a CMMU
+					    gets no write and still takes the
+					    exception.  NO_EXCEPTIONS callers (the
+					    debugger) never get here: the test above
+					    keeps them out.  */
+					{
+						struct m8820x_cmmu *cmmu =
+						    cpu->cd.m88k.cmmu[cache ==
+						    CACHE_INSTRUCTION ? 0 : 1];
+						if (cmmu != NULL) {
+							cmmu->reg[CMMU_PFSR] =
+							    CMMU_PFSR_BERROR << 16;
+							cmmu->reg[CMMU_PFAR] =
+							    (uint32_t) orig_paddr;
+						}
+					}
 					m88k_exception(cpu, cache == CACHE_INSTRUCTION
 					    ? M88K_EXCEPTION_INSTRUCTION_ACCESS
 					    : M88K_EXCEPTION_DATA_ACCESS, 0);
--- HEAD:src/devices/dev_luna88k.c
+++ WT:src/devices/dev_luna88k.c
@@ -622,9 +622,13 @@
 	switch (addr) {
 
 	case 0x3ffffff0:
-		/*  Accessed by OpenBSD/luna88k to trigger an illegal address  */
-		cpu->cd.m88k.cmmu[1]->reg[CMMU_PFSR] = CMMU_PFSR_BERROR << 16;
-		break;
+		/*  Accessed by OpenBSD/luna88k to trigger an illegal address.
+		    #570: refuse it.  memory_rw.c's refused-device arm then
+		    raises the access exception and writes PFSR and PFAR (for a
+		    load or store, in the data CMMU); this case used to write
+		    cmmu[1]'s PFSR only and serve 0.  The case is kept: without
+		    it the access would reach default:, which stops the cpu.  */
+		return 0;
 
 	case PROM_ADDR:		/*  0x41000000  */
 		/*  OpenBSD/luna88k write here during boot. Ignore for now. (?)  */
--- HEAD:src/devices/dev_m8820x.c
+++ WT:src/devices/dev_m8820x.c
@@ -290,13 +290,13 @@
 			/*  #433: ignoring a guest write to SSR corrupts nothing the model
 			    maintains -- but the first version of this comment gave a WRONG
 			    REASON, saying SSR is "written by the MODEL".  Measured: NOTHING
-			    in the tree ever writes reg[CMMU_SSR]; the model writes only PFSR
-			    and PFAR (memory_m88k.c:382-405).  The right reason is stronger:
-			    SSR reads as zero, V-bit clear, so DROPPING the write is what makes
-			    the command arm's own argument true -- if a guest could store here
-			    it could set the V bit, and a dropped PROBE would then read back a
-			    plausible-looking VALID translation instead of a deterministic
-			    miss.  The two decisions are coupled, and row D10 pins them.  */
+			    in the tree ever writes reg[CMMU_SSR]; the model writes only PFSR and
+			    PFAR (memory_m88k.c:382-405 and, since #570, memory_rw.c's refused-device
+			    arm).  The right reason is stronger: SSR reads as zero, V-bit clear, so
+			    DROPPING the write is what makes the command arm's own argument true --
+			    if a guest could store here it could set the V bit, and a dropped PROBE
+			    would then read back a plausible-looking VALID translation instead of a
+			    deterministic miss.  The two decisions are coupled, and row D10 pins them.  */
 			m8820x_unimplemented(d, "write to CMMU_SSR");
 		}
 		break;
@@ -323,10 +323,10 @@
 	 *    PFSR, PFAR   no translation consumer at all.  m88k_translate_v2p never reads
 	 *                 them; they are status OUTPUTS.  The strongest evidence in the
 	 *                 round is that THE MODEL ITSELF already relies on this: the fault
-	 *                 path writes PFSR (memory_m88k.c:382-384, dev_luna88k.c:614) and
-	 *                 PFAR (memory_m88k.c:399,405 -- TWO DISCRETE LINES, and the file has
-	 *                 to be named again: a bare ":399-405" after a dev_luna88k.c citation
-	 *                 reads as dev_luna88k.c:399-405, which is a keyboard scancode switch)
+	 *                 path writes PFSR (memory_m88k.c:382-384; #570: and memory_rw.c's arm -- no
+	 *                 longer dev_luna88k.c) and PFAR (memory_m88k.c:399,405 -- TWO DISCRETE LINES,
+	 *                 the file named again because a bare ":399-405" after a dev_luna88k.c
+	 *                 citation read as a keyboard scancode switch; #570: and memory_rw.c's arm)
 	 *                 DIRECTLY through reg[], with no purge, ~10^5
 	 *                 times per boot -- against 2 guest writes per boot through this
 	 *                 handler.  If a PFSR write owed a purge the model would already
@@ -450,11 +450,11 @@
 		 *  
 		 *  AN EARLIER VERSION OF THIS SENTENCE ALSO CLAIMED the guest's PFSR reads
 		 *  would return zero, and a pass-2 seat showed that is FALSE: the fault path
-		 *  writes PFSR DIRECTLY through reg[] at memory_m88k.c:382-384, never through
-		 *  this handler, so dropping the handler's store would not touch it at all.
-		 *  The SAR consequence stands on its own; the PFSR one was reasoning by
-		 *  analogy from the register beside it.  Removing a purge and removing a
-		 *  store are different changes and only the first is argued for here.
+		 *  writes PFSR DIRECTLY through reg[] at memory_m88k.c:382-384 (and, since #570, in
+		 *  memory_rw.c's refused-device arm), never through this handler, so dropping its
+		 *  store would not touch it at all.  The SAR consequence stands on its own; the PFSR
+		 *  one was reasoning by analogy from the register beside it.  Removing a purge and
+		 *  removing a store are different changes and only the first is argued for here.
 		 */
 		if (writeflag == MEM_WRITE)
 			regs[relative_addr / sizeof(uint32_t)] = idata;
@@ -495,15 +495,15 @@
 		 *  exit(1), so an ordinary guest LOAD of an unmodelled register terminated the
 		 *  host process -- measured at 1007 of 1024 offsets on a read.
 		 *
-		 *  The MMU objection to continuing does not apply here, and that is a measured
-		 *  fact rather than a hope: every register the emulator's own translation
-		 *  consults -- SAPR and UAPR read at memory_m88k.c:135,137, PFSR and PFAR
-		 *  written at :382-405 -- is a HANDLED case label above.  Nothing reaching this
-		 *  arm can alter what the emulator translates.  The defined-but-unhandled
-		 *  registers are all cache diagnostics (CDP0-3, CTP0-3, and the 88204-only
-		 *  CSSP1-3) against a model that has no cache -- and the neighbouring CSSP0 arm
-		 *  ALREADY answers exactly this way, silently, on a path a real boot exercises
-		 *  1024 times.  Continuing here is the same policy, said out loud once.
+		 *  The MMU objection to continuing does not apply here, and that is a measured fact
+		 *  rather than a hope: every register the emulator's own translation consults --
+		 *  SAPR and UAPR read at memory_m88k.c:135,137, PFSR and PFAR written at :382-405
+		 *  and, since #570, in memory_rw.c's refused-device arm -- is a HANDLED case label
+		 *  above.  Nothing reaching this arm can alter what the emulator translates.  The
+		 *  defined-but-unhandled registers are all cache diagnostics (CDP0-3, CTP0-3, and
+		 *  the 88204-only CSSP1-3) against a model that has no cache -- and the neighbouring
+		 *  CSSP0 arm ALREADY answers exactly this way, silently, on a path a real boot
+		 *  exercises 1024 times.  Continuing here is the same policy, said out loud once.
 		 *
 		 *  On a read the caller gets the regs[] value fetched above, which is zero for
 		 *  anything never stored; a write is dropped rather than stored, because
~~~~

### 1.2 `regress/gate_arm.sh` -- the gate-14 block, VERBATIM (`table1_20261023/staged/gate_arm.staged.diff`)
*(HEAD's file against the staged copy built from the HEAD blob; the working-tree file is byte-identical to that staged
copy.  The insertion sits directly after `#568`'s block.)*
~~~~
--- /c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/t36/build/wiring/gate_arm.HEAD.sh	2026-10-23 23:16:01.380828600 -0500
+++ /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/m88kbuserrregs/table1_20261023/staged/gate_arm.sh	2026-10-23 23:16:40.514026700 -0500
@@ -1913,6 +1913,37 @@
 fi
 
 
+#  ------------------------------------------------------------ m88kbuserrregs (#570)
+#  A REFUSED m88k device access -- a device CLAIMS it and returns 0 with the cpu still running -- now records its
+#  bus error in the faulting side's CMMU (memory_rw.c's refused-device arm: PFSR = BERROR << 16, PFAR = the physical
+#  address), and luna-88k's 0x3ffffff0 probe case is refused through that arm instead of being served 0.  The
+#  rung-3 witness (regress/artifacts/m88kbuserrregs/witness_20261023/, 16/24 on HEAD) is NOT run here; this is its
+#  detector: 31 rows, the witness's 24 plus the instruction label (ifetch x4), a NO_EXCEPTIONS caller (dbg noexc)
+#  and a CMMU-less cpu (null surv, null route; mvme187 -n 2).  Needs only the binary: mvme187 -M 64 [-n 2] and
+#  luna-88k, each with a 4-byte dummy image at 0x10000 -- no PROM, no rig image.  Kill table:
+#  regress/artifacts/m88kbuserrregs/table1_20261023/ (SCORES.txt).  Like #568's block above, it runs only if none
+#  of this gate's eleven earlier skip points fired (the probe header names them).
+M88KBELOG=$LOGDIR/m88k_buserr.log
+python3 -u m88k_buserr_probe.py "$PMAX" gate > "$M88KBELOG" 2>&1 || true
+if ! grep -q "M88K_BUSERR_PROBE_DONE" "$M88KBELOG"; then
+    check "m88k buserr probe completed" "no" "yes"
+else
+    check "m88k buserr probe completed" "yes" "yes"
+    check "m88k buserr sentinel once" "$(grep -c '^M88K_BUSERR_PROBE_DONE$' "$M88KBELOG")" "1"
+    mbres=$(sed -n 's/^M88K_BUSERR_RESULT=//p' "$M88KBELOG")
+    check "m88k_buserr rows run"     "${mbres#*/}" 31
+    check "m88k_buserr rows correct" "${mbres%/*}" "31"
+    check "m88k buserr controls" "$(grep -c '^M88K_BUSERR_CONTROL=OK$' "$M88KBELOG")" "1"
+    check "m88k buserr symptom absent" "$(grep -c '^M88K_BUSERR_SYMPTOM=ABSENT$' "$M88KBELOG")" "1"
+    for v in "neg apparatus" "mv devsig" "mv cmmu rt" "ok route" "ok regs" "uld route" "uld pfsr" "uld pfar" "uld icmmu" "ust route" "ust pfsr" "ust pfar" "ust icmmu" "vme route" "vme pfsr" "vme pfar" "vme icmmu" "luna devsig" "luna cmmu rt" "luna route" "luna pfsr" "luna pfar" "luna icmmu" "ifetch route" "ifetch pfsr" "ifetch pfar" "ifetch dcmmu" "dbg noexc" "null surv" "null route" "unasm"; do
+        check "m88k buserr row: $v" "$(count "$M88KBELOG" "^$v  .*ok$")" "1"
+    done
+    check "m88k buserr rows emitted" "$(( $(count "$M88KBELOG" " ok$") + $(count "$M88KBELOG" " FAIL$") ))" "31"
+    check "m88k buserr rows green"   "$(count "$M88KBELOG" " ok$")"   "31"
+    check "m88k buserr rows red"     "$(count "$M88KBELOG" " FAIL$")" "0"
+fi
+
+
 #  ------------------------------------------------------------ hpcmipsctor (#444) + #536
 #  Three of eight advertised hpcmips subtypes SIGABRTed during construction (#444).  Its rung-2
 #  detector (~8 s, no rig image) shipped EXEMPT for want of a construction gate; #536 wires it here.
~~~~
For comparison, `#568`'s block immediately above it (lines 1887-1913, identical at HEAD and in the working tree;
VERBATIM, read from the staged copy):
~~~~
#  ------------------------------------------------------------ vmedefaultkill (#568)
#  dev_vme.c's default: ended the emulator (exit(1), announced only by debug() -- silent while
#  free-running) on any VME2 offset the switch did not name.  Now: the 26 header-named registers
#  the model does not implement DECLINE (reads served the preloaded word, writes dropped, one
#  latched fatal() per register); every other unmatched offset returns 0, and for a guest data load
#  or store memory_rw raises the m88k data-access exception.  The rung-3 witness
#  (regress/artifacts/vmedefaultkill/witness_20261020/, 7 of 7 guest sites rc 1 on 5dbc000e) is NOT
#  run here; this is its detector.  Needs only the binary: the probe constructs mvme88k/mvme187 with
#  -M 64 and a 4-byte dummy image at 0x10000 -- no PROM image.  Kill tables:
#  regress/artifacts/vmedefaultkill/killtable1_20261020/ (rev 2) and killtable2_20261021/ (rev 3).
VMEDLOG=$LOGDIR/vme_default.log
python3 -u vme_default_probe.py "$PMAX" gate > "$VMEDLOG" 2>&1 || true
if ! grep -q "VME_DEFAULT_PROBE_DONE" "$VMEDLOG"; then
    check "vme default probe completed" "no" "yes"
else
    check "vme default probe completed" "yes" "yes"
    vres=$(sed -n 's/^VME_DEFAULT_RESULT=//p' "$VMEDLOG")
    check "vme_default rows run"     "${vres#*/}" 38
    check "vme_default rows correct" "${vres%/*}" "38"
    check "vme default controls" "$(grep -c '^VME_DEFAULT_CONTROL=OK$' "$VMEDLOG")" "1"
    for v in "neg apparatus" "session" "live" "vbr reset" "t1cmp rt" "cased census" "free ctl" "free quiet" "free neg ctl" "tctl rt" "vbr rt" "t1count inc" "cased wr" "p2 rd census" "p2 wr census" "p2 ld widths" "p2 st widths" "p2 ann rd" "p2 ann rd 2" "p2 ann wr" "p2 ann wr 2" "p2 nw rd" "p2 nw wr" "p2 nw rd 2" "p2 nw wr 2" "p2 zero wr" "p1 fault lo" "p1 fault hi" "p1 fault mid" "p1 fault wr" "p1 p2 edge" "p3 interim" "p2 int byte" "p2 int half" "p1 census" "p1 widths" "p1 quiet" "unasm"; do
        check "vme default row: $v" "$(count "$VMEDLOG" "^$v  .*ok$")" "1"
    done
    check "vme default rows emitted" "$(( $(count "$VMEDLOG" " ok$") + $(count "$VMEDLOG" " FAIL$") ))" "38"
    check "vme default rows green"   "$(count "$VMEDLOG" " ok$")"   "38"
    check "vme default rows red"     "$(count "$VMEDLOG" " FAIL$")" "0"
fi
~~~~
And the gate library's two helpers the block uses (`regress/lib.sh`, HEAD): `check` is string equality, `count` is
`grep -ac`:
~~~~
   80| check() {
   81|     _checks=$((_checks+1))
   82|     if [ "$2" = "$3" ]; then
   83|         printf "  ${C_OK}ok${C_OFF}   %-52s %s\n" "$1" "$2"
   84|     else
   85|         printf "  ${C_BAD}FAIL${C_OFF} %-52s got=%s want=%s\n" "$1" "$2" "$3"
   86|         _fails=$((_fails+1))
   87|     fi
   88| }
  326| count() {
  327|     [ -f "$1" ] || { echo 0; return; }
  328|     local c
  329|     c=$(grep -ac -- "$2" "$1" 2>/dev/null)
  330|     echo "${c:-0}"
  331| }
~~~~
The eleven earlier skip points of gate 14, derived at drafting time by
`grep -n -e gate_skip -e need_exec regress/gate_arm.sh` (identical in HEAD and the working tree, all above the
insertion at line 1916):
~~~~
84:need_exec "$PMAX"
85:command -v python3 >/dev/null || gate_skip "python3 not available"
93:" "$STUB" || gate_skip "could not write the load stub"
105:    gate_skip "probe did not complete"
389:    gate_skip "idle probe did not complete"
430:    gate_skip "memcpy probe did not complete"
515:    gate_skip "strlen probe did not complete"
638:    gate_skip "writeback probe did not complete"
695:    gate_skip "bdt probe did not complete"
816:    gate_skip "fold-marker probe did not complete"
949:    gate_skip "endian probe did not complete"
~~~~

### 1.3 `tools/pipeline/check_probe_wiring.py` -- #570's two MANIFEST entries, VERBATIM (`table1_20261023/staged/check_probe_wiring.staged.diff`)
*(HEAD's file against the staged copy built from the HEAD blob.  The same 11 lines are in the working-tree file, which
also carries a peer's 15 lines in two other hunks -- not shown.)*
~~~~
--- /c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/t36/build/wiring/check_probe_wiring.HEAD.py.txt	2026-10-23 23:16:01.415835300 -0500
+++ /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/m88kbuserrregs/table1_20261023/staged/check_probe_wiring.py.txt	2026-10-23 23:16:40.522621100 -0500
@@ -3204,6 +3204,17 @@
         (CLASS_RESEARCH, "argonlate fhfp1 check: the copy of tools/pipeline/stage_tokens.py (blob identical at 5dbc000e and 1a59a47e) that the measurement scripts here import from st/"),
     "artifacts/fableheldform/argonlate_20261020/st/check_stage_panels.py":
         (CLASS_RESEARCH, "argonlate fhfp1 check: the copy of tools/pipeline/check_stage_panels.py (blob identical at 5dbc000e and 1a59a47e) that the section-H simulations here ran"),
+    #  #570 m88kbuserrregs (a refused m88k device access records its bus error in the faulting side's CMMU): the
+    #  gated detector and the rung-3 witness of regress/artifacts/m88kbuserrregs/.  The kill table's frozen
+    #  instrument and drivers are kept as *.py.txt / *.sh.txt, outside this checker's domain.
+    "m88k_buserr_probe.py":
+        (CLASS_DETECTOR, "#570 m88kbuserrregs: 31 rows on unmodified -E mvme88k -e mvme187 -M 64 [-n 2] and -E luna88k -e "
+                         "luna-88k (rev 2); gated in gate_arm.sh (gate 14) under the stem m88k_buserr, pinned at 31; kill "
+                         "table artifacts/m88kbuserrregs/table1_20261023/ (SCORES.txt): pre-fix HEAD 21/31, fixed 31/31, "
+                         "null medium 1/31 CONTROL=FAIL, all 20 variant legs red, 27 of 27 measurements as predicted"),
+    "artifacts/m88kbuserrregs/witness_20261023/m88k_buserr_probe.py":
+        (CLASS_WITNESS, "#570 m88kbuserrregs: the rung-3 pre-fix witness (rev 1, 24 rows, md5 d59798b0) -- 16/24 on HEAD "
+                        "(witness_20261023/WITNESS_headbin.out), 24/24 on the fixed build (table1_20261023/fixed_witness24.out)"),
 }
 
 #  DATED, NAMED DEBT -- not a count and not a silent allowlist.  gate_offline.sh MEASURED that
~~~~
`#568`'s precedent for the same two classes (HEAD, VERBATIM):
~~~~
 2862|     "vme_default_probe.py":
 2863|         (CLASS_DETECTOR, "#568 vmedefaultkill: 38 rows on unmodified -E mvme88k -e mvme187 (rev 3); gated in gate_arm.sh (gate 14) under the stem vme_default, pinned at 38; kill table 2 (artifacts/vmedefaultkill/killtable2_20261021/) BASE 38/38, HEAD 14/38, NULL 5/38 CONTROL=FAIL, 32 of 34 legs killed (M_CAPNARROW by its failed build), the 2 survivors predicted equivalents; addenda 2b/2c/2d: 7 legs, 2 killed, 3 clause-(e) survivors, 2 equivalents"),
 2864|     "artifacts/vmedefaultkill/witness_20261020/vme_sites_probe.py":
 2865|         (CLASS_WITNESS, "#568 the rung-3 witness: 7 of 7 guest access sites end the emulator (rc 1) on HEAD 5dbc000e"),
~~~~
The checker's domain is `.py` files only -- its own comment at HEAD :1238-1250 says a `.sh` path "can therefore NEVER
be in the domain" -- and `regress/artifacts/m88kbuserrregs/` holds exactly ONE `.py` (`witness_20261023/m88k_buserr_probe.py`;
`find -name '*.py'` at drafting time); every other script there is `*.py.txt` / `*.sh.txt`, except the staged gate
copy `table1_20261023/staged/gate_arm.sh` (P12).

### 1.4 The edited regions with the control flow every exit passes through (post-fix working tree)
*The sketch rule: the FULL enclosing functions at HEAD are inlined in the pass-1 packet,
`regress/artifacts/m88kbuserrregs/pass1_20261023/packet.md` sections 8.1 (`MEMORY_RW_ONE_PAGE`, lines 230-786) and
8.2 (`DEVICE_ACCESS(luna88k)`, lines 554-931) -- file-reading seats should read the post-fix functions in `src/`
directly.  Below: every line between the device call and the arm's exits, the LUNA function's entry, early windows,
the edited case, `default:` and its common tail, and the include.*

`src/cpus/memory_rw.c` (anchors `uint64_t orig_paddr = paddr;` and `if (res <= 0 && !no_exceptions) {`, both unique):
~~~~
  436| 	if (paddr >= mem->mmap_dev_minaddr && paddr < mem->mmap_dev_maxaddr) {
  437| 		uint64_t orig_paddr = paddr;
  438| 		int i, start, end, res;
   ...  (#if 0 block 440-473; the device scan starts)
  475| 		start = 0; end = mem->n_mmapped_devices - 1;
  476| 		i = mem->last_accessed_device;
  477| 
  478| 		/*  Scan through all devices:  */
  479| 		do {
  480| 			if (paddr >= mem->devices[i].baseaddr &&
  481| 			    paddr < mem->devices[i].endaddr) {
  482| 				/*  Found a device, let's access it:  */
  483| 				mem->last_accessed_device = i;
  484| 
  485| 				/*  #95: zero the caller's buffer up front on a read
  486| 				    so a device handler that fills only part of it --
  487| 				    or whose access is len-clamped just below -- can
  488| 				    never hand back uninitialised host memory to the
  489| 				    guest.  Root-cause fix for the uninit-read class
  490| 				    (cf. per-device #91/#93/#94).  */
  491| 				if (writeflag == MEM_READ)
  492| 					memset(data, 0, len);
  493| 
  494| 				paddr -= mem->devices[i].baseaddr;
   ...  (495-581: the truncation clamp and the dyntrans fast-path install -- no early return, no gating)
  583| 				res = 0;
  584| 				if (!no_exceptions || (mem->devices[i].flags &
  585| 				    DM_READS_HAVE_NO_SIDE_EFFECTS)) {
  586| 					bool running_before_device_access = cpu->running;
  587| 					res = mem->devices[i].f(cpu, mem, paddr,
  588| 					    data, len, writeflag,
  589| 					    mem->devices[i].extra);
  590| 
  591| 					if (running_before_device_access && !cpu->running)
  592| 						return MEMORY_ACCESS_FAILED;
  593| 				}
  594| 
  595| 				if (res == 0)
  596| 					res = -1;
  597| 
  598| 				/*
  599| 				 *  If accessing the memory mapped device
  600| 				 *  failed, then return with an exception.
  601| 				 *  (Architecture specific.)
  602| 				 */
  603| 				if (res <= 0 && !no_exceptions) {
  604| 					debug("[ %s device '%s' addr %08lx "
  605| 					    "failed ]\n", writeflag?
  606| 					    "writing to" : "reading from",
  607| 					    mem->devices[i].name, (long)paddr);
  608| #ifdef MEM_MIPS
  609| 					mips_cpu_exception(cpu,
  610| 					    cache == CACHE_INSTRUCTION?
  611| 					    EXCEPTION_IBE : EXCEPTION_DBE,
  612| 					    0, vaddr, 0, 0, 0, 0);
  613| #endif
  614| #ifdef MEM_M88K
  615| 					/*  #570: record the bus error in the
  616| 					    faulting side's CMMU first: PFSR =
  617| 					    BERROR << 16 (the field OpenBSD/mvme88k's
  618| 					    trap.c extracts) and PFAR = orig_paddr,
  619| 					    the PHYSICAL address saved before paddr
  620| 					    was made device-relative.  cmmu[0] is the
  621| 					    instruction CMMU, cmmu[1] the data CMMU
  622| 					    (memory_m88k.c's index); the other CMMU
  623| 					    is not written.  A cpu without a CMMU
  624| 					    gets no write and still takes the
  625| 					    exception.  NO_EXCEPTIONS callers (the
  626| 					    debugger) never get here: the test above
  627| 					    keeps them out.  */
  628| 					{
  629| 						struct m8820x_cmmu *cmmu =
  630| 						    cpu->cd.m88k.cmmu[cache ==
  631| 						    CACHE_INSTRUCTION ? 0 : 1];
  632| 						if (cmmu != NULL) {
  633| 							cmmu->reg[CMMU_PFSR] =
  634| 							    CMMU_PFSR_BERROR << 16;
  635| 							cmmu->reg[CMMU_PFAR] =
  636| 							    (uint32_t) orig_paddr;
  637| 						}
  638| 					}
  639| 					m88k_exception(cpu, cache == CACHE_INSTRUCTION
  640| 					    ? M88K_EXCEPTION_INSTRUCTION_ACCESS
  641| 					    : M88K_EXCEPTION_DATA_ACCESS, 0);
  642| #endif
  643| 					return MEMORY_ACCESS_FAILED;
  644| 				}
  645| 				goto do_return_ok;
  646| 			}
  647| 
  648| 			if (paddr < mem->devices[i].baseaddr)
  649| 				end = i - 1;
  650| 			if (paddr >= mem->devices[i].endaddr)
  651| 				start = i + 1;
  652| 			i = (start + end) >> 1;
  653| 		} while (start <= end);
  654| 	}
~~~~
`src/devices/dev_luna88k.c` (anchor `case 0x3ffffff0:`, unique; the function's every return is shown):
~~~~
  554| DEVICE_ACCESS(luna88k)
  555| {
  556| 	struct tm *tmp;
  557| 	time_t timet;
  558|  	uint32_t addr = relative_addr + LUNA88K_REGISTERS_BASE;
  559| 	uint64_t idata = 0, odata = 0;
  560| 	struct luna88k_data *d = (struct luna88k_data *) extra;
  561| 	int cpunr;
  562| 	int sio_devnr;
  563| 
  564| 	if (writeflag == MEM_WRITE)
  565| 		idata = memory_readmax64(cpu, data, len);
  566| 
  567| 	if (addr >= FUSE_ROM_ADDR && len == sizeof(uint32_t) &&
  568| 	    addr < FUSE_ROM_ADDR + FUSE_ROM_SPACE) {
  569| 		if (writeflag == MEM_READ) {
  570| 			odata = d->fuse_rom[(addr - FUSE_ROM_ADDR) / sizeof(uint32_t)];
  571| 			memory_writemax64(cpu, data, len, odata);
  572| 		} else {
  573| 			d->fuse_rom[(addr - FUSE_ROM_ADDR) / sizeof(uint32_t)] = idata;
  574| 		}
  575| 		return 1;
  576| 	}
  577| 
  578| 	if (addr >= FUSE_ROM_ADDR && len == sizeof(uint8_t) &&
  579| 	    addr < FUSE_ROM_ADDR + FUSE_ROM_SPACE) {
  580| 		if (writeflag == MEM_READ) {
  581| 			odata = d->fuse_rom[(addr - FUSE_ROM_ADDR) / sizeof(uint32_t)];
  582| 			odata >>= ((3 - (addr & 3)) * 8);
  583| 			memory_writemax64(cpu, data, len, odata);
  584| 		} else {
  585| 			fatal("TODO: luna88k byte write to fuse\n");
  586| 		}
  587| 		return 1;
  588| 	}
  589| 
  590| 	if (addr >= NVRAM_ADDR && addr + len <= NVRAM_ADDR + NVRAM_SPACE) {
  591| 		size_t offset = addr - NVRAM_ADDR;
  592| 		if (writeflag == MEM_READ) {
  593| 			memcpy(data, d->nvram + offset, len);
  594| 		} else {
  595| 			memcpy(d->nvram + offset, data, len);
  596| 		}
  597| 		return 1;
  598| 	}
  599| 
  600| 	if (addr >= NVRAM_ADDR_88K2 && addr < NVRAM_ADDR_88K2 + NVRAM_SPACE && len == sizeof(uint8_t)) {
  601| 		if (writeflag == MEM_READ) {
  602| 			odata = d->nvram[addr - NVRAM_ADDR_88K2];
  603| 			memory_writemax64(cpu, data, len, odata);
  604| 		} else {
  605| 			d->nvram[addr - NVRAM_ADDR_88K2] = idata;
  606| 		}
  607| 		return 1;
  608| 	}
  609| 
  610| 	if (addr >= TRI_PORT_RAM && addr < TRI_PORT_RAM + TRI_PORT_RAM_SPACE) {
  611| 		size_t offset = addr - TRI_PORT_RAM;
  612| 
  613| 		cpu->memory_rw(cpu, cpu->mem, LANCE_ADDR - 0x100000 + offset,
  614| 			data, len, writeflag, NO_EXCEPTIONS | PHYSICAL);
  615| // if(len==2)
  616| // printf("OFFSET 0x%06x WRITE=%i 0x%02x%02x\n", (int)offset, (int)writeflag, data[0],data[1]);
  617| // else
  618| // printf("OFFSET 0x%06x WRITE=%i 0x%02x\n", (int)offset, (int)writeflag, data[0]);
  619| 		return 1;
  620| 	}
  621| 
  622| 	switch (addr) {
  623| 
  624| 	case 0x3ffffff0:
  625| 		/*  Accessed by OpenBSD/luna88k to trigger an illegal address.
  626| 		    #570: refuse it.  memory_rw.c's refused-device arm then
  627| 		    raises the access exception and writes PFSR and PFAR (for a
  628| 		    load or store, in the data CMMU); this case used to write
  629| 		    cmmu[1]'s PFSR only and serve 0.  The case is kept: without
  630| 		    it the access would reach default:, which stops the cpu.  */
  631| 		return 0;
  632| 
  633| 	case PROM_ADDR:		/*  0x41000000  */
  634| 		/*  OpenBSD/luna88k write here during boot. Ignore for now. (?)  */
  635| 		break;
   ...  (636-912: every other case ends in `break;`)
  908| 	case RESET_CPU_ALL:	/*  0x6d000010: Reset all CPUs  */
  909| 		for (int i = 0; i < cpu->machine->ncpus; ++i)
  910| 			cpu->machine->cpus[i]->running = 0;
  911| 		break;
  912| 
  913| 	default:
  914| 		if (writeflag == MEM_WRITE)
  915| 			debugmsg_cpu(cpu, SUBSYS_DEVICE, "luna88k", VERBOSITY_ERROR,
  916| 		    	    "unimplemented %i-bit WRITE to address 0x%x: 0x%x",
  917| 		    	    len * 8,
  918| 			    (int) addr,
  919| 			    (int) idata);
  920| 		else
  921| 			debugmsg_cpu(cpu, SUBSYS_DEVICE, "luna88k", VERBOSITY_ERROR,
  922| 		    	    "unimplemented %i-bit READ from address 0x%x",
  923| 		    	    len * 8,
  924| 			    (int) addr);
  925| 
  926| 		// Stop the emulation immediately.
  927| 		cpu->running = 0;
  928| 		return 0;
  929| 	}
  930| 
  931| 	if (writeflag == MEM_READ)
  932| 		memory_writemax64(cpu, data, len, odata);
  933| 
  934| 	return 1;
  935| }
~~~~
`src/cpus/cpu_m88k.c` (its includes) and `src/cpus/tmp_m88k_tail.c` (where `memory_rw.c` is compiled for m88k):
~~~~
   44| #include "cpu.h"
   45| #include "float_emul.h"
   46| #include "interrupt.h"
   47| #include "machine.h"
   48| #include "memory.h"
   49| #include "misc.h"
   50| #include "settings.h"
   51| #include "symbol.h"
   52| 
   53| #include "thirdparty/m8820x_pte.h"
   54| /*  #570: memory_rw.c's m88k refused-device arm, compiled into this unit through
   55|     tmp_m88k_tail.c, uses CMMU_PFSR, CMMU_PFAR and CMMU_PFSR_BERROR, which are
   56|     defined only in m8820x.h; upstream adds the same include to this file.  */
   57| #include "thirdparty/m8820x.h"
   58| #include "thirdparty/m88k_dmt.h"
   59| #include "thirdparty/mvmeprom.h"
   60| 
   61| #define DYNTRANS_32
   62| #define DYNTRANS_DELAYSLOT
   63| #include "tmp_m88k_head.c"
   ...
 1689| #include "tmp_m88k_tail.c"
~~~~
~~~~
   36| #undef DYNTRANS_UPDATE_TRANSLATION_TABLE
   37| 
   38| #define MEMORY_RW m88k_memory_rw
   39| #define MEM_M88K
   40| #include "memory_rw.c"
   41| #undef MEM_M88K
   42| #undef MEMORY_RW
~~~~
`src/include/thirdparty/m8820x.h` -- the three names, `NBSG`, and the `#if 0` block (the header's only non-macro content):
~~~~
   64| #define CMMU_SCTR	(0x104 / 4)	/* system control register */
   65| #define CMMU_PFSR	(0x108 / 4)	/* P bus fault status register */
   66| #define CMMU_PFAR	(0x10c / 4)	/* P bus fault address register */
  123| #define	CMMU_PFSR_FAULT(pfsr)	(((pfsr) >> 16) & 0x07)
  124| #define CMMU_PFSR_SUCCESS	0	/* no fault */
  125| #define CMMU_PFSR_BERROR	3	/* bus error */
  180| #define	BATC9_VA		0xfff80000
  181| 
  182| #define NBSG    	(1 << (PDT_BITS + PG_BITS))	/* segment size */
  183| 
  184| #define	INST_CMMU	0x00	/* even number */
  185| #define	DATA_CMMU	0x01	/* odd number */
  186| #define	CMMU_MODE(num)	((num) & 1)
  187| 
  188| #define MAX_CMMUS	8		/* maximum cmmus on the board */
  189| 
  190| #if 0
  191| #ifndef _LOCORE
  192| 
  193| /*
  194|  * CMMU kernel information
  195|  */
  196| struct m8820x_cmmu {
  197| 	volatile u_int32_t *cmmu_regs;	/* CMMU "base" area */
  198| #ifdef M88200_HAS_SPLIT_ADDRESS
  199| 	vaddr_t		cmmu_addr;	/* address range */
  200| 	vaddr_t		cmmu_addr_mask;	/* address mask */
  201| #endif
  202| };
  203| 
  204| extern struct m8820x_cmmu m8820x_cmmu[MAX_CMMUS];
  205| extern u_int cmmu_shift;
  206| extern u_int max_cmmus;
  207| 
  208| void	m8820x_setup_board_config(void);
  209| cpuid_t	m8820x_cpu_number(void);
  210| 
  211| #endif	/* _LOCORE */
  212| #endif
  213| 
  214| #endif	/* __M88K_M8820X_H__ */
~~~~
The port source's include hunk -- upstream trunk against 0.7.0 (`regress/artifacts/research_20261022/trunk_src.diff`,
tracked, VERBATIM):
~~~~
 1914| diff -ruN x_070/gxemul-0.7.0/src/cpus/cpu_m88k.c x_trunk/gxemul-trunk/src/cpus/cpu_m88k.c
 1915| --- x_070/gxemul-0.7.0/src/cpus/cpu_m88k.c	2021-04-22 13:04:18.000000000 -0500
 1916| +++ x_trunk/gxemul-trunk/src/cpus/cpu_m88k.c	2023-07-24 14:14:36.000000000 -0500
 1917| @@ -50,6 +50,7 @@
 1918|  #include "settings.h"
 1919|  #include "symbol.h"
 1920|  
 1921| +#include "thirdparty/m8820x.h"
 1922|  #include "thirdparty/m8820x_pte.h"
 1923|  #include "thirdparty/m88k_dmt.h"
 1924|  #include "thirdparty/mvmeprom.h"
~~~~

---

## 2. THE DETECTOR -- `regress/m88k_buserr_probe.py`, revision 2 (31 rows)

### 2.1 Identity, and the witness it was promoted from
* **This file:** untracked, 836 lines, md5 `d57c12ab7ade903946c7d80a8e153ab7`; byte-identical to
  `table1_20261023/m88k_buserr_probe.rev2.frozen.py.txt`, frozen at 22:42:48 BEFORE any table run (section 3.1) and
  named in every leg's output.  The gate-14 run log's header (written by the builder's run driver) prints the same
  md5 for the file the gate ran (section 3.6).
* **The witness (revision 1, 24 rows)** stays where it was, UNCHANGED: `witness_20261023/m88k_buserr_probe.py`, md5
  `d59798b0383f433b191e214e7848fe49`; that directory's `MANIFEST.md5` verifies **32 of 32** at drafting time.  Its
  pre-fix receipt is `WITNESS_headbin.out` (16/24, SYMPTOM=PRESENT 8/8); its post-fix receipt is
  `table1_20261023/fixed_witness24.out` (24/24, ABSENT).
* **One disclosed pre-freeze run:** the unfrozen file was smoke-run once on the HEAD binary
  (`table1_20261023/smoke_HEAD_unfrozen.out`, 22:42:49), its rows identical to the official pre-fix run
  (`prefix_HEAD.out`, 22:42:52) -- disclosed so that no number is read as fitted (departure 5, section 3.9).

### 2.2 The 31 rows, enumerated (6 + 10 + 15 = 31)
* **CONTROL_ROWS (6)** -- `neg apparatus`, `mv devsig`, `mv cmmu rt`, `luna devsig`, `luna cmmu rt`, `unasm`.
* **SYMPTOM rows (10)** -- `uld pfsr`, `uld pfar`, `ust pfsr`, `ust pfar`, `vme pfsr`, `vme pfar`, `luna route`,
  `luna pfar`, `ifetch pfsr`, `ifetch pfar`.
* **Other scored rows (15)** -- `ok route`, `ok regs`, `uld route`, `uld icmmu`, `ust route`, `ust icmmu`, `vme route`,
  `vme icmmu`, `luna pfsr`, `luna icmmu`, `ifetch route`, `ifetch dcmmu`, `dbg noexc`, `null surv`, `null route`.
* **New in revision 2 (7)** -- `ifetch route`, `ifetch pfsr`, `ifetch pfar`, `ifetch dcmmu`, `dbg noexc`, `null surv`,
  `null route` (24 + 7 = 31).
* **The unasm literal 192** = 7 standard sessions x 23 placed words (`ok`, `uld`, `ust`, `vme`, `luna`, `ifetch`, `dbg`:
  vectors 2 + 2, CODE 13, handler 6) + the `null` session's 31 (those 23 plus cpu 1's 8: CODE1 4, VBR1+0x10 1,
  VBR1+0x18 2, VBR1+0x50 1).  The witness's 115 was 5 x 23.  The apparatus session and INFO `unclaimed` are not counted.

### 2.3 CHANNEL as the header names it, against the MEASURED red sets
*Derived by the drafter from `SCORES.txt` (section 3.4): for each row, every revision-2 leg whose MEASURED red set
contains it.  `pre` = the HEAD binary; L5 = the null medium; L18/L19 red through prerequisite strings (CONTROL=FAIL).
The header's per-row "designed to catch" list (section 2.4, ROWS) was compared row by row: every leg it names for a
row is in that row's measured column; the measured column adds only L5 (the null medium) everywhere, and L18 / L19
(through prerequisite strings) on rows whose header entry does not name them.*
~~~~
row             red under (revision-2 legs, measured)
neg apparatus   (never red -- green by design on the exit-1 stub)
mv devsig       L5 L19
mv cmmu rt      L5 L18 L19
ok route        L5 L18 L19
ok regs         L5 L18 L19
uld route       L5 L17 L18 L19
uld pfsr        pre L3 L5 L6b L10 L18 L19
uld pfar        pre L3 L5 L6b L11 L12 L18 L19
uld icmmu       L5 L6b L13 L14 L18 L19
ust route       L5 L17 L18 L19
ust pfsr        pre L3 L5 L6b L10 L15 L18 L19
ust pfar        pre L3 L5 L6b L11 L12 L15 L18 L19
ust icmmu       L5 L6b L13 L14 L18 L19
vme route       L5 L17 L18 L19
vme pfsr        pre L3 L5 L6b L10 L16 L18 L19
vme pfar        pre L3 L5 L6b L11 L12 L16 L18 L19
vme icmmu       L5 L6b L13 L14 L18 L19
luna devsig     L5 L19
luna cmmu rt    L5 L18 L19
luna route      pre L4 L5 L17 L18 L19 L21 L22
luna pfsr       L3 L5 L6b L10 L18 L19 L21 L22
luna pfar       pre L3 L4 L5 L6b L11 L12 L18 L19 L21 L22
luna icmmu      L5 L6b L13 L14 L18 L19 L22
ifetch route    L5 L17 L18 L19
ifetch pfsr     pre L3 L5 L6 L10 L17 L18 L19
ifetch pfar     pre L3 L5 L6 L11 L12 L17 L18 L19
ifetch dcmmu    L5 L6 L13 L14 L17 L18 L19
dbg noexc       L5 L7 L18 L19
null surv       L5 L8 L8b
null route      L5 L8 L9 L17
unasm           L5
~~~~
**Single-row carriers:** L7 reds only `dbg noexc`; L8b only `null surv`; L9 only `null route`.  L6 reds only the
three `ifetch` rows that carry the instruction label's metadata.

### 2.4 The header -- DEFECT, FIX, CLAIMS, RUNG 3, PROGRAM, ADDRESSES, ROWS with CHANNEL, SYMPTOM, CONTRACT (NOT CLAIMED), GATE 14, TEST-FIRST (VERBATIM, lines 1-220)
~~~~
    1| #!/usr/bin/env python3
    2| """m88k_buserr_probe.py -- rung-3 DETECTOR for m88kbuserrregs (#570, TRIAGE.md T36): a refused m88k device access
    3| records its bus error in the faulting side's CMMU (PFSR = BERROR << 16, PFAR = the physical address).
    4| 
    5| REVISION 2 (2026-10-23), 31 rows.  Promoted from the rung-3 WITNESS (revision 1, 24 rows), which stays byte-identical
    6| at regress/artifacts/m88kbuserrregs/witness_20261023/m88k_buserr_probe.py and remains the round's pre-fix witness.
    7| This revision adds seven rows -- `ifetch route/pfsr/pfar/dcmmu', `dbg noexc', `null surv', `null route' -- per
    8| PASS1_RULINGS.md B5a-B5c and section E, BUILD_SPEC.md sections 3, 10 and 11 (pass1_20261023/), and the PRETABLE
    9| (table1_20261023/PRETABLE.out, with its AMENDMENT 1).
   10| 
   11| DEFECT (HEAD 7fca7187, whose src/ equals 66920157's; both sites are the 0.7.0 import).  When a guest data load or
   12| store reaches a device whose access function REFUSES it (returns 0 with the cpu still running), src/cpus/memory_rw.c's
   13| refused-access arm (`if (res <= 0 && !no_exceptions)') raises the m88k data-access exception (vector 3) and wrote
   14| NOTHING into the data CMMU's P-bus fault status register (PFSR, offset 0x108) or P-bus fault address register (PFAR,
   15| 0x10c); its TODO said "the faulting address should probably be included somewhere too".  A guest fault handler that
   16| reads them saw whatever they held before.  The LUNA probe address -- src/devices/dev_luna88k.c's `case 0x3ffffff0' --
   17| wrote PFSR = CMMU_PFSR_BERROR << 16 on cmmu[1] only (for ANY access class), wrote NO PFAR and `break'ed into
   18| `return 1': the access SUCCEEDED, serving 0, and no exception was raised at all.
   19| 
   20| WHICH ACCESSES REACH THAT ARM -- a premise correction, measured by the witness: only an access a device CLAIMS and
   21| REFUSES.  An access to a physical address NO device claims never enters the device scan's success branch; it falls
   22| through to memory_rw.c's `Outside of physical RAM?' path, where memory_warn_about_unimplemented_addr() prints at most
   23| a warning -- or, under `-T', stops every cpu -- and a read is served zeros: no exception and no CMMU write, before or
   24| after #570 (INFO `unclaimed' below).  So the refusing devices used here are ones the in-tree machine descriptions
   25| install to model absent hardware: mvme187's `unreadable' window and VME population 1.
   26| 
   27| THE FIX (#570, four product files, byte-identical in est/):
   28|   * src/cpus/memory_rw.c, the MEM_M88K block of the refused-access arm: select cmmu[0] for an instruction access and
   29|     cmmu[1] otherwise (`cache == CACHE_INSTRUCTION ? 0 : 1', memory_m88k.c's index); if that pointer is not NULL, write
   30|     PFSR = CMMU_PFSR_BERROR << 16 (0x00030000) and PFAR = (uint32_t) orig_paddr (the PHYSICAL address saved before the
   31|     arm makes `paddr' device-relative).  The NULL check wraps the two writes only; the exception, the
   32|     `!no_exceptions' guard, the debug() line and the failure return are unchanged; the sibling CMMU is not written.
   33|   * src/cpus/cpu_m88k.c: #include "thirdparty/m8820x.h" after m8820x_pte.h (upstream's placement, the transferred
   34|     warrant) -- memory_rw.c is compiled inside cpu_m88k.c's translation unit (tmp_m88k_tail.c), and CMMU_PFSR,
   35|     CMMU_PFAR and CMMU_PFSR_BERROR live only in that header.  Without it the repair does not compile.
   36|   * src/devices/dev_luna88k.c: the 0x3ffffff0 case returns 0, so the access is refused through the repaired arm (its
   37|     own PFSR write deleted; the case kept, because `default:' stops the cpu).
   38|   * src/devices/dev_m8820x.c: comment-only (the PFSR/PFAR writer citations).
   39| 
   40| WHAT #570 MAY CLAIM, AND WHAT IT DISCLAIMS (PASS1_RULINGS A8).  Claimed: fault metadata for CLAIMED, REFUSED,
   41| unsuppressed device accesses that pass the running-transition check, on a cpu that has a CMMU, plus LUNA's probe case
   42| routed into that path.  Disclaimed -- never "every 88K bus error now carries PFSR and PFAR": an UNCLAIMED address (no
   43| exception, no CMMU write; R3); on luna-88k every OTHER device refusal still stops the cpu before the arm; FREE-RUNNING
   44| instruction-fetch refusals (vector 2, then the dyntrans `bad:' tail stops the cpu before any handler -- R1); callers
   45| that pass NO_EXCEPTIONS (the debugger: the arm's own `!no_exceptions' term keeps them out -- `dbg noexc'); the
   46| translation-fault writer (memory_m88k.c, not edited); a sub-word access's PFAR (the byte address is written, a
   47| transferred warrant only -- no MC88200 manual is on disk); CMMU-less cpus (no write, the exception unchanged).
   48| 
   49| RUNG 3: real MC88100 instructions (ld/st/or/br/jmp) through real address decode and real memory_rw, on two
   50| UNMODIFIED in-tree machines: `-E mvme88k -e mvme187 -M 64' (machine_mvme88k.c) and `-E luna88k -e luna-88k'
   51| (machine_luna88k.c), each started with a 4-byte dummy raw image at 0x10000 (no PROM, no disk).  The `null' session
   52| adds `-n 2', a documented command-line option of the same in-tree machine (no machine edit, no device_add): mvme187
   53| attaches both CMMUs to the bootstrap cpu only (dev_mvme187.c), so cpu 1 has none, and the debugger's `pause 1' starts
   54| it (debugger_cmds.c's pause toggles `running').  An optional third argument names the rig images directory; the LUNA
   55| session then runs in luna_absentcpu_probe.py's rig shape (`-e luna-88k -d R:<images>/liveimage-luna88k-raw-20250518.img
   56| boot', cwd = the images directory) -- the witness measured the two shapes identical.  Every session is STEPPED and
   57| feeds the debugger on stdin (vme_default_probe.py's run_piped); no pseudo-terminal driver is used, and none is needed:
   58| a synchronous device refusal is visible while stepping, and a free-running run of the witness's exploration program
   59| gave the same stale registers (witness_20261023/explore2.out case 1).
   60| 
   61| THE PROGRAM (the five witness sessions, `ifetch' and `dbg'; only the ACCESS word and its registers differ):
   62|     0x10   or r7,r0,2 ; br H         vector 2 (INSTRUCTION_ACCESS) marker -- VBR is 0 at reset (measured)
   63|     0x18   or r7,r0,3 ; br H         vector 3 (DATA_ACCESS) marker
   64|     CODE   ld r10,r3,0x0             data CMMU IDR           -- DEVICE SIGNATURE (0x00a90000; RAM cannot answer it)
   65|            ld r9,r2,0x0              instruction CMMU IDR    -- the same, for the sibling
   66|            st r20,r3,0x108 / st r21,r3,0x10c / st r22,r2,0x108 / st r23,r2,0x10c
   67|                                      SEED both CMMUs' PFSR and PFAR with four distinct values
   68|            ld r11,r3,0x108 / ld r12,r3,0x10c / ld r17,r2,0x108 / ld r18,r2,0x10c
   69|                                      LIVENESS through the same decode: each seed reads back
   70|            ACCESS                    the access under test (CODE + 0x28)
   71|            or r6,r0,0x1234 ; br H    FALL-THROUGH marker: runs only if the access raised nothing
   72|     H      ld r13,r3,0x108 / ld r14,r3,0x10c / ld r15,r2,0x108 / ld r16,r2,0x10c
   73|                                      the four registers AFTER the access, read by GUEST LOADS in the handler
   74|            or r31,r0,0x5678 ; br .   the handler ran to its end
   75|   So the reads happen on BOTH paths: a refused access enters vector 3 (or 2) and branches to H; an access that
   76|   raises nothing falls through to the same H.  r7 says which vector was entered, r6 whether it fell through, and
   77|   `reg 0,0' gives SXIP (the faulting instruction | V) and DMA0 (the faulting word address) -- the attribution
   78|   control: the exception came from THIS access.  19 steps reach H's `br .' on either path.  One fault per session:
   79|   the exception sets PSR.SFRZ, and a second fault while it is set becomes ERROR (cpu_m88k.c's m88k_exception).
   80|   `dbg' runs the `ok' program with `step 10' / `dump' / `reg' / `step 9': the debugger reads the unreadable window
   81|   between the readbacks and the accepted access.  `null' is described at its rows.
   82| 
   83| ADDRESSES AND OFFSETS (each cited; literals on purpose, so a header edit cannot silently move them):
   84|   CMMU register offsets -- src/include/thirdparty/m8820x.h CMMU_IDR (0x000 / 4), CMMU_PFSR (0x108 / 4), CMMU_PFAR
   85|       (0x10c / 4); dev_m8820x.c serves a read as regs[relative_addr / 4] and STORES a guest write to PFSR/PFAR (which
   86|       is what makes the seed-and-readback liveness possible); IDR is never stored.  BERROR: m8820x.h CMMU_PFSR_BERROR
   87|       3, the field extract CMMU_PFSR_FAULT ((pfsr >> 16) & 7).
   88|   IDR seed 0x00a90000 = (M88200_ID << 21) | (9 << 16), M88200_ID 5 (m8820x.h; dev_mvme187.c, dev_luna88k.c).
   89|   mvme187 CMMUs: data 0xfff7f000, instruction 0xfff77000 (mvme187.h); cmmu[0] = instruction, cmmu[1] = data
   90|       (dev_mvme187.c; dev_m8820x.c's addr2 decode; memory_m88k.c uses the same index).
   91|   luna-88k CPU-0 CMMUs: data 0xfff06000, instruction 0xfff07000 (luna88k_board.h CMMU_D0 / CMMU_I0).
   92|   refused device #1 -- `unreadable addr=0xfff46000 len=0x1000' (machine_mvme88k.c, the ie0 placeholder):
   93|       dev_unreadable.c's access function is `return 0;'.  0xfff46010 is device-relative 0x10.
   94|   refused device #2 -- VME2 at 0xfff40000 (mvme88k_vme.h VME2_BASE): offset 0x90 is population 1 of #568
   95|       (vmedefaultkill), dev_vme.c's `default:' returns 0.  0xfff40090 is device-relative 0x90.
   96|   accepted device access -- VME VBR at 0xfff40088 (VME2_VBR), served by its cased arm from DEVINIT's
   97|       VME2_SET_VBR0(6) + VME2_SET_VBR1(7) = 0x67000000.
   98|   the LUNA probe address 0x3ffffff0 = LUNA88K_REGISTERS_BASE (dev_luna88k.c), `case 0x3ffffff0'; device-relative 0.
   99|   vectors -- cpu_m88k.h INSTRUCTION_ACCESS 2, DATA_ACCESS 3, ERROR 10; pc = VBR + 8 * vector; SXIP = pc | V (0x2),
  100|       | E (0x1) for an instruction access; DMT0/DMD0/DMA0 copied from the data unit on DATA_ACCESS only.
  101|   `null' session: cpu 1's code at 0x10200 (CODE1), J = 0x1020c, its VBR 0x30000 (set by the debugger), RAM markers
  102|       HANDLED at 0xf000 (value 0x4a4a4a4a) and FELL at 0xf004 (value 0x46464646), zeroed by `put' before cpu 1 runs.
  103| 
  104| ROWS -- each with the variant(s) it is DESIGNED to catch (leg ids of table1_20261023/; L20 = L4, not run) and the
  105| channel that differs.  *** DATED PREDICTIONS (PRETABLE.out section 5 + AMENDMENT 1) UNTIL THE TABLE RUNS; the
  106| measured scores, per leg, are in table1_20261023/SCORES.txt. ***  `prereq:' = the row's cause-free prerequisite
  107| string replaces its value (the session failed something the value depends on; the row stays red, claiming no cause).
  108|   CONTROL rows -- a PREREQUISITE of the scored rows (apparatus, medium, device signature).  CONTROL=FAIL claims no cause.
  109|     neg apparatus  a bogus subtype `187': no machine, no register dump -- the session oracle can go red.  Green BY
  110|                    DESIGN on an exit-1 non-emulator (L5)
  111|     mv devsig      mvme187 data + instruction CMMU IDR = 0x00a90000 each (RAM, or no device, reads 0).  L19
  112|     mv cmmu rt     mvme187: the four seeds read back through the same decode.  L18 (misplaced writes overwrite the
  113|                    seeds), L19
  114|     luna devsig    luna-88k: the same two IDRs.  L19
  115|     luna cmmu rt   luna-88k: the four seeds read back.  L18, L19
  116|     unasm          every placed word re-read by the disassembler; LITERAL count
  117|   accept side (mvme187, `ld r4,r5,0' at VME VBR 0xfff40088 -- an ACCEPTED device access)
  118|     ok route       fall-through, r4 = 0x67000000.  L19 (`res <= 1') -- but the observable is prereq:nodev, because
  119|                    every served CMMU access faults first; the named "v3" channel is not reachable by a global widening
  120|     ok regs        all four seeds survive an accepted access.  L18 (the writes moved before the guard) -- observable
  121|                    prereq:readback, for the same reason; also L19
  122|   generic arm, data LOAD / data STORE / a SECOND refusing device (mvme187, at 0xfff46010 / 0xfff46010 / 0xfff40090)
  123|     uld route / ust route / vme route   vector 3, SXIP = CODE + 0x28 | V, DMA0 = the address (r4 keeps its sentinel
  124|                    for a load).  L17 (exception dropped: fall-through)
  125|     uld pfsr / ust pfsr / vme pfsr      data PFSR = 0x00030000.  HEAD: the seed 0x5a5a5a5a.  L3 (arm reinstated),
  126|                    L10 (raw 3), L6b (always cmmu[0]); ust: L15 (repair conditioned on MEM_READ); vme: L16 (VME
  127|                    excluded)
  128|     uld pfar / ust pfar / vme pfar      data PFAR = the PHYSICAL address.  HEAD: the seed 0x13572468.  L3, L11 (the
  129|                    device-relative paddr: 0x10 / 0x90), L12 (PFSR only), L6b; ust: L15; vme: L16
  130|     uld icmmu / ust icmmu / vme icmmu   the instruction CMMU keeps its seeds.  L13 (both CMMUs), L14 (sibling
  131|                    cleared as the translation-fault writer does), L6b.  (NOT L15/L16: a read-only or device-keyed
  132|                    repair leaves route and sibling alone.)
  133|   the LUNA probe address (luna-88k, `ld r4,r5,0' at 0x3ffffff0)
  134|     luna route     vector 3, SXIP, DMA0 = 0x3ffffff0, r4 keeps its sentinel.  HEAD: fall-through, SXIP 0, DMA0 0,
  135|                    r4 = 0 (SERVED).  L4 (= L20: the case reinstated), L21 (its write deleted, still served), L17,
  136|                    L22 (case deleted: `default:' stops the cpu -> prereq:handler)
  137|     luna pfsr      data PFSR = 0x00030000.  GREEN on HEAD (the case's own write).  L3, L10, L21 (its UNIQUE variant:
  138|                    the write deleted while the access stays served), L22, L6b
  139|     luna pfar      data PFAR = 0x3ffffff0.  HEAD: the seed.  L3, L4, L11 (0x0: the access is AT the base), L12, L21,
  140|                    L22, L6b
  141|     luna icmmu     the instruction CMMU keeps its seeds.  L13, L14, L22, L6b
  142|   the INSTRUCTION label (mvme187, `jmp (r5)' to 0xfff46010) -- B5a
  143|     ifetch route   ATTRIBUTION row, not in CONTROL_ROWS: vector 2, SXIP = 0xfff46013 (| V | E), DMA0 0.  The vector
  144|                    expression reads `cache' independently of the added selector, so this row CANNOT vary under the
  145|                    selector variant (L6) -- by construction.  Its variant: L17 (exception dropped / mis-routed: the
  146|                    step's fetch then reaches R1's `bad:' tail and the handler never runs -> prereq:handler)
  147|     ifetch pfsr    INSTRUCTION CMMU PFSR = 0x00030000.  HEAD: the seed 0x2468ace0 (red on HEAD).  L6 (always-data
  148|                    selector: cmmu[0] not written), L3, L10, L17
  149|     ifetch pfar    INSTRUCTION CMMU PFAR = 0xfff46010.  HEAD: the seed 0x0badf00d.  L6, L3, L11 (0x10), L12, L17
  150|     ifetch dcmmu   the DATA CMMU keeps its seeds after an instruction refusal.  L6 (the data CMMU written), L13, L14
  151|                    (dPFSR := 0), L17
  152|     *** R2 DEPENDENCY, DISCLOSED (PASS1_RULINGS C2): stepped, the instruction refusal reaches the arm through the step
  153|     loop's disassembly pre-read (cpu_dyntrans.c, CACHE_INSTRUCTION without NO_EXCEPTIONS).  When R2 is fixed the
  154|     pre-read stops raising, the step's own fetch reaches R1's `bad:' tail and halts the cpu, and these four rows go
  155|     red for that UNRELATED reason -- they are re-rooted when R1 and R2 land (the obligation is filed with them). ***
  156|   a NO_EXCEPTIONS caller (mvme187, the `ok' program in its own session) -- B5b
  157|     dbg noexc      after the seeds, the debugger command `dump 0xfff46010 0xfff46020' (cpus[bootstrap_cpu], CACHE_NONE |
  158|                    NO_EXCEPTIONS): zeros returned, pc unchanged (0x10028: no vector taken), the program then falls
  159|                    through its accepted access, and all four seeds survive.  The arm IS reached (res 0 -> -1); its
  160|                    `!no_exceptions' term keeps the body out.  L7 (that term dropped: the dump fails, cpu 0 vectors,
  161|                    the data CMMU is written)
  162|   a CMMU-LESS cpu (mvme187 -n 2, cpu 1) -- B5c, the {data, instruction} x {CMMU absent} cells CONJUNCTIVELY
  163|     cpu 0 runs the seeded `uld' program alone (19 steps) and parks in H's `br .' (nothing is scored from it).  cpu 1 is
  164|     set up by `focus 1' (pc, r5, the two marker values, its own VBR); `tlbdump 1' must show no CMMU (the NULL premise);
  165|     `pause 1'; part 1 `step 3': `ld r4,r5,0' at 0xfff46010 -> cpu 1's vector 3 stores HANDLED and branches to J (the
  166|     FELL store after the load runs only if no exception was raised); the markers and `reg 1,0' are read HERE (a second
  167|     fault zeroes DMA0).  Part 2 `step 5': J `jmp (r5)' -> the instruction fetch at 0xfff46010 is refused with cmmu[0]
  168|     NULL.  *** SFRZ, DISCLOSED: the data fault left PSR.SFRZ set and no `rte' clears it (an `rte' would resume at SNIP,
  169|     the FELL store), so this second, non-trap fault is delivered as ERROR (vector 10), VBR1 + 0x50, where `br .' parks
  170|     cpu 1 (VBR1 + 0x10 parks it too).  The arm runs BEFORE m88k_exception, so the NULL test is exercised whatever
  171|     the vector. ***  Stepped, the fetch rides R2 like the ifetch rows; with R2 fixed the step's own fetch reaches the
  172|     same arm, so the NULL-check observable survives and only the after-fault flow changes (R1's halt).
  173|     null route     part 1: HANDLED set, FELL clear, SXIP 0x10202, DMA0 0xfff46010.  L9 (exception moved inside the NULL
  174|                    check: fell), L17 (fell), L8 (the session dies in part 1)
  175|     null surv      the session reaches part 2's prompt alive with both marker dumps readable.  L8 (NULL check removed:
  176|                    cpu 1's data load dereferences NULL), L8b (the check conditioned on the data label: the instruction
  177|                    fetch dereferences NULL in part 2)
  178|   INFO (unscored): a load from an UNCLAIMED physical address (mvme187, 0x10000000: past the 64 MB of RAM, below every
  179|                    device) -- see the premise correction above.  (Revision 1's INFO ifetch line is now four rows.)
  180| 
  181| SYMPTOM CLASSIFICATION (the "did it fail for the reason under test?" line): the TEN rows the fix changes -- uld/ust/vme
  182| pfsr and pfar, luna route, luna pfar, ifetch pfsr, ifetch pfar -- are each STALE (exactly the probe's own seed, or for
  183| luna route the fall-through with r4 served 0), FIXED (got == want) or OTHER.  M88K_BUSERR_SYMPTOM prints PRESENT n/10
  184| when all ten are STALE, ABSENT when all ten are FIXED, else MIXED with the list.  Neither PFSR seed carries BERROR in
  185| the field the guest tests: (0x5a5a5a5a >> 16) & 7 == 2 and (0x2468ace0 >> 16) & 7 == 0.
  186| 
  187| CONTRACT (clause e).  DESIGNED to catch: the pre-fix defect and the variants named per row above (measured per leg in
  188| table1_20261023/SCORES.txt).  NOT CLAIMED, so a later escape is outside the contract rather than an argument:
  189|   * VA != PA.  PFAR := `vaddr' is not an operand the m88k arm reads (the MEM_MIPS block that reads it is compiled out),
  190|     and every session leaves the CMMUs' APR invalid, so physical = virtual (memory_m88k.c).  A guest COULD separate them
  191|     (a SAPR/UAPR store sets APR_V; a BWP store programs a BATC) -- these sessions do not;
  192|   * sub-word accesses and byte addresses: every access is a word at a word-aligned address (PFAR's low bits are
  193|     UNKNOWN for silicon; the byte address is upstream's choice, a transferred warrant);
  194|   * a LUNA STORE at 0x3ffffff0 (the generic direction is pinned by `ust');
  195|   * an UNCLAIMED physical address (INFO `unclaimed'; R3);
  196|   * luna-88k `-n 2..4' (per-cpu CMMU selection beyond the null session's mvme187 cpu 1), xmem, the 88110 (mvme197);
  197|   * FREE-RUNNING instruction-fetch refusals (R1: the cpu stops before any handler); the stepped ifetch and null rows
  198|     ride R2 (above);
  199|   * translation-fault semantics (memory_m88k.c is not edited);
  200|   * the OpenBSD reader itself (trap.c's `(dpfsr >> 16) & 7 == 3' and badaddr()'s eh.S recovery); a boot is measured
  201|     separately (table1_20261023/boot_ab/);
  202|   * the sibling CMMU's real latch semantics: the `icmmu' / `ifetch dcmmu' wants encode the ruling `kept' (A9); the
  203|     hardware behaviour is UNKNOWN, and a guest's snapshots CAN differ (do not read the rows as "unobservable");
  204|   * PFSR / PFAR bits beyond the exact values written; real MC88200 timing or the P-bus.
  205|   Clause (c) (null medium): measured at table1_20261023/L5_stub.out and L5b_absent.out (see SCORES.txt).
  206| 
  207| GATE 14 (regress/gate_arm.sh) runs this probe in the block after #568's.  *** THAT BLOCK CAN BE SKIPPED WITHOUT
  208| RUNNING: gate_arm.sh has eleven earlier skip points (`grep -n -e gate_skip -e need_exec regress/gate_arm.sh': :84
  209| need_exec, :85 python3, :93 the load stub, and the eight probe-completion skips :105 :389 :430 :515 :638 :695 :816
  210| :949), and any one of them ends the gate before this block -- a SKIP, which is never evidence. ***
  211| 
  212| TEST-FIRST SHAPE: on the pre-fix HEAD the ten symptom rows are red (M88K_BUSERR_SYMPTOM=PRESENT 10/10) while the six
  213| controls and the other fifteen scored rows are green; after #570 the same script is all green, SYMPTOM=ABSENT.
  214| 
  215| usage: m88k_buserr_probe.py <gxemul> [label] [images-dir]
  216|        M88K_BUSERR_DUMP=<dir> also writes every session's raw debugger transcript to <dir>/<session>.txt
  217|        (unset: nothing is written; the rows and lines below are identical either way).
  218| Sentinel: M88K_BUSERR_PROBE_DONE (plus M88K_BUSERR_RESULT=n/N, M88K_BUSERR_CONTROL=OK|FAIL,
  219| M88K_BUSERR_SYMPTOM=PRESENT n/10|ABSENT|MIXED ..., M88K_BUSERR_REVISION=2)
  220| """
~~~~

### 2.5 The body -- encodings, sessions, the prerequisite check, every row's got/want, the scoring and the sentinel (VERBATIM, lines 221-836)
*Load-bearing for Q2: `prereq_bad()` (lines 504-515), `row()` / `symptom()` (566-581), `dbg noexc` (674-701), the
`null` session and its two rows (703-788), the `unasm` literal (800-808), the score / CONTROL / SYMPTOM / sentinel /
exit block (810-836).*
~~~~
  221| 
  222| import os
  223| import re
  224| import shutil
  225| import subprocess
  226| import sys
  227| import tempfile
  228| import time
  229| 
  230| if len(sys.argv) < 2:
  231|     sys.stderr.write("usage: m88k_buserr_probe.py <gxemul> [label] [images-dir]\n")
  232|     sys.exit(2)
  233| 
  234| BIN = sys.argv[1]
  235| LABEL = sys.argv[2] if len(sys.argv) > 2 else "local"
  236| IMAGES = sys.argv[3] if len(sys.argv) > 3 else None
  237| DUMP = os.environ.get("M88K_BUSERR_DUMP") or None
  238| REVISION = 2
  239| #  A private dummy file: a shared /tmp path once let two concurrent runs race on it (vme_default_probe.py).
  240| _TMPDIR = tempfile.mkdtemp(prefix="m88k_buserr_")
  241| DUMMY = os.path.join(_TMPDIR, "dummy.bin")
  242| with open(DUMMY, "wb") as _f:
  243|     _f.write(b"\x00\x00\x00\x00")
  244| 
  245| CODE = 0x00010000
  246| H = 0x00010100              # the reading handler both paths reach
  247| VEC_IACC = 0x10             # VBR 0 + 8 * M88K_EXCEPTION_INSTRUCTION_ACCESS (2)
  248| VEC_DACC = 0x18             # VBR 0 + 8 * M88K_EXCEPTION_DATA_ACCESS (3)
  249| SENT = 0xdeadbeef
  250| FALL = 0x1234               # r6: the access raised nothing
  251| LIVE = 0x5678               # r31: the handler ran to its end
  252| D_PFSR_SEED = 0x5a5a5a5a    # (>> 16) & 7 == 2: not BERROR under the guest's extract
  253| D_PFAR_SEED = 0x13572468
  254| I_PFSR_SEED = 0x2468ace0    # (>> 16) & 7 == 0
  255| I_PFAR_SEED = 0x0badf00d
  256| SEEDS = (D_PFSR_SEED, D_PFAR_SEED, I_PFSR_SEED, I_PFAR_SEED)
  257| IDR = (5 << 21) | (9 << 16)                 # 0x00a90000: (M88200_ID << 21) | (9 << 16)
  258| BERROR = 3 << 16                            # CMMU_PFSR_BERROR << 16 = 0x00030000
  259| OFF_IDR, OFF_PFSR, OFF_PFAR = 0x000, 0x108, 0x10c
  260| MV_DCMMU, MV_ICMMU = 0xfff7f000, 0xfff77000   # MVME187_SBC_CMMU_D / _I
  261| LU_DCMMU, LU_ICMMU = 0xfff06000, 0xfff07000   # CMMU_D0 / CMMU_I0
  262| UNREAD = 0xfff46010         # inside `unreadable addr=0xfff46000 len=0x1000': device-relative 0x10
  263| VME = 0xfff40000            # VME2_BASE
  264| VME_P1 = VME + 0x90         # population 1 (#568's FAULT): device-relative 0x90
  265| VME_VBR = VME + 0x88        # VME2_VBR, a CASED register: an accepted access
  266| VBR_SEED = 0x67000000       # dev_vme.c DEVINIT: VME2_SET_VBR0(6) + VME2_SET_VBR1(7)
  267| LUNA_PROBE = 0x3ffffff0     # LUNA88K_REGISTERS_BASE == the `case 0x3ffffff0' label
  268| UNCLAIMED = 0x10000000      # INFO only: past mvme187's 64 MB, below its lowest device (0xff780000)
  269| STVAL = 0xa5a5a5a5
  270| ACCESS_PC = CODE + 4 * 10
  271| SXIP_DATA = ACCESS_PC | 0x2               # M88K_XIP_V
  272| SXIP_IFETCH = UNREAD | 0x2 | 0x1          # M88K_XIP_V | M88K_XIP_E: an instruction access at 0xfff46010
  273| H_END = H + 4 * 5
  274| NSTEPS = 19                               # 10 + access + 2 (vector or fall-through) + 6 handler
  275| #  the `null' session (mvme187 -n 2): cpu 1's own code, vectors and RAM markers
  276| CODE1 = 0x00010200
  277| J = CODE1 + 12                            # cpu 1's `jmp (r5)': the instruction refusal
  278| VBR1 = 0x00030000                         # cpu 1's VBR, set by the debugger (4 KB aligned)
  279| VBR1_IACC, VBR1_DACC, VBR1_ERROR = VBR1 + 8 * 2, VBR1 + 8 * 3, VBR1 + 8 * 10
  280| MARK_H, MARK_F = 0x0000f000, 0x0000f004   # RAM: below CODE, above both vector tables' first page
  281| HANDLED_V, FELL_V = 0x4a4a4a4a, 0x46464646
  282| SXIP_NULL = CODE1 | 0x2                   # cpu 1's refused data load at CODE1
  283| PROMPT = "GXemul> "
  284| RIG_IMG = "liveimage-luna88k-raw-20250518.img"
  285| 
  286| 
  287| # ------------------------------------------------------------------- encodings
  288| class Ins(object):
  289|     __slots__ = ("word", "mnem", "ops")
  290| 
  291|     def __init__(self, word, mnem, ops):
  292|         self.word, self.mnem, self.ops = word, mnem, ops
  293| 
  294| 
  295| def enc(op26, rd, rs1, imm):
  296|     assert 0 <= op26 < 64 and 0 <= rd < 32 and 0 <= rs1 < 32 and 0 <= imm <= 0xffff
  297|     return (op26 << 26) | (rd << 21) | (rs1 << 16) | imm
  298| 
  299| 
  300| def LD(rd, rs1, off):       # op26 0x05 (vme_default_probe.py's table)
  301|     return Ins(enc(0x05, rd, rs1, off), "ld", "r%d,r%d,0x%x" % (rd, rs1, off))
  302| 
  303| 
  304| def ST(rs, rs1, off):       # op26 0x09
  305|     return Ins(enc(0x09, rs, rs1, off), "st", "r%d,r%d,0x%x" % (rs, rs1, off))
  306| 
  307| 
  308| def OR_I(rd, rs1, imm):     # op26 0x16; the disassembler prints this immediate in hex
  309|     assert rd != 0
  310|     return Ins(enc(0x16, rd, rs1, imm), "or", "r%d,r%d,0x%x" % (rd, rs1, imm))
  311| 
  312| 
  313| def BR_TO(frm, to):         # op26 0x30, d26 = (to - frm) / 4
  314|     return Ins(0xc0000000 | (((to - frm) >> 2) & 0x3ffffff), "br", "0x%08x" % to)
  315| 
  316| 
  317| def BR_SELF():              # d26 = 0; the operand is filled in on placement
  318|     return Ins(0xc0000000, "br", None)
  319| 
  320| 
  321| def JMP(rs2):               # jmp (rS2) = 0xf400c000 | rs2 (luna88kprom.c's `jmp (r1)' = 0xf400c001)
  322|     return Ins(0xf400c000 | rs2, "jmp", "(r%d)" % rs2)
  323| 
  324| 
  325| def blocks_for(access):
  326|     vec = [(VEC_IACC, [OR_I(7, 0, 2), BR_TO(VEC_IACC + 4, H)]),
  327|            (VEC_DACC, [OR_I(7, 0, 3), BR_TO(VEC_DACC + 4, H)])]
  328|     code = [LD(10, 3, OFF_IDR), LD(9, 2, OFF_IDR),
  329|             ST(20, 3, OFF_PFSR), ST(21, 3, OFF_PFAR), ST(22, 2, OFF_PFSR), ST(23, 2, OFF_PFAR),
  330|             LD(11, 3, OFF_PFSR), LD(12, 3, OFF_PFAR), LD(17, 2, OFF_PFSR), LD(18, 2, OFF_PFAR),
  331|             access,
  332|             OR_I(6, 0, FALL), BR_TO(CODE + 4 * 12, H)]
  333|     assert CODE + 4 * code.index(access) == ACCESS_PC
  334|     hnd = [LD(13, 3, OFF_PFSR), LD(14, 3, OFF_PFAR), LD(15, 2, OFF_PFSR), LD(16, 2, OFF_PFAR),
  335|            OR_I(31, 0, LIVE), BR_SELF()]
  336|     assert H + 4 * (len(hnd) - 1) == H_END
  337|     return vec + [(CODE, code), (H, hnd)]
  338| 
  339| 
  340| def null_cpu1_blocks():
  341|     """cpu 1's code and vectors in the `null' session.  CODE1: the refused DATA load, the FELL store (reached only if
  342|        the load raised nothing), br J; J: the instruction refusal.  VBR1 + 0x18 (vector 3): the HANDLED store, br J.
  343|        VBR1 + 0x10 (vector 2) and VBR1 + 0x50 (ERROR, 10): park."""
  344|     code1 = [LD(4, 5, 0), ST(21, 0, MARK_F), BR_TO(CODE1 + 8, J), JMP(5)]
  345|     assert CODE1 + 4 * 3 == J
  346|     return [(CODE1, code1),
  347|             (VBR1_IACC, [BR_SELF()]),
  348|             (VBR1_DACC, [ST(20, 0, MARK_H), BR_TO(VBR1_DACC + 4, J)]),
  349|             (VBR1_ERROR, [BR_SELF()])]
  350| 
  351| 
  352| # ------------------------------------------------------------------- sessions
  353| def hx(v):
  354|     return "absent" if v is None else "0x%x" % v
  355| 
  356| 
  357| def argv_for(machine):
  358|     if machine == "mvme187":
  359|         return [BIN, "-V", "-x", "-E", "mvme88k", "-e", "mvme187", "-M", "64", "0x%x:%s" % (CODE, DUMMY)], None
  360|     if machine == "mvme187-n2":     # the documented cpu-count option; cpu 1 gets no CMMU (dev_mvme187.c)
  361|         return ([BIN, "-V", "-x", "-E", "mvme88k", "-e", "mvme187", "-M", "64", "-n", "2", "0x%x:%s" % (CODE, DUMMY)],
  362|                 None)
  363|     if machine == "187":            # the apparatus negative control: no such subtype
  364|         return [BIN, "-V", "-x", "-E", "mvme88k", "-e", "187", "-M", "64", "0x%x:%s" % (CODE, DUMMY)], None
  365|     if machine == "luna-88k":
  366|         if IMAGES:
  367|             return ([BIN, "-V", "-x", "-e", "luna-88k", "-d", "R:" + os.path.join(IMAGES, RIG_IMG), "boot"],
  368|                     IMAGES)
  369|         return [BIN, "-V", "-x", "-E", "luna88k", "-e", "luna-88k", "0x%x:%s" % (CODE, DUMMY)], None
  370|     raise ValueError(machine)
  371| 
  372| 
  373| def seeds(pairs):
  374|     return ["r%d=0x%x" % (r, v) for r, v in pairs]
  375| 
  376| 
  377| def place(blocks):
  378|     """blocks: [(addr, [Ins])] -> (debugger commands, [(addr, Ins)]).  Every block is re-read with
  379|        `unassemble' (end-exclusive) right after it is written."""
  380|     cmds, placed = [], []
  381|     for at, insns in blocks:
  382|         for i, ins in enumerate(insns):
  383|             a = at + 4 * i
  384|             if ins.ops is None:
  385|                 ins = Ins(ins.word, ins.mnem, "0x%08x" % a)
  386|             cmds.append("put w 0x%x, 0x%08x" % (a, ins.word))
  387|             placed.append((a, ins))
  388|         cmds.append("unassemble 0x%x 0x%x" % (at, at + 4 * len(insns)))
  389|     return cmds, placed
  390| 
  391| 
  392| def run_piped(machine, cmds, tag, timeout=90):
  393|     argv, cwd = argv_for(machine)
  394|     inp = ("\n".join(list(cmds) + ["quit"]) + "\n").encode("latin-1")
  395|     try:
  396|         p = subprocess.run(argv, input=inp, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout,
  397|                            cwd=cwd)
  398|         text = p.stdout.decode("latin-1", "replace").replace("\r", "")
  399|         rc = p.returncode
  400|         how = ("sig%d" % -rc) if rc < 0 else ("exit%d" % rc)
  401|     except subprocess.TimeoutExpired as e:
  402|         text, how = (e.output or b"").decode("latin-1", "replace").replace("\r", ""), "TIMEOUT"
  403|     if DUMP:
  404|         with open(os.path.join(DUMP, "%s.txt" % tag), "w") as f:
  405|             f.write("# argv: %s\n# cwd: %s\n# how: %s\n" % (" ".join(argv), cwd, how))
  406|             f.write(text)
  407|     return text, how
  408| 
  409| 
  410| DIS_RE = re.compile(r"^[su]([0-9a-f]{8}): ([0-9a-f]{8})\s+(?:<-\s+)?(\S+)(?:\t(\S+))?[ \t]*$", re.M)
  411| GPR_RE = re.compile(r"\br(\d+)\s*=\s*(0x[0-9a-fA-F]+)")
  412| PC_RE = re.compile(r"cpu\d+:\s+pc\s+=\s+(0x[0-9a-fA-F]+)")
  413| CR_RE = re.compile(r"\b([A-Z][A-Z0-9]*)=(0x[0-9a-fA-F]+)")
  414| 
  415| 
  416| class Res(object):
  417|     pass
  418| 
  419| 
  420| def parts_of(text):
  421|     """[(command, output)] in transcript order (the text after each prompt, split at its first newline)."""
  422|     out = []
  423|     for part in text.split(PROMPT)[1:]:
  424|         cmd, _, o = part.partition("\n")
  425|         out.append((cmd.strip(), o))
  426|     return out
  427| 
  428| 
  429| def regs_of(o):
  430|     """(pc, {gpr: value}) from one `reg' output, or (None, None) when it holds no register dump."""
  431|     m = PC_RE.search(o)
  432|     if not m:
  433|         return None, None
  434|     return int(m.group(1), 16), {int(g.group(1)): int(g.group(2), 16) for g in GPR_RE.finditer(o)}
  435| 
  436| 
  437| def crs_of(o):
  438|     return {g.group(1): int(g.group(2), 16) for g in CR_RE.finditer(o)}
  439| 
  440| 
  441| def analyse(text, how, placed):
  442|     """Split the transcript at the prompts; parse every unassemble, the last `reg' and the last `reg 0,0'."""
  443|     r = Res()
  444|     r.how, r.text, r.placed = how, text, placed
  445|     r.dis, r.regs, r.pc, r.cr = {}, None, None, None
  446|     for cmd, out in parts_of(text):
  447|         if cmd.startswith("unassemble"):
  448|             for m in DIS_RE.finditer(out):
  449|                 r.dis[int(m.group(1), 16)] = (int(m.group(2), 16), m.group(3), m.group(4) or "")
  450|         elif cmd == "reg":
  451|             pc, gp = regs_of(out)
  452|             if pc is not None:
  453|                 r.regs, r.pc = gp, pc
  454|         elif cmd == "reg 0,0":
  455|             cr = crs_of(out)
  456|             if cr:
  457|                 r.cr = cr
  458|     return r
  459| 
  460| 
  461| UNASM = {"ok": 0, "n": 0, "bad": []}
  462| 
  463| 
  464| def check_unasm(r, scored=True):
  465|     ok = n = 0
  466|     for a, ins in r.placed:
  467|         n += 1
  468|         d = r.dis.get(a)
  469|         if d is not None and d == (ins.word, ins.mnem, ins.ops):
  470|             ok += 1
  471|         elif scored:
  472|             UNASM["bad"].append("0x%x:%08x %s %s -> %r" % (a, ins.word, ins.mnem, ins.ops, d))
  473|     if scored:
  474|         UNASM["ok"] += ok
  475|         UNASM["n"] += n
  476|     return ok, n
  477| 
  478| 
  479| def std_regs(dcmmu, icmmu, extra):
  480|     regs = [(2, icmmu), (3, dcmmu), (20, D_PFSR_SEED), (21, D_PFAR_SEED), (22, I_PFSR_SEED), (23, I_PFAR_SEED)]
  481|     return regs + [(rr, SENT) for rr in (4, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 31)] + extra
  482| 
  483| 
  484| def session(tag, machine, dcmmu, icmmu, access, extra, scored=True):
  485|     cmds, placed = place(blocks_for(access))
  486|     cmds = seeds(std_regs(dcmmu, icmmu, extra)) + cmds + ["pc=0x%x" % CODE, "step %d" % NSTEPS, "reg", "reg 0,0"]
  487|     t, how = run_piped(machine, cmds, tag)
  488|     r = analyse(t, how, placed)
  489|     check_unasm(r, scored)
  490|     return r
  491| 
  492| 
  493| TIMEOUTS = ("TIMEOUT",)
  494| 
  495| 
  496| def died(r):
  497|     return ("timeout:%s" if r.how in TIMEOUTS else "died:%s") % r.how
  498| 
  499| 
  500| def g(r, n):
  501|     return r.regs.get(n) if r.regs is not None else None
  502| 
  503| 
  504| def prereq_bad(r):
  505|     """None when the session's own prerequisites held; else a cause-free reason (the row stays red)."""
  506|     if r.regs is None:
  507|         return died(r)
  508|     if g(r, 10) != IDR or g(r, 9) != IDR:
  509|         return "nodev d=%s i=%s: device signature absent, check not made" % (hx(g(r, 10)), hx(g(r, 9)))
  510|     back = (g(r, 11), g(r, 12), g(r, 17), g(r, 18))
  511|     if back != SEEDS:
  512|         return "readback %s: seeds did not round-trip, check not made" % "/".join(hx(v) for v in back)
  513|     if r.pc != H_END or g(r, 31) != LIVE:
  514|         return "handler pc=%s r31=%s: the reads did not complete" % (hx(r.pc), hx(g(r, 31)))
  515|     return None
  516| 
  517| 
  518| def path_of(r):
  519|     v7, v6 = g(r, 7), g(r, 6)
  520|     if v7 == 3 and v6 == SENT:
  521|         return "v3"
  522|     if v7 == 2 and v6 == SENT:
  523|         return "v2"
  524|     if v7 == SENT and v6 == FALL:
  525|         return "fall"
  526|     return "odd(r6=%s,r7=%s)" % (hx(v6), hx(v7))
  527| 
  528| 
  529| def route(r, load):
  530|     cr = r.cr or {}
  531|     s = "%s/%s/%s" % (path_of(r), hx(cr.get("SXIP")), hx(cr.get("DMA0")))
  532|     if load and g(r, 4) != SENT:
  533|         s += " r4=%s" % hx(g(r, 4))
  534|     return s
  535| 
  536| 
  537| def kept_i(r):
  538|     """'kept' when the instruction CMMU's PFSR/PFAR still hold their seeds after the access."""
  539|     if (g(r, 15), g(r, 16)) == (I_PFSR_SEED, I_PFAR_SEED):
  540|         return "kept"
  541|     return "ipfsr=%s ipfar=%s" % (hx(g(r, 15)), hx(g(r, 16)))
  542| 
  543| 
  544| def kept_d(r):
  545|     """'kept' when the data CMMU's PFSR/PFAR still hold their seeds after the access."""
  546|     if (g(r, 13), g(r, 14)) == (D_PFSR_SEED, D_PFAR_SEED):
  547|         return "kept"
  548|     return "dpfsr=%s dpfar=%s" % (hx(g(r, 13)), hx(g(r, 14)))
  549| 
  550| 
  551| DUMP16_RE = re.compile(r"^0x([0-9a-f]{8})  ((?:[0-9a-f]{8} ?){1,4})", re.M)
  552| 
  553| 
  554| def dump_words(o, addr):
  555|     """The 32-bit words a `dump' line printed for `addr', or 'failed' / None."""
  556|     for line in o.splitlines():
  557|         if line.startswith("0x%08x  " % addr):
  558|             if "(memory access failed)" in line:
  559|                 return "failed"
  560|             m = DUMP16_RE.match(line)
  561|             if m:
  562|                 return [int(w, 16) for w in m.group(2).split()]
  563|     return None
  564| 
  565| 
  566| rows = []
  567| SYMPTOM = []                # (row name, classification)
  568| 
  569| 
  570| def row(name, got, want, note=""):
  571|     assert name not in [n for n, _ in rows], "DUPLICATE ROW NAME %r" % name
  572|     assert len(name) <= 15, name     # `%-16s ' keeps a gate's `^$v  .*ok$' satisfiable
  573|     ok = (got == want)
  574|     rows.append((name, ok))
  575|     print("%-16s %-34s %-34s %-62s %s" % (name, str(got), str(want), note, "ok" if ok else "FAIL"))
  576|     sys.stdout.flush()
  577|     return ok
  578| 
  579| 
  580| def symptom(name, got, want, stale):
  581|     SYMPTOM.append((name, "FIXED" if got == want else ("STALE" if got == stale else "OTHER")))
  582| 
  583| 
  584| print("m88kbuserrregs RUNG-3 DETECTOR (revision %d) -- binary=%s label=%s" % (REVISION, BIN, LABEL))
  585| print("machines: -E mvme88k -e mvme187 -M 64 [-n 2] and -E luna88k -e luna-88k (UNMODIFIED); luna shape: %s"
  586|       % ("rig (%s)" % IMAGES if IMAGES else "dummy raw image at 0x%x" % CODE))
  587| print("seeds: dPFSR=%s dPFAR=%s iPFSR=%s iPFAR=%s; want BERROR<<16=%s" % (tuple(hx(v) for v in SEEDS) + (hx(BERROR),)))
  588| t0 = time.time()
  589| print("%-16s %-34s %-34s %-62s %s" % ("row", "got", "want", "note", ""))
  590| 
  591| # ================================================================ apparatus
  592| #  APPARATUS NEGATIVE CONTROL: the session oracle must be able to go red.
  593| cmds, _ = place([(CODE, [OR_I(4, 0, LIVE), BR_SELF()])])
  594| t, how = run_piped("187", seeds([(4, SENT)]) + cmds + ["pc=0x%x" % CODE, "step 1", "reg"], "neg_apparatus")
  595| rn = analyse(t, how, [])
  596| row("neg apparatus", "%s/%s" % (how, hx(g(rn, 4))), "exit1/absent",
  597|     "bogus subtype `187' -> no machine -> no register dump")
  598| 
  599| # ================================================================ accept side (mvme187): an ACCEPTED device access
  600| r_ok = session("ok", "mvme187", MV_DCMMU, MV_ICMMU, LD(4, 5, 0), [(5, VME_VBR)])
  601| bad = prereq_bad(r_ok)
  602| row("mv devsig", died(r_ok) if r_ok.regs is None else "%s/%s" % (hx(g(r_ok, 10)), hx(g(r_ok, 9))),
  603|     "%s/%s" % (hx(IDR), hx(IDR)), "DEVICE SIGNATURE: mvme187 data/instr CMMU IDR (RAM reads 0)")
  604| row("mv cmmu rt", died(r_ok) if r_ok.regs is None else "/".join(hx(g(r_ok, n)) for n in (11, 12, 17, 18)),
  605|     "/".join(hx(v) for v in SEEDS), "LIVENESS: four seeds stored and read back via the CMMU decode")
  606| row("ok route", bad if bad else "%s/r4=%s" % (path_of(r_ok), hx(g(r_ok, 4))), "fall/r4=%s" % hx(VBR_SEED),
  607|     "ld VME VBR 0xfff40088 (cased): served 0x67000000, no exception")
  608| row("ok regs", bad if bad else "/".join(hx(g(r_ok, n)) for n in (13, 14, 15, 16)), "/".join(hx(v) for v in SEEDS),
  609|     "an ACCEPTED device access writes no fault metadata")
  610| 
  611| 
  612| # ================================================================ generic arm: three refused accesses (mvme187)
  613| def refused(tag, access, extra, addr, load, what):
  614|     r = session(tag, "mvme187", MV_DCMMU, MV_ICMMU, access, extra)
  615|     bad = prereq_bad(r)
  616|     w_route = "v3/%s/%s" % (hx(SXIP_DATA), hx(addr & ~3))
  617|     g_route = bad if bad else route(r, load)
  618|     g_pfsr = bad if bad else hx(g(r, 13))
  619|     g_pfar = bad if bad else hx(g(r, 14))
  620|     row(tag + " route", g_route, w_route, "%s: vector 3, SXIP, DMA0 -- the exception is THIS access" % what)
  621|     row(tag + " pfsr", g_pfsr, hx(BERROR), "data CMMU PFSR after the fault (seeded %s)" % hx(D_PFSR_SEED))
  622|     row(tag + " pfar", g_pfar, hx(addr), "data CMMU PFAR after the fault (seeded %s)" % hx(D_PFAR_SEED))
  623|     row(tag + " icmmu", bad if bad else kept_i(r), "kept", "instruction CMMU PFSR/PFAR keep their seeds")
  624|     symptom(tag + " pfsr", g_pfsr, hx(BERROR), hx(D_PFSR_SEED))
  625|     symptom(tag + " pfar", g_pfar, hx(addr), hx(D_PFAR_SEED))
  626|     return r
  627| 
  628| 
  629| refused("uld", LD(4, 5, 0), [(5, UNREAD)], UNREAD, True, "ld 0xfff46010 (unreadable)")
  630| refused("ust", ST(8, 5, 0), [(5, UNREAD), (8, STVAL)], UNREAD, False, "st 0xfff46010 (unreadable)")
  631| refused("vme", LD(4, 5, 0), [(5, VME_P1)], VME_P1, True, "ld 0xfff40090 (VME pop. 1)")
  632| 
  633| # ================================================================ the LUNA probe address (luna-88k)
  634| r_lu = session("luna", "luna-88k", LU_DCMMU, LU_ICMMU, LD(4, 5, 0), [(5, LUNA_PROBE)])
  635| bad = prereq_bad(r_lu)
  636| row("luna devsig", died(r_lu) if r_lu.regs is None else "%s/%s" % (hx(g(r_lu, 10)), hx(g(r_lu, 9))),
  637|     "%s/%s" % (hx(IDR), hx(IDR)), "DEVICE SIGNATURE: luna-88k data/instr CMMU IDR")
  638| row("luna cmmu rt", died(r_lu) if r_lu.regs is None else "/".join(hx(g(r_lu, n)) for n in (11, 12, 17, 18)),
  639|     "/".join(hx(v) for v in SEEDS), "LIVENESS: the four seeds read back")
  640| if bad:
  641|     g_lr = bad
  642| else:
  643|     cr = r_lu.cr or {}
  644|     g_lr = "%s/%s/%s/r4=%s" % (path_of(r_lu), hx(cr.get("SXIP")), hx(cr.get("DMA0")), hx(g(r_lu, 4)))
  645| w_lr = "v3/%s/%s/r4=%s" % (hx(SXIP_DATA), hx(LUNA_PROBE), hx(SENT))
  646| row("luna route", g_lr, w_lr, "ld 0x3ffffff0: a refused access raises vector 3, serves nothing")
  647| g_lpfsr = bad if bad else hx(g(r_lu, 13))
  648| g_lpfar = bad if bad else hx(g(r_lu, 14))
  649| row("luna pfsr", g_lpfsr, hx(BERROR), "data CMMU PFSR (seeded %s)" % hx(D_PFSR_SEED))
  650| row("luna pfar", g_lpfar, hx(LUNA_PROBE), "data CMMU PFAR (seeded %s)" % hx(D_PFAR_SEED))
  651| row("luna icmmu", bad if bad else kept_i(r_lu), "kept", "instruction CMMU PFSR/PFAR keep their seeds")
  652| SYMPTOM.append(("luna route", "FIXED" if g_lr == w_lr else
  653|                 ("STALE" if g_lr == "fall/0x0/0x0/r4=0x0" else "OTHER")))
  654| symptom("luna pfar", g_lpfar, hx(LUNA_PROBE), hx(D_PFAR_SEED))
  655| 
  656| # ================================================================ the INSTRUCTION label (mvme187): B5a
  657| #  Stepped, the step loop's disassembly pre-read reaches the arm with CACHE_INSTRUCTION (R2, disclosed in the header):
  658| #  the selector picks cmmu[0], and vector 2 runs its marker code.  `ifetch route' is an ATTRIBUTION row: the vector
  659| #  expression reads `cache' on its own, so it cannot see the selector; `ifetch pfsr/pfar' carry the selector variant.
  660| r_if = session("ifetch", "mvme187", MV_DCMMU, MV_ICMMU, JMP(5), [(5, UNREAD)])
  661| bad = prereq_bad(r_if)
  662| cri = r_if.cr or {}
  663| g_ir = bad if bad else "%s/%s/%s" % (path_of(r_if), hx(cri.get("SXIP")), hx(cri.get("DMA0")))
  664| row("ifetch route", g_ir, "v2/%s/%s" % (hx(SXIP_IFETCH), hx(0)),
  665|     "jmp (r5) to 0xfff46010: vector 2, SXIP|V|E, no data unit (attribution row)")
  666| g_ipfsr = bad if bad else hx(g(r_if, 15))
  667| g_ipfar = bad if bad else hx(g(r_if, 16))
  668| row("ifetch pfsr", g_ipfsr, hx(BERROR), "INSTRUCTION CMMU PFSR after the refused fetch (seeded %s)" % hx(I_PFSR_SEED))
  669| row("ifetch pfar", g_ipfar, hx(UNREAD), "INSTRUCTION CMMU PFAR after the refused fetch (seeded %s)" % hx(I_PFAR_SEED))
  670| row("ifetch dcmmu", bad if bad else kept_d(r_if), "kept", "the DATA CMMU keeps its seeds after an instruction refusal")
  671| symptom("ifetch pfsr", g_ipfsr, hx(BERROR), hx(I_PFSR_SEED))
  672| symptom("ifetch pfar", g_ipfar, hx(UNREAD), hx(I_PFAR_SEED))
  673| 
  674| # ================================================================ a NO_EXCEPTIONS caller (mvme187, its own session): B5b
  675| #  The `ok' program, with the debugger's `dump' of the unreadable window between the readbacks (step 10) and the
  676| #  accepted access.  The dump runs on cpus[bootstrap_cpu] with CACHE_NONE | NO_EXCEPTIONS: the device is not called,
  677| #  res 0 -> -1, and the arm's `!no_exceptions' term keeps its body out -- zeros, no vector, no CMMU write.  A later
  678| #  fault would overwrite the evidence, so the session has none: its access is the accepted VBR load.
  679| _cmds, _placed = place(blocks_for(LD(4, 5, 0)))
  680| _cmds = seeds(std_regs(MV_DCMMU, MV_ICMMU, [(5, VME_VBR)])) + _cmds + \
  681|     ["pc=0x%x" % CODE, "step 10", "dump 0x%x 0x%x" % (UNREAD, UNREAD + 16), "reg", "step 9", "reg", "reg 0,0"]
  682| t, how = run_piped("mvme187", _cmds, "dbg")
  683| r_db = analyse(t, how, _placed)
  684| check_unasm(r_db)
  685| _dump_o = [o for c, o in parts_of(t) if c.startswith("dump")]
  686| _reg_o = [o for c, o in parts_of(t) if c == "reg"]
  687| bad = prereq_bad(r_db)
  688| if bad:
  689|     g_db = bad
  690| elif not _dump_o or len(_reg_o) < 2:
  691|     g_db = "nodump: the dump or the post-dump reg produced no output"
  692| else:
  693|     _w = dump_words(_dump_o[0], UNREAD)
  694|     _dcls = ("failed" if _w == "failed" else "zeros" if _w == [0, 0, 0, 0] else
  695|              "nodump" if _w is None else "other(%s)" % "/".join(hx(v) for v in _w))
  696|     _pca, _ = regs_of(_reg_o[0])
  697|     _kept = ("kept" if tuple(g(r_db, n) for n in (13, 14, 15, 16)) == SEEDS else
  698|              "/".join(hx(g(r_db, n)) for n in (13, 14, 15, 16)))
  699|     g_db = "%s/%s/%s/%s" % (_dcls, hx(_pca), path_of(r_db), _kept)
  700| row("dbg noexc", g_db, "zeros/%s/fall/kept" % hx(ACCESS_PC),
  701|     "debugger dump of 0xfff46010: zeros, no vector, seeds survive")
  702| 
  703| # ================================================================ a CMMU-LESS cpu (mvme187 -n 2, cpu 1): B5c, conjunctive
  704| #  cpu 0: the seeded `uld' program, alone, then parked (nothing scored from it -- its results are printed as INFO).
  705| #  cpu 1: part 1 the refused DATA load (cmmu[1] NULL), part 2 the refused INSTRUCTION fetch (cmmu[0] NULL; delivered as
  706| #  ERROR because the data fault left PSR.SFRZ set -- see the header).  Prerequisites are cpu 1's own.
  707| _blocks = blocks_for(LD(4, 5, 0)) + null_cpu1_blocks()
  708| _cmds, _placed = place(_blocks)
  709| _c1 = ["focus 1"] + seeds([(5, UNREAD), (20, HANDLED_V), (21, FELL_V), (4, SENT)]) + \
  710|     ["VBR=0x%x" % VBR1, "pc=0x%x" % CODE1, "focus 0"]
  711| _cmds = seeds(std_regs(MV_DCMMU, MV_ICMMU, [(5, UNREAD)])) + _cmds + \
  712|     ["put w 0x%x, 0x0" % MARK_H, "put w 0x%x, 0x0" % MARK_F, "pc=0x%x" % CODE, "step %d" % NSTEPS, "reg 0",
  713|      "tlbdump 1"] + _c1 + \
  714|     ["pause 1", "step 3", "dump 0x%x 0x%x" % (MARK_H, MARK_H + 8), "reg 1", "reg 1,0",
  715|      "step 5", "dump 0x%x 0x%x" % (MARK_H, MARK_H + 8), "reg 1"]
  716| t, how = run_piped("mvme187-n2", _cmds, "null")
  717| r_nl = analyse(t, how, _placed)
  718| check_unasm(r_nl)
  719| _ps = parts_of(t)
  720| _tlb1 = [o for c, o in _ps if c == "tlbdump 1"]
  721| _dumps = [o for c, o in _ps if c.startswith("dump")]
  722| _r1 = [o for c, o in _ps if c == "reg 1"]
  723| _cr1 = [o for c, o in _ps if c == "reg 1,0"]
  724| _r0 = [o for c, o in _ps if c == "reg 0"]
  725| 
  726| 
  727| def _marks(o):
  728|     w = dump_words(o, MARK_H)
  729|     if not isinstance(w, list) or len(w) < 2:
  730|         return None
  731|     hm, fm = w[0], w[1]
  732|     if hm == HANDLED_V and fm == 0:
  733|         return "handled"
  734|     if fm == FELL_V and hm == 0:
  735|         return "fell"
  736|     if hm == HANDLED_V and fm == FELL_V:
  737|         return "both"
  738|     if hm == 0 and fm == 0:
  739|         return "neither"
  740|     return "odd(%s/%s)" % (hx(hm), hx(fm))
  741| 
  742| 
  743| _m1 = _marks(_dumps[0]) if len(_dumps) >= 1 else None
  744| _m2 = _marks(_dumps[1]) if len(_dumps) >= 2 else None
  745| _pc1a = regs_of(_r1[0])[0] if len(_r1) >= 1 else None
  746| _pc1b = regs_of(_r1[1])[0] if len(_r1) >= 2 else None
  747| _crn = crs_of(_cr1[0]) if _cr1 else {}
  748| if not _tlb1:
  749|     _premise = "premise: no `tlbdump 1' output, the NULL cell was not shown"
  750| elif "cpu1: CMMU" in _tlb1[0]:
  751|     _premise = "premise: cpu1 has a CMMU, the cell under test is not the NULL cell"
  752| else:
  753|     _premise = None
  754| #  the failed-access lines the arm prints after part 1's marker dump: the instruction refusal reached the arm
  755| _after1 = t.split("dump 0x%x" % MARK_H, 1)[1] if ("dump 0x%x" % MARK_H) in t else ""
  756| _after1 = _after1.split("\n", 1)[1] if "\n" in _after1 else ""
  757| _after1 = _after1.split("dump 0x%x" % MARK_H, 1)[0]
  758| 
  759| if _m1 is None:
  760|     g_nr = died(r_nl) if how != "exit0" else "nodump: part 1's marker dump produced no marker line"
  761| elif _premise:
  762|     g_nr = _premise
  763| elif _pc1a != J:
  764|     g_nr = "cpu1 pc=%s after part 1: it did not reach J (0x%x), check not made" % (hx(_pc1a), J)
  765| else:
  766|     g_nr = "%s/%s/%s" % (_m1, hx(_crn.get("SXIP")), hx(_crn.get("DMA0")))
  767| if how != "exit0":
  768|     g_ns = died(r_nl)
  769| elif _premise:
  770|     g_ns = _premise
  771| elif _pc1a != J:
  772|     g_ns = "cpu1 pc=%s after part 1: the fetch at J was never reached, check not made" % hx(_pc1a)
  773| elif _pc1b is None or _pc1b == J:
  774|     g_ns = "cpu1 pc=%s after part 2: the fetch was not attempted, check not made" % hx(_pc1b)
  775| elif "failed ]" not in _after1:
  776|     g_ns = "part 2 printed no failed-access line: the instruction refusal did not reach the arm, check not made"
  777| else:
  778|     g_ns = "%s/%s" % (how, "readable" if (_m1 is not None and _m2 is not None) else "unreadable")
  779| row("null surv", g_ns, "exit0/readable",
  780|     "-n 2 cpu 1 (no CMMU): alive after the data AND instruction refusals")
  781| row("null route", g_nr, "handled/%s/%s" % (hx(SXIP_NULL), hx(UNREAD)),
  782|     "cpu 1's refused load: HANDLED set, FELL clear, SXIP, DMA0")
  783| _pc0, _g0 = regs_of(_r0[0]) if _r0 else (None, None)
  784| _g0 = _g0 or {}
  785| _v76 = (_g0.get(7), _g0.get(6))
  786| _p0 = "absent" if not _g0 else "v3" if _v76 == (3, SENT) else "fall" if _v76 == (SENT, FALL) else "odd"
  787| print("INFO null cpu0   (unscored) pc=%s path=%s dPFSR=%s dPFAR=%s r31=%s; cpu1 end pc=%s markers-after-part2=%s"
  788|       % (hx(_pc0), _p0, hx(_g0.get(13)), hx(_g0.get(14)), hx(_g0.get(31)), hx(_pc1b), _m2))
  789| 
  790| # ================================================================ INFO (unscored): an UNCLAIMED physical address
  791| #  An UNCLAIMED physical address never reaches the refused-access arm (the premise correction in the header).
  792| ru = session("info_unclaimed", "mvme187", MV_DCMMU, MV_ICMMU, LD(4, 5, 0), [(5, UNCLAIMED)], scored=False)
  793| cru = ru.cr or {}
  794| print("INFO unclaimed   ld 0x%08x (no device, past RAM): how=%s path=%s r4=%s SXIP=%s dPFSR=%s dPFAR=%s "
  795|       "iPFSR=%s iPFAR=%s non-existant-msg=%d unasm=%d/%d"
  796|       % (UNCLAIMED, ru.how, path_of(ru) if ru.regs else "absent", hx(g(ru, 4)), hx(cru.get("SXIP")),
  797|          hx(g(ru, 13)), hx(g(ru, 14)), hx(g(ru, 15)), hx(g(ru, 16)), ru.text.count("non-existant"),
  798|          *check_unasm(ru, scored=False)))
  799| 
  800| # ================================================================ disassembly cross-check
  801| #  LITERAL want, derived by hand from the final program listing BEFORE the first run (BUILD_SPEC.md section 11, Q9):
  802| #  each standard scored session places 23 words (vectors 2 + 2, CODE 13, handler 6) -- ok, uld, ust, vme, luna,
  803| #  ifetch and dbg: 7 x 23 = 161; the null session places those 23 plus cpu 1's 8 (CODE1 4, VBR1+0x10 1, VBR1+0x18 2,
  804| #  VBR1+0x50 1) = 31.  161 + 31 = 192.  The apparatus session and INFO unclaimed are not counted.  Computing it from
  805| #  the session list would let a shrunk list pass its own count.
  806| row("unasm", "%d/%d" % (UNASM["ok"], UNASM["n"]), "192/192", "every placed word re-read by the disassembler")
  807| for b in UNASM["bad"][:8]:
  808|     print("  unasm mismatch: %s" % b)
  809| 
  810| # ================================================================ score + done
  811| npass = sum(1 for _, ok in rows if ok)
  812| print("SCORE %d/%d" % (npass, len(rows)))
  813| CONTROL_ROWS = ("neg apparatus", "mv devsig", "mv cmmu rt", "luna devsig", "luna cmmu rt", "unasm")
  814| _status = dict(rows)
  815| control_ok = all(_status.get(n, False) for n in CONTROL_ROWS)    # a renamed control fails loudly
  816| assert len(SYMPTOM) == 10, SYMPTOM
  817| _cls = [c for _, c in SYMPTOM]
  818| if all(c == "STALE" for c in _cls):
  819|     sym = "PRESENT %d/10" % len(_cls)
  820| elif all(c == "FIXED" for c in _cls):
  821|     sym = "ABSENT"
  822| else:
  823|     sym = "MIXED " + ",".join("%s=%s" % (n, c) for n, c in SYMPTOM)
  824| print("M88K_BUSERR_RESULT=%d/%d" % (npass, len(rows)))
  825| print("M88K_BUSERR_CONTROL=%s" % ("OK" if control_ok else "FAIL"))
  826| print("M88K_BUSERR_SYMPTOM=%s" % sym)
  827| print("M88K_BUSERR_REVISION=%d" % REVISION)
  828| print("M88K_BUSERR_LABEL=%s" % LABEL)
  829| print("M88K_BUSERR_ELAPSED=%.3fs" % (time.time() - t0))
  830| red = [n for n, ok in rows if not ok]
  831| if red:
  832|     print("M88K_BUSERR_RED=%s" % ",".join(red))
  833| shutil.rmtree(_TMPDIR, ignore_errors=True)
  834| print("M88K_BUSERR_PROBE_DONE")
  835| sys.stdout.flush()
  836| sys.exit(0 if control_ok and npass == len(rows) else 1)
~~~~

---

## 3. THE MEASUREMENTS -- each against its instrument revision and denominator

### 3.1 Order of events (file mtimes, 2026-10-23/24, `ls --time-style` at drafting time)
| time | artifact | what it proves |
|---|---|---|
| 21:53:06 | `pass1_20261023/PASS1_RULINGS.md` (with section E) | the adjudication predates the build |
| 22:02:35 | `table1_20261023/BASELINE.out` | baseline before any edit; work binary == witness base binary `2efeec55` |
| 22:28:08 | `table1_20261023/PRETABLE.out` (body + AMENDMENT 1) | the pre-table check predates every table run |
| 22:29:30 | `table1_20261023/BUILDER_QUESTIONS.md` | the 22 questions (L22's prediction is Q18 here) |
| 22:31:49 | `pass1_20261023/BUILD_SPEC.md` (section 11 rulings) | the rulings predate the freeze |
| 22:42:48 | `table1_20261023/m88k_buserr_probe.rev2.frozen.py.txt` | the instrument frozen before any table run |
| 22:42:52 | `table1_20261023/prefix_HEAD.out` | clause (a) pre-fix, before the product edits |
| 22:47:20 | the four product files (working tree) | the fix lands after the pre-fix run |
| 22:48:45 | `fixed.out`, `fixed_witness24.out` | post-fix, both instruments |
| 22:49-22:53 | `boot_base.out`, `boot_work.out` (written into the artifacts dir at 23:10:39) | the boot A/B BEFORE the variant table (section 10's order) |
| 22:58:22-23:09:12 | `L3...L22`, `L5`, `L5b` | the variant table |
| 23:10:15 | `SCORES.txt` | generated from the leg outputs |
| 23:14:51 | `CLEARANCE.out`, `prop_*.out` | propagation and the two-part clearance |
| 23:16:40 | working-tree `regress/gate_arm.sh` and `check_probe_wiring.py` | the harness insertions -- AFTER propagation (departure 3) |
| 23:17:54-01:30:48 | `gates/gate14_run.out` | gate 14, once, alone |
| 01:31:37-01:35:44 | `gates/gate11_run.out` | gate 11, once |
| 01:36:26 | `CLEARANCE_final.out` | clearance re-run after both gates: identical |

### 3.2 The baseline (`table1_20261023/BASELINE.out`, VERBATIM excerpts: the header and part D)
~~~~
# T36 / round #570 (m88kbuserrregs) -- BASELINE.out, the builder's baseline receipts, BEFORE any edit
# Assembled 2026-10-23 22:02:34 -0500 from the four helper outputs below, each VERBATIM (scripts preserved beside this
# file as *.sh.txt).  NAMED BASELINE: HEAD 7fca71876a996868fa47034fa8727375ce59653d plus the peer's five dirty files
# replaced by their HEAD blobs (the witness's procedure).  The WORK tree /tmp/gxt36/work is that baseline, built
# unmodified; its binary is BYTE-IDENTICAL to the witness's /tmp/gxt36/base/gxemul (md5 2efeec559ec5b3d16b200cccf4203631).
# No tree was mutated: no .MUTANT sentinel was owed or dropped.  Nothing under GXEMUL-SEC was edited except this
# artifacts directory (new files only).
   ...
############## PART D -- baseline control: the FROZEN witness probe on the WORK binary (run_base_witness.sh.txt) ##############
RUN_BASE_WITNESS_START 2026-10-23 22:02:00 -0500
== the witness directory's own MANIFEST.md5 (the frozen probe must still verify) ==
  verified OK: 32 of 32
probe:  d59798b0383f433b191e214e7848fe49  /mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/m88kbuserrregs/witness_20261023/m88k_buserr_probe.py   (witness: d59798b0383f433b191e214e7848fe49)
binary: 2efeec559ec5b3d16b200cccf4203631  /tmp/gxt36/work/gxemul   (witness base: 2efeec559ec5b3d16b200cccf4203631)
freshness: [ gxemul -nt src/cpus/memory_rw.c ] -> FRESH
freshness: [ gxemul -nt src/cpus/cpu_m88k.c ] -> FRESH
freshness: [ gxemul -nt src/devices/dev_luna88k.c ] -> FRESH
freshness: [ gxemul -nt src/devices/dev_m8820x.c ] -> FRESH
PROBE_RC=1  last line: M88K_BUSERR_PROBE_DONE
copied base_witness24.out (cmp clean, 4911 bytes)
copied transcripts_base_witness24 (8 transcripts, diff -r clean)
== row lines and summary lines vs the witness's WITNESS_headbin.out (label, binary path, elapsed excluded) ==
  IDENTICAL: every row line, INFO line and summary line matches the witness (35 lines compared)
== the summary lines ==
  M88K_BUSERR_RESULT=16/24
  M88K_BUSERR_CONTROL=OK
  M88K_BUSERR_SYMPTOM=PRESENT 8/8
  M88K_BUSERR_RED=uld pfsr,uld pfar,ust pfsr,ust pfar,vme pfsr,vme pfar,luna route,luna pfar
  M88K_BUSERR_PROBE_DONE
~~~~

### 3.3 Clause (a): the pre-fix run, whole, and the two post-fix receipts
`table1_20261023/prefix_HEAD.out` -- the frozen detector on the HEAD binary `2efeec55`, VERBATIM:
~~~~
m88kbuserrregs RUNG-3 DETECTOR (revision 2) -- binary=/tmp/gxt36/base/gxemul label=PREFIX-HEAD-7fca7187
machines: -E mvme88k -e mvme187 -M 64 [-n 2] and -E luna88k -e luna-88k (UNMODIFIED); luna shape: dummy raw image at 0x10000
seeds: dPFSR=0x5a5a5a5a dPFAR=0x13572468 iPFSR=0x2468ace0 iPFAR=0xbadf00d; want BERROR<<16=0x30000
row              got                                want                               note                                                           
neg apparatus    exit1/absent                       exit1/absent                       bogus subtype `187' -> no machine -> no register dump          ok
mv devsig        0xa90000/0xa90000                  0xa90000/0xa90000                  DEVICE SIGNATURE: mvme187 data/instr CMMU IDR (RAM reads 0)    ok
mv cmmu rt       0x5a5a5a5a/0x13572468/0x2468ace0/0xbadf00d 0x5a5a5a5a/0x13572468/0x2468ace0/0xbadf00d LIVENESS: four seeds stored and read back via the CMMU decode  ok
ok route         fall/r4=0x67000000                 fall/r4=0x67000000                 ld VME VBR 0xfff40088 (cased): served 0x67000000, no exception ok
ok regs          0x5a5a5a5a/0x13572468/0x2468ace0/0xbadf00d 0x5a5a5a5a/0x13572468/0x2468ace0/0xbadf00d an ACCEPTED device access writes no fault metadata             ok
uld route        v3/0x1002a/0xfff46010              v3/0x1002a/0xfff46010              ld 0xfff46010 (unreadable): vector 3, SXIP, DMA0 -- the exception is THIS access ok
uld pfsr         0x5a5a5a5a                         0x30000                            data CMMU PFSR after the fault (seeded 0x5a5a5a5a)             FAIL
uld pfar         0x13572468                         0xfff46010                         data CMMU PFAR after the fault (seeded 0x13572468)             FAIL
uld icmmu        kept                               kept                               instruction CMMU PFSR/PFAR keep their seeds                    ok
ust route        v3/0x1002a/0xfff46010              v3/0x1002a/0xfff46010              st 0xfff46010 (unreadable): vector 3, SXIP, DMA0 -- the exception is THIS access ok
ust pfsr         0x5a5a5a5a                         0x30000                            data CMMU PFSR after the fault (seeded 0x5a5a5a5a)             FAIL
ust pfar         0x13572468                         0xfff46010                         data CMMU PFAR after the fault (seeded 0x13572468)             FAIL
ust icmmu        kept                               kept                               instruction CMMU PFSR/PFAR keep their seeds                    ok
vme route        v3/0x1002a/0xfff40090              v3/0x1002a/0xfff40090              ld 0xfff40090 (VME pop. 1): vector 3, SXIP, DMA0 -- the exception is THIS access ok
vme pfsr         0x5a5a5a5a                         0x30000                            data CMMU PFSR after the fault (seeded 0x5a5a5a5a)             FAIL
vme pfar         0x13572468                         0xfff40090                         data CMMU PFAR after the fault (seeded 0x13572468)             FAIL
vme icmmu        kept                               kept                               instruction CMMU PFSR/PFAR keep their seeds                    ok
luna devsig      0xa90000/0xa90000                  0xa90000/0xa90000                  DEVICE SIGNATURE: luna-88k data/instr CMMU IDR                 ok
luna cmmu rt     0x5a5a5a5a/0x13572468/0x2468ace0/0xbadf00d 0x5a5a5a5a/0x13572468/0x2468ace0/0xbadf00d LIVENESS: the four seeds read back                             ok
luna route       fall/0x0/0x0/r4=0x0                v3/0x1002a/0x3ffffff0/r4=0xdeadbeef ld 0x3ffffff0: a refused access raises vector 3, serves nothing FAIL
luna pfsr        0x30000                            0x30000                            data CMMU PFSR (seeded 0x5a5a5a5a)                             ok
luna pfar        0x13572468                         0x3ffffff0                         data CMMU PFAR (seeded 0x13572468)                             FAIL
luna icmmu       kept                               kept                               instruction CMMU PFSR/PFAR keep their seeds                    ok
ifetch route     v2/0xfff46013/0x0                  v2/0xfff46013/0x0                  jmp (r5) to 0xfff46010: vector 2, SXIP|V|E, no data unit (attribution row) ok
ifetch pfsr      0x2468ace0                         0x30000                            INSTRUCTION CMMU PFSR after the refused fetch (seeded 0x2468ace0) FAIL
ifetch pfar      0xbadf00d                          0xfff46010                         INSTRUCTION CMMU PFAR after the refused fetch (seeded 0xbadf00d) FAIL
ifetch dcmmu     kept                               kept                               the DATA CMMU keeps its seeds after an instruction refusal     ok
dbg noexc        zeros/0x10028/fall/kept            zeros/0x10028/fall/kept            debugger dump of 0xfff46010: zeros, no vector, seeds survive   ok
null surv        exit0/readable                     exit0/readable                     -n 2 cpu 1 (no CMMU): alive after the data AND instruction refusals ok
null route       handled/0x10202/0xfff46010         handled/0x10202/0xfff46010         cpu 1's refused load: HANDLED set, FELL clear, SXIP, DMA0      ok
INFO null cpu0   (unscored) pc=0x10114 path=v3 dPFSR=0x5a5a5a5a dPFAR=0x13572468 r31=0x5678; cpu1 end pc=0x30050 markers-after-part2=handled
INFO unclaimed   ld 0x10000000 (no device, past RAM): how=exit0 path=fall r4=0x0 SXIP=0x0 dPFSR=0x5a5a5a5a dPFAR=0x13572468 iPFSR=0x2468ace0 iPFAR=0xbadf00d non-existant-msg=1 unasm=23/23
unasm            192/192                            192/192                            every placed word re-read by the disassembler                  ok
SCORE 21/31
M88K_BUSERR_RESULT=21/31
M88K_BUSERR_CONTROL=OK
M88K_BUSERR_SYMPTOM=PRESENT 10/10
M88K_BUSERR_REVISION=2
M88K_BUSERR_LABEL=PREFIX-HEAD-7fca7187
M88K_BUSERR_ELAPSED=0.055s
M88K_BUSERR_RED=uld pfsr,uld pfar,ust pfsr,ust pfar,vme pfsr,vme pfar,luna route,luna pfar,ifetch pfsr,ifetch pfar
M88K_BUSERR_PROBE_DONE
~~~~
`table1_20261023/fixed.out` -- the same frozen detector on the fixed work binary `3cd0501c`, VERBATIM:
~~~~
m88kbuserrregs RUNG-3 DETECTOR (revision 2) -- binary=/tmp/gxt36/work/gxemul label=FIXED-570
machines: -E mvme88k -e mvme187 -M 64 [-n 2] and -E luna88k -e luna-88k (UNMODIFIED); luna shape: dummy raw image at 0x10000
seeds: dPFSR=0x5a5a5a5a dPFAR=0x13572468 iPFSR=0x2468ace0 iPFAR=0xbadf00d; want BERROR<<16=0x30000
row              got                                want                               note                                                           
neg apparatus    exit1/absent                       exit1/absent                       bogus subtype `187' -> no machine -> no register dump          ok
mv devsig        0xa90000/0xa90000                  0xa90000/0xa90000                  DEVICE SIGNATURE: mvme187 data/instr CMMU IDR (RAM reads 0)    ok
mv cmmu rt       0x5a5a5a5a/0x13572468/0x2468ace0/0xbadf00d 0x5a5a5a5a/0x13572468/0x2468ace0/0xbadf00d LIVENESS: four seeds stored and read back via the CMMU decode  ok
ok route         fall/r4=0x67000000                 fall/r4=0x67000000                 ld VME VBR 0xfff40088 (cased): served 0x67000000, no exception ok
ok regs          0x5a5a5a5a/0x13572468/0x2468ace0/0xbadf00d 0x5a5a5a5a/0x13572468/0x2468ace0/0xbadf00d an ACCEPTED device access writes no fault metadata             ok
uld route        v3/0x1002a/0xfff46010              v3/0x1002a/0xfff46010              ld 0xfff46010 (unreadable): vector 3, SXIP, DMA0 -- the exception is THIS access ok
uld pfsr         0x30000                            0x30000                            data CMMU PFSR after the fault (seeded 0x5a5a5a5a)             ok
uld pfar         0xfff46010                         0xfff46010                         data CMMU PFAR after the fault (seeded 0x13572468)             ok
uld icmmu        kept                               kept                               instruction CMMU PFSR/PFAR keep their seeds                    ok
ust route        v3/0x1002a/0xfff46010              v3/0x1002a/0xfff46010              st 0xfff46010 (unreadable): vector 3, SXIP, DMA0 -- the exception is THIS access ok
ust pfsr         0x30000                            0x30000                            data CMMU PFSR after the fault (seeded 0x5a5a5a5a)             ok
ust pfar         0xfff46010                         0xfff46010                         data CMMU PFAR after the fault (seeded 0x13572468)             ok
ust icmmu        kept                               kept                               instruction CMMU PFSR/PFAR keep their seeds                    ok
vme route        v3/0x1002a/0xfff40090              v3/0x1002a/0xfff40090              ld 0xfff40090 (VME pop. 1): vector 3, SXIP, DMA0 -- the exception is THIS access ok
vme pfsr         0x30000                            0x30000                            data CMMU PFSR after the fault (seeded 0x5a5a5a5a)             ok
vme pfar         0xfff40090                         0xfff40090                         data CMMU PFAR after the fault (seeded 0x13572468)             ok
vme icmmu        kept                               kept                               instruction CMMU PFSR/PFAR keep their seeds                    ok
luna devsig      0xa90000/0xa90000                  0xa90000/0xa90000                  DEVICE SIGNATURE: luna-88k data/instr CMMU IDR                 ok
luna cmmu rt     0x5a5a5a5a/0x13572468/0x2468ace0/0xbadf00d 0x5a5a5a5a/0x13572468/0x2468ace0/0xbadf00d LIVENESS: the four seeds read back                             ok
luna route       v3/0x1002a/0x3ffffff0/r4=0xdeadbeef v3/0x1002a/0x3ffffff0/r4=0xdeadbeef ld 0x3ffffff0: a refused access raises vector 3, serves nothing ok
luna pfsr        0x30000                            0x30000                            data CMMU PFSR (seeded 0x5a5a5a5a)                             ok
luna pfar        0x3ffffff0                         0x3ffffff0                         data CMMU PFAR (seeded 0x13572468)                             ok
luna icmmu       kept                               kept                               instruction CMMU PFSR/PFAR keep their seeds                    ok
ifetch route     v2/0xfff46013/0x0                  v2/0xfff46013/0x0                  jmp (r5) to 0xfff46010: vector 2, SXIP|V|E, no data unit (attribution row) ok
ifetch pfsr      0x30000                            0x30000                            INSTRUCTION CMMU PFSR after the refused fetch (seeded 0x2468ace0) ok
ifetch pfar      0xfff46010                         0xfff46010                         INSTRUCTION CMMU PFAR after the refused fetch (seeded 0xbadf00d) ok
ifetch dcmmu     kept                               kept                               the DATA CMMU keeps its seeds after an instruction refusal     ok
dbg noexc        zeros/0x10028/fall/kept            zeros/0x10028/fall/kept            debugger dump of 0xfff46010: zeros, no vector, seeds survive   ok
null surv        exit0/readable                     exit0/readable                     -n 2 cpu 1 (no CMMU): alive after the data AND instruction refusals ok
null route       handled/0x10202/0xfff46010         handled/0x10202/0xfff46010         cpu 1's refused load: HANDLED set, FELL clear, SXIP, DMA0      ok
INFO null cpu0   (unscored) pc=0x10114 path=v3 dPFSR=0x30000 dPFAR=0xfff46010 r31=0x5678; cpu1 end pc=0x30050 markers-after-part2=handled
INFO unclaimed   ld 0x10000000 (no device, past RAM): how=exit0 path=fall r4=0x0 SXIP=0x0 dPFSR=0x5a5a5a5a dPFAR=0x13572468 iPFSR=0x2468ace0 iPFAR=0xbadf00d non-existant-msg=1 unasm=23/23
unasm            192/192                            192/192                            every placed word re-read by the disassembler                  ok
SCORE 31/31
M88K_BUSERR_RESULT=31/31
M88K_BUSERR_CONTROL=OK
M88K_BUSERR_SYMPTOM=ABSENT
M88K_BUSERR_REVISION=2
M88K_BUSERR_LABEL=FIXED-570
M88K_BUSERR_ELAPSED=0.055s
M88K_BUSERR_PROBE_DONE
~~~~
`table1_20261023/fixed_witness24.out` -- the FROZEN 24-row witness on the same fixed binary (witness clause (i); leg L1), VERBATIM:
~~~~
m88kbuserrregs RUNG-3 WITNESS (revision 1) -- binary=/tmp/gxt36/work/gxemul label=FIXED-570-witness24
machines: -E mvme88k -e mvme187 -M 64 and -E luna88k -e luna-88k (UNMODIFIED); luna shape: dummy raw image at 0x10000
seeds: dPFSR=0x5a5a5a5a dPFAR=0x13572468 iPFSR=0x2468ace0 iPFAR=0xbadf00d; want BERROR<<16=0x30000
row              got                                want                               note                                                           
neg apparatus    exit1/absent                       exit1/absent                       bogus subtype `187' -> no machine -> no register dump          ok
mv devsig        0xa90000/0xa90000                  0xa90000/0xa90000                  DEVICE SIGNATURE: mvme187 data/instr CMMU IDR (RAM reads 0)    ok
mv cmmu rt       0x5a5a5a5a/0x13572468/0x2468ace0/0xbadf00d 0x5a5a5a5a/0x13572468/0x2468ace0/0xbadf00d LIVENESS: four seeds stored and read back via the CMMU decode  ok
ok route         fall/r4=0x67000000                 fall/r4=0x67000000                 ld VME VBR 0xfff40088 (cased): served 0x67000000, no exception ok
ok regs          0x5a5a5a5a/0x13572468/0x2468ace0/0xbadf00d 0x5a5a5a5a/0x13572468/0x2468ace0/0xbadf00d an ACCEPTED device access writes no fault metadata             ok
uld route        v3/0x1002a/0xfff46010              v3/0x1002a/0xfff46010              ld 0xfff46010 (unreadable): vector 3, SXIP, DMA0 -- the exception is THIS access ok
uld pfsr         0x30000                            0x30000                            data CMMU PFSR after the fault (seeded 0x5a5a5a5a)             ok
uld pfar         0xfff46010                         0xfff46010                         data CMMU PFAR after the fault (seeded 0x13572468)             ok
uld icmmu        kept                               kept                               instruction CMMU PFSR/PFAR keep their seeds                    ok
ust route        v3/0x1002a/0xfff46010              v3/0x1002a/0xfff46010              st 0xfff46010 (unreadable): vector 3, SXIP, DMA0 -- the exception is THIS access ok
ust pfsr         0x30000                            0x30000                            data CMMU PFSR after the fault (seeded 0x5a5a5a5a)             ok
ust pfar         0xfff46010                         0xfff46010                         data CMMU PFAR after the fault (seeded 0x13572468)             ok
ust icmmu        kept                               kept                               instruction CMMU PFSR/PFAR keep their seeds                    ok
vme route        v3/0x1002a/0xfff40090              v3/0x1002a/0xfff40090              ld 0xfff40090 (VME pop. 1): vector 3, SXIP, DMA0 -- the exception is THIS access ok
vme pfsr         0x30000                            0x30000                            data CMMU PFSR after the fault (seeded 0x5a5a5a5a)             ok
vme pfar         0xfff40090                         0xfff40090                         data CMMU PFAR after the fault (seeded 0x13572468)             ok
vme icmmu        kept                               kept                               instruction CMMU PFSR/PFAR keep their seeds                    ok
luna devsig      0xa90000/0xa90000                  0xa90000/0xa90000                  DEVICE SIGNATURE: luna-88k data/instr CMMU IDR                 ok
luna cmmu rt     0x5a5a5a5a/0x13572468/0x2468ace0/0xbadf00d 0x5a5a5a5a/0x13572468/0x2468ace0/0xbadf00d LIVENESS: the four seeds read back                             ok
luna route       v3/0x1002a/0x3ffffff0/r4=0xdeadbeef v3/0x1002a/0x3ffffff0/r4=0xdeadbeef ld 0x3ffffff0: a refused access raises vector 3, serves nothing ok
luna pfsr        0x30000                            0x30000                            data CMMU PFSR (seeded 0x5a5a5a5a)                             ok
luna pfar        0x3ffffff0                         0x3ffffff0                         data CMMU PFAR (seeded 0x13572468)                             ok
luna icmmu       kept                               kept                               instruction CMMU PFSR/PFAR keep their seeds                    ok
INFO ifetch      jmp (r5) to 0xfff46010: how=exit0 path=v2 SXIP=0xfff46013 iPFSR=0x30000 iPFAR=0xfff46010 dPFSR=0x5a5a5a5a dPFAR=0x13572468 pre-read-msg=1 halt-msg=0 unasm=23/23
INFO unclaimed   ld 0x10000000 (no device, past RAM): how=exit0 path=fall r4=0x0 SXIP=0x0 dPFSR=0x5a5a5a5a dPFAR=0x13572468 iPFSR=0x2468ace0 iPFAR=0xbadf00d non-existant-msg=1 unasm=23/23
unasm            115/115                            115/115                            every placed word re-read by the disassembler                  ok
SCORE 24/24
M88K_BUSERR_RESULT=24/24
M88K_BUSERR_CONTROL=OK
M88K_BUSERR_SYMPTOM=ABSENT
M88K_BUSERR_LABEL=FIXED-570-witness24
M88K_BUSERR_ELAPSED=0.044s
M88K_BUSERR_PROBE_DONE
~~~~
The unscored `INFO null cpu0` line under two variant legs, for P15 (line 35 of `L9_excinnull.out` and of
`L17_excdrop.out`, VERBATIM; compare line 35 of `fixed.out` and `prefix_HEAD.out` above, `cpu1 end pc=0x30050`):
~~~~
INFO null cpu0   (unscored) pc=0x10114 path=v3 dPFSR=0x30000 dPFAR=0xfff46010 r31=0x5678; cpu1 end pc=0xfff46010 markers-after-part2=fell
INFO null cpu0   (unscored) pc=0x10114 path=fall dPFSR=0x30000 dPFAR=0xfff46010 r31=0x5678; cpu1 end pc=0xfff46010 markers-after-part2=fell
~~~~

### 3.4 The variant table -- `table1_20261023/SCORES.txt`, VERBATIM (whole)
*Two notes, both the drafter's: (1) each `measured:` line truncates the SYMPTOM value at 60 characters (the
generator's `[:60]`), so `ust pfar=;` is a cut, not an empty class -- the leg outputs carry the full line, e.g.
`L3_armHEAD.out`: `M88K_BUSERR_SYMPTOM=MIXED uld pfsr=STALE,uld pfar=STALE,ust pfsr=STALE,ust pfar=STALE,vme
pfsr=STALE,vme pfar=STALE,luna route=FIXED,luna pfar=STALE,ifetch pfsr=STALE,ifetch pfar=STALE` (P11).  (2) The header
line names PRETABLE section 5 as the criterion; L22's predicted set is NOT in PRETABLE -- it is BUILDER_QUESTIONS Q18 and
BUILD_SPEC section 11 Q18, both of which predate the leg (3.1; P5).*
~~~~
T36 / #570 (m88kbuserrregs) -- SCORES.txt, the kill table (BUILD_SPEC sections 4-6, 10, 11).  Generated by mk_scores570.py.txt from the outputs in this directory.
Named baseline for every variant: HEAD 7fca7187 + the four #570 files (GXEMUL-SEC working set; work binary 3cd0501c).  Each leg: a cp -a of the work tree in /tmp/gxt36/legs/<leg>, one file replaced, rm src/cpus/*.o,
make, `[ gxemul -nt <file> ]' FRESH, 0 warnings (legs_batch*.out), restored by cp from SEC + cmp, sentinel removed, tree discarded.  The variant vs the fixed file is <leg>.diff (a file only; L3/L4 are HEAD blobs verbatim).
Criterion (section 11, Q14): the MEASURED red set equals PRETABLE section 5's predicted set as amended (AMENDMENT 1); a mismatch is a RESULT.

pre     21/31  MATCH   [rev2 frozen, N=31]  prefix_HEAD.out
        variant : HEAD binary 2efeec55 (clause (a), pre-fix)
        measured: 10 red / 31 rows emitted; CONTROL=OK; SYMPTOM=PRESENT 10/10; sentinel present
        red     : ifetch pfar, ifetch pfsr, luna pfar, luna route, uld pfar, uld pfsr, ust pfar, ust pfsr, vme pfar, vme pfsr
        why     : all ten reds are STALE (SYMPTOM=PRESENT 10/10): the seeds survive every refused access, LUNA serves 0
fix     31/31  MATCH   [rev2 frozen, N=31]  fixed.out
        variant : the #570 fix, work binary 3cd0501c (clause (a), post-fix)
        measured: 0 red / 31 rows emitted; CONTROL=OK; SYMPTOM=ABSENT; sentinel present
        red     : (none)
        why     : --
L1      24/24  MATCH   [rev1 frozen witness, N=24]  fixed_witness24.out
        variant : the FROZEN 24-row witness on the fixed binary (witness clause (i))
        measured: 0 red / 24 rows emitted; CONTROL=OK; SYMPTOM=ABSENT; sentinel present
        red     : (none)
        why     : --
L3      21/31  MATCH   [rev2 frozen, N=31]  L3_armHEAD.out
        variant : clause (b): memory_rw.c's arm reinstated verbatim from HEAD (blob 3d47dd66), the LUNA case fixed
        measured: 10 red / 31 rows emitted; CONTROL=OK; SYMPTOM=MIXED uld pfsr=STALE,uld pfar=STALE,ust pfsr=STALE,ust pfar=; sentinel present
        red     : ifetch pfar, ifetch pfsr, luna pfar, luna pfsr, uld pfar, uld pfsr, ust pfar, ust pfsr, vme pfar, vme pfsr
        why     : no metadata write anywhere: every pfsr/pfar row reads its seed; luna route stays green (the arm still faults)
L3/w24  16/24  MATCH   [rev1 frozen witness, N=24]  L3_armHEAD_witness24.out
        variant : the same L3 binary on the frozen witness
        measured: 8 red / 24 rows emitted; CONTROL=OK; SYMPTOM=MIXED uld pfsr=STALE,uld pfar=STALE,ust pfsr=STALE,ust pfar=; sentinel present
        red     : luna pfar, luna pfsr, uld pfar, uld pfsr, ust pfar, ust pfsr, vme pfar, vme pfsr
        why     : as L3 on the 24-row instrument (B3's 16/24 prediction)
L4      29/31  MATCH   [rev2 frozen, N=31]  L4_caseHEAD.out
        variant : clause (b): dev_luna88k.c's case reinstated verbatim from HEAD (blob 6ecc6908), the arm fixed
        measured: 2 red / 31 rows emitted; CONTROL=OK; SYMPTOM=MIXED uld pfsr=FIXED,uld pfar=FIXED,ust pfsr=FIXED,ust pfar=; sentinel present
        red     : luna pfar, luna route
        why     : the case serves 0 again (fall, r4=0) and writes PFSR but no PFAR; luna pfsr stays green
L4/w24  22/24  MATCH   [rev1 frozen witness, N=24]  L4_caseHEAD_witness24.out
        variant : the same L4 binary on the frozen witness
        measured: 2 red / 24 rows emitted; CONTROL=OK; SYMPTOM=MIXED uld pfsr=FIXED,uld pfar=FIXED,ust pfsr=FIXED,ust pfar=; sentinel present
        red     : luna pfar, luna route
        why     : as L4 on the 24-row instrument (B3's 22/24 prediction)
L5      1/31   MATCH   [rev2 frozen, N=31]  L5_stub.out
        variant : clause (c): an exit-1 non-emulator in the binary's place
        measured: 30 red / 31 rows emitted; CONTROL=FAIL; SYMPTOM=MIXED uld pfsr=OTHER,uld pfar=OTHER,ust pfsr=OTHER,ust pfar=; sentinel present
        red     : dbg noexc, ifetch dcmmu, ifetch pfar, ifetch pfsr, ifetch route, luna cmmu rt, luna devsig, luna icmmu, luna pfar, luna pfsr, luna route, mv cmmu rt, mv devsig, null route, null surv, ok regs, ok route, uld icmmu, uld pfar, uld pfsr, uld route, unasm, ust icmmu, ust pfar, ust pfsr, ust route, vme icmmu, vme pfar, vme pfsr, vme route
        why     : every session is 'died:exit1'; neg apparatus passes by design; CONTROL=FAIL, sentinel printed, exit 1
L6      28/31  MATCH   [rev2 frozen, N=31]  L6_seldata.out
        variant : (d) the added selector weakened to always-data
        measured: 3 red / 31 rows emitted; CONTROL=OK; SYMPTOM=MIXED uld pfsr=FIXED,uld pfar=FIXED,ust pfsr=FIXED,ust pfar=; sentinel present
        red     : ifetch dcmmu, ifetch pfar, ifetch pfsr
        why     : the instruction refusal writes cmmu[1]: the instruction seeds survive, the data CMMU is written
L6b     19/31  MATCH   [rev2 frozen, N=31]  L6b_selinstr.out
        variant : (d) the added selector weakened to always-instruction (Q16)
        measured: 12 red / 31 rows emitted; CONTROL=OK; SYMPTOM=MIXED uld pfsr=STALE,uld pfar=STALE,ust pfsr=STALE,ust pfar=; sentinel present
        red     : luna icmmu, luna pfar, luna pfsr, uld icmmu, uld pfar, uld pfsr, ust icmmu, ust pfar, ust pfsr, vme icmmu, vme pfar, vme pfsr
        why     : every data refusal writes cmmu[0]: the data seeds survive, the instruction CMMU is written
L7      30/31  MATCH   [rev2 frozen, N=31]  L7_noexcdrop.out
        variant : (d) the `!no_exceptions' conjunct dropped from the outer guard
        measured: 1 red / 31 rows emitted; CONTROL=OK; SYMPTOM=ABSENT; sentinel present
        red     : dbg noexc
        why     : the debugger dump enters the body: (memory access failed), cpu 0 vectors, the data CMMU is written
L8      29/31  MATCH   [rev2 frozen, N=31]  L8_nullrm.out
        variant : (d) the added NULL check removed
        measured: 2 red / 31 rows emitted; CONTROL=OK; SYMPTOM=ABSENT; sentinel present
        red     : null route, null surv
        why     : cpu 1's refused data load dereferences its NULL cmmu[1]: the session dies, sig11
L8b     30/31  MATCH   [rev2 frozen, N=31]  L8b_nulldata.out
        variant : (d) the NULL check conditioned on the data label (Q15)
        measured: 1 red / 31 rows emitted; CONTROL=OK; SYMPTOM=ABSENT; sentinel present
        red     : null surv
        why     : part 1 survives (route green, its dump flushed); cpu 1's instruction fetch dereferences NULL in part 2: sig11
L9      30/31  MATCH   [rev2 frozen, N=31]  L9_excinnull.out
        variant : (d) the exception moved inside the NULL check
        measured: 1 red / 31 rows emitted; CONTROL=OK; SYMPTOM=ABSENT; sentinel present
        red     : null route
        why     : cpu 1 takes no exception: FELL set, HANDLED clear, SXIP/DMA0 0
L10     26/31  MATCH   [rev2 frozen, N=31]  L10_raw3.out
        variant : PFSR value: raw 3 instead of 3 << 16
        measured: 5 red / 31 rows emitted; CONTROL=OK; SYMPTOM=MIXED uld pfsr=OTHER,uld pfar=FIXED,ust pfsr=OTHER,ust pfar=; sentinel present
        red     : ifetch pfsr, luna pfsr, uld pfsr, ust pfsr, vme pfsr
        why     : every PFSR row reads 0x3
L11     26/31  MATCH   [rev2 frozen, N=31]  L11_pfarrel.out
        variant : PFAR value: the device-relative paddr
        measured: 5 red / 31 rows emitted; CONTROL=OK; SYMPTOM=MIXED uld pfsr=FIXED,uld pfar=OTHER,ust pfsr=FIXED,ust pfar=; sentinel present
        red     : ifetch pfar, luna pfar, uld pfar, ust pfar, vme pfar
        why     : PFAR reads 0x10 / 0x10 / 0x90 / 0x0 / 0x10, not the physical address
L12     26/31  MATCH   [rev2 frozen, N=31]  L12_pfsronly.out
        variant : PFAR not written (PFSR only)
        measured: 5 red / 31 rows emitted; CONTROL=OK; SYMPTOM=MIXED uld pfsr=FIXED,uld pfar=STALE,ust pfsr=FIXED,ust pfar=; sentinel present
        red     : ifetch pfar, luna pfar, uld pfar, ust pfar, vme pfar
        why     : every PFAR row reads its seed
L13     26/31  MATCH   [rev2 frozen, N=31]  L13_bothcmmu.out
        variant : target: both CMMUs written
        measured: 5 red / 31 rows emitted; CONTROL=OK; SYMPTOM=ABSENT; sentinel present
        red     : ifetch dcmmu, luna icmmu, uld icmmu, ust icmmu, vme icmmu
        why     : the sibling CMMU is written: its seeds change
L14     26/31  MATCH   [rev2 frozen, N=31]  L14_sibclear.out
        variant : target: the sibling's PFSR cleared to SUCCESS (the translation-fault writer's shape)
        measured: 5 red / 31 rows emitted; CONTROL=OK; SYMPTOM=ABSENT; sentinel present
        red     : ifetch dcmmu, luna icmmu, uld icmmu, ust icmmu, vme icmmu
        why     : the sibling PFSR reads 0
L15     29/31  MATCH   [rev2 frozen, N=31]  L15_readonly.out
        variant : guard operand: writes only for MEM_READ
        measured: 2 red / 31 rows emitted; CONTROL=OK; SYMPTOM=MIXED uld pfsr=FIXED,uld pfar=FIXED,ust pfsr=STALE,ust pfar=; sentinel present
        red     : ust pfar, ust pfsr
        why     : the refused store writes nothing
L16     29/31  MATCH   [rev2 frozen, N=31]  L16_novme.out
        variant : guard operand: the VME device excluded (Q17)
        measured: 2 red / 31 rows emitted; CONTROL=OK; SYMPTOM=MIXED uld pfsr=FIXED,uld pfar=FIXED,ust pfsr=FIXED,ust pfar=; sentinel present
        red     : vme pfar, vme pfsr
        why     : the VME population-1 refusal writes nothing
L17     22/31  MATCH   [rev2 frozen, N=31]  L17_excdrop.out
        variant : placement: the exception dropped
        measured: 9 red / 31 rows emitted; CONTROL=OK; SYMPTOM=MIXED uld pfsr=FIXED,uld pfar=FIXED,ust pfsr=FIXED,ust pfar=; sentinel present
        red     : ifetch dcmmu, ifetch pfar, ifetch pfsr, ifetch route, luna route, null route, uld route, ust route, vme route
        why     : refused data accesses fall through; the stepped fetch reaches R1's `bad:' tail (handler never runs)
L18     6/31   MATCH   [rev2 frozen, N=31]  L18_preguard.out
        variant : placement: the NULL-checked writes moved to just before the outer guard (Q14)
        measured: 25 red / 31 rows emitted; CONTROL=FAIL; SYMPTOM=MIXED uld pfsr=OTHER,uld pfar=OTHER,ust pfsr=OTHER,ust pfar=; sentinel present
        red     : dbg noexc, ifetch dcmmu, ifetch pfar, ifetch pfsr, ifetch route, luna cmmu rt, luna icmmu, luna pfar, luna pfsr, luna route, mv cmmu rt, ok regs, ok route, uld icmmu, uld pfar, uld pfsr, uld route, ust icmmu, ust pfar, ust pfsr, ust route, vme icmmu, vme pfar, vme pfsr, vme route
        why     : every served CMMU access also writes PFSR/PFAR, so each CMMU session's readback prerequisite fails
L19     4/31   MATCH   [rev2 frozen, N=31]  L19_res1.out
        variant : outer guard widened to res <= 1
        measured: 27 red / 31 rows emitted; CONTROL=FAIL; SYMPTOM=MIXED uld pfsr=OTHER,uld pfar=OTHER,ust pfsr=OTHER,ust pfar=; sentinel present
        red     : dbg noexc, ifetch dcmmu, ifetch pfar, ifetch pfsr, ifetch route, luna cmmu rt, luna devsig, luna icmmu, luna pfar, luna pfsr, luna route, mv cmmu rt, mv devsig, ok regs, ok route, uld icmmu, uld pfar, uld pfsr, uld route, ust icmmu, ust pfar, ust pfsr, ust route, vme icmmu, vme pfar, vme pfsr, vme route
        why     : the first served IDR load faults, so every CMMU session's device-signature prerequisite fails
L21     28/31  MATCH   [rev2 frozen, N=31]  L21_casewrdel.out
        variant : the LUNA case's write deleted, the case still served (break)
        measured: 3 red / 31 rows emitted; CONTROL=OK; SYMPTOM=MIXED uld pfsr=FIXED,uld pfar=FIXED,ust pfsr=FIXED,ust pfar=; sentinel present
        red     : luna pfar, luna pfsr, luna route
        why     : served 0, no exception, no write: route, pfsr and pfar all read the pre-fix shape
L22     27/31  MATCH   [rev2 frozen, N=31]  L22_casedel.out
        variant : the LUNA case deleted (CL15's counterfactual, Q18)
        measured: 4 red / 31 rows emitted; CONTROL=OK; SYMPTOM=MIXED uld pfsr=FIXED,uld pfar=FIXED,ust pfsr=FIXED,ust pfar=; sentinel present
        red     : luna icmmu, luna pfar, luna pfsr, luna route
        why     : the access reaches default:, which stops the cpu: the handler never runs (prereq:handler)
L5b     --     MATCH   [rev2 frozen]  L5b_absent.out
        variant : clause (c): the binary ABSENT
        measured: FileNotFoundError before row 1, no row emitted, NO sentinel (the gate's sentinel pin reds)
L20     not run: L20 = L4 (HEAD's case verbatim IS 'left returning 1, write kept'; section 11, Q13)

SUMMARY: 27 measurements MATCH their prediction, 0 RESULT (mismatch).  Instrument revisions: the detector rev2 (31 rows) froze BEFORE any table run (md5 d57c12ab, identical to regress/m88k_buserr_probe.py at freeze time); the witness rev1 (24 rows, md5 d59798b0) is the untouched witness_20261023 file.
CLAUSE (c): measured at table1_20261023/L5_stub.out (1/31: only `neg apparatus' green, by design; CONTROL=FAIL; SYMPTOM=MIXED; sentinel printed; exit 1) and L5b_absent.out (no sentinel, no rows).
Every variant leg (L3, L4, L6, L6b, L7, L8, L8b, L9-L19, L21, L22: 20 builds) is red on the 31-row detector; no build failed, none warned.
SCORES_DONE
~~~~
Every one of the 20 variant builds (L3, L4, L6, L6b, L7, L8, L8b, L9, L10, L11, L12, L13, L14, L15, L16, L17, L18,
L19, L21, L22) logged `make rc=0, FRESH binary <md5>, warnings 0, errors 0` and `restored from SEC (cmp clean),
sentinel removed, leg tree discarded` (`legs_batch1.out`-`legs_batch4.out`; 20 distinct binary md5s).  The null-medium
legs (`legs_null_medium.out`, VERBATIM):
~~~~
LEGS_NULL_MEDIUM_START 2026-10-23 23:09:11 -0500
stub: #!/bin/sh;exit 1;  md5 0e982e12da25
L5  rc=1  M88K_BUSERR_RESULT=1/31 M88K_BUSERR_CONTROL=FAIL M88K_BUSERR_SYMPTOM=MIXED uld pfsr=OTHER,uld pfar=OTHER,ust   last: M88K_BUSERR_PROBE_DONE
L5  green rows: neg apparatus;
L5b rc=1  sentinel lines: 0  rows emitted: 0  last: FileNotFoundError: [Errno 2] No such file or directory: '/tmp/gxt36/stub/absent-gxemul'
LEGS_NULL_MEDIUM_DONE 2026-10-23 23:09:12 -0500
~~~~

### 3.5 The pre-table check -- `table1_20261023/PRETABLE.out`, VERBATIM (whole: body, then AMENDMENT 1, which rules where it differs)
*Read section 0's null-session design as SUPERSEDED by AM-1, and section 6's last sentence ("instruction x NULL is not
rowed") as SUPERSEDED by AM-2.  Section 2's CL15 line "No leg in the table builds 'case deleted'" was overtaken by the
Q18 ruling (L22) with no Amendment 2 appended (P5).  Its BUILDER_QUESTIONS ids follow a DRAFT numbering (this file's
mtime, 22:28:08, precedes BUILDER_QUESTIONS.md's, 22:29:30; AMENDMENT 1 self-dates "~22:3x"): in the final file L20 = L4
is Q13 (body: Q5), L6b Q16 (body Q6, AM-4 [Q12]), L16 Q17 (body Q7, AM-4 [Q13]), L18's form Q14 (body "Q8 form"),
`ifetch route` as CONTROL Q8 (AM-5 [Q7]), "case deleted" Q18 (body Q9).  AM-1's [Q1]-[Q4] and AM-4/AM-6's [Q9], [Q14],
[Q15] match the final ids.*
~~~~
# T36 / round #570 (m88kbuserrregs) -- PRETABLE.out, the pre-table check (CLAUDE.md "THE PRE-TABLE CHECK", MANDATORY
# for a round shipping a kill-table-backed detector).  Written by the builder (Opus 5.5) on 2026-10-23 BEFORE table 1:
# its mtime precedes every leg (L1-L21), prefix_HEAD.out and fixed.out.  The only probe runs that precede it are the
# baseline receipts in BASELINE.out (part D: the frozen witness on the unmodified work binary, 16/24 as the witness)
# -- a baseline control, not a table leg.
#
# Sources: read at HEAD 7fca7187.  The four product files are byte-identical to HEAD in the SEC working tree, est/,
# build/, build-asan/, /tmp/gxsec-build and /tmp/gxt36/work (BASELINE.out parts A and C), so the line numbers below
# are HEAD's.  Seat rows cited as <seat>:<line> are lines of pass1_20261023/<seat>_t36p1*.txt.
#
# Rows covered: 31 = the 24 witness rows + the 7 new rows of BUILD_SPEC.md section 3.  The 7 new rows' SESSIONS do
# not exist yet; section 0 states the design every prediction below assumes.  Where that design departs from the
# spec's wording, BUILDER_QUESTIONS.md asks the main loop to rule (ids Q1..Qn there); a ruling that changes a design
# owes an amendment to this file BEFORE table 1, appended below the PRETABLE_DONE line with its date, never an edit
# in place.
#
# Every prediction here is a PREDICTION, read off the source.  None has been measured.  The kill table's measured
# scores are what the record carries; a leg that disagrees with this file is a RESULT (mis-built / dead target /
# mis-cut row), never a silent re-aim.

====================================================================================================================
0. THE SEVEN NEW ROWS -- the cells and observables assumed here (design detail and alternatives: BUILDER_QUESTIONS)
====================================================================================================================
  ifetch route / ifetch pfsr / ifetch pfar / ifetch dcmmu  (B5a)
      The witness's INFO ifetch session, made SCORED: mvme187, the same seeded program with ACCESS = `jmp (r5)', r5 =
      0xfff46010 (the `unreadable' window).  prereq_bad() applies; its 23 placed words count toward `unasm'.
      Channel: the step loop's disassembly pre-read (cpu_dyntrans.c:287-290: CACHE_INSTRUCTION, no NO_EXCEPTIONS --
      R2) reaches memory_rw.c's arm with cache == CACHE_INSTRUCTION.  Wants: route = v2/0xfff46013/0x0 (path v2,
      SXIP = 0xfff46010|V|E, DMA0 0 because only DATA_ACCESS copies the data unit, cpu_m88k.c:912); pfsr = r15 =
      cmmu[0] PFSR = 0x30000 (HEAD: the seed 0x2468ace0); pfar = r16 = cmmu[0] PFAR = 0xfff46010 (HEAD: 0xbadf00d);
      dcmmu = r13/r14 (cmmu[1]) still the data seeds -> "kept".  R2 dependency and the re-root obligation (C1/C2) go
      in the row notes and the contract.
  dbg noexc  (B5b)
      A DEDICATED mvme187 session cloned from `ok' (ACCESS = `ld r4,r5,0' at VME VBR 0xfff40088, accepted): `step 10'
      (IDR loads, seeds, readbacks), then the debugger command `dump 0xfff46010 0xfff46020' (debugger_cmds.c:684,
      :716-717: cpus[bootstrap_cpu], CACHE_NONE | NO_EXCEPTIONS, one 16-byte memory_rw), then `reg' (pc after the
      dump), `step 9', `reg', `reg 0,0'.  got = "<dump>/<pc after dump>/<path at end>/<data+instr seeds at end>";
      want = "zeros/0x10028/fall/kept".  prereq_bad() applies (handler completed = "cpu running").
  null surv / null route  (B5c)
      A SEPARATE mvme187 session with `-n 2'.  cpu 0 is `pause'd before it executes anything; `focus 1' sets cpu 1's
      pc = CODE1 (0x10200), r2 = r3 = 0x20000 (RAM, so the shared handler H never addresses a CMMU window), r5 =
      0xfff46010, sentinels in r4/r6/r7/r13-r16/r31; `tlbdump 1' records the NULL premise (no "cpu1: CMMU" line --
      cpu_m88k.c:354-357 skips NULL slots); `pause 1'; `step 9'; `reg 1'; `reg 1,0'.  CODE1 = ld r4,r5,0 ; or
      r6,r0,0x1234 ; br H.  cpu 1's VBR is 0 (the cpu struct is zeroed_alloc'ed, cpu.c:71), so its vector 3 is the
      shared `or r7,r0,3 ; br H' at 0x18.  No RAM-flag dispatcher and no guest VBR write (BUILDER_QUESTIONS Q1).
      null surv: got = "<how>/<regs1 parsed?>", want "exit0/regs".  null route: got = cpu 1's path/SXIP/DMA0, want
      "v3/0x10202/0xfff46010"; cause-free prerequisite strings when the session died, when `tlbdump 1' shows a CMMU on
      cpu 1 (the cell is not the NULL cell), or when cpu 1 did not reach H_END with r31 = 0x5678.
  Bookkeeping these designs imply (Q-items): `unasm' literal 115 -> 174 (115 + ifetch 23 + dbg 23 + null 13: vectors
  4, H 6, CODE1 3); SYMPTOM list 8 -> 10 (the two ifetch symptom rows, STALE = their instruction seeds), printed
  PRESENT n/10 | ABSENT | MIXED.

====================================================================================================================
1. SIBLING PARITY
====================================================================================================================
  A. The neighbouring arch arms of the same device-failure block (memory_rw.c:603-625):
     | arm                 | exception                     | fault metadata written                                  |
     | MEM_MIPS :608-613   | IBE / DBE (by `cache')        | NONE: BadVAddr is written only for TLB, MOD..ADES and   |
     |                     |                               | VCE (cpu_mips.c:2053; IBE 6, DBE 7, cop0.h:189-190)     |
     | MEM_M88K :614-623   | vector 2 / 3 (by `cache')     | HEAD: NONE (the TODO :615-619).  FIXED: faulting-side   |
     |   (the edited arm)  |                               | CMMU PFSR + PFAR, sibling kept, NULL-checked            |
     | every other arch    | none in this block            | none (debug() + MEMORY_ACCESS_FAILED only; what their   |
     |   (no #ifdef block) |                               | callers do with FAILED was not read -- not this diff)   |
     Asymmetry -> owed: no row (no other arm records a fault address here); ONE SENTENCE owed in the records: the fix
     gives m88k fault metadata no sibling arch in this block has -- never "parity with MIPS".
  B. The other writers of the same two registers (census: grep 'CMMU_PFSR\]|CMMU_PFAR\]' src, 5 hits, + the guest
     store arm dev_m8820x.c:459-460):
     | writer                         | PFSR                       | PFAR             | sibling       | NULL test     |
     | memory_m88k.c:382-405          | status<<16, faulting side  | pfar, or 0 for a | PFSR :=       | faulting cmmu |
     |   (translation fault)          |                            | WRITE fault      | SUCCESS<<16   | NULL returns  |
     |                                |                            |                  | (:383-384)    | at :130-132;  |
     |                                |                            |                  |               | :383 none     |
     | dev_luna88k.c:626 (HEAD case)  | BERROR<<16 on cmmu[1] for  | none             | none          | none          |
     |                                | ANY cache class            |                  |               |               |
     | memory_rw.c arm (FIXED)        | BERROR<<16, faulting side  | orig_paddr       | KEPT          | yes, writes   |
     |                                | (cmmu[cache==INSTR?0:1])   |                  |               | only          |
     | dev_m8820x.c:459-460 (guest st)| the stored word            | the stored word  | --            | n/a (owner c) |
     Asymmetries -> owed: (1) the sibling clear exists in the translation path and NOT in the arm (A9, deliberate)
     -> rows: uld/ust/vme/luna icmmu + ifetch dcmmu pin `kept'; sentence: the contract's sibling note may not say "no
     guest can observe the sibling" (codex:29).  (2) the arm's NULL test -> rows null surv / null route.  (3) the HEAD
     case wrote cmmu[1] even for an instruction access (glm-Q12:14); the fix deletes that write -> no row (no LUNA
     instruction-fetch row; R1/R2) -> one CHANGELOG sentence.

====================================================================================================================
2. CLAIM -> ROW  (the sentences the #570 comments WILL assert -- drafted here; step 5 may not add a claim that is not
   in this list without an amendment below)
====================================================================================================================
  memory_rw.c, replacing the TODO :615-619:
   CL1  "the bus error is recorded in the faulting side's CMMU before the exception is raised"
          -> uld/ust/vme/luna/ifetch pfsr+pfar (written) and the five route rows (exception still raised)
   CL2  "PFSR = CMMU_PFSR_BERROR << 16 (0x00030000, the field OpenBSD/mvme88k's trap.c extracts)"
          -> uld/ust/vme/luna/ifetch pfsr, exact value
   CL3  "PFAR = orig_paddr, the PHYSICAL address saved before the device-relative subtraction (:437 vs :494)"
          -> uld/ust/vme/luna/ifetch pfar: absolute 0xfff46010 / 0xfff40090 / 0x3ffffff0 vs relative 0x10 / 0x90 / 0x0
   CL4  "cmmu[0] is the instruction CMMU, cmmu[1] the data CMMU (memory_m88k.c:112's index)"
          -> data rows (cmmu[1]) and ifetch pfsr/pfar (cmmu[0])
   CL5  "the other CMMU is not written"            -> uld/ust/vme/luna icmmu, ifetch dcmmu
   CL6  "a cpu with no CMMU gets no write"         -> null surv (no host fault on the NULL slot)
   CL7  "... and still takes the exception"        -> null route
   CL8  "the !no_exceptions test keeps debugger reads out: no write, no exception" -> dbg noexc
   CL9  "reached only by an access a device CLAIMS and REFUSES while the cpu keeps running"
          -> claims/refuses: ok route + ok regs (served: no write, no exception) vs the refused rows.
          "while the cpu keeps running": NO ROW -- a device that stops the cpu returns at :591-592 before the arm
          (outside the repair path, unrowed by design; luna-88k's other refusals all do this -- witness correction 2)
   CL10 "an unclaimed address takes the 'Outside of physical RAM?' path and is unchanged" -> NO ROW (INFO
          `unclaimed' stays unscored; R3, clause (e); the contract discloses it)
   CL11 (if written) "a sub-word access records the byte address" -> NO ROW: transferred warrant only (upstream; P2
          UNKNOWN for silicon), clause (e).  RECOMMENDATION: the comment should not assert it.
  cpu_m88k.c:
   CL12 "#570: memory_rw.c's m88k instantiation (tmp_m88k_tail.c:38-40) uses CMMU_PFSR / CMMU_PFAR /
          CMMU_PFSR_BERROR, which this header defines" -> NO ROW: the build is the check (the repair does not compile
          without it; gate 1 / every leg's build)
  dev_luna88k.c, the case at :624-627:
   CL13 "refused: memory_rw.c's arm raises the access exception and writes PFSR and PFAR"
          -> luna route, luna pfsr, luna pfar (a word LOAD).  A store (P10) and an instruction fetch at this address
          are NOT rowed -> the comment should say "for a load or store" at most, with the store disclosed (e)
   CL14 "(it used to write cmmu[1]'s PFSR only and serve 0)" -> the HEAD behaviour, measured by the witness
          (WITNESS_headbin.out: luna route fall/r4=0x0, luna pfsr 0x30000); no post-fix row owed
   CL15 "the case is kept: default: would stop the cpu" -- a COUNTERFACTUAL-consequence claim (semantic trigger) ->
          luna route's prerequisite channel (a deleted case reaches :909-924, `cpu->running = 0', :591-592 returns,
          the handler never runs, luna route reads "handler ...").  No leg in the table builds "case deleted"
          (BUILDER_QUESTIONS Q9 offers one)
  dev_m8820x.c (comment-only, A7):
   CL16 :293-294 "the model writes only PFSR and PFAR" gains its second writer (memory_rw.c's arm)
   CL17 :325-327 the stale "dev_luna88k.c:614" becomes memory_rw.c's arm (PFSR and PFAR)
   CL18 :453 "never through this handler ... at memory_m88k.c:382-384" gains memory_rw.c's arm
   CL19 :500-501 "PFSR and PFAR written at :382-405" gains memory_rw.c's arm
          -> all four: no new observable beyond CL2/CL3 (the pfsr/pfar rows).  NO-ROW sentence: comment-only, no
          behaviour change -- to be MEASURED in step 5 by an object compare (dev_m8820x.o md5 before == after)
  The probe header (B1) is the detector's own text; its rows are its claims, and its NOT CLAIMED list is the no-row
  sentence set (P7 VA!=PA, P10 LUNA store, P2 sub-word, unclaimed, luna -n 2..4, xmem, 88110, OpenBSD reader, R1
  free-running instruction fetch).

====================================================================================================================
3. GUARD FIELD vs BODY FIELD, and the partition the body induces on each lvalue
====================================================================================================================
  The edited lines are memory_rw.c :614-623 (inside the guard :603) and dev_luna88k.c :624-627.  DEPENDS-ON, walked
  to the enclosing function's boundary (MEMORY_RW_ONE_PAGE :230-786; DEVICE_ACCESS(luna88k) :554-931):
  Dominating predicates of the arm (B9's corrected list, in control-flow order):
   T1 :245  `misc_flags & PHYSICAL || cpu->translate_v2p == NULL' -- m88k always has translate_v2p; every guest row
            is non-PHYSICAL.  Cell held: translating.  (PHYSICAL callers -- e.g. dev_luna88k.c:613-614 -- also carry
            NO_EXCEPTIONS, so they meet T7's set cell, not the body.)
   T2 :259  `!ok' after translate_v2p -> return :268.  Cell held: ok = 2 (APR invalid, or a NULL CMMU,
            memory_m88k.c:130-144).  The other cell is the translation-fault path (memory_m88k.c, not edited -- P12).
   T3 :436  outer device range.  Held: in range.  Out of range = unclaimed (R3).
   T4 :480-481  device match in the scan.  Held: matched (unreadable, vme, luna88k).  Unmatched = unclaimed.
   T5 :584-585  device call `!no_exceptions || DM_READS_HAVE_NO_SIDE_EFFECTS' -- COUPLED with T7 and with `res'
            (codex:59): NO_EXCEPTIONS + DM_DEFAULT (all three refusing devices) skips the call, res stays 0 -> -1.
   T6 :591  `running_before_device_access && !cpu->running' -> return :592.  The cell is "running before AND
            stopped after" (codex:58).  Held: not taken.  Taken = outside the repair path (CL9), unrowed by design.
   T7 :595-596 + :603  `res == 0 -> -1', then `res <= 0 && !no_exceptions' -- THE guard.
   T8 (added) `cache == CACHE_INSTRUCTION ? 0 : 1' -- the selector (equality).
   T9 (added) `cmmu != NULL' -- the NULL test.
   (:283-298 watchpoint, :491-492 #95 zero-fill, :495-524 clamp, :526-581 dyntrans: no early return, no gating.)
  Dominating predicates of the LUNA case: the early windows :567-568, :578-579, :590, :600, :610 all test `addr >='
  a base above 0x3ffffff0 (FUSE 0x43000000, NVRAM 0x45000000, NVRAM_88K2 0x47000000, TRI_PORT 0x71000000 --
  luna88k_board.h:58-60, :70, :118), and `addr = relative_addr + 0x3ffffff0' (:558) is never below 0x3ffffff0, so
  none can be true when the case is reached: jointly unreachable, discharged without rows (codex:126; D2 below).
  Then `switch (addr)' :622, case :624.

  GUARD fields: res, no_exceptions (T7); cache (T8); cpu->cd.m88k.cmmu[idx] (T9).
  BODY fields:  cmmu->reg[CMMU_PFSR], cmmu->reg[CMMU_PFAR] (written); orig_paddr, cache, cpu (read: writes,
                selector, exception); writeflag, mem->devices[i].name, paddr (read by debug() :604-607, inside the
                guard, outside the NULL-guarded block -- body-adjacent, legitimate (d) operand sources, glm-Q34:30).
  Guard != body, and where they DISAGREE:
   * cmmu[idx] (T9) vs cpu (exception target): cmmu[] pointers are written only at machine setup
     (dev_mvme187.c:137, :149 for cpus[bootstrap_cpu]; dev_luna88k.c:946, :957 for cpunr < ncpus) and never cleared.
     The disagreeing state -- a RUNNING cpu that takes exceptions and has a NULL slot -- is mvme187 `-n 2' cpu 1
     after `pause 1' (debugger_cmds.c:1302) -> null surv / null route.
   * orig_paddr (:437) vs paddr (:494): disagree whenever base + offset != offset -> rowed at three disagreeing
     points (0x10, 0x90, 0x0 relative vs absolute).
   * cache (T8) vs no_exceptions (T7): coupled for the debugger (CACHE_NONE | NO_EXCEPTIONS) -> dbg noexc.
   * the shared field reg[PFSR]/reg[PFAR] ("who else writes it, and can they set my value?"): the guest seed store
     (dev_m8820x.c:459-460) sets values the fix never writes (seeds chosen so (x >> 16) & 7 is 2 and 0, not 3);
     the translation-fault writer cannot run in these sessions (APR invalid); the HEAD LUNA case writes the SAME PFSR
     value as the fix (0x30000), which is why `luna pfsr' is green on HEAD and the clause-(b) legs (L3/L4) are what
     separate the two writers.
  Partition the body induces, per lvalue (7n-5: EXHAUSTED = every cell of the BODY-TESTED partition rowed):
   | lvalue            | body test(s)                       | cells                    | held by                   | status    |
   | res               | ==0 -> -1 (:595); <= 0 (:603)      | >=1 served / -1 refused  | ok rows / every refused   | EXHAUSTED |
   | no_exceptions     | !no_exceptions (:603; T5 coupled)  | clear / set              | guest rows / dbg noexc    | EXHAUSTED |
   | cache             | == CACHE_INSTRUCTION (selector,    | INSTRUCTION / other      | ifetch rows / data rows   | EXHAUSTED |
   |                   |   vector expression)               | (other: DATA driven;     |                           |           |
   |                   |                                    |  NONE w/o NO_EXC only    |                           |           |
   |                   |                                    |  from dev_ether, codex:9)|                           |           |
   | cmmu[idx] pointer | != NULL (added)                    | non-NULL / NULL          | refused rows / null rows  | EXHAUSTED |
   | orig_paddr        | none (written verbatim)            | --                       | 0xfff46010, 0xfff40090,   | SAMPLED   |
   |                   |                                    |                          | 0x3ffffff0; untested:     |           |
   |                   |                                    |                          | sub-word residues (P2),   |           |
   |                   |                                    |                          | VA!=PA (P7)               |           |
   | cpu (accessing)   | none                               | --                       | cpu 0 (all), cpu 1 (null) | SAMPLED   |
   | writeflag         | none (debug() only)                | --                       | read: uld vme luna null;  | SAMPLED   |
   |                   |                                    |                          | write: ust; instr x write |           |
   |                   |                                    |                          | unreachable (codex:61)    |           |
   | paddr (relative)  | none (debug() only)                | --                       | 0x10, 0x90, 0x0           | SAMPLED   |
   | devices[i]        | none (name in debug() only)        | -- (SAMPLES, codex:60)   | unreadable, vme, luna88k  | SAMPLED   |
   | len / alignment   | none in the arm (alignment traps   | per width: byte {0..3},  | word, residue 0 only      | SAMPLED   |
   |                   |  first, loadstore.c:168-186)       | half {0,2}, word {0},    |                           | (P2, (e)) |
   |                   |                                    | double {0 mod 8} codex:62|                           |           |
   | LUNA addr         | switch (addr) :622                 | the case / other labels /| the case (word load)      | edited    |
   |                   |                                    | default:                 |                           | arm only  |
  D2 (bound compares the fix depends on): `res <= 0' at B = 0 -- B+1 = 1 served (ok rows), B-1 = -1 refused (every
  refused row), the at-member 0 is mapped away at :595-596.  DISCHARGED.  T8 and T9 are an equality and a NULL test,
  not bounds.  The LUNA early windows' `addr >=' compares cannot reach the case (above) -- discharged, no rows.

====================================================================================================================
4. CHANNEL per row -- the mutant(s) each row kills (leg ids from BUILD_SPEC section 6; L6b proposed in Q6) and the
   observable that differs under it.  "prereq:<kind>" = the row's cause-free prerequisite string replaces its value.
====================================================================================================================
   1 neg apparatus  CONTROL (apparatus).  Bogus subtype `187' -> exit 1, no register dump.  Green by DESIGN on the
                    exit-1 stub (L5); no product variant reaches it.
   2 mv devsig      CONTROL (device signature).  r10/r9 = 0x00a90000.  L19: the IDR load itself faults -> r10/r9
                    stay 0xdeadbeef.
   3 mv cmmu rt     CONTROL (liveness).  r11/r12/r17/r18 = the seeds.  L18: the misplaced write overwrites the data
                    CMMU after every served CMMU access -> r11 0x30000, r12 0xfff7f108.  L19: never loaded.
   4 ok route      L19 (res <= 1).  THE NAMED "v3" CHANNEL IS NOT REACHED: every served CMMU access faults first,
                    so the observable is prereq:nodev (codex:116).  Also red under L18 (prereq:readback).
   5 ok regs        L18 (writes outside res <= 0).  NAMED "changed seeds" CHANNEL NOT REACHED: the readback
                    prerequisite fails first (prereq:readback).  Also L19 (prereq:nodev).
   6 uld route      L17 (exception dropped): path fall, SXIP 0, DMA0 0.
   7 uld pfsr       HEAD/L3 (seed 0x5a5a5a5a), L10 (0x3), L6b (seed).
   8 uld pfar       HEAD/L3 (seed 0x13572468), L11 (0x10), L12 (seed), L6b (seed).
   9 uld icmmu      L13 (iPFSR/iPFAR := 0x30000/0xfff46010), L14 (iPFSR := 0), L6b (written).
  10 ust route      L17 (fall: the store is abandoned, no vector).
  11 ust pfsr       HEAD/L3, L10, L15 (direction-conditioned: seed), L6b.
  12 ust pfar       HEAD/L3, L11, L12, L15, L6b.
  13 ust icmmu      L13, L14, L6b.  (NOT L15 -- codex:114: a read-only repair leaves route and sibling alone.)
  14 vme route      L17.
  15 vme pfsr       HEAD/L3, L10, L16 (VME excluded: seed), L6b.
  16 vme pfar       HEAD/L3, L11 (0x90), L12, L16, L6b.
  17 vme icmmu      L13, L14, L6b.  (NOT L16 -- codex:115.)
  18 luna devsig    CONTROL.  L19.
  19 luna cmmu rt   CONTROL.  L18, L19.
  20 luna route     HEAD (fall/0x0/0x0/r4=0x0: served 0), L4 = L20 (the same), L21 (the same), L17 (fall, r4 kept:
                    the arm returns FAILED, the load writes no register).
  21 luna pfsr      L3 (seed: the case's write gone, the arm unrepaired), L10 (0x3), L21 (seed: write deleted, still
                    served -- the row's UNIQUE variant, codex:117), L6b.  GREEN on HEAD, L4, L20 (the case writes it).
  22 luna pfar      HEAD/L3/L4/L20/L21 (seed), L11 (0x0: the access is AT the device base), L12, L6b.
  23 luna icmmu     L13, L14, L6b.
  24 unasm          CONTROL (literal count).  L5: "0/174".
  25 ifetch route   L17: without the exception the pre-read and to_be_translated both fail, `bad:' stops the cpu
                    (R1, cpu_m88k_instr.c:2989-2993), the handler never runs -> prereq:handler.  (No enumerated
                    variant changes the VECTOR expression; this row would also see vector 3 for an instruction refusal.)
  26 ifetch pfsr    HEAD/L3 (seed 0x2468ace0), L6 (cmmu[0] not written: seed), L10 (0x3), L17 (prereq:handler).
  27 ifetch pfar    HEAD/L3 (seed 0xbadf00d), L6, L11 (0x10), L12, L17.
  28 ifetch dcmmu   L6 (the data CMMU written: 0x30000/0xfff46010), L13, L14 (dPFSR := 0), L17.
  29 dbg noexc      L7: the dump enters the body -> "(memory access failed)", cpu 0 vectors (pc 0x18 after the
                    dump), path v3 at the end, data seeds 0x30000/0xfff46010.  Every component differs.
  30 null surv      L8: cpu 1's refused load dereferences its NULL cmmu[1] -> host SIGSEGV -> how = sig11, no regs.
  31 null route     L9: no exception for cpu 1 -> the abandoned load falls through -> path fall (FELL r6 set,
                    r7 clear).  L17: the same.  L8: prereq:died.
  CHANNEL CHECK (is each named channel able to vary under its named mutant?): yes for 1-3, 6-31.  For 4 and 5 the
  NAMED channel (v3 on an accepted access; changed seeds after an accepted access) cannot be reached by ANY global
  widening, because the probe's own prerequisites are served device accesses that fire first; the row still reds,
  through its prerequisite string.  NOT VACUOUS (the got string varies), but the header must name the channel that
  is actually available (codex:116; B6).  This answers the CHANNEL line's write-time question for this round: the
  channel under each mutant WAS knowable at writing time, and for two rows it is not the one grok:108-109 named.

====================================================================================================================
5. PREDICTED red set per leg (31-row detector; section 0's designs).  The measured table is compared against this.
====================================================================================================================
   leg   variant                                     predicted red rows                                       score
   pre   HEAD binary (prefix_HEAD.out)               uld/ust/vme pfsr+pfar, luna route, luna pfar,            21/31
                                                     ifetch pfsr, ifetch pfar  (SYMPTOM=PRESENT 10/10)
   fix   the four-file fix (fixed.out)               none  (SYMPTOM=ABSENT)                                   31/31
   L1    frozen witness, fixed binary                24/24, SYMPTOM=ABSENT                                    24/24
   L3    arm reinstated, case fixed                  uld/ust/vme pfsr+pfar, luna pfsr, luna pfar,             21/31
                                                     ifetch pfsr, ifetch pfar  (luna route GREEN)
   L4    case reinstated, arm fixed                  luna route, luna pfar  (luna pfsr GREEN)                 29/31
   L5    exit-1 non-emulator stub                    all but `neg apparatus'; CONTROL=FAIL, SYMPTOM=MIXED,    1/31
                                                     exit 1, sentinel printed
   L5b   binary absent                               FileNotFoundError before row 1: no rows, NO sentinel      --
   L6    selector always-data                        ifetch pfsr, ifetch pfar, ifetch dcmmu                    28/31
   L6b   (proposed, Q6) selector always-instruction  uld/ust/vme/luna pfsr+pfar, uld/ust/vme/luna icmmu        19/31
   L7    `!no_exceptions' dropped                    dbg noexc                                                30/31
   L8    NULL check removed                          null surv, null route                                    29/31
   L9    exception moved inside the NULL check       null route                                               30/31
   L10   raw 3                                       uld/ust/vme/luna/ifetch pfsr                             26/31
   L11   PFAR := device-relative paddr               uld/ust/vme/luna/ifetch pfar                             26/31
   L12   PFSR only                                   uld/ust/vme/luna/ifetch pfar                             26/31
   L13   both CMMUs (inside the NULL check)          uld/ust/vme/luna icmmu, ifetch dcmmu                     26/31
   L14   sibling cleared (inside the NULL check)     uld/ust/vme/luna icmmu, ifetch dcmmu                     26/31
   L15   conditioned on writeflag == MEM_READ        ust pfsr, ust pfar                                       29/31
   L16   device-keyed (VME excluded, Q7)             vme pfsr, vme pfar                                       29/31
   L17   exception dropped                           uld/ust/vme/luna route, ifetch route/pfsr/pfar/dcmmu,    22/31
                                                     null route
   L18   writes before the guard (Q8 form)           mv cmmu rt, ok route, ok regs, uld/ust/vme x4, luna      6/31
                                                     cmmu rt, luna x4, ifetch x4, dbg noexc (25 rows; green:
                                                     neg apparatus, mv/luna devsig, unasm, null surv/route)
   L19   guard widened to res <= 1                   mv devsig, mv cmmu rt, ok x2, uld/ust/vme x4, luna       4/31
                                                     devsig, luna cmmu rt, luna x4, ifetch x4, dbg noexc (27;
                                                     green: neg apparatus, unasm, null surv, null route)
   L20   case left returning 1, write kept           == L4 BEHAVIOURALLY (Q5): luna route, luna pfar          29/31
   L21   case write deleted, still returning 1       luna route, luna pfsr, luna pfar                         28/31
  Consequences for BUILD_SPEC section 6's expected column (all in BUILDER_QUESTIONS): "nothing else red" for
  L10-L19 cannot hold as worded, because grok's table predates the ifetch/dbg/null rows -- L10-L14 also red the
  matching ifetch row, L17 also reds the four ifetch rows and null route -- and because L18/L19 fire in every
  session's own prerequisites; L6 also reds ifetch dcmmu; L20 is L4.  Proposed criterion: "the red set equals this
  section's predicted set".

====================================================================================================================
6. DIFF AGAINST THE BRIEF'S SECTION 7 (packet.md:1091-1125) AND PASS1_RULINGS B9
====================================================================================================================
  axis 1 claim                 unchanged (unclaimed is not this arm; R3).
  axis 2 device call           NOT an independent cell: coupled with no_exceptions and res (T5; codex:59).
  axis 3 cpu stopped           relabelled "running before AND stopped after" (codex:58); "unobservable" was wrong
                               (glm-Q12:34) -- it is outside the repair path, unrowed by design (CL9).
  axis 4 res                   unchanged; D2 discharged.
  axis 5 !no_exceptions        set cell: unrowed -> ROWED (dbg noexc; B5b).
  axis 6 selector              instruction label: unrowed -> ROWED (four stepped ifetch rows, R2-dependent; B5a).
  axis 7 NULL check            "no reachable cell found" -> REACHABLE and ROWED (null surv, null route; B5c).
  axis 8 writeflag             debug()-only read inside the guard: a legitimate (d) operand source (L15); P10 stays
                               (e); instruction x write is unreachable (codex:61).
  axis 9 refusing device       SAMPLES, not a body partition (codex:60).
  axis 10 PFAR operand         relabelled: `paddr' is read by debug() inside the guard, outside the NULL-guarded
                               block (glm-Q34:30); `vaddr' is read by NO live m88k code in this unit (the MEM_MIPS
                               block is compiled out) and the sessions leave the APR invalid (P7, clause (e)).
  axis 11 PFSR value           unchanged.
  axis 12 sibling              + ifetch dcmmu (the sibling of cmmu[0]).
  axis 13 width/alignment      + per-width residues (codex:62); misaligned wider accesses trap before memory_rw
                               (cpu_m88k_instr_loadstore.c:168-186).
  axis 14 which cpu            + cpu 1 (mvme187 -n 2, the null rows); luna -n 2..4 still NOT CLAIMED.
  axis 15 LUNA dispatch        + the early-window exclusions, discharged (section 3).
  NEW (B9) T1 translation branch, T2 translation success / early return, T3 outer device range, T4 device match --
                               each held at one cell by every row; the other cells are other paths.
  Section 7's floor sentence is REPLACED by B5: floor = {refused, no_exceptions clear} x {data, instruction} x
  {non-NULL, NULL} as far as jointly reachable, plus served and no_exceptions-set -- all rowed by the 31 rows
  (instruction x NULL is not rowed: cpu 1's instruction fetch would need a refused fetch on a CMMU-less cpu, which
  free-running halts (R1) and stepped rides R2 -- disclosed as clause (e), Q10).

====================================================================================================================
7. WHERE MY READING DIFFERS FROM THE BRIEF, THE RULINGS OR THE SPEC (each with its line; detail in BUILDER_QUESTIONS)
====================================================================================================================
  R-a  C5 / CHECKS #4 / PASS1_RULINGS line 17-19 ("dev_m8820x.c:108 dereferences ... for the ACCESSING cpu") is NOT
       what the code does.  :108 is in m8820x_command(struct cpu *cpu, ...) (:106), whose ONLY caller is :284,
       `m8820x_command(c, d)', with `c = cpu->machine->cpus[d->cpu_nr]' (:250).  So :108 dereferences the CMMU
       OWNER's slot, exactly as :251-252 do.  On mvme187 every CMMU window decodes cpu_nr 0 (:542-543, addr2 0/1),
       and cpus[0] owns both CMMUs, so a CMMU access by CMMU-less cpu 1 reads/writes cpu 0's CMMUs and dereferences
       nothing NULL.  C5 as filed is refuted by reading; the NULL dereference at :250-252 exists only in C4's
       configuration (a random non-zero bootstrap cpu).  The B5c constraint "cpu 1 never touches the CMMU window"
       stays harmless (this design keeps it), but its stated reason is wrong.
  R-b  A6's ordering warrant (grok:32 "order matters because NBSG uses PDT_BITS and PG_BITS") is wrong: NBSG
       (m8820x.h:182) is an object-like macro, expanded only at a use, and nothing in src/ uses it; upstream itself
       placed the include BEFORE m8820x_pte.h (trunk_src.diff:1921-1922).  Either order compiles; "directly after
       :53" is fine, the reason is not.
  R-c  B5c's dispatcher premise ("both cpus start at one pc, so the program begins with a RAM-flag dispatcher") does
       not follow: `focus 1' (debugger_cmds.c:1125) makes `pc=' / `rN=' / `VBR=' act on cpu 1 (debugger_expr.c:167
       resolves names as cpu[debugger_cur_cpu].<name>; cpu_m88k.c:141-153 registers pc, r0-r31 and the control
       registers by name), and `reg 1' / `reg 1,0' (debugger_cmds.c:1653) read cpu 1's registers.  Markers can live
       in registers (the probe's existing path_of idiom), not RAM.
  R-d  Stepping with two RUNNING cpus advances BOTH, one instruction each per step (machine_run,
       machines/machine.c:710; single-step run_instr executes one instruction, cpu_dyntrans.c:272-327).  The design
       therefore pauses cpu 0 before cpu 1 runs, so each cpu's step count is exact.
  R-e  B5b's "already killed by `ok regs'" dissent (GLM-Q12:34) is correctly rejected by the ruling: under L7 the
       accepted access is unaffected; only a NO_EXCEPTIONS access to a refusing device changes -- the dump.
  R-f  The 24-row detector's grok:98-111 table (B6) predates the new rows; section 5 above re-derives the red set for
       31 rows.  Notably L6 reds ifetch dcmmu too, and L18/L19's named channels are unreachable (section 4).

PRETABLE_DONE

####################################################################################################################
AMENDMENT 1 -- 2026-10-23 ~22:3x -0500, still BEFORE table 1 (no leg, no prefix/fixed run has happened).
Cause: BUILD_SPEC.md section 10 and PASS1_RULINGS.md section E were found in the spec files (BUILD_SPEC mtime
21:53:27) after the body above was drafted from the 21:46 text; plus three HEAD-binary explorations
(explore_20261023/: E1-E2 explore_null_dbg.out, E3-E4 explore_c5_ixnull.out, E5 explore_conj.out -- explorations,
not rows, not legs).  The body above is NOT edited; where this amendment differs, this amendment rules.  Every design
point marked [Q<n>] still needs the main loop's ruling (BUILDER_QUESTIONS.md).
####################################################################################################################

AM-1  THE NULL SESSION IS REDESIGNED to section 10's CONJUNCTIVE form, in the STEPPED shape the piped idiom can carry
      [Q1].  Measured on the HEAD binary as E5 (explore_conj.out): mvme187 `-n 2'; cpu 0 runs the seeded `uld' program
      alone (19 steps) and parks in H's `br .'; `tlbdump 1' (no "cpu1: CMMU" line = the NULL premise); RAM markers
      0xf000 (HANDLED) / 0xf004 (FELL) zero-initialised by `put'; `focus 1' sets cpu 1's pc = 0x10200, r5 = 0xfff46010,
      r20 = 0x4a4a4a4a, r21 = 0x46464646 and its OWN VBR = 0x30000 by `VBR=' [Q3]; `pause 1'; then
        part 1  `step 3': ld r4,r5,0 (refused DATA load, cmmu[1] NULL) -> cpu 1's vector 3 at 0x30018: st r20 -> HANDLED,
                br J  (the FELL store `st r21,r0,0xf004' after the load runs only if no exception was raised; br J)
                -> `dump 0xf000 0xf008', `reg 1', `reg 1,0'   [E5: H=4a4a4a4a F=0, pc J=0x1020c; SXIP/DMA0 read HERE,
                because the second fault zeroes DMA0 (cpu_m88k.c:870-879; E5: DMA0 0 at the end)]
        part 2  `step 5': J: jmp (r5) -> the instruction fetch at 0xfff46010 is refused with cmmu[0] NULL (stepped:
                the R2 pre-read reaches memory_rw.c's arm); SFRZ is still set, so the vector is ERROR (10), VBR1+0x50,
                where `br .' parks cpu 1 [Q2]  -> `dump 0xf000 0xf008', `reg 1'   [E5: markers unchanged, pc 0x30050,
                one "SFRZ already set" line, three device-failed lines in the session: cpu 0's, cpu 1's data, cpu 1's
                instruction]
      ROWS:  null route = part 1: "<handled|fell|both|neither>/<SXIP>/<DMA0>", want "handled/0x10202/0xfff46010".
             null surv  = "<how>/<both marker dumps readable>", want "exit0/readable".
      PREREQUISITES (cause-free strings, cpu 1 only [Q4]): `tlbdump 1' shows no cpu1 CMMU; cpu 1 at J after part 1;
             cpu 1 OFF J after part 2 (the fetch was attempted); for null surv also a device-failed line after part 1's
             dump (the instruction refusal reached the arm).  cpu 0's results feed no null row.
      The B5c constraint "cpu 1 never touches the CMMU window" is WITHDRAWN (section E; E3 MEASURED it: cpu 1 read both
      IDR windows -- cpu 0's 0x00a90000 -- and stored an SCR command that reaches m8820x_command(), :108; exit0, no
      fault).  cpu 1 still touches no CMMU window, because nothing in its path needs one.

AM-2  THE {data, instruction} x {CMMU present, absent} CROSS-PRODUCT (section 10 / E B5c), with the rows holding each:
        data x present         uld/ust/vme/luna pfsr, pfar, icmmu (+ their route rows as attribution)
        instruction x present  ifetch pfsr, ifetch pfar, ifetch dcmmu (+ ifetch route as attribution CONTROL, AM-5)
        data x absent          null route (HANDLED set and FELL clear = the exception stayed OUTSIDE the NULL check;
                               reaching part 1's dump = survival through the data cell)
        instruction x absent   null surv (reaching part 2's prompt with both dumps readable = survival through the
                               instruction refusal's arm with cmmu[0] NULL)
      The joint cell licenses no cpu-number, address or device-name products (section E, Q3 bound).

AM-3  WHICH BODY each field list of section 3 enumerates (section 10):
        OUTER refusal-guard body (`if (res <= 0 && !no_exceptions)', :603-625): debug() reads writeflag,
            mem->devices[i].name and paddr (:604-607); the M88K block reads cache and cpu (selector, exception) and
            the inner guard's operands; return MEMORY_ACCESS_FAILED.  writeflag / paddr / devices[i] are body fields
            of THIS body only.
        INNER NULL-guard body (added): reads the selected cmmu pointer, orig_paddr and the constant
            CMMU_PFSR_BERROR; writes cmmu->reg[CMMU_PFSR] and cmmu->reg[CMMU_PFAR].  Nothing else.
      So section 3's "body-adjacent" writeflag / paddr / devices[i] are OUTER-body fields; the inner body reads none of
      them.

AM-4  VARIANT CLASSES (section 10: VALUE corruption vs guard-OPERAND swaps):
        VALUE / TARGET corruption (inner body; who is written stays right, what or where is wrong):
            L10 raw 3 (PFSR value); L11 PFAR := paddr and L12 PFAR not written (PFAR value); L6 always-data and L6b
            always-instruction [Q12] (target CMMU); L13 both CMMUs and L14 sibling cleared (extra target).  Not
            built, clause (e): PFAR := vaddr (P7), sub-word PFAR (P2).
        GUARD-OPERAND swaps and PLACEMENT (which accesses are written, or where the exception sits):
            inner guard: L8 NULL check removed; L8b NULL check conditioned on the data label [Q15]; L15 + writeflag;
            L16 + device name [Q13]; L9 exception moved inside it.  Outer guard / body: L7 `!no_exceptions' dropped;
            L19 `res <= 1'; L18 writes moved before it [Q14]; L17 exception dropped.

AM-5  CHANNEL changes to section 4:
        25 ifetch route  an ATTRIBUTION CONTROL (section 10; E B5a): the vector expression (:620-622) reads `cache'
                         independently of the added selector, so it CANNOT vary under L6 -- VACUOUS against the selector
                         by construction.  Its variant: L17 (exception dropped / mis-routed) [Q7: CONTROL_ROWS or not].
        26-27            ifetch pfsr / ifetch pfar carry L6 (unchanged).
        30 null surv     L8 (sig11 in part 1), L8b (sig11 in part 2 -- the instruction refusal's dereference).
        31 null route    L8 (died before part 1's dump), L9 (fell: no exception for a NULL-CMMU cpu), L17 (fell).
                         GREEN under L8b: part 1's dump precedes the crash and is flushed at the next prompt
                         (debugger.c:380-383 fflush(stdout) after printing the prompt).

AM-6  PREDICTED red sets -- changes to section 5 only (everything else stands):
        L8    null surv, null route                                                         29/31 (unchanged)
        L8b   null surv                                                                     30/31 (NEW leg)
        L9    null route                                                                    30/31 (unchanged)
        L17   uld/ust/vme/luna route, ifetch route/pfsr/pfar/dcmmu, null route              22/31 (unchanged; null
              surv GREEN: part 2's fetch takes R1's halt, cpu 1 stops off J, both dumps readable)
        L18   as section 5 (null rows GREEN: cpu 1's accesses are a refused load, RAM stores and a refused fetch)
        L19   as section 5 (null rows GREEN for the same reason; cpu 0's uld path may halt at its ERROR vector, which
              feeds no null row)
        L3/L4 on BOTH instruments (section 10): frozen 24-row witness L3 16/24 (uld/ust/vme pfsr+pfar, luna pfsr,
              luna pfar), L4 22/24 (luna route, luna pfar); 31-row detector L3 21/31, L4 29/31 (section 5).
        unasm literal: re-derived by hand before the first run [Q9]: 115 + ifetch 23 + dbg 23 + null 31 (VEC0 4,
              CODE0 13, H 6, CODE1 4, VEC1 4) = 192 under Q4(a); 169 under Q4(b) (null 8).

AM-7  Section 7 R-a (C5) and R-b (A6) are now RULED the same way by section E (C5 withdrawn; "order matters"
      withdrawn).  R-c/R-d stand and are now MEASURED (E2, E5).  New: section 10's "vector 2" for cpu 1's instruction
      refusal is contradicted by cpu_m88k.c:811-819 once the data fault has set SFRZ (measured E5: ERROR) -- the arm
      still runs first (memory_rw.c:614-622 order), so the NULL test and L8b's dereference are reached either way [Q2].
      And section 10's machine-wide-breakpoint concern (cpu_dyntrans.c:1802-1804) does not arise: the stepped form
      uses no breakpoint.

PRETABLE_AMENDMENT_1_DONE
~~~~

### 3.6 The gates (`table1_20261023/gates/`)
Gate 14 (`gate14_run.out`; `run.sh 14`; PMAX = `build/gxemul` `931e69fa`, which also carries the peer's uncommitted
files; private LOGDIR) -- the header, `#568`'s pin, the whole `#570` block, the verdict, VERBATIM:
~~~~
RUN_GATE_START gate 14 2026-10-23 23:17:54 -0500  LOGDIR=/tmp/gxt36/gatelogs14  PMAX=<default $ROOT/build/gxemul>
build/gxemul: 931e69fad9624daef30e83d274a4493d  /mnt/c/DocumentNoSnc/CC/GXEMUL/build/gxemul  mtime 2026-10-23 23:11:37.989651700 -0500
regress/gate_arm.sh md5 5ee94e61a100473ba95db05f43f34a96; m88k_buserr_probe.py md5 d57c12ab7ade903946c7d80a8e153ab7
   ...
  ok   vme default probe completed                          yes
  ok   vme_default rows run                                 38
  ok   vme_default rows correct                             38
  ok   vme default controls                                 1
   ...  (1777-1814: the 38 per-row checks of #568, all ok)
  ok   vme default rows emitted                             38
  ok   vme default rows green                               38
  ok   vme default rows red                                 0
  ok   m88k buserr probe completed                          yes
  ok   m88k buserr sentinel once                            1
  ok   m88k_buserr rows run                                 31
  ok   m88k_buserr rows correct                             31
  ok   m88k buserr controls                                 1
  ok   m88k buserr symptom absent                           1
  ok   m88k buserr row: neg apparatus                       1
  ok   m88k buserr row: mv devsig                           1
  ok   m88k buserr row: mv cmmu rt                          1
  ok   m88k buserr row: ok route                            1
  ok   m88k buserr row: ok regs                             1
  ok   m88k buserr row: uld route                           1
  ok   m88k buserr row: uld pfsr                            1
  ok   m88k buserr row: uld pfar                            1
  ok   m88k buserr row: uld icmmu                           1
  ok   m88k buserr row: ust route                           1
  ok   m88k buserr row: ust pfsr                            1
  ok   m88k buserr row: ust pfar                            1
  ok   m88k buserr row: ust icmmu                           1
  ok   m88k buserr row: vme route                           1
  ok   m88k buserr row: vme pfsr                            1
  ok   m88k buserr row: vme pfar                            1
  ok   m88k buserr row: vme icmmu                           1
  ok   m88k buserr row: luna devsig                         1
  ok   m88k buserr row: luna cmmu rt                        1
  ok   m88k buserr row: luna route                          1
  ok   m88k buserr row: luna pfsr                           1
  ok   m88k buserr row: luna pfar                           1
  ok   m88k buserr row: luna icmmu                          1
  ok   m88k buserr row: ifetch route                        1
  ok   m88k buserr row: ifetch pfsr                         1
  ok   m88k buserr row: ifetch pfar                         1
  ok   m88k buserr row: ifetch dcmmu                        1
  ok   m88k buserr row: dbg noexc                           1
  ok   m88k buserr row: null surv                           1
  ok   m88k buserr row: null route                          1
  ok   m88k buserr row: unasm                               1
  ok   m88k buserr rows emitted                             31
  ok   m88k buserr rows green                               31
  ok   m88k buserr rows red                                 0
   ...
gate 14: ARM/Thumb flags (#311/#312/#319-#322/#328/#329): PASS (1310 checks)

############################################################
## SUMMARY
############################################################
  PASS 14. gate_arm

  passed 1   failed 0   skipped 0
  GATE_COVERAGE=1/16 (SUBSET: 14)

REGRESS_PASS
RUN_SH_RC=0  wall=7974s
copied m88k_buserr.log (5863 bytes; last line: M88K_BUSERR_PROBE_DONE)
copied vme_default.log (6450 bytes; last line: VME_DEFAULT_PROBE_DONE)
copied gate_arm.log (12360 bytes; last line: ARM_FLAGS_RESULT=190/190)
RUN_GATE_DONE gate 14 2026-10-24 01:30:48 -0500
~~~~
*(Drafter's count of that log: 1310 `ok` check lines, 0 `FAIL`.  The `#570` block is 40 checks: 6 structural before
the loop, the 31 rows, 3 after.)*

Gate 11 (`gate11_run.out`; `run.sh 11`; the luna rig image present), the verdict, VERBATIM:
~~~~
RUN_GATE_START gate 11 2026-10-24 01:31:37 -0500  LOGDIR=/tmp/gxt36/gatelogs11  PMAX=<default $ROOT/build/gxemul>
build/gxemul: 931e69fad9624daef30e83d274a4493d  /mnt/c/DocumentNoSnc/CC/GXEMUL/build/gxemul  mtime 2026-10-23 23:11:37.989651700 -0500
regress/gate_arm.sh md5 5ee94e61a100473ba95db05f43f34a96; m88k_buserr_probe.py md5 d57c12ab7ade903946c7d80a8e153ab7
   ...
gate 11: m88k rounding mode (#298): PASS (111 checks)

############################################################
## SUMMARY
############################################################
  PASS 11. gate_m88k_rounding

  passed 1   failed 0   skipped 0
  GATE_COVERAGE=1/16 (SUBSET: 11)

REGRESS_PASS
RUN_SH_RC=0  wall=247s
copied gate_m88k_rounding.log (4063 bytes; last line: M88K_ROUND_RESULT=80/80)
copied gate_m88k_idle.log (240 bytes; last line: M380_RESULT=3/3)
copied m8820x_sites.log (1739 bytes; last line: PROBE_WALL=3.7s for 9 rows)
copied luna_intmask.log (2252 bytes; last line: PROBE_WALL=1.0s)
copied m88k_exc.log (12715 bytes; last line: M88KEXC_DONE)
copied luna_absentcpu.log (9378 bytes; last line: LUNAABS_DONE)
RUN_GATE_DONE gate 11 2026-10-24 01:35:44 -0500
~~~~
*(111 `ok`, 0 `FAIL`.)*  `gates/grep3ffffff0.out` -- `grep -rn 3ffffff0 regress/*.py regress/*.sh`, VERBATIM:
~~~~
regress/m88k_buserr_probe.py:16:reads them saw whatever they held before.  The LUNA probe address -- src/devices/dev_luna88k.c's `case 0x3ffffff0' --
regress/m88k_buserr_probe.py:36:  * src/devices/dev_luna88k.c: the 0x3ffffff0 case returns 0, so the access is refused through the repaired arm (its
regress/m88k_buserr_probe.py:98:  the LUNA probe address 0x3ffffff0 = LUNA88K_REGISTERS_BASE (dev_luna88k.c), `case 0x3ffffff0'; device-relative 0.
regress/m88k_buserr_probe.py:133:  the LUNA probe address (luna-88k, `ld r4,r5,0' at 0x3ffffff0)
regress/m88k_buserr_probe.py:134:    luna route     vector 3, SXIP, DMA0 = 0x3ffffff0, r4 keeps its sentinel.  HEAD: fall-through, SXIP 0, DMA0 0,
regress/m88k_buserr_probe.py:139:    luna pfar      data PFAR = 0x3ffffff0.  HEAD: the seed.  L3, L4, L11 (0x0: the access is AT the base), L12, L21,
regress/m88k_buserr_probe.py:194:  * a LUNA STORE at 0x3ffffff0 (the generic direction is pinned by `ust');
regress/m88k_buserr_probe.py:267:LUNA_PROBE = 0x3ffffff0     # LUNA88K_REGISTERS_BASE == the `case 0x3ffffff0' label
regress/m88k_buserr_probe.py:646:row("luna route", g_lr, w_lr, "ld 0x3ffffff0: a refused access raises vector 3, serves nothing")
regress/gate_arm.sh:1919:#  address), and luna-88k's 0x3ffffff0 probe case is refused through that arm instead of being served 0.  The
~~~~

### 3.7 The LUNA boot A/B (A11) -- `boot_base.out`, `boot_work.out`, `boot_ab/console_diff_base_vs_fixed.txt`, VERBATIM
~~~~
BOOT_AB_START base 2026-10-23 22:49:37 -0500
binary: 2efeec559ec5b3d16b200cccf4203631  /tmp/gxt36/base/gxemul  mtime 2026-10-23 19:43:15.594860199 -0500
image : 2147483648 Jul 28 23:51 /mnt/c/DocumentNoSnc/CC/GXEMUL/_images/liveimage-luna88k-raw-20250518.img
shape : run_emu_progress 1800 12000000000 120 'login:' /mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/m88kbuserrregs/table1_20261023/boot_ab/ab_luna_base.log /tmp/gxt36/base/gxemul -N -e luna-88k -d R:/mnt/c/DocumentNoSnc/CC/GXEMUL/_images/liveimage-luna88k-raw-20250518.img boot
result: reason=MARKER ninstrs=7651336103 wall=125
markers 'LUNA-88K BOOT':'M88100':'login:' = 1:1:1
log: 17495 bytes, 329 lines; last non-blank line: login: 
BOOT_AB_DONE base 2026-10-23 22:51:42 -0500
BOOT_AB_START work-fixed 2026-10-23 22:51:52 -0500
binary: 3cd0501cf7c854e0662797ccee1fce64  /tmp/gxt36/work/gxemul  mtime 2026-10-23 22:48:32.737750921 -0500
image : 2147483648 Jul 28 23:51 /mnt/c/DocumentNoSnc/CC/GXEMUL/_images/liveimage-luna88k-raw-20250518.img
shape : run_emu_progress 1800 12000000000 120 'login:' /mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/m88kbuserrregs/table1_20261023/boot_ab/ab_luna_work-fixed.log /tmp/gxt36/work/gxemul -N -e luna-88k -d R:/mnt/c/DocumentNoSnc/CC/GXEMUL/_images/liveimage-luna88k-raw-20250518.img boot
result: reason=MARKER ninstrs=7550665157 wall=120
markers 'LUNA-88K BOOT':'M88100':'login:' = 1:1:1
log: 17305 bytes, 326 lines; last non-blank line: login: 
BOOT_AB_DONE work-fixed 2026-10-23 22:53:52 -0500
~~~~
~~~~
14c14
<             overlay 0: /tmp/gxemul.6.overlay.ueE6ZHhP
---
>             overlay 0: /tmp/gxemul.6.overlay.K1x4sQX3
20,22c20,22
< |/-\|/-\|booting sd(0,0):/bsd: /-\|/3232300-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-
< \|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|+494212/ [184081-\|/-\|/-\|/-\|/-\|/-\|+82+179408/-\|/-\|/-\|/-\|/-\|/
< -+152550\|/-\|/-\|/-\|/-\|/]=0x6ffeec
---
> |/-\|/-\|booting sd(0,0):/bsd: /-\|/3232300-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/
> -\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|+494212/ [184081-\|/-\|/-\|/-\|/-\|/-\|+82+179408/-\|/-\|/-\|/-\|/
> -\|/-+152550\|/-\|/-\|/-\|/-\|/]=0x6ffeec
93c93,94
< checking quotas: done.
---
> checking quotas:
>  done.
104c105
< Sat Oct 24 12:51:37 JST 2026
---
> Sat Oct 24 12:53:47 JST 2026
~~~~
*Drafter's reading: neither boot log carries a line naming 0x3ffffff0, a failed device access or an exception
(`grep -i '3ffffff0\|failed\|bus error\|exception'` over both: no hits), so these logs do not show whether the boot
touched the LUNA probe address (P7).*

### 3.8 The build, the object compare and the two-part clearance
`table1_20261023/build_work_fixed.out`, VERBATIM:
~~~~
BUILD_WORK_FIXED_START 2026-10-23 22:48:04 -0500
  copied src/cpus/memory_rw.c  cmp vs SEC: CLEAN  md5=b36c9e1331688ee515f416788a453b80
  copied src/cpus/cpu_m88k.c  cmp vs SEC: CLEAN  md5=0321e2ba68c8a44a604b995a2e2cc908
  copied src/devices/dev_luna88k.c  cmp vs SEC: CLEAN  md5=e43c39ca5722c1a798cccff03fd1e02f
  copied src/devices/dev_m8820x.c  cmp vs SEC: CLEAN  md5=c229294fd28f6c6fa313fbe572589ba2
  removed src/cpus/*.o and the binary; objects left: 178
  MAKE_RC=0 (not the freshness test)
  error lines: 0   'warning:' lines: 0
  compiled in this build (cc -c lines naming a source): 48
  -rwxr-xr-x 1 root root 6159736 2026-10-23 22:48:32.737750921 -0500 /tmp/gxt36/work/gxemul
  [ gxemul -nt src/cpus/memory_rw.c ] -> FRESH
  [ gxemul -nt src/cpus/cpu_m88k.c ] -> FRESH
  [ gxemul -nt src/devices/dev_luna88k.c ] -> FRESH
  [ gxemul -nt src/devices/dev_m8820x.c ] -> FRESH
  3cd0501cf7c854e0662797ccee1fce64  /tmp/gxt36/work/gxemul
== object compare, pre-edit (unmodified HEAD build) vs fixed build ==
  CHANGED gxemul
  CHANGED src/cpus/cpu_m88k.o
  CHANGED src/devices/dev_luna88k.o
  identical: 221   changed: 3
  /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/t36/build/objmd5_work_before.txt:e695696d2e3d99acb0924b929d75a8ac  src/devices/dev_m8820x.o
  /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/t36/build/objmd5_work_after.txt:e695696d2e3d99acb0924b929d75a8ac  src/devices/dev_m8820x.o
BUILD_WORK_FIXED_DONE 2026-10-23 22:48:32 -0500
~~~~
*(`work_fixed_make.log` line 75 compiles `dev_m8820x.o` from the edited `dev_m8820x.c` -- so its identical md5 is a
measurement of an object that WAS rebuilt.)*  `table1_20261023/CLEARANCE_final.out`, VERBATIM:
~~~~
CLEARANCE_START 2026-10-24 01:36:24 -0500
SEC md5s: memory_rw.c=b36c9e133168 cpu_m88k.c=0321e2ba68c8 dev_luna88k.c=e43c39ca5722 dev_m8820x.c=c229294fd28f 
divergence set (derived; none of the four may be in it): src/devices/.index src/devices/Makefile.skel src/devices/autodev.c src/devices/dev_jazz.c src/devices/dev_ne2000.c src/machines/machine_arc.c 
  /mnt/c/DocumentNoSnc/CC/GXEMUL/est part1 CLEAN      part2 N/A (source tree, no binary); no sentinel
  /mnt/c/DocumentNoSnc/CC/GXEMUL/build part1 CLEAN      part2 FRESH (binary 931e69fad962, 2026-10-23 23:11:37); no sentinel
  /mnt/c/DocumentNoSnc/CC/GXEMUL/build-asan part1 CLEAN      part2 FRESH (binary 9d0e06809a1d, 2026-10-23 23:14:18); no sentinel
  /tmp/gxsec-build                   part1 CLEAN      part2 FRESH (binary 8d882c052a5b, 2026-10-23 23:12:15); no sentinel
  /tmp/gxt36/work                    part1 CLEAN      part2 FRESH (binary 3cd0501cf7c8, 2026-10-23 22:48:32); no sentinel
  leg trees left in /tmp/gxt36/legs: 0
CLEARANCE_DONE 2026-10-24 01:36:26 -0500
~~~~

### 3.9 The builder's own report -- `table1_20261023/BUILD_REPORT.md` sections 6 and 7, VERBATIM
~~~~
## 6. Where this build disagreed with the spec or a ruling (by id)

1. **BUILD_SPEC section 10, section 5.1's rationale.**  It says "after m8820x_pte.h because that is upstream's placement".
   Upstream placed the include BEFORE m8820x_pte.h (`research_20261022/trunk_src.diff:1921-1922`, as packet.md 3.4
   quotes it).  I placed it after `:53` as sections 5.1, 10 and 11 direct; the comment claims only that upstream adds the
   same include to this file, not its position.  The position is not load-bearing (NBSG is expanded only at a use, and
   nothing uses it).
2. **The staged checker copy is named `staged/check_probe_wiring.py.txt`**, not `.py`.  This follows Q19: a `.py` under
   regress/artifacts that is ever staged needs a MANIFEST line itself.  The copy is byte-for-byte what the commit should
   carry.
3. **The working-tree insertions into `gate_arm.sh` and the checker were made after section 7, not in section 3.**  The
   staged copies were made at the same moment, and the insertions are measured identical.  The working-tree gate 14
   therefore never ran the new block against a build/ that did not yet carry the fix.
4. **Gate 14 ran as a harness-tracked background job, not in the foreground.**  Its last full run took about 2 h 12 min
   (the /tmp/gxregress logs of 2026-10-19), and the Bash tool's foreground cap is 10 min.  A timed-out foreground WSL
   call orphans the job, which the carrier warns against.  It ran alone, one job at a time, with a private LOGDIR.
   Gate 11 and the boots ran in the foreground.
5. **The unfrozen detector was smoke-run once on the HEAD binary before the freeze** (`smoke_HEAD_unfrozen.out`).  Its
   rows are identical to the official `prefix_HEAD.out`.  It is disclosed so that no number is read as fitted.
6. **dev_m8820x.c's comments were rewrapped so the line count did not change**, because `FAILURE()` embeds `__LINE__` at
   `:537`.  One wording changed at the `:453` site to fit: "dropping the handler's store" became "dropping its store".
7. **C5 is WITHDRAWN** (section E) and is also MEASURED: on the HEAD binary, CMMU-less cpu 1 read both IDR windows
   (cpu 0's 0x00a90000) and stored an SCR command that reaches `m8820x_command()` (`:108`); exit 0, no fault
   (`explore_20261023/explore_c5_ixnull.out`, E3).  **C4** stays conditional on a NONZERO bootstrap cpu,
   source-derived and unmeasured.
8. **Records were not edited** (CHANGELOG, OUTSTANDING_BUGS, ledger, matrix); they are the main loop's.  For Q2's
   "record the SFRZ mechanism in the CHANGELOG", a draft sentence: *In the `null` session cpu 1's instruction-fetch
   refusal follows its data fault while PSR.SFRZ is still set (no `rte` clears it: an `rte` would resume at SNIP, the
   FELL store), so m88k_exception delivers it as ERROR (vector 10) -- the arm, and its NULL test, run before the
   exception either way; measured E5 and in every null-session transcript.*

## 7. Open items (for pass 2 and the main loop)

* B14: the one ask-again on this clean table is the main loop's.
* The R2 re-root obligation of the four `ifetch` rows and of the null session's instruction cell goes with C1/C2
  (the contract discloses it).
* The working-tree `check_probe_wiring.py` now reports 7 GHOSTs: the 5 earlier unowned ones plus this round's two,
  until the two `.py` files are staged.  A simulated staging run (domain() patched, no index touched) of the
  HEAD-based staged copy gives PROBEWIRING_PASS: the detector is "RUN by gate_arm.sh:1927" and the witness "not run
  (correct)" (`drivers/sim_staged_wiring.py.txt`).
* `/tmp/gxt36/work` now holds the FIXED tree (binary `3cd0501c`); `/tmp/gxt36/base` is the HEAD baseline (`2efeec55`).
  No leg tree is left, and no `.MUTANT` sentinel exists anywhere.
~~~~

---

## 4. Section C0 -- has this round already shipped?  (`C0_OUTPUT.txt` beside this brief, VERBATIM)
~~~~
# SECTION C0 -- has round #570 (m88kbuserrregs) already shipped?  Run 2026-10-24 01:48:26 -0500 against
# HEAD 7fca71876a996868fa47034fa8727375ce59653d.  git OBJECT reads only (log / show / ls-tree / ls-files); no status, no diff.

## 0. HEAD
$ git log --oneline -3
7fca7187 records: `m88kscaledbyte` names its landing commit 66920157, and 66920157's committed-tree proofs and pass-2/3 receipts
66920157 #569 m88kscaledbyte: the m88k load/store table's 24 scaled-byte slots were NULL and indexed unguarded -- the generator names the unscaled byte handlers, the table is regenerated, a 123-row offline detector is gated in gate 2; held for Fable
0efeb283 probe wiring: alpha_tbi_probe.py's gate-wiring exemption came due 2026-10-22 with its Alpha gate home still owed and refused every commit -- re-dated to 2026-11-06 by owner ruling, in its own commit

## 1. git log -1 -- <each file the round touches>
$ git log -1 --format='%h %ad %s' --date=short -- src/cpus/memory_rw.c
50fb2ee0 2026-08-20 PIT panel recorded, and the pass 2 the hook demanded found two real things in my own comment
$ git log -1 --format='%h %ad %s' --date=short -- src/cpus/cpu_m88k.c
79cd12e8 2026-09-06 #502 pass 9-12 and #503: two fixes shipped, a filing overturned to a floor breach and repaired, and a detector's own contract predicting both of its escapes
$ git log -1 --format='%h %ad %s' --date=short -- src/devices/dev_luna88k.c
79cd12e8 2026-09-06 #502 pass 9-12 and #503: two fixes shipped, a filing overturned to a floor breach and repaired, and a detector's own contract predicting both of its escapes
$ git log -1 --format='%h %ad %s' --date=short -- src/devices/dev_m8820x.c
2a5bc480 2026-08-16 R9 (#435): half this device's translation-cache purges were for registers nothing reads
$ git log -1 --format='%h %ad %s' --date=short -- regress/gate_arm.sh
2ca79b90 2026-10-21 #568 (vmedefaultkill): dev_vme.c's default: no longer ends the emulator -- the 26 header-named registers decline with one announce each, every other offset faults to the guest; a 3
$ git log -1 --format='%h %ad %s' --date=short -- tools/pipeline/check_probe_wiring.py
0efeb283 2026-10-23 probe wiring: alpha_tbi_probe.py's gate-wiring exemption came due 2026-10-22 with its Alpha gate home still owed and refused every commit -- re-dated to 2026-11-06 by owner ruling,
$ git log -1 --format='%h %ad %s' --date=short -- regress/m88k_buserr_probe.py
(no commit touches this path -- it does not exist at HEAD)
$ git log -1 --format='%h %ad %s' --date=short -- CHANGELOG.md
7fca7187 2026-10-23 records: `m88kscaledbyte` names its landing commit 66920157, and 66920157's committed-tree proofs and pass-2/3 receipts
$ git log -1 --format='%h %ad %s' --date=short -- OUTSTANDING_BUGS.md
66920157 2026-10-23 #569 m88kscaledbyte: the m88k load/store table's 24 scaled-byte slots were NULL and indexed unguarded -- the generator names the unscaled byte handlers, the table is regenerated, a
$ git log -1 --format='%h %ad %s' --date=short -- tools/pipeline/ledger.json
7fca7187 2026-10-23 records: `m88kscaledbyte` names its landing commit 66920157, and 66920157's committed-tree proofs and pass-2/3 receipts
$ git log -1 --format=%h -- regress/artifacts/m88kbuserrregs/
(no commit touches this directory)

## 2. grep <row id> CHANGELOG.md / OUTSTANDING_BUGS.md (at HEAD, via git show HEAD:<file>)
$ git show HEAD:CHANGELOG.md | grep -c -- 'm88kbuserrregs'   ->  0
$ git show HEAD:OUTSTANDING_BUGS.md | grep -c -- 'm88kbuserrregs'   ->  3
$ git show HEAD:CHANGELOG.md | grep -c -- '#570'   ->  0
$ git show HEAD:OUTSTANDING_BUGS.md | grep -c -- '#570'   ->  0
$ git show HEAD:CHANGELOG.md | grep -c -- 'm88k_buserr_probe'   ->  0
$ git show HEAD:OUTSTANDING_BUGS.md | grep -c -- 'm88k_buserr_probe'   ->  0
$ git show HEAD:CHANGELOG.md | grep -c -- 'T36'   ->  3
$ git show HEAD:OUTSTANDING_BUGS.md | grep -c -- 'T36'   ->  4
-- the HEAD CHANGELOG lines naming '#570' or 'm88kbuserrregs' (none expected if the round has not shipped):
-- the HEAD OUTSTANDING_BUGS lines naming 'm88kbuserrregs':
34:> 5. `m88kbuserrregs` (MED, new) -- 88K bus errors carry no PFSR/PFAR; the carrier of the reopened PFAR item.  T36;
1934:>   defect, reopened under `m88kbuserrregs` (TRIAGE.md T36, filed in the 2026-10-22 section at the end of this
25336:* **`m88kbuserrregs` (MED, open)** -- new.  cpus/memory_rw.c MEM_M88K device-failure arm + devices/dev_luna88k.c case

## 3. ls <the directories the round's new files live in>
$ git ls-files regress/ | grep -i -E "buserr"   (tracked at HEAD/index)
(none tracked)
$ git ls-tree -r --name-only HEAD regress/artifacts/m88kbuserrregs/ | wc -l
0
$ ls regress/ | grep -i buserr   (working tree, read-only)
m88k_buserr_probe.py
$ ls regress/artifacts/m88kbuserrregs/   (working tree, UNTRACKED)
pass1_20261023
pass2_20261023
table1_20261023
witness_20261023
$ git ls-tree --name-only HEAD tools/pipeline/ | grep -i -E "wiring|witness"
tools/pipeline/check_probe_wiring.py
tools/pipeline/check_witness.py

## 4. the ledger row at HEAD (git show HEAD:tools/pipeline/ledger.json)
rows in ledger: 1073; rows with id m88kbuserrregs: 1
state='open' sev='MED' witness='none' commits='' opened='2026-10-22'
stages present: []

## 5. est/ twin -- the four product files are SHARED (not in tools/est_divergence.txt)
$ grep -vE "^\s*(#|$)" tools/est_divergence.txt   (derived, not quoted)
src/devices/.index
src/devices/Makefile.skel
src/devices/autodev.c
src/devices/dev_jazz.c
src/devices/dev_ne2000.c
src/machines/machine_arc.c
cmp WT:src/cpus/memory_rw.c est/src/cpus/memory_rw.c -> IDENTICAL
cmp WT:src/cpus/cpu_m88k.c est/src/cpus/cpu_m88k.c -> IDENTICAL
cmp WT:src/devices/dev_luna88k.c est/src/devices/dev_luna88k.c -> IDENTICAL
cmp WT:src/devices/dev_m8820x.c est/src/devices/dev_m8820x.c -> IDENTICAL

## 6. the round's files: HEAD vs working tree (the numstat-equivalent; plain diff(1) of git show HEAD:<f> against
##    the working file, because this drafter may not run git diff)
    4     0  src/cpus/cpu_m88k.c
   24     5  src/cpus/memory_rw.c
    7     3  src/devices/dev_luna88k.c
   25    25  src/devices/dev_m8820x.c
   31     0  regress/gate_arm.sh
   26     0  tools/pipeline/check_probe_wiring.py
  836     0  regress/m88k_buserr_probe.py   (untracked: new file)

## 7. every working-tree difference from HEAD, and the untracked files (wt_inventory.py: ls-tree + Python blob hashes)
HEAD tree blobs compared: 31975
working-tree files differing from HEAD: 25
  M  regress/artifacts/recordfix_20261002/chk_hrec.py.txt
  M  regress/diff_wdc_identify.c
  M  regress/gate_arm.sh
  M  regress/gate_offline.sh
  M  regress/gate_sh_rounding.sh
  M  regress/gdrom_default_probe.py
  M  regress/sh4_chcr_probe.py
  M  regress/wdc_addtoinbuf_probe.py
  M  src/cpus/cpu_alpha_palcode.c
  M  src/cpus/cpu_m88k.c
  M  src/cpus/memory_rw.c
  M  src/devices/dev_lca.c
  M  src/devices/dev_luna88k.c
  M  src/devices/dev_m8820x.c
  M  src/devices/dev_pcc2.c
  M  src/devices/dev_sh4.c
  M  src/include/thirdparty/mvme_pcctworeg.h
  M  tools/BRIEF_TEMPLATE.md
  M  tools/CLAUDE.md
  M  tools/PIPELINE.md
  M  tools/adjudicate.sh
  M  tools/panel.sh
  M  tools/pipeline/check_probe_wiring.py
  M  tools/pipeline/ledger.json
  M  tools/pipeline/matrix.html
HEAD paths absent from the working tree: 0
untracked (not ignored) files: 12212 total; 276 outside regress/artifacts/, 11936 inside
  ?  _scratchpad/CHECKPOINT.md
  ?  _scratchpad/README_THIS_IS_NOT_THE_SCRATCHPAD.md
  ?  _scratchpad/census.py
  ?  regress/alpha_dummy.bin
  ?  regress/arm_bfx_stub.bin
  ?  regress/lca_isaphys_probe.py
  ?  regress/m88k_buserr_probe.py
  ?  regress/sgi_mte_dummy.bin
  ?  tools/pipeline/check_fix_seats.py
  ?  tools/pipeline/check_probe_wiring.py.orig
  ?  tools/pipeline/ledger.json.before_nul546
  ?  tools/precommit_check.sh.orig
  ?  _scratchpad/agy_tbi_20260908/  (2 files; GXEMUL-SEC/_scratchpad panel/job directories, condensed per directory)
  ?  _scratchpad/fable_adj_20260902/  (1 files; GXEMUL-SEC/_scratchpad panel/job directories, condensed per directory)
  ?  _scratchpad/panel_20260831_033247/  (12 files; GXEMUL-SEC/_scratchpad panel/job directories, condensed per directory)
  ?  _scratchpad/panel_20260831_045142/  (6 files; GXEMUL-SEC/_scratchpad panel/job directories, condensed per directory)
  ?  _scratchpad/panel_20260831_053346/  (6 files; GXEMUL-SEC/_scratchpad panel/job directories, condensed per directory)
  ?  _scratchpad/panel_20260831_054552/  (12 files; GXEMUL-SEC/_scratchpad panel/job directories, condensed per directory)
  ?  _scratchpad/panel_20260831_060010/  (6 files; GXEMUL-SEC/_scratchpad panel/job directories, condensed per directory)
  ?  _scratchpad/panel_20260831_065643/  (12 files; GXEMUL-SEC/_scratchpad panel/job directories, condensed per directory)
  ?  _scratchpad/panel_20260831_075321/  (6 files; GXEMUL-SEC/_scratchpad panel/job directories, condensed per directory)
  ?  _scratchpad/panel_20260831_081810/  (12 files; GXEMUL-SEC/_scratchpad panel/job directories, condensed per directory)
  ?  _scratchpad/panel_20260831_093043/  (12 files; GXEMUL-SEC/_scratchpad panel/job directories, condensed per directory)
  ?  _scratchpad/panel_20260831_094355_texguard/  (6 files; GXEMUL-SEC/_scratchpad panel/job directories, condensed per directory)
  ?  _scratchpad/panel_20260831_102152_500p2/  (12 files; GXEMUL-SEC/_scratchpad panel/job directories, condensed per directory)
  ?  _scratchpad/panel_20260901_173956_500p3/  (12 files; GXEMUL-SEC/_scratchpad panel/job directories, condensed per directory)
  ?  _scratchpad/panel_20260901_183841_pcc2p1/  (12 files; GXEMUL-SEC/_scratchpad panel/job directories, condensed per directory)
  ?  _scratchpad/panel_20260901_192203_500p4/  (12 files; GXEMUL-SEC/_scratchpad panel/job directories, condensed per directory)
  ?  _scratchpad/panel_514p2_20260908/  (8 files; GXEMUL-SEC/_scratchpad panel/job directories, condensed per directory)
  ?  _scratchpad/panel_514p3_20260908/  (8 files; GXEMUL-SEC/_scratchpad panel/job directories, condensed per directory)
  ?  _scratchpad/panel_514p4_20260908/  (8 files; GXEMUL-SEC/_scratchpad panel/job directories, condensed per directory)
  ?  _scratchpad/panel_514p5_20260908/  (8 files; GXEMUL-SEC/_scratchpad panel/job directories, condensed per directory)
  ?  _scratchpad/panel_514p6_20260908/  (9 files; GXEMUL-SEC/_scratchpad panel/job directories, condensed per directory)
  ?  _scratchpad/panel_alphatbinegsel_20260908/  (10 files; GXEMUL-SEC/_scratchpad panel/job directories, condensed per directory)
  ?  _scratchpad/panel_bfi_20260908/  (8 files; GXEMUL-SEC/_scratchpad panel/job directories, condensed per directory)
  ?  _scratchpad/panel_lcabadval_20260908/  (6 files; GXEMUL-SEC/_scratchpad panel/job directories, condensed per directory)
  ?  _scratchpad/panel_sgirandomcolour_20260908/  (10 files; GXEMUL-SEC/_scratchpad panel/job directories, condensed per directory)
  ?  _scratchpad/panel_sgirekills_pass2_20260908/  (12 files; GXEMUL-SEC/_scratchpad panel/job directories, condensed per directory)
  ?  _scratchpad/panel_sgirekills_pass3_20260908/  (12 files; GXEMUL-SEC/_scratchpad panel/job directories, condensed per directory)
  ?  _scratchpad/panel_sgirekills_pass4_20260908/  (10 files; GXEMUL-SEC/_scratchpad panel/job directories, condensed per directory)
  ?  _scratchpad/panel_swpctx_20260908/  (6 files; GXEMUL-SEC/_scratchpad panel/job directories, condensed per directory)
  ?  _scratchpad/panel_tbi_20260908/  (8 files; GXEMUL-SEC/_scratchpad panel/job directories, condensed per directory)
  ?  regress/artifacts/agypack_20261001/  (9 files)
  ?  regress/artifacts/agypack_20261013/  (369 files)
  ?  regress/artifacts/allocsize_20260917/  (2 files)
  ?  regress/artifacts/alphaifetchkill/  (618 files)
  ?  regress/artifacts/alphavmkill/  (698 files)
  ?  regress/artifacts/armthumbabortkill/  (7 files)
  ?  regress/artifacts/asiceventaddr/  (6027 files)
  ?  regress/artifacts/astrafiling_20261002/  (18 files)
  ?  regress/artifacts/astraretro_20260926/  (89 files)
  ?  regress/artifacts/astraretro_harness_20260926/  (89 files)
  ?  regress/artifacts/b115/  (10 files)
  ?  regress/artifacts/b120/  (2 files)
  ?  regress/artifacts/batterymissedruns_20260925/  (482 files)
  ?  regress/artifacts/closeassess_20261002/  (13 files)
  ?  regress/artifacts/codex_research_20260913/  (22 files)
  ?  regress/artifacts/codexfarm_20260926/  (45 files)
  ?  regress/artifacts/codexpack_20260928/  (55 files)
  ?  regress/artifacts/cpusexitsweep/  (3 files)
  ?  regress/artifacts/cpusweep_20260917/  (2 files)
  ?  regress/artifacts/crimewidthkill/  (3 files)
  ?  regress/artifacts/cxultra_20260926/  (18 files)
  ?  regress/artifacts/fbclearread/  (8 files)
  ?  regress/artifacts/fbdisabled/  (2 files)
  ?  regress/artifacts/gdromdefault_461/  (3 files)
  ?  regress/artifacts/gdromdmadefault/  (38 files)
  ?  regress/artifacts/grokjobs_20260930/  (108 files)
  ?  regress/artifacts/haltclass/  (2 files)
  ?  regress/artifacts/heldqueue/  (1 files)
  ?  regress/artifacts/hlen/  (2 files)
  ?  regress/artifacts/idless_20261002/  (43 files)
  ?  regress/artifacts/idlessaudit_20261002/  (27 files)
  ?  regress/artifacts/idlessread_20261002/  (1 files)
  ?  regress/artifacts/landiskaux/  (2 files)
  ?  regress/artifacts/lcaconfwidth/  (1 files)
  ?  regress/artifacts/lcaisaphys/  (509 files)
  ?  regress/artifacts/lcaisasize/  (2 files)
  ?  regress/artifacts/lunadefaultstop_20260917/  (3 files)
  ?  regress/artifacts/m88kbuserrregs/  (233 files)
  ?  regress/artifacts/makercfalse/  (2 files)
  ?  regress/artifacts/multiaccesswarms/  (1 files)
  ?  regress/artifacts/n6/  (1 files)
  ?  regress/artifacts/neverqueued_20260917/  (2 files)
  ?  regress/artifacts/panelseatlabel/  (15 files)
  ?  regress/artifacts/ppcrlwhighhalf/  (6 files)
  ?  regress/artifacts/probedeathoracle_20260917/  (2 files)
  ?  regress/artifacts/probewiring/  (2 files)
  ?  regress/artifacts/recordfix_20261002/  (50 files)
  ?  regress/artifacts/recordfix_20261013/  (161 files)
  ?  regress/artifacts/recordsaudit_20260917/  (1 files)
  ?  regress/artifacts/seataudit_20260917/  (38 files)
  ?  regress/artifacts/sgirandomcolour/  (1 files)
  ?  regress/artifacts/sh4dmacie/  (16 files)
  ?  regress/artifacts/sh4rtcflags/  (2 files)
  ?  regress/artifacts/sh4sqwrite/  (2 files)
  ?  regress/artifacts/shprotld/  (2 files)
  ?  regress/artifacts/sighunt_20260917/  (3 files)
  ?  regress/artifacts/stateaudit_20260923/  (1172 files)
  ?  regress/artifacts/upstreamdeleteprose_20260924/  (1 files)
  ?  regress/artifacts/wdc473floor/  (854 files)
  ?  regress/artifacts/wdcaltdigin/  (8 files)
  ?  regress/artifacts/wdcerrfamily/  (4 files)
  ?  regress/artifacts/wdcnullxfer/  (11 files)
  ?  regress/artifacts/wdcrearmzero/  (9 files)
  ?  regress/artifacts/wiringcliff/  (2 files)
  ?  regress/artifacts/witnessspecset/  (2 files)
WT_INVENTORY_DONE

C0_DONE
~~~~
**VERDICT of C0:** the CHANGELOG names neither `m88kbuserrregs` nor `#570` at HEAD; no commit touches
`regress/m88k_buserr_probe.py` or `regress/artifacts/m88kbuserrregs/`; the ledger row at HEAD is `open`, witness
`none`, commits `''`, no stages.  **THE ROUND HAS NOT SHIPPED** -- this is a pass 2 on uncommitted work.

---

## 5. PREMISES ALREADY SETTLED, RE-INLINED SO NOBODY SPENDS AN ANSWER RE-DERIVING THEM

Settled by the pass-1 adjudication (`pass1_20261023/PASS1_RULINGS.md` section E: GPT-6 Astra, 2026-10-23, VERDICT AMEND,
four reviewing seats), the builder rulings (`BUILD_SPEC.md` sections 10-11) and section 3's measurements.  Source facts
were **re-read in this scope** (working tree, drafting time), with the line read.

**What pass 1 settled**
* **S1 -- the repair (A1-A7, as amended by E).**  A1 selector `cpu->cd.m88k.cmmu[cache == CACHE_INSTRUCTION ? 0 : 1]`.  A2
  PFSR = `CMMU_PFSR_BERROR << 16` = 0x00030000; PFAR = `(uint32_t) orig_paddr`, unmasked; PFAR's low two bits on silicon
  are UNKNOWN (no MC88200 manual on disk): a transferred warrant; a sub-word row is clause (e).  A3 the NULL check wraps
  the TWO WRITES ONLY; `m88k_exception`, the `!no_exceptions` guard, the `debug()` line and the failure return stay
  outside, unchanged; its licence is "transferred warrant" until the null rows MEASURE the delta (P9).  A4 nothing else
  in the arm moves.  A5 `case 0x3ffffff0:` -> `return 0;`, its PFSR write deleted, the case KEPT (without it the access
  reaches `default:`, which stops the cpu).  A6 the include in `cpu_m88k.c` after `m8820x_pte.h` -- placement upheld,
  the "order matters" rationale WITHDRAWN.  A7 exactly FOUR product files; `dev_m8820x.c` comment-only at four sites,
  without inventing an "only" its `memory_m88k.c:382-384` sentence never said.  The arm's TODO is replaced.
* **S2 -- what #570 may claim (A8).**  "Metadata for CLAIMED, REFUSED, unsuppressed device accesses that pass the
  running-transition check, plus LUNA's probe case routed into that path."  It must DISCLAIM: unclaimed addresses (R3);
  luna-88k's other device refusals (they stop the cpu before the arm); free-running instruction-fetch refusals (R1);
  NO_EXCEPTIONS callers; translation-fault semantics (unchanged); sub-word PFAR without a local warrant; CMMU-less
  machines (unchanged).  Never "every 88K bus error now carries PFSR and PFAR".  A9: the sibling CMMU is `kept`; never
  "no guest can observe the sibling"; the hardware latch semantics are UNKNOWN.
* **S3 -- the floor cells (B5, as amended by E).**  B5a the INSTRUCTION label is FLOOR; `ifetch route` is VACUOUS against
  the always-data selector (the vector expression, `memory_rw.c` :639-641, reads `cache` independently) and stays as an
  ATTRIBUTION row whose own variant is "exception dropped / mis-routed" (L17); `ifetch pfsr` / `ifetch pfar` carry the
  selector variant (L6).  B5b the `no_exceptions`-SET cell is FLOOR: one row, `dbg noexc`, observing preservation with no
  later fault (D3).  B5c the NULL-CMMU cell is FLOOR, AND the INSTRUCTION x NULL joint cell is OWED: {data, instruction}
  x {CMMU present, absent}, closed conjunctively by the two null rows; E (`PASS1_RULINGS.md` :233-234): "A survival
  control with a real channel discharges the floor obligation; the label does not change its evidentiary value."  (E's
  vector-2-then-R1 mechanism became the stepped SFRZ / ERROR form, S9 Q1-Q2.)  VA != PA, the LUNA store and sub-word
  PFAR (pass-1 premises P7, P10, P2 -- not this brief's P-numbers) are clause (e).  The joint cell licenses no
  cpu-number, address or device-name products.
* **S4 -- C5 WITHDRAWN.**  `static void m8820x_command(struct cpu *cpu, struct m8820x_data *d)` (`dev_m8820x.c` :106) is
  called only at :284, `m8820x_command(c, d);`, with `c = cpu->machine->cpus[d->cpu_nr]` (:250): the OWNING cpu
  (re-read).  Measured on HEAD (E3): a CMMU-less cpu 1 read both IDR windows (cpu 0's 0x00a90000) and stored an SCR
  command; exit 0, no fault.  The ban on cpu 1 touching the CMMU window goes with it.
* **S5 -- C4 CONDITIONAL.**  `dev_mvme187.c` attaches both CMMUs to `cpus[bootstrap_cpu]` (:137, :149) while
  `dev_m8820x.c` decodes `cpu_nr` 0; a mismatch exists only if the chosen bootstrap cpu is NONZERO, which the
  random-bootstrap option does not guarantee.  Source-derived, UNMEASURED; filed by name.
* **S6 -- R1, R2, R3 (C1-C3) upheld as filings.**  R1: a refused FREE-RUNNING instruction fetch takes vector 2, then the
  failed read in `to_be_translated` (`cpu_m88k_instr.c` :2989-2993, `goto bad;`) reaches the dyntrans `bad:` tail, which
  stops the faulting cpu before the handler runs.  R2: the single-step disassembly pre-read passes `CACHE_INSTRUCTION`
  WITHOUT `NO_EXCEPTIONS` (`cpu_dyntrans.c` :287-288, under `if (single_step || cpu->machine->instruction_trace)`) -- the
  channel of every stepped instruction cell here.  R3: an unclaimed address raises no bus error (`memory_rw.c` :681).
* **S7 -- D1-D5.**  D1 the NULL cell is reachable and admissible: a cpu-count option and a debugger command change
  configuration and execution state, not the machine description or dispatch (witness clause (iii));
  `debugger_cmds.c` :1302 is `m->cpus[cpuid]->running = !m->cpus[cpuid]->running;`.  D2 with R2 fixed, the stepped
  instruction rows go RED for an unrelated reason (R1's halt).  D3 `ok regs` (res = 1) cannot see a dropped
  `!no_exceptions`.  D4 an exit-1 stub was predicted 1/24 on the witness; an absent binary gives an uncaught
  `FileNotFoundError`, no sentinel.  D5 include placement upheld.
* **S8 -- literal N also needs (E, Q3):** each row identity once, an emitted-row census, zero failures, one CONTROL /
  SYMPTOM / completion record each; a RE-DERIVED disassembly census; prerequisites for every new session; disclosure
  that gate 14's earlier skips can stop the pins being reached.
* **S9 -- the builder rulings (`BUILD_SPEC.md` section 11, Q1-Q22).**  Q1 a STEPPED conjunctive null session (no
  `continue`, pty or breakpoint; cpu 1 set up by `focus 1`; part 1 `step 3` = the data refusal, part 2 `step 5` = the
  instruction refusal).  Q2 that refusal is delivered as ERROR, vector 10 (the data fault left PSR.SFRZ set; an `rte`
  would resume at SNIP and write a false FELL); `null surv` does not depend on the vector.  Q3 the debugger sets cpu 1's
  VBR.  Q4 cpu 0 runs its seeded `uld` path, unscored.  Q6 `dbg noexc` in its own session.  Q7 prerequisites are
  cause-free strings inside each row; N = 31.  Q8 `ifetch route` is not a CONTROL row.  Q9 unasm 192.  Q10 SYMPTOM has
  ten members.  Q12 the header names gate 14's eleven earlier skips.  Q13 L20 = L4, not run.  Q14 a leg passes when its
  measured red set equals the pre-table prediction (a mismatch is a RESULT); L18 = the NULL-checked writes moved just
  before the outer guard.  Q15 L8b = the NULL check conditioned on the data label.  Q16-Q18 add L6b (always the
  instruction CMMU), L16 excludes VME, add L22 (the LUNA case deleted).  Q19 frozen copies under artifacts are `*.py.txt`
  / `*.sh.txt`.  Q20 gates 14 and 11 once each on `build/gxemul`.  Q21 the boot A/B before the table.  Q22 compare
  `dev_m8820x.o` before and after.

**The source (re-read in the working tree)**
* **S10 -- `orig_paddr` is PHYSICAL and in scope:** `uint64_t orig_paddr = paddr;` (`memory_rw.c` :437) after
  translation; `paddr -= mem->devices[i].baseaddr;` (:494) makes `paddr` device-relative before the device call.
* **S11 -- the arm's path (1.4).**  The device is called only `if (!no_exceptions || (mem->devices[i].flags &
  DM_READS_HAVE_NO_SIDE_EFFECTS))` (:584-585); a device that stops the cpu returns at :591-592, before the arm;
  `if (res == 0) res = -1;` (:595-596); guard `if (res <= 0 && !no_exceptions) {` (:603); `debug()` with the
  DEVICE-RELATIVE `paddr` (:604-607); the #570 block (:615-638) in `#ifdef MEM_M88K` (:614-642), before `m88k_exception`
  (:639-641); `return MEMORY_ACCESS_FAILED;` (:643); served: `goto do_return_ok;` (:645).  Only a CLAIMED-and-REFUSED
  access reaches the arm; an unclaimed address gets zeros, no exception, no CMMU write (`Outside of physical RAM?`, :681).
* **S12 -- access classes.**  Data `ld`/`st`/`xmem`: `CACHE_DATA`; the fetch: `CACHE_INSTRUCTION` (`cpu_m88k_instr.c`
  :2989-2990); the debugger's `dump`: `CACHE_NONE | NO_EXCEPTIONS` on `cpus[bootstrap_cpu]` (`debugger_cmds.c` :716-717);
  the disassembler's look-behind: `CACHE_INSTRUCTION | NO_EXCEPTIONS`; the single-step pre-read: `CACHE_INSTRUCTION`
  WITHOUT `NO_EXCEPTIONS` (R2).  Non-debugger `NO_EXCEPTIONS` callers exist (`dev_luna88k.c` :613-614).
* **S13 -- cmmu[0] = instruction, cmmu[1] = data** (`memory_m88k.c` :112).
* **S14 -- which cpus have CMMUs.**  MVME187: both on `cpus[bootstrap_cpu]` (`dev_mvme187.c` :136-149); under `-n 2`
  cpu 1 has none, and `pause 1` starts it.  luna-88k: both on every cpu below `ncpus`.  A NULL CMMU translates
  physical = virtual (`memory_m88k.c` :130).  E2 measured on HEAD: no "cpu1: CMMU" line in `tlbdump 1`; cpu 1 runs.
* **S15 -- exception delivery** (`cpu_m88k.c`, anchor `void m88k_exception(struct cpu *cpu, int vector, int is_trap)`,
  :693; HEAD :689): a non-trap exception while PSR.SFRZ is set becomes ERROR (:815; HEAD :811); SXIP = pc | V, plus E
  for an instruction access (:864); DMA0 zeroed (:877) and copied on DATA_ACCESS only (:916); pc = VBR + 8 x vector.
* **S16 -- the include.**  `memory_rw.c` compiles INSIDE `cpu_m88k.c`'s unit (`tmp_m88k_tail.c` :38-40: `#define
  MEMORY_RW m88k_memory_rw` / `#define MEM_M88K` / `#include "memory_rw.c"`; `cpu_m88k.c` :1689 includes the tail).
  `CMMU_PFSR`, `CMMU_PFAR`, `CMMU_PFSR_BERROR` are defined ONLY in `src/include/thirdparty/m8820x.h` (:65, :66, :125).
  **Upstream's trunk adds the include to `cpu_m88k.c` BEFORE `m8820x_pte.h`** (`trunk_src.diff` :1921-1922; 1.4).
  `NBSG` (:182) is used nowhere in `src/`; the header's struct/extern block is under `#if 0` (:190-212).  Drafter's
  collision check: of the 103 macros `m8820x.h` defines, only those three appear in any file of `cpu_m88k.c`'s unit
  (`src/include/*.h`, `m8820x_pte.h`, `m88k_dmt.h`, `mvmeprom.h`, `cpu_m88k*.c`, `tmp_m88k_*.c`, `memory_rw.c`,
  `cpu_dyntrans.c`).  The fixed build: 0 warnings under `-Wall -Wextra -Wshadow`.
* **S17 -- the LUNA case path** (1.4).  `uint32_t addr = relative_addr + LUNA88K_REGISTERS_BASE;` (`dev_luna88k.c`
  :558; base 0x3ffffff0); the early windows (:567-620) all start above 0x3ffffff0; `switch (addr)` :622; the case :624
  -> `return 0;` :631; `default:` (:913-928) logs at ERROR level, sets `cpu->running = 0;`, returns 0; the common tail
  (:931-934) writes the read buffer `memory_rw` already zeroed (`memory_rw.c` :491-492).  HEAD's body was
  `cpu->cd.m88k.cmmu[1]->reg[CMMU_PFSR] = CMMU_PFSR_BERROR << 16; break;`; both defect sites date from the 0.7.0 import
  (`git show 39748e3c:` re-read).
* **S18 -- shared files:** the four product files are not in `tools/est_divergence.txt` and are byte-identical in `est/`.
* **S19 -- the guest reader and the manual.**  OpenBSD 2.2 mvme88k recovers a guarded kernel bus error only when
  `(frame->dpfsr >> 16 & 0x7) == 0x3` (`C:\DocumentNoSnc\cc\GXEMUL\_guest-src-openbsd22\sys\arch\mvme88k\mvme88k\trap.c`
  :326, re-read).  The luna rig boots OpenBSD/luna88k, whose source is NOT on disk; the MC88200 manual is NOT on disk.

**The measurements (section 3)**
* **S20 -- the scores** (3.4), against the frozen instruments (detector rev 2, md5 `d57c12ab`, N = 31; witness rev 1, md5
  `d59798b0`, N = 24): **27 measurements** (pre, fix, L1, L3, L3/w24, L4, L4/w24, L5, L5b, L6, L6b, L7, L8, L8b, L9, L10,
  L11, L12, L13, L14, L15, L16, L17, L18, L19, L21, L22), each recorded as matching its pre-table prediction; **20
  variant builds**, each red on the 31-row detector; L20 = L4, not run.
* **S21 -- the build.**  221 of 224 outputs (223 objects + the binary) byte-identical to the unmodified build; changed:
  `gxemul`, `cpu_m88k.o`, `dev_luna88k.o`.  `dev_m8820x.o` is identical AND was recompiled: "comment-only" is measured.
* **S22 -- the two-part clearance** (01:36): `est/` CLEAN, part 2 N/A (source tree); `build/`, `build-asan/`,
  `/tmp/gxsec-build`, the work clone: CLEAN and FRESH; no sentinel.
* **S23 -- the gates.**  Gate 14 PASS, 1310 checks, 0 FAIL, wall 7974 s, once, alone, a harness-tracked background job
  (departure 4), on `build/gxemul`; the `#570` block's 40 checks green; the `#568` pin 38/38.  Gate 11 PASS, 111 checks.
  `grep 3ffffff0` over `regress/*.py` / `*.sh`: no committed hit at HEAD.
* **S24 -- the boot A/B** (3.7): luna rig image, `gate_ab.sh`'s `luna_run` shape (budget 12e9 instructions, stall 120 s,
  backstop 1800 s, marker `login:`): BASE `2efeec55` reason=MARKER after 7,651,336,103 instructions / 125 s; FIXED
  `3cd0501c` reason=MARKER after 7,550,665,157 / 120 s; markers 1:1:1 both; consoles differ only cosmetically (temp
  name, spinner wrap, a line break, the date).
* **S25 -- section C0: not shipped** (section 4).  **S26 -- gate 6 was not run;** the probe carries none of its census
  tokens (`endswith(`, pty-driving imports): grep counts 0 and 0.

---

## 6. PREMISES STATED AS QUESTIONS -- the drafter's doubts; check these, ratification is not wanted

* **P1 -- "(the debugger)" in the new `memory_rw.c` comment.**  "NO_EXCEPTIONS callers (the debugger) never get here: the
  test above keeps them out" is true of every `NO_EXCEPTIONS` caller (S11).  But the parenthetical reads as an identity,
  and one debugger-driven access is NOT `NO_EXCEPTIONS` and DOES get here -- the single-step pre-read (R2), the channel
  of this round's stepped `ifetch` rows and of the null session's part 2; and some `NO_EXCEPTIONS` callers are not the
  debugger (S12).  Harmless shorthand, TRUE-BUT-MISLEADING, or an L4 owed before commit?
* **P2 -- this diff moves lines an edited file cites.**  The +4 include shifts every later line of `cpu_m88k.c`.
  `dev_m8820x.c` :361 -- in a file this diff edits to correct citations -- cites `(cpu_m88k.c:354-355)`, at HEAD the
  `for (cmmu_nr = 0; ...)` loop over `cpu->cd.m88k.cmmu[cmmu_nr]`, now :358-359.  Five tracked regress files cite
  `cpu_m88k.c` lines numbered after 53: `diff_m8820x.c` :996 (`:362-375`), `diff_m8invread.c` :161 (`:121-122`),
  `luna_intmask_probe.py` :23 and `m8820x_sites_probe.py` :27 (both `:991-1019`), `readiness_predicate_test.py` :70
  (`:277`).  Is the `dev_m8820x.c` one an L4 this diff owes (R18), and the five filed rather than swept?
* **P3 -- the PROBE HEADER says "after m8820x_pte.h (upstream's placement, the transferred warrant)"** (header line 33).
  Upstream puts it BEFORE (S16); the product comment says only "upstream adds the same include to this file" (true).  Is
  the header sentence an L4 owed before commit -- and, the header being part of the frozen instrument (md5 `d57c12ab`)
  that the gate log and the MANIFEST line identify, does fixing it owe a re-freeze or a records note?  And is "upstream
  adds the same include" a SUFFICIENT warrant, the position not being load-bearing (S16)?
* **P4 -- a count over a set it was not measured on.**  `dev_m8820x.c` :325-333 now folds "#570: and memory_rw.c's arm"
  into the fault-path writers that write "DIRECTLY through reg[], with no purge, ~10^5 times per boot -- against 2 guest
  writes per boot".  The ~10^5 described the translation-fault writer; nothing counts the arm's writes.  Still true, or a
  frozen number restated over a new set?
* **P5 -- L22's prediction is not where the table says.**  `SCORES.txt`'s criterion names "PRETABLE section 5's predicted
  set as amended (AMENDMENT 1)"; L22 is in neither -- its prediction is BUILDER_QUESTIONS Q18 (22:29:30) and BUILD_SPEC
  section 11 Q18 (22:31:49), both before the leg (23:08).  PRETABLE section 2 still says "No leg in the table builds 'case
  deleted'" although its header requires an amendment for a design-changing ruling.  A records correction owed, and
  where?  Does it touch the MANIFEST line's "27 of 27 measurements as predicted"?
* **P6 -- the LUNA instruction-fetch cell.**  HEAD's case wrote cmmu[1]'s PFSR for ANY access class (A5's note); PRETABLE
  1.B(3) and CL13 route the instruction-fetch cell to "no row ... one CHANGELOG sentence".  The probe's NOT CLAIMED list
  names the LUNA STORE and free-running instruction fetches, not a stepped instruction fetch AT 0x3ffffff0.  A clause-(e)
  gap, or covered by an existing line?
* **P7 -- what the boot A/B shows.**  Both boots reach `login:` (S24).  The instruction counts differ by 100,670,946
  (1.3 %) with no base-against-base control, and neither log shows whether the boot touched 0x3ffffff0 (3.7).  May the
  records claim more than "no regression to login:"?
* **P8 -- clause (a) at the GATE.**  The block was inserted after propagation (departure 3), so the gate never ran it on a
  pre-fix binary; the probe-level pre-fix receipt (21/31) exists, and the literal pins (`rows correct` == 31,
  `SYMPTOM=ABSENT` x1) would red on it.  Is "by construction via those pins, leg not run" the right record -- and is that
  form available for clause (a) at all (R2 defines it for (c))?
* **P9 -- A3's licence.**  E kept the NULL check at "transferred warrant until the null rows measure the delta".  L8 (the
  check removed) measured it: `null surv` and `null route` read `died:sig11` (`L8_nullrm.out`).  Does the record now say
  "licensed by a measured delta (L8; L8b for the instruction label)"?
* **P10 -- an unmeasured prediction worded as fact.**  The header says that with R2 fixed "the step's own fetch reaches the
  same arm, so the NULL-check observable survives and only the after-fault flow changes (R1's halt)".  The Q1 ruling asked
  for this disclosure; nothing measured it.  Should it say "predicted (source-derived)"?
* **P11 -- `SCORES.txt` truncates SYMPTOM at 60 characters** (3.4): hygiene, or a durable record misstating itself?
* **P12 -- `table1_20261023/staged/gate_arm.sh` keeps a `.sh` suffix** where Q19 named `*.sh.txt`; inert for
  `check_probe_wiring.py` (`.py` only) and `run.sh` (its GATES array) -- but should a 144 KB copy of a live gate be
  committed at all, and under which name?
* **P13 -- "DATED PREDICTIONS ... UNTIL THE TABLE RUNS"** is still in the header after every prediction matched.  Keep it
  (byte-identity with the frozen instrument), or is it stale?
* **P14 -- the gate comment.**  "A REFUSED m88k device access -- a device CLAIMS it and returns 0 with the cpu still
  running -- now records its bus error in the faulting side's CMMU" omits A8's "unsuppressed" and the CMMU-less case.
  Acceptable summary, or overclaim?
* **P15 -- no scored row observes exception DELIVERY in the instruction x NULL cell.**  E closed that cell with a
  survival control and said so (S3).  The product comment says more -- "A cpu without a CMMU gets no write and still
  takes the exception" (`memory_rw.c` :623-625) -- and PRETABLE maps "still takes the exception" to `null route` alone
  (CL7, `PRETABLE.out` :99), which reads part 1 only (the DATA refusal).  `null surv` reads survival plus three
  prerequisites -- cpu 1 at J after part 1, cpu 1 OFF J after part 2, a `failed ]` line after part 1's dump -- and its
  want, "exit0/readable", does not depend on where cpu 1 is delivered (S9 Q2).  Where cpu 1 ends is printed only by
  the UNSCORED `INFO null cpu0` line: `cpu1 end pc=0x30050` (VBR1 + 0x50, ERROR) on the fixed build and on HEAD, but
  `cpu1 end pc=0xfff46010` (no exception taken) under L9 and L17 -- where `null surv` stays GREEN and only `null route`
  reds (3.3).  The data x NULL cell has a survival row AND a route row; the instruction x NULL cell has survival only.
  For the instruction label, does that sentence owe a row or an explicit no-row sentence (the PRE-TABLE CHECK's
  CLAIM -> ROW: "every ADDED comment sentence asserting an OBSERVABLE CONSEQUENCE owes a row or an explicit no-row
  sentence"), or does E's survival ruling cover it (R6, R7)?

---

## 7. The project rules the questions apply -- quoted with their bounds

*Quoted from the WORKING-TREE carrier `GXEMUL-SEC/tools/CLAUDE.md` (byte-identical to the root `CLAUDE.md`; 4104
lines; HEAD's copy has 3846 and lacks the 2026-10-09 clause-(c) block and rule D2).  Line numbers are that file's.*

**R1 -- THE FLOOR:**
~~~~
 1328| > **THE FLOOR.** A detector is VACUOUS — replace it IN-ROUND — unless it (a) fails on the
 1329| > pre-fix build, (b) fails on a **VERBATIM REINSTATEMENT of the removed defect at EVERY fixed
 1330| > site**, and (c) fails on a **NULL MEDIUM** -- a product medium carrying none of the behaviour under
 1331| > test (the clause-(c) block below says what that is per instrument kind). Below the floor, the
 1332| > round's own claim to have "shipped a detector with the fix" is a WRONG RECORD, which the
 1333| > stopping rule already fixes in-round.
~~~~
**R2 -- clause (c): the null medium, the pre-fix build, the two record forms, and when a claimed clause is L4:**
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
 1350| > **THE PRE-FIX BUILD IS CLAUSE (a)'S MEDIUM AND NEVER CLAUSE (c)'S.**  It carries every behaviour of the
 1351| > product, one of them wrong, so a detector can red on it and still pass a comment-only file -- `#446`,
 1352| > the instance that created this clause.  A table that wrote "null medium" over a pre-fix leg carries a
 1353| > WRONG RECORD (L4: correct it in place, quoting what it refutes, as
 1354| > `ppcrldimimask/killtable_20260911/SCORES.txt` does), NOT a floor breach: clause (c) is then
 1355| > UNMEASURED there.  **A breach is a genuine null medium coming back GREEN, and nothing else** -- "a
 1356| > sharper medium was available" is not a floor criterion (at most clause-(e) debt).
 1357| >
 1358| > **RECORD CLAUSE (c) IN ONE OF EXACTLY TWO FORMS, never as a bare clause letter beside a row name:**
 1359| > * `(c): measured at <artifact>` -- the leg was run and its receipt is durable;
 1360| > * `(c): by construction via <row/pin>, leg not run` -- e.g. the gate pins the row count by EQUALITY
 1361| >   and a named row reds on a dead run, or the differential `#include`s the product and its gate reds
 1362| >   on a compile failure.  **A by-construction claim is checked by READING that shape; where the reading
 1363| >   fails -- no runtime gate wiring, no pin, `check_min`, a control computed over the row list
 1364| >   (`all([])` is True) -- the leg is OWED** (7n-1's two: the unwired `ppc_rldicl_probe.py` and
 1365| >   `alpha_tbi_probe.py`).  Predict a dead run's score from the source, not from the row count (Astra
 1366| >   measured luna's at 0/14 with four gate checks red, and SGI's at 6/46 because six rows test only
 1367| >   exit status).
 1368| >
 1369| > **A claimed-but-unmeasured floor clause is L4 exactly when the record asserts a MEASUREMENT or a
 1370| > NUMBER that was not made** (`#488`'s "pinned at 90": no preserved 90-row output exists, and the
 1371| > differential pins 98).  The E1 `[IDENTITY]` self-count row is detector hygiene, NOT clause (c).
~~~~
**R3 -- clause (d), and R4 -- its two shapes:**
~~~~
 1376| > **(d) The detector must also fail when the fix is PRESENT but its REPAIR IS NULLED —
 1377| > the guard kept, its effect removed.**
 1428| > **The two shapes, once the enumeration is right:**
 1429| > * **fix ADDS a predicate** -> weaken the added one (unchanged; the original rule).
 1430| > * **fix adds none** -> the (d) mutant reroutes an EXISTING guard's repair. For a
 1431| >   de-fatalisation: **swap the guard's operand for a field the guarded BODY reads.**
 1432| >   For a pure deletion: **re-introduce the removed behaviour under a DIFFERENT predicate**
 1433| >   -- not the same one widened, which is (b) wearing (d)'s clothes.
~~~~
**R5 -- the DEPENDS-ON bound:**
~~~~
 1448| > > **DEPENDS ON enumerates exactly two things: (1) the predicates DOMINATING the diff's
 1449| > > edited lines, walked up only to the ENCLOSING FUNCTION BOUNDARY -- never into callees
 1450| > > or callers; and (2) for operand-swap forms, swaps drawn ONLY from fields the guarded
 1451| > > BODY reads (the guard-field/body-field grep the pre-table check already mandates).**
~~~~
**R6 -- joint cells: the body-tested partition:**
~~~~
 1464| > > **DEPENDS-ON enumerates JOINT cells over the guard's operands and the body-read lvalues EXACTLY
 1465| > > WHEN THE GUARDED BODY'S OWN CODE DISTINGUISHES THEM.**  For each lvalue take the PARTITION the
 1466| > > body's own tests induce (`pending > 0` gives {0, >0}; `relative_addr == PCCTWO_T1ICR` gives
 1467| > > {T1, T2}); the enumerated cells are the CROSS-PRODUCT of those partitions -- never arbitrary
 1468| > > boolean functions of the read-set.  A mutant exempting a single cell whose reachability is
 1469| > > MEASURED is a floor breach; close the whole cross-product in ONE diff and write into the
 1470| > > contract which cells are rowed.  A value or combination the body never tests as a case
 1471| > > (`idata == k`; a byte no conditional distinguishes; both counts >= 2 where the body tests `> 0`)
 1472| > > is DISCLOSED under clause (e).
~~~~
**R7 -- the floor (cells a row is OWED for) versus clause-(e) disclosure:**
~~~~
 1517| > > **The rule ENUMERATES joint cells wherever the body distinguishes them; the FLOOR -- the cells a row
 1518| > > is OWED for -- is the cross-product of the guard's dominating predicates with the device-STATE lvalues
 1519| > > the fix's own repair path reads that are JOINTLY REACHABLE through its own data flow.**  The bits of
 1520| > > the single value being written are single-operand MARGINALS, not floor; joint cells outside the floor
 1521| > > are clause-(e) coverage debt, subject to the one ask-again.  A filter may reject or discharge a cell
 1522| > > but may demand a new row only for a floor cell -- so it cannot grow unbounded.
~~~~
**R8 -- rule D2: a relational compare is pinned at its edges:**
~~~~
 1557| > > For a relational compare against a constant bound B that a fix DEPENDS ON (`X > B`, `e < 96`), each region of its
 1558| > > generating set is discharged by the row that varies under the LEAST-OBSERVABLE non-equivalent move of B: **X = B+1
 1559| > > for the region past the bound and X = B-1 for the region below it** (the "at" member is dead where the branch maps B
 1560| > > to itself).  **A far row proves the branch EXISTS and discharges the BRANCH partition; it never pins the BOUND.**
 1561| > > Measured on `#473`'s shipped WDC detector: its rows at 68928 and 4998 let `> 32769` and `> 32766` at each clamp --
 1562| > > one-token bound moves -- pass all 128 rows, while rows at 32769 and 32767 red each one
 1563| > > (`regress/artifacts/wdc473floor/pass1_20261009/fable5_meas/`).  **Bound: at most two rows per compare the fix
 1564| > > depends on -- the compare's own two edges.**  It adds no axis; it moves the rows a region already owes to where the
 1565| > > bound is observable, so it cannot become `#392`.  It is the accept-row finding -- *a single accept row pins exactly
 1566| > > ONE bound, the one it is near* -- stated for compares.
~~~~
**R9 -- GUARD FIELD vs BODY FIELD, and the CHANNEL line:**
~~~~
 1740| > | **GUARD FIELD vs BODY FIELD** | list fields the PREDICATE reads and fields the guarded BODY reads; where they differ, grep whether they are written at the same sites. If not, the detector owes a state where they DISAGREE.  **Also record, per lvalue, the PARTITION THE BODY INDUCES on it** (its tested masks and compare regions) -- EXHAUSTED / SAMPLED is read off this column, never asserted (7n-5, 2026-10-09) | the guard's operand swapped for a field whose third state no row built |
 1741| > | **CHANNEL** | for each row, name **the mutant it kills** and **the observable that differs under that mutant**. A row whose named channel cannot vary under its named mutant is VACUOUS BY CONSTRUCTION, and that is knowable at writing time, before any table runs | a survival oracle at a REFUSAL-EFFECT site: guarded and unguarded code both survive |
~~~~
**R10 -- a filter cannot demand a row, and R10b -- clause (e), the contract:**
~~~~
 1783| > > **A FILTER CAN REJECT OR REPAIR A ROW; IT CAN NEVER DEMAND A NEW ONE -- SO IT CANNOT GROW
 1784| > > WITHOUT BOUND.**  That is the stop condition, and it is structural rather than a cap: the
 1801| > **(e) THE CONTRACT.** The probe header names which edits this detector is designed
 1802| > to catch. *A detector that says so is falsifiable; one claiming completeness is
 1803| > not* -- and a later escape becomes "outside the contract" or "a breach of it",
 1804| > which are different dispositions, rather than an argument about overclaiming.
 1805| > Two lines in a header.
~~~~
**R11 -- the anchor rule and its reviewer check:**
~~~~
 1814| > **Rows that assert only PAIRWISE DISTINCTNESS, or a same-path round-trip, test the decode
 1815| > against ITSELF.** They are therefore invariant under any edit that re-maps addresses
 1816| > INJECTIVELY over the probed set -- translations first among them -- and they catch a re-map
 1817| > only where it COLLIDES on that set.
 1888| > **A DETECTOR CLAIMING TO PIN *WHERE* AN ACCESS LANDS MUST CARRY AT LEAST ONE ANCHORED ROW:
 1889| > > an oracle tied to a SPECIFIC CELL by a channel OUTSIDE the decode under test** -- a side
 1890| > > effect (a tick that zeroes the cell), an architectural reset value, or a second access path
 1891| > > to the same cell. **One anchored row converts a whole distinctness suite from relative to
 1892| > > absolute.**
 1893| >
 1894| > **THE REVIEWER CHECK, and it costs two seconds** -- it belongs beside *"does this diff delete
 1895| > `exit(` from a device? then look for accept rows"*:
 1896| >
 1897| > > ***"If every address in this device shifted one word, which row reds?"*** If the answer is
 1898| > > NONE, position is unpinned, whatever the row count.
~~~~
**R13 -- the addition licence:**
~~~~
 2334| > > **Additions to product code in a hardening fork are licensed by MEASURED DELTAS or by a
 2335| > > TRANSFERRED WARRANT -- never by "it cannot hurt."**
~~~~
**R14 -- the witness clauses:**
~~~~
 2788| **A rung-2–4 witness is INVALID unless all of:** (i) it shows the defect symptom on the pre-fix
 2789| committed HEAD and goes green post-fix with the same script — this is test-first itself, restated
 2790| per-probe; (ii) **for ACCESS witnesses (rungs 3–4)** it carries a LIVENESS control (a known value
 2791| returns through the same decode) AND a DEVICE-SIGNATURE control (the observed value could only
 2792| have come from the device — RAM would answer differently; **the footbridge probe's first draft
 2793| returned 0x0 everywhere WITH ITS RAM CONTROL GREEN**, so one control is not enough); (iii) the
 2794| machine description and dispatch are committed and unmodified — a machine or `device_add`
 2795| introduced IN ORDER TO reach the site is
 2796| laundering, not witnessing.
~~~~
**R15 -- the ask-again cap, and that it counts ASKS, not findings:**
~~~~
 2471| > **CAPPED AT ONE ASK-AGAIN PER DETECTOR PER ROUND.** This is not the #392 chain — #392 was
 2472| > unbounded fix-of-fix passes with no stop condition; this is a single extra adversarial query
 2473| > against a clean table with a measured stop: nothing found, done; something found, row added
 2474| > under L1, done. **The cap IS the anti-#392 clause.** A second ask-again after an empty first
 2475| > is exactly where the chain starts, and anything found past the cap is FILED, never fixed.
 2481| > > Everything ONE ask returns is disposed of INDIVIDUALLY under L1–L4 and the floor — and **a
 2482| > > floor breach among the findings is L2, repaired in-round however late it is found.** A
 2483| > > second ASK is where the #392 chain starts; the number of rows one ask yields is not.
~~~~
**R16 -- the four licences for an in-round fix of detector material:**
~~~~
 2606| > ### THE FOUR REASONS THAT LICENSE AN IN-ROUND FIX OF DETECTOR MATERIAL
 2607| >
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
**R17 -- a closing pass must be a valid pass:**
~~~~
 2670| > > **A closing pass must be a VALID pass: the diff actually delivered; the roster complete or
 2671| > > its misses named per the seat ledger; and the zero carried WITH ITS DENOMINATOR -- which
 2672| > > cells, which mutant shapes, were swept.** *"Zero found"* and *"zero looked for"* must not
 2673| > > render the same, which is this project's oldest rule about blanks turned on its own stop
 2674| > > condition.
~~~~
**R18 -- a line number in a comment is invalidated by your own edits:**
~~~~
 3786| **A LINE NUMBER IN A COMMENT IS INVALIDATED BY YOUR OWN EDITS TO THAT FILE.** The same
 3787| round cited `dev_sh4.c:2379-2381` correctly, then inserted a seven-line comment ABOVE it
 3788| in a later step, moving the target to `:2386-2388` and making its own fresh citation
 3789| wrong. **Re-grep every same-file citation AFTER the last edit to that file**, not when
 3790| first written.
~~~~
**R19 -- a score claim names its artifact; a count names its deriver:**
~~~~
 3707| > **THE RULE: a score claim names its artifact — `8/32 pre-fix (kill461e.out)`.**
 3622| > **A COUNT WRITTEN INTO A DURABLE RECORD NAMES ITS DERIVER** -- the command, script, manifest
 3623| > or log that produces it -- **or carries its method and date inline. And a count being
 3624| > CORRECTED may never land as a fresh bare literal: it lands as deriver-plus-demoted-prose.**
~~~~
*Not binding here, said so that nobody spends an answer on it: the de-escalation clause and accept-row failability
bind a diff that DELETES an `exit(` -- this diff deletes none.*

---

## 8. QUESTIONS -- VERDICT LINE FIRST (format in section 0)

**Q1 -- THE DIFF AGAINST THE RULINGS.**

(a) **Hunk by hunk against A1-A7 as amended by E (S1).**  `memory_rw.c`: exactly A1 + A2 (the `(uint32_t)` cast kept) +
A3 (the NULL check around the two writes ONLY; exception, guard, `debug()` and return untouched) + A4, with the TODO
replaced?  `dev_luna88k.c`: A5?  `cpu_m88k.c`: A6 (after `m8820x_pte.h`, no "order matters" text)?  `dev_m8820x.c`: A7
(comment-only at four sites, no invented "only", object identical -- S21; one wording change for the line budget,
"dropping the handler's store" -> "dropping its store", departure 6)?

(b) **The include (departure 1).**  BUILD_SPEC section 10 gave "upstream's placement" as the reason for the position;
upstream places it BEFORE (S16).  Is the comment's "upstream adds the same include to this file" TRUE, and SUFFICIENT as
the include's warrant?  And P3.

(c) **Every sentence the new comments assert -- TRUE, FALSE or TRUE-BUT-INCOMPLETE?**  Cite the line you read for each.
`memory_rw.c` -- [M1] "record the bus error in the faulting side's CMMU first"; [M2] "PFSR = BERROR << 16 (the field
OpenBSD/mvme88k's trap.c extracts)"; [M3] "PFAR = orig_paddr, the PHYSICAL address saved before paddr was made
device-relative"; [M4] "cmmu[0] is the instruction CMMU, cmmu[1] the data CMMU (memory_m88k.c's index)"; [M5] "the other
CMMU is not written"; [M6] "A cpu without a CMMU gets no write and still takes the exception"; [M7] "NO_EXCEPTIONS
callers (the debugger) never get here: the test above keeps them out" (P1).
`cpu_m88k.c` -- [C1] "... uses CMMU_PFSR, CMMU_PFAR and CMMU_PFSR_BERROR, which are defined only in m8820x.h"; [C2]
"upstream adds the same include to this file".
`dev_luna88k.c` -- [L1] "Accessed by OpenBSD/luna88k to trigger an illegal address" (kept from HEAD; no OpenBSD/luna88k
source on disk); [L2] "memory_rw.c's refused-device arm then raises the access exception and writes PFSR and PFAR (for a
load or store, in the data CMMU)"; [L3] "this case used to write cmmu[1]'s PFSR only and serve 0"; [L4] "The case is
kept: without it the access would reach default:, which stops the cpu" (measured by L22).
`dev_m8820x.c` -- [D1] :293-295 "the model writes only PFSR and PFAR (memory_m88k.c:382-405 and, since #570,
memory_rw.c's refused-device arm)"; [D2] :325-333, the writer list with "~10^5 times per boot" (P4); [D3] :451-455 "(and,
since #570, in memory_rw.c's refused-device arm), never through this handler"; [D4] :498-502 "PFSR and PFAR written at
:382-405 and, since #570, in memory_rw.c's refused-device arm -- is a HANDLED case label above".

(d) **Does the diff make an EXISTING record false?**  P2.

(e) **Return paths.**  The LUNA case's `return 0` skips the common tail (S17): inert for a failing access?  (f) **Any L4
wrong record in the diff?**  Name, grade, and say whether it must be fixed before the commit.

**Q2 -- THE DETECTOR AND ITS FLOOR.**

(a) **Clause (a).**  Pre-fix 21/31, SYMPTOM=PRESENT 10/10, exactly the ten predicted reds; post-fix 31/31 ABSENT; the
frozen witness 24/24 post-fix (L1) after 16/24 pre-fix.  Anything owed beyond these?  And P8.

(b) **Clause (b), both sites, both instruments.**  L3 (`memory_rw.c` = HEAD blob `3d47dd66`, LUNA case fixed): 21/31 and
16/24.  L4 (`dev_luna88k.c` = HEAD blob `6ecc6908`, arm fixed): 29/31 and 22/24.  Red for the reason under test?  (L3
keeps `luna route` green: the refused case still enters the unrepaired arm, which still raises the exception.  L4 keeps
`luna pfsr` green: the case's own PFSR write is back.)

(c) **Clause (c).**  L5 (an exit-1 non-emulator): 1/31, only `neg apparatus` green by design, CONTROL=FAIL, sentinel
printed.  L5b (no binary): `FileNotFoundError`, no row, no sentinel -- the gate's `probe completed` check reds.  Recorded
as "(c): measured at table1_20261023/L5_stub.out and L5b_absent.out".  The right form (R2)?  Anything owed beyond it?

(d) **Clause (d) and the joint cell (S3).**  Measured: L6 (selector always-data) reds the three `ifetch` metadata rows;
L6b (always-instruction) reds the twelve data-label pfsr / pfar / icmmu rows; L7 (`!no_exceptions` dropped) reds `dbg
noexc`; L8 (NULL check removed) reds both null rows; L8b (NULL check conditioned on the data label) reds `null surv`; L9
(exception moved inside the NULL check) reds `null route`.  Carriers (PRETABLE AM-2): data x present -- `uld` / `ust` /
`vme` / `luna` pfsr, pfar, icmmu; instruction x present -- `ifetch pfsr`, `ifetch pfar`, `ifetch dcmmu`; data x absent --
`null route` (and `null surv` via part 1); instruction x absent -- `null surv` (part 2; survival only, P15).  Is every
floor cell rowed by a row whose CHANNEL can vary under that cell's variants?  Name any floor cell, or any observable of
one, still UNROWED.  Candidates from the records with their dispositions: the LUNA store, sub-word PFAR, VA != PA
(clause (e), S3); luna-88k `-n 2..4` (NOT CLAIMED); a stepped instruction fetch AT the LUNA address (P6); delivery in
the instruction x NULL cell (P15).

(e) **CHANNEL against the measured red sets (2.3; PRETABLE section 4, AM-5).**  Is any row VACUOUS by construction beyond
`ifetch route` against L6 (disclosed; its own variant is L17)?  Is any leg RED FOR THE WRONG REASON -- in particular L18
(writes moved before the guard: 25 red, CONTROL=FAIL) and L19 (guard widened to `res <= 1`: 27 red, CONTROL=FAIL), where
`ok route` / `ok regs` red only through prerequisite strings because the probe's own served CMMU accesses are overwritten
or fault first (PRETABLE section 4, CHANNEL CHECK)?  The only channel those two rows have, or a missing row?

(f) **A BREACH the records do not grade as one?**  They grade none (27 of 27 as predicted, all 20 variant builds red).
Scrutinise the single-row carriers (2.3).

(g) **The R2 dependency and the ERROR vector -- disclosed correctly?**  The four `ifetch` rows (`ifetch pfsr` / `ifetch
pfar` being the B5a selector carriers and SYMPTOM members) and the null session's part 2 reach the arm ONLY through the
single-step pre-read (R2).  With R2 fixed the `ifetch` rows red for an unrelated reason and are re-rooted (D2); the
header says `null surv`'s observable SURVIVES an R2 fix (P10).  cpu 1's instruction refusal is delivered as ERROR, vector
10, the data fault having left PSR.SFRZ set (S9 Q2, S15); the arm and its NULL test run first either way -- and no scored
row observes the delivery (P15).  True and sufficient, in the header and for the records?

(h) **The gate-14 block (1.2) and the MANIFEST lines (1.3).**  Row identities held in the gate (31 names, each
`count "$LOG" "^$v  .*ok$"` == 1); `rows run` / `rows correct` == 31 by literal equality; sentinel once; `CONTROL=OK` x1;
`SYMPTOM=ABSENT` x1; emitted / green / red == 31 / 31 / 0; no `check_min`.  Anything missing, unsatisfiable or
self-satisfying?  (`%-16s` and the 15-character assert keep `^$v  ` satisfiable; the longest name, `neg apparatus`, is
13.)  The skip disclosure (eleven earlier skip points, 1.2; S8): adequate in the header and the gate comment?

(i) **THE ONE ASK-AGAIN (R15; B14), on this clean table.**  Name the classes of change -- an id (AA1, AA2, ...) and ONE
phrase each, no code and no diff -- that you believe the 31 rows would NOT distinguish from the shipped repair; for each,
name its cell (S3's cross-product, PRETABLE section 3's partition, or the LUNA dispatch) and say FLOOR (a row owed now,
L2) or CLAUSE (e) (disclosed debt).  Everything this one ask returns is disposed of individually; there is no second ask.

**Q3 -- THE RECORDS.**  The CHANGELOG `#570` block, the OUTSTANDING_BUGS section and the ledger row are not yet written;
the probe header (2.4) and the gate comment (1.2) are.

(a) **The CHANGELOG block: what must it say, and NOT claim?**  At least: A8's claim and disclaimers (S2); the boot A/B as
measured (S24, P7); C5 withdrawn with E3's measurement (S4); C4 conditional, source-derived (S5); the include's rationale
(S16, P3); the R2 dependency and the SFRZ / ERROR mechanism (Q2(g)); clause (c) in the measured form; each score with
its artifact and instrument revision (R19); HEAD's case wrote cmmu[1] for ANY access class, a second wrong the fix removes
(PRETABLE 1.B(3)); no "parity with MIPS" (PRETABLE 1.A); the builder's departures (3.9: gate 14 as a background job of
7974 s; the harness insertions after propagation, so the gate never ran the block pre-fix -- P8; the include placement
against the spec's rationale; the staged checker copy named `.py.txt`; the pre-freeze smoke run; the rewrap).

(b) **OUTSTANDING_BUGS:** what is FILED (C1/R1 with the re-root obligation of the stepped instruction rows; C2/R2;
C3/R3; C4 conditional), what is WITHDRAWN (C5), and where the dispositions of P2, P5, P11, P12 and P15 belong.

(c) **The ledger row:** state `held` for Fable (with its hold question); witness
`probe:regress/artifacts/m88kbuserrregs/witness_20261023/m88k_buserr_probe.py` (rung 3; not implying instruction-fetch or
boot coverage); commits; stage entries naming their panel directories, with this pass's NOT FIRED and HELD entries.
Anything else owed?

(d) **The probe header and gate comment as written:** any sentence false or overclaiming (P3, P6, P10, P13, P14, P15)?

(e) **Which of the above is an L4 if written wrongly?**  List them.

**Q4 -- THE STANDING LICENSE.**

```
If, while verifying a claim, you found something ELSE — say so.
```

By id, with no reproduction recipe.  The drafter's own doubts are section 6 (P1-P15): confirm or refute each you checked.

---

## 9. Every path this brief names -- checked with `ls` at drafting time (`LS_PERMITTED.txt` beside this brief, VERBATIM)
~~~~
# Every path the T36 / #570 pass-2 brief names, checked 2026-10-24 02:08:38 -0500.  HEAD 7fca7187.
# Repo paths are relative to C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC; 'tracked' = git ls-files --error-unmatch succeeds.
OK    tracked   src/cpus/memory_rw.c
OK    tracked   src/cpus/cpu_m88k.c
OK    tracked   src/devices/dev_luna88k.c
OK    tracked   src/devices/dev_m8820x.c
OK    tracked   src/cpus/tmp_m88k_tail.c
OK    tracked   src/cpus/memory_m88k.c
OK    tracked   src/cpus/cpu_m88k_instr.c
OK    tracked   src/cpus/cpu_dyntrans.c
OK    tracked   src/debugger/debugger_cmds.c
OK    tracked   src/devices/dev_mvme187.c
OK    tracked   src/include/thirdparty/m8820x.h
OK    tracked   src/include/thirdparty/m8820x_pte.h
OK    tracked   src/include/thirdparty/m88k_dmt.h
OK    tracked   src/include/thirdparty/mvmeprom.h
OK    tracked   src/include/thirdparty/mvme_pcctworeg.h
OK    tracked   src/cpus/cpu_alpha_palcode.c
OK    tracked   src/devices/dev_lca.c
OK    tracked   src/devices/dev_pcc2.c
OK    tracked   src/devices/dev_sh4.c
OK    UNTRACKED regress/m88k_buserr_probe.py
OK    tracked   regress/gate_arm.sh
OK    tracked   regress/lib.sh
OK    tracked   regress/run.sh
OK    tracked   regress/gate_ab.sh
OK    tracked   regress/vme_default_probe.py
OK    tracked   regress/diff_wdc_identify.c
OK    tracked   regress/gate_offline.sh
OK    tracked   regress/gate_sh_rounding.sh
OK    tracked   regress/gdrom_default_probe.py
OK    tracked   regress/sh4_chcr_probe.py
OK    tracked   regress/wdc_addtoinbuf_probe.py
OK    UNTRACKED regress/lca_isaphys_probe.py
OK    tracked   regress/diff_m8820x.c
OK    tracked   regress/diff_m8invread.c
OK    tracked   regress/luna_intmask_probe.py
OK    tracked   regress/m8820x_sites_probe.py
OK    tracked   regress/readiness_predicate_test.py
OK    tracked   regress/artifacts/recordfix_20261002/chk_hrec.py.txt
OK    tracked   tools/BRIEF_TEMPLATE.md
OK    tracked   tools/CLAUDE.md
OK    tracked   tools/PIPELINE.md
OK    tracked   tools/adjudicate.sh
OK    tracked   tools/panel.sh
OK    tracked   tools/pipeline/ledger.json
OK    tracked   tools/pipeline/matrix.html
OK    tracked   tools/pipeline/check_probe_wiring.py
OK    tracked   tools/est_divergence.txt
OK    tracked   CHANGELOG.md
OK    tracked   OUTSTANDING_BUGS.md
OK    tracked   regress/artifacts/research_20261022/trunk_src.diff
OK    UNTRACKED regress/artifacts/m88kbuserrregs/pass1_20261023/PASS1_RULINGS.md
OK    UNTRACKED regress/artifacts/m88kbuserrregs/pass1_20261023/BUILD_SPEC.md
OK    UNTRACKED regress/artifacts/m88kbuserrregs/pass1_20261023/packet.md
OK    UNTRACKED regress/artifacts/m88kbuserrregs/pass2_20261023/roster_NOT_FIRED.txt
OK    UNTRACKED regress/artifacts/m88kbuserrregs/pass2_20261023/fable5.HELD.txt
OK    UNTRACKED regress/artifacts/m88kbuserrregs/pass2_20261023/argon.NOT_FIRED.txt
OK    UNTRACKED regress/artifacts/m88kbuserrregs/table1_20261023/fix570.diff
OK    UNTRACKED regress/artifacts/m88kbuserrregs/table1_20261023/staged/gate_arm.staged.diff
OK    UNTRACKED regress/artifacts/m88kbuserrregs/table1_20261023/staged/gate_arm.sh
OK    UNTRACKED regress/artifacts/m88kbuserrregs/table1_20261023/staged/check_probe_wiring.staged.diff
OK    UNTRACKED regress/artifacts/m88kbuserrregs/table1_20261023/staged/check_probe_wiring.py.txt
OK    UNTRACKED regress/artifacts/m88kbuserrregs/table1_20261023/m88k_buserr_probe.rev2.frozen.py.txt
OK    UNTRACKED regress/artifacts/m88kbuserrregs/table1_20261023/smoke_HEAD_unfrozen.out
OK    UNTRACKED regress/artifacts/m88kbuserrregs/table1_20261023/prefix_HEAD.out
OK    UNTRACKED regress/artifacts/m88kbuserrregs/table1_20261023/fixed.out
OK    UNTRACKED regress/artifacts/m88kbuserrregs/table1_20261023/fixed_witness24.out
OK    UNTRACKED regress/artifacts/m88kbuserrregs/table1_20261023/SCORES.txt
OK    UNTRACKED regress/artifacts/m88kbuserrregs/table1_20261023/PRETABLE.out
OK    UNTRACKED regress/artifacts/m88kbuserrregs/table1_20261023/BUILDER_QUESTIONS.md
OK    UNTRACKED regress/artifacts/m88kbuserrregs/table1_20261023/BASELINE.out
OK    UNTRACKED regress/artifacts/m88kbuserrregs/table1_20261023/legs_batch1.out
OK    UNTRACKED regress/artifacts/m88kbuserrregs/table1_20261023/legs_batch2.out
OK    UNTRACKED regress/artifacts/m88kbuserrregs/table1_20261023/legs_batch3.out
OK    UNTRACKED regress/artifacts/m88kbuserrregs/table1_20261023/legs_batch4.out
OK    UNTRACKED regress/artifacts/m88kbuserrregs/table1_20261023/legs_null_medium.out
OK    UNTRACKED regress/artifacts/m88kbuserrregs/table1_20261023/L3_armHEAD.out
OK    UNTRACKED regress/artifacts/m88kbuserrregs/table1_20261023/L5_stub.out
OK    UNTRACKED regress/artifacts/m88kbuserrregs/table1_20261023/L5b_absent.out
OK    UNTRACKED regress/artifacts/m88kbuserrregs/table1_20261023/L8_nullrm.out
OK    UNTRACKED regress/artifacts/m88kbuserrregs/table1_20261023/gates/gate14_run.out
OK    UNTRACKED regress/artifacts/m88kbuserrregs/table1_20261023/gates/gate11_run.out
OK    UNTRACKED regress/artifacts/m88kbuserrregs/table1_20261023/gates/grep3ffffff0.out
OK    UNTRACKED regress/artifacts/m88kbuserrregs/table1_20261023/boot_base.out
OK    UNTRACKED regress/artifacts/m88kbuserrregs/table1_20261023/boot_work.out
OK    UNTRACKED regress/artifacts/m88kbuserrregs/table1_20261023/boot_ab/console_diff_base_vs_fixed.txt
OK    UNTRACKED regress/artifacts/m88kbuserrregs/table1_20261023/build_work_fixed.out
OK    UNTRACKED regress/artifacts/m88kbuserrregs/table1_20261023/work_fixed_make.log
OK    UNTRACKED regress/artifacts/m88kbuserrregs/table1_20261023/CLEARANCE.out
OK    UNTRACKED regress/artifacts/m88kbuserrregs/table1_20261023/CLEARANCE_final.out
OK    UNTRACKED regress/artifacts/m88kbuserrregs/table1_20261023/prop_build.out
OK    UNTRACKED regress/artifacts/m88kbuserrregs/table1_20261023/BUILD_REPORT.md
OK    UNTRACKED regress/artifacts/m88kbuserrregs/table1_20261023/explore_20261023/explore_c5_ixnull.out
OK    UNTRACKED regress/artifacts/m88kbuserrregs/witness_20261023/m88k_buserr_probe.py
OK    UNTRACKED regress/artifacts/m88kbuserrregs/witness_20261023/MANIFEST.md5
OK    UNTRACKED regress/artifacts/m88kbuserrregs/witness_20261023/WITNESS_headbin.out
# directories:
OK    dir       regress/artifacts/m88kbuserrregs/
OK    dir       regress/artifacts/m88kbuserrregs/pass1_20261023/
OK    dir       regress/artifacts/m88kbuserrregs/pass2_20261023/
OK    dir       regress/artifacts/m88kbuserrregs/table1_20261023/
OK    dir       regress/artifacts/m88kbuserrregs/table1_20261023/staged/
OK    dir       regress/artifacts/m88kbuserrregs/table1_20261023/gates/
OK    dir       regress/artifacts/m88kbuserrregs/table1_20261023/boot_ab/
OK    dir       regress/artifacts/m88kbuserrregs/witness_20261023/
# outside the repository (absolute):
OK         18509 bytes  C:\DocumentNoSnc\cc\GXEMUL\_guest-src-openbsd22\sys\arch\mvme88k\mvme88k\trap.c
OK          8281 bytes  C:\DocumentNoSnc\cc\GXEMUL\_guest-src-openbsd22\sys\arch\mvme88k\include\m882xx.h
OK        309189 bytes  C:\DocumentNoSnc\cc\GXEMUL\CLAUDE.md
OK         28239 bytes  C:\DocumentNoSnc\cc\GXEMUL\est\src\cpus\memory_rw.c
OK         48416 bytes  C:\DocumentNoSnc\cc\GXEMUL\est\src\cpus\cpu_m88k.c
OK         33675 bytes  C:\DocumentNoSnc\cc\GXEMUL\est\src\devices\dev_luna88k.c
OK         25870 bytes  C:\DocumentNoSnc\cc\GXEMUL\est\src\devices\dev_m8820x.c
OK    dir       C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\
# result: 0 missing
~~~~
