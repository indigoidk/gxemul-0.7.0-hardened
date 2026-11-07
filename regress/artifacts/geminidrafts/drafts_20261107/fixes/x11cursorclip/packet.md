# GXemul hardened fork -- DRAFT A FIX for one filed issue, `x11cursorclip` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `x11cursorclip`, state `open`, severity `HIGH`)

**title:** console/x11.c:x11_redraw_cursor + devices/dev_fb.c:dev_fb_setcursor -- the cursor is clamped against VRAM size while the X image has the visible size, and `XSubImage` is not clipped, so a cursor below the visible area makes Xlib read past the image -- HOST-STOP (host heap over-read; X11 build run with -X)

**state_note (head):**

QUEUE: external-research batch tail 5 of 6 (regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md D).  Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T13 (class HOST-STOP; reach K*, guest kernel with -X or a similar option; effort: small (~20 lines); report rows: A2-12, A(c)#3).  Source URLs: https://github.com/rpajarola/gxemul/commit/fe69c7bb763d9012ccafbe689cc3617d1684655e.  Our site at de8c7547: src/console/x11.c:247-251; src/devices/dev_fb.c:244-252, :913-914; src/devices/dev_turbochannel.c:250-251.  Portable fix: yes -- port rpajarola fe69c7b; also clamp against the visible size in dev_fb_setcursor.  Filing check (TRIAGE.md): 0 hits for XSubImage / redraw_cursor / setcursor.  Tail position 5 (regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md D).  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port rpajarola fe69c7b and clamp against visible size in dev_fb_setcursor

## The code at the cited lines

### `src/console/x11.c` around the row's cited line 247 (HEAD 2d25df65, lines 202-292)

```c
  202| 
  203| 	x11_unhide_cursor();
  204| 
  205| 	grabbed = NULL;
  206| 
  207| 	x11_set_standard_properties(fbwin);
  208| 
  209| 	debugmsg(SUBSYS_X11, "grab", VERBOSITY_DEBUG, "Releasing grab.");
  210| 
  211| 	XUngrabPointer(fbwin->x11_display, CurrentTime);
  212| 
  213| 	setMousePointerCoordinates(fbwin, mouseXbeforeGrab, mouseYbeforeGrab);
  214| }
  215| 
  216| 
  217| /*
  218|  *  x11_redraw_cursor():
  219|  *
  220|  *  Redraw a framebuffer's X11 cursor.
  221|  *
  222|  *  NOTE: It is up to the caller to call XFlush.
  223|  */
  224| void x11_redraw_cursor(struct machine *m, int i)
  225| {
  226| 	struct fb_window *fbwin = m->x11_md.fb_windows[i];
  227| 
  228| 	if (fbwin->x11_display == NULL)
  229| 		return;
  230| 
  231| 	/*  Remove old cursor, if any:  */
  232| 	if (fbwin->OLD_cursor_on) {
  233| 		XPutImage(fbwin->x11_display, fbwin->x11_fb_window,
  234| 		    fbwin->x11_fb_gc, fbwin->fb_ximage,
  235| 		    fbwin->OLD_cursor_x/fbwin->scaledown,
  236| 		    fbwin->OLD_cursor_y/fbwin->scaledown,
  237| 		    fbwin->OLD_cursor_x/fbwin->scaledown,
  238| 		    fbwin->OLD_cursor_y/fbwin->scaledown,
  239| 		    fbwin->OLD_cursor_xsize/fbwin->scaledown + 1,
  240| 		    fbwin->OLD_cursor_ysize/fbwin->scaledown + 1);
  241| 	}
  242| 
  243| 	if (!fbwin->cursor_on)
  244| 		return;
  245| 
  246| 	XImage *xtmp;
  247| 	CHECK_ALLOCATION(xtmp = XSubImage(fbwin->fb_ximage,
  248| 	    fbwin->cursor_x/fbwin->scaledown,
  249| 	    fbwin->cursor_y/fbwin->scaledown,
  250| 	    fbwin->cursor_xsize/fbwin->scaledown + 1,
  251| 	    fbwin->cursor_ysize/fbwin->scaledown + 1));
  252| 
  253| 	for (int y = 0; y < fbwin->cursor_ysize; y += fbwin->scaledown) {
  254| 		for (int x = 0; x < fbwin->cursor_xsize; x += fbwin->scaledown) {
  255| 			int px = x/fbwin->scaledown;
  256| 			int py = y/fbwin->scaledown;
  257| 			int p = 0, n = 0, c = 0;
  258| 			unsigned long oldcol;
  259| 
  260| 			for (int suby = 0; suby < fbwin->scaledown; suby++)
  261| 				for (int subx = 0; subx < fbwin->scaledown; subx++) {
  262| 					c = fbwin->cursor_pixels[y+suby][x+subx];
  263| 					if (c >= 0) {
  264| 						p += c;
  265| 						n++;
  266| 					}
  267| 				}
  268| 			if (n > 0)
  269| 				p /= n;
  270| 			else
  271| 				p = c;
  272| 
  273| 			switch (p) {
  274| 			case CURSOR_COLOR_TRANSPARENT:
  275| 				break;
  276| 
  277| 			case CURSOR_COLOR_INVERT:
  278| 				oldcol = XGetPixel(xtmp, px, py);
  279| 				if (oldcol != fbwin->
  280| 				    x11_graycolor[N_GRAYCOLORS-1].pixel)
  281| 					oldcol = fbwin->x11_graycolor[N_GRAYCOLORS-1].pixel;
  282| 				else
  283| 					oldcol = fbwin->x11_graycolor[0].pixel;
  284| 
  285| 				XPutPixel(xtmp, px, py, oldcol);
  286| 				break;
  287| 
  288| 			default:	/*  Normal grayscale:  */
  289| 				XPutPixel(xtmp, px, py, fbwin->x11_graycolor[p].pixel);
  290| 			}
  291| 		}
  292| 	}
```

### `src/devices/dev_fb.c` around the row's cited line 244 (HEAD 2d25df65, lines 199-289)

```c
  199| 	d->xsize = d->visible_xsize = new_xsize;
  200| 	d->ysize = d->visible_ysize = new_ysize;
  201| 
  202| 	d->x11_xsize = d->xsize / d->vfb_scaledown;
  203| 	d->x11_ysize = d->ysize / d->vfb_scaledown;
  204| 
  205| 	memory_device_update_data(d->memory, d, d->framebuffer);
  206| 
  207| 	/*  #182: (Codex/Fable) also resize the device's mapped length so the
  208| 	    dyntrans fast-map gate cannot install a host mapping past the new
  209| 	    (possibly smaller) framebuffer allocation on a guest-driven shrink.
  210| 	    The #157 invalidation below then drops any stale fast-path pointers
  211| 	    so the next access re-derives against the new length.  */
  212| 	memory_device_update_length(d->memory, d, size);
  213| 
  214| 	/*  #157: (Codex/Fable) the framebuffer memory was just freed and
  215| 	    reallocated, so invalidate all CPUs' translation caches (same
  216| 	    idiom as dev_fbctrl), otherwise dyntrans fast-path host pointers
  217| 	    would still point into the freed old framebuffer.  */
  218| 	if (d->machine != NULL) {
  219| 		int i;
  220| 		for (i = 0; i < d->machine->ncpus; i++)
  221| 			d->machine->cpus[i]->invalidate_translation_caches(
  222| 			    d->machine->cpus[i], 0, INVALIDATE_ALL);
  223| 	}
  224| 
  225| 	set_title(d);
  226| 
  227| #ifdef WITH_X11
  228| 	if (d->fb_window != NULL) {
  229| 		x11_fb_resize(d->fb_window, d->x11_xsize, d->x11_ysize);
  230| 		if (d->fb_window->name != NULL)
  231| 			free(d->fb_window->name);
  232| 		d->fb_window->name = strdup(d->title);
  233| 		x11_set_standard_properties(d->fb_window);
  234| 	}
  235| #endif
  236| }
  237| 
  238| 
  239| /*
  240|  *  dev_fb_setcursor():
  241|  */
  242| void dev_fb_setcursor(struct vfb_data *d, int cursor_x, int cursor_y, int on,
  243| 	int cursor_xsize, int cursor_ysize)
  244| {
  245| 	if (cursor_x < 0)
  246| 		cursor_x = 0;
  247| 	if (cursor_y < 0)
  248| 		cursor_y = 0;
  249| 	if (cursor_x + cursor_xsize >= d->xsize)
  250| 		cursor_x = d->xsize - cursor_xsize;
  251| 	if (cursor_y + cursor_ysize >= d->ysize)
  252| 		cursor_y = d->ysize - cursor_ysize;
  253| 
  254| #ifdef WITH_X11
  255| 	if (d->fb_window != NULL) {
  256| 		d->fb_window->cursor_x      = cursor_x;
  257| 		d->fb_window->cursor_y      = cursor_y;
  258| 		d->fb_window->cursor_on     = on;
  259| 		d->fb_window->cursor_xsize  = cursor_xsize;
  260| 		d->fb_window->cursor_ysize  = cursor_ysize;
  261| 	}
  262| #endif
  263| 
  264| 	/*  debug("dev_fb_setcursor(%i,%i, size %i,%i, on=%i)\n",
  265| 	    cursor_x, cursor_y, cursor_xsize, cursor_ysize, on);  */
  266| }
  267| 
  268| 
  269| /*
  270|  *  framebuffer_blockcopyfill():
  271|  *
  272|  *  This function should be used by devices that are capable of doing
  273|  *  block copy/fill.
  274|  *
  275|  *  If fillflag is non-zero, then fill_[rgb] should contain the color
  276|  *  with which to fill. (In 8-bit mode, only fill_r is used.)
  277|  *
  278|  *  If fillflag is zero, copy mode is used, and from_[xy] should contain
  279|  *  the offset on the framebuffer where we should copy from.
  280|  *
  281|  *  NOTE:  Overlapping copies are undefined!
  282|  */
  283| void framebuffer_blockcopyfill(struct vfb_data *d, int fillflag, int fill_r,
  284| 	int fill_g, int fill_b, int x1, int y1, int x2, int y2,
  285| 	int from_x, int from_y)
  286| {
  287| 	int x, y;
  288| 	size_t from_ofs, dest_ofs, linelen;
  289| 
```

### `src/devices/dev_turbochannel.c` around the row's cited line 250 (HEAD 2d25df65, lines 205-295)

```c
  205| 	memset(d->card_module_name, ' ', 8);
  206| 	memcpy(d->card_module_name, device_name, strlen(device_name));
  207| 
  208| 	/*
  209| 	 *  According to NetBSD/pmax:
  210| 	 *
  211| 	 *  PMAD-AA:  le1 at tc0 slot 2 offset 0x0: address 00:00:00:00:00:00
  212| 	 *  PMAG-AA:  mfb0 at tc0 slot 2 offset 0x0: 1280x1024x8
  213| 	 *  PMAG-BA:  cfb0 at tc0 slot 2 offset 0x0cfb0: 1024x864x8
  214| 	 *  PMAG-CA:  px0 at tc0 slot 2 offset 0x0: 2D, 4x1 stamp, 8 plane
  215| 	 *	(PMAG-DA,EA,FA,FB are also pixelstamps)
  216| 	 *  PMAG-DV:  xcfb0 at tc0 slot 2 offset 0x0: 1024x768x8
  217| 	 *  PMAG-JA:  "truecolor" in Ultrix
  218| 	 *  PMAGB-BA: sfb0 at tc0 slot 0 offset 0x0: 0x0x8
  219| 	 *  PMAGB-VA: sfb0 at tc0 slot 2 offset 0x0: 0x0x8
  220| 	 *  PMAZ-AA:  asc0 at tc0 slot 2 offset 0x0: NCR53C94, 25MHz, SCSI ID 7
  221| 	 *
  222| 	 *  PMAF-FA:  fta0 at tc0 slot 0  (fddi network, "DEC", "V1.0b")
  223| 	 */
  224| 
  225| 	if (strcmp(device_name, "PMAD-AA")==0) {
  226| 		/*  le in NetBSD, Lance ethernet  */
  227| 		dev_le_init(machine, mem, baseaddr, 0, 0,
  228| 		    irq_path, DEV_LE_LENGTH);
  229| 		/*  One ROM at 0x1c03e0, and one at 0x3c0000.  */
  230| 		rom_skip = 0x300;
  231| 		rom_offset = 0x1c0000;
  232| 		rom_length = 0x201000;
  233| 	} else if (strcmp(device_name, "PMAZ-AA")==0) {
  234| 		/*  asc in NetBSD, SCSI  */
  235| 		dev_asc_init(machine, mem, baseaddr, irq_path, d,
  236| 		    DEV_ASC_DEC, NULL, NULL);
  237| 		rom_offset = 0xc0000;
  238| 		/*  There is a copy at 0x0, at least that's where Linux
  239| 		    looks for the rom signature  */
  240| 	} else if (strcmp(device_name, "PMAG-AA")==0) {
  241| 		/*  mfb in NetBSD  */
  242| 		fb = dev_fb_init(machine, mem, baseaddr + VFB_MFB_VRAM,
  243| 		    VFB_GENERIC, 1280, 1024, 2048, 1024, 8, device_name);
  244| 		/*  bt455 = palette, bt431 = cursor  */
  245| 		dev_bt455_init(mem, baseaddr + VFB_MFB_BT455, fb);
  246| 		dev_bt431_init(mem, baseaddr + VFB_MFB_BT431, fb, 8);
  247| 		rom_offset = 0;
  248| 	} else if (strcmp(device_name, "PMAG-BA")==0) {
  249| 		/*  cfb in NetBSD  */
  250| 		fb = dev_fb_init(machine, mem, baseaddr, VFB_GENERIC,
  251| 		    1024,864, 1024,1024,8, device_name);
  252| 		dev_bt459_init(machine, mem, baseaddr + VFB_CFB_BT459,
  253| 		    baseaddr + 0x300000, fb, 8, irq_path, BT459_BA);
  254| 		/*  ROM at both 0x380000 and 0x3c0000?  */
  255| 		rom_offset = 0x380000;
  256| 		rom_length = 0x080000;
  257| 	} else if (strcmp(device_name, "PMAGB-BA")==0) {
  258| 		/*  sfb in NetBSD  */
  259| 		/*  TODO: This is not working with Ultrix yet.  */
  260| 		fb = dev_fb_init(machine, mem, baseaddr + SFB_OFFSET_VRAM,
  261| 		    VFB_GENERIC, 1280,1024, 1280,1024,8, device_name);
  262| 		dev_sfb_init(machine, mem, baseaddr + SFB_ASIC_OFFSET, fb);
  263| 		/*  TODO: the CLEAR doesn't get through, as the address
  264| 			range is already in use by the asic  */
  265| 		dev_bt459_init(machine, mem, baseaddr + SFB_OFFSET_BT459,
  266| 		    baseaddr + SFB_CLEAR, fb, 8, irq_path, BT459_BBA);
  267| 		rom_offset = 0x0;	/*  ? TODO  */
  268| 	} else if (strcmp(device_name, "PMAG-CA")==0) {
  269| 		/*  px in NetBSD  */
  270| 		dev_px_init(machine, mem, baseaddr, DEV_PX_TYPE_PX, irq_path);
  271| 		rom_offset = 0x3c0000;
  272| 	} else if (strcmp(device_name, "PMAG-DA")==0) {
  273| 		/*  pxg in NetBSD  */
  274| 		dev_px_init(machine, mem, baseaddr, DEV_PX_TYPE_PXG, irq_path);
  275| 		rom_offset = 0x3c0000;
  276| 	} else if (strcmp(device_name, "PMAG-EA")==0) {
  277| 		/*  pxg+ in NetBSD: TODO  (not supported by the kernel
  278| 		    I've tried)  */
  279| 		fatal("TODO (see dev_turbochannel.c)\n");
  280| 		rom_offset = 0x3c0000;
  281| 	} else if (strcmp(device_name, "PMAG-FA")==0) {
  282| 		/*  "pxg+ Turbo" in NetBSD  */
  283| 		dev_px_init(machine, mem, baseaddr,
  284| 		    DEV_PX_TYPE_PXGPLUSTURBO, irq_path);
  285| 		rom_offset = 0x3c0000;
  286| 	} else if (strcmp(device_name, "PMAG-DV")==0) {
  287| 		/*  xcfb in NetBSD: TODO  */
  288| 		fb = dev_fb_init(machine, mem, baseaddr + 0x2000000,
  289| 		    VFB_DEC_MAXINE, 0, 0, 0, 0, 0, "PMAG-DV");
  290| 		/*  TODO:  not yet usable, needs a IMS332 vdac  */
  291| 		rom_offset = 0x3c0000;
  292| 	} else if (strcmp(device_name, "PMAG-JA")==0) {
  293| 		/*  "Truecolor", mixed 8- and 24-bit  */
  294| 		dev_pmagja_init(machine, mem, baseaddr, irq_path);
  295| 		rom_offset = 0;		/*  NOTE: 0, not 0x3c0000  */
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

End with one line: `FIXDRAFT_X11CURSORCLIP: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
