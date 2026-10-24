# PASS-2 DIFF REVIEW -- round #570, ledger row `m88kbuserrregs` (research item T36) -- GXemul hardened fork
**Brief v1, COMPACT form (packet-fed seats).  It stands alone: sections 5, 6 and 8 -- every premise and question -- are
the FULL form's word for word; other evidence is condensed where marked.**  Drafted 2026-10-24 against HEAD `7fca7187`
plus the round's uncommitted edits, from `GXEMUL-SEC/tools/BRIEF_TEMPLATE.md`.

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

## 0. What this is, and how to answer

**The project.**  GXemul is an emulator that runs legacy operating systems in a sandbox; this fork does correctness work
on its C code and keeps each fix under a regression test.  *Guest* = the program inside; *host* = the emulator process.
A *variant* (also *mutant*) is a deliberately altered copy of the code used to test the tests; a *leg* is one such
measurement, `L<n>`.

**The defect.**  On MVME187 and LUNA-88K (the 88K machines modelled with MC88200 CMMUs), a guest access REFUSED by a
device raised the access exception but left the CMMU's PFSR (fault status, offset 0x108) and PFAR (fault address, 0x10c)
stale; at LUNA-88K's 0x3ffffff0 the board device wrote PFSR itself and then SERVED the access (no exception, no PFAR).
WRONG-RESULT; the fixed code ends no host process.

**The fix (four product files, byte-identical in `est/`).**  The MEM_M88K refused-device arm in `memory_rw.c` picks the
faulting side's CMMU by `cache` and, if that pointer is not NULL, writes PFSR = `CMMU_PFSR_BERROR << 16` and PFAR =
`(uint32_t) orig_paddr` before the unchanged exception; `cpu_m88k.c` includes the header defining those names; the LUNA
case returns 0 so the access is refused through that arm; `dev_m8820x.c` gets comment-only corrections.  The detector is
the rung-3 witness promoted to 31 rows and wired into gate 14.

**This pass.**  PASS 2 on the ACTUAL DIFF and its MEASURED detector, against the pass-1 rulings AS ADJUDICATED (section E
rules) and the builder rulings (S9).  The builder (Opus 5.5) is not on this panel; GPT-6 Astra adjudicates afterwards.
Nobody is asked to write code, a guest program or a variant: the variants are the records' own, by leg id.

A peer's unrelated uncommitted files share the working tree (`cpu_alpha_palcode.c`, `dev_lca.c`, `dev_pcc2.c`,
`dev_sh4.c`, `mvme_pcctworeg.h`, some regress and harness files).  Line numbers: working tree (HEAD where marked);
`cpu_m88k.c` is +4 relative to HEAD below its line 53.

**Answer format -- VERDICT LINE FIRST:**
~~~~
VERDICT: SHIP | SHIP WITH CHANGES | DO NOT SHIP -- <one line>
Q1: <one line>   Q2: <one line>   Q3: <one line>   Q4: <one line>
~~~~
Then a section per question; number findings F1..; mark claims READ / DERIVED (from this packet) / NOT CHECKABLE; cite
S1.. / P1..; grade defects L1-L4 (section 7), saying whether one is a floor breach.

---

## 1. THE DIFF

| + | - | file | shown |
|---|---|---|---|
| 4 / 24 / 7 / 25 | 0 / 5 / 3 / 25 | `cpu_m88k.c` / `memory_rw.c` / `dev_luna88k.c` / `dev_m8820x.c` | INLINED whole, 1.1 |
| 31 | 0 | `regress/gate_arm.sh` | INLINED whole, 1.2 |
| 11 (of 26) | 0 | `tools/pipeline/check_probe_wiring.py` | #570's 11 lines INLINED, 1.3 (15 are a peer's -- NOT SHOWN) |
| 836 | 0 | `regress/m88k_buserr_probe.py` (new) | SUMMARIZED: header extracts and scoring code, 2.4-2.5 |
| -- | -- | `regress/artifacts/m88kbuserrregs/` (new) | evidence, condensed in section 3; variant sources NOT SHOWN by design |
| -- | -- | CHANGELOG, OUTSTANDING_BUGS, ledger | NOT YET WRITTEN (Q3) |

