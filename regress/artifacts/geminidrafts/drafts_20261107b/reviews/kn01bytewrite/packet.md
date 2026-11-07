# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `kn01bytewrite` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `kn01bytewrite`, state `open`)

**title:** src/devices/dev_kn01.c:89-101 -- a CSR read that is not two bytes wide only prints a message and then writes data[0] and data[1], so a byte load writes one byte past the caller's one-byte stack buffer -- OOB-WRITE (DECstation 3100)

**state_note (head):** 

**The drafter's own reading:** STILL PRESENT: YES -- src/devices/dev_kn01.c:89-102

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_kn01.c b/src/devices/dev_kn01.c
index 355bf2ab..5a78b212 100644
--- a/src/devices/dev_kn01.c
+++ b/src/devices/dev_kn01.c
@@ -89,6 +89,7 @@ DEVICE_ACCESS(kn01)
 	if (len != 2 || relative_addr != 0) {
 		fatal("[ kn01: trying to read something which is not "
 		    "the first half-word of the csr ]");
+		return 0;
 	}
 
 	csr = d->csr;
```

## Every edited function, after the fix

### `src/devices/dev_kn01.c` -- post-edit lines 78-106 (`+` marks a line the diff added or the point of a deletion)

```c
   78|  DEVICE_ACCESS(kn01)
   79|  {
   80|  	struct kn01_data *d = (struct kn01_data *) extra;
   81|  	int csr;
   82|  
   83|  	if (writeflag == MEM_WRITE) {
   84|  		/*  TODO  */
   85|  		return 1;
   86|  	}
   87|  
   88|  	/*  Read:  */
   89|  	if (len != 2 || relative_addr != 0) {
   90|  		fatal("[ kn01: trying to read something which is not "
   91|  		    "the first half-word of the csr ]");
   92|+ 		return 0;
   93|  	}
   94|  
   95|  	csr = d->csr;
   96|  
   97|  	if (cpu->byte_order == EMUL_LITTLE_ENDIAN) {
   98|  		data[0] = csr & 0xff;
   99|  		data[1] = (csr >> 8) & 0xff;
  100|  	} else {
  101|  		data[1] = csr & 0xff;
  102|  		data[0] = (csr >> 8) & 0xff;
  103|  	}
  104|  
  105|  	return 1;
  106|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_KN01BYTEWRITE: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_KN01BYTEWRITE: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
