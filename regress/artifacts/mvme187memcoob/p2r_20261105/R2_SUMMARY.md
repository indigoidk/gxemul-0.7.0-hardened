Replication readings of the two cloud seats on the same repair-pass-2 packet (`RemoteTrigger run`, same prompt; badge s -- same-model
replication, never a second family).  Banked verbatim at p2r_20261105/OPUS_r2.md and FABLE_r2.md.  New items only; the rest repeat N1-N18.

N19 (Opus r2 GAP 1) a memconf store KEPT ONCE THE LATCH IS SET: `if (!d->warned_memconf) { notice; d->warned_memconf = 1; } else
   d->memcreg.memc_memconf = idata;`.  R3's only memconf read follows its first store; its second store (controller 1) is its last access;
   R7's store is its last access; R8 never reads memconf.  MINE: ACCEPT, floor; the proposed R3 (LD +0x108 after the controller-1 store,
   want 0x3) and R9 (two stores then two loads) catch it.  Opus: "The same shape on the default arm ... is not reachable: the default arm has
   no storage".
N20 (Opus r2, minor) the docstring's "R8's loads at +0x84..+0x87 ... are expected to report under ASan" should say "under B3": under the fix
   the default arm reads no struct byte, so nothing can report.  MINE: ACCEPT (wording).
N21 (Fable r2 G1) a WORD-GRANULAR ALIAS of the served registers: `switch (relative_addr & 0xfc)` (or `case 0x01: case 0x02: case 0x03:`
   added to the chipid arm, likewise chiprev and memconf) -- +0x01..+0x03 would read 0x80, +0x05..+0x07 0x1, +0x09..+0x0b 0x3, and a store
   to +0x09 would be announced as a memconf write; no row reads any such offset.  MINE: ACCEPT, floor (the switch selector is the dispatch
   the fix rewrote); R11 gains loads of +0x01 and +0x0a, want 0 each (a bit-0 mask maps +0x01 onto chipid, a bit-1 mask maps +0x0a onto
   memconf; both come after R11's first default access, so the notice stays about +0xff).
NOT NEW: Opus r2 GAP 2 (text between "ignored" and " (once) ]") is N10; its F2 is N17 and F3 is N11; the file-scope static latch is N16's
   disclosure.  Fable r2 G2 is conditional on the default arm printing read and write notices from two calls -- the code has ONE call with a
   direction string (section 4, lines 128-134), so it is void; its F1-F3 are N10, N12 and N11.
