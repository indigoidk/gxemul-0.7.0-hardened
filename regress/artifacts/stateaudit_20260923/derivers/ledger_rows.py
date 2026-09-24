import json, io, sys, re
# Print the ledger rows (HEAD copy by default) whose text mentions any of the given needles:
# id, state, commits, witness, closure note head, and the entries that carry a needle (trimmed).
path = sys.argv[1]
needles = sys.argv[2:]
L = json.load(io.open(path, encoding='utf-8'))
w = io.open(sys.stdout.fileno(), 'w', encoding='utf-8', closefd=False)
for r in L['rows']:
    blob = json.dumps(r, ensure_ascii=False)
    hit = [n for n in needles if n in blob]
    if not hit:
        continue
    w.write('=' * 100 + '\n')
    w.write('ROW %s  state=%s  commits=%s\n  witness=%s\n  title=%s\n  hits=%s\n' % (
        r.get('id'), r.get('state'), r.get('commits'), str(r.get('witness'))[:200], str(r.get('title'))[:200], hit))
    cl = r.get('closure') or {}
    if cl:
        w.write('  closure.by=%s note=%s\n' % (cl.get('by'), str(cl.get('note'))[:600]))
    h = r.get('hold')
    if h:
        w.write('  hold=%s\n' % str(h)[:400])
    for i, e in enumerate(r.get('entries') or []):
        es = json.dumps(e, ensure_ascii=False)
        if any(n in es for n in needles):
            txt = e.get('text') or e.get('note') or es
            w.write('  [%d] %s %s %s: %s\n' % (i, e.get('date', ''), e.get('phase', ''), e.get('seat', ''),
                                              str(txt)[:900].replace('\n', ' ')))
w.flush()
