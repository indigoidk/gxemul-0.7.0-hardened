# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `mk48clock` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `mk48clock`, state `open`)

**title:** devices/dev_mk48txx.c -- the time-of-day registers refresh only at init and on a READ 0-to-1 transition -- WRONG-RESULT (clock does not run)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T88 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A7-48).  Source URLs: https://github.com/ajfa/mvme187-sysv88-gxemul/commit/4a01173afc4beafabbd61ca385bd158d07d4a415.  Our site at de8c7547: src/devices/dev_mk48txx.c:165, :129-135.  Portable fix: yes -- port ajfa mvme187 4a01173 patch 06 (NVRAM file backing is a feature).  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- `src/devices/dev_mk48txx.c:84`

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_mk48txx.c b/src/devices/dev_mk48txx.c
index 16174d78..7f4a038c 100644
--- a/src/devices/dev_mk48txx.c
+++ b/src/devices/dev_mk48txx.c
@@ -81,8 +81,14 @@ DEVICE_ACCESS(mk48txx)
 	if (writeflag == MEM_WRITE)
 		idata = memory_readmax64(cpu, data, len);
 
-	if (writeflag == MEM_READ)
+	if (writeflag == MEM_READ) {
+		/* #mk48clock: refresh registers if clock runs */
+		if (relative_addr >= MK48T08_CLKOFF + MK48TXX_ISEC &&
+		    !(d->reg[MK48T08_CLKOFF + MK48TXX_ICSR] & MK48TXX_CSR_READ)) {
+			mk48txx_update_regs(d);
+		}
 		odata = d->reg[relative_addr];
+	}
 
 	/*  #521 (mk48nvramkill): the lower bound was MK48T08_CLKOFF, i.e. 0x1ff0,
 	    and it was missing its `+ MK48TXX_ICSR'.  The switch below holds exactly
```

## Every edited function, after the fix

### `src/devices/dev_mk48txx.c` -- post-edit lines 76-161 (`+` marks a line the diff added or the point of a deletion)

```c
   76|  DEVICE_ACCESS(mk48txx)
   77|  {
   78|  	struct mk48txx_data *d = (struct mk48txx_data *) extra;
   79|  	uint64_t idata = 0, odata = 0;
   80|  
   81|  	if (writeflag == MEM_WRITE)
   82|  		idata = memory_readmax64(cpu, data, len);
   83|  
   84|+ 	if (writeflag == MEM_READ) {
   85|+ 		/* #mk48clock: refresh registers if clock runs */
   86|+ 		if (relative_addr >= MK48T08_CLKOFF + MK48TXX_ISEC &&
   87|+ 		    !(d->reg[MK48T08_CLKOFF + MK48TXX_ICSR] & MK48TXX_CSR_READ)) {
   88|+ 			mk48txx_update_regs(d);
   89|+ 		}
   90|  		odata = d->reg[relative_addr];
   91|+ 	}
   92|  
   93|  	/*  #521 (mk48nvramkill): the lower bound was MK48T08_CLKOFF, i.e. 0x1ff0,
   94|  	    and it was missing its `+ MK48TXX_ICSR'.  The switch below holds exactly
   95|  	    ONE case, MK48T08_CLKOFF + MK48TXX_ICSR (0x1ff8), so the eight offsets
   96|  	    0x1ff0..0x1ff7 fell through it to a `default:' that calls exit(1) --
   97|  	    EIGHT bytes inside the device's own 8192-byte registration ending the
   98|  	    emulator process on an ordinary access.  MEASURED at rung 3 BEFORE this
   99|  	    edit, on unmodified `-E mvme88k -e mvme187':
  100|  	        artifacts/mk48nvramkill/opus_mk48_nvram_witness_20260910.py
  101|  	        artifacts/mk48nvramkill/opus_witness_run_20260910.txt  -- 15/47,
  102|  	            all 15 controls green and all 32 kill rows red.
  103|  	    THE POPULATION IS SIXTEEN CELLS, NOT EIGHT: every offset kills in BOTH
  104|  	    directions, ld.bu and st.b alike, and all sixteen were driven.  The kill
  105|  	    is WIDTH-INDEPENDENT -- `len' never enters the guard, so ld / ld.h /
  106|  	    ld.bu all die at the same start offset and there is no width axis here.
  107|  
  108|  	    THOSE EIGHT ARE ORDINARY NVRAM ON THIS PART, which is what licenses
  109|  	    accepting them rather than declining.  mk48txxreg.h says the first bank
  110|  	    of eight registers at (nvramsz - 16) -- exactly 0x1ff0 -- is "available
  111|  	    only on more recent MK48Txx models", and names them IFLAGS, IASEC,
  112|  	    IAMIN, IAHOUR, IADAY, IINTR, IWDOG.  They are the MK48T59's alarm and
  113|  	    watchdog bank; this file implements the MK48T08 alone, where the region
  114|  	    is plain non-volatile RAM.  Storage already existed -- `reg' is
  115|  	    MK48TXX_LEN bytes -- so this is a BOUNDARY CORRECTION, not new policy,
  116|  	    and no vendored constant is wrong.
  117|  
  118|  	    The upper bound stays at MK48TXX_ISEC deliberately: it routes the
  119|  	    time-of-day registers to this same path, which is correct because
  120|  	    mk48txx_update_regs() writes into this very array, and moving it would
  121|  	    be a different change.  */
  122|  	if (relative_addr < MK48T08_CLKOFF + MK48TXX_ICSR ||
  123|  	    relative_addr >= MK48T08_CLKOFF + MK48TXX_ISEC) {
  124|  		/*  Reads and writes to the RAM part of the mk48txx, or
  125|  		    the clock registers, are OK:  */
  126|  		if (writeflag == MEM_WRITE)
  127|  			d->reg[relative_addr] = idata;
  128|  		goto ret;
  129|  	}
  130|  
  131|  	switch (relative_addr) {
  132|  
  133|  	case MK48T08_CLKOFF + MK48TXX_ICSR:
  134|  		if (writeflag == MEM_WRITE) {
  135|  			if ((idata & MK48TXX_CSR_READ) &&
  136|  			    !(d->reg[relative_addr] & MK48TXX_CSR_READ)) {
  137|  				/*  Switching the read bit from 0 to 1 causes
  138|  				    registers to be "froozen". In the emulator,
  139|  				    simply updating them with data from the
  140|  				    host should be good enough.  */
  141|  				mk48txx_update_regs(d);
  142|  			}
  143|  			d->reg[relative_addr] = idata;
  144|  		}
  145|  		break;
  146|  
  147|  	default:if (writeflag == MEM_READ)
  148|  			fatal("[ mk48txx: unimplemented READ from offset 0x%x ]"
  149|  			    "\n", (int)relative_addr);
  150|  		else
  151|  			fatal("[ mk48txx: unimplemented WRITE to offset 0x%x: "
  152|  			    "0x%x ]\n", (int)relative_addr, (int)idata);
  153|  		exit(1);
  154|  	}
  155|  
  156|  ret:
  157|  	if (writeflag == MEM_READ)
  158|  		memory_writemax64(cpu, data, len, odata);
  159|  
  160|  	return 1;
  161|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_MK48CLOCK: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_MK48CLOCK: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
