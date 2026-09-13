#!/usr/bin/env python3
"""mapledmaaddr (#528) OPUS FINAL run-3 mutator.  usage: mut_final3.py <SEC dev_dreamcast_maple.c> <out> <LEG>
Each find-text must occur EXACTLY ONCE or the leg is REFUSED.  Backslashes are built with chr(92) (carrier rule)."""
import io, sys

BS = chr(92)
NL = BS + "n"                                   # the two characters backslash-n, for C string literals
ASSIGN = "\t\t\todata = d->dmaaddr;\n"
T = "\t\t\t"
HDR = "DEVICE_ACCESS(dreamcast_maple)\n"
MSG = "[ dreamcast_maple: DMAADDR was read ]" + NL
TICKHEAD = ("DEVICE_TICK(maple)\n{\n\tstruct dreamcast_maple_data *d = (struct dreamcast_maple_data *) extra;\n"
            "\tint key;\n")


def deferred(body, keyed):
    cond = "d->dmaaddr != 0 && " if keyed else ""
    return [(HDR, "static int maple_q_reg = 0;\nstatic void maple_q_die(void)\n{\n\t" + body + "\n}\n\n\n" + HDR),
            (ASSIGN, ASSIGN + T + "if (" + cond + "!maple_q_reg) { maple_q_reg = 1; atexit(maple_q_die); }\n")]


LEGS = {
    # the exit(1) half of the removed defect, moved to process exit, keyed on a nonzero field: silent, status 1
    "M_EXITATQUIT": deferred("_Exit(1);", True),
    # the same as a crash at teardown (SIGABRT), keyed on a nonzero field
    "M_ABORTATQUIT": deferred("abort();", True),
    # CONTROL: unkeyed -- the marker session (field 0) registers it too, so `exit status' must red
    "M_EXITATQUIT0": deferred("_Exit(1);", False),
    # the diagnostic announced on the THIRD maple tick after the read (a session sees <= 3: the first-step tick + the
    # two cpu_run_deinit() ticks) -- predicted caught only where the read is the first stepped instruction
    "M_TICKDEFER3": [(TICKHEAD, "static int maple_rd_flag = 0, maple_rd_age = 0;\n" + TICKHEAD
                      + "\tif (maple_rd_flag && ++maple_rd_age == 3) { maple_rd_flag = 0; fatal(\"" + MSG + "\"); }\n"),
                     (ASSIGN, ASSIGN + T + "if (!maple_rd_flag) { maple_rd_flag = 1; maple_rd_age = 0; }\n")],
    # a PERIODIC SUMMARY: every 4th maple tick, report how many DMAADDR reads happened since the last report (a
    # bounded, rate-limited announce) -- predicted never printed in any probe session
    "M_TICKPERIODIC4": [(TICKHEAD, "static int maple_rd_count = 0, maple_tick_n = 0;\n" + TICKHEAD
                         + "\tif (++maple_tick_n % 4 == 0 && maple_rd_count) { fatal(\"[ dreamcast_maple: DMAADDR was"
                         + " read (%i times) ]" + NL + "\", maple_rd_count); maple_rd_count = 0; }\n"),
                        (ASSIGN, ASSIGN + T + "maple_rd_count++;\n")],
}

src, dst, leg = sys.argv[1:4]
t = io.open(src, encoding="utf-8").read()
if leg not in LEGS:
    sys.exit("unknown leg %s -- REFUSING" % leg)
for old, new in LEGS[leg]:
    if t.count(old) != 1:
        sys.stderr.write("find-text for %s occurs %d times -- REFUSING\n" % (leg, t.count(old)))
        sys.exit(3)
    t = t.replace(old, new)
io.open(dst, "w", encoding="utf-8", newline="\n").write(t)
print("MUTATED %s" % leg)
