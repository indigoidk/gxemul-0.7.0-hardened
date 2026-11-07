# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `tcemptyslot` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `tcemptyslot`, state `open`)

**title:** devices/dev_turbochannel.c:DEVICE_ACCESS -- empty-slot reads at 0x3e0-0x4ff return zero with no bus error on every model -- WRONG-RESULT (KN02-BA PROM reports a bad option ROM per empty slot)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T73 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A2-45).  Source URLs: https://github.com/rpajarola/gxemul/commit/042b61b040deedf4c1aafb361a563fdc4f9eedb9.  Our site at de8c7547: src/devices/dev_turbochannel.c:143-149.  Portable fix: yes -- port rpajarola 042b61b.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/devices/dev_turbochannel.c` -- AT HEAD, lines 64-162 (`*` marks a line your previous draft changed)

```c
   64|  DEVICE_ACCESS(turbochannel)
   65|  {
   66|  	struct turbochannel_data *d = (struct turbochannel_data *) extra;
   67|  	uint64_t idata = 0, odata = 0;
   68|  
   69|  	if (writeflag == MEM_WRITE)
   70|  		idata = memory_readmax64(cpu, data, len);
   71|  
   72|  	relative_addr += d->rom_skip;
   73|  
   74|  	if (writeflag == MEM_READ) {
   75|  		debug("[ turbochannel: read from slot %i addr 0x%08lx (",
   76|  		    d->slot_nr, (long)relative_addr);
   77|  
   78|  		relative_addr &= 0x7fff;
   79|  
   80|  		switch (relative_addr) {
   81|  		case 0x3e0:
   82|  			odata = 0x00000001; debug("ROM width");
   83|  			break;
   84|  		case 0x3e4:
   85|  			odata = 0x00000004; debug("ROM stride");
   86|  			break;
   87|  		case 0x3e8:
   88|  			/*  8KB * romsize  */
   89|  			odata = 0x00000001; debug("ROM size");
   90|  			break;
   91|  		case 0x3ec:
   92|  			/*  4MB * slotsize  */
   93|  			odata = 0x00000001; debug("slot size");
   94|  			break;
   95|  		case 0x3f0:
   96|  			odata = 0x55555555; debug("ROM signature byte 0");
   97|  			break;
   98|  		case 0x3f4:
   99|  			odata = 0x00000000; debug("ROM signature byte 1");
  100|  			break;
  101|  		case 0x3f8:
  102|  			odata = 0xaaaaaaaa; debug("ROM signature byte 2");
  103|  			break;
  104|  		case 0x3fc:
  105|  			odata = 0xffffffff; debug("ROM signature byte 3");
  106|  			break;
  107|  		case 0x470:
  108|  			/*  0=nothing, 1=parity  */
  109|  			odata = 0x00000000; debug("flags"); break;
  110|  		default:
  111|  			if (relative_addr >= 0x400 && relative_addr < 0x420)
  112|  				odata = d->card_firmware_version[
  113|  				    (relative_addr-0x400)/4];
  114|  			else if (relative_addr >= 0x420 &&
  115|  			    relative_addr < 0x440)
  116|  				odata = d->card_vendor_name[
  117|  				    (relative_addr-0x420)/4];
  118|  			else if (relative_addr >= 0x440 &&
  119|  			    relative_addr < 0x460)
  120|  				odata = d->card_module_name[
  121|  				    (relative_addr-0x440)/4];
  122|  			else if (relative_addr >= 0x460 &&
  123|  			    relative_addr < 0x470)
  124|  				odata = d->card_firmware_type[
  125|  				    (relative_addr-0x460)/4];
  126|  			else {
  127|  				debug("?");
  128|  			}
  129|  		}
  130|  
  131|  		/*
  132|  		 *  If this slot is empty, return an error so that a DBE
  133|  		 *  exception is caused. (This is the way DECstation operating
  134|  		 *  systems have to detect the absence of cards in a
  135|  		 *  TURBOchannel slot.)
  136|  		 *
  137|  		 *  NOTE:  The Sprite kernel reads from offsets 0x3e0..0x400
  138|  		 *  without handling the DBE exception, and both Ultrix and
  139|  		 *  NetBSD seem to detect the DBE exception using addresses
  140|  		 *  around offset 0x0 or 0x3c0000.  This code seems to work
  141|  		 *  with all of the those OS kernels:
  142|  		 */
  143|  		if (d->card_module_name[0] ==  ' ') {
  144|  			/*  Return no data for empty slot:  */
  145|  			odata = 0;
  146|  
  147|  			/*  Return DBE exception in some cases:  */
  148|* 			if (relative_addr < 0x3e0 || relative_addr >= 0x500)
  149|* 				return 0;
  150|  		}
  151|  
  152|  		debug(") ]\n");
  153|  	} else {
  154|  		debug("[ turbochannel: write to  0x%08lx: 0x%08x ]\n",
  155|  		    (long)relative_addr, (int)idata);
  156|  	}
  157|  
  158|  	if (writeflag == MEM_READ)
  159|  		memory_writemax64(cpu, data, len, odata);
  160|  
  161|  	return 1;
  162|  }
```

## The data structures those files define (every field that exists)

### `src/devices/dev_turbochannel.c` -- `struct turbochannel_data {` (HEAD lines 47-61)

