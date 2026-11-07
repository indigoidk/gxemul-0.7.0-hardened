# GXemul hardened fork -- DRAFT A FIX for one filed issue, `vgagfxwindowend` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `vgagfxwindowend`, state `open`, severity `LOW`)

**title:** src/devices/dev_vga.c DEVICE_ACCESS(vga_graphics) -- `relative_addr + len >= GFX_ADDR_WINDOW` declines an access that ends exactly at the window's end (the window's last word), an off-by-one; it is the producer the #582 design rulings found for the PowerPC failed-read block's arm (d)

**state_note (head):**

Filed 2026-11-05 by #582: the design rulings' dev_vga bound (regress/artifacts/qhslowifetch/adj_20261104/FABLE_FINAL_r2.md, its F1, and RECON_FABLE.md, which carries 'the dev_vga >= filing' into the merged design).  Read, not measured: src/devices/dev_vga.c:617.  Fixing it removes `ppcifetchdeclineprod`'s producer (ROW 5).

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- Fixing the off-by-one error directly removes the producer for another bug.

## The code at the cited lines

### `src/devices/dev_vga.c` around the row's cited line 617 (HEAD 8d9df658, lines 497-737)

```c
  497| }
  498| 
  499| 
  500| /*
  501|  *  vga_update_cursor():
  502|  */
  503| static void vga_update_cursor(struct machine *machine, struct vga_data *d)
  504| {
  505| 	int onoff = 1, height = d->crtc_reg[VGA_CRTC_CURSOR_SCANLINE_END]
  506| 	    - d->crtc_reg[VGA_CRTC_CURSOR_SCANLINE_START] + 1;
  507| 
  508| 	if (d->cur_mode != MODE_CHARCELL)
  509| 		onoff = 0;
  510| 
  511| 	if (d->crtc_reg[VGA_CRTC_CURSOR_SCANLINE_START] >
  512| 	    d->crtc_reg[VGA_CRTC_CURSOR_SCANLINE_END]) {
  513| 		onoff = 0;
  514| 		height = 1;
  515| 	}
  516| 
  517| 	if (d->crtc_reg[VGA_CRTC_CURSOR_SCANLINE_START] >= d->font_height)
  518| 		onoff = 0;
  519| 
  520| 	dev_fb_setcursor(d->fb,
  521| 	    d->cursor_x * d->font_width * d->pixel_repx, (d->cursor_y *
  522| 	    d->font_height + d->crtc_reg[VGA_CRTC_CURSOR_SCANLINE_START]) *
  523| 	    d->pixel_repy, onoff, d->font_width * d->pixel_repx, height *
  524| 	    d->pixel_repy);
  525| }
  526| 
  527| 
  528| DEVICE_TICK(vga)
  529| {
  530| 	struct vga_data *d = (struct vga_data *) extra;
  531| 	int64_t low = -1, high;
  532| 
  533| 	vga_update_cursor(cpu->machine, d);
  534| 
  535| 	/*  TODO: text vs graphics tick?  */
  536| 	memory_device_dyntrans_access(cpu, cpu->mem, extra,
  537| 	    (uint64_t *) &low, (uint64_t *) &high);
  538| 
  539| 	if (low != -1) {
  540| 		int base = ((d->crtc_reg[VGA_CRTC_START_ADDR_HIGH] << 8)
  541| 		    + d->crtc_reg[VGA_CRTC_START_ADDR_LOW]) * 2;
  542| 		int new_u_y1, new_u_y2;
  543| 		debug("[ dev_vga_tick: dyntrans access, %" PRIx64" .. %"
  544| 		    PRIx64" ]\n", (uint64_t) low, (uint64_t) high);
  545| 		low -= base;
  546| 		high -= base;
  547| 		d->update_x1 = 0;
  548| 		d->update_x2 = d->max_x - 1;
  549| 		new_u_y1 = (low/2) / d->max_x;
  550| 		new_u_y2 = ((high/2) / d->max_x) + 1;
  551| 		if (new_u_y1 < d->update_y1)
  552| 			d->update_y1 = new_u_y1;
  553| 		if (new_u_y2 > d->update_y2)
  554| 			d->update_y2 = new_u_y2;
  555| 		if (d->update_y1 < 0)
  556| 			d->update_y1 = 0;
  557| 		if (d->update_y2 >= d->max_y)
  558| 			d->update_y2 = d->max_y - 1;
  559| 		d->modified = 1;
  560| 	}
  561| 
  562| 	if (d->n_is1_reads > N_IS1_READ_THRESHOLD &&
  563| 	    d->retrace_palette != NULL) {
  564| 		d->use_palette_per_line = 1;
  565| 		d->update_x1 = 0;
  566| 		d->update_x2 = d->max_x - 1;
  567| 		d->update_y1 = 0;
  568| 		d->update_y2 = d->max_y - 1;
  569| 		d->modified = 1;
  570| 	} else {
  571| 		if (d->use_palette_per_line) {
  572| 			d->use_palette_per_line = 0;
  573| 			d->update_x1 = 0;
  574| 			d->update_x2 = d->max_x - 1;
  575| 			d->update_y1 = 0;
  576| 			d->update_y2 = d->max_y - 1;
  577| 			d->modified = 1;
  578| 		}
  579| 	}
  580| 
  581| 	if (!cpu->machine->x11_md.in_use) {
  582| 		/*  NOTE: 2 > 0, so this only updates the cursor, no
  583| 		    character cells.  */
  584| 		vga_update_textmode(cpu->machine, d, 0, 2, 0);
  585| 	}
  586| 
  587| 	if (d->modified) {
  588| 		if (d->cur_mode == MODE_CHARCELL)
  589| 			vga_update_text(cpu->machine, d, d->update_x1,
  590| 			    d->update_y1, d->update_x2, d->update_y2);
  591| 		else
  592| 			vga_update_graphics(cpu->machine, d, d->update_x1,
  593| 			    d->update_y1, d->update_x2, d->update_y2);
  594| 
  595| 		d->palette_modified = 0;
  596| 		d->modified = 0;
  597| 		d->update_x1 = 999999;
  598| 		d->update_x2 = -1;
  599| 		d->update_y1 = 999999;
  600| 		d->update_y2 = -1;
  601| 	}
  602| 
  603| 	if (d->n_is1_reads > N_IS1_READ_THRESHOLD)
  604| 		d->n_is1_reads = 0;
  605| }
  606| 
  607| 
  608| /*
  609|  *  Reads and writes to the VGA video memory (pixels).
  610|  */
  611| DEVICE_ACCESS(vga_graphics)
  612| {
  613| 	struct vga_data *d = (struct vga_data *) extra;
  614| 	int j, x=0, y=0, x2=0, y2=0, modified = 0;
  615| 	size_t i;
  616| 
  617| 	if (relative_addr + len >= GFX_ADDR_WINDOW)
  618| 		return 0;
  619| 
  620| 	if (d->cur_mode != MODE_GRAPHICS)
  621| 		return 1;
  622| 
  623| 	switch (d->graphics_mode) {
  624| 	case GRAPHICS_MODE_8BIT:
  625| 		y = relative_addr / d->max_x;
  626| 		x = relative_addr % d->max_x;
  627| 		y2 = (relative_addr+len-1) / d->max_x;
  628| 		x2 = (relative_addr+len-1) % d->max_x;
  629| 
  630| 		if (writeflag == MEM_WRITE) {
  631| 			if (relative_addr + len <= (uint64_t)d->gfx_mem_size) {	/* OB-15 */
  632| 				memcpy(d->gfx_mem + relative_addr, data, len);
  633| 				modified = 1;	/* OB-15b: only mark dirty when copied */
  634| 			} else {
  635| 				static int w_warned = 0;	/* #119: loud-once */
  636| 				if (!w_warned) {
  637| 					fatal("[ vga: gfx write 0x%x+%i beyond 0x%x; "
  638| 					    "ignored ]\n", (int)relative_addr, (int)len,
  639| 					    (int)d->gfx_mem_size);
  640| 					w_warned = 1;
  641| 				}
  642| 			}
  643| 		} else {
  644| 			if (relative_addr + len <= (uint64_t)d->gfx_mem_size)	/* OB-15 */
  645| 				memcpy(data, d->gfx_mem + relative_addr, len);
  646| 			else {
  647| 				static int r_warned = 0;	/* #119: loud-once */
  648| 				if (!r_warned) {
  649| 					fatal("[ vga: gfx read 0x%x+%i beyond 0x%x; "
  650| 					    "zero-filled ]\n", (int)relative_addr, (int)len,
  651| 					    (int)d->gfx_mem_size);
  652| 					r_warned = 1;
  653| 				}
  654| 				memset(data, 0, len);	/* OB-15c: don't leak uninit host memory */
  655| 			}
  656| 		}
  657| 		break;
  658| 	case GRAPHICS_MODE_4BIT:
  659| 		y = relative_addr * 8 / d->max_x;
  660| 		x = relative_addr * 8 % d->max_x;
  661| 		y2 = ((relative_addr+len)*8-1) / d->max_x;
  662| 		x2 = ((relative_addr+len)*8-1) % d->max_x;
  663| 		/*  TODO: color stuff  */
  664| 
  665| 		/*  Read/write d->gfx_mem in 4-bit color:  */
  666| 		if (writeflag == MEM_WRITE) {
  667| 			/*  i is byte index to write, j is bit index  */
  668| 			for (i=0; i<len; i++)
  669| 				for (j=0; j<8; j++) {
  670| 					int pixelmask = 1 << (7-j);
  671| 					int b = data[i] & pixelmask;
  672| 					int m = d->sequencer_reg[
  673| 					    VGA_SEQ_MAP_MASK] & 0x0f;
  674| 					uint32_t addr = (y * d->max_x + x +
  675| 					    i*8 + j) * d->bits_per_pixel / 8;
  676| 					unsigned char byte;
  677| 					if (!(d->graphcontr_reg[
  678| 					    VGA_GRAPHCONTR_MASK] & pixelmask))
  679| 						continue;
  680| 					if (addr >= d->gfx_mem_size)
  681| 						continue;
  682| 					byte = d->gfx_mem[addr];
  683| 					if (b && j&1)
  684| 						byte |= m << 4;
  685| 					if (b && !(j&1))
  686| 						byte |= m;
  687| 					if (!b && j&1)
  688| 						byte &= ~(m << 4);
  689| 					if (!b && !(j&1))
  690| 						byte &= ~m;
  691| 					d->gfx_mem[addr] = byte;
  692| 				}
  693| 			modified = 1;
  694| 		} else {
  695| 			fatal("TODO: 4 bit graphics read, mask=0x%02x\n",
  696| 			    d->sequencer_reg[VGA_SEQ_MAP_MASK]);
  697| 			for (i=0; i<len; i++)
  698| 				data[i] = random();
  699| 		}
  700| 		break;
  701| 	default:fatal("dev_vga: Unimplemented graphics mode %i\n",
  702| 		    d->graphics_mode);
  703| 		cpu->running = 0;
  704| 	}
  705| 
  706| 	if (modified) {
  707| 		d->modified = 1;
  708| 		if (x < d->update_x1)  d->update_x1 = x;
  709| 		if (x > d->update_x2)  d->update_x2 = x;
  710| 		if (y < d->update_y1)  d->update_y1 = y;
  711| 		if (y > d->update_y2)  d->update_y2 = y;
  712| 		if (x2 < d->update_x1)  d->update_x1 = x2;
  713| 		if (x2 > d->update_x2)  d->update_x2 = x2;
  714| 		if (y2 < d->update_y1)  d->update_y1 = y2;
  715| 		if (y2 > d->update_y2)  d->update_y2 = y2;
  716| 		if (y != y2) {
  717| 			d->update_x1 = 0;
  718| 			d->update_x2 = d->max_x - 1;
  719| 		}
  720| 	}
  721| 	return 1;
  722| }
  723| 
  724| 
  725| /*
  726|  *  Reads and writes the VGA video memory (charcells).
  727|  */
  728| DEVICE_ACCESS(vga)
  729| {
  730| 	struct vga_data *d = (struct vga_data *) extra;
  731| 	uint64_t idata = 0, odata = 0;
  732| 	int x, y, x2, y2, r, base;
  733| 	size_t i;
  734| 
  735| 	if (writeflag == MEM_WRITE)
  736| 		idata = memory_readmax64(cpu, data, len);
  737| 
```

