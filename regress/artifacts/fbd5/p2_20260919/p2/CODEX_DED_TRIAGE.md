# Dedicated codex p2 (GPT-6, 12.7 KB, VERDICT L2) -- main-loop triage, BEFORE merging with the panel consolidation
Answer: _scratchpad/fbd5/p2/codex_ded/codex_fbd5p2.txt (it read BOTH the 111-row packet and the 134-row current tree).
REPAIR (floor / row validity -- fix in-round, one repair diff):
 R1 `&& idata` on each write-decline latch guard; `&& d->irq_enable` on the 18c read guard -> zero-data first access never
    announces.  Rows: X4 -- fresh instance, FIRST access carries 0 (18c read with irq_enable 0) -> announces once, state kept.
 R2 writeflag operand swap: `writeflag == MEM_READ` -> `!idata` (status cases); `writeflag == MEM_WRITE` -> `idata`
    (EnableClear).  X4's zero writes catch the first; a LEGAL zero EnableClear write must announce nothing (new row).
 R3 SEED COLLISION: 0x18&0x30 == 0x50&0x30 == 0x18&0x50 == 0x10 -> `irq_status`->`fiq_status` and `irq_enable`->
    `fiq_status` in the IRQ_STATUS read escape P0/P7/X2.  Re-seed fiq_status 0x50 -> 0x60 (enumerated: every a&b over
    {0x18,0x30,0x60,0xc0} gives 0x10 only for 0x18&0x30 and 0x40 only for 0x60&0xc0; raw values distinct).
 R4 N rows count texts over ALL diagnostics -> swapping two sites' texts keeps every N row green.  Add an ORDER row: the
    five announces appear in access order N1..N5 (arm S accesses the sites in that order); header wording fixed.
 R5 gate pins: SC1/SA1, S1-S5, SF1/SF2 are counts -- a duplicate green line substitutes for a missing id.  Add
    distinct-id pins; `count=1.*` matches count=10 -> `count=1 `.
 R6 narrow DECLINED READ value unchecked (X1 counts only): assert the byte/half 18c read returns 0 (2 rows).
WRONG RECORDS (L4, fix in place):
 W1 sites header: "S3 (... a zero write preserves) is E5's row" -- E5 writes 0x2002; P8 writes 0x10; no zero Clear write.
 W2 sites header: FIQ expression "unpinned everywhere" -- P0/X2 pin it against SYNTHETIC seeded state.
 W3 differential comment: "callbacks are NULL" -- NULL in a bare calloc'd instance; this block INSTALLS no-ops.
 W4 `0x70` "a value inside BOTH enables" -- it has bits in both (0x70&0x30=0x30, 0x70&0xc0=0x40); not inside either.
 W5 pending-probe headers still describe the retired arm K as current.
 W6 the teardown-reorder disclosure names the sites probe only; drain/witness have the same gap (move s.close() first).
DISCLOSE / FILE (coverage debt, above floor):
 D1 H2 vacating edit: next-send result replaced by the saved quit_rc (green, proves nothing new) -- disclose.
 D2 drain/witness H1 score wait()==False; sites checks no prompt ANYWHERE -- tighten both to `"GXemul>" not in buf` (cheap).
 D3 interrupt-output preservation asserted only after the first word decline; X1 instances discard state -- file.
 D4 the gate pins only the sites launcher's legs (drain/witness not gate-run) -- known, recorded.
