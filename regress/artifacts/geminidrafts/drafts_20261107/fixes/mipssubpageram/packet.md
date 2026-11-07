# GXemul hardened fork -- DRAFT A FIX for one filed issue, `mipssubpageram` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD d2a6f233).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `mipssubpageram`, state `open`, severity `MED`)

**title:** cpus/memory_rw.c MIPS PROM-area fallthrough + devices/dev_mc146818.c init -- sub-page devices in the 0x1fc00000 window (KN02 RTC 0x100 bytes, DZ 0x80 bytes): one access past the registers maps the whole page as RAM and later accesses bypass the device -- WRONG-RESULT (device silently disconnected; NVRAM stores lost)

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T37 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A2-66, A(c)#8).  Source URLs: https://github.com/rpajarola/gxemul/commit/e37235e61de104fc7402793e6bba9fdd7aeb2607.  Our site at de8c7547: src/cpus/memory_rw.c:662-667, :738-750; src/devices/dev_mc146818.c:671-682; src/include/devices.h:167.  Portable fix: yes -- port rpajarola e37235e (register the whole page) or fix the PROM-area fallthrough.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- register the whole page for sub-page devices.

## The code at the cited lines

### `src/cpus/memory_rw.c` around the row's cited line 662 (HEAD d2a6f233, lines 617-707)

```c
  617| 					    OpenBSD/mvme88k's trap.c extracts) and PFAR =
  618| 					    orig_paddr, the PHYSICAL address saved before paddr
  619| 					    was made device-relative.  cmmu[0] is the instruction
  620| 					    CMMU, cmmu[1] the data CMMU (memory_m88k.c's index);
  621| 					    the other CMMU is not written.  For a CPU without a
  622| 					    CMMU, this arm makes no register write; the exception
  623| 					    call is unchanged.  `null route` scores data-access
  624| 					    delivery; instruction-access delivery is unscored
  625| 					    (`null surv` scores survival only).  NO_EXCEPTIONS
  626| 					    callers (e.g. the debugger's dump) never get here:
  627| 					    the test above keeps them out.  */
  628| 					{
  629| 						struct m8820x_cmmu *cmmu =
  630| 						    cpu->cd.m88k.cmmu[cache ==
  631| 						    CACHE_INSTRUCTION ? 0 : 1];
  632| 						if (cmmu != NULL) {
  633| 							cmmu->reg[CMMU_PFSR] =
  634| 							    CMMU_PFSR_BERROR << 16;
  635| 							cmmu->reg[CMMU_PFAR] =
  636| 							    (uint32_t) orig_paddr;
  637| 						}
  638| 					}
  639| 					m88k_exception(cpu, cache == CACHE_INSTRUCTION
  640| 					    ? M88K_EXCEPTION_INSTRUCTION_ACCESS
  641| 					    : M88K_EXCEPTION_DATA_ACCESS, 0);
  642| #endif
  643| 					return MEMORY_ACCESS_FAILED;
  644| 				}
  645| 				goto do_return_ok;
  646| 			}
  647| 
  648| 			if (paddr < mem->devices[i].baseaddr)
  649| 				end = i - 1;
  650| 			if (paddr >= mem->devices[i].endaddr)
  651| 				start = i + 1;
  652| 			i = (start + end) >> 1;
  653| 		} while (start <= end);
  654| 	}
  655| 
  656| 
  657| #ifdef MEM_MIPS
  658| 	/*
  659| 	 *  Data and instruction cache emulation:
  660| 	 */
  661| 
  662| 	switch (cpu->cd.mips.cpu_type.mmu_model) {
  663| 	case MMU3K:
  664| 		/*  if not uncached addess  (TODO: generalize this)  */
  665| 		if (!(misc_flags & PHYSICAL) && cache != CACHE_NONE &&
  666| 		    !((vaddr & 0xffffffffULL) >= 0xa0000000ULL &&
  667| 		      (vaddr & 0xffffffffULL) <= 0xbfffffffULL)) {
  668| 			if (memory_cache_R3000(cpu, cache, paddr,
  669| 			    writeflag, len, data))
  670| 				goto do_return_ok;
  671| 		}
  672| 		break;
  673| 	default:
  674| 		/*  R4000 etc  */
  675| 		/*  TODO  */
  676| 		;
  677| 	}
  678| #endif	/*  MEM_MIPS  */
  679| 
  680| 
  681| 	/*  Outside of physical RAM?  */
  682| 	if (paddr >= mem->physical_max) {
  683| #ifdef MEM_MIPS
  684| 		if ((paddr & 0xffffc00000ULL) == 0x1fc00000) {
  685| 			/*  Ok, this is PROM stuff  */
  686| 		} else if ((paddr & 0xfffff00000ULL) == 0x1ff00000) {
  687| 			/*  Sprite reads from this area of memory...  */
  688| 			/*  TODO: is this still correct?  */
  689| 			if (writeflag == MEM_READ)
  690| 				memset(data, 0, len);
  691| 			goto do_return_ok;
  692| 		} else
  693| #endif /* MIPS */
  694| 		{
  695| 			if (paddr >= mem->physical_max && !no_exceptions)
  696| 				if (memory_warn_about_unimplemented_addr
  697| 				    (cpu, mem, writeflag, paddr, len))
  698| 					return MEMORY_ACCESS_FAILED;
  699| 
  700| 			if (writeflag == MEM_READ) {
  701| 				/*  Return all zeroes? (Or 0xff? TODO)  */
  702| 				memset(data, 0, len);
  703| 
  704| #if 0
  705| /*
  706|  *  NOTE: This code prevents a PROM image from a real 5000/200 from booting.
  707|  *  I think I introduced it because it was how some guest OS (NetBSD?) detected
```