*(Counts: `diff(1)` of `git show HEAD:<file>` against the working file.)*

### 1.1 The four product files (`table1_20261023/fix570.diff`, VERBATIM; equals a fresh regeneration)
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

### 1.2 `regress/gate_arm.sh`: the gate-14 block (`staged/gate_arm.staged.diff`, VERBATIM; = the working tree)
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
`check` is string equality, `count` is `grep -ac`.  The block copies `#568`'s directly above it and adds the
sentinel-once and SYMPTOM checks.  Gate 14's eleven earlier skip points are the header's GATE 14 list (2.4), re-checked
against the working tree at drafting time.

### 1.3 `check_probe_wiring.py`: #570's two MANIFEST entries (`staged/check_probe_wiring.staged.diff`, VERBATIM)
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
The checker reads `.py` only; the artifacts directory's one `.py` is the witness (others: `*.py.txt` / `*.sh.txt`, but
`staged/gate_arm.sh` -- P12).

### 1.4 The control flow around the edits (post-fix; CONDENSED, elisions marked)
`memory_rw.c`: `uint64_t orig_paddr = paddr;` is :437 and `paddr -= mem->devices[i].baseaddr;` :494 (S10); then:
~~~~
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
   ...  (608-613: the MEM_MIPS block; 614-642: the MEM_M88K block exactly as in 1.1)
  643| 					return MEMORY_ACCESS_FAILED;
  644| 				}
  645| 				goto do_return_ok;
  646| 			}
~~~~
`dev_luna88k.c`: 1.1's third hunk shows the case; S17 gives the rest.
The port source's include hunk (`regress/artifacts/research_20261022/trunk_src.diff`, VERBATIM):
~~~~
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

### 2.1 Identity
Untracked, 836 lines, md5 `d57c12ab`, byte-identical to the copy frozen before any table run.  The witness (rev 1, 24
rows, md5 `d59798b0`) is UNCHANGED (its `MANIFEST.md5` verifies 32 of 32).

### 2.2 The 31 rows (6 + 10 + 15)
* **CONTROL_ROWS (6):** `neg apparatus`, `mv devsig`, `mv cmmu rt`, `luna devsig`, `luna cmmu rt`, `unasm`.
* **SYMPTOM (10):** `uld pfsr`, `uld pfar`, `ust pfsr`, `ust pfar`, `vme pfsr`, `vme pfar`, `luna route`, `luna pfar`,
  `ifetch pfsr`, `ifetch pfar`.
* **Others (15):** `ok route`, `ok regs`, `uld route`, `uld icmmu`, `ust route`, `ust icmmu`, `vme route`, `vme icmmu`,
  `luna pfsr`, `luna icmmu`, `ifetch route`, `ifetch dcmmu`, `dbg noexc`, `null surv`, `null route`.
* New in revision 2: the four `ifetch` rows, `dbg noexc`, the two `null` rows.  **unasm 192** = 7 sessions x 23 words
  (`ok`, `uld`, `ust`, `vme`, `luna`, `ifetch`, `dbg`) + the `null` session's 31 (23 + cpu 1's 8).

### 2.3 CHANNEL against the measured red sets
Drafter's check against 3.4: every leg the header names for a row is in that row's measured red set; the measured sets
add only L5, and L18 / L19 via prerequisite strings.  **Single-row carriers:** L7 -> `dbg noexc`; L8b -> `null surv`; L9
-> `null route`; L6 -> the three `ifetch` metadata rows.

