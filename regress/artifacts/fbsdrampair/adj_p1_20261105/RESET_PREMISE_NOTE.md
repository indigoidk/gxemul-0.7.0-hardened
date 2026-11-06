# fbsdrampair -- the "documented reset value 00FC0000h" was a FALSE PREMISE of the pass-1 packet (read 2026-11-05)

The pass-1 packet (cloud_r3/MYTHOS_FBSDRAM_P1.md, section 4b) cited _scratchpad/dc21285.txt:3225 -- "The SDRAM base address mask is
reset to 00FC0000h" -- as the register's reset value.  Read in context it is NOT the general reset value:
* dc21285.txt:3206-3210 -- "Blank ROM Programming.  The 21285 has a mode that allows programming of blank Flash ROMs in place on a
  circuit board.  This mode is enabled if both ma[6] and pci_cfn are 0 when the 21285 is reset.  When this mode is enabled:" -- and
  :3212-3228 is that list (nRESET held on the SA-110 "since there may be no code in the ROM yet", ..., the SDRAM mask reset to
  00FC0000h).  It is the blank-ROM-programming default only.
* The register tables give the normal reset value: 7.3.9 (dc21285.txt:5849-5873) -- reading the pdftotext stagger with the offset
  table as the calibrator (7.3.10, :5902-5914, where "Read only as 0." on the 27:18 line belongs to 17:0 and the Offset field's
  description ends "Reset value: 0.") -- the Mask field's description ends "Reset value: 0." (printed on the 30:28 line) and bit 31
  (SDRAM window disable) carries "Reset value: 0." (:5873).  7.3.10's Offset field: "Reset value: 0." (:5912).
* Both registers "must be written by the SA-110 before the initialize complete bit [1] in the SA-110 control register is set"
  (:5846-5847, :5899-5900).
So in normal operation BOTH registers reset to 0: the declined value 0 is the house decline value (#545) AND the documented normal
reset value.  The design rulings that chose RESET = 0x00FC0000 (ADJ_MYTHOS_r2.md, ADJ_MYTHOS_r3.md; and four of the six pass-1
readings) rested on this premise; ADJ_MYTHOS.md ruled ZERO on independent grounds (member discipline, the transient reset, the #545
precedent, F2).  Disposition recorded, not ruled: implement ZERO; the comment cites 7.3.9/7.3.10 (R/W registers, normal reset value 0)
and notes 00FC0000h as the blank-ROM-programming default; carry this note to the pass-2 panel so the reset-value seats can answer it.

*Corrected 2026-11-05 (main loop): this file's time-of-day stamp(s) (removed: ~08:1xZ) were GUESSES from the main loop's wrong clock -- later than this file's own creation time, so impossible as written.  The file's own timestamps are the record: created 07:44Z, last written 07:44Z before this note (UTC).*
