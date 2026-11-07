# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `mipssubpageram` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `mipssubpageram`, state `open`)

**title:** cpus/memory_rw.c MIPS PROM-area fallthrough + devices/dev_mc146818.c init -- sub-page devices in the 0x1fc00000 window (KN02 RTC 0x100 bytes, DZ 0x80 bytes): one access past the registers maps the whole page as RAM and later accesses bypass the device -- WRONG-RESULT (device silently disconnected; NVRAM stores lost)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T37 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A2-66, A(c)#8).  Source URLs: https://github.com/rpajarola/gxemul/commit/e37235e61de104fc7402793e6bba9fdd7aeb2607.  Our site at de8c7547: src/cpus/memory_rw.c:662-667, :738-750; src/devices/dev_mc146818.c:671-682; src/include/devices.h:167.  Portable fix: yes -- port rpajarola e37235e (register the whole page) or fix the PROM-area fallthrough.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/cpus/memory_rw.c` -- AT HEAD, lines 232-805 (`*` marks a line your previous draft changed)

```c
  232|  {
  233|  	const int offset_mask = MRW_OFFSET_MASK;
  234|  
  235|  	int ok = 2;
  236|  	uint64_t paddr;
     | [... lines 237-575 not shown ...]
  576|  					if (host_addr != NULL)
  577|  						cpu->update_translation_table(
  578|  						    cpu, vaddr & ~offset_mask,
  579|  						    host_addr, wf,
  580|  						    orig_paddr & ~offset_mask);
  581|  				}
  582|  
  583|  				res = 0;
  584|  				if (!no_exceptions || (mem->devices[i].flags &
  585|  				    DM_READS_HAVE_NO_SIDE_EFFECTS)) {
  586|  					bool running_before_device_access = cpu->running;
  587|  					res = mem->devices[i].f(cpu, mem, paddr,
  588|  					    data, len, writeflag,
  589|  					    mem->devices[i].extra);
  590|  
  591|  					if (running_before_device_access && !cpu->running)
  592|  						return MEMORY_ACCESS_FAILED;
  593|  				}
  594|  
  595|  				if (res == 0)
  596|  					res = -1;
  597|  
  598|  				/*
  599|  				 *  If accessing the memory mapped device
  600|  				 *  failed, then return with an exception.
  601|  				 *  (Architecture specific.)
  602|  				 */
  603|  				if (res <= 0 && !no_exceptions) {
  604|  					debug("[ %s device '%s' addr %08lx "
  605|  					    "failed ]\n", writeflag?
  606|  					    "writing to" : "reading from",
  607|  					    mem->devices[i].name, (long)paddr);
  608|  #ifdef MEM_MIPS
  609|  					mips_cpu_exception(cpu,
  610|  					    cache == CACHE_INSTRUCTION?
  611|  					    EXCEPTION_IBE : EXCEPTION_DBE,
  612|  					    0, vaddr, 0, 0, 0, 0);
  613|  #endif
  614|  #ifdef MEM_M88K
  615|  					/*  #570: record the bus error in the faulting side's
  616|  					    CMMU first: PFSR = BERROR << 16 (the field
  617|  					    OpenBSD/mvme88k's trap.c extracts) and PFAR =
  618|  					    orig_paddr, the PHYSICAL address saved before paddr
  619|  					    was made device-relative.  cmmu[0] is the instruction
  620|  					    CMMU, cmmu[1] the data CMMU (memory_m88k.c's index);
  621|  					    the other CMMU is not written.  For a CPU without a
  622|  					    CMMU, this arm makes no register write; the exception
  623|  					    call is unchanged.  `null route` scores data-access
  624|  					    delivery; instruction-access delivery is unscored
  625|  					    (`null surv` scores survival only).  NO_EXCEPTIONS
  626|  					    callers (e.g. the debugger's dump) never get here:
  627|  					    the test above keeps them out.  */
  628|  					{
  629|  						struct m8820x_cmmu *cmmu =
  630|  						    cpu->cd.m88k.cmmu[cache ==
  631|  						    CACHE_INSTRUCTION ? 0 : 1];
  632|  						if (cmmu != NULL) {
  633|  							cmmu->reg[CMMU_PFSR] =
  634|  							    CMMU_PFSR_BERROR << 16;
  635|  							cmmu->reg[CMMU_PFAR] =
  636|  							    (uint32_t) orig_paddr;
  637|  						}
  638|  					}
  639|  					m88k_exception(cpu, cache == CACHE_INSTRUCTION
  640|  					    ? M88K_EXCEPTION_INSTRUCTION_ACCESS
  641|  					    : M88K_EXCEPTION_DATA_ACCESS, 0);
  642|  #endif
  643|  					return MEMORY_ACCESS_FAILED;
  644|  				}
  645|  				goto do_return_ok;
  646|  			}
  647|  
  648|  			if (paddr < mem->devices[i].baseaddr)
  649|  				end = i - 1;
  650|  			if (paddr >= mem->devices[i].endaddr)
  651|  				start = i + 1;
  652|  			i = (start + end) >> 1;
  653|  		} while (start <= end);
  654|  	}
  655|  
  656|  
  657|  #ifdef MEM_MIPS
  658|  	/*
  659|  	 *  Data and instruction cache emulation:
  660|  	 */
  661|  
  662|  	switch (cpu->cd.mips.cpu_type.mmu_model) {
  663|  	case MMU3K:
  664|  		/*  if not uncached addess  (TODO: generalize this)  */
  665|  		if (!(misc_flags & PHYSICAL) && cache != CACHE_NONE &&
  666|  		    !((vaddr & 0xffffffffULL) >= 0xa0000000ULL &&
  667|  		      (vaddr & 0xffffffffULL) <= 0xbfffffffULL)) {
  668|  			if (memory_cache_R3000(cpu, cache, paddr,
  669|  			    writeflag, len, data))
  670|  				goto do_return_ok;
  671|  		}
  672|  		break;
  673|  	default:
  674|  		/*  R4000 etc  */
  675|  		/*  TODO  */
  676|  		;
  677|  	}
  678|  #endif	/*  MEM_MIPS  */
  679|  
  680|  
  681|  	/*  Outside of physical RAM?  */
  682|  	if (paddr >= mem->physical_max) {
  683|  #ifdef MEM_MIPS
  684|  		if ((paddr & 0xffffc00000ULL) == 0x1fc00000) {
  685|  			/*  Ok, this is PROM stuff  */
  686|* 		} else if ((paddr & 0xfffff00000ULL) == 0x1ff00000) {
  687|  			/*  Sprite reads from this area of memory...  */
  688|  			/*  TODO: is this still correct?  */
  689|  			if (writeflag == MEM_READ)
  690|  				memset(data, 0, len);
  691|  			goto do_return_ok;
  692|  		} else
  693|  #endif /* MIPS */
  694|  		{
  695|  			if (paddr >= mem->physical_max && !no_exceptions)
  696|  				if (memory_warn_about_unimplemented_addr
  697|  				    (cpu, mem, writeflag, paddr, len))
  698|  					return MEMORY_ACCESS_FAILED;
  699|  
  700|  			if (writeflag == MEM_READ) {
  701|  				/*  Return all zeroes? (Or 0xff? TODO)  */
  702|  				memset(data, 0, len);
  703|  
  704|  #if 0
  705|  /*
  706|   *  NOTE: This code prevents a PROM image from a real 5000/200 from booting.
  707|   *  I think I introduced it because it was how some guest OS (NetBSD?) detected
  708|   *  the amount of RAM on some machine.
  709|   *
  710|   *  TODO: Figure out if it is not needed anymore, and remove it completely.
  711|   */
  712|  #ifdef MEM_MIPS
  713|  				/*
  714|  				 *  For real data/instruction accesses, cause
  715|  				 *  an exceptions on an illegal read:
  716|  				 */
  717|  				if (cache != CACHE_NONE && !no_exceptions &&
  718|  				    paddr >= mem->physical_max &&
  719|  				    paddr < mem->physical_max+1048576) {
  720|  					mips_cpu_exception(cpu,
  721|  					    EXCEPTION_DBE, 0, vaddr, 0,
  722|  					    0, 0, 0);
  723|  				}
  724|  #endif  /*  MEM_MIPS  */
  725|  #endif
  726|  			}
  727|  
  728|  			/*  Hm? Shouldn't there be a DBE exception for
  729|  			    invalid writes as well?  TODO  */
  730|  
  731|  			goto do_return_ok;
  732|  		}
  733|  	}
  734|  
  735|  
  736|  	/*
  737|  	 *  Uncached access:
  738|  	 *
  739|  	 *  1)  Translate the physical address to a host address.
  740|  	 *
  741|  	 *  2)  Insert this virtual->physical->host translation into the
  742|  	 *      fast translation arrays (using update_translation_table()).
  743|  	 *
  744|  	 *  3)  If this was a Write, then invalidate any code translations
  745|  	 *      in that page.
  746|  	 */
     | [... lines 747-775 not shown ...]
  776|  	if ((writeflag == MEM_WRITE
  777|  	    || (ok == 2 && cache == CACHE_DATA)
  778|  	    ) && cpu->invalidate_code_translation != NULL)
  779|  		cpu->invalidate_code_translation(cpu, paddr, INVALIDATE_PADDR);
  780|  
  781|  	if ((paddr&((1<<BITS_PER_MEMBLOCK)-1)) + len > (1<<BITS_PER_MEMBLOCK)) {
  782|  		/*  #165: (Codex/Fable) split accesses that cross a memblock
  783|  		    boundary (e.g. large DMA transfers) at the boundary,
  784|  		    instead of exiting the whole emulator.  */
  785|  		size_t len_head = (size_t) ((1<<BITS_PER_MEMBLOCK) -
  786|  		    (paddr & ((1<<BITS_PER_MEMBLOCK)-1)));
  787|  
  788|  		if (writeflag == MEM_WRITE)
  789|  			memcpy(memblock + offset, data, len_head);
  790|  		else
  791|  			memcpy(data, memblock + offset, len_head);
  792|  
  793|  		return MEMORY_RW(cpu, mem, vaddr + len_head, data + len_head,
  794|  		    len - len_head, writeflag, misc_flags);
  795|  	}
  796|  
  797|  	/*  And finally, read or write the data:  */
  798|  	if (writeflag == MEM_WRITE)
  799|  		memcpy(memblock + offset, data, len);
  800|  	else
  801|  		memcpy(data, memblock + offset, len);
  802|  
  803|  do_return_ok:
  804|  	return MEMORY_ACCESS_OK;
  805|  }
```

