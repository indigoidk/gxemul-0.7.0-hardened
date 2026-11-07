# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `dec5800ncpushift` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `dec5800ncpushift`, state `open`)

**title:** src/devices/dev_dec5800.c:359-367 -- (1 << ncpus) - 1 is undefined for 31 or more CPUs, which -n allows (up to 256) -- WRONG-RESULT (host -n option)

**state_note (head):** 

**The drafter's own reading:** STILL PRESENT: YES -- `odata = (1 << cpu->machine->ncpus) - 1;`

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_dec5800.c b/src/devices/dev_dec5800.c
index 3a43ef9c..0b0446a3 100644
--- a/src/devices/dev_dec5800.c
+++ b/src/devices/dev_dec5800.c
@@ -357,12 +357,12 @@ DEVICE_ACCESS(deccca)
 		break;
 	case 20:
 		if (writeflag == MEM_READ)
-			odata = (1 << cpu->machine->ncpus) - 1;
+			odata = cpu->machine->ncpus >= 64 ? ~(uint64_t)0 : (1ULL << cpu->machine->ncpus) - 1;
 			    /*  one bit for each cpu  */
 		break;
 	case 28:
 		if (writeflag == MEM_READ)
-			odata = (1 << cpu->machine->ncpus) - 1;
+			odata = cpu->machine->ncpus >= 64 ? ~(uint64_t)0 : (1ULL << cpu->machine->ncpus) - 1;
 			    /*  one bit for each enabled(?) cpu  */
 		break;
 	default:
```

## Every edited function, after the fix

### `src/devices/dev_dec5800.c` -- post-edit lines 339-382 (`+` marks a line the diff added or the point of a deletion)

```c
  339|  DEVICE_ACCESS(deccca)
  340|  {
  341|  	uint64_t idata = 0, odata = 0;
  342|  	/*  struct deccca_data *d = extra;  */
  343|  
  344|  	if (writeflag == MEM_WRITE)
  345|  		idata = memory_readmax64(cpu, data, len);
  346|  
  347|  	switch (relative_addr) {
  348|  	case 6:
  349|  	case 7:
  350|  		/*  CCA "ID" bytes? These must be here, or Ultrix complains.  */
  351|  		if (writeflag == MEM_READ)
  352|  			odata = 67;
  353|  		break;
  354|  	case 8:
  355|  		if (writeflag == MEM_READ)
  356|  			odata = cpu->machine->ncpus;
  357|  		break;
  358|  	case 20:
  359|  		if (writeflag == MEM_READ)
  360|+ 			odata = cpu->machine->ncpus >= 64 ? ~(uint64_t)0 : (1ULL << cpu->machine->ncpus) - 1;
  361|  			    /*  one bit for each cpu  */
  362|  		break;
  363|  	case 28:
  364|  		if (writeflag == MEM_READ)
  365|+ 			odata = cpu->machine->ncpus >= 64 ? ~(uint64_t)0 : (1ULL << cpu->machine->ncpus) - 1;
  366|  			    /*  one bit for each enabled(?) cpu  */
  367|  		break;
  368|  	default:
  369|  		if (writeflag==MEM_READ) {
  370|  			debug("[ deccca: read from 0x%08lx ]\n",
  371|  			    (long)relative_addr);
  372|  		} else {
  373|  			debug("[ deccca: write to  0x%08lx: 0x%08x ]\n",
  374|  			    (long)relative_addr, (int)idata);
  375|  		}
  376|  	}
  377|  
  378|  	if (writeflag == MEM_READ)
  379|  		memory_writemax64(cpu, data, len, odata);
  380|  
  381|  	return 1;
  382|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_DEC5800NCPUSHIFT: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_DEC5800NCPUSHIFT: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
