#!/usr/bin/env python3
"""#545 repair 3d -- 3c's own pass (panel_20260923_192724, the codex dedicated job, the Opus seat's q2f).
No row is added.  Five X14 checks read what their names and COVERED claim; X12/X13's buffer bytes above the
width are non-zero; the contract's records are corrected.  Writes the patched copy given as argv[2] from argv[1]."""
import io, sys

src, dst = sys.argv[1], sys.argv[2]
s = io.open(src, encoding="utf-8", newline="").read()
T = "\t"


def rep(old, new, count=1):
    global s
    n = s.count(old)
    assert n == count, (n, old[:90])
    s = s.replace(old, new)


# ---------------------------------------------------------------- code
#  E1: the DEVINIT Clear 0x20 row's name claims the pending status (codex, grok, glm)
rep(T * 3 + "/*  repair 3c: the other polarity of the drive at these values -- a Clear that leaves an enabled line\n"
    + T * 3 + "    pending must ASSERT (the row above ends where the drive deasserts)  */\n",
    T * 3 + "/*  repair 3c: the other polarity of the drive at these values -- a Clear that leaves an enabled line\n"
    + T * 3 + "    pending must ASSERT (the row above ends where the drive deasserts); 3d: and the raw status stays\n"
    + T * 3 + "    0x18, as the name says (codex, grok, glm: a Clear that zeroed it here passed every row)  */\n")
rep(T * 3 + "check_u(zn, rv == 1 && x->irq_enable == 0x10 && ZCPU(1, 0) && fatal_calls == 0, 1);\n",
    T * 3 + "check_u(zn, rv == 1 && x->irq_enable == 0x10 && x->irq_status == 0x18 && ZCPU(1, 0) && fatal_calls == 0,\n"
    + T * 3 + "    1);\n")
#  E2: the IRQ_STATUS read row claims "value, fields, output" -- all five fields (grok, glm)
rep(T * 2 + "    && x->irq_enable == 0x10 && x->irq_asserted == 1 && ZCPU(0, 0), 1);\n",
    T * 2 + "    && x->irq_enable == 0x10 && x->irq_asserted == 1 && x->fiq_status == 0 && x->fiq_enable == 0\n"
    + T * 2 + "    && ZCPU(0, 0), 1);\n")
#  E3: the asserted Clears keep the RAW status (the Opus seat's FS01); irq_asserted is left unpinned on purpose
rep(T * 3 + "snprintf(zn, sizeof(zn), \"X14 line 4 raised by a device: Clear %s, CPU line %s once\",\n",
    T * 3 + "snprintf(zn, sizeof(zn), \"X14 line 4 raised by a device: Clear %s, the raw status kept, CPU line %s once\",\n")
rep(T * 3 + "check_u(zn, ok && rv == 1 && x->irq_enable == (k ? 0x10u : 0u) && (k ? ZCPU(1, 0) : ZCPU(0, 1))\n"
    + T * 3 + "    && fatal_calls == 0, 1);\n",
    T * 3 + "/*  3d: a Clear writes the enable only -- the raw status is the sources' (the Opus seat's FS01, a Clear\n"
    + T * 3 + "    dropping the masked line from it, passed).  irq_asserted is NOT pinned here: the enable arms never\n"
    + T * 3 + "    write it, which is `fbirqstuck`'s defect, and a row pinning it would pin that defect.  */\n"
    + T * 3 + "check_u(zn, ok && rv == 1 && x->irq_enable == (k ? 0x10u : 0u) && x->irq_status == 0x10\n"
    + T * 3 + "    && (k ? ZCPU(1, 0) : ZCPU(0, 1)) && fatal_calls == 0, 1);\n")
#  E4: the re-arm row -- irq_asserted and the FIQ fields kept (codex's dedicated job, grok; a decline clearing
#      irq_asserted passed)
rep(T * 2 + "    ok && f0 == 5 && fatal_calls == 5 && ZCPU(1, 0) && x->irq_status == 0x10 && x->irq_enable == 0x10, 1);\n",
    T * 2 + "    ok && f0 == 5 && fatal_calls == 5 && ZCPU(1, 0) && x->irq_status == 0x10 && x->irq_enable == 0x10\n"
    + T * 2 + "    && x->irq_asserted == 1 && x->fiq_status == 0 && x->fiq_enable == 0, 1);\n")
