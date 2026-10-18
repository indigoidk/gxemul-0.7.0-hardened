**Your token: `ASTRA_CLOSE526B_20261018`** -- open your answer with it.

# `xscaleinten`'s closure -- confirm the three in-place corrections

Your closure check (`codex_close526.txt` beside this file) and Grok's (`grok_close526.txt`) each found the same three wrong
records.  They are corrected IN PLACE in the closure commit, beside the sentences they correct.  Confirm the wording.
The tree is `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC`; the corrections are NOT yet in its files.  READ-ONLY.

## 1. The ledger note (`tools/pipeline/ledger.json`, row `xscaleinten`), the sentence and its correction

FAULT is unavailable here in any case: memory_rw.c delivers a failed-device exception for MIPS and M88K only, and this is ARM.  [CORRECTED 2026-10-18 at the row's closure (the closure checks of GPT-6 Astra and Grok 4.7, regress/artifacts/xscaleinten/close_20261018/, each finding it independently; verified at source): wrong, and reasoned from the wrong mechanism -- the bug file retracted its own copy of this sentence on 2026-09-11.  A coprocessor register transfer is not a device access and never reaches memory_rw.c, and ARM does deliver undefined-instruction exceptions: `arm_cdp()` in src/cpus/cpu_arm.c raises `ARM_EXCEPTION_UND`.  ACCEPT stands on its own warrant -- the read is implemented and is not ignored.]

## 2. The bug file's two notes (diff against HEAD)

```diff
--- a/OUTSTANDING_BUGS.md
+++ b/OUTSTANDING_BUGS.md
@@ -18756,8 +18756,14 @@
 the author hit the exit he happened to reach while developing and not the sibling he did not. *That is a
 far stronger warrant than "it is a host kill", and it is one grep away* -- which is exactly what the
 option-set rule's sibling check is for.
 
+*[CORRECTED 2026-10-18 at the row's closure (the closure checks of GPT-6 Astra and Grok 4.7,
+regress/artifacts/xscaleinten/close_20261018/, each finding it independently; verified at source): `case 4:`'s STORE
+arm is not quiet -- a nonzero store calls `fatal()` and `exit(1)` (the `i80321_isteer` store in
+src/cpus/cpu_arm_coproc.c).  Only its LOAD arm is quiet, and the load arm is the sibling this warrant needs; the
+ledger's copy already draws that line.]*
+
 Reachability is explicit rather than inferred: `machine_iq80321.c` installs it with
 `cpu->cd.arm.coproc[6] = arm_coproc_i80321_6;`, and Iyonix does the same. Emulated firmware reading its
 own interrupt-enable register is the natural consumer, and the generic coprocessor dispatcher enforces no
 supervisor-only precondition.
@@ -19328,8 +19334,14 @@
 *** I had guessed that nothing in `regress/` drives a coprocessor transfer. FIVE probes already execute
 CP15 MRC/MCR on `cats`, *** and `footbridge_sites_probe.py` is the directly reusable pattern -- plant
 instructions in RAM, set the pc, step, inspect registers -- pointed at IQ80321 instead. **No machine or
 device addition is required**, which is what the witness ladder demands.
+
+*[CORRECTED 2026-10-18 at the row's closure (the closure checks of GPT-6 Astra and Grok 4.7,
+regress/artifacts/xscaleinten/close_20261018/, each finding it independently; verified at source): four of the five
+run on `cats` (`footbridge_sites_probe.py`, `fbpending_witness.py`, `fbpending_drain_probe.py`,
+`pit8253_latch_probe.py`); the fifth, gate 14's `arm_flags_probe.py`, runs on `testarm` -- as the ledger's copy of
+this sentence says.]*
 
 **An oracle trap that applies well beyond this row: a printed step disassembly does NOT prove the
 instruction executed, or even that its condition passed** -- the engine prints the disassembly *before*
 executing it. Any probe treating a stepped disassembly line as evidence of execution is asserting
```

## Questions

**Q1.**  Is each correction TRUE against the source and the records -- `src/cpus/cpu_arm_coproc.c` (the `i80321_isteer`
store), `src/cpus/cpu_arm.c` (`arm_cdp()`), the four probes' machines, OUTSTANDING_BUGS.md's 2026-09-11 retraction?
**Q2.**  Does each sit beside the sentence it corrects, and say no more than the evidence shows?

**Format:** the token, then ONE line `VERDICT: <n> flags -- <one line>`, then Q1, Q2.  Every defect a line starting `FLAG:`.
