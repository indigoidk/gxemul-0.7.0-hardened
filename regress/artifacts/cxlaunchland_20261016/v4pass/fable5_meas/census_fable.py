import os, re, sys, collections
roots = [r"C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC", r"C:\DocumentNoSnc\cc\GXEMUL\_scratchpad"]
ESC = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
ALTS = [("refusal", "flagged for possible cybersecurity"), ("refusal", "cannot help with"), ("refusal", "can.t help with"),
        ("refusal", "I won.t help"), ("wall", "usage limit"), ("wall", "quota"), ("wall", "rate limit"), ("wall", "not authenticated")]
ALTRE = [(k, a, re.compile(a, re.I)) for k, a in ALTS]
n_err = 0; lines_all = collections.Counter(); files_all = collections.Counter(); lines_cls = collections.Counter(); files_cls = collections.Counter()
errlines_total = errlines_cls = n_cls = 0
banner_at = collections.Counter(); model_at = collections.Counter(); blocks = 0
model_trailing = 0; model_cr = 0; prefixed_banner_before = 0; prefixed_files = []
upper_variants = collections.Counter()
for root in roots:
    for dp, dn, fn in os.walk(root):
        if os.sep + ".git" in dp or dp.endswith(".git"):
            continue
        for f in fn:
            if not (f.endswith(".err") and "codex" in f.lower()):
                continue
            p = os.path.join(dp, f)
            try:
                raw = open(p, "rb").read()
            except OSError:
                continue
            n_err += 1
            text = ESC.sub("", raw.decode("utf-8", "replace"))
            lines = text.split("\n")
            errl = [l for l in lines if l.startswith("ERROR:")]
            errlines_total += len(errl)
            t = p[:-4] + ".txt"
            cls = (not os.path.exists(t)) or os.path.getsize(t) == 0
            if cls:
                n_cls += 1; errlines_cls += len(errl)
            for k, a, r in ALTRE:
                c = sum(1 for l in errl if r.search(l))
                if c:
                    lines_all[a] += c; files_all[a] += 1
                    if cls:
                        lines_cls[a] += c; files_cls[a] += 1
                    # case: does the alternative occur with any upper-case letter (i.e. would -c miss it)?
                    for l in errl:
                        m = r.search(l)
                        if m and m.group(0) != m.group(0).lower():
                            upper_variants[a] += 1
            # opening block by the landed rule
            h = 0; bl = ml = None; saw_prefixed = False
            for i, l in enumerate(lines, 1):
                if i > 12 and h < 2:
                    break
                if h == 0 and "OpenAI Codex" in l and not l.startswith("OpenAI Codex"):
                    saw_prefixed = True
                if h == 0 and l.startswith("OpenAI Codex"):
                    h = 1; bl = i; continue
                if h == 1 and l.startswith("--------"):
                    h = 2; continue
                if h == 2 and l.startswith("--------"):
                    break
                if h == 2 and l.startswith("model:") and ml is None:
                    ml = i
                    if l != l.rstrip():
                        model_trailing += 1
                    if l.endswith("\r"):
                        model_cr += 1
            if h == 2:
                blocks += 1; banner_at[bl] += 1; model_at[ml] += 1
                if saw_prefixed:
                    prefixed_banner_before += 1; prefixed_files.append(p)
print("roots:", " ".join(roots))
print("codex .err files read: %d | column-0 ERROR: lines in them: %d | classification population (sibling .txt empty/absent): %d files, %d ERROR: lines" % (n_err, errlines_total, n_cls, errlines_cls))
print("per ALTERNATIVE of the launcher's refusal/wall patterns -- column-0 ERROR: lines matching (ANSI-stripped, case-insensitive):")
print("  %-40s %10s %10s | %12s %12s | %s" % ("alternative", "lines/all", "files/all", "lines/cls", "files/cls", "upper-case variants (would escape grep -c)"))
for k, a in ALTS:
    print("  %-40s %10d %10d | %12d %12d | %d" % (k + ": " + a, lines_all[a], files_all[a], lines_cls[a], files_cls[a], upper_variants[a]))
print("opening blocks by the landed rule: %d of %d" % (blocks, n_err))
print("  banner line histogram: %s" % dict(sorted(banner_at.items(), key=lambda kv: (kv[0] is None, kv[0]))))
print("  model line histogram:  %s" % dict(sorted(model_at.items(), key=lambda kv: (kv[0] is None, kv[0]))))
print("  opening-block model: lines with trailing whitespace: %d | ending in CR: %d (of %d blocks)" % (model_trailing, model_cr, blocks))
print("  files whose first 12 lines carry a NON-column-0 'OpenAI Codex' BEFORE the column-0 banner: %d" % prefixed_banner_before)
for q in prefixed_files[:10]:
    print("    prefixed-before:", q)
# launch-log census: lines like `codex rc=N   stdout=M b`
RC = re.compile(r"codex rc=(\d+)\s+stdout=(\d+) b")
cells = collections.Counter(); nlog = 0; rows = 0
for root in roots:
    for dp, dn, fn in os.walk(root):
        if os.sep + ".git" in dp or dp.endswith(".git"):
            continue
        for f in fn:
            if not f.endswith(".log"):
                continue
            p = os.path.join(dp, f)
            try:
                raw = open(p, "rb").read()
            except OSError:
                continue
            ms = RC.findall(raw.decode("utf-8", "replace"))
            if ms:
                nlog += 1
            for rc, so in ms:
                rows += 1
                cells[(int(rc) if int(rc) in (0, 1) else "other", "stdout>0" if int(so) > 0 else "stdout=0")] += 1
print("launch-log census (.log files carrying `codex rc=N stdout=M b' lines): %d files, %d launcher rows" % (nlog, rows))
for k, v in sorted(cells.items(), key=lambda kv: str(kv[0])):
    print("  rc=%s %s: %d" % (k[0], k[1], v))
print("CENSUS_FABLE_DONE")