## The data structures those files define (every field that exists)

### `src/devices/dev_mc146818.c` -- `struct mc_data {` (HEAD lines 65-88)

```c
   65| struct mc_data {
   66| 	int		access_style;
   67| 	int		last_addr;
   68| 
   69| 	int		register_choice;
   70| 	int		reg[N_REGISTERS];
   71| 	int		addrdiv;
   72| 
   73| 	int		use_bcd;
   74| 
   75| 	int		timebase_hz;
   76| 	int		interrupt_hz;
   77| 	int		old_interrupt_hz;
   78| 	struct interrupt irq;
   79| 	struct timer	*timer;
   80| 	volatile int	pending_timer_interrupts;
   81| 
   82| 	int		previous_second;
   83| 	int		n_seconds_elapsed;
   84| 	int		uip_threshold;
   85| 
   86| 	int		ugly_netbsd_prep_hack_done;
   87| 	int		ugly_netbsd_prep_hack_sec;
   88| };
```

### `src/include/devices.h` -- `struct pic8259_data {` (HEAD lines 63-75)

```c
   63| struct pic8259_data {
   64| 	struct interrupt irq;
   65| 
   66| 	int		irq_base;
   67| 	int		current_command;
   68| 
   69| 	int		init_state;
   70| 
   71| 	int		priority_reg;
   72| 	uint8_t		irr;		/*  interrupt request register  */
   73| 	uint8_t		isr;		/*  interrupt in-service register  */
   74| 	uint8_t		ier;		/*  interrupt enable register  */
   75| };
```

