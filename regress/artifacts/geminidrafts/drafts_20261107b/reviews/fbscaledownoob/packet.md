# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `fbscaledownoob` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `fbscaledownoob`, state `open`)

**title:** src/devices/dev_fb.c:634-656 + src/devices/fb_include.c:232-239 -- the tick clamps update_y2 to the last visible row and then rounds it up to a multiple of the scale-down factor, so the redraw loop can reach the row at visible_ysize and the scale-down redraw reads past the end of the framebuffer -- OOB-READ (X11 build, scale-down factor above 1)

**state_note (head):** 

**The drafter's own reading:** STILL PRESENT: YES -- src/devices/dev_fb.c:641-644

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_fb.c b/src/devices/dev_fb.c
index 75bb8d81..da8489b4 100644
--- a/src/devices/dev_fb.c
+++ b/src/devices/dev_fb.c
@@ -643,6 +643,11 @@ DEVICE_TICK(fb)
 		d->update_y1 = d->update_y1 / q * q;
 		d->update_y2 = d->update_y2 / q * q;
 
+		if (d->update_x2 >= d->visible_xsize)
+			d->update_x2 = d->visible_xsize - 1;
+		if (d->update_y2 >= d->visible_ysize)
+			d->update_y2 = d->visible_ysize - 1;
+
 #ifdef WITH_X11
 		addr  = d->update_y1 * d->bytes_per_line +
 		    d->update_x1 * d->bit_depth / 8;
```

## Every edited function, after the fix

### `src/devices/dev_fb.c` -- post-edit lines 497-700 (`+` marks a line the diff added or the point of a deletion)

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
  646|+ 		if (d->update_x2 >= d->visible_xsize)
  647|+ 			d->update_x2 = d->visible_xsize - 1;
  648|+ 		if (d->update_y2 >= d->visible_ysize)
  649|+ 			d->update_y2 = d->visible_ysize - 1;
  650|+ 
  651|  #ifdef WITH_X11
  652|  		addr  = d->update_y1 * d->bytes_per_line +
  653|  		    d->update_x1 * d->bit_depth / 8;
  654|  		addr2 = d->update_y1 * d->bytes_per_line +
  655|  		    d->update_x2 * d->bit_depth / 8;
  656|  
  657|  		for (y=d->update_y1; y<=d->update_y2; y+=q) {
  658|  			d->redraw_func(d, addr, addr2 - addr);
  659|  			addr  += d->bytes_per_line * q;
  660|  			addr2 += d->bytes_per_line * q;
  661|  		}
  662|  
  663|  		XPutImage(d->fb_window->x11_display, d->fb_window->
  664|  		    x11_fb_window, d->fb_window->x11_fb_gc, d->fb_window->
  665|  		    fb_ximage, d->update_x1/d->vfb_scaledown, d->update_y1/
  666|  		    d->vfb_scaledown, d->update_x1/d->vfb_scaledown,
  667|  		    d->update_y1/d->vfb_scaledown,
  668|  		    (d->update_x2 - d->update_x1)/d->vfb_scaledown + 1,
  669|  		    (d->update_y2 - d->update_y1)/d->vfb_scaledown + 1);
  670|  
  671|  		need_to_flush_x11 = 1;
  672|  #endif
  673|  
  674|  		d->update_x1 = d->update_y1 = 99999;
  675|  		d->update_x2 = d->update_y2 = -1;
  676|  	}
  677|  
  678|  #ifdef WITH_X11
  679|  	if (need_to_redraw_cursor) {
  680|  		/*  Paint new cursor:  */
  681|  		if (d->fb_window->cursor_on) {
  682|  			x11_redraw_cursor(cpu->machine,
  683|  			    d->fb_window->fb_number);
  684|  			d->fb_window->OLD_cursor_on = d->fb_window->cursor_on;
  685|  			d->fb_window->OLD_cursor_x = d->fb_window->cursor_x;
  686|  			d->fb_window->OLD_cursor_y = d->fb_window->cursor_y;
  687|  			d->fb_window->OLD_cursor_xsize = d->fb_window->
  688|  			    cursor_xsize;
  689|  			d->fb_window->OLD_cursor_ysize = d->fb_window->
  690|  			    cursor_ysize;
  691|  			need_to_flush_x11 = 1;
  692|  		}
  693|  	}
  694|  #endif
  695|  
  696|  #ifdef WITH_X11
  697|  	if (need_to_flush_x11)
  698|  		XFlush(d->fb_window->x11_display);
  699|  #endif
  700|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_FBSCALEDOWNOOB: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_FBSCALEDOWNOOB: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
