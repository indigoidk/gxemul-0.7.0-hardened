import os, re
roots = [r"C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC", r"C:\DocumentNoSnc\cc\GXEMUL\_scratchpad"]
ESC = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
n = blocks = coloured = coloured_answered = launcher_coloured = 0; ex = []
for root in roots:
    for dp, dn, fn in os.walk(root):
        if os.sep + ".git" in dp or dp.endswith(".git"): continue
        for f in fn:
            if not (f.endswith(".err") and "codex" in f.lower()): continue
            p = os.path.join(dp, f)
            try: raw = open(p, "rb").read()
            except OSError: continue
            n += 1
            rawlines = raw.decode("utf-8", "replace").split("\n")[:45]
            lines = [ESC.sub("", l) for l in rawlines]
            h = 0; blk = []
            for i, l in enumerate(lines):
                if i + 1 > 12 and h < 2: break
                if h == 0 and l.startswith("OpenAI Codex"): h = 1; continue
                if h == 1 and l.startswith("--------"): h = 2; continue
                if h == 2 and l.startswith("--------"): break
                if h == 2: blk.append(i)
            if h != 2: continue
            blocks += 1
            if any("\x1b" in rawlines[i] for i in blk):
                coloured += 1
                t = p[:-4] + ".txt"
                if os.path.exists(t) and os.path.getsize(t) > 0: coloured_answered += 1; ex.append(p)
print("codex .err files %d | opening blocks %d | blocks with ANSI inside the block %d | of those with a NON-EMPTY sibling .txt (an answered, rc-0-shaped run) %d" % (n, blocks, coloured, coloured_answered))
for q in ex[:8]: print("  coloured header, answered:", q)
print("COLHDR_DONE")
