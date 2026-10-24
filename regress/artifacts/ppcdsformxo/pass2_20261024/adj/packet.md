# ADJUDICATION of T2 (`ppcdsformxo`, round `#571`) PASS 2 -- for GPT-6 Astra and Grok 4.7 (owner roster 2026-10-23/24)

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

You adjudicate the pass-2 DIFF REVIEW of one regression-testing round in the GXemul hardened fork: a correctness fix to the
emulator's PowerPC instruction decoder (the 64-bit DS-form load/store forms selected by the instruction word's two XO bits,
which the committed decoder folded into the displacement) and the 39-row regression detector, kill table and gate block
shipped with it.  Seven answers from five seats came back, all LAND WITH CHANGES, and the main loop has read every one and
written its dispositions in `..\PASS2_RULINGS.md` (the parent directory of this packet): twenty-eight findings F1-F28, two
disputes D1-D2, twelve measured checks M1-M12.  **Your job is to find which of those dispositions is WRONG.**  The main loop
ACCEPTED or REFINED twenty-six of twenty-eight findings and REJECTED one seat's Q2 outright; that is a suspicious ratio and
agreement is not evidence.  You may open every file named here and the tree at HEAD `add098b9` plus this round's working-tree
edits (`src/cpus/cpu_ppc_instr.c`, `regress/gate_ppc.sh`, `regress/ppc_dsform_probe.py`, `tools/precommit_check.sh`;
`tools/pipeline/check_probe_wiring.py` carries uncommitted PEER edits -- read it via `git show HEAD:<path>` and the staged copy
`..\..\table1_20261024\staged\check_probe_wiring.py.txt`).  Do not build or run anything; do not propose reproduction recipes
or program listings; state dispositions by id.

**Self-review is disclosed and asked to be HARDER:** Astra reviews its own findings F17, F19, F20, F21, F22 and its D1
position; Grok reviews its own D2 dissent and the D1 ruling made in its favour.  A ruling in your favour is the one you are
least likely to test -- test it first.  Check that the REPAIRS are right, not merely that the findings were.

All paths are under `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\ppcdsformxo\` unless absolute.  The brief the
seats answered is `pass2_20261024\packet.md` (FULL: Astra, Grok) / `packet_compact.md` (Argon) / `packet_packetfed.md` (GLM and
DeepSeek, split Q1-2 / Q3-4).  The measured table is `table1_20261024\` (its three records carry dated ADDENDA written after the
seats answered; `PRETABLE.out` and `PREDICTIONS.txt` are untouched); the witness is `witness_20261024\`.

## 1. The seats and where their answers are

| seat | file | verdict | class | note |
|---|---|---|---|---|
| GPT-6 Astra (you, as reviewer) | `pass2_20261024\codex_t2p2.txt` | LAND WITH CHANGES | file-reading | rc 0, refusal 0, gpt-6-astra / ultra |
| Grok 4.7 (you, as reviewer; plan mode, WORKING tree) | `pass2_20261024\grok_t2p2.txt` | LAND WITH CHANGES | file-reading | exit 0 |
| Gemini 4 Argon through agy | `pass2_20261024\argon_agy_t2p2.txt` | LAND WITH CHANGES | file-reading | **Q2(a), Q2(b), Q3(f) REJECTED -- see F25** |
| GLM 5.3 | `ollama_glm_t2p2_Q12.txt`, `ollama_glm_t2p2_Q34.txt` | LAND WITH CHANGES x2 | packet-fed | labels READ / REASONED / NOT CHECKABLE |
| DeepSeek v4-pro | `ollama_deepseek_t2p2_Q12.txt`, `ollama_deepseek_t2p2_Q34.txt` | LAND WITH CHANGES x2 | packet-fed | |
| Fable 5.1 | `fable5.HELD.txt` | HELD by the owner, with its question | -- | |
| kimi, minimax, Opus-as-seat | `roster_NOT_FIRED.txt` | DELIBERATELY NOT FIRED by roster | -- | |

## 2. What the main loop did in response (the material you adjudicate)

**No product-code change.**  All seven seats found the diff to `src/cpus/cpu_ppc_instr.c` exact (F1); the main loop changed
nothing in it (D2 below is the one request for a product-comment edit, ruled against).

**One docstring/comment-only revision of the detector (D1, F2, F19)** -- applied 10:11, verified code-identical by stripping
the docstring and comments from both revisions and comparing the rest (`table1_20261024\repair_p2\probe_docfix.py.txt`),
re-measured 10:15-10:16 (`repair_p2\remeasure.out`): the revised detector on the BASE binary (`prefix_BASE2.out`) 22/39
CONTROL=OK SYMPTOM=PRESENT 17/17 with the RED line byte-identical to `prefix_BASE.out`'s; on the fixed `build/gxemul`
(`fixed2.out`) 39/39 ABSENT RED=none; gate 13 alone (`gate13b_20261024.out`) PASS 193 checks, REGRESS_PASS, the `#571` block
all ok.  md5 `0266228894811ba6c51cff82585753c9` (836 lines, measured by every leg) -> `59e83491a5819a599c610b1aa8e8b847`
(845 lines, shipped).  The diff, verbatim:

