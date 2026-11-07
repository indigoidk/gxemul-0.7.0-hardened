# GXemul hardened fork -- DRAFT A FIX for one filed issue, `fbscaledownoob` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `fbscaledownoob`, state `open`, severity `LOW`)

**title:** src/devices/dev_fb.c:634-656 + src/devices/fb_include.c:232-239 -- the tick clamps update_y2 to the last visible row and then rounds it up to a multiple of the scale-down factor, so the redraw loop can reach the row at visible_ysize and the scale-down redraw reads past the end of the framebuffer -- OOB-READ (X11 build, scale-down factor above 1)

**state_note (head):**



**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- Rounding up can push update_y2 past the end of the framebuffer, causing OOB reads.

## The code at the cited lines

### `src/devices/dev_fb.c` around the row's cited line 634 (HEAD 2d25df65, lines 589-679)

```c
  589| 		      d->fb_window->OLD_cursor_xsize)) ||
  590| 		     (d->update_x1 <  d->fb_window->OLD_cursor_x &&
  591| 		      d->update_x2 >= (d->fb_window->OLD_cursor_x +
  592| 		      d->fb_window->OLD_cursor_xsize)) ) &&
  593| 		   ( (d->update_y1 >= d->fb_window->OLD_cursor_y &&
  594| 		      d->update_y1 < (d->fb_window->OLD_cursor_y +
  595| 		      d->fb_window->OLD_cursor_ysize)) ||
  596| 		     (d->update_y2 >= d->fb_window->OLD_cursor_y &&
  597| 		      d->update_y2 < (d->fb_window->OLD_cursor_y +
  598| 		      d->fb_window->OLD_cursor_ysize)) ||
  599| 		     (d->update_y1 <  d->fb_window->OLD_cursor_y &&
  600| 		      d->update_y2 >= (d->fb_window->OLD_cursor_y +
  601| 		     d->fb_window->OLD_cursor_ysize)) ) )
  602| 			need_to_redraw_cursor = 1;
  603| 	}
  604| 
  605| 	if (need_to_redraw_cursor) {
  606| 		/*  Remove old cursor, if any:  */
  607| 		if (d->fb_window->OLD_cursor_on) {
  608| 			XPutImage(d->fb_window->x11_display,
  609| 			    d->fb_window->x11_fb_window,
  610| 			    d->fb_window->x11_fb_gc, d->fb_window->fb_ximage,
  611| 			    d->fb_window->OLD_cursor_x/d->vfb_scaledown,
  612| 			    d->fb_window->OLD_cursor_y/d->vfb_scaledown,
  613| 			    d->fb_window->OLD_cursor_x/d->vfb_scaledown,
  614| 			    d->fb_window->OLD_cursor_y/d->vfb_scaledown,
  615| 			    d->fb_window->OLD_cursor_xsize/d->vfb_scaledown + 1,
  616| 			    d->fb_window->OLD_cursor_ysize/d->vfb_scaledown +1);
  617| 		}
  618| 	}
  619| #endif
  620| 
  621| 	if (d->update_x2 != -1) {
  622| #ifdef WITH_X11
  623| 		int y;
  624| 		int addr, addr2;
  625| #endif
  626| 		int q = d->vfb_scaledown;
  627| 
  628| 		if (d->update_x1 >= d->visible_xsize)
  629| 			d->update_x1 = d->visible_xsize - 1;
  630| 		if (d->update_x2 >= d->visible_xsize)
  631| 			d->update_x2 = d->visible_xsize - 1;
  632| 		if (d->update_y1 >= d->visible_ysize)
  633| 			d->update_y1 = d->visible_ysize - 1;
  634| 		if (d->update_y2 >= d->visible_ysize)
  635| 			d->update_y2 = d->visible_ysize - 1;
  636| 
  637| 		/*  Without these, we might miss the rightmost/bottom pixel:  */
  638| 		d->update_x2 += (q - 1);
  639| 		d->update_y2 += (q - 1);
  640| 
  641| 		d->update_x1 = d->update_x1 / q * q;
  642| 		d->update_x2 = d->update_x2 / q * q;
  643| 		d->update_y1 = d->update_y1 / q * q;
  644| 		d->update_y2 = d->update_y2 / q * q;
  645| 
  646| #ifdef WITH_X11
  647| 		addr  = d->update_y1 * d->bytes_per_line +
  648| 		    d->update_x1 * d->bit_depth / 8;
  649| 		addr2 = d->update_y1 * d->bytes_per_line +
  650| 		    d->update_x2 * d->bit_depth / 8;
  651| 
  652| 		for (y=d->update_y1; y<=d->update_y2; y+=q) {
  653| 			d->redraw_func(d, addr, addr2 - addr);
  654| 			addr  += d->bytes_per_line * q;
  655| 			addr2 += d->bytes_per_line * q;
  656| 		}
  657| 
  658| 		XPutImage(d->fb_window->x11_display, d->fb_window->
  659| 		    x11_fb_window, d->fb_window->x11_fb_gc, d->fb_window->
  660| 		    fb_ximage, d->update_x1/d->vfb_scaledown, d->update_y1/
  661| 		    d->vfb_scaledown, d->update_x1/d->vfb_scaledown,
  662| 		    d->update_y1/d->vfb_scaledown,
  663| 		    (d->update_x2 - d->update_x1)/d->vfb_scaledown + 1,
  664| 		    (d->update_y2 - d->update_y1)/d->vfb_scaledown + 1);
  665| 
  666| 		need_to_flush_x11 = 1;
  667| #endif
  668| 
  669| 		d->update_x1 = d->update_y1 = 99999;
  670| 		d->update_x2 = d->update_y2 = -1;
  671| 	}
  672| 
  673| #ifdef WITH_X11
  674| 	if (need_to_redraw_cursor) {
  675| 		/*  Paint new cursor:  */
  676| 		if (d->fb_window->cursor_on) {
  677| 			x11_redraw_cursor(cpu->machine,
  678| 			    d->fb_window->fb_number);
  679| 			d->fb_window->OLD_cursor_on = d->fb_window->cursor_on;
```

