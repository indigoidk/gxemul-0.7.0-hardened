# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `x11cursorclip` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `x11cursorclip`, state `open`)

**title:** console/x11.c:x11_redraw_cursor + devices/dev_fb.c:dev_fb_setcursor -- the cursor is clamped against VRAM size while the X image has the visible size, and `XSubImage` is not clipped, so a cursor below the visible area makes Xlib read past the image -- HOST-STOP (host heap over-read; X11 build run with -X)

**state_note (head):** QUEUE: external-research batch tail 5 of 6 (regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md D).  Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T13 (class HOST-STOP; reach K*, guest kernel with -X or a similar option; effort: small (~20 lines); report rows: A2-12, A(c)#3).  Source URLs: https://github.com/rpajarola/gxemul/commit/fe69c7bb763d9012ccafbe689cc3617d1684655e.  Our site at de8c7547: src/console/x11.c:247-251; src/devices/dev_fb.c:244-252, :913-914; src/devices/dev_turbochannel.c:250-251.  Portable fix: yes -- port rpajarola fe69c7b; also clamp against the visible size in dev_fb_setcursor.  Filing check (TRIAGE.md): 0 hits for XSubImage / redraw_cursor / setcursor.  Tail position 5 (regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md D).  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- `src/console/x11.c:300`

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/console/x11.c b/src/console/x11.c
index 698173c7..7d0d61f2 100644
--- a/src/console/x11.c
+++ b/src/console/x11.c
@@ -243,17 +243,28 @@ void x11_redraw_cursor(struct machine *m, int i)
 	if (!fbwin->cursor_on)
 		return;
 
-	XImage *xtmp;
-	CHECK_ALLOCATION(xtmp = XSubImage(fbwin->fb_ximage,
-	    fbwin->cursor_x/fbwin->scaledown,
-	    fbwin->cursor_y/fbwin->scaledown,
-	    fbwin->cursor_xsize/fbwin->scaledown + 1,
-	    fbwin->cursor_ysize/fbwin->scaledown + 1));
+	int cxsize = fbwin->cursor_xsize/fbwin->scaledown + 1;
+	int cysize = fbwin->cursor_ysize/fbwin->scaledown + 1;
+	if (fbwin->cursor_x/fbwin->scaledown + cxsize > fbwin->fb_ximage->width)
+		cxsize = fbwin->fb_ximage->width - fbwin->cursor_x/fbwin->scaledown;
+	if (fbwin->cursor_y/fbwin->scaledown + cysize > fbwin->fb_ximage->height)
+		cysize = fbwin->fb_ximage->height - fbwin->cursor_y/fbwin->scaledown;
+
+	XImage *xtmp = NULL;
+	if (cxsize > 0 && cysize > 0) {
+		CHECK_ALLOCATION(xtmp = XSubImage(fbwin->fb_ximage,
+		    fbwin->cursor_x/fbwin->scaledown,
+		    fbwin->cursor_y/fbwin->scaledown,
+		    cxsize, cysize));
+	}
 
+	if (xtmp != NULL) {
 	for (int y = 0; y < fbwin->cursor_ysize; y += fbwin->scaledown) {
 		for (int x = 0; x < fbwin->cursor_xsize; x += fbwin->scaledown) {
 			int px = x/fbwin->scaledown;
 			int py = y/fbwin->scaledown;
+			if (px >= cxsize || py >= cysize)
+				continue;
 			int p = 0, n = 0, c = 0;
 			unsigned long oldcol;
 
@@ -291,16 +302,17 @@ void x11_redraw_cursor(struct machine *m, int i)
 		}
 	}
 
-	XPutImage(fbwin->x11_display,
-	    fbwin->x11_fb_window,
-	    fbwin->x11_fb_gc,
-	    xtmp, 0, 0,
-	    fbwin->cursor_x/fbwin->scaledown,
-	    fbwin->cursor_y/fbwin->scaledown,
-	    fbwin->cursor_xsize/fbwin->scaledown,
-	    fbwin->cursor_ysize/fbwin->scaledown);
-
-	XDestroyImage(xtmp);
+		XPutImage(fbwin->x11_display,
+		    fbwin->x11_fb_window,
+		    fbwin->x11_fb_gc,
+		    xtmp, 0, 0,
+		    fbwin->cursor_x/fbwin->scaledown,
+		    fbwin->cursor_y/fbwin->scaledown,
+		    cxsize,
+		    cysize);
+
+		XDestroyImage(xtmp);
+	}
 
 	fbwin->OLD_cursor_on = fbwin->cursor_on;
 	fbwin->OLD_cursor_x = fbwin->cursor_x;
diff --git a/src/devices/dev_fb.c b/src/devices/dev_fb.c
index 75bb8d81..8c8871ba 100644
--- a/src/devices/dev_fb.c
+++ b/src/devices/dev_fb.c
@@ -246,10 +246,10 @@ void dev_fb_setcursor(struct vfb_data *d, int cursor_x, int cursor_y, int on,
 		cursor_x = 0;
 	if (cursor_y < 0)
 		cursor_y = 0;
-	if (cursor_x + cursor_xsize >= d->xsize)
-		cursor_x = d->xsize - cursor_xsize;
-	if (cursor_y + cursor_ysize >= d->ysize)
-		cursor_y = d->ysize - cursor_ysize;
+	if (cursor_x + cursor_xsize >= d->visible_xsize)
+		cursor_x = d->visible_xsize > cursor_xsize ? d->visible_xsize - cursor_xsize : 0;
+	if (cursor_y + cursor_ysize >= d->visible_ysize)
+		cursor_y = d->visible_ysize > cursor_ysize ? d->visible_ysize - cursor_ysize : 0;
 
 #ifdef WITH_X11
 	if (d->fb_window != NULL) {
```

## Every edited function, after the fix

### `src/console/x11.c` -- post-edit lines 224-322 (`+` marks a line the diff added or the point of a deletion)

```c
  224|  void x11_redraw_cursor(struct machine *m, int i)
  225|  {
  226|  	struct fb_window *fbwin = m->x11_md.fb_windows[i];
  227|  
  228|  	if (fbwin->x11_display == NULL)
  229|  		return;
  230|  
  231|  	/*  Remove old cursor, if any:  */
  232|  	if (fbwin->OLD_cursor_on) {
  233|  		XPutImage(fbwin->x11_display, fbwin->x11_fb_window,
  234|  		    fbwin->x11_fb_gc, fbwin->fb_ximage,
  235|  		    fbwin->OLD_cursor_x/fbwin->scaledown,
  236|  		    fbwin->OLD_cursor_y/fbwin->scaledown,
  237|  		    fbwin->OLD_cursor_x/fbwin->scaledown,
  238|  		    fbwin->OLD_cursor_y/fbwin->scaledown,
  239|  		    fbwin->OLD_cursor_xsize/fbwin->scaledown + 1,
  240|  		    fbwin->OLD_cursor_ysize/fbwin->scaledown + 1);
  241|  	}
  242|  
  243|  	if (!fbwin->cursor_on)
  244|  		return;
  245|  
  246|+ 	int cxsize = fbwin->cursor_xsize/fbwin->scaledown + 1;
  247|+ 	int cysize = fbwin->cursor_ysize/fbwin->scaledown + 1;
  248|+ 	if (fbwin->cursor_x/fbwin->scaledown + cxsize > fbwin->fb_ximage->width)
  249|+ 		cxsize = fbwin->fb_ximage->width - fbwin->cursor_x/fbwin->scaledown;
  250|+ 	if (fbwin->cursor_y/fbwin->scaledown + cysize > fbwin->fb_ximage->height)
  251|+ 		cysize = fbwin->fb_ximage->height - fbwin->cursor_y/fbwin->scaledown;
  252|+ 
  253|+ 	XImage *xtmp = NULL;
  254|+ 	if (cxsize > 0 && cysize > 0) {
  255|+ 		CHECK_ALLOCATION(xtmp = XSubImage(fbwin->fb_ximage,
  256|+ 		    fbwin->cursor_x/fbwin->scaledown,
  257|+ 		    fbwin->cursor_y/fbwin->scaledown,
  258|+ 		    cxsize, cysize));
  259|+ 	}
  260|  
  261|+ 	if (xtmp != NULL) {
  262|  	for (int y = 0; y < fbwin->cursor_ysize; y += fbwin->scaledown) {
  263|  		for (int x = 0; x < fbwin->cursor_xsize; x += fbwin->scaledown) {
  264|  			int px = x/fbwin->scaledown;
  265|  			int py = y/fbwin->scaledown;
  266|+ 			if (px >= cxsize || py >= cysize)
  267|+ 				continue;
  268|  			int p = 0, n = 0, c = 0;
  269|  			unsigned long oldcol;
  270|  
  271|  			for (int suby = 0; suby < fbwin->scaledown; suby++)
  272|  				for (int subx = 0; subx < fbwin->scaledown; subx++) {
  273|  					c = fbwin->cursor_pixels[y+suby][x+subx];
  274|  					if (c >= 0) {
  275|  						p += c;
  276|  						n++;
  277|  					}
  278|  				}
  279|  			if (n > 0)
  280|  				p /= n;
  281|  			else
  282|  				p = c;
  283|  
  284|  			switch (p) {
  285|  			case CURSOR_COLOR_TRANSPARENT:
  286|  				break;
  287|  
  288|  			case CURSOR_COLOR_INVERT:
  289|  				oldcol = XGetPixel(xtmp, px, py);
  290|  				if (oldcol != fbwin->
  291|  				    x11_graycolor[N_GRAYCOLORS-1].pixel)
  292|  					oldcol = fbwin->x11_graycolor[N_GRAYCOLORS-1].pixel;
  293|  				else
  294|  					oldcol = fbwin->x11_graycolor[0].pixel;
  295|  
  296|  				XPutPixel(xtmp, px, py, oldcol);
  297|  				break;
  298|  
  299|  			default:	/*  Normal grayscale:  */
  300|  				XPutPixel(xtmp, px, py, fbwin->x11_graycolor[p].pixel);
  301|  			}
  302|  		}
  303|  	}
  304|  
  305|+ 		XPutImage(fbwin->x11_display,
  306|+ 		    fbwin->x11_fb_window,
  307|+ 		    fbwin->x11_fb_gc,
  308|+ 		    xtmp, 0, 0,
  309|+ 		    fbwin->cursor_x/fbwin->scaledown,
  310|+ 		    fbwin->cursor_y/fbwin->scaledown,
  311|+ 		    cxsize,
  312|+ 		    cysize);
  313|+ 
  314|+ 		XDestroyImage(xtmp);
  315|+ 	}
  316|  
  317|  	fbwin->OLD_cursor_on = fbwin->cursor_on;
  318|  	fbwin->OLD_cursor_x = fbwin->cursor_x;
  319|  	fbwin->OLD_cursor_y = fbwin->cursor_y;
  320|  	fbwin->OLD_cursor_xsize = fbwin->cursor_xsize;
  321|  	fbwin->OLD_cursor_ysize = fbwin->cursor_ysize;
  322|  }
```

### `src/devices/dev_fb.c` -- post-edit lines 244-266 (`+` marks a line the diff added or the point of a deletion)

```c
  244|  {
  245|  	if (cursor_x < 0)
  246|  		cursor_x = 0;
  247|  	if (cursor_y < 0)
  248|  		cursor_y = 0;
  249|+ 	if (cursor_x + cursor_xsize >= d->visible_xsize)
  250|+ 		cursor_x = d->visible_xsize > cursor_xsize ? d->visible_xsize - cursor_xsize : 0;
  251|+ 	if (cursor_y + cursor_ysize >= d->visible_ysize)
  252|+ 		cursor_y = d->visible_ysize > cursor_ysize ? d->visible_ysize - cursor_ysize : 0;
  253|  
  254|  #ifdef WITH_X11
  255|  	if (d->fb_window != NULL) {
  256|  		d->fb_window->cursor_x      = cursor_x;
  257|  		d->fb_window->cursor_y      = cursor_y;
  258|  		d->fb_window->cursor_on     = on;
  259|  		d->fb_window->cursor_xsize  = cursor_xsize;
  260|  		d->fb_window->cursor_ysize  = cursor_ysize;
  261|  	}
  262|  #endif
  263|  
  264|  	/*  debug("dev_fb_setcursor(%i,%i, size %i,%i, on=%i)\n",
  265|  	    cursor_x, cursor_y, cursor_xsize, cursor_ysize, on);  */
  266|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_X11CURSORCLIP: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_X11CURSORCLIP: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
