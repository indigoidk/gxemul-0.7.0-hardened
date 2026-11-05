#!/usr/bin/env python3
"""apply_draft.py <dev_pvr.c> -- write the pvrrenderexit FIX DRAFT (_scratchpad/cloud_fable_20261103/pvrrenderexit/11_packet_fixdraft.md)
into a SCRATCH CLONE's dev_pvr.c, for measurement only.  Every edit is an exact-string replacement whose count is checked; the script
refuses otherwise.  C text is held in raw strings so its escapes reach the file unchanged."""
import io
import sys

p = sys.argv[1]
t = io.open(p, encoding="latin-1", newline="").read()


def rep(old, new, count=1):
    global t
    n = t.count(old)
    if n != count:
        sys.exit("REFUSED: %d hits (want %d) for %r" % (n, count, old[:80]))
    t = t.replace(old, new)


# 1. the two fields, after the struct's first member line
i = t.index("struct pvr_data {")
j = t.index("\n", i) + 1
t = t[:j] + "\tint\t\tzwrite_disabled;\t/*  #NNN: the current polygon's Z-write-disable bit  */\n" \
           + "\tint\t\twarned_nozwrite;\t/*  #NNN: (once) latch  */\n" + t[j:]
# 2. both rasterizers' depth stores
rep("d->vram_z[ofs] = z;", "if (!d->zwrite_disabled)\t/*  #NNN  */\n\t\t\t\t\td->vram_z[ofs] = z;", count=2)
# 3. the exit, replaced by the draft's latch
old = r'''			if (!zwrite) {
				fatal("pvr: no zwrite? not implemented yet.\n");
				exit(1);
			}
'''
new = r'''			/*  #NNN: Z-write DISABLE: depth-tested and drawn, no depth store.  */
			d->zwrite_disabled = !zwrite;
			if (!zwrite && !d->warned_nozwrite) {
				fatal("[ pvr: polygon with Z-write disabled; depth test"
				    " kept, depth store skipped (once) ]\n");
				d->warned_nozwrite = 1;
			}
'''
rep(old, new)
io.open(p, "w", encoding="latin-1", newline="").write(t)
print("draft applied to", p)
