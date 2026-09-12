#!/bin/bash
OUT=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/sgirandomcolour/pass2_20260911
python3 - "$OUT" <<'PY'
import os, re, sys
OUT = sys.argv[1]
print("=== PASS-2 SUMMARY: instrument score vs CONTROL score, per mutant ===")
print("%-24s %-9s %-9s %s" % ("mutant", "59-row", "control", "what the control saw at the three off-instrument cells"))
legs = []
for f in sorted(os.listdir(OUT)):
    if f.endswith(".raw"):
        legs.append(f[:-4])
order = ["BASE", "BASE_B", "M28r_permit_othernib", "M30_tilenrdecline", "M31_tilenrguard",
         "M32_tilenrxdecline", "M33_tiledorigin", "M34_ofsguard", "M35_xguard",
         "M36_yguard", "M37_fgvalue"]
legs = [l for l in order if l in legs] + [l for l in legs if l not in order]
for nm in legs:
    raw = os.path.join(OUT, nm + ".raw"); ctl = os.path.join(OUT, nm + ".ctrl")
    s = c = "-"; vals = ""
    if os.path.exists(raw):
        t = open(raw, errors="replace").read()
        m = re.search(r"SGICOLOUR_RESULT=(\d+/\d+)", t); s = m.group(1) if m else "NO SENTINEL"
    if os.path.exists(ctl):
        t = open(ctl, errors="replace").read()
        m = re.search(r"SGICTRL_RESULT=(\d+/\d+)", t); c = m.group(1) if m else "NO SENTINEL"
        m = re.search(r"CTRL_T1YCRCB=(\S+) CTRL_TY1YCRCB=(\S+) CTRL_NIB60=(\S+)", t)
        if m:
            lab = []
            for k, v in zip(("t1", "ty1", "nib60"), m.groups()):
                lab.append("%s=%s%s" % (k, v, "" if v == "0x11223344" else " <-WROTE"))
            vals = "  ".join(lab)
    print("%-24s %-9s %-9s %s" % (nm, s, c, vals))
print()
print("=== ESCAPES: 59/59 on the instrument AND a control cell written ===")
for nm in legs:
    if nm.startswith("BASE"):
        continue
    raw = os.path.join(OUT, nm + ".raw"); ctl = os.path.join(OUT, nm + ".ctrl")
    if not (os.path.exists(raw) and os.path.exists(ctl)):
        continue
    t = open(raw, errors="replace").read(); u = open(ctl, errors="replace").read()
    m = re.search(r"SGICOLOUR_RESULT=(\d+)/(\d+)", t)
    if not m:
        continue
    full = m.group(1) == m.group(2)
    wrote = re.search(r"CTRL_T1YCRCB=(\S+) CTRL_TY1YCRCB=(\S+) CTRL_NIB60=(\S+)", u)
    if wrote:
        bad = [k for k, v in zip(("t1", "ty1", "nib60"), wrote.groups()) if v != "0x11223344"]
    else:
        bad = []
    if full and bad:
        print("   *** %-24s TOTAL ESCAPE of the 59-row instrument; guest memory written at: %s"
              % (nm, ", ".join(bad)))
    elif full:
        print("       %-24s 59/59 but no control cell written (EQUIVALENT / unreachable?)" % nm)
    elif bad:
        print("       %-24s killed by the instrument (%s), and also wrote at: %s"
              % (nm, m.group(0).split("=")[1], ", ".join(bad)))
PY
