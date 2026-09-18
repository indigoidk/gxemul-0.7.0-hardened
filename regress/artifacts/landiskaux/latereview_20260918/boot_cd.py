#!/usr/bin/env python3
"""boot_cd.py <tree> <out> -- boot_cmp.py's CD-ROM twin: the same scratch image
attached as an IDE CD-ROM (`icR:`), stop at the installer prompt, print the
guest's wdc0 attach block with the emulator's own warnings stripped."""
import collections, os, re, select, subprocess, sys, time

T, OUT = sys.argv[1], sys.argv[2]
BIN = "/tmp/gxopus_lax_%s/gxemul" % T
IMG = "/mnt/c/DocumentNoSnc/CC/GXEMUL/_images"
argv = [BIN, "-E", "landisk", "-M", "64", "-d", "icR:%s/wdc-scratch-64m.img" % IMG,
        "%s/openbsd76-landisk-bsd.rd" % IMG]
DEADLINE = 120.0
t0 = time.time()
p = subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT)
buf = bytearray()
prompt = False
while time.time() - t0 < DEADLINE:
    r, _, _ = select.select([p.stdout], [], [], 0.5)
    if r:
        d = os.read(p.stdout.fileno(), 1 << 16)
        if not d:
            break
        buf += d
        if b"(I)nstall, (U)pgrade" in buf:
            prompt = True
            time.sleep(1.0)
            break
elapsed = time.time() - t0
p.kill()
try:
    rest = p.communicate(timeout=5)[0]
    if rest:
        buf += rest
except Exception:
    pass
open(OUT, "wb").write(bytes(buf))
txt = bytes(buf).decode("latin-1")
WARN = re.compile(r"\[ memory (?:READ|WRITE): [^\]]*\]\r?\n?")
clean = WARN.sub("", txt)
print("TREE=%s CDROM BYTES=%d ELAPSED=%.1fs PROMPT_REACHED=%s" % (T, len(buf), elapsed, prompt))
print("BANNER_CDROM=%d" % len(re.findall(r"IDE CD-?ROM", txt)))
print("WD0=%d ATAPISCSI=%d CD0=%d" % (clean.count("wd0 at wdc0"),
      clean.count("atapiscsi0 at wdc0"), clean.count("cd0 at")))
nx = collections.Counter(re.findall(r"non-existant paddr=(0x[0-9a-f]+)", txt))
print("NONEX_2C=%d NONEX_TOTAL=%d" % (nx.get("0x1400002c", 0), sum(nx.values())))
m = re.search(r"wdc0 at obio0.*?(?:root on|\(I\)nstall)", clean, re.S)
print("ATTACH_BLOCK<<<")
print(m.group(0) if m else "NOT FOUND")
print(">>>")
print("BOOT_CD_DONE")
