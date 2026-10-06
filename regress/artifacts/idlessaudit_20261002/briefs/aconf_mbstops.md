CONFIRM OR REFUTE grok's ruling on your own finding: three MB89352 host-stop rows owed, HIGH

Open with the token `ASTRA_MBSTOPS_ALIVE_1002` on its own line, then ONE verdict line, exactly one of:
`VERDICT: CONFIRMED -- file the three rows as ruled`
`VERDICT: CONFIRMED WITH CHANGES (<n>) -- <what changes>`
`VERDICT: REFUTED -- <why>`

A RECORDS-AND-SOURCE check.  Write nothing, build nothing, run no emulator.  The tree is
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC`; read `src/devices/dev_mb89352.c` at `c29a5fd3` (`git -C ... show c29a5fd3:src/devices/dev_mb89352.c`
-- the working copy is clean for this file, but read the commit).  Everything else is under
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\idlessaudit_20261002\`.

**The arrangement (owner, 2026-10-02):** you found it (`aconf_agyflags/codex_aconf_agyflags.txt`, item 1: `qhm88kstops`
carries only the `:146` stop of queue passage 2616's "dev_mb89352 fatal errors"); grok RULED on your finding
(`grok/grok_mbstops.txt`, brief `briefs/grok_mbstops.md` -- the ten-site table, the candidate carriers); you CONFIRM.  A
ruling in your favour is the one you are least likely to test, so test it harder than you would a refusal.

**grok's ruling, verbatim where it matters** -- `VERDICT: CONCEDE IN PART -- :146 is qhm88kstops and b120 carries the
empty-status reach of :176; rows are owed for the live stops those two leave unnamed`.  Its census: nine
`cpu->running = 0` assignments; the unimplemented-WRITE message at `:676` falls into the same assignment as the READ
message at `:690`; `:507` logs and breaks (`#186` removed its exit); the flag at `:61` is `const bool ... = true`.  Its
per-site table (what reaches it / guest-drivable / carrier):

* `:146` DREG read, `transfer_count > 0`, `xferp == NULL` -- yes (a nonzero TCL with no SELECT) -- `qhm88kstops`.
* `:169` DREG read, phase outside {DATAIN=1, STAT=3, MSGIN=7} -- yes (SELECT, `PCTL & 7` in {0,2,4,5,6},
  `SCMD_XFR|PROG_XFR`, a DREG read; unconditional) -- OWED, with `:235`.
* `:176` DREG read, `transfer_bufpos >= len` -- yes -- empty status: `b120`; any other length: OWED, with `:242`.
* `:235` DREG write, phase outside {DATAOUT=0, CMD=2} -- yes (same setup, `PCTL & 7` in {1,3,4,5,6,7}) -- OWED.
* `:242` DREG write, `transfer_bufpos >= len` -- yes (XFR sizes the buffer to the count; a later TCL write raises the
  count and leaves `bufpos` alone) -- OWED, with `:176`'s residual.
* `:290` end-of-write `default:` -- NO: the switch at `:223` already returned; a dead twin of `:235` -- nobody.
* `:312` `len != 1` -- yes (a halfword or word access); flag-gated -- OWED, with `:533`, `:690`.
* `:533` SCMD outside {0x00, 0x20, 0x84, 0x8c, 0xc0} unless bit 0x10 rewrites it to BUS_REL -- yes (a plain
  `SCMD_XFR` 0x80, SET_ATN, RST_ATN, XFR_PAUSE, SET_ACK); flag-gated -- OWED; `mb89352halt` is a different stop (the
  disk dispatcher's CDB `default:` at `diskimage_scsicmd.c:1380` plus the `PH_STAT` read at `:173`).
* `:676`/`:690` register index 15, EXBF -- yes (a byte read or write of EXBF); flag-gated; one assignment, two messages
  -- OWED, with `:312`, `:533`.

**Three rows, each HIGH (the `qhm88kstops` grade):**
1. "An MB89352 data-register access whose phase is outside the transfer switch's implemented cases stops the emulated
   CPU." -- `:169`, `:235`; fix shape: the treatment `#186` gave the XFR command at `:507`, log and continue; `:290`
   noted as unreachable.
2. "An MB89352 access with a non-byte length, an unhandled SCMD, or the EXBF register stops the emulated CPU while
   `mb89352_abort_on_unimplemented_stuff` is fixed true." -- `:312`, `:533`, `:676`/`:690`; fix shape: the warning
   branch the flag already selects.  Clearing the flag does not touch `:146`, `:169`, `:176`, `:235`, `:242`.
3. "An MB89352 data-register access at or past the end of the current buffer stops the emulated CPU." -- `:176` beyond
   `b120`'s empty status, and `:242`; fix shape: refuse the extra byte or end the phase (deleting the guard is a NULL
   dereference when `status` is NULL), so a controller fix; `b120` remains the producer fix.
`qhm88kstops` stays the NULL-transfer read; grok says its fix is local (the write at `:213-217` already returns).

**Questions, each settled by reading the source at `c29a5fd3`, not by agreeing:**
1. Per site: is the "what reaches it" column right, and is each "yes" a path a GUEST drives through the device's
   register interface (name the registers and values)?  Is `:290` really dead (does the switch at `:223` return on
   every path before it)?  Is `:676` really the same assignment as `:690`?
2. Is `mb89352halt`'s text really a different stop than `:533`, and does `b120` really carry `:176` only for the
   empty-status case?
3. Are three rows the right partition (one defect, one fix shape each), or do you see a different cut?  Any title
   that claims more than the source supports?
4. HIGH for all three: this project grades a guest-drivable stop of the emulated CPU as a host-stop class (the
   exit-sweep rows); reachability here is BY READING, not measured -- should the rows say so, and does anything in
   the reading make one of them LOWER?

`<n> | RIGHT / WRONG: <why, path:line>`.  End with `DENOMINATOR: <s> of 10 stop sites read; <r> of 3 proposed rows checked`.