## The data structures those files define (every field that exists)

### `src/devices/dev_vga.c` -- `struct vga_data {` (HEAD lines 69-149)

```c
   69| struct vga_data {
   70| 	uint64_t	videomem_base;
   71| 	uint64_t	control_base;
   72| 
   73| 	struct vfb_data *fb;
   74| 	uint32_t	fb_size;
   75| 
   76| 	int		fb_max_x;		/*  pixels  */
   77| 	int		fb_max_y;		/*  pixels  */
   78| 	int		max_x;			/*  charcells or pixels  */
   79| 	int		max_y;			/*  charcells or pixels  */
   80| 
   81| 	/*  Selects charcell mode or graphics mode:  */
   82| 	int		cur_mode;
   83| 
   84| 	/*  Common for text and graphics modes:  */
   85| 	int		pixel_repx, pixel_repy;
   86| 
   87| 	/*  Textmode:  */
   88| 	int		font_width;
   89| 	int		font_height;
   90| 	unsigned char	*font;
   91| 	size_t		charcells_size;
   92| 	unsigned char	*charcells;		/*  2 bytes per char  */
   93| 	unsigned char	*charcells_outputed;	/*  text  */
   94| 	unsigned char	*charcells_drawn;	/*  framebuffer  */
   95| 
   96| 	/*  Graphics:  */
   97| 	int		graphics_mode;
   98| 	int		bits_per_pixel;
   99| 	unsigned char	*gfx_mem;
  100| 	uint32_t	gfx_mem_size;
  101| 
  102| 	/*  Registers:  */
  103| 	int		attribute_state;	/*  0 or 1  */
  104| 	unsigned char	attribute_reg_select;
  105| 	unsigned char	attribute_reg[256];
  106| 
  107| 	unsigned char	misc_output_reg;
  108| 
  109| 	unsigned char	sequencer_reg_select;
  110| 	unsigned char	sequencer_reg[256];
  111| 
  112| 	unsigned char	graphcontr_reg_select;
  113| 	unsigned char	graphcontr_reg[256];
  114| 
  115| 	unsigned char	crtc_reg_select;
  116| 	unsigned char	crtc_reg[256];
  117| 
  118| 	/*  #271: one-shot latch for the unimplemented-video-mode warning
  119| 	    (crtc_reg[0xff] holding a mode byte that is not listed below).
  120| 	    Deliberately NOT cleared by register_reset(): a guest could
  121| 	    otherwise re-arm the warning by selecting an accepted mode in
  122| 	    between. Zeroed by the memset in dev_vga_init().  */
  123| 	int		invalid_mode_warned;
  124| 
  125| 	unsigned char	palette_read_index;
  126| 	char		palette_read_subindex;
  127| 	unsigned char	palette_write_index;
  128| 	char		palette_write_subindex;
  129| 
  130| 	int		current_retrace_line;
  131| 	int		input_status_1;
  132| 
  133| 	/*  Palette per scanline during retrace:  */
  134| 	unsigned char	*retrace_palette;
  135| 	int		use_palette_per_line;
  136| 	int64_t		n_is1_reads;
  137| 
  138| 	/*  Misc.:  */
  139| 	int		console_handle;
  140| 
  141| 	int		cursor_x;
  142| 	int		cursor_y;
  143| 
  144| 	int		modified;
  145| 	int		palette_modified;
  146| 	int		update_x1;
  147| 	int		update_y1;
  148| 	int		update_x2;
  149| 	int		update_y2;
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

End with one line: `FIXDRAFT_VGAGFXWINDOWEND: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
