# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `ppctlbieseg` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `ppctlbieseg`, state `open`)

**title:** cpus/cpu_ppc_instr.c:X(tlbie) -- invalidates only the exact EA, not the page index in every segment -- WRONG-RESULT

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T41 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A4-21).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/59cc4103f41689f2d4b79626cfda6b9065e6595c, https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/3dafe76542ea0ee67176456cfffbeeeaa98e983c.  Our site at de8c7547: src/cpus/cpu_ppc_instr.c:3930-3935.  Portable fix: yes -- port rs6000 59cc410 (branch-only working form; rs6000 3dafe76).  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- `cpu->invalidate_translation_caches(cpu, reg(ic->arg[0]), INVALIDATE_VADDR);`

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/cpus/cpu_ppc_instr.c b/src/cpus/cpu_ppc_instr.c
index 508e9181..34a0fabb 100644
--- a/src/cpus/cpu_ppc_instr.c
+++ b/src/cpus/cpu_ppc_instr.c
@@ -3943,8 +3943,7 @@ X(tlbia)
 X(tlbie)
 {
 	/*  fatal("[ tlbie ]\n");  */
-	cpu->invalidate_translation_caches(cpu, reg(ic->arg[0]),
-	    INVALIDATE_VADDR);
+	cpu->invalidate_translation_caches(cpu, 0, INVALIDATE_ALL); /* #T41: safely over-invalidate since segment-wise invalidation is unavailable here */
 }
```

## Every edited function, after the fix

### `src/cpus/cpu_ppc_instr.c` -- post-edit lines 3943-3947 (`+` marks a line the diff added or the point of a deletion)

```c
 3943|  X(tlbie)
 3944|  {
 3945|  	/*  fatal("[ tlbie ]\n");  */
 3946|+ 	cpu->invalidate_translation_caches(cpu, 0, INVALIDATE_ALL); /* #T41: safely over-invalidate since segment-wise invalidation is unavailable here */
 3947|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_PPCTLBIESEG: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_PPCTLBIESEG: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
