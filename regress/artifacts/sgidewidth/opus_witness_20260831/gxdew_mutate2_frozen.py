#!/usr/bin/env python3
"""Build sgidewidth candidate variants in /tmp/gxopusdew.  Never touches GXEMUL-SEC."""
import sys, os, subprocess, shutil, time
D    = "/tmp/gxopusdew"
SRC  = D + "/src/devices/dev_sgi_re.c"
ORIG = "/tmp/gxdew_dev_sgi_re.c.PRISTINE"
SEC  = "/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/devices/dev_sgi_re.c"

KILL = (
	"\t} else {\n"
	"\t\tfatal(\"sgi_de: len = %i not implemented\\n\", len);\n"
	"\t\texit(1);\n"
	"\t}\n")

ENUM_OLD = "\tSGIRE_W_LINB_LEN  = 1 << 5,\n};"
ENUM_NEW = "\tSGIRE_W_LINB_LEN  = 1 << 5,\n\tSGIRE_W_DE_LEN    = 1 << 6,\n};"

LATCH = (
	"\t} else {\n"
	"\t\t/*\n"
	"\t\t *  #TBD: an unserviceable width used to end the host process.\n"
	"\t\t *  Decline it, announce once per device instance.\n"
	"\t\t */\n"
	"\t\tif (!(d->warned & SGIRE_W_DE_LEN)) {\n"
	"\t\t\td->warned |= SGIRE_W_DE_LEN;\n"
	"\t\t\tfatal(\"[ sgi_de: unimplemented len=%i -- declined.  (once) ]\\n\", (int) len);\n"
	"\t\t}\n"
	"@@EXTRA@@"
	"\t}\n")

def L(extra):
    return LATCH.replace("@@EXTRA@@", extra)

START0 = "\t\tstartFlag = 0;\n"
RET1   = "\t\treturn 1;\n"

MASK_OLD = "\trelative_addr += 0x2000;\n"
MASK_NEW = "\trelative_addr += 0x2000;\n\tstartFlag = 0;\n"

VARIANTS = {
  "fix": (ENUM_NEW, L(START0)),
  "mA":  (ENUM_NEW, L("")),
  "mB":  (ENUM_NEW, L(RET1)),
  "mC":  (ENUM_NEW, L(START0).replace("SGIRE_W_DE_LEN","SGIRE_W_TLBA_LEN")),
  #  mD: brace slip -- the repair lands at the end of the len==4 ACCEPT arm
  "mD":  (ENUM_NEW, L("").replace("\t} else {", "\tstartFlag = 0;\n\t} else {", 1)),
  #  mE: clause-(d) -- keep the guard, WIDEN the repair to every access
  "mE":  ((ENUM_NEW, MASK_OLD, MASK_NEW), L("")),
  #  mF: clause-(d) -- qualify the repair with a predicate it need not have
  "mF":  (ENUM_NEW, L("\t\tif (writeflag == MEM_WRITE)\n\t\t\tstartFlag = 0;\n")),
}

def build(name):
    open(D + "/.MUTANT", "w").write("dev_sgi_re.c variant=%s\n" % name)
    txt = open(ORIG).read()
    enum, arm = VARIANTS[name]
    assert txt.count(ENUM_OLD) == 1, "enum anchor"
    assert txt.count(KILL) == 1, "kill anchor"
    if isinstance(enum, tuple):
        e0, mo, mn = enum
        assert txt.count(mo) == 1, 'mask anchor'
        txt = txt.replace(mo, mn)
        enum = e0
    txt = txt.replace(ENUM_OLD, enum).replace(KILL, arm)
    open(SRC, "w").write(txt)
    t0 = time.time()
    rc = subprocess.call("cd %s && make -j8 > /tmp/gxdew_build_%s.log 2>&1" % (D, name),
                         shell=True)
    out = "/tmp/gxdew_bin_%s" % name
    fresh = os.path.exists(D+"/gxemul") and os.path.getmtime(D+"/gxemul") > os.path.getmtime(SRC)
    print("build %-4s rc=%d fresh=%s %.0fs" % (name, rc, fresh, time.time()-t0), flush=True)
    if rc != 0 or not fresh:
        print(open("/tmp/gxdew_build_%s.log" % name).read()[-2500:]); sys.exit(3)
    shutil.copy(D + "/gxemul", out)
    os.remove(D + "/.MUTANT")
    return out

if __name__ == "__main__":
    if not os.path.exists(ORIG):
        shutil.copy(SEC, ORIG)
    #  prove the pristine copy IS the repo's file
    rc = subprocess.call(["cmp", "-s", ORIG, SEC])
    print("PRISTINE cmp vs GXEMUL-SEC: %s" % ("CLEAN" if rc == 0 else "DIVERGED"))
    assert rc == 0
    if not os.path.exists("/tmp/gxdew_bin_base"):
        shutil.copy(ORIG, SRC)
        subprocess.call("cd %s && make -j8 > /tmp/gxdew_build_base.log 2>&1" % D, shell=True)
        shutil.copy(D + "/gxemul", "/tmp/gxdew_bin_base")
        print("build base ok")
    for v in sys.argv[1:] or list(VARIANTS):
        build(v)
    #  RESTORE + rebuild, verified against GXEMUL-SEC (never against our own backup)
    shutil.copy(SEC, SRC)
    subprocess.call("cd %s && make -j8 > /tmp/gxdew_build_restore.log 2>&1" % D, shell=True)
    rc = subprocess.call(["cmp", "-s", SRC, SEC])
    fresh = os.path.getmtime(D+"/gxemul") > os.path.getmtime(SRC)
    print("RESTORE cmp-vs-SEC=%s  binary-newer=%s" % ("CLEAN" if rc==0 else "DIVERGED", fresh))
    if os.path.exists(D + "/.MUTANT"): os.remove(D + "/.MUTANT")
    print("MUTATE_DONE")
