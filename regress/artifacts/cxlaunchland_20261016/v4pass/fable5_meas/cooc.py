import os, re
roots = [r"C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC", r"C:\DocumentNoSnc\cc\GXEMUL\_scratchpad"]
ESC = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
REF = re.compile(r"flagged for possible cybersecurity|cannot help with|can.t help with|I won.t help", re.I)
WAL = re.compile(r"usage limit|quota|rate limit|not authenticated", re.I)
n = cls = both_all = both_cls = rc0_quote_both = 0; ex = []
for root in roots:
    for dp, dn, fn in os.walk(root):
        if os.sep + ".git" in dp or dp.endswith(".git"): continue
        for f in fn:
            if not (f.endswith(".err") and "codex" in f.lower()): continue
            p = os.path.join(dp, f)
            try: raw = open(p, "rb").read()
            except OSError: continue
            n += 1
            errl = [l for l in ESC.sub("", raw.decode("utf-8", "replace")).split("\n") if l.startswith("ERROR:")]
            b = any(REF.search(l) for l in errl) and any(WAL.search(l) for l in errl)
            t = p[:-4] + ".txt"; c = (not os.path.exists(t)) or os.path.getsize(t) == 0
            cls += c; both_all += b; both_cls += (b and c)
            if b and not c: ex.append(p)
print("files %d | classification population %d | BOTH refusal+wall column-0 ERROR lines: all %d, in the classification population %d" % (n, cls, both_all, both_cls))
for q in ex[:6]: print("  both, but answered (rc-0 shape, never classified):", q)
print("COOC_DONE")
