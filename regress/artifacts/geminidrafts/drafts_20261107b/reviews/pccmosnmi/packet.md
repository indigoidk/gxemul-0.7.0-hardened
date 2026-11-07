# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `pccmosnmi` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `pccmosnmi`, state `open`)

**title:** devices/dev_pccmos.c:DEVICE_ACCESS index port -- the index is stored without masking bit 7 (NMI disable), so such a guest misses RTC registers 0x00-0x0d -- WRONG-RESULT

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T99 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: one-line; report rows: A5-28).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/bb3294595335d7c2480b7662f2d021d67a6a5436.  Our site at de8c7547: src/devices/dev_pccmos.c:74.  Portable fix: yes -- port the masking of rs6000 bb32945.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- 			d->select = idata;

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_pccmos.c b/src/devices/dev_pccmos.c
index 8de9edf9..135e2cb4 100644
--- a/src/devices/dev_pccmos.c
+++ b/src/devices/dev_pccmos.c
@@ -71,8 +71,9 @@ DEVICE_ACCESS(pccmos)
 
 	if ((relative_addr & 1) == 0) {
 		if (writeflag == MEM_WRITE) {
-			d->select = idata;
-			if (idata <= 0x0d) {
+			/* #99: mask NMI disable bit */
+			b = d->select = idata & 0x7f;
+			if (d->select <= 0x0d) {
 				r = cpu->memory_rw(cpu, cpu->mem,
 				    PCCMOS_MC146818_FAKE_ADDR, &b, 1,
 				    MEM_WRITE, PHYSICAL);
```

## Every edited function, after the fix

### `src/devices/dev_pccmos.c` -- post-edit lines 57-110 (`+` marks a line the diff added or the point of a deletion)

```c
   57|  DEVICE_ACCESS(pccmos)
   58|  {
   59|  	struct pccmos_data *d = (struct pccmos_data *) extra;
   60|  	uint64_t idata = 0, odata = 0;
   61|  	unsigned char b = 0;
   62|  	int r = 1;
   63|  
   64|  	if (writeflag == MEM_WRITE)
   65|  		b = idata = memory_readmax64(cpu, data, len);
   66|  
   67|  	/*
   68|  	 *  Accesses to CMOS register 0 .. 0xd are rerouted to the
   69|  	 *  RTC; all other access are treated as CMOS RAM read/writes.
   70|  	 */
   71|  
   72|  	if ((relative_addr & 1) == 0) {
   73|  		if (writeflag == MEM_WRITE) {
   74|+ 			/* #99: mask NMI disable bit */
   75|+ 			b = d->select = idata & 0x7f;
   76|+ 			if (d->select <= 0x0d) {
   77|  				r = cpu->memory_rw(cpu, cpu->mem,
   78|  				    PCCMOS_MC146818_FAKE_ADDR, &b, 1,
   79|  				    MEM_WRITE, PHYSICAL);
   80|  			}
   81|  		} else
   82|  			odata = d->select;
   83|  	} else {
   84|  		if (d->select <= 0x0d) {
   85|  			if (writeflag == MEM_WRITE) {
   86|  				r = cpu->memory_rw(cpu, cpu->mem,
   87|  				    PCCMOS_MC146818_FAKE_ADDR + 1, &b, 1,
   88|  				    MEM_WRITE, PHYSICAL);
   89|  			} else {
   90|  				r = cpu->memory_rw(cpu, cpu->mem,
   91|  				    PCCMOS_MC146818_FAKE_ADDR + 1, &b, 1,
   92|  				    MEM_READ, PHYSICAL);
   93|  				odata = b;
   94|  			}
   95|  		} else {
   96|  			if (writeflag == MEM_WRITE)
   97|  				d->ram[d->select] = idata;
   98|  			else
   99|  				odata = d->ram[d->select];
  100|  		}
  101|  	}
  102|  
  103|  	if (r == 0)
  104|  		fatal("[ pccmos: memory_rw() error! ]\n");
  105|  
  106|  	if (writeflag == MEM_READ)
  107|  		memory_writemax64(cpu, data, len, odata);
  108|  
  109|  	return 1;
  110|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_PCCMOSNMI: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_PCCMOSNMI: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
