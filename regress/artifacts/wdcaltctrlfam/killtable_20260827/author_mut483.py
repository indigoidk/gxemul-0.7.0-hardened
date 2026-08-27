"""#483 mutant applier.

*** THE FILENAME CARRIES AN `author_` PREFIX ON PURPOSE. ***  This session lost `mut482.py`
when a panel seat wrote its own generator to the same path in the shared scratchpad -- silent,
unwarned, and only noticed because the file's contents were suddenly someone else's. The
lesson is applied here rather than only written down.

The mutants are the escapes the #482 panel MEASURED against the 100-row form. Each must now
DIE. If one does not, the corresponding row is decoration.

  disj2     `if (write_in_progress || atapi_cmd_in_progress)` -- built INDEPENDENTLY by
            BOTH flagship seats, and the repair a maintainer most plausibly writes after
            reading #482's four rows.  Killed only by an orphan ring: both flags clear,
            bytes staged.
  wipocc    `if (write_in_progress || ring-occupancy)` -- the same shape through the ring.
  hob6      mask widened with bit 6.  #482's 0x88 row pins bit 7 ONLY, so this escaped it.
  hob7      mask widened with bit 7 -- the one 0x88 does catch, kept as a CONTROL so the
            sweep is shown to subsume the point pin rather than merely coexist with it.
  narrow    the mask NARROWED to 0x06 (RST|IDS): a value with bit 2 but not bit 1 stops
            latching.  *** THIS IS THE DIRECTION A POINT PIN CANNOT SEE AT ALL, and it is
            the whole argument for an IFF assertion. ***
  revert    clause (b), the head-count bit with no helper call.
"""
import os
import shutil

S = "/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC"
C = ("/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL"
     "/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/r483")
O = "/tmp/gx483k"

NL, T = chr(10), chr(9)
GUARD = (T * 2 + "if (idata & WDCTL_RST) {" + NL +
         T * 3 + "d->cur_command = COMMAND_RESET;" + NL +
         T * 3 + "wdc_new_command_reset(d);" + NL +
         T * 2 + "}" + NL)
CALL = T * 3 + "wdc_new_command_reset(d);" + NL


def uniq(t, s, name):
    n = t.count(s)
    assert n == 1, "anchor for %s occurs %d times, want 1" % (name, n)


def qualify(cond, label):
    def f(t):
        uniq(t, CALL, label)
        return t.replace(CALL, T * 3 + "if (" + cond + ")" + NL + T + CALL, 1)
    return f


def mask(expr, label):
    def f(t):
        uniq(t, GUARD, label)
        return t.replace(GUARD, GUARD.replace("idata & WDCTL_RST", expr), 1)
    return f


def m_revert(t):
    uniq(t, GUARD, "revert")
    return t.replace(GUARD,
                     T * 2 + "if (idata & WDCTL_4BIT)" + NL +
                     T * 3 + "d->cur_command = COMMAND_RESET;" + NL, 1)


MUT = {
    "disj2":  qualify("d->write_in_progress || d->atapi_cmd_in_progress", "disj2"),
    "wipocc": qualify("d->write_in_progress || d->inbuf_head != d->inbuf_tail", "wipocc"),
    "hob6":   mask("idata & (WDCTL_RST | 0x40)", "hob6"),
    "hob7":   mask("idata & (WDCTL_RST | 0x80)", "hob7"),
    "narrow": mask("(idata & (WDCTL_RST | WDCTL_IDS)) == (WDCTL_RST | WDCTL_IDS)",
                   "narrow"),
    "revert": m_revert,
    #  ---- the abort-nulling family, found INDEPENDENTLY by BOTH flagship seats ----
    #  The sweep pinned the DECODE across 256 values and the PURGE at none, so any
    #  guard qualifying the abort alone escaped everything.  abort4bit is reachable
    #  by real driver behaviour: 0x04 and 0x06 both lack bit 3.
    "abort4bit": qualify("idata & WDCTL_4BIT", "abort4bit"),
    "abort_ids": qualify("!(idata & WDCTL_IDS)", "abort_ids"),
    "abort_b0":  qualify("!(idata & 0x01)", "abort_b0"),
    "abort_b5":  qualify("!(idata & 0x20)", "abort_b5"),
    #  the opus seat MEASURED this escaping the WEAK sweep while dying to the 0x88
    #  point pin -- which is why "the sweep SUBSUMES the point pin" was FALSE.  It
    #  aborts on a high bit and does NOT latch, so a decode-only sweep cannot see it.
    "hi_abort":  qualify("idata & 0x80", "hi_abort"),
}

if __name__ == "__main__":
    src = open(C + "/src/devices/dev_wdc.c").read()
    shutil.rmtree(O, ignore_errors=True)
    for name, fn in MUT.items():
        d = "%s/%s" % (O, name)
        os.makedirs(d + "/regress")
        os.makedirs(d + "/src/devices")
        shutil.copy(C + "/regress/diff_wdc_identify.c", d + "/regress/")
        t2 = fn(src)
        assert t2 != src, "MUTANT %s CHANGED NOTHING" % name
        open(d + "/src/devices/dev_wdc.c", "w").write(t2)
        print("built", name)
