## The derivations (READ, from `DEVICE_ACCESS(crime)`, dev_sgi_ip32.c md5 8c1d1545; every one also measured)

Three facts carry all eleven non-rowed dispositions:

* **F1 -- the prelude rewrites two registers on every access, before the width dispatch, declined or not:**
  `d->reg[CRIME_REV / sizeof(uint64_t)] = d->use_fb? 0xa1 : 0x11;` (:229) and
  `d->reg[CRIME_CONTROL / sizeof(uint64_t)] = CRIME_CONTROL_ENDIANESS;` (:231).  `struct crime_data` is private to the
  file, and no function but `DEVICE_ACCESS(crime)` reads `reg[0]` or `reg[1]` -- `dev_crime_tick`,
  `crime_interrupt_reassert`, `crime_interrupt_assert/deassert` and `crime_update_crime_time` touch SOFTINT, HARDINT,
  INTMASK, INTSTAT and TIME only (grep over the file; `dev_crime_init` is the only other user of the struct).  So a
  value stored into `reg[0]` or `reg[1]` is overwritten before anything can read it.
* **F2 -- the tail is common to both paths:** `crime_declined:` restores HARDINT to its entry value, recomputes
  INTSTAT, and answers a read with `odata` (0 on a decline; memory_rw pre-zeroes the buffer anyway, #95).
* **F3 -- the only text an accepted 4/8-byte access can print** is the CONTROL arm's `fatal()` for a nonzero residue
  (:377-379) and the default arm's `debug()` lines (:397-408).  A silent decline prints nothing.

**E-REV (entries 1, 3, 4).**  Stores at +0x00 (1: 8W, 3: 4W high lane) land in `reg[0]` -- F1.  A 4-byte read at
+0x00 (4) takes the HIGH lane, `odata = (int32_t)(odata >> 32)` (:293-294), which is 0 for 0x11 and for 0xa1 -- the 0 a
decline answers (F2).  The REV arm acts only when `((uint32_t)cpu->pc & 0xffffff00) == (uint32_t)0xbfc05100` (:344),
false for these three (issued from CODE), and prints nothing.  Nothing differs, host text included.

**E-CTL4R (entry 8).**  `lw +0x08` takes CONTROL's high lane: 0x100 >> 32 = 0, the decline's answer.  The CONTROL arm
acts only under `if (writeflag == MEM_WRITE)` (:356).  Nothing differs.  (Also measured before: table 16's
`G_clr_ctl4r` 226/226, and repair 14's `ctl4r.py` 9/9 with its lane-flip liveness control at 8/9.  The `acc ctl4r' /
`p acc ctl4r' rows drive this cell and read 0 either way -- they are the vacuous half of the +0x0c pair, as the
contract already says.)

**E-CTLW (entries 12, 16 = 0; 13, 17 = 0x0200; 43, 44 = 0x0100; each at 4W and 8W).**  The store lands in `reg[1]` --
F1.  The arm clears DOG (:361-363), finds HARD_RESET clear (:364), clears ENDIANESS (:375) and prints only
`if (idata != 0)` (:377-379): for these three values the residue is 0, so no text and no halt.  Nothing differs, host
text included.  The `ctldog sw/sd msg' rows DRIVE 13 and 17 latch-CLEAR and cannot see their decline -- they count
the 0x0201 twin's text, one either way; they exist for `D_nodogclear' (the DOG clear deleted), which is a different
edit.

**H-40 (entry 40, `sw +0x04').**  The store lands in `reg[0]`'s LOW lane (:283-284) -- F1, so no guest channel.
`switch (0x04)` matches no case, so the accepted store reaches the default arm, whose `debug()` prints
`[ crime: write to 0x4: 00 00 00 00 (len=4) ]` while the probe single-steps.  A decline prints nothing.  No row counts
`[ crime: write to 0x4:` -- `dflt ctl' counts the READ line `[ crime: read from 0x4,'.  HOST-DIAGNOSTIC ONLY.

**T (entries 10, 11, 14, 15).**  0x0201 and 0x0001 both leave residue 0x1 (the DOG clear takes 0x0200), so the arm
prints `[ CRIME_CONTROL: unimplemented control 0x0000000000000001 ]` (:377-379); the store itself is overwritten
(F1).  That text is the only difference -- no guest channel -- and it IS counted, in both latch states.
