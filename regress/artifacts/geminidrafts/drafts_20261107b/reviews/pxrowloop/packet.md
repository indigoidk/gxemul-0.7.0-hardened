# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `pxrowloop` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `pxrowloop`, state `open`)

**title:** src/devices/dev_px.c:351,396,426-434 -- the erasecols/eraserows fill takes its row-loop length from a guest DMA word (up to about 2^29 rows) and records each row in update_y2, so one command costs that many loop passes and leaves an out-of-range update rectangle; rows outside the framebuffer are skipped -- WRONG-RESULT

**state_note (head):** 

**The drafter's own reading:** STILL PRESENT: YES -- 426

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_px.c b/src/devices/dev_px.c
index 07b4d12c..08051673 100644
--- a/src/devices/dev_px.c
+++ b/src/devices/dev_px.c
@@ -423,6 +423,10 @@ void dev_px_dma(struct cpu *cpu, uint32_t sys_addr, struct px_data *d)
 		if (x2 > d->vfb_data->update_x2)
 			d->vfb_data->update_x2 = x2;
 
+		/*  #pxrowloop: clamp lw to the framebuffer boundaries  */
+		if (y2 + lw > PX_YSIZE)
+			lw = PX_YSIZE - y2;
+
 		for (fb_y=y; fb_y < y2 + lw; fb_y ++) {
 			if (fb_y >= 0 && fb_y < PX_YSIZE && x >= 0 && x2 <= PX_XSIZE && x2 >= x)	/* OB-3 */
 			memcpy(d->vfb_data->framebuffer + (fb_y * PX_XSIZE + x)
```

## Every edited function, after the fix

### `src/devices/dev_px.c` -- post-edit lines 138-568 (`+` marks a line the diff added or the point of a deletion)

```c
  138|  void dev_px_dma(struct cpu *cpu, uint32_t sys_addr, struct px_data *d)
  139|  {
  140|  	unsigned char dma_buf[32768];
  141|  	size_t dma_len = sizeof(dma_buf);
  142|  	int bytesperpixel;
     | [... lines 143-315 not shown ...]
  316|  
  317|  			if (span_len > PX_XSIZE)
  318|  				span_len = PX_XSIZE;
  319|  
  320|  			/*  debug("  span %i: len=%i src=%i dst=%i\n",
  321|  			    spannr, span_len, span_src, span_dst);  */
  322|  
  323|  			if (span_dst < (uint32_t)PX_YSIZE && span_src < (uint32_t)PX_YSIZE)	/* OB-3: span row bound */
  324|  			memmove(d->vfb_data->framebuffer + span_dst *
  325|  			    PX_XSIZE * bytesperpixel, d->vfb_data->framebuffer
  326|  			    + span_src * PX_XSIZE * bytesperpixel, span_len *
  327|  			    bytesperpixel);
  328|  
  329|  			d->vfb_data->update_x1 = 0; d->vfb_data->update_x2 =
  330|  			    PX_XSIZE-1;
  331|  			if ((int32_t)span_dst < d->vfb_data->update_y1)
  332|  				d->vfb_data->update_y1 = span_dst;
  333|  			if ((int32_t)span_dst > d->vfb_data->update_y2)
  334|  				d->vfb_data->update_y2 = span_dst;
  335|  			if ((int32_t)span_src < d->vfb_data->update_y1)
  336|  				d->vfb_data->update_y1 = span_src;
  337|  			if ((int32_t)span_src > d->vfb_data->update_y2)
  338|  				d->vfb_data->update_y2 = span_src;
  339|  		}
  340|  	}
  341|  
  342|  	/*  NetBSD and Ultrix erasecols/eraserows  */
  343|  	if (cmdword == 0x411) {
  344|  		uint32_t v1, v2, attr;
  345|  		int32_t lw;
  346|  		int x,y,x2,y2;
  347|  		int fb_y;
  348|  		int bg_r, bg_g, bg_b;
  349|  		unsigned char pixels[PX_XSIZE * 3];
  350|  
  351|  		lw = px_readword(cpu, dma_buf, 16);
  352|  		attr = px_readword(cpu, dma_buf, 20);
  353|  		v1 = px_readword(cpu, dma_buf, 24);
  354|  		v2 = px_readword(cpu, dma_buf, 28);
  355|  #if 0
  356|  		if (cpu->byte_order == EMUL_LITTLE_ENDIAN)
  357|  			lw = dma_buf[16] + (dma_buf[17] << 8) +
  358|  			    (dma_buf[18] << 16) + (dma_buf[19] << 24);
  359|  		else
  360|  			lw = dma_buf[19] + (dma_buf[18] << 8) +
  361|  			    (dma_buf[17] << 16) + (dma_buf[16] << 24);
  362|  
  363|  		if (cpu->byte_order == EMUL_LITTLE_ENDIAN)
  364|  			v1 = dma_buf[24] + (dma_buf[25] << 8) +
  365|  			    (dma_buf[26] << 16) + (dma_buf[27] << 24);
  366|  		else
  367|  			v1 = dma_buf[27] + (dma_buf[26] << 8) +
  368|  			    (dma_buf[25] << 16) + (dma_buf[24] << 24);
  369|  
  370|  		if (cpu->byte_order == EMUL_LITTLE_ENDIAN)
  371|  			v2 = dma_buf[28] + (dma_buf[29] << 8) +
  372|  			    (dma_buf[30] << 16) + (dma_buf[31] << 24);
  373|  		else
  374|  			v2 = dma_buf[31] + (dma_buf[30] << 8) +
  375|  			    (dma_buf[29] << 16) + (dma_buf[28] << 24);
  376|  #endif
  377|  		bg_r = (attr >> 16) & 255;
  378|  		bg_g = (attr >> 8) & 255;
  379|  		bg_b = attr & 255;
  380|  		if (bg_r == 0)
  381|  			bg_r = bg_g = bg_b = 0;
  382|  		else
  383|  		if (bg_r == 7)
  384|  			bg_r = bg_g = bg_b = 192;
  385|  		else
  386|  			bg_r = bg_g = bg_b = 255;
  387|  
  388|  		v1 -= lw;
  389|  		v2 -= lw;
  390|  
  391|  		x = (v1 >> 19) & 2047;
  392|  		y = (v1 >> 3) & 1023;
  393|  		x2 = (v2 >> 19) & 2047;
  394|  		y2 = (v2 >> 3) & 1023;
  395|  
  396|  		lw = (lw + 1) >> 2;
  397|  
  398|  		/*  OB-3b: a guest can drive x2 < x; clamp so the memset()/
  399|  		    memcpy() of (x2 - x) below is never a negative width.  */
  400|  		if (x2 < x)
  401|  			x2 = x;
  402|  		if (x2 - x > PX_XSIZE)
  403|  			x2 = PX_XSIZE;
  404|  
  405|  		if (px_debug)
  406|  			debug("[ px: clear/fill: v1 = 0x%08x  v2 = 0x%08x "
  407|  			    "lw=%i x=%i y=%i x2=%i y2=%i ]\n", (int)v1, (int)v2,
  408|  			    lw, x,y, x2,y2);
  409|  
  410|  		if (bytesperpixel == 3) {
  411|  			int xi;
  412|  			for (xi=0; xi<x2-x; xi++) {
  413|  				/*  TODO:  rgb order?  */
  414|  				pixels[xi*3 + 0] = bg_r;
  415|  				pixels[xi*3 + 1] = bg_g;
  416|  				pixels[xi*3 + 2] = bg_b;
  417|  			}
  418|  		} else
  419|  			memset(pixels, attr, (x2 - x) * bytesperpixel);
  420|  
  421|  		if (x < d->vfb_data->update_x1)
  422|  			d->vfb_data->update_x1 = x;
  423|  		if (x2 > d->vfb_data->update_x2)
  424|  			d->vfb_data->update_x2 = x2;
  425|  
  426|+ 		/*  #pxrowloop: clamp lw to the framebuffer boundaries  */
  427|+ 		if (y2 + lw > PX_YSIZE)
  428|+ 			lw = PX_YSIZE - y2;
  429|+ 
  430|  		for (fb_y=y; fb_y < y2 + lw; fb_y ++) {
  431|  			if (fb_y >= 0 && fb_y < PX_YSIZE && x >= 0 && x2 <= PX_XSIZE && x2 >= x)	/* OB-3 */
  432|  			memcpy(d->vfb_data->framebuffer + (fb_y * PX_XSIZE + x)
  433|  			    * bytesperpixel, pixels, (x2-x)*bytesperpixel);
  434|  
  435|  			if (fb_y < d->vfb_data->update_y1)
  436|  				d->vfb_data->update_y1 = fb_y;
  437|  			if (fb_y > d->vfb_data->update_y2)
  438|  				d->vfb_data->update_y2 = fb_y;
  439|  		}
  440|  	}
  441|  
  442|  	/*  NetBSD and Ultrix putchar  */
  443|  	if (cmdword == 0xa21) {
  444|  		/*  Ugly test code:  */
  445|  		unsigned char pixels[16 * 3];
  446|  		int pixels_len = 16;
  447|  		uint32_t v1, v2, fgcolor, bgcolor;
  448|  		int x, y, x2,y2, i, maxi;
  449|  		int xbit;
  450|  		int suby;
  451|  		int fg_r, fg_g, fg_b;
  452|  		int bg_r, bg_g, bg_b;
  453|  
  454|  		v1 = px_readword(cpu, dma_buf, 52);
  455|  		v2 = px_readword(cpu, dma_buf, 56);
  456|  		fgcolor = px_readword(cpu, dma_buf, 16 * 4);
  457|  		bgcolor = px_readword(cpu, dma_buf, 29 * 4);
  458|  
  459|  		/*
  460|  		 *  TODO:  Which one is r, which one is g, and which one is b?
  461|  		 *  TODO 2:  Use the BT459 palette, these values are hardcoded
  462|  		 *  for NetBSD and Ultrix grayscale only.
  463|  		 */
  464|  		fg_r = (fgcolor >> 16) & 255;
  465|  		fg_g = (fgcolor >> 8) & 255;
  466|  		fg_b = fgcolor & 255;
  467|  		if (fg_r == 0)
  468|  			fg_r = fg_g = fg_b = 0;
  469|  		else
  470|  		if (fg_r == 7)
  471|  			fg_r = fg_g = fg_b = 192;
  472|  		else
  473|  			fg_r = fg_g = fg_b = 255;
  474|  
  475|  		bg_r = (bgcolor >> 16) & 255;
  476|  		bg_g = (bgcolor >> 8) & 255;
  477|  		bg_b = bgcolor & 255;
  478|  		if (bg_r == 0)
  479|  			bg_r = bg_g = bg_b = 0;
  480|  		else
  481|  		if (bg_r == 7)
  482|  			bg_r = bg_g = bg_b = 192;
  483|  		else
  484|  			bg_r = bg_g = bg_b = 255;
  485|  
  486|  		x = (v1 >> 19) & 2047;
  487|  		y = ((v1 - 63) >> 3) & 1023;
  488|  		x2 = (v2 >> 19) & 2047;
  489|  		y2 = ((v2 - 63) >> 3) & 1023;
     | [... lines 490-538 not shown ...]
  539|  						    j*2 + 0] & (1 << xbit))?
  540|  						    (fgcolor & 255) :
  541|  						    (bgcolor & 255);
  542|  						pixels[xbit + 8] = (dma_buf[i*4
  543|  						    + j*2 + 1] & (1 << xbit))?
  544|  						    (fgcolor & 255) :
  545|  						    (bgcolor & 255);
  546|  					}
  547|  				}
  548|  
  549|  				if (y + suby >= 0 && y + suby < PX_YSIZE && x >= 0 && pixels_len >= 0 && pixels_len <= 16 && x + pixels_len <= PX_XSIZE)	/* OB-3 */
  550|  					memcpy(d->vfb_data->framebuffer + ((y+suby)
  551|  				    * PX_XSIZE + x) * bytesperpixel,
  552|  				    pixels, pixels_len * bytesperpixel);
  553|  
  554|  				if (y+suby < d->vfb_data->update_y1)
  555|  					d->vfb_data->update_y1 = y+suby;
  556|  				if (y+suby > d->vfb_data->update_y2)
  557|  					d->vfb_data->update_y2 = y+suby;
  558|  
  559|  				suby ++;
  560|  			}
  561|  
  562|  		if (x < d->vfb_data->update_x1)
  563|  			d->vfb_data->update_x1 = x;
  564|  		if (x2 > d->vfb_data->update_x2)
  565|  			d->vfb_data->update_x2 = x2;
  566|  		}
  567|  	}
  568|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_PXROWLOOP: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_PXROWLOOP: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
