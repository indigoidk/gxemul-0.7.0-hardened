# GXemul hardened fork -- DRAFT A FIX for one filed issue, `pvrdirtyregion` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD d2a6f233).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `pvrdirtyregion`, state `open`, severity `HIGH`)

**title:** PVR pvr_extend_update_region(): with zero display width it divides by zero (SIGFPE) on any multi-byte VRAM write whose span straddles DIWADDRL; with ordinary geometry...

**state_note (head):**

[2026-11-02, records] Site: pvr_extend_update_region() is src/devices/dev_pvr.c:2307 at 987cb596.  ||  GOVERNING TEXT (from the dispositions file, cut at 400 characters): CONFIRMED-NEW HIGH pvrdirtyregion "PVR pvr_extend_update_region(): with zero display width it divides by zero (SIGFPE) on any multi-byte VRAM write whose span straddles DIWADDRL; with ordinary geometry an unclipped lower endpoint below the display start yields an inverted region and the visible update is discarded"

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- Prevents a confirmed SIGFPE on zero display width.

## The code at the cited lines

### `src/devices/dev_pvr.c` around the row's cited line 2307 (HEAD d2a6f233, lines 2262-2352)

```c
 2262| 			d->tilebuf_xsize = idata & TILEBUF_SIZE_WIDTH_MASK;
 2263| 			d->tilebuf_xsize ++; d->tilebuf_ysize ++;
 2264| 			debug("[ pvr: TILEBUF_SIZE set to %i x %i ]\n",
 2265| 			    d->tilebuf_xsize, d->tilebuf_ysize);
 2266| 			DEFAULT_WRITE;
 2267| 		}
 2268| 		break;
 2269| 
 2270| 	case PVRREG_TA_OPB_CFG:
 2271| 		if (writeflag == MEM_WRITE) {
 2272| 			debug("[ pvr: TA_OPB_CFG set to 0x%x ]\n",
 2273| 			    (int) idata);
 2274| 			DEFAULT_WRITE;
 2275| 		}
 2276| 		break;
 2277| 
 2278| 	case PVRREG_TA_INIT:
 2279| 		if (writeflag == MEM_WRITE) {
 2280| 			debug("[ pvr: TA_INIT ]\n");
 2281| 
 2282| 			if (idata & PVR_TA_INIT)
 2283| 				pvr_ta_init(cpu, d);
 2284| 
 2285| 			if (idata != PVR_TA_INIT && idata != 0)
 2286| 				fatal("{ TA_INIT = 0x%08" PRIx32" is not "
 2287| 				    "yet implemented! }", (int) idata);
 2288| 
 2289| 			/*  Always reset to 0.  */
 2290| 			idata = 0;
 2291| 			DEFAULT_WRITE;
 2292| 		}
 2293| 		break;
 2294| 
 2295| 	case PVRREG_YUV_STAT:
 2296| 		// TODO. The "luftvarg" demo accesses this register.
 2297| 		break;
 2298| 
 2299| 	default:if (writeflag == MEM_READ) {
 2300| 			fatal("[ pvr: read from UNIMPLEMENTED addr 0x%x ]\n",
 2301| 			    (int)relative_addr);
 2302| 		} else {
 2303| 			fatal("[ pvr: write to UNIMPLEMENTED addr 0x%x: 0x%x"
 2304| 			    " ]\n", (int)relative_addr, (int)idata);
 2305| 			DEFAULT_WRITE;
 2306| 		}
 2307| 
 2308| 		/*  #187: (Codex/Fable) guest-reachable MMIO (default case for any
 2309| 		    unhandled PVR register); logged above, don't exit(1).  */
 2310| 	}
 2311| 
 2312| return_ok:
 2313| 	if (writeflag == MEM_READ)
 2314| 		memory_writemax64(cpu, data, len, odata);
 2315| 
 2316| 	return 1;
 2317| }
 2318| 
 2319| 
 2320| void pvr_extend_update_region(struct pvr_data *d, uint64_t low, uint64_t high)
 2321| {
 2322| 	int vram_ofs = REG(PVRREG_DIWADDRL);
 2323| 	int bytes_per_line = d->xsize * d->bytes_per_pixel;
 2324| 
 2325| 	low -= vram_ofs;
 2326| 	high -= vram_ofs;
 2327| 
 2328| 	/*  Access inside visible part of VRAM?  */
 2329| 	if ((int64_t)high >= 0 && (int64_t)low <
 2330| 	    bytes_per_line * d->ysize) {
 2331| 		int new_y1, new_y2;
 2332| 
 2333| 		d->fb_update_x1 = 0;
 2334| 		d->fb_update_x2 = d->xsize - 1;
 2335| 
 2336| 		/*  Calculate which line the low and high addresses
 2337| 		    correspond to:  */
 2338| 		new_y1 = low / bytes_per_line;
 2339| 		new_y2 = high / bytes_per_line + 1;
 2340| 
 2341| 		if (d->fb_update_y1 < 0 || new_y1 < d->fb_update_y1)
 2342| 			d->fb_update_y1 = new_y1;
 2343| 		if (d->fb_update_y2 < 0 || new_y2 > d->fb_update_y2)
 2344| 			d->fb_update_y2 = new_y2;
 2345| 
 2346| 		if (d->fb_update_y1 < 0)
 2347| 			d->fb_update_y1 = 0;
 2348| 		if (d->fb_update_y2 >= d->ysize)
 2349| 			d->fb_update_y2 = d->ysize - 1;
 2350| 	}
 2351| }
 2352| 
```