#  E5: X12/X13 -- the buffer bytes above the width are not zero (deepseek: a fetch of 4 bytes passed)
rep(T * 4 + "memory_writemax64(cpu, b, CY[c].w, CY[c].data);\n",
    T * 4 + "memset(b, 0xa5, sizeof(b));      /*  3d: the bytes above the width are NOT zero  */\n"
    + T * 4 + "memory_writemax64(cpu, b, CY[c].w, CY[c].data);\n", count=2)

# ---------------------------------------------------------------- records
rep("    X12: a legal IRQ Clear write at len 1 and 2 with 0x70, and at len 1, 2 and 4 with all-ones data, latches clear\n"
    "\t         (x 4 states): it returns 1, clears (ne = ie & ~idata, idata the low bytes the width carries), drives the\n",
    "    X12: a legal IRQ Clear write at len 1 and 2 with 0x70, and at len 1, 2 and 4 with all-ones data, latches clear\n"
    "\t         (x 4 states): it returns 1, clears (ne = ie & ~idata, idata the low bytes the width carries -- 3d: the\n"
    "\t         buffer's bytes above the width hold 0xa5, as a real store's are not zero, so a fetch past len clears\n"
    "\t         more; deepseek's `memory_readmax64(cpu, data, 4)` passed every row while they were 0), drives the\n")
rep(T + " *  driven, or left alone, and no timer interrupt was touched.  Repair 3c (this block's own pass -- the Opus seat\n"
    + T + " *  measured nine edits at cells this header claimed, on channels its rows did not read: a drive at DEVINIT\n"
    + T + " *  values in either polarity, a decline or the status read driving or clearing while irq_asserted, the reads\n"
    + T + " *  after the latches set returning 0) gave the DEVINIT reads, Set/Clear and declines, the IRQ_STATUS read and\n",
    T + " *  driven, or left alone, and no timer interrupt was touched.  Repair 3c (this block's own pass -- the Opus seat\n"
    + T + " *  measured nine edits at cells this header claimed, on channels its rows did not read: a Clear's drive at\n"
    + T + " *  DEVINIT values in either polarity, a decline driving at those values (TD04) or while irq_asserted (IA14),\n"
    + T + " *  the status read clearing or driving while irq_asserted, the reads after the latches set returning 0) gave\n"
    + T + " *  the DEVINIT reads, Set/Clear and declines, the IRQ_STATUS read and\n")
rep(T + " *  keeps a line pending (q2_20260923/q2e_opus/SUMMARY.txt).\n"
    + T + " *  Width 8 is X6/X7/X9/X10's; +0x184, +0x18c and +0x284 cannot take an 8-byte access.\n",
    T + " *  keeps a line pending (q2_20260923/q2e_opus/SUMMARY.txt).  Repair 3d (3c's own pass): five of those checks\n"
    + T + " *  now read what their names and COVERED claim -- the raw status at the DEVINIT Clear 0x20 (codex, grok, glm:\n"
    + T + " *  a Clear zeroing it there passed) and at the asserted Clears (the Opus seat's FS01), the FIQ fields at the\n"
    + T + " *  IRQ_STATUS read and the re-arm row (grok: a read setting fiq_enable passed), and irq_asserted at the\n"
    + T + " *  re-arm row (a decline clearing it passed) -- with no new row (q2_20260923/r3d_20260923).\n"
    + T + " *  Width 8 is X6/X7/X9/X10's; +0x184, +0x18c and +0x284 cannot take an 8-byte access.\n")
rep(T + " *  COVERED -- the rows named, each observing the channels it names: the return value, the announce count, the\n"
    + T + " *  four fields, the interrupt calls and the read data over the width, except X7 (the return value and the\n"
    + T + " *  announce count only) and X14's rows (the channels in each row's name and header):\n",
    T + " *  COVERED -- the rows named, each observing the channels it names: the return value, the announce count, the\n"
    + T + " *  four fields, the interrupt calls and, for a read, the read data over the width, except X7 (the return\n"
    + T + " *  value and the announce count only) and X14's rows (the channels in each row's name and header):\n")
