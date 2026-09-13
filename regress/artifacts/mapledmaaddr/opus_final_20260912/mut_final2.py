import io, sys
BS = chr(92)
NL = BS + "n"                      # the two characters backslash-n, for C string literals
ASSIGN = "\t\t\todata = d->dmaaddr;\n"
T = "\t\t\t"
MSG = "[ dreamcast_maple: DMAADDR was read ]" + NL
TICKHEAD = ("DEVICE_TICK(maple)\n{\n\tstruct dreamcast_maple_data *d = (struct dreamcast_maple_data *) extra;\n"
            "\tint key;\n")
LEGS = {
 "M_STDERR": [(ASSIGN, T + 'fprintf(stderr, "' + MSG + '");\n' + ASSIGN)],
 "M_FILE":   [(ASSIGN, T + '{ FILE *f = fopen("/tmp/maple_leak_final", "a"); if (f) { fprintf(f, "read' + NL
                       + '"); fclose(f); } }\n' + ASSIGN)],
 "M_ATEXITPRINTF": [("DEVICE_ACCESS(dreamcast_maple)\n",
                     "static int maple_pf_reg = 0;\nstatic void maple_pf_atexit(void)\n{\n"
                     '\tprintf("' + MSG + '");\n}\n\n\nDEVICE_ACCESS(dreamcast_maple)\n'),
                    (ASSIGN, ASSIGN + T + "if (!maple_pf_reg) { maple_pf_reg = 1; atexit(maple_pf_atexit); }\n")],
 # the diagnostic deferred to the device's own tick: the read sets a flag, the next maple tick announces it
 "M_TICKDEFER": [(TICKHEAD, "static int maple_rd_flag = 0;\n" + TICKHEAD
                  + '\tif (maple_rd_flag) { maple_rd_flag = 0; fatal("' + MSG + '"); }\n'),
                 (ASSIGN, ASSIGN + T + "maple_rd_flag = 1;\n")],
 # the same, announced on the SECOND tick after the read (a one-period report delay)
 "M_TICKDEFER2": [(TICKHEAD, "static int maple_rd_flag = 0, maple_rd_pend = 0;\n" + TICKHEAD
                   + '\tif (maple_rd_pend) { maple_rd_pend = 0; fatal("' + MSG + '"); }\n'
                   + "\tif (maple_rd_flag) { maple_rd_flag = 0; maple_rd_pend = 1; }\n"),
                  (ASSIGN, ASSIGN + T + "maple_rd_flag = 1;\n")],
}
src, dst, leg = sys.argv[1:4]
t = io.open(src, encoding="utf-8").read()
if leg not in LEGS: sys.exit("unknown leg %s" % leg)
for old, new in LEGS[leg]:
    if t.count(old) != 1:
        sys.stderr.write("find-text for %s occurs %d times -- REFUSING\n" % (leg, t.count(old))); sys.exit(3)
    t = t.replace(old, new)
io.open(dst, "w", encoding="utf-8", newline="\n").write(t)
print("MUTATED %s" % leg)
