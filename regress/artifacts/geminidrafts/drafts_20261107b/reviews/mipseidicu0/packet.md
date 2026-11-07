# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `mipseidicu0` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `mipseidicu0`, state `open`)

**title:** src/cpus/cpu_mips_instr.c:2719-2726 -- the Release-2 EI/DI handler X(ei_or_di) writes Status.IE with no cop0_availability_check, so user mode gets no Coprocessor Unusable exception -- WRONG-RESULT (user mode, Release-2 CPUs)

**state_note (head):** 

**The drafter's own reading:** STILL PRESENT: YES -- 2719-2726

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/cpus/cpu_mips_instr.c b/src/cpus/cpu_mips_instr.c
index 0df67fd9..075171e0 100644
--- a/src/cpus/cpu_mips_instr.c
+++ b/src/cpus/cpu_mips_instr.c
@@ -2718,6 +2718,9 @@ X(tlbr)
  */
 X(ei_or_di)
 {
+	if (!cop0_availability_check(cpu, ic))
+		return;
+
 	reg(ic->arg[0]) = cpu->cd.mips.coproc[0]->reg[COP0_STATUS];
 	if (ic->arg[1])
 		cpu->cd.mips.coproc[0]->reg[COP0_STATUS] |= STATUS_IE;
```

## Every edited function, after the fix

### `src/cpus/cpu_mips_instr.c` -- post-edit lines 2719-2729 (`+` marks a line the diff added or the point of a deletion)

```c
 2719|  X(ei_or_di)
 2720|  {
 2721|+ 	if (!cop0_availability_check(cpu, ic))
 2722|+ 		return;
 2723|+ 
 2724|  	reg(ic->arg[0]) = cpu->cd.mips.coproc[0]->reg[COP0_STATUS];
 2725|  	if (ic->arg[1])
 2726|  		cpu->cd.mips.coproc[0]->reg[COP0_STATUS] |= STATUS_IE;
 2727|  	else
 2728|  		cpu->cd.mips.coproc[0]->reg[COP0_STATUS] &= ~STATUS_IE;
 2729|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_MIPSEIDICU0: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

1. Does the diff remove the defect the issue describes, at every site the issue names?  Name any site it misses.
2. CONTROL FLOW: does any added `return`, `goto`, `break` or early exit skip code the function would otherwise run -- above
   all its COMMON TAIL (for example, code after a switch that writes a read's result to the guest, then `return 1;`)?
   Quote the tail line it skips.  An edit that skips the tail hands the guest an unwritten result.
3. RETURN VALUE: does any path now return something different?  Say what the shown code implies the value means.
4. What ELSE does the diff change -- state left set or cleared, a value the guest can now see, a message on a path that
   did not print one -- beyond removing the defect?
5. House idioms (low severity): a diagnostic a guest can trigger repeatedly should print ONCE per device instance (a latch
   field) with `(once)` in the message; a new comment carries a `/* #NNN: ... */` tag; lines stay within 79 columns.

Each finding: `file:line` in the POST-EDIT numbering shown above, severity DEFECT / QUESTION / STYLE, and the smallest fix
in ONE line.  When the excerpt does not show what a question needs, say UNSETTLED and name what is missing.

End with one line: `FIXREVIEW_MIPSEIDICU0: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
