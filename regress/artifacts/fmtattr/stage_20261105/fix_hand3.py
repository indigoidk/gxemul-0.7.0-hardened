#!/usr/bin/env python3
"""fix_hand3.py -- the seven repairs GPT-6 Astra's pass 2 found in the staged format fixes (p2_astra/codex_fmtp2.txt), each an
exact anchor asserted once in the STAGED file.  Run after apply_fmt.py, fix_hand.py and fix_hand2.py.
  cpu_ppc.c   the PPC601 line: supply x (the cpu id exists there) instead of dropping `cpu%i`
  cpu_arm.c   two size_t expressions: %zu, not PRIi64
  dev_bt455.c, dev_dc7085.c x2, dev_le.c: idata is logged BEFORE any masking (debugger `put d` can store 0x100000001), so print
              it full width -- PRIx64 for the three hex logs (their minimum widths kept), PRIu64 for LE's decimal one."""
import io

ST = "C:/DocumentNoSnc/cc/GXEMUL/_scratchpad/codescan/fmtfix/stage/"
BS = chr(92)
N, T = BS + "n", BS + "t"
E = [
    ("src/cpus/cpu_ppc.c", 'debug("cpu:  PPC601-style, TODO!' + N + '");', 'debug("cpu%i:  PPC601-style, TODO!' + N + '", x);'),
    ("src/cpus/cpu_arm.c", 'debug("%s%s' + T + 'r%i,[r%i,#%" PRIi64 "]' + N + '",', 'debug("%s%s' + T + 'r%i,[r%i,#%zu]' + N + '",'),
    ("src/cpus/cpu_arm.c", 'debug("%sh' + T + 'r%i,[r%i,#%" PRIi64 "]' + N + '",', 'debug("%sh' + T + 'r%i,[r%i,#%zu]' + N + '",'),
    ("src/devices/dev_bt455.c", '\t\t\tdebug("[ bt455: write to addr_cmap, 0x%02x ]' + N + '", (int)idata);',
     '\t\t\tdebug("[ bt455: write to addr_cmap, 0x%02" PRIx64\n\t\t\t    " ]' + N + '", (uint64_t)idata);'),
    ("src/devices/dev_dc7085.c", '\t\t\tdebug("[ dc7085 write to CSR: 0x%04x ]' + N + '", (int)idata);',
     '\t\t\tdebug("[ dc7085 write to CSR: 0x%04" PRIx64 " ]' + N + '",\n\t\t\t    (uint64_t)idata);'),
    ("src/devices/dev_dc7085.c", '\t\t\tdebug("[ dc7085 write to LPR: 0x%04x ]' + N + '", (int)idata);',
     '\t\t\tdebug("[ dc7085 write to LPR: 0x%04" PRIx64 " ]' + N + '",\n\t\t\t    (uint64_t)idata);'),
    ("src/devices/dev_le.c", '\t\t\t\t    "WARNING! register %i (max is %i)",\n\t\t\t\t    (int)idata, N_REGISTERS - 1);',
     '\t\t\t\t    "WARNING! register %" PRIu64\n\t\t\t\t    " (max is %i)", (uint64_t)idata,\n\t\t\t\t    N_REGISTERS - 1);'),
]
for f, old, new in E:
    p = ST + f
    t = io.open(p, encoding="latin-1", newline="").read()
    if t.count(old) == 0 and t.count(new) == 1:
        continue                                     # already applied (the script is re-runnable)
    assert t.count(old) == 1, (f, old, t.count(old))
    t = t.replace(old, new)
    wide = [l for l in new.split("\n") if len(l.expandtabs(8)) > 79]
    assert not wide, (f, wide)
    io.open(p, "w", encoding="latin-1", newline="").write(t)
print("pass-2 repairs: %d edits" % len(E))