rep(T + " *    the legal READS of the five readable registers x width (the site's domain) x state, every latch clear (X9)\n"
    + T + " *    and every latch set (X10; X7 for the announce channel);\n",
    T + " *    the legal READS of the five readable registers x width -- 1, 2 and 4 at all five, and 8 at IRQ_STATUS\n"
    + T + " *    and FIQ_STATUS (IRQEnable's 8-byte read is NOT covered, below) -- x state, every latch clear (X9) and\n"
    + T + " *    every latch set (X10; X7 for the announce channel);\n")
rep(T + " *    2 and 4 with all-ones data (0xff, 0xffff, 0xffffffff), every latch clear (X12) and set (X13); at len 4 with\n",
    T + " *    2 and 4 with all-ones data (0xff, 0xffff, 0xffffffff) and the buffer's bytes above the width not zero,\n"
    + T + " *    every latch clear (X12) and set (X13); at len 4 with\n")
rep(T + " *    tick pending, at the five legal reads, a Set and a Clear (the drive in both polarities), and the five\n"
    + T + " *    declines, each with the interrupt output (X14); irq_asserted = 1, raised through the real producer, at the\n"
    + T + " *    IRQ_STATUS read (value, fields, output), the Clear write both ways, and a re-arm row -- five declines, the\n"
    + T + " *    legal reads with their values and a Clear, five declines again: 5 announces, one CPU assert (X14).\n",
    T + " *    tick pending, at the five legal reads, a Set and a Clear (the drive in both polarities, and the raw status\n"
    + T + " *    kept where a Clear leaves a line pending), and the five declines, each with the interrupt output (X14);\n"
    + T + " *    irq_asserted = 1, raised through the real producer, at the IRQ_STATUS read (the value, the five fields --\n"
    + T + " *    irq_status, irq_enable, irq_asserted, fiq_status, fiq_enable -- and the output), the Clear write both ways\n"
    + T + " *    (the enable, the raw status kept, the output), and a re-arm row -- five declines, the legal reads with\n"
    + T + " *    their values and a Clear, five declines again: 5 announces, one CPU assert, the fields and irq_asserted\n"
    + T + " *    kept (X14).\n")
rep(T + " *    a condition on one EXACT field or data value (`d->fiq_enable != 0x10`; `idata == 0` at a latched Clear write\n"
    + T + " *    -- measured green, r3c_20260923; `idata != 0x20` and the `irq_enable`/`irq_status != 0x10` forms at +0x180\n"
    + T + " *    and +0x18c are red since X14, whose rows happen to write 0x20 and hold 0x10 -- by value, not by design): the\n"
    + T + " *    bodies compare nothing against a constant, and no practical set of\n"
    + T + " *    seeded states holds every value (a field's domain is finite, 2^32, but not enumerable here);\n",
    T + " *    a condition on one EXACT field or data value (`d->fiq_enable != 0x10`; `idata == 0` at a latched Clear write\n"
    + T + " *    -- measured green, r3c_20260923): the bodies compare nothing against a constant, and no practical set of\n"
    + T + " *    seeded states holds every value (a field's domain is finite, 2^32, but not enumerable here).  Some such\n"
    + T + " *    forms are red only because a row happens to hold the value, not because a row was written to pin it: the\n"
    + T + " *    `irq_enable`/`irq_status != 0x10` forms at the direction tests of +0x180, +0x184 (since 3c) and +0x18c\n"
    + T + " *    and at all five latch tests (X14 holds 0x10), and `idata != 0x20` at +0x18c since 3c's Clear 0x20 row;\n"
    + T + " *    the same forms at +0x280/+0x284's direction tests, and every `fiq_*` form, are green (the Opus seat,\n"
    + T + " *    3c's pass);\n")
rep(T + " *    a mask on one of the 25 bits of the drive test no device raises (a guest cannot set them in irq_status);\n",
    T + " *    a mask on one of the 25 bits of the drive test no device raises (a guest cannot set them in irq_status),\n"
    + T + " *    except bit 16, which the wide state holds: 24 such masks pass, N_SB16 is red on X9, X10, X12 and X13\n"
    + T + " *    (r3c_20260923);\n")
