# `lcaisaphys` -- FIX DESIGN REVIEW **BEFORE** THE EDIT.  You raised this one to HIGH yourself.

## VERDICT LINE FIRST.

**TREE: `GXEMUL-SEC/src/devices/dev_lca.c`.**  You can read files.  Three pristine-2021 upstream
copies sit under the PROJECT root -- ignore them.  **PLEASE DO NOT RATIFY** -- I am proposing an
edit and I want it attacked, not approved.

## S1 -- THIS IS YOUR OWN FINDING COMING BACK

Two hours ago you triaged three unreviewed `dev_lca.c` rows and ruled:

> *"`lcaisaphys` is the first round and is under-ranked at MED -- the window-death claim holds for
> this address ... Fix size: one flag on two calls, house idiom `CACHE_NONE | PHYSICAL` (already how
> `dev_sh4.c`, `dev_pccmos.c`, Maple, etc. forward a known physical address).  It does not disturb
> `#530`'s packing, and it is what makes a post-paging test of the decoder possible."*

**I acted on it: the row is now HIGH.**  Now I want the FIX design attacked before it is built --
the same pre-review that today refused one of my two L2 repairs and saved a wasted table.

## S2 -- THE PROPOSED EDIT, IN FULL

Both nested calls in `DEVICE_ACCESS(lca_isa)` currently pass bare `CACHE_NONE`:

```c
	if (writeflag == MEM_WRITE) {
		byte = data[ofs];
		return cpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE +
		    relative_addr, &byte, 1, writeflag, CACHE_NONE);
	}

	cpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE + relative_addr,
	    &byte, 1, MEM_READ, CACHE_NONE);
```

**Proposed: `CACHE_NONE | PHYSICAL` on both.**  Two tokens, no other change.

## S3 -- THE QUESTIONS

1. **IS `PHYSICAL` ALONE ENOUGH, OR DOES THIS PATH ALSO NEED `NO_EXCEPTIONS`?**  Several in-tree
   forwarders pass `PHYSICAL | NO_EXCEPTIONS`.  **If the translator is bypassed, what is left that
   can still raise?**  I would rather add nothing than add a flag on "it cannot hurt" -- this
   project's addition licence requires a MEASURED DELTA or a TRANSFERRED WARRANT, never a
   plausibility argument.

2. **WHAT DOES THE FIX DO TO THE `fatal()` THAT THE ROW SAYS FLOODS?**  If the window stops dying,
   does the flood stop too, or is there a second guest-drivable `fatal()` on this path that survives
   the flag?  *(Settled premise: `fatal()` here is a PRINT, not a kill -- `src/core/debugmsg.c` has
   no `exit(`/`abort(` and no `-q` early-out -- so the symptom is a flood plus a dead window, not a
   host death.)*

3. ***DOES IT REALLY NOT DISTURB `#530`?***  You said it does not disturb the packing, and I believe
   you -- but `#530`'s detector is **352 rows** and re-tabling it is the expensive outcome.  **Name
   the specific reason the 352 cannot move**, so the claim is checkable rather than trusted.

4. **HOW IS IT WITNESSED?**  You found the gate blind-spot yourself: *every existing LCA probe AND
   `#530`'s 352-row detector run with PTBR=0*, so nothing in the tree can currently see this defect
   OR its fix.  **What is the cheapest rung-3 witness** -- a guest that enables page tables and then
   touches the ISA window?  If there is no cheap one, say so plainly; a round may ship
   documented-only with the attempt recorded, but it may NOT ship pretending it was witnessed.

5. **WHAT IS THE SMALLEST EDIT THAT BREAKS THE FIX AND STILL PASSES?**  The clause-(d) question,
   asked before the detector exists so the detector can be designed against it.

**STANDING LICENSE: if while checking this you find something else, say so.**  Every one of today's
best findings came from a seat checking a different claim.
