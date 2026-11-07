# GXemul hardened fork -- DRAFT A FIX for one filed issue, `gdromdmareentr` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at lines the coordinator LOCATED from names the row uses (the row cites none) (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `gdromdmareentr`, state `open`, severity `HIGH`)

**title:** A guest-aimed GD-ROM DMA into its own +0x18 trigger recurses unboundedly and exhausts the host stack -- CONDITIONAL: a nonzero staged word, count and enable armed, data loaded, and the destination inside the trigger window

**state_note (head):**

GOVERNING TEXT (from the dispositions file, cut at 400 characters): `gdromdmareentr` HIGH -- GD-ROM DMA aimed at its own `+0x18` trigger re-enters `dev_dreamcast_gdrom_dma_access` through `memory_rw(PHYSICAL)` with the arming words and `d->data` unchanged: unbounded recursion, the process ends (dev_dreamcast_gdrom.c:1502-1503; memory_rw.c dispatches back into the same handler). No in-f  [title corrected: grok's re-read: true only under a condition the title omitted; Astra ACCEPTS the condition (afile_07)]

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- Unbounded DMA recursion exhausting the host stack is a confirmed crash-on-malformed-input defect.

## The code at the cited lines

### `src/devices/dev_dreamcast_gdrom.c` around line 1697 -- LOCATED BY THE COORDINATOR from the name `dev_dreamcast_gdrom_dma_access` the row uses (the row cites no line; check this is the defect's site) (HEAD 8d9df658, lines 1577-1702)

```c
 1577| 	 *  THE RULE: an UNALIGNED access never stores.  Alignment alone separates
 1578| 	 *  "unimplemented word" from "misaligned access to an implemented one",
 1579| 	 *  and only the first keeps store-and-return.
 1580| 	 *
 1581| 	 *  WHY THAT IS SOUND, as a proof rather than an appeal to intuition about
 1582| 	 *  switch statements -- and INDEPENDENTLY RE-DERIVED by a review seat
 1583| 	 *  before it was believed.  On multiples of 4 the map off -> off/4 is
 1584| 	 *  INJECTIVE, so an aligned offset reaching this arm cannot share an index
 1585| 	 *  with any implemented case: if it did, it would BE that case and the
 1586| 	 *  switch would have matched it.  The implemented DMA offsets are
 1587| 	 *  0x04/0x08/0x0c/0x14/0x18, i.e. indices 1/2/3/5/6; every aligned offset
 1588| 	 *  reaching here yields 0, 4, or 7..31.  Disjoint by construction, not by
 1589| 	 *  inspection.  Truncation can only collide for UNALIGNED addresses, which
 1590| 	 *  is exactly what the guard rejects.
 1591| 	 *
 1592| 	 *  *** A FUTURE `case` AT AN ALIGNED OFFSET KEEPS THIS TRUE AUTOMATICALLY;
 1593| 	 *  ONE AT AN UNALIGNED OFFSET WOULD BREAK IT. ***  There is no such thing
 1594| 	 *  in this device, and the same seat checked the CONTROL window: its
 1595| 	 *  default arm has no store tail at all, so there is no aliasing channel
 1596| 	 *  there to guard, which is why the rule is stated only here.
 1597| 	 *
 1598| 	 *  The bitmap's own bounds guard does NOT help here -- it protects the
 1599| 	 *  latch array, and dma_reg is a different array reached by a different
 1600| 	 *  index.  Two arrays, two bounds problems, and only one of them was
 1601| 	 *  guarded before a seat read the tail.
 1602| 	 */
 1603| 	default:if (GDROM_UNIMPL_FIRST(d->dma_unimpl_reported[
 1604| 		    writeflag == MEM_READ ? GDROM_RD : GDROM_WR],
 1605| 		    relative_addr)) {
 1606| 			if (writeflag == MEM_READ)
 1607| 				fatal("[ dreamcast_gdrom_dma: read from"
 1608| 				    " addr 0x%x -- unimplemented, returning %s."
 1609| 				    "  (once per offset per direction) ]\n", (int)relative_addr,
 1610| 				    (relative_addr & (sizeof(uint32_t) - 1)) ?
 1611| 				    "0" : "the shadow value");
 1612| 			else
 1613| 				fatal("[ dreamcast_gdrom_dma: write to addr"
 1614| 				    " 0x%x: 0x%x -- unimplemented, %s."
 1615| 				    "  (once per offset per direction) ]\n",
 1616| 				    (int)relative_addr, (int)idata,
 1617| 				    (relative_addr & (sizeof(uint32_t) - 1)) ?
 1618| 				    "dropped" : "stored but inert");
 1619| 		}
 1620| 
 1621| 		/*  #461 pass 2: an UNALIGNED declined access must not reach the
 1622| 		    tail, whose truncating index would alias an implemented word.
 1623| 		    Returning here skips BOTH tails; a declined unaligned READ
 1624| 		    therefore also stops leaking the aliased word's value, which
 1625| 		    is the same defect pointing the other way.  */
 1626| 		if (relative_addr & (sizeof(uint32_t) - 1)) {
 1627| 			if (writeflag == MEM_READ)
 1628| 				memory_writemax64(cpu, data, len, 0);
 1629| 			return 1;
 1630| 		}
 1631| 
 1632| 		break;
 1633| 	}
 1634| 
 1635| 	/*  Default write:  */
 1636| 	/*
 1637| 	 *  *** THIS STORE IS WIDTH-BLIND, AND THAT IS ASSESSED-NOT-CHANGED RATHER
 1638| 	 *  THAN OVERLOOKED.  `gdromdmawidth`, adjudicated 2026-08-23. ***
 1639| 	 *
 1640| 	 *  `len` is used ONLY to marshal bytes (memory_readmax64 in, memory_writemax64
 1641| 	 *  out).  An ALIGNED narrow write to an IMPLEMENTED offset therefore widens
 1642| 	 *  to 32 bits zero-extended.  MEASURED on this build: seed +0x04 with
 1643| 	 *  0x11223344 (32-bit), then byte-write 0xff at +0x04, then read back ->
 1644| 	 *  0x000000ff.  Liveness control in the same run returned 0x12345678.
 1645| 	 *
 1646| 	 *  *** THE #461 ALIGNMENT RULE ABOVE NEITHER CAUSES NOR EXCUSES THIS. ***
 1647| 	 *  That rule says an ALIGNED offset reaching the DEFAULT arm is genuinely an
 1648| 	 *  unimplemented word.  It says nothing about an aligned NARROW access to an
 1649| 	 *  IMPLEMENTED offset, which is a separate WIDTH question -- address
 1650| 	 *  decoding and width validation are independent axes.  Written here
 1651| 	 *  because a reader who applies that rule to this store would conclude the
 1652| 	 *  site is safe.
 1653| 	 *
 1654| 	 *  NOT FIXED, and the reason is an ABSENT ORACLE, not laziness.  0x005f74xx
 1655| 	 *  is Sega's Holly ASIC, outside the SH7750 manual, and this project holds
 1656| 	 *  NO documentation for it -- so "real hardware preserves the upper bits"
 1657| 	 *  would be an oracle from plausibility, the #357/#362 shape this tree has
 1658| 	 *  already been burned by once.
 1659| 	 *
 1660| 	 *  *** AND MAINLINE LINUX CONSTRAINS ANY FUTURE FIX, WHICH IS THE FINDING
 1661| 	 *  THAT KILLED THE PANEL'S UNANIMOUS ANSWER. ***  drivers/cdrom/gdrom.c
 1662| 	 *  BYTE-WRITES this window's +0x18 to trigger every DMA transfer, and
 1663| 	 *  BYTE-READS it to poll for completion; the four VALUE registers it uses
 1664| 	 *  (+0x04/08/0c/14) are always 32-bit.  So the width-blind code delivers
 1665| 	 *  exactly what the one real narrow user needs, and a blanket "decline
 1666| 	 *  narrow writes" would BREAK a booting Linux.
 1667| 	 *
 1668| 	 *  THE DECIDED DESIGN, if a fix is ever warranted: decline with a latched
 1669| 	 *  diagnostic at the four VALUE registers ONLY, keeping +0x18 byte-capable.
 1670| 	 *  The discriminating row is seed 0x11223344 / byte 0xff / read back:
 1671| 	 *  0x000000ff today, 0x11223344 declined, 0x112233ff merged.  It must NOT
 1672| 	 *  ship as a green row pinning 0x000000ff -- that would enshrine this
 1673| 	 *  model's own behaviour as an oracle.
 1674| 	 */
 1675| 	if (writeflag == MEM_WRITE)
 1676| 		d->dma_reg[relative_addr / sizeof(uint32_t)] = idata;
 1677| 
 1678| 	if (writeflag == MEM_READ)
 1679| 		memory_writemax64(cpu, data, len, odata);
 1680| 
 1681| 	return 1;
 1682| }
 1683| 
 1684| 
 1685| DEVINIT(dreamcast_gdrom)
 1686| {
 1687| 	struct dreamcast_gdrom_data *d;
 1688| 
 1689| 	CHECK_ALLOCATION(d = (struct dreamcast_gdrom_data *) malloc(sizeof(struct dreamcast_gdrom_data)));
 1690| 	memset(d, 0, sizeof(struct dreamcast_gdrom_data));
 1691| 
 1692| 	memory_device_register(devinit->machine->memory, devinit->name,
 1693| 	    0x005f7000, 0x100, dev_dreamcast_gdrom_access, d,
 1694| 	    DM_DEFAULT, NULL);
 1695| 
 1696| 	memory_device_register(devinit->machine->memory, "gdrom_dma", 0x005f7400,
 1697| 	    0x80, dev_dreamcast_gdrom_dma_access, d, DM_DEFAULT, NULL);
 1698| 
 1699| 	return 1;
 1700| }
 1701| 
 1702| 
```

## The data structures those files define (every field that exists)

### `src/devices/dev_dreamcast_gdrom.c` -- `struct dreamcast_gdrom_data {` (HEAD lines 129-177)

```c
  129| struct dreamcast_gdrom_data {
  130| 	// 0x005f7000: GDROM control registers
  131| 	uint8_t		busy;		/*  Busy status  */
  132| 	uint8_t		stat;		/*  Status  */
  133| 	int		cnt;		/*  Data length in bytes  */
  134| 	uint8_t		cond;
  135| 
  136| 	int		cmd_count;
  137| 	uint8_t		cmd[12];
  138| 
  139| 	uint8_t		*data;
  140| 	int		data_len;
  141| 	int		cur_data_offset;
  142| 	int		cur_cnt;
  143| 
  144| 	/*
  145| 	 *  #460: once-only diagnostic latch, ONE BIT PER SITE.
  146| 	 *
  147| 	 *  Modelled on dev_wdc.c's `warned_badlen` (#337) FOR THE MECHANISM ONLY
  148| 	 *  -- note that dev_wdc.c SHARES one flag between its two sites (:731
  149| 	 *  and :761), so the per-site decision below is this round's own measured
  150| 	 *  warrant and must not be attributed to that precedent.  Not on
  151| 	 *  sh4_val_first().  A review seat named the reason: dev_wdc.c is this
  152| 	 *  tree's OTHER ATA/ATAPI data port and fixed this exact class the same
  153| 	 *  way, while sh4_val_first() is an SH4 helper whose storage lives in
  154| 	 *  sh4_data -- and the GD-ROM is on the Holly/G1 bus, not the SH4.
  155| 	 *
  156| 	 *  Per-site and not one shared bit, MEASURED: a shared bit scores
  157| 	 *  identically on every row that drives ONE site per session -- which
  158| 	 *  was every row this detector had -- and diverges only when two sites
  159| 	 *  run in one session, where it loses the second diagnostic for good.
  160| 	 */
  161| 	uint32_t	warned;
  162| 
  163| 	/*
  164| 	 *  #461: one bit per (direction, word) for each window's default arm.
  165| 	 *  16 + 8 = 24 bytes.
  166| 	 *
  167| 	 *  KEPT SEPARATE FROM #460's `warned` ABOVE, deliberately: those four bits
  168| 	 *  key on a CONDITION at a single offset (0x80), so an offset key cannot
  169| 	 *  separate them.  #443 could unify its three classes only because all of
  170| 	 *  them key on the register offset.  A reviewer will ask; this is why.
  171| 	 */
  172| 	uint32_t	unimpl_reported[GDROM_NDIR][GDROM_BITWORDS(GDROM_NKEYS)];
  173| 	uint32_t	dma_unimpl_reported[GDROM_NDIR][GDROM_BITWORDS(GDROM_DMA_NKEYS)];
  174| 
  175| 	// 0x005f7400: GDROM DMA
  176| 	uint32_t	dma_reg[NREGS_GDROM_DMA];
  177| };
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

End with one line: `FIXDRAFT_GDROMDMAREENTR: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