rep(T + " *    the PRODUCER PAIR's own logic: X14 calls footbridge_interrupt_assert() only to BUILD its instances, and\n"
    + T + " *    nothing here calls _deassert() -- deleting the `~` in its `irq_status &= ~interrupt->line` passes all 862\n"
    + T + " *    rows (codex, repair 3's pass; measured, q2_20260923/r3_20260923/t_deassert.txt).  That pair is\n"
    + T + " *    `fbirqstuck`'s round;\n",
    T + " *    the PRODUCER PAIR's own logic: X14 calls footbridge_interrupt_assert() to build its line-4 instances and\n"
    + T + " *    checks only that one raise from an empty status (irq_status 0x10, irq_asserted 1, one CPU assert -- PR09\n"
    + T + " *    reds it), and nothing here calls _deassert(): deleting the `~` in its `irq_status &= ~interrupt->line`\n"
    + T + " *    passes every row (codex, repair 3's pass; t_deassert.txt, r3_20260923, on 862 rows then; PR04, green on\n"
    + T + " *    864, r3c_20260923).  The pair's bit logic (PR01, PR03, PR04) is filed under `fbirqstuck` by owner ruling\n"
    + T + " *    (2026-09-23), apart from that item's stuck-high line (F13), with the Opus seat's ready rows;\n"
    + T + " *    the CALLER context: every row calls the handler with mem NULL on a machine of type MACHINE_NONE, so a\n"
    + T + " *    condition on `mem` or on the machine type in any test passes every row (the Opus seat, 3c's pass: MC01-\n"
    + T + " *    MC05 and MC07 green on 864; a cats or netwinder caller with a real mem reddens them in its scratch,\n"
    + T + " *    q2f/opus/SUMMARY.txt);\n"
    + T + " *    the announce TEXT: rows count the announces and never read them (TX01);\n"
    + T + " *    a latch's HISTORY beyond the rowed repeats -- X6's first and repeat, X11's pairs, P1's four declines at\n"
    + T + " *    one site: a latch that re-arms after more (codex, 3c's pass: `!(d->warned_irq_status_w++ & 3)`, which\n"
    + T + " *    re-announces at the fifth) passes;\n")
rep(T + " *    the interrupt output's LEVEL: these rows count calls on stubbed callbacks, so a line left high\n"
    + T + " *    (`fbirqstuck`) is invisible here;\n",
    T + " *    the interrupt output's LEVEL: these rows count calls on stubbed callbacks, so a line left high\n"
    + T + " *    (`fbirqstuck`) is invisible here, and so is a Clear that clears irq_asserted (the Opus seat's FS02);\n")
rep(T + " *    N_T08, announce count only), irq_asserted = 1 at the other legal accesses and widths, and a pending tick\n"
    + T + " *    at the other timers.  (F1, `&& !timer_control[0]` on a latch guard, passed every row until X14's DEVINIT\n",
    T + " *    N_T08, announce count only), irq_asserted = 1 at the other legal accesses and widths, a pending tick at\n"
    + T + " *    the other timers, and the rest of the instance (the CPU interrupt's own fields, pcibus, console_handle,\n"
    + T + " *    the timer handles: W03-W05, green on 864).  (F1, `&& !timer_control[0]` on a latch guard, passed every\n"
    + T + " *    row until X14's DEVINIT\n")
rep(T + " *    on the 862 rows, r3_20260923.)  fiq_status has NO writer in the product, so every FIQ status value these\n",
    T + " *    on the 862 rows, r3_20260923, and on the 864, r3c_20260923.)  fiq_status has NO writer in the product,\n"
    + T + " *    so every FIQ status value these\n")
rep("X11's other three states +60; X13 20; X14 19); repair 3's own pass (3c): 862 -> 864 (X14 +2).  */\n",
    "X11's other three states +60; X13 20; X14 19); repair 3's own pass (3c): 862 -> 864 (X14 +2); 3c's own\n"
    "\t    pass (3d): 864, no row added -- five X14 checks read more, and X12/X13's buffer bytes above the width.  */\n")

io.open(dst, "w", encoding="utf-8", newline="").write(s)
print("patched ->", dst)