### 2.4 The header (extracts)
VERBATIM -- the include sentence (lines 33-35, P3) and WHAT #570 MAY CLAIM (lines 40-47):
~~~~
  * src/cpus/cpu_m88k.c: #include "thirdparty/m8820x.h" after m8820x_pte.h (upstream's placement, the transferred
    warrant) -- memory_rw.c is compiled inside cpu_m88k.c's translation unit (tmp_m88k_tail.c), and CMMU_PFSR,
    CMMU_PFAR and CMMU_PFSR_BERROR live only in that header.  Without it the repair does not compile.
   ...
WHAT #570 MAY CLAIM, AND WHAT IT DISCLAIMS (PASS1_RULINGS A8).  Claimed: fault metadata for CLAIMED, REFUSED,
unsuppressed device accesses that pass the running-transition check, on a cpu that has a CMMU, plus LUNA's probe case
routed into that path.  Disclaimed -- never "every 88K bus error now carries PFSR and PFAR": an UNCLAIMED address (no
exception, no CMMU write; R3); on luna-88k every OTHER device refusal still stops the cpu before the arm; FREE-RUNNING
instruction-fetch refusals (vector 2, then the dyntrans `bad:' tail stops the cpu before any handler -- R1); callers
that pass NO_EXCEPTIONS (the debugger: the arm's own `!no_exceptions' term keeps them out -- `dbg noexc'); the
translation-fault writer (memory_m88k.c, not edited); a sub-word access's PFAR (the byte address is written, a
transferred warrant only -- no MC88200 manual is on disk); CMMU-less cpus (no write, the exception unchanged).
~~~~
ROWS, CONDENSED from header lines 104-161 (VERBATIM in the FULL form).  Each session seeds both CMMUs' PFSR / PFAR
(data 0x5a5a5a5a / 0x13572468, instruction 0x2468ace0 / 0x0badf00d), makes the access, and reads the four back.
~~~~
neg apparatus: bogus subtype `187': exit1, no register dump -- green BY DESIGN on an exit-1 non-emulator (L5)
mv devsig / luna devsig: both IDRs 0x00a90000 -- L19
mv cmmu rt / luna cmmu rt: the four seeds read back -- L18 (misplaced writes overwrite the seeds), L19
unasm: every placed word re-read, LITERAL 192
ok route (VME VBR, an accepted access): fall-through, r4 = 0x67000000 -- L19, observable prereq:nodev (every served
    CMMU access faults first; "v3" is not reachable by a global widening)
ok regs: all four seeds survive -- L18 (observable prereq:readback), L19
uld / ust / vme route: v3, SXIP = CODE+0x28 | V, DMA0 = the address -- L17
uld / ust / vme pfsr: data PFSR 0x30000 (HEAD: the seed) -- L3, L10, L6b; ust also L15; vme also L16
uld / ust / vme pfar: data PFAR = the physical address (HEAD: the seed) -- L3, L11 (0x10 / 0x90), L12, L6b; ust L15;
    vme L16
uld / ust / vme icmmu: the instruction CMMU keeps its seeds -- L13, L14, L6b (NOT L15 / L16)
luna route (0x3ffffff0): v3, SXIP, DMA0 = 0x3ffffff0, r4 kept (HEAD: fall-through, served 0) -- L4 (= L20), L21, L17,
    L22 (prereq:handler)
luna pfsr: 0x30000, GREEN on HEAD (the case's own write) -- L3, L10, L21 (its UNIQUE variant), L22, L6b
luna pfar: 0x3ffffff0 (HEAD: the seed) -- L3, L4, L11 (0x0), L12, L21, L22, L6b
luna icmmu: kept -- L13, L14, L22, L6b
ifetch route (jmp to 0xfff46010): v2, SXIP 0xfff46013 (V|E), DMA0 0; an ATTRIBUTION row, not a CONTROL row -- L17
    (prereq:handler); it CANNOT vary under L6, by construction (the vector expression reads `cache` itself)
ifetch pfsr: instruction PFSR 0x30000 (HEAD 0x2468ace0) -- L6, L3, L10, L17
ifetch pfar: instruction PFAR 0xfff46010 (HEAD 0xbadf00d) -- L6, L3, L11 (0x10), L12, L17
ifetch dcmmu: the DATA CMMU keeps its seeds -- L6, L13, L14, L17
dbg noexc (the `ok' program, own session): `dump 0xfff46010 0xfff46020' after the seeds gives zeros, pc stays 0x10028,
    fall-through, seeds kept -- L7 (the term dropped: the dump fails, cpu 0 vectors, the data CMMU is written)
