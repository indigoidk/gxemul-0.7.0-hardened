# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `fbscaledownoob` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `fbscaledownoob`, state `open`)

**title:** src/devices/dev_fb.c:634-656 + src/devices/fb_include.c:232-239 -- the tick clamps update_y2 to the last visible row and then rounds it up to a multiple of the scale-down factor, so the redraw loop can reach the row at visible_ysize and the scale-down redraw reads past the end of the framebuffer -- OOB-READ (X11 build, scale-down factor above 1)

**state_note (head):** 

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/devices/dev_fb.c` -- AT HEAD, lines 497-695 (`*` marks a line your previous draft changed)

```c
  497|  DEVICE_TICK(fb)
  498|  {
  499|  	struct vfb_data *d = (struct vfb_data *) extra;
  500|  #ifdef WITH_X11
  501|  	int need_to_flush_x11 = 0;
  502|  	int need_to_redraw_cursor = 0;
  503|  #endif
  504|  
  505|  	if (!cpu->machine->x11_md.in_use)
  506|  		return;
  507|  
  508|  	do {
  509|  		uint64_t high, low = (uint64_t)(int64_t) -1;
  510|  		int x, y;
  511|  
  512|  		memory_device_dyntrans_access(cpu, cpu->mem,
  513|  		    extra, &low, &high);
  514|  		if ((int64_t)low == -1)
  515|  			break;
  516|  
  517|  		/*  printf("low=%016llx high=%016llx\n",
  518|  		    (long long)low, (long long)high);  */
  519|  
  520|  		x = (low % d->bytes_per_line) * 8 / d->bit_depth;
  521|  		y = low / d->bytes_per_line;
  522|  		if (x < d->update_x1 || d->update_x1 == -1)
  523|  			d->update_x1 = x;
  524|  		if (x > d->update_x2 || d->update_x2 == -1)
  525|  			d->update_x2 = x;
  526|  		if (y < d->update_y1 || d->update_y1 == -1)
  527|  			d->update_y1 = y;
  528|  		if (y > d->update_y2 || d->update_y2 == -1)
  529|  			d->update_y2 = y;
  530|  
  531|  		x = ((low+7) % d->bytes_per_line) * 8 / d->bit_depth;
  532|  		y = (low+7) / d->bytes_per_line;
  533|  		if (x < d->update_x1 || d->update_x1 == -1)
  534|  			d->update_x1 = x;
  535|  		if (x > d->update_x2 || d->update_x2 == -1)
  536|  			d->update_x2 = x;
  537|  		if (y < d->update_y1 || d->update_y1 == -1)
  538|  			d->update_y1 = y;
  539|  		if (y > d->update_y2 || d->update_y2 == -1)
  540|  			d->update_y2 = y;
  541|  
  542|  		x = (high % d->bytes_per_line) * 8 / d->bit_depth;
  543|  		y = high / d->bytes_per_line;
  544|  		if (x < d->update_x1 || d->update_x1 == -1)
  545|  			d->update_x1 = x;
  546|  		if (x > d->update_x2 || d->update_x2 == -1)
  547|  			d->update_x2 = x;
  548|  		if (y < d->update_y1 || d->update_y1 == -1)
  549|  			d->update_y1 = y;
  550|  		if (y > d->update_y2 || d->update_y2 == -1)
  551|  			d->update_y2 = y;
  552|  
  553|  		x = ((high+7) % d->bytes_per_line) * 8 / d->bit_depth;
  554|  		y = (high+7) / d->bytes_per_line;
  555|  		if (x < d->update_x1 || d->update_x1 == -1)
  556|  			d->update_x1 = x;
  557|  		if (x > d->update_x2 || d->update_x2 == -1)
  558|  			d->update_x2 = x;
  559|  		if (y < d->update_y1 || d->update_y1 == -1)
  560|  			d->update_y1 = y;
  561|  		if (y > d->update_y2 || d->update_y2 == -1)
  562|  			d->update_y2 = y;
  563|  
  564|  		/*
  565|  		 *  An update covering more than one line will automatically
  566|  		 *  force an update of all the affected lines:
  567|  		 */
  568|  		if (d->update_y1 != d->update_y2) {
  569|  			d->update_x1 = 0;
  570|  			d->update_x2 = d->xsize-1;
  571|  		}
  572|  	} while (0);
  573|  
  574|  #ifdef WITH_X11
  575|  	/*  Do we need to redraw the cursor?  */
  576|  	if (d->fb_window->cursor_on != d->fb_window->OLD_cursor_on ||
  577|  	    d->fb_window->cursor_x != d->fb_window->OLD_cursor_x ||
  578|  	    d->fb_window->cursor_y != d->fb_window->OLD_cursor_y ||
  579|  	    d->fb_window->cursor_xsize != d->fb_window->OLD_cursor_xsize ||
  580|  	    d->fb_window->cursor_ysize != d->fb_window->OLD_cursor_ysize)
  581|  		need_to_redraw_cursor = 1;
  582|  
  583|  	if (d->update_x2 != -1) {
  584|  		if (((d->update_x1 >= d->fb_window->OLD_cursor_x &&
  585|  		      d->update_x1 < (d->fb_window->OLD_cursor_x +
  586|  		      d->fb_window->OLD_cursor_xsize)) ||
  587|  		     (d->update_x2 >= d->fb_window->OLD_cursor_x &&
  588|  		      d->update_x2 < (d->fb_window->OLD_cursor_x +
  589|  		      d->fb_window->OLD_cursor_xsize)) ||
  590|  		     (d->update_x1 <  d->fb_window->OLD_cursor_x &&
  591|  		      d->update_x2 >= (d->fb_window->OLD_cursor_x +
  592|  		      d->fb_window->OLD_cursor_xsize)) ) &&
  593|  		   ( (d->update_y1 >= d->fb_window->OLD_cursor_y &&
  594|  		      d->update_y1 < (d->fb_window->OLD_cursor_y +
  595|  		      d->fb_window->OLD_cursor_ysize)) ||
  596|  		     (d->update_y2 >= d->fb_window->OLD_cursor_y &&
  597|  		      d->update_y2 < (d->fb_window->OLD_cursor_y +
  598|  		      d->fb_window->OLD_cursor_ysize)) ||
  599|  		     (d->update_y1 <  d->fb_window->OLD_cursor_y &&
  600|  		      d->update_y2 >= (d->fb_window->OLD_cursor_y +
  601|  		     d->fb_window->OLD_cursor_ysize)) ) )
  602|  			need_to_redraw_cursor = 1;
  603|  	}
  604|  
  605|  	if (need_to_redraw_cursor) {
  606|  		/*  Remove old cursor, if any:  */
  607|  		if (d->fb_window->OLD_cursor_on) {
  608|  			XPutImage(d->fb_window->x11_display,
  609|  			    d->fb_window->x11_fb_window,
  610|  			    d->fb_window->x11_fb_gc, d->fb_window->fb_ximage,
  611|  			    d->fb_window->OLD_cursor_x/d->vfb_scaledown,
  612|  			    d->fb_window->OLD_cursor_y/d->vfb_scaledown,
  613|  			    d->fb_window->OLD_cursor_x/d->vfb_scaledown,
  614|  			    d->fb_window->OLD_cursor_y/d->vfb_scaledown,
  615|  			    d->fb_window->OLD_cursor_xsize/d->vfb_scaledown + 1,
  616|  			    d->fb_window->OLD_cursor_ysize/d->vfb_scaledown +1);
  617|  		}
  618|  	}
  619|  #endif
  620|  
  621|  	if (d->update_x2 != -1) {
  622|  #ifdef WITH_X11
  623|  		int y;
  624|  		int addr, addr2;
  625|  #endif
  626|  		int q = d->vfb_scaledown;
  627|  
  628|  		if (d->update_x1 >= d->visible_xsize)
  629|  			d->update_x1 = d->visible_xsize - 1;
  630|  		if (d->update_x2 >= d->visible_xsize)
  631|  			d->update_x2 = d->visible_xsize - 1;
  632|  		if (d->update_y1 >= d->visible_ysize)
  633|  			d->update_y1 = d->visible_ysize - 1;
  634|  		if (d->update_y2 >= d->visible_ysize)
  635|  			d->update_y2 = d->visible_ysize - 1;
  636|  
  637|  		/*  Without these, we might miss the rightmost/bottom pixel:  */
  638|  		d->update_x2 += (q - 1);
  639|  		d->update_y2 += (q - 1);
  640|  
  641|  		d->update_x1 = d->update_x1 / q * q;
  642|  		d->update_x2 = d->update_x2 / q * q;
  643|  		d->update_y1 = d->update_y1 / q * q;
  644|  		d->update_y2 = d->update_y2 / q * q;
  645|  
  646|* #ifdef WITH_X11
  647|  		addr  = d->update_y1 * d->bytes_per_line +
  648|  		    d->update_x1 * d->bit_depth / 8;
  649|  		addr2 = d->update_y1 * d->bytes_per_line +
  650|  		    d->update_x2 * d->bit_depth / 8;
  651|  
  652|  		for (y=d->update_y1; y<=d->update_y2; y+=q) {
  653|  			d->redraw_func(d, addr, addr2 - addr);
  654|  			addr  += d->bytes_per_line * q;
  655|  			addr2 += d->bytes_per_line * q;
  656|  		}
  657|  
  658|  		XPutImage(d->fb_window->x11_display, d->fb_window->
  659|  		    x11_fb_window, d->fb_window->x11_fb_gc, d->fb_window->
  660|  		    fb_ximage, d->update_x1/d->vfb_scaledown, d->update_y1/
  661|  		    d->vfb_scaledown, d->update_x1/d->vfb_scaledown,
  662|  		    d->update_y1/d->vfb_scaledown,
  663|  		    (d->update_x2 - d->update_x1)/d->vfb_scaledown + 1,
  664|  		    (d->update_y2 - d->update_y1)/d->vfb_scaledown + 1);
  665|  
  666|  		need_to_flush_x11 = 1;
  667|  #endif
  668|  
  669|  		d->update_x1 = d->update_y1 = 99999;
  670|  		d->update_x2 = d->update_y2 = -1;
  671|  	}
  672|  
  673|  #ifdef WITH_X11
  674|  	if (need_to_redraw_cursor) {
  675|  		/*  Paint new cursor:  */
  676|  		if (d->fb_window->cursor_on) {
  677|  			x11_redraw_cursor(cpu->machine,
  678|  			    d->fb_window->fb_number);
  679|  			d->fb_window->OLD_cursor_on = d->fb_window->cursor_on;
  680|  			d->fb_window->OLD_cursor_x = d->fb_window->cursor_x;
  681|  			d->fb_window->OLD_cursor_y = d->fb_window->cursor_y;
  682|  			d->fb_window->OLD_cursor_xsize = d->fb_window->
  683|  			    cursor_xsize;
  684|  			d->fb_window->OLD_cursor_ysize = d->fb_window->
  685|  			    cursor_ysize;
  686|  			need_to_flush_x11 = 1;
  687|  		}
  688|  	}
  689|  #endif
  690|  
  691|  #ifdef WITH_X11
  692|  	if (need_to_flush_x11)
  693|  		XFlush(d->fb_window->x11_display);
  694|  #endif
  695|  }