## The data structures those files define (every field that exists)

### `src/devices/dev_pvr.c` -- `struct pvr_data {` (HEAD lines 96-155)

```c
   96| struct pvr_data {
   97| 	struct vfb_data		*fb;
   98| 	int			fb_update_x1;
   99| 	int			fb_update_y1;
  100| 	int			fb_update_x2;
  101| 	int			fb_update_y2;
  102| 
  103| 	struct timer		*vblank_timer;
  104| 	int			vblank_interrupts_pending;
  105| 
  106| 	/*  PVR registers:  */
  107| 	uint32_t		reg[PVRREG_REGSIZE / sizeof(uint32_t)];
  108| 
  109| 	/*  Calculated by pvr_geometry_updated():  */
  110| 	int			xsize, ysize;
  111| 	int			bytes_per_pixel;
  112| 
  113| 	/*  Cached values (from registers):  */
  114| 	/*  DIWMODE:  */
  115| 	int			clock_double;
  116| 	int			strip_buffer_enabled;
  117| 	int			strip_length;
  118| 	int			argb8888_threshold;
  119| 	int			extend;
  120| 	int			pixelmode;
  121| 	int			line_double;
  122| 	int			display_enabled;
  123| 	/*  BRDCOLR:  */
  124| 	int			border_updated;
  125| 	/*  SYNCCONF:  */
  126| 	int			video_enabled;
  127| 	int			broadcast_standard;
  128| 	int			interlaced;
  129| 	int			h_sync_positive;
  130| 	int			v_sync_positive;
  131| 	/*  TILEBUF_SIZE:  */
  132| 	int			tilebuf_xsize;
  133| 	int			tilebuf_ysize;
  134| 
  135| 	/*  Current Tile Accelerator Command (64 bytes):  */
  136| 	uint32_t		ta[64 / sizeof(uint32_t)];
  137| 
  138| 	/*  Stored list of TA commands:  */
  139| 	int			current_list_type;
  140| 	uint32_t		*ta_commands;
  141| 	size_t			allocated_ta_commands;
  142| 	size_t			n_ta_commands;
  143| 
  144| 	/*  Video RAM and Z information:  */
  145| 	uint8_t			*vram;
  146| 	double			*vram_z;
  147| 	int			zwrite_disabled;	/*  #583: ISP/TSP word 1 bit 26 of the
  148| 							    polygon being rendered.  When set, the
  149| 							    rasterizers skip their vram_z stores.
  150| 							    Cleared at every pvr_render entry.  */
  151| 
  152| 	/*  DMA registers:  */
  153| 	uint32_t		dma_reg[N_PVR_DMA_REGS];
  154| 	uint32_t		dma_more_reg[N_PVR_DMA_REGS];
  155| };
```

RULES FOR THE EDITS: change ONLY text that appears in this packet; use ONLY fields, functions and macros that appear in it
(a draft that calls an undeclared function or a field that does not exist does not compile); make each `old` long enough to
occur exactly once in its file -- include a distinctive neighbouring line when a statement repeats.

## WHAT TO RETURN

1. One line: `STILL PRESENT: YES|NO|UNSETTLED -- <the line of code shown that shows it>`.  The cited line numbers may have
   moved since the row was written; judge from the code shown.  If NO, say what already fixed it and STOP (no edits).
2. If YES: EXACTLY ONE fenced ```json block -- a list of edits, the smallest fix that removes the defect without changing any
   other behaviour: [{"file": "src/...", "old": "<exact text from the code above, without the line-number prefix; it must occur
   EXACTLY ONCE in that file>", "new": "<replacement>", "why": "<one line>"}].  Use JSON escapes (\t, \n).  Tabs stay tabs;
   lines within 79 columns; tag a new comment `/* #NNN: ... */`.  Prefer the file's existing idioms (a decline, a once-per-
   device announce, a clamp) over new machinery.
3. After the block: what the fix deliberately does NOT change, and anything you could not settle from the code shown.

End with one line: `FIXDRAFT_PVRDIRTYREGION: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
