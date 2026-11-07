# GXemul hardened fork -- DRAFT A FIX for one filed issue, `sgimtetlbdefault` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at lines the coordinator LOCATED from names the row uses (the row cites none) (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `sgimtetlbdefault`, state `open`, severity `low`)

**title:** dev_sgi_re.c do_mte_transfer(): the `switch (dst_tlb)' default: arm is a guest-drivable UNLATCHED fatal() -- dst_tlb values 3/6/7 come straight from a guest MTE_MODE write (the DST_BUF field), one message per transfer, unbounded.  A READING by the Opus seat during the sgimtelabelcells table, not measured.  Fix shape settled by the file's own ten-bit SGIRE_W_* latch enum and its `own bit, never shared' precedent; the measurement is one session (fill_at(A, RE_TLB_A, 3 << 2)).  Not a host kill (fat [... 33 more characters not shown]

**state_note (head):**

Filed 2026-09-10 from the Opus seat on the sgimtelabelcells repair.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- guest-drivable unlatched fatal with a known, settled fix shape.

## The code at the cited lines

### `src/devices/dev_sgi_re.c` around line 172 -- LOCATED BY THE COORDINATOR from the name `do_mte_transfer` the row uses (the row cites no line; check this is the defect's site) (HEAD 8d9df658, lines 52-292)