```



## Your previous draft's edits

```json
[
  {
    "file": "src/devices/dev_fb.c",
    "old": "\t\td->update_x1 = d->update_x1 / q * q;\n\t\td->update_x2 = d->update_x2 / q * q;\n\t\td->update_y1 = d->update_y1 / q * q;\n\t\td->update_y2 = d->update_y2 / q * q;",
    "new": "\t\td->update_x1 = d->update_x1 / q * q;\n\t\td->update_x2 = d->update_x2 / q * q;\n\t\td->update_y1 = d->update_y1 / q * q;\n\t\td->update_y2 = d->update_y2 / q * q;\n\n\t\tif (d->update_x2 >= d->visible_xsize)\n\t\t\td->update_x2 = d->visible_xsize - 1;\n\t\tif (d->update_y2 >= d->visible_ysize)\n\t\t\td->update_y2 = d->visible_ysize - 1;",
    "why": "Clamp the update region's upper bounds after rounding up to scaledown multiples to prevent the redraw loop from reading past the end of the framebuffer."
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_FBSCALEDOWNOOB: DEFECT, 1 FINDINGS
1. **Does the diff remove the defect the issue describes, at every site the issue names?** No. The issue ledger explicitly names two locations: `src/devices/dev_fb.c:634-656` and `src/devices/fb_include.c:232-239`. The proposed fix entirely ignores `src/devices/fb_include.c`, leaving the out-of-bounds read defect present there.
2. **CONTROL FLOW:** No. The diff only introduces simple conditional value clamps (variable assignments). No `return`, `goto`, `break`, or early exits are added, so it does not skip any tail code.
3. **RETURN VALUE:** No. The function has a `void` or implicit void return (exiting only via `return;` or reaching the end of the block), and the patch does not add or alter any return statements.
4. **What ELSE does the diff change?** Nothing. It strictly recalculates bounds on `d->update_x2` and `d->update_y2` to prevent the variables from exceeding `d->visible_xsize` and `d->visible_ysize` after rounding up to the scale-down factor.
5. **House idioms:** No new comments or diagnostics were introduced by the diff, so there are no style idiom violations.
**Findings:**
`src/devices/fb_include.c:232` (approximate, missing from diff), DEFECT, apply the identical bounds-clamping fix to the `fb_include.c` file as requested by the issue ticket.
FIXREVIEW_FBSCALEDOWNOOB: DEFECT, 1 FINDINGS
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

End with two lines: `REVISION_FBSCALEDOWNOOB: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_FBSCALEDOWNOOB: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
