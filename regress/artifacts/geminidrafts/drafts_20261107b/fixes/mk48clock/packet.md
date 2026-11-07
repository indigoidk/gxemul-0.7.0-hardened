# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `mk48clock` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `mk48clock`, state `open`)

**title:** devices/dev_mk48txx.c -- the time-of-day registers refresh only at init and on a READ 0-to-1 transition -- WRONG-RESULT (clock does not run)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T88 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A7-48).  Source URLs: https://github.com/ajfa/mvme187-sysv88-gxemul/commit/4a01173afc4beafabbd61ca385bd158d07d4a415.  Our site at de8c7547: src/devices/dev_mk48txx.c:165, :129-135.  Portable fix: yes -- port ajfa mvme187 4a01173 patch 06 (NVRAM file backing is a feature).  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/devices/dev_mk48txx.c` -- AT HEAD, lines 76-155 (`*` marks a line your previous draft changed)

```c
   76|  DEVICE_ACCESS(mk48txx)
   77|  {
   78|  	struct mk48txx_data *d = (struct mk48txx_data *) extra;
   79|  	uint64_t idata = 0, odata = 0;
   80|  
   81|  	if (writeflag == MEM_WRITE)
   82|  		idata = memory_readmax64(cpu, data, len);
   83|  
   84|  	if (writeflag == MEM_READ)
   85|  		odata = d->reg[relative_addr];
   86|  
   87|  	/*  #521 (mk48nvramkill): the lower bound was MK48T08_CLKOFF, i.e. 0x1ff0,
   88|  	    and it was missing its `+ MK48TXX_ICSR'.  The switch below holds exactly
   89|  	    ONE case, MK48T08_CLKOFF + MK48TXX_ICSR (0x1ff8), so the eight offsets
   90|  	    0x1ff0..0x1ff7 fell through it to a `default:' that calls exit(1) --
   91|  	    EIGHT bytes inside the device's own 8192-byte registration ending the
   92|  	    emulator process on an ordinary access.  MEASURED at rung 3 BEFORE this
   93|  	    edit, on unmodified `-E mvme88k -e mvme187':
   94|  	        artifacts/mk48nvramkill/opus_mk48_nvram_witness_20260910.py
   95|  	        artifacts/mk48nvramkill/opus_witness_run_20260910.txt  -- 15/47,
   96|  	            all 15 controls green and all 32 kill rows red.
   97|  	    THE POPULATION IS SIXTEEN CELLS, NOT EIGHT: every offset kills in BOTH
   98|  	    directions, ld.bu and st.b alike, and all sixteen were driven.  The kill
   99|  	    is WIDTH-INDEPENDENT -- `len' never enters the guard, so ld / ld.h /
  100|  	    ld.bu all die at the same start offset and there is no width axis here.
  101|  
  102|  	    THOSE EIGHT ARE ORDINARY NVRAM ON THIS PART, which is what licenses
  103|  	    accepting them rather than declining.  mk48txxreg.h says the first bank
  104|  	    of eight registers at (nvramsz - 16) -- exactly 0x1ff0 -- is "available
  105|  	    only on more recent MK48Txx models", and names them IFLAGS, IASEC,
  106|  	    IAMIN, IAHOUR, IADAY, IINTR, IWDOG.  They are the MK48T59's alarm and
  107|  	    watchdog bank; this file implements the MK48T08 alone, where the region
  108|  	    is plain non-volatile RAM.  Storage already existed -- `reg' is
  109|  	    MK48TXX_LEN bytes -- so this is a BOUNDARY CORRECTION, not new policy,
  110|  	    and no vendored constant is wrong.
  111|  
  112|  	    The upper bound stays at MK48TXX_ISEC deliberately: it routes the
  113|  	    time-of-day registers to this same path, which is correct because
  114|  	    mk48txx_update_regs() writes into this very array, and moving it would
  115|  	    be a different change.  */
  116|  	if (relative_addr < MK48T08_CLKOFF + MK48TXX_ICSR ||
  117|  	    relative_addr >= MK48T08_CLKOFF + MK48TXX_ISEC) {
  118|  		/*  Reads and writes to the RAM part of the mk48txx, or
  119|  		    the clock registers, are OK:  */
  120|  		if (writeflag == MEM_WRITE)
  121|  			d->reg[relative_addr] = idata;
  122|  		goto ret;
  123|  	}
  124|  
  125|  	switch (relative_addr) {
  126|  
  127|  	case MK48T08_CLKOFF + MK48TXX_ICSR:
  128|  		if (writeflag == MEM_WRITE) {
  129|  			if ((idata & MK48TXX_CSR_READ) &&
  130|  			    !(d->reg[relative_addr] & MK48TXX_CSR_READ)) {
  131|  				/*  Switching the read bit from 0 to 1 causes
  132|  				    registers to be "froozen". In the emulator,
  133|  				    simply updating them with data from the
  134|  				    host should be good enough.  */
  135|  				mk48txx_update_regs(d);
  136|  			}
  137|  			d->reg[relative_addr] = idata;
  138|  		}
  139|  		break;
  140|  
  141|  	default:if (writeflag == MEM_READ)
  142|  			fatal("[ mk48txx: unimplemented READ from offset 0x%x ]"
  143|  			    "\n", (int)relative_addr);
  144|  		else
  145|  			fatal("[ mk48txx: unimplemented WRITE to offset 0x%x: "
  146|  			    "0x%x ]\n", (int)relative_addr, (int)idata);
  147|  		exit(1);
  148|  	}
  149|  
  150|  ret:
  151|* 	if (writeflag == MEM_READ)
  152|* 		memory_writemax64(cpu, data, len, odata);
  153|* 
  154|  	return 1;
  155|  }
