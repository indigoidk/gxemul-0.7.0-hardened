import json, io, re, sys
# REVERSE RECONCILIATION, extraction half (mechanical): ledger entries dated in [LO, HI] whose note CLAIMS that a
# change was applied / corrected in place / is in the working tree, and that name at least one source-like file.
# Output: one numbered claim per entry, with the matched sentence(s) and the files named -- the DENOMINATOR a
# reviewing seat checks against the tree.  Nothing here judges whether the claim is true.
path, LO, HI, out = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
CLAIM = re.compile(r"(FOUR APPLIED|THREE APPLIED|TWO APPLIED|\bAPPLIED\b|\bapplied (?:in|to|here|this)\b|corrected in place|CORRECTED IN PLACE|"
                   r"in the working[- ]tree(?: diff)?|working-tree diff|now reads\b|now says\b|past-tensed|Past-tensed|"
                   r"repaired in (?:the )?tree|is now in the tree|landed in the working tree|was re-pinned|re-pinned)", re.I)
FILE = re.compile(r"\b[\w./-]+\.(?:c|h|py|sh|md|json)\b")
L = json.load(io.open(path, encoding='utf-8'))
n = 0
w = io.open(out, 'w', encoding='utf-8', newline='\n')
for r in L['rows']:
    for i, e in enumerate(r.get('entries') or []):
        d = e.get('date') or ''
        if not (LO <= d <= HI):
            continue
        t = e.get('note') or ''
        ms = list(CLAIM.finditer(t))
        files = sorted(set(f for f in FILE.findall(t) if not f.startswith(('http', 'www'))))
        if not ms:
            continue
        n += 1
        w.write('=' * 110 + '\n')
        w.write('CLAIM %03d  row=%s  entry=[%d]  date=%s  phase=%s  seat=%s  row-state=%s\n' % (
            n, r['id'], i, d, e.get('phase', ''), e.get('seat', ''), r.get('state')))
        w.write('  files named: %s\n' % ', '.join(files[:14]))
        seen = set()
        for m in ms[:4]:
            a, b = max(0, m.start() - 300), min(len(t), m.end() + 300)
            if any(abs(a - s) < 200 for s in seen):
                continue
            seen.add(a)
            w.write('  ...%s...\n' % t[a:b].replace('\n', ' '))
w.close()
print('claims extracted: %d  (entries dated %s..%s that name a file and use an applied/in-tree verb)' % (n, LO, HI))
