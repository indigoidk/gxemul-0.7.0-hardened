#!/usr/bin/env python3
"""Patch /tmp/gxcensusB/src/cpus/memory_rw.c with a window-census hook.

BUILD B IS AN INSTRUMENTED COPY.  GXEMUL-SEC IS NEVER TOUCHED.

*** THE TRAP THIS PATCH EXISTS TO AVOID, MEASURED ON ITS OWN FIRST VERSION. ***
The hook sits at `do_return_ok:`, which every successful path reaches.  But the
device-dispatch arm does `paddr -= mem->devices[i].baseaddr;` BEFORE calling the
handler, so a device access arrives at do_return_ok with paddr == the RELATIVE
offset (0x00..0x0f for the wdc), not 0x14000000+.  A window test written on
`paddr` therefore sees the UNMAPPED accesses and is blind to the MAPPED ones --
and prints a clean, confident, half-empty census.  Version 1 of this hook did
exactly that: 12 unmapped writes, zero command-block accesses, no error.

So the window is tested on GXC_P0, latched from paddr immediately after address
translation and never touched again.  GXC_LEN0 likewise: the device arm can
truncate `len` at the end of a device's range.
"""
import sys

SRC = "/tmp/gxcensusB/src/cpus/memory_rw.c"
subs = []

#  (1) two extra locals, beside the existing ones
subs.append((
    "\tint cache, no_exceptions, offset;\n",
    "\tint cache, no_exceptions, offset;\n"
    "\tuint64_t gxc_p0 = 0; size_t gxc_len0 = 0;\t/*  CENSUS: build B only  */\n"))

#  (2) latch the ENTRY paddr, right after the v2p block closes
subs.append((
    "\t/*\n\t *  #250: data write-watchpoint.",
    "\tgxc_p0 = paddr; gxc_len0 = len;\t/*  CENSUS: build B only  */\n\n"
    "\t/*\n\t *  #250: data write-watchpoint."))

#  (3) the report itself
subs.append((
    "do_return_ok:\n\treturn MEMORY_ACCESS_OK;\n}",
    r"""do_return_ok:
	/*  ***  CENSUS HOOK -- BUILD B ONLY, NOT IN GXEMUL-SEC.  ***  */
	if (gxc_p0 >= 0x14000000ULL && gxc_p0 < 0x14000040ULL) {
		size_t ci_;
		fprintf(stderr, "GXCENSUS %s paddr=0x%08x len=%d nx=%d val=0x",
		    writeflag == MEM_WRITE ? "W" : "R",
		    (unsigned int) gxc_p0, (int) gxc_len0,
		    no_exceptions ? 1 : 0);
		for (ci_ = 0; ci_ < gxc_len0 && ci_ < 8; ci_++)
			fprintf(stderr, "%02x", data[gxc_len0 - 1 - ci_]);
		fprintf(stderr, " pc=0x%08x\n", (unsigned int) cpu->pc);
		fflush(stderr);
	}
	return MEMORY_ACCESS_OK;
}"""))

s = open(SRC).read()
for old, new in subs:
    n = s.count(old)
    print("anchor occurrences: %d (want 1) for %r" % (n, old[:44]))
    if n != 1:
        sys.exit("ANCHOR NOT UNIQUE -- refusing to patch")
    s = s.replace(old, new)
open(SRC, "w").write(s)
print("patched", SRC)