### `src/devices/dev_mc146818.c` around the row's cited line 671 (HEAD d2a6f233, lines 626-691)

```c
  626| 		d->reg[0x0d] = ether_address[3];
  627| 		d->reg[0x11] = ether_address[4];
  628| 		d->reg[0x15] = ether_address[5];
  629| 		/*  TODO:  19, 1d, 21, 25 = checksum bytes 1,2,2,1 resp. */
  630| 		d->reg[0x29] = ether_address[5];
  631| 		d->reg[0x2d] = ether_address[4];
  632| 		d->reg[0x31] = ether_address[3];
  633| 		d->reg[0x35] = ether_address[2];
  634| 		d->reg[0x39] = ether_address[1];
  635| 		d->reg[0x3d] = ether_address[1];
  636| 		d->reg[0x41] = ether_address[0];
  637| 		d->reg[0x45] = ether_address[1];
  638| 		d->reg[0x49] = ether_address[2];
  639| 		d->reg[0x4d] = ether_address[3];
  640| 		d->reg[0x51] = ether_address[4];
  641| 		d->reg[0x55] = ether_address[5];
  642| 		/*  TODO:  59, 5d = checksum bytes 1,2 resp. */
  643| 		d->reg[0x61] = 0xff;
  644| 		d->reg[0x65] = 0x00;
  645| 		d->reg[0x69] = 0x55;
  646| 		d->reg[0x6d] = 0xaa;
  647| 		d->reg[0x71] = 0xff;
  648| 		d->reg[0x75] = 0x00;
  649| 		d->reg[0x79] = 0x55;
  650| 		d->reg[0x7d] = 0xaa;
  651| 
  652| 		/*  Battery valid, for DECstations  */
  653| 		d->reg[0xf8] = 1;
  654| 	}
  655| 
  656| 	/*
  657| 	 *  uip_threshold should ideally be 1, but when Linux polls the UIP bit
  658| 	 *  it looses speed. This hack gives Linux the impression that the cpu
  659| 	 *  is uip_threshold times faster than the slow clock it would
  660| 	 *  otherwise detect.
  661| 	 *
  662| 	 *  TODO:  Find out if this messes up Sprite emulation; if so, then
  663| 	 *         this hack has to be removed.
  664| 	 */
  665| 	d->uip_threshold = 8;
  666| 
  667| 	if (access_style == MC146818_ARC_JAZZ)
  668| 		memory_device_register(mem, "mc146818_jazz", 0x90000070ULL,
  669| 		    1, dev_mc146818_jazz_access, d, DM_DEFAULT, NULL);
  670| 
  671| 	dev_len = DEV_MC146818_LENGTH;
  672| 	switch (access_style) {
  673| 	case MC146818_CATS:
  674| 	case MC146818_PC_CMOS:
  675| 		dev_len = 2;
  676| 		break;
  677| 	case MC146818_SGI:
  678| 		dev_len = 0x400;
  679| 	}
  680| 
  681| 	memory_device_register(mem, "mc146818", baseaddr,
  682| 	    dev_len * addrdiv, dev_mc146818_access,
  683| 	    d, DM_DEFAULT, NULL);
  684| 
  685| 	mc146818_update_time(d);
  686| 
  687| 	machine_add_tickfunction(machine, dev_mc146818_tick, d,
  688| 	    MC146818_TICK_SHIFT);
  689| }
  690| 
  691| 
```

### `src/include/devices.h` around the row's cited line 167 (HEAD d2a6f233, lines 122-212)

