# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `pvrdirtyregion` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `pvrdirtyregion`, state `open`)

**title:** PVR pvr_extend_update_region(): with zero display width it divides by zero (SIGFPE) on any multi-byte VRAM write whose span straddles DIWADDRL; with ordinary geometry...

**state_note (head):** [2026-11-02, records] Site: pvr_extend_update_region() is src/devices/dev_pvr.c:2307 at 987cb596.  ||  GOVERNING TEXT (from the dispositions file, cut at 400 characters): CONFIRMED-NEW HIGH pvrdirtyregion "PVR pvr_extend_update_region(): with zero display width it divides by zero (SIGFPE) on any multi-byte VRAM write whose span straddles DIWADDRL; with ordinary geometry an unclipped lower endpoint below the display start yields an inverted region and the visible update is discarded"

**The drafter's own reading:** STILL PRESENT: YES -- src/devices/dev_pvr.c:2338

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_pvr.c b/src/devices/dev_pvr.c
index 42f800dd..95c034fe 100644
--- a/src/devices/dev_pvr.c
+++ b/src/devices/dev_pvr.c
@@ -2326,7 +2326,7 @@ void pvr_extend_update_region(struct pvr_data *d, uint64_t low, uint64_t high)
 	high -= vram_ofs;
 
 	/*  Access inside visible part of VRAM?  */
-	if ((int64_t)high >= 0 && (int64_t)low <
+	if (bytes_per_line > 0 && (int64_t)high >= 0 && (int64_t)low <
 	    bytes_per_line * d->ysize) {
 		int new_y1, new_y2;
 
@@ -2335,8 +2335,8 @@ void pvr_extend_update_region(struct pvr_data *d, uint64_t low, uint64_t high)
 
 		/*  Calculate which line the low and high addresses
 		    correspond to:  */
-		new_y1 = low / bytes_per_line;
-		new_y2 = high / bytes_per_line + 1;
+		new_y1 = (int64_t)low / bytes_per_line;
+		new_y2 = (int64_t)high / bytes_per_line + 1;
 
 		if (d->fb_update_y1 < 0 || new_y1 < d->fb_update_y1)
 			d->fb_update_y1 = new_y1;
```

## Every edited function, after the fix

### `src/devices/dev_pvr.c` -- post-edit lines 2320-2351 (`+` marks a line the diff added or the point of a deletion)

```c
 2320|  void pvr_extend_update_region(struct pvr_data *d, uint64_t low, uint64_t high)
 2321|  {
 2322|  	int vram_ofs = REG(PVRREG_DIWADDRL);
 2323|  	int bytes_per_line = d->xsize * d->bytes_per_pixel;
 2324|  
 2325|  	low -= vram_ofs;
 2326|  	high -= vram_ofs;
 2327|  
 2328|  	/*  Access inside visible part of VRAM?  */
 2329|+ 	if (bytes_per_line > 0 && (int64_t)high >= 0 && (int64_t)low <
 2330|  	    bytes_per_line * d->ysize) {
 2331|  		int new_y1, new_y2;
 2332|  
 2333|  		d->fb_update_x1 = 0;
 2334|  		d->fb_update_x2 = d->xsize - 1;
 2335|  
 2336|  		/*  Calculate which line the low and high addresses
 2337|  		    correspond to:  */
 2338|+ 		new_y1 = (int64_t)low / bytes_per_line;
 2339|+ 		new_y2 = (int64_t)high / bytes_per_line + 1;
 2340|  
 2341|  		if (d->fb_update_y1 < 0 || new_y1 < d->fb_update_y1)
 2342|  			d->fb_update_y1 = new_y1;
 2343|  		if (d->fb_update_y2 < 0 || new_y2 > d->fb_update_y2)
 2344|  			d->fb_update_y2 = new_y2;
 2345|  
 2346|  		if (d->fb_update_y1 < 0)
 2347|  			d->fb_update_y1 = 0;
 2348|  		if (d->fb_update_y2 >= d->ysize)
 2349|  			d->fb_update_y2 = d->ysize - 1;
 2350|  	}
 2351|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_PVRDIRTYREGION: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_PVRDIRTYREGION: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