~~~~
VERBATIM -- the R2 disclosure (152-155) and the CMMU-less block with its two rows (162-177):
~~~~
    *** R2 DEPENDENCY, DISCLOSED (PASS1_RULINGS C2): stepped, the instruction refusal reaches the arm through the step
    loop's disassembly pre-read (cpu_dyntrans.c, CACHE_INSTRUCTION without NO_EXCEPTIONS).  When R2 is fixed the
    pre-read stops raising, the step's own fetch reaches R1's `bad:' tail and halts the cpu, and these four rows go
    red for that UNRELATED reason -- they are re-rooted when R1 and R2 land (the obligation is filed with them). ***
   ...
  a CMMU-LESS cpu (mvme187 -n 2, cpu 1) -- B5c, the {data, instruction} x {CMMU absent} cells CONJUNCTIVELY
    cpu 0 runs the seeded `uld' program alone (19 steps) and parks in H's `br .' (nothing is scored from it).  cpu 1 is
    set up by `focus 1' (pc, r5, the two marker values, its own VBR); `tlbdump 1' must show no CMMU (the NULL premise);
    `pause 1'; part 1 `step 3': `ld r4,r5,0' at 0xfff46010 -> cpu 1's vector 3 stores HANDLED and branches to J (the
    FELL store after the load runs only if no exception was raised); the markers and `reg 1,0' are read HERE (a second
    fault zeroes DMA0).  Part 2 `step 5': J `jmp (r5)' -> the instruction fetch at 0xfff46010 is refused with cmmu[0]
    NULL.  *** SFRZ, DISCLOSED: the data fault left PSR.SFRZ set and no `rte' clears it (an `rte' would resume at SNIP,
    the FELL store), so this second, non-trap fault is delivered as ERROR (vector 10), VBR1 + 0x50, where `br .' parks
    cpu 1 (VBR1 + 0x10 parks it too).  The arm runs BEFORE m88k_exception, so the NULL test is exercised whatever
    the vector. ***  Stepped, the fetch rides R2 like the ifetch rows; with R2 fixed the step's own fetch reaches the
    same arm, so the NULL-check observable survives and only the after-fault flow changes (R1's halt).
    null route     part 1: HANDLED set, FELL clear, SXIP 0x10202, DMA0 0xfff46010.  L9 (exception moved inside the NULL
                   check: fell), L17 (fell), L8 (the session dies in part 1)
    null surv      the session reaches part 2's prompt alive with both marker dumps readable.  L8 (NULL check removed:
                   cpu 1's data load dereferences NULL), L8b (the check conditioned on the data label: the instruction
                   fetch dereferences NULL in part 2)
~~~~
VERBATIM -- CONTRACT (NOT CLAIMED) and GATE 14 (lines 187-210; SYMPTOM's ten members are listed in 2.2, its classes in
2.5's code):
~~~~
CONTRACT (clause e).  DESIGNED to catch: the pre-fix defect and the variants named per row above (measured per leg in
table1_20261023/SCORES.txt).  NOT CLAIMED, so a later escape is outside the contract rather than an argument:
  * VA != PA.  PFAR := `vaddr' is not an operand the m88k arm reads (the MEM_MIPS block that reads it is compiled out),
    and every session leaves the CMMUs' APR invalid, so physical = virtual (memory_m88k.c).  A guest COULD separate them
    (a SAPR/UAPR store sets APR_V; a BWP store programs a BATC) -- these sessions do not;
  * sub-word accesses and byte addresses: every access is a word at a word-aligned address (PFAR's low bits are
    UNKNOWN for silicon; the byte address is upstream's choice, a transferred warrant);
  * a LUNA STORE at 0x3ffffff0 (the generic direction is pinned by `ust');
  * an UNCLAIMED physical address (INFO `unclaimed'; R3);
  * luna-88k `-n 2..4' (per-cpu CMMU selection beyond the null session's mvme187 cpu 1), xmem, the 88110 (mvme197);
  * FREE-RUNNING instruction-fetch refusals (R1: the cpu stops before any handler); the stepped ifetch and null rows
    ride R2 (above);
  * translation-fault semantics (memory_m88k.c is not edited);
  * the OpenBSD reader itself (trap.c's `(dpfsr >> 16) & 7 == 3' and badaddr()'s eh.S recovery); a boot is measured
    separately (table1_20261023/boot_ab/);
  * the sibling CMMU's real latch semantics: the `icmmu' / `ifetch dcmmu' wants encode the ruling `kept' (A9); the
    hardware behaviour is UNKNOWN, and a guest's snapshots CAN differ (do not read the rows as "unobservable");
  * PFSR / PFAR bits beyond the exact values written; real MC88200 timing or the P-bus.
  Clause (c) (null medium): measured at table1_20261023/L5_stub.out and L5b_absent.out (see SCORES.txt).

GATE 14 (regress/gate_arm.sh) runs this probe in the block after #568's.  *** THAT BLOCK CAN BE SKIPPED WITHOUT
RUNNING: gate_arm.sh has eleven earlier skip points (`grep -n -e gate_skip -e need_exec regress/gate_arm.sh': :84
need_exec, :85 python3, :93 the load stub, and the eight probe-completion skips :105 :389 :430 :515 :638 :695 :816
:949), and any one of them ends the gate before this block -- a SKIP, which is never evidence. ***
~~~~

### 2.5 The scoring code (VERBATIM: `row()`, `symptom()`, the null rows, score, sentinel)
*(Not shown: `prereq_bad()`, which replaces a row's value with a cause-free string when a prerequisite fails, and
`_marks()`, the RAM markers as handled / fell / both / neither.)*
~~~~
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
   ...
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
   ...
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

## 3. THE MEASUREMENTS (CONDENSED)

**3.1 Order (mtimes).**  PRETABLE 22:28 -> probe frozen 22:42:48 -> pre-fix run 22:42:52 -> product edits 22:47 ->
post-fix 22:48 -> boot A/B 22:49 -> variant table 22:58-23:09 -> propagation 23:14 -> harness insertions 23:16 -> gate 14
23:17-01:30 -> gate 11 01:31.

**3.3 Clause (a), VERBATIM** -- `prefix_HEAD.out`, `fixed.out` (witness: L1, 3.4); then the unscored `INFO null
cpu0` line, fixed build and L9 (P15; HEAD prints `cpu1 end pc=0x30050` like the fix, L17 `0xfff46010` like L9):
~~~~
M88K_BUSERR_RESULT=21/31
M88K_BUSERR_CONTROL=OK
M88K_BUSERR_SYMPTOM=PRESENT 10/10
M88K_BUSERR_RESULT=31/31
M88K_BUSERR_CONTROL=OK
M88K_BUSERR_SYMPTOM=ABSENT
INFO null cpu0   (unscored) pc=0x10114 path=v3 dPFSR=0x30000 dPFAR=0xfff46010 r31=0x5678; cpu1 end pc=0x30050 markers-after-part2=handled
INFO null cpu0   (unscored) pc=0x10114 path=v3 dPFSR=0x30000 dPFAR=0xfff46010 r31=0x5678; cpu1 end pc=0xfff46010 markers-after-part2=fell
~~~~

**3.4 The variant table** (CONDENSED from `SCORES.txt`: leg, score, instrument -- `d31` detector, `w24` witness --
CONTROL, description, measured red set; three marked complements).  All 27 recorded as matching their prediction; all
20 variant builds FRESH, 0 warnings, restored (P5, P11 concern this file).
~~~~
pre    21/31 d31 OK   HEAD binary 2efeec55 (clause (a), pre-fix)
       red: ifetch pfar, ifetch pfsr, luna pfar, luna route, uld pfar, uld pfsr, ust pfar, ust pfsr, vme pfar, vme pfsr
fix    31/31 d31 OK   the #570 fix, work binary 3cd0501c (clause (a), post-fix)
       red: (none)
L1     24/24 w24 OK   the FROZEN 24-row witness on the fixed binary (witness clause (i))
       red: (none)
L3     21/31 d31 OK   clause (b): memory_rw.c's arm reinstated verbatim from HEAD (blob 3d47dd66), the LUNA case fixed
       red: ifetch pfar, ifetch pfsr, luna pfar, luna pfsr, uld pfar, uld pfsr, ust pfar, ust pfsr, vme pfar, vme pfsr
L3/w24 16/24 w24 OK   the same L3 binary on the frozen witness
       red: luna pfar, luna pfsr, uld pfar, uld pfsr, ust pfar, ust pfsr, vme pfar, vme pfsr
L4     29/31 d31 OK   clause (b): dev_luna88k.c's case reinstated verbatim from HEAD (blob 6ecc6908), the arm fixed
       red: luna pfar, luna route
L4/w24 22/24 w24 OK   the same L4 binary on the frozen witness
       red: luna pfar, luna route
L5     1/31  d31 FAIL clause (c): an exit-1 non-emulator in the binary's place
       red: 30 rows -- every row EXCEPT neg apparatus  [complement form, CONDENSED]
L6     28/31 d31 OK   (d) the added selector weakened to always-data
       red: ifetch dcmmu, ifetch pfar, ifetch pfsr
L6b    19/31 d31 OK   (d) the added selector weakened to always-instruction (Q16)
       red: luna icmmu, luna pfar, luna pfsr, uld icmmu, uld pfar, uld pfsr, ust icmmu, ust pfar, ust pfsr, vme icmmu, vme pfar, vme pfsr
L7     30/31 d31 OK   (d) the `!no_exceptions' conjunct dropped from the outer guard
       red: dbg noexc
L8     29/31 d31 OK   (d) the added NULL check removed
       red: null route, null surv
L8b    30/31 d31 OK   (d) the NULL check conditioned on the data label (Q15)
       red: null surv
L9     30/31 d31 OK   (d) the exception moved inside the NULL check
       red: null route
L10    26/31 d31 OK   PFSR value: raw 3 instead of 3 << 16
       red: ifetch pfsr, luna pfsr, uld pfsr, ust pfsr, vme pfsr
L11    26/31 d31 OK   PFAR value: the device-relative paddr
       red: ifetch pfar, luna pfar, uld pfar, ust pfar, vme pfar
L12    26/31 d31 OK   PFAR not written (PFSR only)
       red: ifetch pfar, luna pfar, uld pfar, ust pfar, vme pfar
L13    26/31 d31 OK   target: both CMMUs written
       red: ifetch dcmmu, luna icmmu, uld icmmu, ust icmmu, vme icmmu
L14    26/31 d31 OK   target: the sibling's PFSR cleared to SUCCESS (the translation-fault writer's shape)
       red: ifetch dcmmu, luna icmmu, uld icmmu, ust icmmu, vme icmmu
L15    29/31 d31 OK   guard operand: writes only for MEM_READ
       red: ust pfar, ust pfsr
L16    29/31 d31 OK   guard operand: the VME device excluded (Q17)
       red: vme pfar, vme pfsr
L17    22/31 d31 OK   placement: the exception dropped
       red: ifetch dcmmu, ifetch pfar, ifetch pfsr, ifetch route, luna route, null route, uld route, ust route, vme route
L18    6/31  d31 FAIL placement: the NULL-checked writes moved to just before the outer guard (Q14)
       red: 25 rows -- every row EXCEPT neg apparatus, mv devsig, luna devsig, null surv, null route, unasm  [complement form, CONDENSED]
L19    4/31  d31 FAIL outer guard widened to res <= 1
       red: 27 rows -- every row EXCEPT neg apparatus, null surv, null route, unasm  [complement form, CONDENSED]
L21    28/31 d31 OK   the LUNA case's write deleted, the case still served (break)
       red: luna pfar, luna pfsr, luna route
L22    27/31 d31 OK   the LUNA case deleted (CL15's counterfactual, Q18)
       red: luna icmmu, luna pfar, luna pfsr, luna route
L5b    --    d31 --   clause (c): the binary ABSENT
       red: (FileNotFoundError before row 1: no row emitted, NO sentinel)
L20    not run: L20 = L4 (HEAD's case verbatim IS 'left returning 1, write kept'; section 11, Q13)
~~~~

**3.5 The pre-table check** (`PRETABLE.out`, VERBATIM): AMENDMENT 1's AM-2, and section 4's CHANNEL CHECK.
~~~~
AM-2  THE {data, instruction} x {CMMU present, absent} CROSS-PRODUCT (section 10 / E B5c), with the rows holding each:
        data x present         uld/ust/vme/luna pfsr, pfar, icmmu (+ their route rows as attribution)
        instruction x present  ifetch pfsr, ifetch pfar, ifetch dcmmu (+ ifetch route as attribution CONTROL, AM-5)
        data x absent          null route (HANDLED set and FELL clear = the exception stayed OUTSIDE the NULL check;
                               reaching part 1's dump = survival through the data cell)
        instruction x absent   null surv (reaching part 2's prompt with both dumps readable = survival through the
                               instruction refusal's arm with cmmu[0] NULL)
      The joint cell licenses no cpu-number, address or device-name products (section E, Q3 bound).
   ...
  CHANNEL CHECK (is each named channel able to vary under its named mutant?): yes for 1-3, 6-31.  For 4 and 5 the
  NAMED channel (v3 on an accepted access; changed seeds after an accepted access) cannot be reached by ANY global
  widening, because the probe's own prerequisites are served device accesses that fire first; the row still reds,
  through its prerequisite string.  NOT VACUOUS (the got string varies), but the header must name the channel that
  is actually available (codex:116; B6).  This answers the CHANNEL line's write-time question for this round: the
  channel under each mutant WAS knowable at writing time, and for two rows it is not the one grok:108-109 named.
~~~~
Its section-3 partition, CONDENSED: `res`, `no_exceptions`, `cache`, the `cmmu[idx]` pointer EXHAUSTED; `orig_paddr`,
cpu, `writeflag`, relative `paddr`, device, width SAMPLED (sub-word and VA != PA untested).

**3.6-3.9.**  Gate 14 `PASS (1310 checks)`, `wall=7974s`, the `#570` block's 40 checks `ok`, the `#568` pin 38 / 38; gate
11 `PASS (111 checks)`.  Boot A/B: base `reason=MARKER ninstrs=7651336103 wall=125`, fixed `reason=MARKER
ninstrs=7550665157 wall=120`, markers 1:1:1 both; neither log names 0x3ffffff0, a failed access or an exception (P7).
**The builder's departures** (`BUILD_REPORT.md` section 6, CONDENSED): (1) the include after `m8820x_pte.h` as directed,
though upstream puts it before; (2) the staged checker copy named `.py.txt`; (3) the harness insertions made after
propagation -- the gate never ran the block pre-fix; (4) gate 14 as a tracked background job; (5) a pre-freeze smoke
run; (6) `dev_m8820x.c` rewrapped to keep its line count (`FAILURE()` embeds `__LINE__`); (7) C5 measured withdrawn, C4
conditional; (8) records left to the main loop.

---

## 4. Section C0 (CONDENSED; VERBATIM in the FULL form)
At HEAD: no CHANGELOG mention of the row or `#570`; no commit touches the probe or its artifacts; the ledger row is
`open`, witness `none`, no commits; 25 tracked files differ from HEAD, 6 of them #570's.  **NOT SHIPPED.**

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

## 7. The project rules the questions apply (load-bearing lines, VERBATIM, working-tree `tools/CLAUDE.md`)
~~~~
 1328| > **THE FLOOR.** A detector is VACUOUS — replace it IN-ROUND — unless it (a) fails on the
 1329| > pre-fix build, (b) fails on a **VERBATIM REINSTATEMENT of the removed defect at EVERY fixed
 1330| > site**, and (c) fails on a **NULL MEDIUM** -- a product medium carrying none of the behaviour under
 1331| > test (the clause-(c) block below says what that is per instrument kind). Below the floor, the
 1358| > **RECORD CLAUSE (c) IN ONE OF EXACTLY TWO FORMS, never as a bare clause letter beside a row name:**
 1359| > * `(c): measured at <artifact>` -- the leg was run and its receipt is durable;
 1360| > * `(c): by construction via <row/pin>, leg not run` -- e.g. the gate pins the row count by EQUALITY
 1361| >   and a named row reds on a dead run, or the differential `#include`s the product and its gate reds
 1362| >   on a compile failure.  **A by-construction claim is checked by READING that shape; where the reading
 1376| > **(d) The detector must also fail when the fix is PRESENT but its REPAIR IS NULLED —
 1377| > the guard kept, its effect removed.**
 1517| > > **The rule ENUMERATES joint cells wherever the body distinguishes them; the FLOOR -- the cells a row
 1518| > > is OWED for -- is the cross-product of the guard's dominating predicates with the device-STATE lvalues
 1519| > > the fix's own repair path reads that are JOINTLY REACHABLE through its own data flow.**  The bits of
 1741| > | **CHANNEL** | for each row, name **the mutant it kills** and **the observable that differs under that mutant**. A row whose named channel cannot vary under its named mutant is VACUOUS BY CONSTRUCTION, and that is knowable at writing time, before any table runs | a survival oracle at a REFUSAL-EFFECT site: guarded and unguarded code both survive |
 2481| > > Everything ONE ask returns is disposed of INDIVIDUALLY under L1–L4 and the floor — and **a
 2482| > > floor breach among the findings is L2, repaired in-round however late it is found.** A
 2613| > * **L2 — floor breach.** The shipped detector fails vacuity-floor clause (a), (b) or (c) —
 2614| >   replace in-round however late it is found.
 2615| > * **L3 — undischarged obligation.** The row is the sole carrier of something the round OWES
 2616| >   (a de-escalation accept row; the "shipped a detector" claim itself). A vacuous sole carrier
 2617| >   makes the round's record false.
 2618| > * **L4 — wrong record.** Prose or comments claiming coverage a measurement refutes.
 3789| wrong. **Re-grep every same-file citation AFTER the last edit to that file**, not when
~~~~
(R1 floor; R2 clause (c)'s forms; R3 clause (d); R7 floor vs clause (e); R9 CHANNEL; R15 one ask-again, counting
asks; R16 L2-L4 (L1 = still under construction); R18 re-grep after your own edits.  R5, R6, R19: FULL form.)

---

**THIS FIRING ANSWERS Q3 AND Q4 ONLY.**  Q1 and Q2 went to a separate firing of this same packet; treat the settled design as given here and do not answer them.  Keep hidden reasoning short and put the VERDICT line and the answers in the response itself.

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

## 9. Paths
Checked with `ls` at drafting time: 0 missing (listed in the FULL form).
