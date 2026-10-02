#!/usr/bin/env python3
"""#529 closing pass (Opus seat) -- mutants of src/devices/dev_sgi_ip32.c, DEVICE_ACCESS(crime).
usage: mutants_close.py <name> <file>   (edits in place; every find-text must occur EXACTLY once, else exit 1 --
so a find that matches nothing is a FAIL, never a silent no-op)"""
import sys

LATCH_T = "\t\tif (!(d->warned & CRIME_W_LEN)) {\n\t\t\td->warned |= CRIME_W_LEN;\n"
GOTO = "\t\t}\n\t\tgoto crime_declined;\n\t}\n\n\tswitch (relative_addr) {\n"
LEN4 = "\t} else if (len == 4) {\n\t\tif (writeflag == MEM_WRITE) {\n\t\t\tif (relative_addr & 4) {\n"
TIMEARM = "\t\tcrime_update_crime_time(d);\n\t\tbreak;\n"
CTLMSG = "\t\t\tif (idata != 0)\n\t\t\t\tfatal(\"[ CRIME_CONTROL: unimplemented \"\n"


def goto_with(prefix):
    return GOTO.replace("\t\tgoto crime_declined;\n", "\t\t" + prefix + "goto crime_declined;\n")


M = {
    "base": [],
    # spot-checks of the pass-2/F2 Opus findings, as table 3 built them
    "lt_len": [("\t\t\td->warned |= CRIME_W_LEN;\n", "\t\t\td->warned |= len;\n")],
    "c_dog": [(GOTO, goto_with("if (relative_addr != CRIME_CONTROL || !(idata & CRIME_CONTROL_DOG_ENABLE)) "))],
    # latch RE-ARMED by an accepted 4-byte access (the sibling of table 3's `rearm', which sat in the len == 8 path)
    "rearm4": [(LEN4, LEN4.replace("\t} else if (len == 4) {\n", "\t} else if (len == 4) {\n\t\td->warned = 0;\n"))],
    # latch PRE-SET by an accepted 4-byte access (the notice silenced before the first refusal)
    "pre4": [(LEN4, LEN4.replace("\t} else if (len == 4) {\n",
                                 "\t} else if (len == 4) {\n\t\td->warned |= CRIME_W_LEN;\n"))],
    # latch re-armed at one named switch label other than DOG
    "rearm_time": [(TIMEARM, "\t\td->warned = 0;\n" + TIMEARM)],
    # a future second latch that reuses bit 0: the CONTROL arm's unimplemented-control text latched on CRIME_W_LEN
    "ctl_collide": [(CTLMSG, CTLMSG.replace("if (idata != 0)",
                                            "if (idata != 0 && !(d->warned & CRIME_W_LEN) && (d->warned |= CRIME_W_LEN))"))],
    # the >= 0x200 partition at the cells hi keeps / hi nodflt do not row
    "wst_mc2": [(GOTO, goto_with("if (writeflag == MEM_WRITE && len == 2 && relative_addr >= 0x200) "
                                 "d->reg[relative_addr / 8] = idata; "))],
    "rd_hi": [(GOTO, goto_with("if (writeflag == MEM_READ && relative_addr >= 0x200) "
                               "odata = d->reg[relative_addr / 8]; "))],
    "lt_blk": [(LATCH_T, "\t\tif (!(d->warned & (CRIME_W_LEN << (relative_addr >= 0x200)))) {\n"
                         "\t\t\td->warned |= CRIME_W_LEN << (relative_addr >= 0x200);\n")],
    # notice keyed on writeflag AND len (brief's untried shape) -- predicted DETECTED
    "lt_wl": [(LATCH_T, "\t\tif (!(d->warned & (CRIME_W_LEN << (2 * (writeflag == MEM_WRITE) + (len == 2))))) {\n"
                        "\t\t\td->warned |= CRIME_W_LEN << (2 * (writeflag == MEM_WRITE) + (len == 2));\n")],
    # a fall-through keyed on a NONZERO written value at the three labels whose refused-store rows all write 0
    "wnz_lbl": [(GOTO, goto_with("if (!(writeflag == MEM_WRITE && idata != 0 && (relative_addr == CRIME_INTSTAT || "
                                 "relative_addr == CRIME_INTMASK || relative_addr == CRIME_TIME))) "))],
    # the goto CONDITIONED ON DEVICE STATE the rows hold constant: (d) operand drawn from a field the skipped code reads.
    # hi_gate: HARDINT, which the enclosing function's own tail reads (restore + recompute) -- in-function, so inside the
    # DEPENDS-ON bound.  pa_gate: prev_asserted, read only in the callee crime_interrupt_reassert() -- outside the bound.
    "hi_gate": [(GOTO, goto_with("if (!d->reg[CRIME_HARDINT / sizeof(uint64_t)]) "))],
    "pa_gate": [(GOTO, goto_with("if (!d->prev_asserted) "))],
    # an accept-side edit at the anchored row's own address, in the width the anchor does not use
    "acc4_210": [(LEN4, LEN4.replace("} else if (len == 4) {", "} else if (len == 4 && relative_addr != 0x210) {"))],
}

name, path = sys.argv[1], sys.argv[2]
src = open(path).read()
for find, repl in M[name]:
    n = src.count(find)
    if n != 1:
        print("MUTANT_TEXT_COUNT %s = %d (want 1)" % (name, n))
        sys.exit(1)
    src = src.replace(find, repl)
open(path, "w").write(src)
print("MUTANT_APPLIED %s (%d edits)" % (name, len(M[name])))
