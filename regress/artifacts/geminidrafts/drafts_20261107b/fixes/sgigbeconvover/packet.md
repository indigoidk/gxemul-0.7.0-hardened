# GXemul hardened fork -- DRAFT A FIX for one filed issue, `sgigbeconvover` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at lines the coordinator LOCATED from names the row uses (the row cites none) (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `sgigbeconvover`, state `open`, severity `low`)

**title:** dev_sgi_gbe.c DEVICE_TICK: the tile-line conversion loop runs to 512 while memory_rw filled only `len' bytes -- an uninitialised read whose results are computed and then discarded

**state_note (head):**

FILED 2026-09-07.  **RAISED BY THE CODEX SEAT** on the `sgirebufuninit' pass-1 panel, as a narrowing of one of
my own SAFE verdicts, and VERIFIED at HEAD before filing.

`DEVICE_TICK(sgi_gbe)' reads one tile line into a stack buffer and then converts it to host framebuffer
pixels.  **The read length and the conversion bound disagree:**

    int len = tilex < width_in_tiles ? 512 : (partial_pixels * bytes_per_pixel);
    if (len > 512) len = 512;                                  /* OB-14 */
    cpu->memory_rw(cpu, cpu->mem, base + 512 * line, buf, len, MEM_READ, ...);
    ...
    for (int i = 0; i < 512; i += bytes_per_pixel) {           /* <-- 512, NOT len */
            ... color built from buf[i] .. buf[i+3] ...
            get_rgb(d, color, &fb_buf[fb_i], ...);
    }

`memory_rw' fills exactly `len' bytes.  The loop reads `buf[0..511]' **unconditionally**.  `len < 512' is
reachable: on the last tile column (`tilex >= width_in_tiles') it is `partial_pixels * bytes_per_pixel'.  So
`buf[len..511]' is read UNINITIALISED and fed through `get_rgb()'.

*** SCOPE, STATED HONESTLY AND MATCHING THE SEAT'S OWN HEDGE: THIS IS NOT A DISCLOSURE. ***  Only
`fb_len = (len / bytes_per_pixel) * 3' bytes are forwarded by `dev_fb_access', and `fb_len' is derived from
`len' -- so the pixels built from the uninitialised tail are COMPUTED AND DISCARDED.  codex said exactly this:
the smaller forwarded prefix *"prevents me from calling this a demonstrated guest disclosure; it nevertheless
invalidates the blanket initialization-safety claim."*  That is the right call and it is why this is LOW.

**What it IS: an uninitialised read of up to 511 bytes per tile line** -- undefined behaviour, and the kind of
thing an ASAN/MSan sweep is supposed to catch.  `build-asan/' exists and is kept clean, so a cheap first step
is to check whether a sweep already flags this and, if not, why not.

**The fix is one token: `i < len' instead of `i < 512'.**  Note the neighbouring OB-14 clamp shows someone has
already reasoned about this loop's bounds ONCE -- and bounded the READ while leaving the CONSUMPTION at a
literal.  That is the same shape as [[sgirebufuninit]] one file over: a previous round fixed the SIZE and did
not ask what fills, or here consumes, the difference.

NO WITNESS.  Reachability of `len < 512' is established by reading; nothing here shows a guest driving it.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- replace i < 512 with i < len

## The code at the cited lines

### `src/devices/dev_sgi_gbe.c` around line 112 -- LOCATED BY THE COORDINATOR from the name `get_rgb` the row uses (the row cites no line; check this is the defect's site) (HEAD 8d9df658, lines 1-232)

```c
    1| /*
    2|  *  Copyright (C) 2003-2019  Anders Gavare.  All rights reserved.
    3|  *
    4|  *  Redistribution and use in source and binary forms, with or without
    5|  *  modification, are permitted provided that the following conditions are met:
    6|  *
    7|  *  1. Redistributions of source code must retain the above copyright
    8|  *     notice, this list of conditions and the following disclaimer.
    9|  *  2. Redistributions in binary form must reproduce the above copyright  
   10|  *     notice, this list of conditions and the following disclaimer in the 
   11|  *     documentation and/or other materials provided with the distribution.
   12|  *  3. The name of the author may not be used to endorse or promote products
   13|  *     derived from this software without specific prior written permission.
   14|  *
   15|  *  THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
   16|  *  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
   17|  *  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
   18|  *  ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE   
   19|  *  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
   20|  *  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
   21|  *  OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
   22|  *  HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
   23|  *  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
   24|  *  OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
   25|  *  SUCH DAMAGE.
   26|  *   
   27|  *
   28|  *  COMMENT: SGI "Graphics Back End", graphics controller + framebuffer
   29|  *
   30|  *  Guesswork, based on how Linux, NetBSD, and OpenBSD use the graphics on
   31|  *  the SGI O2. Using NetBSD terminology (from crmfbreg.h):
   32|  *
   33|  *  dev_sgi_re.cc:
   34|  *	0x15001000	rendering engine (TLBs)
   35|  *	0x15002000	drawing engine
   36|  *	0x15003000	memory transfer engine
   37|  *	0x15004000	status registers for drawing engine
   38|  *
   39|  *  dev_sgi_gbe.cc:
   40|  *	0x16000000	crm (or GBE) framebuffer control / video output
   41|  *
   42|  *  According to https://www.linux-mips.org/wiki/GBE, the GBE is also used in
   43|  *  the SGI Visual Workstation.
   44|  */
   45| 
   46| #include <stdio.h>
   47| #include <stdlib.h>
   48| #include <string.h>
   49| 
   50| #include "console.h"
   51| #include "cpu.h"
   52| #include "devices.h"
   53| #include "machine.h"
   54| #include "memory.h"
   55| #include "misc.h"
   56| 
   57| #include "thirdparty/crmfbreg.h"
   58| 
   59| 
   60| /*  Let's hope nothing is there already...  */
   61| #define	FAKE_GBE_FB_ADDRESS	0x380000000ULL
   62| 
   63| 
   64| // #define	GBE_DEBUG
   65| // #define debug fatal
   66| 
   67| #define	GBE_DEFAULT_XRES		1280
   68| #define	GBE_DEFAULT_YRES		1024
   69| #define	GBE_DEFAULT_BITDEPTH		8
   70| 
   71| 
   72| struct sgi_gbe_data {
   73| 	// CRM / GBE registers:
   74| 	uint32_t	ctrlstat;		/* 0x00000  */
   75| 	uint32_t	dotclock;		/* 0x00004  */
   76| 	uint32_t	i2c;			/* 0x00008  */
   77| 	uint32_t	i2cfp;			/* 0x00010  */
   78| 
   79| 	uint32_t	freeze;	/* and xy */	/* 0x10000  */
   80| 	uint32_t	y_intr01;		/* 0x10020  */
   81| 	uint32_t	y_intr23;		/* 0x10024  */
   82| 
   83| 	uint32_t	ovr_tilesize;		/* 0x20000  */
   84| 	uint32_t	ovr_control;		/* 0x2000c  */
   85| 
   86| 	uint32_t	tilesize;		/* 0x30000  */
   87| 	uint32_t	frm_control;		/* 0x3000c  */
   88| 
   89| 	uint32_t	palette[32 * 256];	/* 0x50000  */
   90| 
   91| 	uint32_t	cursor_pos;		/* 0x70000  */
   92| 	uint32_t	cursor_control;		/* 0x70004  */
   93| 	uint32_t	cursor_cmap0;		/* 0x70008  */
   94| 	uint32_t	cursor_cmap1;		/* 0x7000c  */
   95| 	uint32_t	cursor_cmap2;		/* 0x70010  */
   96| 	uint32_t	cursor_bitmap[64];	/* 0x78000  */
   97| 
   98| 	// Emulator's representation:
   99| 	int		xres, yres;
  100| 	int 		width_in_tiles;
  101| 	int		partial_pixels;
  102| 	int 		ovr_width_in_tiles;
  103| 	int		ovr_partial_pixels;
  104| 	int		bitdepth;
  105| 	int		color_mode;
  106| 	int		cmap_select;
  107| 	uint32_t	selected_palette[256];
  108| 	struct vfb_data *fb_data;
  109| };
  110| 
  111| 
  112| void get_rgb(struct sgi_gbe_data *d, uint32_t color, uint8_t* r, uint8_t* g, uint8_t* b)
  113| {
  114| 	// TODO: Don't switch on color_mode. For overlays, this is always 
  115| 	// 8-bit index mode!
  116| 	switch (d->color_mode) {
  117| 	case CRMFB_MODE_TYP_I8:
  118| 		color &= 0xff;
  119| 		*r = d->selected_palette[color] >> 24;
  120| 		*g = d->selected_palette[color] >> 16;
  121| 		*b = d->selected_palette[color] >>  8;
  122| 		break;
  123| 	case CRMFB_MODE_TYP_RG3B2:	// Used by NetBSD console mode
  124| 		*r = 255 * ((color >> 5) & 7) / 7;
  125| 		*g = 255 * ((color >> 2) & 7) / 7;
  126| 		*b = (color & 3) * 85;
  127| 		break;
  128| 	case CRMFB_MODE_TYP_RGB8:	// Used by NetBSD's X11 server
  129| 		*r = color >> 24;
  130| 		*g = color >> 16;
  131| 		*b = color >>  8;
  132| 		break;
  133| 	default:/*  #196: (Codex/Fable) d->color_mode is guest-controlled; an
  134| 		    unimplemented WID mode must not exit() the host (get_rgb is
  135| 		    per-pixel, so don't fatal()-flood either) -- render black.  */
  136| 		*r = *g = *b = 0;
  137| 		break;
  138| 	}
  139| }
  140| 
  141| 
  142| void select_palette(struct sgi_gbe_data *d, int palette_nr)
  143| {
  144| 	memmove(&d->selected_palette[0],
  145| 		&d->palette[256 * palette_nr],
  146| 		256 * sizeof(uint32_t));
  147| }
  148| 
  149| 
  150| /*
  151|  *  dev_sgi_gbe_tick():
  152|  *
  153|  *  Every now and then, copy data from the framebuffer in normal ram
  154|  *  to the actual framebuffer (which will then redraw the window).
  155|  *
  156|  *  NOTE: This is very slow, even slower than the normal emulated framebuffer,
  157|  *  which is already slow as it is.
  158|  *
  159|  *  frm_control contains a pointer to an array of uint16_t. These numbers
  160|  *  (when shifted 16 bits to the left) are pointers to the tiles. Tiles are
  161|  *  512x128 in 8-bit mode, 256x128 in 16-bit mode, and 128x128 in 32-bit mode.
  162|  *
  163|  *  An exception is how Linux/O2 uses the framebuffer, in a "tweaked" mode
  164|  *  which resembles linear mode. This code attempts to support both.
  165|  */
  166| DEVICE_TICK(sgi_gbe)
  167| {
  168| 	struct sgi_gbe_data *d = (struct sgi_gbe_data *) extra;
  169| 	uint64_t tiletable;
  170| 	unsigned char buf[16384];	/*  must be power of 2, at most 65536 */
  171| 	int bytes_per_pixel = d->bitdepth / 8;
  172| 	int partial_pixels, width_in_tiles;
  173| 
  174| 	if (!cpu->machine->x11_md.in_use)
  175| 		return;
  176| 
  177| 	// If not frozen...
  178| 	if (!(d->freeze & 0x80000000)) {
  179| 		// ... check if the guest OS wants interrupts based on Y:
  180| 		if ((d->y_intr01 & CRMFB_INTR_0_MASK) != 0xfff000 ||
  181| 		    (d->y_intr01 & CRMFB_INTR_1_MASK) != 0xfff ||
  182| 		    (d->y_intr23 & CRMFB_INTR_2_MASK) != 0xfff000 ||
  183| 		    (d->y_intr23 & CRMFB_INTR_3_MASK) != 0xfff) {
  184| 			fatal("[ sgi_gbe: WARNING: Y interrupts not yet implemented. ]\n");
  185| 		}
  186| 	}
  187| 
  188| 	// printf("d->frm_control = %08x  d->ovr_control = %08x\n", d->frm_control,d->ovr_control);
  189| 
  190| 	// NetBSD's crmfbreg.h documents the tileptr as having a "9 bit shift",
  191| 	// but IRIX seems to put a value ending in 0x......80 there, and the
  192| 	// last part of that address seems to matter.
  193| 	// TODO: Double-check this with the real hardware.
  194| 	
  195| 	if (d->ovr_control & CRMFB_DMA_ENABLE) {
  196| 		tiletable = (d->ovr_control & 0xffffff80);
  197| 		bytes_per_pixel = 1;
  198| 		partial_pixels = d->ovr_partial_pixels;
  199| 		width_in_tiles = d->ovr_width_in_tiles;
  200| 		select_palette(d, 17);	// TODO: is it always palette nr 17 for overlays?
  201| 	} else if (d->frm_control & CRMFB_DMA_ENABLE) {
  202| 		tiletable = (d->frm_control & 0xffffff80);
  203| 		partial_pixels = d->partial_pixels;
  204| 		width_in_tiles = d->width_in_tiles;
  205| 		select_palette(d, d->cmap_select);
  206| 	} else {
  207| 		return;
  208| 	}
  209| 
  210| #ifdef GBE_DEBUG
  211| 	fatal("[ sgi_gbe: dev_sgi_gbe_tick(): tiletable = 0x%llx, bytes_per_pixel = %i ]\n", (long long)tiletable,
  212| 		bytes_per_pixel);
  213| #endif
  214| 
  215| 	if (tiletable == 0)
  216| 		return;
  217| 
  218| 	// Nr of tiles horizontally:
  219| 	int w = width_in_tiles + (partial_pixels > 0 ? 1 : 0);
  220| 
  221| 	// Actually, the number of tiles vertically is usually very few,
  222| 	// but this algorithm will render "up to" 256 and abort as soon
  223| 	// as the screen is filled instead. This makes it work for both
  224| 	// Linux' "tweaked linear" mode and all the other guest OSes.
  225| 	const int max_nr_of_tiles = 256;
  226| 	
  227| 	uint32_t tile[max_nr_of_tiles];
  228| 	uint8_t alltileptrs[max_nr_of_tiles * sizeof(uint16_t)];
  229| 	
  230| 	cpu->memory_rw(cpu, cpu->mem, tiletable,
  231| 	    alltileptrs, sizeof(alltileptrs), MEM_READ,
  232| 	    NO_EXCEPTIONS | PHYSICAL);
```

## The data structures those files define (every field that exists)

### `src/devices/dev_sgi_gbe.c` -- `struct sgi_gbe_data {` (HEAD lines 72-109)

```c
   72| struct sgi_gbe_data {
   73| 	// CRM / GBE registers:
   74| 	uint32_t	ctrlstat;		/* 0x00000  */
   75| 	uint32_t	dotclock;		/* 0x00004  */
   76| 	uint32_t	i2c;			/* 0x00008  */
   77| 	uint32_t	i2cfp;			/* 0x00010  */
   78| 
   79| 	uint32_t	freeze;	/* and xy */	/* 0x10000  */
   80| 	uint32_t	y_intr01;		/* 0x10020  */
   81| 	uint32_t	y_intr23;		/* 0x10024  */
   82| 
   83| 	uint32_t	ovr_tilesize;		/* 0x20000  */
   84| 	uint32_t	ovr_control;		/* 0x2000c  */
   85| 
   86| 	uint32_t	tilesize;		/* 0x30000  */
   87| 	uint32_t	frm_control;		/* 0x3000c  */
   88| 
   89| 	uint32_t	palette[32 * 256];	/* 0x50000  */
   90| 
   91| 	uint32_t	cursor_pos;		/* 0x70000  */
   92| 	uint32_t	cursor_control;		/* 0x70004  */
   93| 	uint32_t	cursor_cmap0;		/* 0x70008  */
   94| 	uint32_t	cursor_cmap1;		/* 0x7000c  */
   95| 	uint32_t	cursor_cmap2;		/* 0x70010  */
   96| 	uint32_t	cursor_bitmap[64];	/* 0x78000  */
   97| 
   98| 	// Emulator's representation:
   99| 	int		xres, yres;
  100| 	int 		width_in_tiles;
  101| 	int		partial_pixels;
  102| 	int 		ovr_width_in_tiles;
  103| 	int		ovr_partial_pixels;
  104| 	int		bitdepth;
  105| 	int		color_mode;
  106| 	int		cmap_select;
  107| 	uint32_t	selected_palette[256];
  108| 	struct vfb_data *fb_data;
  109| };
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

End with one line: `FIXDRAFT_SGIGBECONVOVER: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
