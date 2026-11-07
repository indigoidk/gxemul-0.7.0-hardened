# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `pcicfgaddrlow` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `pcicfgaddrlow`, state `open`)

**title:** devices/bus_pci.c:bus_pci_decompose_1 -- CONFIG_ADDRESS keeps bits 1:0 in the register number and every unaligned select prints an unlatched `fatal()` -- WRONG-RESULT

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T100 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: one-line; report rows: A5-30).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/eb4c571747357b394ec15fc2b9f9a31efb999ef5.  Our site at de8c7547: src/devices/bus_pci.c:77-82.  Portable fix: yes -- port rs6000 eb4c571.  Filing check (TRIAGE.md): `pciaddrreadclobber` is a different 0xcf8 defect.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- src/devices/bus_pci.c:77

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/bus_pci.c b/src/devices/bus_pci.c
index b54e7692..09e00e70 100644
--- a/src/devices/bus_pci.c
+++ b/src/devices/bus_pci.c
@@ -74,12 +74,7 @@ void bus_pci_decompose_1(uint32_t t, int *bus, int *dev, int *func, int *reg)
 	*bus  = (t >> 16) & 0xff;
 	*dev  = (t >> 11) & 0x1f;
 	*func = (t >>  8) &  0x7;
-	*reg  =  t        & 0xff;
-
-	/*  Warn about unaligned register access:  */
-	if (t & 3)
-		fatal("[ bus_pci_decompose_1: WARNING: reg = 0x%02x ]\n",
-		    t & 0xff);
+	*reg  =  t        & 0xfc;
 }
```

## Every edited function, after the fix

### `src/devices/bus_pci.c` -- post-edit lines 72-78 (`+` marks a line the diff added or the point of a deletion)

```c
   72|  void bus_pci_decompose_1(uint32_t t, int *bus, int *dev, int *func, int *reg)
   73|  {
   74|  	*bus  = (t >> 16) & 0xff;
   75|  	*dev  = (t >> 11) & 0x1f;
   76|  	*func = (t >>  8) &  0x7;
   77|+ 	*reg  =  t        & 0xfc;
   78|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_PCICFGADDRLOW: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_PCICFGADDRLOW: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