```

## The data structures those files define (every field that exists)

### `src/devices/dev_mk48txx.c` -- `struct mk48txx_data {` (HEAD lines 53-55)

```c
   53| struct mk48txx_data {
   54| 	uint8_t		reg[MK48TXX_LEN];
   55| };
```


## Your previous draft's edits

```json
[
  {
    "file": "src/devices/dev_mk48txx.c",
    "old": "ret:\n\tif (writeflag == MEM_READ)\n\t\tmemory_writemax64(cpu, data, len, odata);",
    "new": "ret:\n\tif (writeflag == MEM_READ) {\n\t\tif (!(d->reg[MK48T08_CLKOFF + MK48TXX_ICSR] & MK48TXX_CSR_READ)) {\n\t\t\tmk48txx_update_regs(d);\n\t\t\todata = d->reg[relative_addr];\n\t\t}\n\t\tmemory_writemax64(cpu, data, len, odata);\n\t}",
    "why": "Update the clock registers on any read if they are not frozen by the READ bit, so the clock runs continuously."
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_MK48CLOCK: DEFECT, 1 FINDINGS
1. Does the diff remove the defect the issue describes, at every site the issue names? Name any site it misses.
Yes, the diff dynamically updates the clock registers on every read when the freeze bit is not set, addressing the "clock does not run" WRONG-RESULT defect. It misses no named sites (the explicit 0-to-1 freeze transition logic at line 131 is safely preserved).
2. CONTROL FLOW: does any added return, goto, break or early exit skip code the function would otherwise run?
No. The fix adds no jumps, returns, or breaks. It strictly wraps the existing common tail execution and still always reaches `memory_writemax64`.
3. RETURN VALUE: does any path now return something different? Say what the shown code implies the value means.
No. The return value remains `1` on all paths, which implies that the memory access was successfully handled by the device emulator.
4. What ELSE does the diff change -- state left set or cleared, a value the guest can now see, a message on a path that did not print one?
The fix triggers a full time-of-day register recalculation (`mk48txx_update_regs`) and a re-fetch of `odata` on EVERY single read access to the entire NVRAM device (any `relative_addr`), rather than strictly isolating this work to reads targeting the clock registers region. 
5. House idioms (low severity): a diagnostic a guest can trigger repeatedly should print ONCE per device instance (a latch field) with (once) in the message; a new comment carries a /* #NNN: ... */ tag; lines stay within 79 columns.
The added code introduces new behavioral logic without including the required house idiom comment tag identifying the issue.
src/devices/dev_mk48txx.c:151 STYLE missing house idiom tag; fix: `/* #mk48clock: refresh registers if clock runs */`
```

## WHAT TO RETURN

1. For EACH review finding, one line: `ACCEPT` or `REJECT`, and why, citing the code shown.  A suggestion that uses a
   function, macro or field that appears nowhere in this packet does not exist in HEAD: reject it or replace it with an
   idiom the packet shows.
2. One line: `STILL PRESENT: YES|NO|UNSETTLED -- <the line of code that shows it>`.
3. If YES: EXACTLY ONE fenced ```json block -- the COMPLETE corrected edit list (not a delta), applying to the HEAD text
   above: [{"file": "src/...", "old": "<exact HEAD text, occurring EXACTLY ONCE in that file>", "new": "<replacement>",
   "why": "<one line>"}].  JSON escapes (\t, \n); tabs stay tabs; lines within 79 columns; a new comment carries
   `/* #NNN: ... */`.  Never an empty list and never comment-only edits for a defect in behaviour.  If every finding is
   rejected, return the previous edits unchanged.
4. After the block: what the fix deliberately does not change.

End with two lines: `REVISION_MK48CLOCK: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_MK48CLOCK: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
