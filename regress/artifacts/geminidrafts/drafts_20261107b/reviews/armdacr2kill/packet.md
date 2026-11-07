# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `armdacr2kill` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `armdacr2kill`, state `open`)

**title:** src/cpus/memory_arm.c:78-79: arm_check_access() case 2: fatal(..."1 shouldn't be used"); exit(1).  cpu_arm_coproc.c:203 stores MCR's operand into dacr unfiltered; memory_arm.c:153 derives dav from it -- a guest writing 0b10 into any domain field and touching that domain ends the process.  Architecturally reserved; the fix is one case 2: treated as no-access.  Witness: rung 3, MMU ON, DACR written by a guest mcr.  kimi CLI (:254) and the main loop's follow-up read (:79), fbdeclinefive pass 1; fab [... 7 more characters not shown]

**state_note (head):** 

**The drafter's own reading:** STILL PRESENT: YES -- 78| 	case 2:	fatal("arm_check_access(): 1 shouldn't be used\n");

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/cpus/memory_arm.c b/src/cpus/memory_arm.c
index 679532ee..f65172d3 100644
--- a/src/cpus/memory_arm.c
+++ b/src/cpus/memory_arm.c
@@ -75,8 +75,8 @@ static int arm_check_access(struct cpu *cpu, int ap, int dav, int user)
 		return 0;
 	case 1:	/*  Normal access check.  */
 		break;
-	case 2:	fatal("arm_check_access(): 1 shouldn't be used\n");
-		exit(1);
+	case 2:	/* #armdacr2kill: reserved, treat as no-access */
+		return 0;
 	case 3:	/*  Anything is allowed.  */
 		return 2;
 	}
```

## Every edited function, after the fix

### `src/cpus/memory_arm.c` -- post-edit lines 69-100 (`+` marks a line the diff added or the point of a deletion)

```c
   69|  static int arm_check_access(struct cpu *cpu, int ap, int dav, int user)
   70|  {
   71|  	int s, r;
   72|  
   73|  	switch (dav) {
   74|  	case 0:	/*  No access at all.  */
   75|  		return 0;
   76|  	case 1:	/*  Normal access check.  */
   77|  		break;
   78|+ 	case 2:	/* #armdacr2kill: reserved, treat as no-access */
   79|+ 		return 0;
   80|  	case 3:	/*  Anything is allowed.  */
   81|  		return 2;
   82|  	}
   83|  
   84|  	switch (ap) {
   85|  	case 0:	s = (cpu->cd.arm.control & ARM_CONTROL_S)? 1 : 0;
   86|  		r = (cpu->cd.arm.control & ARM_CONTROL_R)? 2 : 0;
   87|  		switch (s + r) {
   88|  		case 0:	return 0;
   89|  		case 1:	return user? 0 : 1;
   90|  		case 2:	return 1;
   91|  		}
   92|  		fatal("arm_check_access: UNPREDICTABLE s+r value!\n");
   93|  		return 0;
   94|  	case 1:	return user? 0 : 2;
   95|  	case 2:	return user? 1 : 2;
   96|  	}
   97|  
   98|  	/*  "case 3":  */
   99|  	return 2;
  100|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_ARMDACR2KILL: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_ARMDACR2KILL: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