```c
   52| #include "misc.h"
   53| 
   54| #include "thirdparty/crmfbreg.h"
   55| #include "thirdparty/sgi_gl.h"
   56| 
   57| 
   58| /*
   59|  *  #497: one latch bit per WIDTH-guard site in DEVICE_ACCESS(sgi_re).
   60|  *
   61|  *  SIX FLAGS, NOT ONE.  dev_wdc.c's own comment adjudicates this: sharing a
   62|  *  latch is licensed only across sites that are MUTUALLY EXCLUSIVE at
   63|  *  runtime.  These six are six different address windows, and any driver
   64|  *  bringing up the rendering engine walks all of them in ONE session, so a
   65|  *  shared latch would report the first odd-width access and silence the
   66|  *  other five.
   67|  */
   68| enum {
   69| 	SGIRE_W_TLBA_LEN  = 1 << 0,
   70| 	SGIRE_W_TLBB_LEN  = 1 << 1,
   71| 	SGIRE_W_TLBC_LEN  = 1 << 2,
   72| 	SGIRE_W_TEX_LEN   = 1 << 3,
   73| 	SGIRE_W_LINA_LEN  = 1 << 4,
   74| 	SGIRE_W_LINB_LEN  = 1 << 5,
   75| 
   76| 	/*  #498: sgi_de's width decline.  ONE bit, not six: the six above are one
   77| 	    per SITE because six windows with six distinct message texts are walked
   78| 	    in a single bring-up session, and one latch would report the first and
   79| 	    silence five.  sgi_de has ONE guard and ONE message text, so the house
   80| 	    per-message-site rule gives one bit.  Measured cost: `sb' then `sh' at
   81| 	    one offset announces len=1 and never len=2 -- accepted, and small,
   82| 	    because the message already prints the width.
   83| 
   84| 	    It must be its OWN bit.  Reusing SGIRE_W_TLBA_LEN scored 23/25: the
   85| 	    four handlers share one malloc'd struct, so any odd-width access to
   86| 	    sgi_re's TLB_A window would silence sgi_de's decline entirely.  */
   87| 	SGIRE_W_DE_LEN    = 1 << 6,
   88| 
   89| 	/*  #499: the unmatched-address catch-all.  TWO bits, one per DIRECTION:
   90| 	    a driver probing an unmapped window commonly reads and writes it in
   91| 	    one pass, and one bit would announce the first and silence the other.
   92| 
   93| 	    PLACED AFTER SGIRE_W_DE_LEN ON PURPOSE.  An earlier draft inserted
   94| 	    these two after SGIRE_W_LINB_LEN (1 << 5), which left the enum ending
   95| 	    at 1 << 6 -- so a maintainer scanning to the LAST enumerator for the
   96| 	    next free bit would take 1 << 7, WHICH THESE TWO LINES BELOW ALREADY
   97| 	    USE.  A duplicate enumerator is legal C and silent, and all four
   98| 	    handlers share one malloc'd struct, so the collision crosses devices.
   99| 
  100| 	    (Wording sharpened after a pass-2 seat read "which is already used"
  101| 	    as a standalone claim about 1 << 7 and reported the comment as
  102| 	    self-contradictory against the code three lines down.  The claim was
  103| 	    right and the sentence did not say BY WHAT.)  */
  104| 	SGIRE_W_UNMAP_WR  = 1 << 7,
  105| 	SGIRE_W_UNMAP_RD  = 1 << 8,
  106| 
  107| 	/*  #500: draw_primitive()'s unimplemented drawing op.  ITS OWN BIT,
  108| 	    for the reason #498 measured on SGIRE_W_DE_LEN: a latch shared with
  109| 	    another site is silenced by that site's ordinary traffic, so the
  110| 	    announce this fix exists to make would never fire.
  111| 
  112| 	    (This comment used to end "The next free bit is 1 << 10; the enum
  113| 	    ends HERE on purpose so that a maintainer scanning to the last
  114| 	    enumerator finds it."  BOTH HALVES WENT FALSE when sgirandompixel
  115| 	    added SGIRE_W_BADMODE = 1 << 10 BELOW this line.  Demoted rather
  116| 	    than deleted, because the REASONING is still why the convention
  117| 	    exists -- and leaving it live would have pointed the next reader at
  118| 	    a taken bit, which is the duplicate-enumerator collision #499
  119| 	    already paid for and warns about four lines up.  The live
  120| 	    next-free claim is on the LAST enumerator, where it belongs.)  */
  121| 	SGIRE_W_PRIM_OP   = 1 << 9,
  122| 
  123| 	/*  sgirandompixel: horrible_getputpixel()'s unimplemented-mode arm.  ITS
  124| 	    OWN BIT, for the reason #498 measured and #500 repeated -- the four
  125| 	    handlers share one malloc'd struct, so a latch shared with another
  126| 	    site is silenced by that site's ordinary traffic and the announce
  127| 	    never fires.  This one matters more than most: the helper is
  128| 	    PER-PIXEL, called inside line, rectangle and tiled-MTE loops, so an
  129| 	    UNLATCHED announce is a per-pixel flood rather than a diagnostic.
  130| 
  131| 	    (This comment used to end "The next free bit is 1 << 11; the enum
  132| 	    ends HERE on purpose, as above."  BOTH HALVES WENT FALSE when #513
  133| 	    added SGIRE_W_TEX_RD = 1 << 11 BELOW this line -- the SAME failure,
  134| 	    in the SAME enum, that the comment ten lines up already records
  135| 	    happening to SGIRE_W_PRIM_OP.  Demoted rather than deleted, for that
  136| 	    comment's own reason: the REASONING is still why the convention
  137| 	    exists, and leaving the claim live would point the next reader at a
  138| 	    TAKEN bit.  The live next-free claim is on the LAST enumerator.)  */
  139| 	SGIRE_W_BADMODE   = 1 << 10,
  140| 
  141| 	/*
  142| 	    #513: THE TEX READ DECLINE GETS ITS OWN BIT, not SGIRE_W_TEX_LEN.
  143| 	    Sharing one was measured at 23/25 for SGIRE_W_DE_LEN in #498: an
  144| 	    ordinary narrow write fires the width latch, and the read decline is
  145| 	    then silently suppressed for the life of the instance.  The detector
  146| 	    has a row for exactly this (`tex xbit', which fires all six width
  147| 	    latches before reading).
  148| 
  149| 	    (This comment used to end "THE NEXT FREE BIT IS 1 << 12, AND THIS
  150| 	    IS THE LAST ENUMERATOR".  #519 added SGIRE_W_BADCOLOR = 1 << 12
  151| 	    BELOW this line and moved the sentence with it, as this comment
  152| 	    itself instructed.  Demoted, not deleted, for the same reason as
  153| 	    the two demotions above it.)
  154| 	 */
  155| 	SGIRE_W_TEX_RD    = 1 << 11,
  156| 
  157| 	/*  #519 (sgirandomcolour): the colour-type PUT decline in
  158| 	    horrible_getputpixel() gets its OWN bit, per the rule every entry
  159| 	    above records: the helper is per-pixel, the struct is shared by
  160| 	    four handlers, and a latch shared with any other site is silenced
  161| 	    by that site's ordinary traffic.  SGIRE_W_BADMODE (1 << 10) is the
  162| 	    TLB/mode switch's decline in the same function and is a different
  163| 	    event with a different text; sharing it would collapse the two.
  164| 
  165| 	    (This comment used to end "THE NEXT FREE BIT IS 1 << 13, AND THIS
  166| 	    IS THE LAST ENUMERATOR".  #564 added SGIRE_W_MTE_STIPPLE ..
  167| 	    SGIRE_W_MTE_BYTEMASK = 1 << 13 .. 1 << 17 BELOW this line and moved
  168| 	    the sentence with them, as this comment itself instructed.  Demoted,
  169| 	    not deleted, for the same reason as the demotions above it.)  */
  170| 	SGIRE_W_BADCOLOR  = 1 << 12,
  171| 
  172| 	/*  #564 (sgirekills, MTE half): do_mte_transfer()'s five declines, ONE
  173| 	    BIT PER SITE, for the reason every entry above records -- a latch
  174| 	    shared with another site is silenced by that site's traffic.  LIN_A
  175| 	    and LIN_B are two values of ONE guard at S3-S5, the shape of
  176| 	    SGIRE_W_BADMODE (one bit, the value in the text).
  177| 
  178| 	    THE NEXT FREE BIT IS 1 << 18, AND THIS IS THE LAST ENUMERATOR --
  179| 	    which is where that claim belongs, per the convention above.  A
  180| 	    maintainer adding a bit BELOW this line must move this sentence
  181| 	    with it and demote the copy here.  */
  182| 	SGIRE_W_MTE_STIPPLE  = 1 << 13,
  183| 	SGIRE_W_MTE_SRC      = 1 << 14,
  184| 	SGIRE_W_MTE_COPY     = 1 << 15,
  185| 	SGIRE_W_MTE_DEPTH    = 1 << 16,
  186| 	SGIRE_W_MTE_BYTEMASK = 1 << 17,
  187| };
  188| 
  189| struct sgi_re_data {
  190| 	// Rendering engine registers:
  191| 	uint16_t	re_tlb_a[256];
  192| 	uint16_t	re_tlb_b[256];
  193| 	uint16_t	re_tlb_c[256];
  194| 	uint16_t	re_tex[112];
  195| 	// todo: clip_ids registers.
  196| 	uint32_t	re_linear_a[32];
  197| 	uint32_t	re_linear_b[32];
  198| 
  199| 	// Drawing engine registers:
  200| 	uint32_t	de_reg[DEV_SGI_DE_LENGTH / sizeof(uint32_t)];
  201| 
  202| 	// Memory transfer engine registers:
  203| 	uint32_t	mte_reg[DEV_SGI_MTE_LENGTH / sizeof(uint32_t)];
  204| 
  205| 	/*
  206| 	 *  #497: width-guard decline latches; see the enum above.
  207| 	 *
  208| 	 *  PLACED LAST, DELIBERATELY, AND THE ORDER IS LOAD-BEARING.
  209| 	 *  re_linear_a/b are written at [tlbi] AND [tlbi+1] with tlbi able to
  210| 	 *  reach 31, so index 32 of either array lands on whichever field
  211| 	 *  FOLLOWS it.  An earlier draft of this change put `warned' between
  212| 	 *  re_linear_b and de_reg; measured with offsetof, that made
  213| 	 *  re_linear_b[32] alias `warned' rather than de_reg[0] -- which both
  214| 	 *  falsified the adjacency the two LINEAR site comments cite, and made
  215| 	 *  an over-run SET WARNING LATCH BITS and silence this device's own
  216| 	 *  diagnostics.  Keeping the latch after mte_reg restores the
  217| 	 *  documented adjacency: re_linear_a[32] is re_linear_b[0] and
  218| 	 *  re_linear_b[32] is de_reg[0].
  219| 	 */
  220| 	uint32_t	warned;
  221| };
  222| 
  223| 
  224| /*
  225|  *  horrible_getputpixel():
  226|  *
  227|  *  This routine gets/puts a pixel in one of the tiles, from the perspective of
  228|  *  the rendering/drawing engine. Given x and y, it figures out which tile
  229|  *  number it is, and then finally does a slow read/write to get/put the pixel
  230|  *  at the correct sub-coordinates within the tile.
  231|  *
  232|  *  Tiles are always 512 _bytes_ wide, and 128 pixels high. For 32-bit color
  233|  *  modes, for example, that means 128 x 128 pixels.
  234|  *
  235|  *  For "linear" modes, y is ignored and x is an offset to select which linear
  236|  *  TLB entry to use.
  237|  */
  238| void horrible_getputpixel(int put, struct cpu* cpu, struct sgi_re_data* d,
  239| 	int x, int y, uint32_t* color, int mode)
  240| {
  241| 	uint32_t color_mode = mode & DE_MODE_TYPE_MASK;
  242| 	int bufdepth = 1 << ((mode >> 8) & 3); 
  243| 
  244| 	// dst_mode (see NetBSD's crmfbreg.h):
  245| 	// #define DE_MODE_TLB_A           0x00000000
  246| 	// #define DE_MODE_TLB_B           0x00000400
  247| 	// #define DE_MODE_TLB_C           0x00000800
  248| 	// #define DE_MODE_LIN_A           0x00001000
  249| 	// #define DE_MODE_LIN_B           0x00001400
  250| 	uint32_t tlb_mode = (mode >> 10) & 0x7;
  251| 	int linear = tlb_mode > 3;
  252| 
  253| 	if (!linear && (x < 0 || y < 0 || x >= 2048 || y >= 2048))
  254| 		return;
  255| 
  256| 	int tilewidth_in_pixels = 512 / bufdepth;
  257| 	
  258| 	int tile_nr_x = x / tilewidth_in_pixels;
  259| 	int tile_nr_y = y >> 7;
  260| 
  261| 	unsigned int tile_nr = tile_nr_y * 16 + tile_nr_x;
  262| 
  263| 	y &= 127;
  264| 	int xofs = (x % tilewidth_in_pixels) * bufdepth;
  265| 	int ofs = 512 * y + xofs;
  266| 
  267| 	uint32_t tileptr = 0;
  268| 
  269| 	/*  #100: cases 0-2 index re_tlb_[abc][256] with a guest-derived
  270| 	    tile_nr = (y>>7)*16 + x/tilewidth; bound it (case 4 self-checks).  */
  271| 	if (tlb_mode <= 2 && tile_nr >= 256)
  272| 		return;
  273| 
  274| 	switch (tlb_mode) {
  275| 	case 0:	tileptr = d->re_tlb_a[tile_nr] << 16;
  276| 		break;
  277| 	case 1:	tileptr = d->re_tlb_b[tile_nr] << 16;
  278| 		break;
  279| 	case 2:	tileptr = d->re_tlb_c[tile_nr] << 16;
  280| 		break;
  281| 	case 4:	tile_nr = x >> 12;
  282| 		if (tile_nr >= 32)
  283| 			return;
  284| 		tileptr = 0x80000000 | (d->re_linear_a[tile_nr] << 12);
  285| 		ofs = x & 4095;
  286| 		// TODO... probably not correct!
  287| 		// printf("tileptr = %08x x = %i y = %i tile_nr = %i ofs = %i\n", tileptr, x, y, tile_nr, ofs);
  288| 		break;
  289| 	default:/*  sgirandompixel: this arm used to assign `*color = random()' -- with
  290| 		    its exit(1) commented out -- so a failed GET handed the CALLER a
  291| 		    random value, and draw_primitive() then wrote it to the destination
  292| 		    in the same loop iteration, since `color' is shared by the XFER GET
```

## The data structures those files define (every field that exists)

### `src/devices/dev_sgi_re.c` -- `struct sgi_re_data {` (HEAD lines 189-221)

```c
  189| struct sgi_re_data {
  190| 	// Rendering engine registers:
  191| 	uint16_t	re_tlb_a[256];
  192| 	uint16_t	re_tlb_b[256];
  193| 	uint16_t	re_tlb_c[256];
  194| 	uint16_t	re_tex[112];
  195| 	// todo: clip_ids registers.
  196| 	uint32_t	re_linear_a[32];
  197| 	uint32_t	re_linear_b[32];
  198| 
  199| 	// Drawing engine registers:
  200| 	uint32_t	de_reg[DEV_SGI_DE_LENGTH / sizeof(uint32_t)];
  201| 
  202| 	// Memory transfer engine registers:
  203| 	uint32_t	mte_reg[DEV_SGI_MTE_LENGTH / sizeof(uint32_t)];
  204| 
  205| 	/*
  206| 	 *  #497: width-guard decline latches; see the enum above.
  207| 	 *
  208| 	 *  PLACED LAST, DELIBERATELY, AND THE ORDER IS LOAD-BEARING.
  209| 	 *  re_linear_a/b are written at [tlbi] AND [tlbi+1] with tlbi able to
  210| 	 *  reach 31, so index 32 of either array lands on whichever field
  211| 	 *  FOLLOWS it.  An earlier draft of this change put `warned' between
  212| 	 *  re_linear_b and de_reg; measured with offsetof, that made
  213| 	 *  re_linear_b[32] alias `warned' rather than de_reg[0] -- which both
  214| 	 *  falsified the adjacency the two LINEAR site comments cite, and made
  215| 	 *  an over-run SET WARNING LATCH BITS and silence this device's own
  216| 	 *  diagnostics.  Keeping the latch after mte_reg restores the
  217| 	 *  documented adjacency: re_linear_a[32] is re_linear_b[0] and
  218| 	 *  re_linear_b[32] is de_reg[0].
  219| 	 */
  220| 	uint32_t	warned;
  221| };
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

End with one line: `FIXDRAFT_SGIMTETLBDEFAULT: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
