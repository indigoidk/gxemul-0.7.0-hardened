#!/usr/bin/env python3
"""boot_cmp.py <tree> <verbose:0|1> <out> -- rung-4 boot census, ONE script for
pre-fix and post-fix.  Boots OpenBSD 7.6 RAMDISK on UNMODIFIED -E landisk (same
argv as regress/artifacts/landiskaux/census_20260827/run_boot.sh) and stops at
the installer prompt, then tallies.  Counts are OCCURRENCES, not lines: the
emulator's warnings interleave with the guest console mid-word."""
import collections, os, re, select, subprocess, sys, time

T, VERB, OUT = sys.argv[1], sys.argv[2] == "1", sys.argv[3]
BIN = "/tmp/gxopus_lax_%s/gxemul" % T
IMG = "/mnt/c/DocumentNoSnc/CC/GXEMUL/_images"
argv = [BIN] + (["-v"] if VERB else []) + [
    "-E", "landisk", "-M", "64", "-d", "iR:%s/wdc-scratch-64m.img" % IMG,
    "%s/openbsd76-landisk-bsd.rd" % IMG]
DEADLINE = 240.0
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
        if b"(I)nstall, (U)pgrade" in buf[-4096:] or b"(I)nstall, (U)pgrade" in buf:
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

print("TREE=%s VERBOSE=%d BIN=%s" % (T, VERB, BIN))
print("BYTES=%d ELAPSED=%.1fs PROMPT_REACHED=%s" % (len(buf), elapsed, prompt))
print("WD0_ATTACH=%d" % txt.count("wd0 at wdc0 chan"))
print("WD0_GEOMETRY=%d" % len(re.findall(r"64MB, 131 cyl, 16 head, 63 sec", txt)))
nx = collections.Counter(re.findall(r"(READ|WRITE): (?:to|from) non-existant paddr=(0x[0-9a-f]+) len=(\d+)", txt))
print("NONEXISTANT_TOTAL=%d" % sum(nx.values()))
for (d, a, l), c in sorted(nx.items(), key=lambda kv: kv[0][1]):
    print("   nonexistant %-5s %s len=%s x%d" % (d, a, l, c))
print("NONEX_2C_WRITES=%d" % nx.get(("WRITE", "0x1400002c", "1"), 0))
print("NONEX_206_ANY=%d" % sum(c for (d, a, l), c in nx.items() if a == "0x14000206"))
if VERB:
    alt = re.findall(r"wdc: write to ALT\. CTRL: (0x[0-9a-f]+)", txt)
    print("ALTCTRL_WRITES=%d SEQ=%s" % (len(alt), ",".join(alt)))
    print("ALTCTRL_HIST=%s" % dict(collections.Counter(alt)))
    print("ALTSTATUS_READS=%d" % len(re.findall(r"wdc: read from ALTSTATUS", txt)))
    print("DRIVE_ADDR_WRITES=%d" % len(re.findall(r"wdc: write to DRIVE ADDRESS", txt)))
    print("DATA_READS=%d" % len(re.findall(r"wdc: read from DATA", txt)))
print("WDC_WARNINGS=%d" % len(re.findall(r"wdc: WARNING", txt)))
print("BOOT_CMP_DONE")
