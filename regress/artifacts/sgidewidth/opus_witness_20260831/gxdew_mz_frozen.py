#!/usr/bin/env python3
"""
DOES #95 PRE-ZERO THE DEVICE-READ BUFFER BEFORE THE HANDLER RUNS?

Attribution control, not an argument.  Two builds differing in ONE byte of
memory_rw.c: the #95 fill value, 0x00 vs 0xa5.  Both carry the same
early-`return 1' decline in DEVICE_ACCESS(sgi_de) (variant mB), so the handler
NEVER writes the caller's buffer.  Whatever the guest reads therefore came from
memory_rw.c, and the fill value says so by name.
"""
import os, sys, subprocess, shutil, time
D="/tmp/gxopusdew"
SGI=D+"/src/devices/dev_sgi_re.c"; MRW=D+"/src/cpus/memory_rw.c"
SECS="/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/devices/dev_sgi_re.c"
SECM="/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/cpus/memory_rw.c"
sys.path.insert(0,"/tmp"); 
import importlib.util
spec=importlib.util.spec_from_file_location("mut","/tmp/gxdew_mutate2_frozen.py")
mut=importlib.util.module_from_spec(spec)
src=open("/tmp/gxdew_mutate2_frozen.py").read().split("if __name__")[0]
ns={}; exec(src, ns)

OLD95 = ns["__builtins__"] and None
ANCHOR = "#95: zero the caller's buffer up front"

def build(tag, mrw_patch):
    open(D+"/.MUTANT","w").write("mz variant=%s\n"%tag)
    txt = open(ns["ORIG"]).read()
    enum, arm = ns["VARIANTS"]["mB"]
    txt = txt.replace(ns["ENUM_OLD"], enum).replace(ns["KILL"], arm)
    open(SGI,"w").write(txt)
    m = open(SECM).read()
    if mrw_patch:
        a = m.index(ANCHOR)                     # the #95 site, by its own comment
        k = m.index("memset(data, 0, len);", a)
        assert m.count("memset(data, 0xa5", 0) == 0
        m = m[:k] + "memset(data, 0xa5, len);" + m[k+len("memset(data, 0, len);"):]
        assert m.count("memset(data, 0xa5, len);") == 1
    open(MRW,"w").write(m)
    subprocess.call("cd %s && rm -f src/cpus/*.o && make -j8 > /tmp/gxdew_build_%s.log 2>&1"%(D,tag), shell=True)
    fresh = os.path.getmtime(D+"/gxemul") > os.path.getmtime(MRW)
    print("build %-4s fresh=%s" % (tag, fresh), flush=True)
    assert fresh
    shutil.copy(D+"/gxemul", "/tmp/gxdew_bin_"+tag)
    os.remove(D+"/.MUTANT")

if __name__ == "__main__":
    build("z0", False)     # #95 fills 0x00   (== stock)
    build("za", True)      # #95 fills 0xa5
    shutil.copy(SECS, SGI); shutil.copy(SECM, MRW)
    subprocess.call("cd %s && rm -f src/cpus/*.o && make -j8 > /tmp/gxdew_build_zrestore.log 2>&1"%D, shell=True)
    r1=subprocess.call(["cmp","-s",SGI,SECS]); r2=subprocess.call(["cmp","-s",MRW,SECM])
    print("RESTORE dev_sgi_re=%s memory_rw=%s binary-newer=%s" %
          ("CLEAN" if r1==0 else "DIRTY", "CLEAN" if r2==0 else "DIRTY",
           os.path.getmtime(D+"/gxemul") > os.path.getmtime(MRW)))
    print("MZ_BUILD_DONE")