### `src/devices/fb_include.c` around the row's cited line 232 (HEAD 2d25df65, lines 187-277)

```c
  187| 
  188| 				r *= 8;
  189| 				g *= 4;
  190| 				b *= 8;
  191| 				break;
  192| 			default:
  193| 				r = g = b = random() & 255;
  194| 			}
  195| 
  196| 			macro_put_pixel;
  197| 			x++;
  198| 		}
  199| 	}
  200| 
  201| #else	/*  FB_SCALEDOWN  */
  202| 
  203| 	/*  scaledown > 1:  */
  204| 	int scaledown = d->vfb_scaledown;
  205| 	int scaledownXscaledown = scaledown * scaledown;
  206| 
  207| 	/*  Which framebuffer pixel does addr correspond to?  */
  208| 	pixel = addr * 8 / d->bit_depth;
  209| 	y = pixel / d->xsize;
  210| 	x = pixel % d->xsize;
  211| 
  212| 	/*  How many framebuffer pixels?  */
  213| 	npixels = len * 8 / d->bit_depth;
  214| 
  215| 	/*  Which x11 pixel?  */
  216| 	x /= scaledown;
  217| 	y /= scaledown;
  218| 
  219| 	/*  How many x11 pixels:  */
  220| 	npixels /= scaledown;
  221| 	if (npixels == 0)
  222| 		npixels = 1;
  223| 
  224| 	if (d->bit_depth < 8) {
  225| 		for (pixel=0; pixel<npixels; pixel++) {
  226| 			int subx, suby, r, g, b;
  227| 			int64_t color_r = 0, color_g = 0, color_b = 0;
  228| 			for (suby=0; suby<scaledown; suby++)
  229| 			    for (subx=0; subx<scaledown; subx++) {
  230| 				int fb_x, fb_y, fb_addr, c;
  231| 
  232| 				fb_x = x * scaledown + subx;
  233| 				fb_y = y * scaledown + suby;
  234| 				fb_addr = fb_y * d->xsize + fb_x;
  235| 				fb_addr = fb_addr * d->bit_depth;
  236| 				/*  fb_addr is now which _bit_ in
  237| 				    the framebuffer  */
  238| 
  239| 				c = d->framebuffer[fb_addr >> 3];
  240| 				fb_addr &= 7;
  241| 
  242| 				/*  HPC is reverse:  */
  243| 				if (d->vfb_type == VFB_HPC || d->vfb_type == VFB_REVERSEBITS)
  244| 					fb_addr = 8 - d->bit_depth - fb_addr;
  245| 
  246| 				c = (c >> fb_addr) & ((1<<d->bit_depth) - 1);
  247| 				/*  c <<= (8 - d->bit_depth);  */
  248| 
  249| 				r = d->rgb_palette[c*3 + 0];
  250| 				g = d->rgb_palette[c*3 + 1];
  251| 				b = d->rgb_palette[c*3 + 2];
  252| 
  253| 				color_r += r;
  254| 				color_g += g;
  255| 				color_b += b;
  256| 			    }
  257| 
  258| 			r = color_r / scaledownXscaledown;
  259| 			g = color_g / scaledownXscaledown;
  260| 			b = color_b / scaledownXscaledown;
  261| 			macro_put_pixel;
  262| 			x++;
  263| 		}
  264| 	} else if (d->bit_depth == 8) {
  265| 		for (pixel=0; pixel<npixels; pixel++) {
  266| 			int subx, suby, r, g, b;
  267| 			int64_t color_r = 0, color_g = 0, color_b = 0;
  268| 			for (suby=0; suby<scaledown; suby++)
  269| 			    for (subx=0; subx<scaledown; subx++) {
  270| 				int fb_x, fb_y, fb_addr, c;
  271| 
  272| 				fb_x = x * scaledown + subx;
  273| 				fb_y = y * scaledown + suby;
  274| 				fb_addr = fb_y * d->xsize + fb_x;
  275| 				/*  fb_addr is which _byte_ in framebuffer  */
  276| 				c = d->framebuffer[fb_addr] * 3;
  277| 				r = d->rgb_palette[c + 0];
```

## WHAT TO RETURN

1. One line: `STILL PRESENT: YES|NO|UNSETTLED -- <the line of code shown that shows it>`.  The cited line numbers may have
   moved since the row was written; judge from the code shown.  If NO, say what already fixed it and STOP (no edits).
2. If YES: EXACTLY ONE fenced ```json block -- a list of edits, the smallest fix that removes the defect without changing any
   other behaviour: [{"file": "src/...", "old": "<exact text from the code above, without the line-number prefix; it must occur
   EXACTLY ONCE in that file>", "new": "<replacement>", "why": "<one line>"}].  Use JSON escapes (\t, \n).  Tabs stay tabs;
   lines within 79 columns; tag a new comment `/* #NNN: ... */`.  Prefer the file's existing idioms (a decline, a once-per-
   device announce, a clamp) over new machinery.
3. After the block: what the fix deliberately does NOT change, and anything you could not settle from the code shown.

End with one line: `FIXDRAFT_FBSCALEDOWNOOB: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