### `src/include/devices.h` -- `struct dec_ioasic_data {` (HEAD lines 82-110)

```c
   82| struct dec_ioasic_data {
   83| 	uint32_t	scsi_dmaptr;		/*  0x000  */
   84| 	uint32_t	scsi_nextptr;		/*  0x010  */
   85| 	uint32_t	lance_dmaptr;		/*  0x020  */
   86| 	uint32_t	floppy_dmaptr;		/*  0x070  */
   87| 	uint32_t	isdn_x_dmaptr;		/*  0x080  */
   88| 	uint32_t	isdn_x_nextptr;		/*  0x090  */
   89| 	uint32_t	isdn_r_dmaptr;		/*  0x0a0  */
   90| 	uint32_t	isdn_r_nextptr;		/*  0x0b0  */
   91| 	uint32_t	csr;			/*  0x100  */
   92| 	uint32_t	intr;			/*  0x110  */
   93| 	uint32_t	imsk;			/*  0x120  */
   94| 	uint32_t	isdn_x_data;		/*  0x140  */
   95| 	uint32_t	isdn_r_data;		/*  0x150  */
   96| 	uint32_t	lance_decode;		/*  0x160  */
   97| 	uint32_t	scsi_decode;		/*  0x170  */
   98| 	uint32_t	scc0_decode;		/*  0x180  */
   99| 	uint32_t	scc1_decode;		/*  0x190  */
  100| 	uint32_t	floppy_decode;		/*  0x1a0  */
  101| 	uint32_t	scsi_scr;		/*  0x1b0  */
  102| 	uint32_t	scsi_sdr0;		/*  0x1c0  */
  103| 	uint32_t	scsi_sdr1;		/*  0x1d0  */
  104| 
  105| 	int		(*dma_func[MAX_IOASIC_DMA_FUNCTIONS])(struct cpu *, void *, uint64_t addr, size_t dma_len, int tx);
  106| 	void		*dma_func_extra[MAX_IOASIC_DMA_FUNCTIONS];
  107| 	int		rackmount_flag;
  108| 	struct interrupt *irq;
  109| 	int		int_asserted;
  110| };
```

