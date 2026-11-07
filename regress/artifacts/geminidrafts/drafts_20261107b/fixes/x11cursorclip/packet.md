# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `x11cursorclip` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `x11cursorclip`, state `open`)

**title:** console/x11.c:x11_redraw_cursor + devices/dev_fb.c:dev_fb_setcursor -- the cursor is clamped against VRAM size while the X image has the visible size, and `XSubImage` is not clipped, so a cursor below the visible area makes Xlib read past the image -- HOST-STOP (host heap over-read; X11 build run with -X)

**state_note (head):** QUEUE: external-research batch tail 5 of 6 (regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md D).  Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T13 (class HOST-STOP; reach K*, guest kernel with -X or a similar option; effort: small (~20 lines); report rows: A2-12, A(c)#3).  Source URLs: https://github.com/rpajarola/gxemul/commit/fe69c7bb763d9012ccafbe689cc3617d1684655e.  Our site at de8c7547: src/console/x11.c:247-251; src/devices/dev_fb.c:244-252, :913-914; src/devices/dev_turbochannel.c:250-251.  Portable fix: yes -- port rpajarola fe69c7b; also clamp against the visible size in dev_fb_setcursor.  Filing check (TRIAGE.md): 0 hits for XSubImage / redraw_cursor / setcursor.  Tail position 5 (regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md D).  witness: none -- research finding, not yet reproduced here.

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/console/x11.c` -- AT HEAD, lines 224-310 (`*` marks a line your previous draft changed)

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
  246|* 	XImage *xtmp;
  247|  	CHECK_ALLOCATION(xtmp = XSubImage(fbwin->fb_ximage,
  248|  	    fbwin->cursor_x/fbwin->scaledown,
  249|  	    fbwin->cursor_y/fbwin->scaledown,
  250|* 	    fbwin->cursor_xsize/fbwin->scaledown + 1,
  251|* 	    fbwin->cursor_ysize/fbwin->scaledown + 1));
  252|* 
  253|  	for (int y = 0; y < fbwin->cursor_ysize; y += fbwin->scaledown) {
  254|  		for (int x = 0; x < fbwin->cursor_xsize; x += fbwin->scaledown) {
  255|  			int px = x/fbwin->scaledown;
  256|  			int py = y/fbwin->scaledown;
  257|* 			int p = 0, n = 0, c = 0;
  258|  			unsigned long oldcol;
  259|  
  260|  			for (int suby = 0; suby < fbwin->scaledown; suby++)
  261|  				for (int subx = 0; subx < fbwin->scaledown; subx++) {
  262|  					c = fbwin->cursor_pixels[y+suby][x+subx];
  263|  					if (c >= 0) {
  264|  						p += c;
  265|  						n++;
  266|  					}
  267|  				}
  268|  			if (n > 0)
  269|  				p /= n;
  270|  			else
  271|  				p = c;
  272|  
  273|  			switch (p) {
  274|  			case CURSOR_COLOR_TRANSPARENT:
  275|  				break;
  276|  
  277|  			case CURSOR_COLOR_INVERT:
  278|  				oldcol = XGetPixel(xtmp, px, py);
  279|  				if (oldcol != fbwin->
  280|  				    x11_graycolor[N_GRAYCOLORS-1].pixel)
  281|  					oldcol = fbwin->x11_graycolor[N_GRAYCOLORS-1].pixel;
  282|  				else
  283|  					oldcol = fbwin->x11_graycolor[0].pixel;
  284|  
  285|  				XPutPixel(xtmp, px, py, oldcol);
  286|  				break;
  287|  
  288|  			default:	/*  Normal grayscale:  */
  289|  				XPutPixel(xtmp, px, py, fbwin->x11_graycolor[p].pixel);
  290|  			}
  291|  		}
  292|  	}
  293|  
  294|  	XPutImage(fbwin->x11_display,
  295|  	    fbwin->x11_fb_window,
  296|  	    fbwin->x11_fb_gc,
  297|  	    xtmp, 0, 0,
  298|  	    fbwin->cursor_x/fbwin->scaledown,
  299|  	    fbwin->cursor_y/fbwin->scaledown,
  300|  	    fbwin->cursor_xsize/fbwin->scaledown,
  301|  	    fbwin->cursor_ysize/fbwin->scaledown);
  302|  
  303|  	XDestroyImage(xtmp);
  304|  
  305|  	fbwin->OLD_cursor_on = fbwin->cursor_on;
  306|  	fbwin->OLD_cursor_x = fbwin->cursor_x;
  307|  	fbwin->OLD_cursor_y = fbwin->cursor_y;
  308|  	fbwin->OLD_cursor_xsize = fbwin->cursor_xsize;
  309|  	fbwin->OLD_cursor_ysize = fbwin->cursor_ysize;
  310|  }
```

### `src/devices/dev_fb.c` -- AT HEAD, lines 244-266 (`*` marks a line your previous draft changed)

```c
  244|  {
  245|  	if (cursor_x < 0)
  246|  		cursor_x = 0;
  247|  	if (cursor_y < 0)
  248|  		cursor_y = 0;
  249|* 	if (cursor_x + cursor_xsize >= d->xsize)
  250|* 		cursor_x = d->xsize - cursor_xsize;
  251|* 	if (cursor_y + cursor_ysize >= d->ysize)
  252|* 		cursor_y = d->ysize - cursor_ysize;
  253|* 
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

## The data structures those files define (every field that exists)

### `src/devices/dev_turbochannel.c` -- `struct turbochannel_data {` (HEAD lines 47-61)

```c
   47| struct turbochannel_data {
   48| 	int		slot_nr;
   49| 	uint64_t	baseaddr;
   50| 	uint64_t	endaddr;
   51| 
   52| 	int		rom_skip;
   53| 
   54| 	char		device_name[DEVICE_MAX_NAMELEN];  /*  NUL-terminated  */
   55| 
   56| 	/*  These should be terminated with spaces  */
   57| 	char		card_firmware_version[CARD_NAME_BUFLEN];
   58| 	char		card_vendor_name[CARD_NAME_BUFLEN];
   59| 	char		card_module_name[CARD_NAME_BUFLEN];
   60| 	char		card_firmware_type[CARD_FIRMWARE_BUFLEN];
   61| };
```

### `src/include/devices.h` -- `struct vfb_data` (HEAD lines 201-239)

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


## Your previous draft's edits

```json
[
  {
    "file": "src/console/x11.c",
    "old": "\tXImage *xtmp;\n\tCHECK_ALLOCATION(xtmp = XSubImage(fbwin->fb_ximage,\n\t    fbwin->cursor_x/fbwin->scaledown,\n\t    fbwin->cursor_y/fbwin->scaledown,\n\t    fbwin->cursor_xsize/fbwin->scaledown + 1,\n\t    fbwin->cursor_ysize/fbwin->scaledown + 1));",
    "new": "\tint cxsize = fbwin->cursor_xsize/fbwin->scaledown + 1;\n\tint cysize = fbwin->cursor_ysize/fbwin->scaledown + 1;\n\tif (fbwin->cursor_x/fbwin->scaledown + cxsize > fbwin->fb_ximage->width)\n\t\tcxsize = fbwin->fb_ximage->width - fbwin->cursor_x/fbwin->scaledown;\n\tif (fbwin->cursor_y/fbwin->scaledown + cysize > fbwin->fb_ximage->height)\n\t\tcysize = fbwin->fb_ximage->height - fbwin->cursor_y/fbwin->scaledown;\n\tif (cxsize <= 0 || cysize <= 0)\n\t\treturn;\n\n\tXImage *xtmp;\n\tCHECK_ALLOCATION(xtmp = XSubImage(fbwin->fb_ximage,\n\t    fbwin->cursor_x/fbwin->scaledown,\n\t    fbwin->cursor_y/fbwin->scaledown,\n\t    cxsize, cysize));",
    "why": "Clip XSubImage dimensions to the image bounds to prevent out-of-bounds reads in Xlib (#233)"
  },
  {
    "file": "src/console/x11.c",
    "old": "\t\t\tint px = x/fbwin->scaledown;\n\t\t\tint py = y/fbwin->scaledown;\n\t\t\tint p = 0, n = 0, c = 0;",
    "new": "\t\t\tint px = x/fbwin->scaledown;\n\t\t\tint py = y/fbwin->scaledown;\n\t\t\tif (px >= cxsize || py >= cysize)\n\t\t\t\tcontinue;\n\t\t\tint p = 0, n = 0, c = 0;",
    "why": "Prevent out-of-bounds pixel access in the clipped XSubImage (#233)"
  },
  {
    "file": "src/devices/dev_fb.c",
    "old": "\tif (cursor_x + cursor_xsize >= d->xsize)\n\t\tcursor_x = d->xsize - cursor_xsize;\n\tif (cursor_y + cursor_ysize >= d->ysize)\n\t\tcursor_y = d->ysize - cursor_ysize;",
    "new": "\tif (cursor_x + cursor_xsize >= d->visible_xsize)\n\t\tcursor_x = d->visible_xsize - cursor_xsize;\n\tif (cursor_y + cursor_ysize >= d->visible_ysize)\n\t\tcursor_y = d->visible_ysize - cursor_ysize;",
    "why": "Clamp cursor coordinates against visible size rather than VRAM size to match X11 window dimensions (#233)"
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_X11CURSORCLIP: DEFECT, 3 FINDINGS
1. No, the diff does not remove the defect at every site. It entirely misses `src/devices/dev_fb.c:913-914` and `src/devices/dev_turbochannel.c:250-251` which were named in the issue. Additionally, within the edited `x11_redraw_cursor`, it misses the `XPutImage` call at `src/console/x11.c:310-311` which still uses the unclamped `cursor_xsize` and `cursor_ysize`, meaning Xlib will still read past the end of the `xtmp` image buffer.
2. Yes. The early return `if (cxsize <= 0 || cysize <= 0) return;` at `src/console/x11.c:253` skips the common tail that updates the old cursor state for the next frame. It skips: `fbwin->OLD_cursor_on = fbwin->cursor_on;` (line 315) and the subsequent state assignments.
3. No path returns a different value; both edited functions return `void`.
4. In `dev_fb_setcursor`, the diff introduces a state corruption: if `cursor_xsize` is larger than `d->visible_xsize`, the new clamping logic at `src/devices/dev_fb.c:249-250` sets `cursor_x` to a negative number. Because the lower-bound check (`cursor_x < 0`) happened *before* this clamp (lines 245-246), the negative coordinate is written to the guest-visible window state.
5. No house idiom or style violations found. All lines are within 79 columns and no new diagnostics were added.
src/console/x11.c:310, DEFECT, `cxsize, cysize);`
src/console/x11.c:253, DEFECT, `goto skip_draw;`
src/devices/dev_fb.c:250, DEFECT, `cursor_x = d->visible_xsize > cursor_xsize ? d->visible_xsize - cursor_xsize : 0;`
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

End with two lines: `REVISION_X11CURSORCLIP: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_X11CURSORCLIP: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
