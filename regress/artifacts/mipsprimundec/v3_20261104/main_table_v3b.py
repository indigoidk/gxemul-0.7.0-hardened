#!/usr/bin/env python3
"""main_table.py <gxemul> <label> [workdir] -- the per-word exception table for mipsprimundec, measured by the main loop (2026-11-04)
after the m_mpu seat stopped on a classifier refusal.  For each of the eight words and each CPU (-C R4400, -C R3000, the default testmips
5KE), one cold `-E testmips` session: `put w` the word at PLANT, PC = PLANT, `step 1`, `reg`, `reg ,0`.  Prints ExcCode/CE, BD, EPC, PC and
whether the CPU stopped.  Then a delay-slot case on the R4400: `beq zero,zero,1` at PLANT, the word at PLANT+4.  Prints TABLE_DONE."""
import os
import re
import subprocess
import sys
import tempfile

BIN, LABEL = sys.argv[1], sys.argv[2]
WORK = sys.argv[3] if len(sys.argv) > 3 else None
d = tempfile.mkdtemp(prefix="mputab_")
DUMMY = os.path.join(d, "z.bin")
open(DUMMY, "wb").write(bytes(4))
PLANT = 0xffffffff80020000
CPUS = [("R4400", ["-C", "R4400"]), ("R3000", ["-C", "R3000"]), ("5KE", []), ("24KEc", ["-C", "24KEc"]), ("R5000", ["-C", "R5000"])]   # v3b: + 24KEc (MIPS32, MODE32) and R5000 (ISA IV, the `> 4` catch GLM named)
WORDS = [("jalx", 0x74000000), ("mdmx", 0x78000000), ("lwc2", 0xc8000000), ("lwc3", 0xcc000000),
         ("ldc2", 0xd8000000), ("swc2", 0xe8000000), ("swc3", 0xec000000), ("sdc2", 0xf8000000)]
CAUSE = re.compile(r"cause:\s+(\S+) \(exccode (\d+)\)( bd)? ce=(\d+)")   # ` bd` sits between the exccode and ce= (cpu_mips.c)


def run(tag, extra, words):
    cmds = []
    for i, w in enumerate(words):
        cmds.append("put w 0x%x, 0x%08x" % (PLANT + 4 * i, w))
    cmds += ["pc=0x%x" % PLANT, "step 1", "reg", "reg ,0", "quit"]
    argv = [BIN, "-V", "-x", "-E", "testmips"] + extra + ["0x%x:%s" % (PLANT, DUMMY)]
    p = subprocess.run(argv, input=("\n".join(cmds) + "\n").encode(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60)
    t = p.stdout.decode("latin-1", "replace").replace("\r", "")
    if WORK:
        os.makedirs(WORK, exist_ok=True)
        open(os.path.join(WORK, "%s_%s.txt" % (LABEL, tag)), "w", encoding="latin-1").write("$ " + " ".join(argv) + "\n" + t)
    i, j = t.rfind("GXemul> reg\n"), t.rfind("GXemul> reg ,0")
    pc = re.search(r"\bpc\s*=\s*(?:0x)?([0-9a-fA-F]+)", t[i:j]) if 0 <= i < j else None
    epc = re.search(r"\bepc\s*=\s*(?:0x)?([0-9a-fA-F]+)", t[j:]) if j >= 0 else None
    c = CAUSE.search(t[j:]) if j >= 0 else None
    mnem = re.search(r"\n[0-9a-f]+: [0-9a-f]{8}\s+(.*)", t[t.find("GXemul> step 1"):]) if "GXemul> step 1" in t else None
    return dict(exit=p.returncode, pc=pc.group(1) if pc else "none", epc=epc.group(1) if epc else "none",
                exc=("%s/%s/ce=%s%s" % (c.group(1), c.group(2), c.group(4), "/BD" if c.group(3) else "")) if c else "none",
                stopped="STOP" if "UNIMPLEMENTED instruction" in t else "-",
                mnem=(mnem.group(1).strip()[:34] if mnem else "?"))


print("label=%s binary=%s" % (LABEL, BIN))
print("%-6s %-5s %-34s %-22s %-18s %-18s %s" % ("cpu", "word", "disassembly", "cause/exccode/ce", "epc", "pc", "stop"))
for cname, extra in CPUS:
    for wname, w in WORDS:
        r = run("%s_%s" % (cname, wname), extra, [w])
        print("%-6s %-5s %-34s %-22s %-18s %-18s %s" % (cname, wname, r["mnem"], r["exc"], r["epc"], r["pc"], r["stopped"]))
r = run("R4400_delayslot_jalx", ["-C", "R4400"], [0x10000001, 0x74000000])          # beq zero,zero,+1 ; then the word in its slot
print("%-6s %-5s %-34s %-22s %-18s %-18s %s" % ("R4400", "DS:jx", r["mnem"], r["exc"], r["epc"], r["pc"], r["stopped"]))
print("TABLE_DONE")
