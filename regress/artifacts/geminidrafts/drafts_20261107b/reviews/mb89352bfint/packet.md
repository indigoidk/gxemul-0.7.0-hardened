# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `mb89352bfint` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `mb89352bfint`, state `open`)

**title:** devices/dev_mb89352.c -- the BUS FREE interrupt (PCTL_BFINT_ENAB) is a TODO -- WRONG-RESULT

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T90 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A1-27, C U9(a)).  Source URLs: https://github.com/retroprom/gxemul/commit/a1cafe7c.  Our site at de8c7547: src/devices/dev_mb89352.c:107.  Portable fix: yes -- port upstream a1cafe7c.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- 107

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_mb89352.c b/src/devices/dev_mb89352.c
index 179a47a2..a6d9247f 100644
--- a/src/devices/dev_mb89352.c
+++ b/src/devices/dev_mb89352.c
@@ -104,7 +104,8 @@ static void reassert_interrupts(struct mb89352_data *d)
 {
 	bool assert = d->reg[INTS] != 0;
 
-	// TODO: BUS FREE interrupt enable: PCTL_BFINT_ENAB
+	if ((d->reg[PCTL] & PCTL_BFINT_ENAB) && (d->phase == PH_BUS_FREE))
+		assert = true;
 
 	if (!(d->reg[SCTL] & SCTL_INTR_ENAB))
 		assert = false;
```

## Every edited function, after the fix

### `src/devices/dev_mb89352.c` -- post-edit lines 103-121 (`+` marks a line the diff added or the point of a deletion)

```c
  103|  static void reassert_interrupts(struct mb89352_data *d)
  104|  {
  105|  	bool assert = d->reg[INTS] != 0;
  106|  
  107|+ 	if ((d->reg[PCTL] & PCTL_BFINT_ENAB) && (d->phase == PH_BUS_FREE))
  108|+ 		assert = true;
  109|  
  110|  	if (!(d->reg[SCTL] & SCTL_INTR_ENAB))
  111|  		assert = false;
  112|  	if (d->reg[SCTL] & SCTL_DISABLE)
  113|  		assert = false;
  114|  
  115|  	if (assert && !d->irq_asserted)
  116|  		INTERRUPT_ASSERT(d->irq);
  117|  	else if (!assert && d->irq_asserted)
  118|  		INTERRUPT_DEASSERT(d->irq);
  119|  
  120|  	d->irq_asserted = assert;
  121|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_MB89352BFINT: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_MB89352BFINT: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