~~~~
--- a/regress/ppc_dsform_probe.py (md5 0266228894811ba6c51cff82585753c9)
+++ b/regress/ppc_dsform_probe.py
@@ -46,11 +46,15 @@
   CLAIMED: for ld, ldu, lwa, std and stdu, the effective address (the XO bits are never part of
     the displacement), the width and extension of the transfer, and whether RA is written (ldu
-    and stdu write EA; ld, lwa and std leave RA alone); the expected bytes at every store's
-    destination, and for stdu the seeded bytes around it; the three reserved XO encodings stop
+    and stdu write EA; ld, lwa and std perform no base update -- a load with RT = RA still
+    changes that register through its destination write, which no row drives); the expected
+    bytes at every store's destination, and for the ordinary stdu (DS != 0, RA != RS) the seeded
+    bytes around it (`stdu neigh'; the other stores' flanks are printed, not graded); the three
+    reserved XO encodings stop
     the CPU and write nothing; ldu and stdu with RA = 0 (DS != 0) stop the CPU and write
     nothing; lwz +6 and stw +6 keep the low two bits of a D-form displacement.  The DS = 0 value
     rows pin the address each access reaches, not which half of the handler table was selected.
   NOT CLAIMED:
-    * ldu with RA = RT (an invalid form; after the fix it leaves RT = EA; not checked);
+    * ldu with RA = RT (an invalid form; after the fix, when the access succeeds, it leaves
+      RT = EA -- the handler returns before the update on a failed access; not checked);
     * 32-bit CPUs: opcodes 58 and 62 are illegal on 32-bit implementations; before and after
       this fix a 32-bit CPU decodes them through the same arm; the MODE32 table has real
@@ -60,4 +64,8 @@
     * the joints of DS = 0 with RA = 0: ldu and stdu (the only observer of an update
       conditioned on a non-zero displacement), ld and std, and lwa;
+    * the sign of DS crossed with RA -- a negative DS at RA = 0 and a positive DS at RA != 0
+      for ld, ldu, std and stdu, and any negative DS for lwa -- and the reserved encodings at
+      DS = 0 or RA = 0: the case bodies read neither the sign of DS nor RA, so these are not
+      floor cells; not rowed;
     * lwa of a word whose bit 31 is clear;
     * the D-form opcodes other than lwz and stw;
@@ -161,5 +169,6 @@
 def row(name, got, want, note=""):
     assert name not in [n for n, _ in rows], "DUPLICATE ROW NAME %r" % name
-    #  14, not 15: gate 13 pins each row as `^name  ' (two spaces) inside this %-16s column.
+    #  14 is a margin: gate 13 pins each row as `^name  ' (two spaces) inside this %-16s column,
+    #  which gives a 15-character name its two spaces as well (16 misses); the cap stays one under.
     assert len(name) <= 14, name
     ok = (got == want)
~~~~

**One comment + title edit of the gate (F3/K2, F16)** -- `repair_p2\gate_fix.diff`, no check line changed
(`regress/gate_ppc.sh` is +41/-1 against HEAD; the staged copy `table1_20261024\staged\gate_ppc.sh.txt` refreshed):

~~~~
-gate_begin "gate 13: PowerPC FP conversion + FPSCR (#304/#305/#324-#330) + rlwimi/rldimi/rldicl"
+gate_begin "gate 13: PowerPC FP conversion + FPSCR (#304/#305/#324-#330) + rlwimi/rldimi/rldicl + #571 DS-form"
...
-# the reason the rlwimi block gives: `-E bareppc -M 64' needs no image, so a red row is recorded first.  Eight
-# debugger-stepped sessions (loads, stores and five stop sessions, each stop word last) and one bogus-machine
-# session; the rung-3 witness of the loads (regress/artifacts/ppcdsformxo/witness_20261024/) is NOT run here.
+# the reason the rlwimi block gives: `-E bareppc -M 64' needs no image, so a red row is recorded first.  Seven
+# debugger-stepped guest sessions (loads, stores and five stop sessions, each stop word last) plus one
+# bogus-machine session that exits before any step -- eight in all; the rung-3 witness of the loads
+# (regress/artifacts/ppcdsformxo/witness_20261024/) is NOT run here.
~~~~

**Records:** dated addenda appended to `table1_20261024\DETECTOR_FREEZE.txt`, `SCORES.txt` and `BUILD_REPORT.md` (each quotes
what it corrects: K3, K4, K5, K6 + F7, K12/K13, K14, F17, F27, the revision note); the frozen leg drivers preserved as
`table1_20261024\drivers\*.txt` with an md5 manifest (K4); the landing drafts (CHANGELOG round block, commit message,
OUTSTANDING_BUGS section, ledger ops -- in the session scratchpad, inlined for the seats in the pass-2 brief's section 9)
corrected for K1, K2, K5, K7-K11, K12, F15, F17, F20, F21, F22, F24.

## 3. The two DISPUTES (each side verbatim in `..\PASS2_RULINGS.md` section DISPUTES; summarised here)

* **D1 -- K1, the probe's false names-cap comment: EDIT (re-freeze) or ERRATUM?**  GLM: an edit "falsifies the 'measured by the
  FROZEN detector md5 0266228...' citations ... re-freezing and re-measuring 17 legs to delete one comment is disproportionate
  -- but the panel should choose explicitly".  Grok: "Correct the comment ... Exhibit the comment-only diff.  The sixteen legs
  stay the record of the behaviour."  Astra: "Correct the probe comment".  **RULED EDIT** in Grok's form: the carrier's L4
  corrects a wrong record in place; the diff is docstring/comment-only (verified mechanically), so the sixteen legs stand
  and only clause (a) and the post-fix run were re-measured on the shipped md5 (identical red set; 39/39; gate PASS 193); the
  MANIFEST key carries no md5.  Both revisions are named in every record.
* **D2 -- K7, must the STD case's product comment state the `stdu` RA = 0 stop?**  Grok: "It does not state that `stdu` with
  RA=0 now stops ... Add that clause.  Licence L4 (site comment)."  DeepSeek: "a record improvement (L4)".  Astra: "optional L1
  clarity".  GLM: "Accurate as written ... no R-L licence".  Argon: "no product edit".  **RULED NO product edit**: L4 is the
  licence for a WRONG record and no seat says the comment is wrong -- "as for PPC_HI6_LD above" incorporates the LD comment,
  which states the guard; `case 1: update = 1` sits three lines below; the contract's BEHAVIOUR CHANGES and the CHANGELOG name
  both stops; and a product-comment edit re-opens est/ propagation, three build-tree rebuilds and the two-part clearance for a
  derivable sentence.

## 4. Dispositions you should aim at (the ones most likely wrong, in the main loop's own estimate)

* **F22** -- the filed design row `ppc64on32gate`: Astra and Grok said LOW was not established by the design-only ruling; the main
  loop set the ledger `sev` to `RESEARCH` (the ledger's only existing value for such a row, used once, by `cpusexitsweep`) and
  the OUTSTANDING_BUGS entry to "(design, open)".  Is `RESEARCH` the right value, or should the row carry a provisional LOW with
  the caveat in its note?
* **F25** -- Argon's Q2(a)/(b) and Q3(f) describe rows, legs, seed values and scores that occur ZERO times in the probe, in
  `pass1_20261024\BUILD_SPEC.md`, in the pass-1 brief and in the compact packet it was given (`stdu rars`, `std low4`,
  `lwa pos value`, `ldu neg val`, `stdu window`, `xo58_3 stop`, `L6c`, `L11a`, `0x3028`, `0x1122334455667788`, "L1 BASE 11/39",
  "unasm census ... 78"); its K14 claim of an `examine 0x0 0x20` at probe :517 is false (the probe has no `examine` command).
  The main loop credits its Q1 (line numbers match the WT) and discounts the rest, recording a seat defect (a CONFABULATED
  INSTRUMENT) on the row's agy entry.  Is that the right disposition, and does any finding credited to another seat rest on
  Argon's agreement?
* **F19 / D1** -- the four docstring changes: is any of them WRONG about the code?  (`ld`/`lwa`/`std` "perform no base update";
  RT = EA "when the access succeeds" -- `cpu_ppc_instr_loadstore.c` returns before the update on a failed access; the flank
  claim scoped to the ordinary `stdu`; the sign x RA joints and reserved corners "not floor cells".)
* **F17** -- the L10 loads session stops at the RA-zero `lwa` word (XO 2, pc=0x10060), L9a's at the RA-zero `ld` (pc=0x10064);
  SCORES's per-leg lines are right and its SUMMARY line is corrected by addendum.  Right?
* **F7** -- PRETABLE's per-row "kills" lists are recorded as incomplete PREDICTIONS, never the kill map, and PRETABLE stays
  unedited (its mtime is the order proof).  Is "carried erratum, never edit" the right form, or does the carrier's L4 demand
  the correction IN PRETABLE itself?
* **The chain** -- the carrier says a repair made in response to a pass 2 owes its own pass 2, closing on the first VALID pass that
  finds zero floor breaches, with its denominator.  This packet is that pass for the two repair diffs above.  Denominator:
  the docstring/comment diff (five hunks), the gate comment/title diff (two hunks), and the three re-measured runs.

## 5. THE THREE QUESTIONS (answer in this order; VERDICT line first: `VERDICT: UPHOLD | AMEND | OVERTURN -- <one sentence>`)

1. Adjudicate F1-F28 and D1-D2 of `..\PASS2_RULINGS.md`: UPHOLD / OVERTURN / REFINE / CANNOT SETTLE, one line each with a
   reason; group the unanimous records items (F3-F6, F8-F14, F24) if you uphold them all.
2. **WHICH OF THE MAIN LOOP'S ACCEPTED DISPOSITIONS IS WRONG?**  Twenty-six of twenty-eight were accepted or refined; name the
   count you think is actually wrong and which.
3. **WHAT DID ALL SEVEN ANSWERS MISS?**  You now have the whole panel's output and the repairs.  In particular: does the
   docstring-only revision change any observable the gate or the kill table reads (it must not); is the chain CLOSED by this
   pass (zero floor breaches, denominator stated), or does something owe another pass; and is anything in the CHANGELOG /
   commit / OUTSTANDING_BUGS drafts (brief section 9, plus the pass-2 corrections listed in section 2 above) still a wrong
   record?

End with one line: `LANDING: GO | GO WITH THE CHANGES NAMED ABOVE | HOLD -- <reason>`.