### `src/include/devices.h` -- `struct vfb_data {` (HEAD lines 201-239)

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

### `src/include/devices.h` -- `struct px_data {` (HEAD lines 345-357)

```c
  345| struct px_data {
  346| 	struct memory		*fb_mem;
  347| 	struct vfb_data		*vfb_data;
  348| 	int			type;
  349| 	const char		*px_name;
  350| 	struct interrupt	irq;
  351| 	int			bitdepth;
  352| 	int			xconfig;
  353| 	int			yconfig;
  354| 
  355| 	uint32_t		intr;
  356| 	unsigned char		sram[128 * 1024];
  357| };
```

### `src/include/devices.h` -- `struct sgi_ip20_data {` (HEAD lines 434-436)

```c
  434| struct sgi_ip20_data {
  435| 	int		dummy;
  436| };
```

### `src/include/devices.h` -- `struct sgi_ip22_data {` (HEAD lines 446-452)

```c
  446| struct sgi_ip22_data {
  447| 	int		guiness_flag;
  448| 	uint32_t	reg[DEV_SGI_IP22_LENGTH / 4];
  449| 	uint32_t	imc_reg[DEV_SGI_IP22_IMC_LENGTH / 4];
  450| 	uint32_t	unknown2_reg[DEV_SGI_IP22_UNKNOWN2_LENGTH / 4];
  451| 	uint32_t	unknown_timer;
  452| };
```

### `src/include/devices.h` -- `struct lk201_data {` (HEAD lines 517-531)

```c
  517| struct lk201_data {
  518|         int                     use_fb;
  519| 	int			console_handle;
  520| 
  521|         int                     (*space_available_in_queue)(void *,int);
  522|         void                    (*add_to_rx_queue)(void *,int,int);
  523| 	void			*add_data;
  524|                 
  525|         unsigned char           keyb_buf[8];
  526|         int                     keyb_buf_pos;
  527|                         
  528|         int                     mouse_mode;
  529|         int                     mouse_revision;         /*  0..15  */  
  530|         int                     mouse_buttons;
  531| };
```


## Your previous draft's edits

```json
[
  {
    "file": "src/cpus/memory_rw.c",
    "old": "\t\tif ((paddr & 0xffffc00000ULL) == 0x1fc00000) {\n\t\t\t/*  Ok, this is PROM stuff  */\n\t\t} else if ((paddr & 0xfffff00000ULL) == 0x1ff00000) {",
    "new": "\t\tif ((paddr & 0xffffc00000ULL) == 0x1fc00000) {\n\t\t\t/*  Ok, this is PROM stuff  */\n\t\t\tgoto do_return_ok;\n\t\t} else if ((paddr & 0xfffff00000ULL) == 0x1ff00000) {",
    "why": "The PROM area fallthrough continues past the if/else chain and hits the default behaviour of either aborting or filling with zeroes and returning MEMORY_ACCESS_FAILED. Since the issue says 'one access past the registers maps the whole page as RAM and later accesses bypass the device', adding the goto do_return_ok ensures it returns successfully without falling through."
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_MIPSSUBPAGERAM: DEFECT, 1 FINDINGS
1. The diff addresses the PROM-area fallthrough in `memory_rw.c`. While it does not touch `dev_mc146818.c` or `devices.h`, the issue notes that fixing the fallthrough is an acceptable portable alternative to registering the whole page.
2. CONTROL FLOW: Yes, the added `goto do_return_ok;` at line 686 skips the fallthrough to line 738 (which wrongly mapped the page as RAM) but also skips initializing the read buffer. It skips `memset(data, 0, len);` or `memcpy(data, memblock + offset, len);` that the function would normally execute to populate the guest's read request.
3. RETURN VALUE: The return value itself is unchanged (`MEMORY_ACCESS_OK`), but it implies success while returning uninitialized host memory (garbage) in `data` to the guest on a read.
4. ELSE: Because `data` is left unmodified on read, the guest guest can now see uninitialized memory contents from the emulator process for addresses in this region not covered by a device.
5. HOUSE IDIOMS: No new style or idiom violations were introduced by the single-line addition.
src/cpus/memory_rw.c:686, DEFECT, `if (writeflag == MEM_READ) memset(data, 0, len); goto do_return_ok;`
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

End with two lines: `REVISION_MIPSSUBPAGERAM: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_MIPSSUBPAGERAM: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
