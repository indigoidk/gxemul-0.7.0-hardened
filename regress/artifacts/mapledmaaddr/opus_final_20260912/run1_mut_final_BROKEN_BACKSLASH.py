import io, sys
ASSIGN = "\t\t\todata = d->dmaaddr;\n"
T = "\t\t\t"
LEGS = {
 # stderr, inline during the read -- is stderr carried by the pty and caught?
 "M_STDERR":    (ASSIGN, T + "fprintf(stderr, \"[ dreamcast_maple: DMAADDR read ]\n\");\n" + ASSIGN),
 # stdout printf WITHOUT a newline -- line-buffered; flushes glued onto next output or at exit
 "M_STDOUTNONL":(ASSIGN, T + "printf(\"JUNKDMAADDR\");\n" + ASSIGN),
 # off-channel: write to a file (DISCLOSED as outside the test's reach) -- confirm it escapes
 "M_FILE":      (ASSIGN, T + "{ FILE *f = fopen(\"/tmp/maple_leak_final\", \"a\"); if (f) { fprintf(f, \"read\n\"); fclose(f); } }\n" + ASSIGN),
 # stdout printf WITH newline, but deferred to atexit via a buffered path -- already covered by M_ATEXIT(fatal);
 # here use printf to test the *buffered stdout* variant flushing at exit
 "M_ATEXITPRINTF": [("DEVICE_ACCESS(dreamcast_maple)\n",
                     "static int maple_pf_reg = 0;\nstatic void maple_pf_atexit(void)\n{\n"
                     "\tprintf(\"[ dreamcast_maple: DMAADDR was read ]\n\");\n}\n\n\nDEVICE_ACCESS(dreamcast_maple)\n"),
                    (ASSIGN, ASSIGN + T + "if (!maple_pf_reg) { maple_pf_reg = 1; atexit(maple_pf_atexit); }\n")],
}
src, dst, leg = sys.argv[1:4]
t = io.open(src, encoding="utf-8").read()
if leg not in LEGS: sys.exit("unknown leg %s" % leg)
edits = LEGS[leg] if isinstance(LEGS[leg], list) else [LEGS[leg]]
for old, new in edits:
    if t.count(old) != 1:
        sys.stderr.write("find-text for %s occurs %d times -- REFUSING\n" % (leg, t.count(old))); sys.exit(3)
    t = t.replace(old, new)
io.open(dst, "w", encoding="utf-8", newline="\n").write(t)
print("MUTATED %s" % leg)
