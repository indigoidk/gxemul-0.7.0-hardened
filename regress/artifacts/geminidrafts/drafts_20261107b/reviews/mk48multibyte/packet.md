# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `mk48multibyte` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `mk48multibyte`, state `open`)

**title:** devices/dev_mk48txx.c access -- multi-byte NVRAM accesses read or write a single byte -- WRONG-RESULT (187Bug checksums)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T87 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A7-47).  Source URLs: https://github.com/ajfa/mvme187-sysv88-gxemul/commit/4a01173afc4beafabbd61ca385bd158d07d4a415.  Our site at de8c7547: src/devices/dev_mk48txx.c:84-85, :121.  Portable fix: yes -- port ajfa mvme187 4a01173 patch 06.  Filing check (TRIAGE.md): `mk48nvramkill`, closed, was the 0x1ff0-0x1ff7 exit.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- src/devices/dev_mk48txx.c:84-85 and 120-121

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_mk48txx.c b/src/devices/dev_mk48txx.c
index 16174d78..0a6b1ebd 100644
--- a/src/devices/dev_mk48txx.c
+++ b/src/devices/dev_mk48txx.c
@@ -81,8 +81,9 @@ DEVICE_ACCESS(mk48txx)
 	if (writeflag == MEM_WRITE)
 		idata = memory_readmax64(cpu, data, len);
 
+	/* #mk48multibyte: read wide accesses fully from NVRAM */
 	if (writeflag == MEM_READ)
-		odata = d->reg[relative_addr];
+		odata = memory_readmax64(cpu, &d->reg[relative_addr], len);
 
 	/*  #521 (mk48nvramkill): the lower bound was MK48T08_CLKOFF, i.e. 0x1ff0,
 	    and it was missing its `+ MK48TXX_ICSR'.  The switch below holds exactly
@@ -118,7 +119,7 @@ DEVICE_ACCESS(mk48txx)
 		/*  Reads and writes to the RAM part of the mk48txx, or
 		    the clock registers, are OK:  */
 		if (writeflag == MEM_WRITE)
-			d->reg[relative_addr] = idata;
+			memory_writemax64(cpu, &d->reg[relative_addr], len, idata);
 		goto ret;
 	}
```

## Every edited function, after the fix

### `src/devices/dev_mk48txx.c` -- post-edit lines 76-156 (`+` marks a line the diff added or the point of a deletion)

```c
   76|  DEVICE_ACCESS(mk48txx)
   77|  {
   78|  	struct mk48txx_data *d = (struct mk48txx_data *) extra;
   79|  	uint64_t idata = 0, odata = 0;
   80|  
   81|  	if (writeflag == MEM_WRITE)
   82|  		idata = memory_readmax64(cpu, data, len);
   83|  
   84|+ 	/* #mk48multibyte: read wide accesses fully from NVRAM */
   85|  	if (writeflag == MEM_READ)
   86|+ 		odata = memory_readmax64(cpu, &d->reg[relative_addr], len);
   87|  
   88|  	/*  #521 (mk48nvramkill): the lower bound was MK48T08_CLKOFF, i.e. 0x1ff0,
   89|  	    and it was missing its `+ MK48TXX_ICSR'.  The switch below holds exactly
   90|  	    ONE case, MK48T08_CLKOFF + MK48TXX_ICSR (0x1ff8), so the eight offsets
   91|  	    0x1ff0..0x1ff7 fell through it to a `default:' that calls exit(1) --
   92|  	    EIGHT bytes inside the device's own 8192-byte registration ending the
   93|  	    emulator process on an ordinary access.  MEASURED at rung 3 BEFORE this
   94|  	    edit, on unmodified `-E mvme88k -e mvme187':
   95|  	        artifacts/mk48nvramkill/opus_mk48_nvram_witness_20260910.py
   96|  	        artifacts/mk48nvramkill/opus_witness_run_20260910.txt  -- 15/47,
   97|  	            all 15 controls green and all 32 kill rows red.
   98|  	    THE POPULATION IS SIXTEEN CELLS, NOT EIGHT: every offset kills in BOTH
   99|  	    directions, ld.bu and st.b alike, and all sixteen were driven.  The kill
  100|  	    is WIDTH-INDEPENDENT -- `len' never enters the guard, so ld / ld.h /
  101|  	    ld.bu all die at the same start offset and there is no width axis here.
  102|  
  103|  	    THOSE EIGHT ARE ORDINARY NVRAM ON THIS PART, which is what licenses
  104|  	    accepting them rather than declining.  mk48txxreg.h says the first bank
  105|  	    of eight registers at (nvramsz - 16) -- exactly 0x1ff0 -- is "available
  106|  	    only on more recent MK48Txx models", and names them IFLAGS, IASEC,
  107|  	    IAMIN, IAHOUR, IADAY, IINTR, IWDOG.  They are the MK48T59's alarm and
  108|  	    watchdog bank; this file implements the MK48T08 alone, where the region
  109|  	    is plain non-volatile RAM.  Storage already existed -- `reg' is
  110|  	    MK48TXX_LEN bytes -- so this is a BOUNDARY CORRECTION, not new policy,
  111|  	    and no vendored constant is wrong.
  112|  
  113|  	    The upper bound stays at MK48TXX_ISEC deliberately: it routes the
  114|  	    time-of-day registers to this same path, which is correct because
  115|  	    mk48txx_update_regs() writes into this very array, and moving it would
  116|  	    be a different change.  */
  117|  	if (relative_addr < MK48T08_CLKOFF + MK48TXX_ICSR ||
  118|  	    relative_addr >= MK48T08_CLKOFF + MK48TXX_ISEC) {
  119|  		/*  Reads and writes to the RAM part of the mk48txx, or
  120|  		    the clock registers, are OK:  */
  121|  		if (writeflag == MEM_WRITE)
  122|+ 			memory_writemax64(cpu, &d->reg[relative_addr], len, idata);
  123|  		goto ret;
  124|  	}
  125|  
  126|  	switch (relative_addr) {
  127|  
  128|  	case MK48T08_CLKOFF + MK48TXX_ICSR:
  129|  		if (writeflag == MEM_WRITE) {
  130|  			if ((idata & MK48TXX_CSR_READ) &&
  131|  			    !(d->reg[relative_addr] & MK48TXX_CSR_READ)) {
  132|  				/*  Switching the read bit from 0 to 1 causes
  133|  				    registers to be "froozen". In the emulator,
  134|  				    simply updating them with data from the
  135|  				    host should be good enough.  */
  136|  				mk48txx_update_regs(d);
  137|  			}
  138|  			d->reg[relative_addr] = idata;
  139|  		}
  140|  		break;
  141|  
  142|  	default:if (writeflag == MEM_READ)
  143|  			fatal("[ mk48txx: unimplemented READ from offset 0x%x ]"
  144|  			    "\n", (int)relative_addr);
  145|  		else
  146|  			fatal("[ mk48txx: unimplemented WRITE to offset 0x%x: "
  147|  			    "0x%x ]\n", (int)relative_addr, (int)idata);
  148|  		exit(1);
  149|  	}
  150|  
  151|  ret:
  152|  	if (writeflag == MEM_READ)
  153|  		memory_writemax64(cpu, data, len, odata);
  154|  
  155|  	return 1;
  156|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_MK48MULTIBYTE: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_MK48MULTIBYTE: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