```c
   47| struct turbochannel_data {
   48| 	int		slot_nr;
   49| 	uint64_t	baseaddr;
   50| 	uint64_t	endaddr;
   51| 
   52| 	int		rom_skip;
   53| 
   54| 	char		device_name[DEVICE_MAX_NAMELEN];  /*  NUL-terminated  */
   55| 
   56| 	/*  These should be terminated with spaces  */
   57| 	char		card_firmware_version[CARD_NAME_BUFLEN];
   58| 	char		card_vendor_name[CARD_NAME_BUFLEN];
   59| 	char		card_module_name[CARD_NAME_BUFLEN];
   60| 	char		card_firmware_type[CARD_FIRMWARE_BUFLEN];
   61| };
```

### `src/include/devices.h` -- `struct vfb_data` (HEAD lines 201-239)

```c
  201| struct vfb_data {
  202| 	struct memory	*memory;
  203| 	/*  #157: (Codex/Fable) machine handle, for all-CPU dyntrans
  204| 	    invalidation when the framebuffer is resized  */
  205| 	struct machine	*machine;
  206| 	int		vfb_type;
  207| 
  208| 	int		vfb_scaledown;
  209| 
  210| 	int		xsize;
  211| 	int		ysize;
  212| 	int		bit_depth;
  213| 	int		color32k;	/*  hack for 16-bit HPCmips  */
  214| 	int		psp_15bit;	/*  playstation portable hack  */
  215| 
  216| 	unsigned char	color_plane_mask;
  217| 
  218| 	int		bytes_per_line;		/*  cached  */
  219| 
  220| 	int		visible_xsize;
  221| 	int		visible_ysize;
  222| 
  223| 	size_t		framebuffer_size;
  224| 	int		x11_xsize, x11_ysize;
  225| 
  226| 	int		update_x1, update_y1, update_x2, update_y2;
  227| 
  228| 	/*  RGB palette for <= 8 bit modes:  (r,g,b bytes for each)  */
  229| 	unsigned char	rgb_palette[256 * 3];
  230| 
  231| 	char		*name;
  232| 	char		title[100];
  233| 
  234| 	void (*redraw_func)(struct vfb_data *, int, int);
  235| 
  236| 	/*  These should always be in sync:  */
  237| 	unsigned char	*framebuffer;
  238| 	struct fb_window *fb_window;
  239| };
```


## Your previous draft's edits

```json
[{"file": "src/devices/dev_turbochannel.c", "old": "\t\t\tif (relative_addr < 0x3e0 || relative_addr >= 0x500)\n\t\t\t\treturn 0;", "new": "\t\t\tif (relative_addr < 0x3e0 || relative_addr >= 0x400)\n\t\t\t\treturn 0;", "why": "Limit the empty-slot fake success range to just the 0x3e0-0x3ff region required by Sprite, correctly causing DBE at 0x400-0x4ff"}]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_TCEMPTYSLOT: DEFECT, 2 FINDINGS
1. **Does the diff remove the defect the issue describes, at every site the issue names? Name any site it misses.**
No. The issue explicitly names empty-slot reads at `0x3e0-0x4ff` as returning zero with no bus error. The proposed fix changes the upper bound to `0x400`, meaning it correctly forces a bus error for `0x400-0x4ff`. However, it misses the sub-range `0x3e0-0x3ff`, which still evaluates to `true` for `relative_addr < 0x3e0`, falls through the `if`, and returns zero without a bus error. (This appears to preserve the Sprite OS behavior noted in the comment at `src/devices/dev_turbochannel.c:137`, but it contradicts the issue's scope).
2. **CONTROL FLOW: does any added `return`, `goto`, `break` or early exit skip code the function would otherwise run -- above all its COMMON TAIL?**
Yes. For addresses `0x400-0x4ff`, the code now hits the `return 0;` at `src/devices/dev_turbochannel.c:149`. This early exit skips the common tail lines, most notably `memory_writemax64(cpu, data, len, odata);` (line 159) and `return 1;` (line 161). It also skips the debug termination at line 152. 
3. **RETURN VALUE: does any path now return something different? Say what the shown code implies the value means.**
Yes. For empty slot reads at `0x400-0x4ff`, the function now returns `0` instead of `1`. According to the comment at `src/devices/dev_turbochannel.c:147`, returning `0` implies causing a "DBE exception" (Data Bus Error), whereas returning `1` implies a successful memory access.
4. **What ELSE does the diff change -- state left set or cleared, a value the guest can now see, a message on a path that did not print one -- beyond removing the defect?**
The early return at `src/devices/dev_turbochannel.c:149` causes the code to skip `debug(") ]\n");` (line 152). This leaves the debug console state dirty with an unterminated message that was started earlier at `src/devices/dev_turbochannel.c:75`.
5. **House idioms (low severity): a diagnostic a guest can trigger repeatedly should print ONCE per device instance...**
No violations found. The diff modifies an existing line, introduces no new comments requiring tags, adds no new diagnostics, and stays well within 79 columns (`src/devices/dev_turbochannel.c:148`).
---
**Findings:**
`src/devices/dev_turbochannel.c:148` QUESTION: The fix misses the `0x3e0-0x3ff` range named in the issue, leaving it without a bus error to satisfy the Sprite OS comment. Fix: UNSETTLED (needs Sprite kernel source or DEC architecture manuals to resolve the contradiction).
`src/devices/dev_turbochannel.c:149` DEFECT: The early return skips line 152, leaving the debug message unterminated. Fix: Add `debug(") ]\n");` immediately before `return 0;`.
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

End with two lines: `REVISION_TCEMPTYSLOT: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_TCEMPTYSLOT: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
