import subprocess, sys, os, shutil
TAB = chr(9); NL = chr(10)
SRC = "/tmp/gxopus500/src/devices/dev_sgi_re.c"
BASE = "/tmp/gxopus500_baseline.c"
MUTANTS = {
 "base": [],
 "M8_maskwide": [("switch (op & 0xff000000) {", "switch (op & 0xffff0000) {")],
 "M9_notext":   [(' pattern=0x%08x -- declined.  (once) ]', ' pattern=0x%08x ]')],
 "M10_debug":   [(TAB*3 + 'fatal("[ sgi_de: UNIMPLEMENTED drawing op',
                  TAB*3 + 'debug("[ sgi_de: UNIMPLEMENTED drawing op')],
}
def apply(name):
    txt = open(BASE).read()
    for old, new in MUTANTS[name]:
        if txt.count(old) != 1:
            print("MUTANT_TEXT_NOT_FOUND %s count=%d" % (name, txt.count(old))); sys.exit(9)
        txt = txt.replace(old, new)
    open(SRC, "w").write(txt)
def build():
    subprocess.call(["rm", "-f", "/tmp/gxopus500/src/devices/dev_sgi_re.o", "/tmp/gxopus500/gxemul"])
    subprocess.call("cd /tmp/gxopus500 && make -j4 > /tmp/mb2.log 2>&1", shell=True)
    if not os.path.exists("/tmp/gxopus500/gxemul"): return False
    return os.path.getmtime("/tmp/gxopus500/gxemul") >= os.path.getmtime(SRC)
for name in sys.argv[1:]:
    open("/tmp/gxopus500/.MUTANT", "w").write("dev_sgi_re.c " + name + NL)
    apply(name)
    if not build():
        print("=== %s BUILD FAIL" % name); print(open("/tmp/mb2.log").read()[-1500:]); continue
    out = subprocess.run(["python3", "-u", "/tmp/probe500b.py", "/tmp/gxopus500/gxemul", name],
                         capture_output=True, text=True, timeout=1800).stdout
    open("/tmp/b_" + name + ".txt", "w").write(out)
    res = [l for l in out.splitlines() if "OPUS500_RESULT" in l]
    fails = [l for l in out.splitlines() if "RED" in l or l.rstrip().endswith("FAIL")]
    print("=== %-14s %s" % (name, " ".join(res)))
    for f in fails[:8]: print("      " + f.strip())
    sys.stdout.flush()
shutil.copy(BASE, SRC); os.remove("/tmp/gxopus500/.MUTANT"); print("RESTORED")
