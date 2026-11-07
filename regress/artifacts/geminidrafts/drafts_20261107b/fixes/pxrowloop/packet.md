# GXemul hardened fork -- DRAFT A FIX for one filed issue, `pxrowloop` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `pxrowloop`, state `open`, severity `LOW`)

**title:** src/devices/dev_px.c:351,396,426-434 -- the erasecols/eraserows fill takes its row-loop length from a guest DMA word (up to about 2^29 rows) and records each row in update_y2, so one command costs that many loop passes and leaves an out-of-range update rectangle; rows outside the framebuffer are skipped -- WRONG-RESULT

**state_note (head):**



**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- clamp lw to the framebuffer boundaries before the loop

## The code at the cited lines

### `src/devices/dev_px.c` around the row's cited line 351 (HEAD 8d9df658, lines 231-471)

```c
  231| 		debug(" ]\n");
  232| 	}
  233| 
  234| 	/*  NetBSD and Ultrix copyspans  */
  235| 	if (cmdword == 0x405) {
  236| 		uint32_t nspans, lw;
  237| 		uint32_t spannr, ofs;
  238| 		uint32_t span_len, span_src, span_dst;
  239| 		/*  unsigned char pixels[PX_XSIZE * 3];  */
  240| 
  241| 		if (cpu->byte_order == EMUL_LITTLE_ENDIAN)
  242| 			nspans = dma_buf[4] + (dma_buf[5] << 8) +
  243| 			    (dma_buf[6] << 16) + (dma_buf[7] << 24);
  244| 		else
  245| 			nspans = dma_buf[7] + (dma_buf[6] << 8) +
  246| 			    (dma_buf[5] << 16) + (dma_buf[4] << 24);
  247| 
  248| 		if (cpu->byte_order == EMUL_LITTLE_ENDIAN)
  249| 			lw = dma_buf[16] + (dma_buf[17] << 8) +
  250| 			    (dma_buf[18] << 16) + (dma_buf[19] << 24);
  251| 		else
  252| 			lw = dma_buf[19] + (dma_buf[18] << 8) +
  253| 			    (dma_buf[17] << 16) + (dma_buf[16] << 24);
  254| 
  255| 		nspans >>= 24;
  256| 		/*  Why not this?  lw = (lw + 1) >> 2;  */
  257| 
  258| 		if (px_debug)
  259| 			debug("[ px: copyspans:  nspans = %i, lw = %i ]\n", nspans, lw);
  260| 
  261| 		/*  Reread copyspans command if it wasn't completely read:  */
  262| 		if (dma_len < 4*(5 + nspans*3)) {
  263| 			dma_len = 4 * (5+nspans*3);
  264| 			if (d->type == DEV_PX_TYPE_PX)
  265| 				cpu->memory_rw(cpu, cpu->mem, sys_addr,
  266| 				    dma_buf, dma_len, MEM_READ,
  267| 				    NO_EXCEPTIONS | PHYSICAL);
  268| 			else
  269| 				{
  270| 					/*  #207: (Codex/Fable) bound the SRAM source span
  271| 					    so a guest-forced dma_len can't read past
  272| 					    d->sram[] (128 KiB) into adjacent host heap.  */
  273| 					size_t so = sys_addr & 0x1ffff;
  274| 					size_t sl = so < sizeof(d->sram)?
  275| 					    sizeof(d->sram) - so : 0;
  276| 					memmove(dma_buf, &d->sram[so],
  277| 					    dma_len < sl? dma_len : sl);
  278| 				}
  279| 		}
  280| 
  281| 		ofs = 4*5;
  282| 		for (spannr=0; spannr<nspans; spannr++) {
  283| 			if (cpu->byte_order == EMUL_LITTLE_ENDIAN)
  284| 				span_len = dma_buf[ofs+0] + (dma_buf[ofs+1] <<
  285| 				    8) + (dma_buf[ofs+2] << 16) +
  286| 				    (dma_buf[ofs+3] << 24);
  287| 			else
  288| 				span_len = dma_buf[ofs+3] + (dma_buf[ofs+2] <<
  289| 				    8) + (dma_buf[ofs+1] << 16) +
  290| 				    (dma_buf[ofs+0] << 24);
  291| 			ofs += 4;
  292| 
  293| 			if (cpu->byte_order == EMUL_LITTLE_ENDIAN)
  294| 				span_src = dma_buf[ofs+0] + (dma_buf[ofs+1] <<
  295| 				    8) + (dma_buf[ofs+2] << 16) +
  296| 				    (dma_buf[ofs+3] << 24);
  297| 			else
  298| 				span_src = dma_buf[ofs+3] + (dma_buf[ofs+2] <<
  299| 				    8) + (dma_buf[ofs+1] << 16) +
  300| 				    (dma_buf[ofs+0] << 24);
  301| 			ofs += 4;
  302| 
  303| 			if (cpu->byte_order == EMUL_LITTLE_ENDIAN)
  304| 				span_dst = dma_buf[ofs+0] + (dma_buf[ofs+1] <<
  305| 				    8) + (dma_buf[ofs+2] << 16) +
  306| 				    (dma_buf[ofs+3] << 24);
  307| 			else
  308| 				span_dst = dma_buf[ofs+3] + (dma_buf[ofs+2] <<
  309| 				    8) + (dma_buf[ofs+1] << 16) +
  310| 				    (dma_buf[ofs+0] << 24);
  311| 			ofs += 4;
  312| 
  313| 			span_len >>= 3;
  314| 			span_dst >>= 3;
  315| 			span_src >>= 3;
  316| 
  317| 			if (span_len > PX_XSIZE)
  318| 				span_len = PX_XSIZE;
  319| 
  320| 			/*  debug("  span %i: len=%i src=%i dst=%i\n",
  321| 			    spannr, span_len, span_src, span_dst);  */
  322| 
  323| 			if (span_dst < (uint32_t)PX_YSIZE && span_src < (uint32_t)PX_YSIZE)	/* OB-3: span row bound */
  324| 			memmove(d->vfb_data->framebuffer + span_dst *
  325| 			    PX_XSIZE * bytesperpixel, d->vfb_data->framebuffer
  326| 			    + span_src * PX_XSIZE * bytesperpixel, span_len *
  327| 			    bytesperpixel);
  328| 
  329| 			d->vfb_data->update_x1 = 0; d->vfb_data->update_x2 =
  330| 			    PX_XSIZE-1;
  331| 			if ((int32_t)span_dst < d->vfb_data->update_y1)
  332| 				d->vfb_data->update_y1 = span_dst;
  333| 			if ((int32_t)span_dst > d->vfb_data->update_y2)
  334| 				d->vfb_data->update_y2 = span_dst;
  335| 			if ((int32_t)span_src < d->vfb_data->update_y1)
  336| 				d->vfb_data->update_y1 = span_src;
  337| 			if ((int32_t)span_src > d->vfb_data->update_y2)
  338| 				d->vfb_data->update_y2 = span_src;
  339| 		}
  340| 	}
  341| 
  342| 	/*  NetBSD and Ultrix erasecols/eraserows  */
  343| 	if (cmdword == 0x411) {
  344| 		uint32_t v1, v2, attr;
  345| 		int32_t lw;
  346| 		int x,y,x2,y2;
  347| 		int fb_y;
  348| 		int bg_r, bg_g, bg_b;
  349| 		unsigned char pixels[PX_XSIZE * 3];
  350| 
  351| 		lw = px_readword(cpu, dma_buf, 16);
  352| 		attr = px_readword(cpu, dma_buf, 20);
  353| 		v1 = px_readword(cpu, dma_buf, 24);
  354| 		v2 = px_readword(cpu, dma_buf, 28);
  355| #if 0
  356| 		if (cpu->byte_order == EMUL_LITTLE_ENDIAN)
  357| 			lw = dma_buf[16] + (dma_buf[17] << 8) +
  358| 			    (dma_buf[18] << 16) + (dma_buf[19] << 24);
  359| 		else
  360| 			lw = dma_buf[19] + (dma_buf[18] << 8) +
  361| 			    (dma_buf[17] << 16) + (dma_buf[16] << 24);
  362| 
  363| 		if (cpu->byte_order == EMUL_LITTLE_ENDIAN)
  364| 			v1 = dma_buf[24] + (dma_buf[25] << 8) +
  365| 			    (dma_buf[26] << 16) + (dma_buf[27] << 24);
  366| 		else
  367| 			v1 = dma_buf[27] + (dma_buf[26] << 8) +
  368| 			    (dma_buf[25] << 16) + (dma_buf[24] << 24);
  369| 
  370| 		if (cpu->byte_order == EMUL_LITTLE_ENDIAN)
  371| 			v2 = dma_buf[28] + (dma_buf[29] << 8) +
  372| 			    (dma_buf[30] << 16) + (dma_buf[31] << 24);
  373| 		else
  374| 			v2 = dma_buf[31] + (dma_buf[30] << 8) +
  375| 			    (dma_buf[29] << 16) + (dma_buf[28] << 24);
  376| #endif
  377| 		bg_r = (attr >> 16) & 255;
  378| 		bg_g = (attr >> 8) & 255;
  379| 		bg_b = attr & 255;
  380| 		if (bg_r == 0)
  381| 			bg_r = bg_g = bg_b = 0;
  382| 		else
  383| 		if (bg_r == 7)
  384| 			bg_r = bg_g = bg_b = 192;
  385| 		else
  386| 			bg_r = bg_g = bg_b = 255;
  387| 
  388| 		v1 -= lw;
  389| 		v2 -= lw;
  390| 
  391| 		x = (v1 >> 19) & 2047;
  392| 		y = (v1 >> 3) & 1023;
  393| 		x2 = (v2 >> 19) & 2047;
  394| 		y2 = (v2 >> 3) & 1023;
  395| 
  396| 		lw = (lw + 1) >> 2;
  397| 
  398| 		/*  OB-3b: a guest can drive x2 < x; clamp so the memset()/
  399| 		    memcpy() of (x2 - x) below is never a negative width.  */
  400| 		if (x2 < x)
  401| 			x2 = x;
  402| 		if (x2 - x > PX_XSIZE)
  403| 			x2 = PX_XSIZE;
  404| 
  405| 		if (px_debug)
  406| 			debug("[ px: clear/fill: v1 = 0x%08x  v2 = 0x%08x "
  407| 			    "lw=%i x=%i y=%i x2=%i y2=%i ]\n", (int)v1, (int)v2,
  408| 			    lw, x,y, x2,y2);
  409| 
  410| 		if (bytesperpixel == 3) {
  411| 			int xi;
  412| 			for (xi=0; xi<x2-x; xi++) {
  413| 				/*  TODO:  rgb order?  */
  414| 				pixels[xi*3 + 0] = bg_r;
  415| 				pixels[xi*3 + 1] = bg_g;
  416| 				pixels[xi*3 + 2] = bg_b;
  417| 			}
  418| 		} else
  419| 			memset(pixels, attr, (x2 - x) * bytesperpixel);
  420| 
  421| 		if (x < d->vfb_data->update_x1)
  422| 			d->vfb_data->update_x1 = x;
  423| 		if (x2 > d->vfb_data->update_x2)
  424| 			d->vfb_data->update_x2 = x2;
  425| 
  426| 		for (fb_y=y; fb_y < y2 + lw; fb_y ++) {
  427| 			if (fb_y >= 0 && fb_y < PX_YSIZE && x >= 0 && x2 <= PX_XSIZE && x2 >= x)	/* OB-3 */
  428| 			memcpy(d->vfb_data->framebuffer + (fb_y * PX_XSIZE + x)
  429| 			    * bytesperpixel, pixels, (x2-x)*bytesperpixel);
  430| 
  431| 			if (fb_y < d->vfb_data->update_y1)
  432| 				d->vfb_data->update_y1 = fb_y;
  433| 			if (fb_y > d->vfb_data->update_y2)
  434| 				d->vfb_data->update_y2 = fb_y;
  435| 		}
  436| 	}
  437| 
  438| 	/*  NetBSD and Ultrix putchar  */
  439| 	if (cmdword == 0xa21) {
  440| 		/*  Ugly test code:  */
  441| 		unsigned char pixels[16 * 3];
  442| 		int pixels_len = 16;
  443| 		uint32_t v1, v2, fgcolor, bgcolor;
  444| 		int x, y, x2,y2, i, maxi;
  445| 		int xbit;
  446| 		int suby;
  447| 		int fg_r, fg_g, fg_b;
  448| 		int bg_r, bg_g, bg_b;
  449| 
  450| 		v1 = px_readword(cpu, dma_buf, 52);
  451| 		v2 = px_readword(cpu, dma_buf, 56);
  452| 		fgcolor = px_readword(cpu, dma_buf, 16 * 4);
  453| 		bgcolor = px_readword(cpu, dma_buf, 29 * 4);
  454| 
  455| 		/*
  456| 		 *  TODO:  Which one is r, which one is g, and which one is b?
  457| 		 *  TODO 2:  Use the BT459 palette, these values are hardcoded
  458| 		 *  for NetBSD and Ultrix grayscale only.
  459| 		 */
  460| 		fg_r = (fgcolor >> 16) & 255;
  461| 		fg_g = (fgcolor >> 8) & 255;
  462| 		fg_b = fgcolor & 255;
  463| 		if (fg_r == 0)
  464| 			fg_r = fg_g = fg_b = 0;
  465| 		else
  466| 		if (fg_r == 7)
  467| 			fg_r = fg_g = fg_b = 192;
  468| 		else
  469| 			fg_r = fg_g = fg_b = 255;
  470| 
  471| 		bg_r = (bgcolor >> 16) & 255;
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

End with one line: `FIXDRAFT_PXROWLOOP: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
