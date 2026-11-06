#!/usr/bin/env python3
"""fmt_bootblock_probe.py <gxemul> [label] -- the format round's one OUTPUT row (fmtattr; GPT-6 Astra's pass 2b).

The printf-format attributes make a TYPE mismatch a compiler warning, which gate 1 refuses.  They cannot see a type-compatible
wrong value or radix: `PRIx64` -> `PRIu64`, or `(uint64_t)(uint32_t)x`.  This row pins one representative wide-hex repair.

bootblock.c's SGI path prints `Loading voldir entry "sash", 0x200 bytes from disk offset 0x...` BEFORE it reads the loader, so
a one-sector image whose voldir names `sash` at block 0x00800000 (512 bytes) gives offset 0x100000000 without a large backing
file.  Before the fix the offset was printed with %x and showed the low 32 bits (0x0); the radix mutant shows 0x4294967296.
The later, unchanged read-failure warning ALSO prints the right offset, so the row matches the LOADING line only.

Machine: unmodified `-E sgi -e ip32 -M 64`, no kernel file, so emul.c calls load_bootblock().  Controls: the session ended by
itself, and bootblock.c parsed the image (its voldir line `name: sash (512 bytes, block 8388608) [FOUND OSLoader]`).
Final lines: FMTBB_RESULT=<ok>/<n>, FMTBB_CONTROL=OK|FAIL, FMTBB_DONE."""
import os
import re
import struct
import subprocess
import sys
import tempfile

if len(sys.argv) < 2:
    sys.exit("usage: fmt_bootblock_probe.py <gxemul> [label]")
BIN = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "run"
BLOCK, BYTES = 0x00800000, 512
WANT = 'Loading voldir entry "sash", 0x200 bytes from disk offset 0x100000000'

blk = bytearray(512)                                   # struct sgi_boot_block, packed, big-endian (bootblock.h)
struct.pack_into(">I", blk, 0, 0x0be5a941)             # magic
struct.pack_into(">8sii", blk, 72, b"sash", BLOCK, BYTES)   # voldir[0]: name, block, bytes (voldir starts at offset 72)

rows, controls = [], []


def row(name, got, want, control=False):
    ok = got == want
    rows.append(ok)
    if control:
        controls.append(ok)
    print("%-16s %-74s want %-74s %s" % (name, str(got)[:74], str(want)[:74], "ok" if ok else "FAIL"))


with tempfile.TemporaryDirectory(prefix="gxfmtbb_") as d:
    img = os.path.join(d, "sgi_boot.img")
    open(img, "wb").write(bytes(blk))
    argv = [BIN, "-E", "sgi", "-e", "ip32", "-M", "64", "-d", img]
    try:
        p = subprocess.run(argv, input=b"quit\n", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60)
        out = p.stdout.decode("latin-1", "replace").replace("\r", "")
        how = "exit%d" % p.returncode if p.returncode >= 0 else "sig%d" % -p.returncode
    except subprocess.TimeoutExpired as e:
        out, how = (e.output or b"").decode("latin-1", "replace"), "TIMEOUT"
    except OSError as e:
        out, how = "", "NOBIN(%s)" % e.__class__.__name__

print("fmt_bootblock_probe label=%s binary=%s" % (LABEL, BIN))
row("session ended", "yes" if how not in ("TIMEOUT",) and not how.startswith("NOBIN") else how, "yes", True)
parsed = re.search(r"name: sash \(512 bytes, block 8388608\) \[FOUND OSLoader\]", out)
row("voldir parsed", "yes" if parsed else "no", "yes", True)
m = re.search(r'Loading voldir entry "sash"[^\n]*', out)
row("loading offset", m.group(0).strip() if m else "(no loading line)", WANT)
print("FMTBB_RESULT=%d/%d" % (sum(rows), len(rows)))
print("FMTBB_CONTROL=%s" % ("OK" if controls and all(controls) else "FAIL"))
print("FMTBB_DONE")
