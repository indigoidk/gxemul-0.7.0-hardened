# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `vgagfxwindowend` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `vgagfxwindowend`, state `open`)

**title:** src/devices/dev_vga.c DEVICE_ACCESS(vga_graphics) -- `relative_addr + len >= GFX_ADDR_WINDOW` declines an access that ends exactly at the window's end (the window's last word), an off-by-one; it is the producer the #582 design rulings found for the PowerPC failed-read block's arm (d)

**state_note (head):** Filed 2026-11-05 by #582: the design rulings' dev_vga bound (regress/artifacts/qhslowifetch/adj_20261104/FABLE_FINAL_r2.md, its F1, and RECON_FABLE.md, which carries 'the dev_vga >= filing' into the merged design).  Read, not measured: src/devices/dev_vga.c:617.  Fixing it removes `ppcifetchdeclineprod`'s producer (ROW 5).

**The drafter's own reading:** STILL PRESENT: YES -- line 617: `if (relative_addr + len >= GFX_ADDR_WINDOW)`

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_vga.c b/src/devices/dev_vga.c
index 16681cd6..de31be48 100644
--- a/src/devices/dev_vga.c
+++ b/src/devices/dev_vga.c
@@ -614,7 +614,7 @@ DEVICE_ACCESS(vga_graphics)
 	int j, x=0, y=0, x2=0, y2=0, modified = 0;
 	size_t i;
 
-	if (relative_addr + len >= GFX_ADDR_WINDOW)
+	if (relative_addr + len > GFX_ADDR_WINDOW)
 		return 0;
 
 	if (d->cur_mode != MODE_GRAPHICS)
```

## Every edited function, after the fix

### `src/devices/dev_vga.c` -- post-edit lines 611-722 (`+` marks a line the diff added or the point of a deletion)

```c
  611|  DEVICE_ACCESS(vga_graphics)
  612|  {
  613|  	struct vga_data *d = (struct vga_data *) extra;
  614|  	int j, x=0, y=0, x2=0, y2=0, modified = 0;
  615|  	size_t i;
  616|  
  617|+ 	if (relative_addr + len > GFX_ADDR_WINDOW)
  618|  		return 0;
  619|  
  620|  	if (d->cur_mode != MODE_GRAPHICS)
  621|  		return 1;
  622|  
  623|  	switch (d->graphics_mode) {
  624|  	case GRAPHICS_MODE_8BIT:
  625|  		y = relative_addr / d->max_x;
  626|  		x = relative_addr % d->max_x;
  627|  		y2 = (relative_addr+len-1) / d->max_x;
  628|  		x2 = (relative_addr+len-1) % d->max_x;
  629|  
  630|  		if (writeflag == MEM_WRITE) {
  631|  			if (relative_addr + len <= (uint64_t)d->gfx_mem_size) {	/* OB-15 */
  632|  				memcpy(d->gfx_mem + relative_addr, data, len);
  633|  				modified = 1;	/* OB-15b: only mark dirty when copied */
  634|  			} else {
  635|  				static int w_warned = 0;	/* #119: loud-once */
  636|  				if (!w_warned) {
  637|  					fatal("[ vga: gfx write 0x%x+%i beyond 0x%x; "
  638|  					    "ignored ]\n", (int)relative_addr, (int)len,
  639|  					    (int)d->gfx_mem_size);
  640|  					w_warned = 1;
  641|  				}
  642|  			}
  643|  		} else {
  644|  			if (relative_addr + len <= (uint64_t)d->gfx_mem_size)	/* OB-15 */
  645|  				memcpy(data, d->gfx_mem + relative_addr, len);
  646|  			else {
  647|  				static int r_warned = 0;	/* #119: loud-once */
  648|  				if (!r_warned) {
  649|  					fatal("[ vga: gfx read 0x%x+%i beyond 0x%x; "
  650|  					    "zero-filled ]\n", (int)relative_addr, (int)len,
  651|  					    (int)d->gfx_mem_size);
  652|  					r_warned = 1;
  653|  				}
  654|  				memset(data, 0, len);	/* OB-15c: don't leak uninit host memory */
  655|  			}
  656|  		}
  657|  		break;
  658|  	case GRAPHICS_MODE_4BIT:
  659|  		y = relative_addr * 8 / d->max_x;
  660|  		x = relative_addr * 8 % d->max_x;
  661|  		y2 = ((relative_addr+len)*8-1) / d->max_x;
  662|  		x2 = ((relative_addr+len)*8-1) % d->max_x;
  663|  		/*  TODO: color stuff  */
  664|  
  665|  		/*  Read/write d->gfx_mem in 4-bit color:  */
  666|  		if (writeflag == MEM_WRITE) {
  667|  			/*  i is byte index to write, j is bit index  */
  668|  			for (i=0; i<len; i++)
  669|  				for (j=0; j<8; j++) {
  670|  					int pixelmask = 1 << (7-j);
  671|  					int b = data[i] & pixelmask;
  672|  					int m = d->sequencer_reg[
  673|  					    VGA_SEQ_MAP_MASK] & 0x0f;
  674|  					uint32_t addr = (y * d->max_x + x +
  675|  					    i*8 + j) * d->bits_per_pixel / 8;
  676|  					unsigned char byte;
  677|  					if (!(d->graphcontr_reg[
  678|  					    VGA_GRAPHCONTR_MASK] & pixelmask))
  679|  						continue;
  680|  					if (addr >= d->gfx_mem_size)
  681|  						continue;
  682|  					byte = d->gfx_mem[addr];
  683|  					if (b && j&1)
  684|  						byte |= m << 4;
  685|  					if (b && !(j&1))
  686|  						byte |= m;
  687|  					if (!b && j&1)
  688|  						byte &= ~(m << 4);
  689|  					if (!b && !(j&1))
  690|  						byte &= ~m;
  691|  					d->gfx_mem[addr] = byte;
  692|  				}
  693|  			modified = 1;
  694|  		} else {
  695|  			fatal("TODO: 4 bit graphics read, mask=0x%02x\n",
  696|  			    d->sequencer_reg[VGA_SEQ_MAP_MASK]);
  697|  			for (i=0; i<len; i++)
  698|  				data[i] = random();
  699|  		}
  700|  		break;
  701|  	default:fatal("dev_vga: Unimplemented graphics mode %i\n",
  702|  		    d->graphics_mode);
  703|  		cpu->running = 0;
  704|  	}
  705|  
  706|  	if (modified) {
  707|  		d->modified = 1;
  708|  		if (x < d->update_x1)  d->update_x1 = x;
  709|  		if (x > d->update_x2)  d->update_x2 = x;
  710|  		if (y < d->update_y1)  d->update_y1 = y;
  711|  		if (y > d->update_y2)  d->update_y2 = y;
  712|  		if (x2 < d->update_x1)  d->update_x1 = x2;
  713|  		if (x2 > d->update_x2)  d->update_x2 = x2;
  714|  		if (y2 < d->update_y1)  d->update_y1 = y2;
  715|  		if (y2 > d->update_y2)  d->update_y2 = y2;
  716|  		if (y != y2) {
  717|  			d->update_x1 = 0;
  718|  			d->update_x2 = d->max_x - 1;
  719|  		}
  720|  	}
  721|  	return 1;
  722|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_VGAGFXWINDOWEND: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_VGAGFXWINDOWEND: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
