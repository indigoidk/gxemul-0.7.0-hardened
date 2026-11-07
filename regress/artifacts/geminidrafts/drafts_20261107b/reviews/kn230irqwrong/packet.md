# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `kn230irqwrong` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `kn230irqwrong`, state `open`)

**title:** src/devices/dev_kn230.c:72-75,89-92 -- the SII/LANCE condition (assert3) asserts and deasserts mips_irq_2 instead of mips_irq_3, so those interrupts arrive on MIPS interrupt 2 and the deassert can drop line 2 while a DZ or option-slot source is still pending -- WRONG-RESULT (MIPSMATE 5100)

**state_note (head):** 

**The drafter's own reading:** STILL PRESENT: YES -- `src/devices/dev_kn230.c:75` and `src/devices/dev_kn230.c:92`

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_kn230.c b/src/devices/dev_kn230.c
index 6454746c..9ff5296d 100644
--- a/src/devices/dev_kn230.c
+++ b/src/devices/dev_kn230.c
@@ -72,7 +72,7 @@ void kn230_interrupt_assert(struct interrupt *interrupt)
 	if (assert2)
                 INTERRUPT_ASSERT(d->mips_irq_2);
 	if (assert3)
-                INTERRUPT_ASSERT(d->mips_irq_2);
+                INTERRUPT_ASSERT(d->mips_irq_3);
 }
 void kn230_interrupt_deassert(struct interrupt *interrupt)
 {
@@ -89,7 +89,7 @@ void kn230_interrupt_deassert(struct interrupt *interrupt)
 	if (!assert2)
                 INTERRUPT_DEASSERT(d->mips_irq_2);
 	if (!assert3)
-                INTERRUPT_DEASSERT(d->mips_irq_2);
+                INTERRUPT_DEASSERT(d->mips_irq_3);
 }
```

## Every edited function, after the fix

### `src/devices/dev_kn230.c` -- post-edit lines 60-76 (`+` marks a line the diff added or the point of a deletion)

```c
   60|  void kn230_interrupt_assert(struct interrupt *interrupt)
   61|  {
   62|  	struct kn230_data *d = (struct kn230_data *) interrupt->extra;
   63|  	int assert2 = 0, assert3 = 0;
   64|  
   65|  	d->csr |= interrupt->line;
   66|  	if (d->csr & (KN230_CSR_INTR_SII | KN230_CSR_INTR_LANCE))
   67|  		assert3 = 1;
   68|  	if (d->csr & (KN230_CSR_INTR_DZ0 |
   69|  	    KN230_CSR_INTR_OPT0 | KN230_CSR_INTR_OPT1))
   70|  		assert2 = 1;
   71|  
   72|  	if (assert2)
   73|                  INTERRUPT_ASSERT(d->mips_irq_2);
   74|  	if (assert3)
   75|+                 INTERRUPT_ASSERT(d->mips_irq_3);
   76|  }
```

### `src/devices/dev_kn230.c` -- post-edit lines 77-93 (`+` marks a line the diff added or the point of a deletion)

```c
   77|  void kn230_interrupt_deassert(struct interrupt *interrupt)
   78|  {
   79|  	struct kn230_data *d = (struct kn230_data *) interrupt->extra;
   80|  	int assert2 = 0, assert3 = 0;
   81|  
   82|  	d->csr &= ~interrupt->line;
   83|  	if (d->csr & (KN230_CSR_INTR_SII | KN230_CSR_INTR_LANCE))
   84|  		assert3 = 1;
   85|  	if (d->csr & (KN230_CSR_INTR_DZ0 |
   86|  	    KN230_CSR_INTR_OPT0 | KN230_CSR_INTR_OPT1))
   87|  		assert2 = 1;
   88|  
   89|  	if (!assert2)
   90|                  INTERRUPT_DEASSERT(d->mips_irq_2);
   91|  	if (!assert3)
   92|+                 INTERRUPT_DEASSERT(d->mips_irq_3);
   93|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_KN230IRQWRONG: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_KN230IRQWRONG: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
