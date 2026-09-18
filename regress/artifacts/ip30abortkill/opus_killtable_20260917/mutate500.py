import subprocess, sys, os, shutil
BS = chr(92); TAB = chr(9); NL = chr(10)
SRC = "/tmp/gxopus500/src/devices/dev_sgi_re.c"
BASE = "/tmp/gxopus500_baseline.c"

FATAL_ARG = TAB*3 + "    op, x1, y1, x2, y2, fg, bg, pattern);"

MUTANTS = {
 "base":  [],
 "M1_exit0":     [(FATAL_ARG, FATAL_ARG + NL + TAB*2 + "}" + NL + TAB*2 + "exit(0);" + NL + TAB*2 + "if (0) {")],
 "M2_bit1s6":    [("SGIRE_W_PRIM_OP   = 1 << 9,", "SGIRE_W_PRIM_OP   = 1 << 6,")],
 "M3_nolatch":   [(TAB*3 + "d->warned |= SGIRE_W_PRIM_OP;" + NL, "")],
 "M4_notext":    [(' pattern=0x%08x -- declined.  (once) ]', ' pattern=0x%08x ]')],
 "M5_exit1":     [(FATAL_ARG, FATAL_ARG + NL + TAB*2 + "}" + NL + TAB*2 + "exit(1);" + NL + TAB*2 + "if (0) {")],
 "M6_debug":     [(TAB*3 + 'fatal("[ sgi_de: UNIMPLEMENTED drawing op', TAB*3 + 'debug("[ sgi_de: UNIMPLEMENTED drawing op')],
 "M7_bit1s0":    [("SGIRE_W_PRIM_OP   = 1 << 9,", "SGIRE_W_PRIM_OP   = 1 << 0,")],
}

def apply(name):
    txt = open(BASE).read()
    for old, new in MUTANTS[name]:
        n = txt.count(old)
        if n != 1:
            print("MUTANT_TEXT_NOT_FOUND %s count=%d" % (name, n)); sys.exit(9)
        txt = txt.replace(old, new)
    open(SRC, "w").write(txt)

def build():
    subprocess.call(["rm", "-f", "/tmp/gxopus500/src/devices/dev_sgi_re.o",
                     "/tmp/gxopus500/gxemul"])
    rc = subprocess.call("cd /tmp/gxopus500 && make -j4 > /tmp/mb.log 2>&1", shell=True)
    if not os.path.exists("/tmp/gxopus500/gxemul"):
        return False, "NO_BINARY rc=%d" % rc
    if os.path.getmtime("/tmp/gxopus500/gxemul") < os.path.getmtime(SRC):
        return False, "STALE_BINARY"
    return True, "ok"

if not os.path.exists(BASE):
    shutil.copy(SRC, BASE)

for name in sys.argv[1:]:
    open("/tmp/gxopus500/.MUTANT", "w").write("dev_sgi_re.c " + name + NL)
    apply(name)
    ok, msg = build()
    print("=== %s build %s (%s)" % (name, "OK" if ok else "FAIL", msg)); sys.stdout.flush()
    if not ok:
        print(open("/tmp/mb.log").read()[-2000:]); continue
    out = subprocess.run(["python3", "-u", "/tmp/probe500.py", "/tmp/gxopus500/gxemul", name],
                         capture_output=True, text=True, timeout=1800).stdout
    open("/tmp/res_" + name + ".txt", "w").write(out)
    fails = [l.split()[0] for l in out.splitlines() if l.rstrip().endswith("FAIL")]
    res = [l for l in out.splitlines() if "OPUS498T_RESULT" in l or "OPUS498T_DONE" in l
           or "OPUS498T_CONTROL" in l]
    print("    %s  FAILING_ROWS=%s" % (" ".join(res), ",".join(fails) if fails else "(none)"))
    sys.stdout.flush()

shutil.copy(BASE, SRC)
os.remove("/tmp/gxopus500/.MUTANT")
print("RESTORED")
