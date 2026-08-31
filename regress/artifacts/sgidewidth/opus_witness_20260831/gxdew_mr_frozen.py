#!/usr/bin/env python3
"""Variant mR -- the recommended shape: latched decline, ONE common exit,
   reached by the in-tree `goto <label>` device idiom (dev_dc7085, dev_i80321,
   dev_le, dev_pvr, dev_sgi_mec).  Skips the register-name switch AND the
   draw; still answers a declined read and still `return 1'."""
import os, sys, subprocess, shutil
D="/tmp/gxopusdew"; SGI=D+"/src/devices/dev_sgi_re.c"
SEC="/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/devices/dev_sgi_re.c"
ns={}; exec(open("/tmp/gxdew_mutate2_frozen.py").read().split("if __name__")[0], ns)
BS=chr(92); T=BS+"t"; N=BS+"n"

ARM = ("\t} else {\n"
       "\t\t/*\n"
       "\t\t *  #TBD: an unserviceable width used to end the host process.\n"
       "\t\t *  Decline it, announce once per device instance, and jump to\n"
       "\t\t *  the common exit: falling through would (a) let the switch\n"
       "\t\t *  announce a TODO about a write that never happened and (b)\n"
       "\t\t *  let the tail run draw_primitive() for a DECLINED access.\n"
       "\t\t */\n"
       "\t\tif (!(d->warned & SGIRE_W_DE_LEN)) {\n"
       "\t\t\td->warned |= SGIRE_W_DE_LEN;\n"
       '\t\t\tfatal("[ sgi_de: unimplemented len=%i -- declined.'
       '  (once) ]' + BS + 'n", (int) len);\n'
       "\t\t}\n"
       "\t\tgoto de_declined;\n"
       "\t}\n")

TAIL_OLD = ("\tif (startFlag)\n\t\tdraw_primitive(cpu, d);\n\n"
            "\tif (writeflag == MEM_READ)\n"
            "\t\tmemory_writemax64(cpu, data, len, odata);\n\n\treturn 1;\n")
TAIL_NEW = ("\tif (startFlag)\n\t\tdraw_primitive(cpu, d);\n\n"
            " de_declined:\n"
            "\tif (writeflag == MEM_READ)\n"
            "\t\tmemory_writemax64(cpu, data, len, odata);\n\n\treturn 1;\n")

txt = open(ns["ORIG"]).read()
assert txt.count(ns["ENUM_OLD"])==1 and txt.count(ns["KILL"])==1
assert txt.count(TAIL_OLD)==1, "tail anchor count=%d" % txt.count(TAIL_OLD)
txt = txt.replace(ns["ENUM_OLD"], ns["ENUM_NEW"]).replace(ns["KILL"], ARM).replace(TAIL_OLD, TAIL_NEW)
open(D+"/.MUTANT","w").write("mR\n"); open(SGI,"w").write(txt)
rc=subprocess.call("cd %s && make -j8 > /tmp/gxdew_build_mR.log 2>&1"%D, shell=True)
fresh = os.path.getmtime(D+"/gxemul") > os.path.getmtime(SGI)
print("build mR rc=%d fresh=%s"%(rc,fresh))
if rc or not fresh: print(open("/tmp/gxdew_build_mR.log").read()[-2000:])
else: shutil.copy(D+"/gxemul","/tmp/gxdew_bin_mR")
shutil.copy(SEC, SGI)
subprocess.call("cd %s && make -j8 > /tmp/gxdew_build_mRrestore.log 2>&1"%D, shell=True)
print("RESTORE cmp=%s binary-newer=%s" %
      ("CLEAN" if subprocess.call(["cmp","-s",SGI,SEC])==0 else "DIRTY",
       os.path.getmtime(D+"/gxemul") > os.path.getmtime(SGI)))
os.remove(D+"/.MUTANT"); print("MR_DONE")