```c
  122| 	const char *irq_path, void *turbochannel, int mode,
  123| 	size_t (*dma_controller)(void *dma_controller_data,
  124| 		unsigned char *data, size_t len, int writeflag),
  125| 	void *dma_controller_data);
  126| 
  127| /*  dev_bt431.c:  */
  128| #define	DEV_BT431_LENGTH		0x20
  129| #define	DEV_BT431_NREGS			0x800	/*  ?  */
  130| int dev_bt431_access(struct cpu *cpu, struct memory *mem,
  131| 	uint64_t relative_addr, unsigned char *data, size_t len,
  132| 	int writeflag, void *);
  133| struct vfb_data;
  134| void dev_bt431_init(struct memory *mem, uint64_t baseaddr,
  135| 	struct vfb_data *vfb_data, int color_fb_flag);
  136| 
  137| /*  dev_bt455.c:  */
  138| #define	DEV_BT455_LENGTH		0x20
  139| int dev_bt455_access(struct cpu *cpu, struct memory *mem,
  140| 	uint64_t relative_addr, unsigned char *data, size_t len,
  141| 	int writeflag, void *);
  142| struct vfb_data;
  143| void dev_bt455_init(struct memory *mem, uint64_t baseaddr,
  144| 	struct vfb_data *vfb_data);
  145| 
  146| /*  dev_bt459.c:  */
  147| #define	DEV_BT459_LENGTH		0x20
  148| #define	DEV_BT459_NREGS			0x1000
  149| #define	BT459_PX		1	/*  px[g]  */
  150| #define	BT459_BA		2	/*  cfb  */
  151| #define	BT459_BBA		3	/*  sfb  */
  152| int dev_bt459_access(struct cpu *cpu, struct memory *mem,
  153| 	uint64_t relative_addr, unsigned char *data, size_t len,
  154| 	int writeflag, void *);
  155| struct vfb_data;
  156| void dev_bt459_init(struct machine *machine, struct memory *mem,
  157| 	uint64_t baseaddr, uint64_t baseaddr_irq, struct vfb_data *vfb_data,
  158| 	int color_fb_flag, const char *irq_path, int type);
  159| 
  160| /*  dev_colorplanemask.c:  */
  161| #define	DEV_COLORPLANEMASK_LENGTH	0x0000000000000010
  162| int dev_colorplanemask_access(struct cpu *cpu, struct memory *mem,
  163| 	uint64_t relative_addr, unsigned char *data, size_t len,
  164| 	int writeflag, void *);
  165| void dev_colorplanemask_init(struct memory *mem, uint64_t baseaddr,
  166| 	unsigned char *color_plane_mask);
  167| 
  168| /*  dev_dc7085.c:  */
  169| #define	DEV_DC7085_LENGTH		0x0000000000000080
  170| /*  see dc7085.h for more info  */
  171| void dev_dc7085_tick(struct cpu *cpu, void *);
  172| int dev_dc7085_access(struct cpu *cpu, struct memory *mem,
  173| 	uint64_t relative_addr, unsigned char *data, size_t len,
  174| 	int writeflag, void *);
  175| int dev_dc7085_init(struct machine *machine, struct memory *mem,
  176| 	uint64_t baseaddr, char *irq_path, int use_fb);
  177| 
  178| /*  dev_dec5800.c:  */
  179| #define	DEV_DECCCA_LENGTH			0x10000	/*  ?  */
  180| #define	DEC_DECCCA_BASEADDR			0x19000000	/*  ?  I just made this up  */
  181| int dev_deccca_access(struct cpu *cpu, struct memory *mem, uint64_t relative_addr, unsigned char *data, size_t len, int writeflag, void *);
  182| void dev_deccca_init(struct memory *mem, uint64_t baseaddr);
  183| #define	DEV_DECXMI_LENGTH			0x800000
  184| int dev_decxmi_access(struct cpu *cpu, struct memory *mem, uint64_t relative_addr, unsigned char *data, size_t len, int writeflag, void *);
  185| void dev_decxmi_init(struct memory *mem, uint64_t baseaddr);
  186| 
  187| /*  dev_fb.c:  */
  188| #define	DEV_FB_LENGTH		0x3c0000	/*  3c0000 to not colide with */
  189| 						/*  turbochannel rom,         */
  190| 						/*  otherwise size = 4MB      */
  191| /*  Type:  */
  192| #define	VFB_GENERIC		0
  193| #define	VFB_HPC			1
  194| #define	VFB_DEC_VFB01		2
  195| #define	VFB_DEC_VFB02		3
  196| #define	VFB_DEC_MAXINE		4
  197| #define	VFB_PLAYSTATION2	5
  198| #define	VFB_REVERSEBITS		6
  199| /*  Extra flags:  */
  200| #define	VFB_REVERSE_START	0x10000
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

End with one line: `FIXDRAFT_MIPSSUBPAGERAM: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
