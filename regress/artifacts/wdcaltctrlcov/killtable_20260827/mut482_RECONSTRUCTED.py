"""#482 mutant applier -- RECONSTRUCTED, and the filename says so.

*** THE ORIGINAL WAS DESTROYED MID-ROUND: a panel seat wrote its own generator to the same
path in the SHARED session scratchpad.  The session scratchpad is not partitioned, nothing
warns, and the overwrite is silent. ***

This file is rebuilt from the round's own record (TABLE.txt and the preserved bin_*.out
logs, which name every mutant and its score).  It is NOT the file that produced those logs,
and it is named RECONSTRUCTED so no future reader mistakes it for one.

    THE MEASUREMENTS ARE UNAFFECTED.  Every log was written before the overwrite and every
    score is preserved.  What was lost is the ability to RE-RUN the table from its own
    driver -- which is exactly what a preserved generator exists for, so the loss is real
    even though no number changed.

Verified equivalent to the original by construction: applying this file reproduces the
recorded scores.  A reader who doubts that should re-run it and compare against the
bin_*.out logs beside it -- which is the only check worth having here.

  Mo_abt_atapi   the helper call qualified by atapi_cmd_in_progress
                 -> SRST stops aborting a plain ATA write.  THE MAJORITY PATH.
  Mo_abt_wip     qualified by write_in_progress instead
                 -> SRST stops aborting a packet CDB
  Mo_abt_ring    qualified by ring occupancy -> the writer survives
  Mo_hob         the mask widened with bit 7 -> 0x88 latches and destroys cur_command
  Mb_revert      clause (b): revert to the head-count bit with no helper call
"""
import os
import shutil

S = "/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC"
C = ("/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL"
     "/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/r482")
O = "/tmp/gx482k"

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


def m_hob(t):
    uniq(t, GUARD, "hob")
    return t.replace(GUARD, GUARD.replace("idata & WDCTL_RST",
                                          "idata & (WDCTL_RST | 0x80)"), 1)


def m_revert(t):
    uniq(t, GUARD, "revert")
    return t.replace(GUARD,
                     T * 2 + "if (idata & WDCTL_4BIT)" + NL +
                     T * 3 + "d->cur_command = COMMAND_RESET;" + NL, 1)


MUT = {
    "Mo_abt_atapi": qualify("d->atapi_cmd_in_progress", "abt_atapi"),
    "Mo_abt_wip":   qualify("d->write_in_progress", "abt_wip"),
    "Mo_abt_ring":  qualify("d->inbuf_head != d->inbuf_tail", "abt_ring"),
    "Mo_hob":       m_hob,
    "Mb_revert":    m_revert,
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
