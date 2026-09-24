import json, io, sys, re
# Every ledger row (working-tree ledger, the newest record) whose entries/closure/hold say that work is
# UNCOMMITTED / in the WORKING TREE / held -- with the row state, commits, and the newest such sentence.
path = sys.argv[1]
L = json.load(io.open(path, encoding='utf-8'))
PAT = re.compile(r'(still uncommitted|uncommitted|not (yet )?committed|NOT committed|in the working tree|working-tree diff|'
                 r'working tree|held uncommitted|NOT YET COMMITTED|awaits? (the )?commit|commit (is )?held|HOLD THE COMMIT)', re.I)
w = io.open(sys.stdout.fileno(), 'w', encoding='utf-8', closefd=False)
n = 0
for r in L['rows']:
    hits = []
    for i, e in enumerate(r.get('entries') or []):
        t = ' '.join(str(e.get(k) or '') for k in ('note','text','outcome_note','verdict'))
        m = PAT.search(t)
        if m:
            s = max(0, m.start() - 220)
            hits.append((e.get('date', ''), i, e.get('phase', ''), e.get('seat', ''), t[s:m.end() + 260].replace('\n', ' ')))
    for k in ('hold',):
        v = r.get(k)
        if v and PAT.search(str(v)):
            hits.append(('', -1, k, '', str(v)[:500]))
    if not hits:
        continue
    n += 1
    hits.sort()
    d, i, ph, seat, snip = hits[-1]
    w.write('%-26s state=%-9s commits=%-28s newest-uncommitted-mention=%s [%d %s %s]\n     ...%s...\n' % (
        r['id'], r.get('state'), str(r.get('commits'))[:28], d, i, ph, seat, snip))
w.write('\nrows with an uncommitted/working-tree mention: %d of %d\n' % (n, len(L['rows'])))
w.flush()
