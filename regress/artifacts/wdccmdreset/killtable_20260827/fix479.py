"""#479 F-narrow: one helper, called from the TOP of wdc_command().

Every element below was decided by measurement before this file was written:

  WHERE   the TOP, before the switch.  A five-variant matrix measured the end-flush
          form destroying the IDENTIFY response 256/256 words AND a freshly-read
          sector -- and the shipped detector could not see it.
  WHAT    the write flag, the ring, and the phase.  Three sites, one sentence.
  NOT     cur_command -- wdc__write() reads it, and it is set immediately above.
  NOT     the warned_* latches.  A seat named that as the mutant to press: it reads
          as COMPLETING the helper and undoes #337/#464.  dev_asc.c states the rule
          outright at its own latch declarations.
  SCOPE   wdc_command only.  ALT-CTRL is a separate round -- extending the helper to
          the arm as it stands was MEASURED to cancel a legal transfer on a routine
          0x08 Device Control write.
"""
import io

NL, T = chr(10), chr(9)
P = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\src\devices\dev_wdc.c"
s = io.open(P, encoding="utf-8", newline="").read()

# ---- the helper, placed immediately above wdc_command ------------------------
ANCHOR = (NL + "/*" + NL + " *  wdc_command():" + NL)
assert s.count(ANCHOR) == 1, "wdc_command header anchor %d" % s.count(ANCHOR)

HELPER = [
"",
"/*",
" *  wdc_new_command_reset():",
" *",
" *  #479: A NEW COMMAND STARTS WITHOUT THE PREVIOUS COMMAND'S WRITER, BUFFERED",
" *  BYTES, OR PHASE.",
" *",
" *  wdc_command() cleared the ATAPI flag and the error and nothing else, so three",
" *  pieces of the previous command's state survived into the next one.  All three",
" *  were reproduced with liveness controls before this was written:",
" *",
" *    write_in_progress   an ATA write stayed armed across a packet command, so one",
" *                        shared ring served the disk-write path and the CDB path at",
" *                        once.  MEASURED: a guest's own sector write put 512 CD-ROM",
" *                        DATA-IN bytes and ZERO of its own on the image.",
" *    the input ring      residue from an under-drained transfer was never cleared.",
" *                        MEASURED: the drain then fires early and the guest's sector",
" *                        arrives with the previous transfer's bytes at its head.",
" *    atapi_phase         PHASE_CMDOUT survived an ordinary WRITE command.  Latent",
" *                        while the dispatch tests the flag AND the phase -- and #477's",
" *                        comment was pointing a future round straight at it.",
" *",
" *  WHY THE TOP, AND NOT THE END.  IDENTIFY loads its 512-byte response INTO the ring",
" *  as part of the command, and wdc__read() does the same for every ordinary READ.  A",
" *  seat measured the end-of-function form destroying both -- 256 of 256 IDENTIFY",
" *  words wrong, and a freshly-read sector gone -- while every row this round pins",
" *  stayed GREEN.  Clean-up-on-exit reads as the more principled placement and is the",
" *  more dangerous one.",
" *",
" *  WHAT THIS DELIBERATELY DOES NOT TOUCH:",
" *",
" *    cur_command     wdc__write() reads it, and the caller sets it immediately",
" *                    above.  Clearing it here would break the write it is about to",
" *                    set up.",
" *    the warned_*    latches.  Zeroing them alongside everything else reads as",
" *                    COMPLETING this helper and is the mutant to press: it undoes",
" *                    #337 and #464, and it is STRICTLY WORSE than the equivalent",
" *                    mistake in dev_asc.c, because wdc_command() runs far more often",
" *                    than a chip reset.  dev_asc.c says so at its own latch",
" *                    declarations: \"Deliberately NOT cleared by dev_asc_reset() or",
" *                    dev_asc_fifo_flush(): a guest could otherwise re-arm the flood.\"",
" *",
" *  SCOPE.  Called from wdc_command() only.  The ALT-CTRL register is a separately",
" *  registered device that writes state without coming through here, so this does NOT",
" *  establish the invariant on that path -- said out loud rather than implied, and a",
" *  row is red against it.  Extending the helper to that arm AS IT STANDS was MEASURED",
" *  to cancel a legal transfer on an ordinary 0x08 Device Control write, which real",
" *  drivers hold as their steady state.  That extension needs the arm's bit test fixed",
" *  first (WDCTL_RST, not WDCTL_4BIT) and is a separate round.",
" */",
"static void wdc_new_command_reset(struct wdc_data *d)",
"{",
T + "d->atapi_cmd_in_progress = 0;",
T + "d->atapi_phase = 0;",
T + "d->write_in_progress = 0;",
"",
T + "/*  pointer reset rather than a drain loop, matching dev_asc_fifo_flush()'s",
T + "    count-zeroing: there is no consumer to notify and nothing to hand back.  */",
T + "d->inbuf_head = d->inbuf_tail = 0;",
"}",
"",
]
s = s.replace(ANCHOR, NL + NL.join(HELPER) + "/*" + NL + " *  wdc_command():" + NL, 1)

# ---- call it, replacing the partial clear -----------------------------------
OLD = (T + "d->cur_command = idata;" + NL +
       T + "d->atapi_cmd_in_progress = 0;" + NL +
       T + "d->error = 0;" + NL)
assert s.count(OLD) == 1, "wdc_command head anchor %d" % s.count(OLD)
NEW = (T + "d->cur_command = idata;" + NL +
       T + "d->error = 0;" + NL + NL +
       T + "/*  #479: this replaced a bare `d->atapi_cmd_in_progress = 0;`.  The flag" + NL +
       T + "    was one of three pieces of the previous command's state, and clearing" + NL +
       T + "    only the one that had been noticed is what left the other two.  */" + NL +
       T + "wdc_new_command_reset(d);" + NL)
s = s.replace(OLD, NEW, 1)

io.open(P, "w", encoding="utf-8", newline="").write(s)
print("  #479 F-narrow applied: helper added, called from the top of wdc_command()")
